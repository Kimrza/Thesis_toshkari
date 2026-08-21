"""Merge per-month Madrigal coverage runs into one calendar-year evidence set.

The audit notebook runs one month per Kaggle session, so each month lands in its own
evidence folder with its own manifest and hashes. The G-P1A whole-year coverage figure
cannot be read off any one of those -- it has to be computed over the union of all of
them. This script does that and nothing else: it derives, it never re-fetches.

Input : evidence/audit_evidence_2022-MM/madrigal_coverage_raw_records.csv  (one per month),
        plus any month relocated under evidence/locked_test_restricted/ -- see CUSTODY below.
Output: evidence/locked_test_restricted/audit_evidence_2022-FULL/ with the same artifact
        contract as a single run, plus provenance fields recording that it was merged
        rather than retrieved. The output is restricted because the merged year contains
        December 2022 target values.

CUSTODY (decision D-15, 2026-08-21). Technical Environment section 12 requires locked-test
artifacts to reside under a restricted path until G-05 is complete. December 2022 target
values therefore live only under evidence/locked_test_restricted/, and this script resolves
month folders under BOTH the ordinary evidence root and the restricted root. Two properties
follow, and both are deliberate:

  * a merge that needs December will find it, so the year figure stays computable;
  * every month is reported with the root it was resolved from, so a run that silently
    picked up a restricted month is visible in the log rather than invisible.

WHAT THE RESTRICTED PATH IS AND IS NOT. It is a governance boundary, not an access control.
The directory carries no special filesystem permission, no encryption and no ACL in this
repository: anything that can read evidence/ can read evidence/locked_test_restricted/.
What it provides is (a) a single declared location, so an unintended December read is a
detectable path violation rather than an untraceable one, (b) an enforceable invariant,
asserted by tests/test_acquisition_window.py, and (c) a place where the access-log
obligation in Vision section 8.3 is unambiguous. Do not describe it as preventing access.

Two things it is careful about:

1. DEDUPLICATION. Madrigal experiments straddle UTC day boundaries, so consecutive monthly
   runs legitimately fetch the same file twice -- the 30nov22 file appears in both the
   November and December runs. Counting those rows twice would inflate record counts.
   Rows are deduplicated on (station, ut1_unix, gdlat, glon).

2. YEAR GUARD. Same rule as the notebook: rows outside the audit year are excluded from
   coverage statistics but kept in the merged raw records, so the evidence stays complete.

Usage:  python scripts/merge_coverage_year.py
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

AUDIT_YEAR = 2022
EVIDENCE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'evidence')
RESTRICTED_DIR = os.path.join(EVIDENCE_DIR, 'locked_test_restricted')
# Roots searched for per-month evidence, in precedence order. The restricted root holds
# every month carrying December 2022 target values (D-15).
EVIDENCE_ROOTS = (EVIDENCE_DIR, RESTRICTED_DIR)
# The merged year contains December, so it is written inside the restricted root.
OUT_DIR = os.path.join(RESTRICTED_DIR, 'audit_evidence_%d-FULL' % AUDIT_YEAR)

DAYS_IN_YEAR = 366 if (AUDIT_YEAR % 4 == 0 and (AUDIT_YEAR % 100 != 0 or AUDIT_YEAR % 400 == 0)) else 365
DAYS_IN_MONTH = {1: 31, 2: 29 if DAYS_IN_YEAR == 366 else 28, 3: 31, 4: 30, 5: 31, 6: 30,
                 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def month_dirs():
    """Every per-month evidence folder, in month order, across both evidence roots.

    Searches the ordinary evidence root and the restricted root (D-15). A month found in
    both roots is an ambiguity, not a preference: the run stops rather than guessing which
    copy is authoritative, because silently choosing one would make the merged year depend
    on directory-listing order.

    Ignores any previous FULL merge, and ignores superseded_* snapshots -- those are
    retained history, not run inputs.
    """
    found = {}
    origins = {}
    for root in EVIDENCE_ROOTS:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name)
            if not os.path.isdir(path) or name.endswith('-FULL'):
                continue
            if not name.startswith('audit_evidence_'):
                continue
            suffix = name.rsplit('-', 1)[-1]
            if not suffix.isdigit():
                print('SKIP (unrecognised folder name):', name)
                continue
            month = int(suffix)
            if month in found:
                sys.exit(
                    'Month %02d resolves in two roots:\n  %s\n  %s\n'
                    'Refusing to guess which copy is authoritative. Remove or rename one, '
                    'or record a decision naming the authoritative root.'
                    % (month, found[month], path)
                )
            found[month] = path
            origins[month] = 'restricted' if os.path.abspath(root) == os.path.abspath(RESTRICTED_DIR) else 'ordinary'
    for month in sorted(found):
        print('Month %02d resolved from the %s root: %s' % (month, origins[month], found[month]))
    return dict(sorted(found.items()))


def main():
    months = month_dirs()
    if not months:
        sys.exit('No per-month evidence folders found under ' + EVIDENCE_DIR)

    missing = [m for m in range(1, 13) if m not in months]
    print('Months found :', list(months))
    if missing:
        print('Months MISSING:', missing)
        print('This merge will produce a PARTIAL-year figure, not the G-P1A whole-year number.')

    # --- verify each month's own hashes before trusting its data ---------------------
    for month, path in months.items():
        hashes_path = os.path.join(path, 'sha256_manifest.json')
        if not os.path.exists(hashes_path):
            sys.exit('Month %d has no sha256_manifest.json -- refusing to merge unverified evidence.' % month)
        with open(hashes_path) as fh:
            hashes = json.load(fh)
        for name, expected in hashes.items():
            target = os.path.join(path, name)
            if not os.path.exists(target):
                sys.exit('Month %d: %s listed in hash manifest but missing on disk.' % (month, name))
            if sha256_of_file(target) != expected:
                sys.exit('Month %d: %s FAILED hash check -- evidence altered since the run.' % (month, name))
    print('All per-month hash manifests verify.')

    # --- load and deduplicate --------------------------------------------------------
    seen = set()
    merged = []
    fieldnames = None
    duplicates = 0
    per_month_source = {}

    for month, path in months.items():
        raw_path = os.path.join(path, 'madrigal_coverage_raw_records.csv')
        with open(raw_path, newline='') as fh:
            reader = csv.DictReader(fh)
            fieldnames = reader.fieldnames
            count = 0
            for row in reader:
                key = (row['station'], row['ut1_unix'], row['gdlat'], row['glon'])
                if key in seen:
                    duplicates += 1
                    continue
                seen.add(key)
                merged.append(row)
                count += 1
            per_month_source[month] = count

    print('Merged %d unique rows (%d cross-month duplicates dropped)' % (len(merged), duplicates))

    in_year = [r for r in merged if int(r['year']) == AUDIT_YEAR]
    print('Rows outside %d excluded from coverage stats: %d' % (AUDIT_YEAR, len(merged) - len(in_year)))
    if not in_year:
        sys.exit('No rows inside the audit year -- nothing to report.')

    # --- per-station whole-year summary ----------------------------------------------
    stations = sorted({r['station'] for r in in_year})
    summary = []
    monthly = {}

    for station in stations:
        srows = [r for r in in_year if r['station'] == station]
        dates = {r['date'] for r in srows}
        hours = {r['hour'] for r in srows}
        dec_dates = {r['date'] for r in srows if int(r['month']) == 12}
        summary.append({
            'station': station,
            'records_in_cell': len(srows),
            'unique_days': len(dates),
            'coverage_pct_days': round(100.0 * len(dates) / DAYS_IN_YEAR, 3),
            'unique_hourly_bins': len(hours),
            'december_days_present': len(dec_dates),
            'december_coverage_pct': round(100.0 * len(dec_dates) / 31.0, 3),
            'months_run': ','.join(str(m) for m in months),
        })
        for r in srows:
            monthly.setdefault(int(r['month']), {}).setdefault(station, set()).add(r['date'])

    for row in summary:
        if row['coverage_pct_days'] > 100.0 or row['december_coverage_pct'] > 100.0:
            sys.exit('Coverage above 100%% for %s -- dedup or year guard failed.' % row['station'])

    os.makedirs(OUT_DIR, exist_ok=True)

    summary_path = os.path.join(OUT_DIR, 'madrigal_coverage_summary.csv')
    with open(summary_path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)

    monthly_path = os.path.join(OUT_DIR, 'madrigal_coverage_monthly.csv')
    with open(monthly_path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['month'] + stations + ['days_in_month'])
        for m in sorted(monthly):
            w.writerow([m] + [len(monthly[m].get(s, ())) for s in stations] + [DAYS_IN_MONTH[m]])

    raw_path = os.path.join(OUT_DIR, 'madrigal_coverage_raw_records.csv')
    with open(raw_path, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(merged)

    # --- manifest: say plainly that this was derived, not retrieved -------------------
    source_manifests = {}
    for month, path in months.items():
        with open(os.path.join(path, 'request_manifest.json')) as fh:
            src = json.load(fh)
        source_manifests[str(month)] = {
            'folder': os.path.basename(path),
            'retrieved_at_utc': src.get('retrieved_at_utc'),
            'run_months': src.get('run_months'),
            'rows_fetched_total': src.get('rows_fetched_total'),
            'file_level_errors': len(src.get('file_level_errors', [])),
            'sha256_manifest': sha256_of_file(os.path.join(path, 'sha256_manifest.json')),
        }

    first = list(months.values())[0]
    with open(os.path.join(first, 'request_manifest.json')) as fh:
        template = json.load(fh)

    manifest = {
        'artifact_kind': 'MERGED -- derived from per-month runs, NOT a fresh retrieval',
        'merged_at_utc': datetime.now(timezone.utc).isoformat(),
        'merge_tool': 'scripts/merge_coverage_year.py',
        'audit_year': AUDIT_YEAR,
        'months_merged': list(months),
        'months_missing': missing,
        'partial_run': bool(missing),
        'rows_merged_unique': len(merged),
        'cross_month_duplicate_rows_dropped': duplicates,
        'rows_outside_audit_year_excluded': len(merged) - len(in_year),
        'rows_contributed_per_month': per_month_source,
        'source_runs': source_manifests,
        # carried unchanged from the source runs -- identical across all of them
        'madrigal_url': template.get('madrigal_url'),
        'instrument_code': template.get('instrument_code'),
        'kindat_code': template.get('kindat_code'),
        'parameters_requested': template.get('parameters_requested'),
        'stations': template.get('stations'),
        'coordinate_to_cell_convention': template.get('coordinate_to_cell_convention'),
        'user_fullname': template.get('user_fullname'),
        'user_affiliation': template.get('user_affiliation'),
    }

    manifest_path = os.path.join(OUT_DIR, 'request_manifest.json')
    with open(manifest_path, 'w') as fh:
        json.dump(manifest, fh, indent=2, default=str)

    hashes = {os.path.basename(p): sha256_of_file(p)
              for p in [summary_path, monthly_path, raw_path, manifest_path]}
    with open(os.path.join(OUT_DIR, 'sha256_manifest.json'), 'w') as fh:
        json.dump(hashes, fh, indent=2)

    print('\nWritten to', OUT_DIR)
    for row in summary:
        print('  %-5s %3d/%d days  %7.3f%%  |  December %2d/31  |  %d records'
              % (row['station'], row['unique_days'], DAYS_IN_YEAR, row['coverage_pct_days'],
                 row['december_days_present'], row['records_in_cell']))
    if missing:
        print('\nPARTIAL: months %s absent. coverage_pct_days is NOT the whole-year figure.' % missing)


if __name__ == '__main__':
    main()
