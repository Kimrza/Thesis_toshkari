"""Build revision 3 of kaggle/kaggle_iri2016_verification.ipynb from the preserved
revision-2 file, embedding iri_net_preflight.py (outer cells) and iri_index_checks.py
(inner script). Never modifies the preserved revision-2 copy."""
import hashlib
import json
import sys
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
REPO = Path.cwd()
EV = REPO / 'evidence' / 'iri2016_kaggle_verification_2026-09-19'
REV2 = EV / 'kaggle_iri2016_verification.ipynb'
OUT = REPO / 'kaggle' / 'kaggle_iri2016_verification.ipynb'
REV2_SHA = 'b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa'

rev2_bytes = REV2.read_bytes()
assert hashlib.sha256(rev2_bytes).hexdigest() == REV2_SHA, 'preserved revision-2 copy does not hash as expected'
nb = json.loads(rev2_bytes.decode('utf-8'))
cells = nb['cells']
assert len(cells) == 17

net_src = (SCRATCH / 'iri_net_preflight.py').read_text(encoding='utf-8')
idx_src = (SCRATCH / 'iri_index_checks.py').read_text(encoding='utf-8')
assert "'''" not in idx_src and "'''" not in net_src


def src(i):
    return ''.join(cells[i]['source'])


def set_src(i, text):
    cells[i]['source'] = text.splitlines(keepends=True)


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(keepends=True)}


def code(text):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
            'source': text.splitlines(keepends=True)}


# --- cell 0: intro ------------------------------------------------------------------
intro = src(0)
rev_note = '''# IRI-2016 Kaggle Verification (Diagnostic Only) — revision 3

> **Revision 3 (2026-09-19) — NOT yet executed on Kaggle.** The successful Kaggle run of
> 2026-09-19 (bundle `iri_verification_bundle.zip`, SHA-256 `3a0723a1…`) was produced by
> **revision 2**, SHA-256 `b8399c98f248749fca3b6e5acebec9543c262ec0cc83dde2dab0042460d564fa`,
> preserved unchanged at `evidence/iri2016_kaggle_verification_2026-09-19/`. Nothing in
> that evidence is attributable to this file. Revision 3 adds, without changing the
> smoke test or the pins: a bounded **network preflight** before any install (Step 1b),
> a closed-set **failure classification** on every failed command, and full
> **`ig_rz.dat` / `apf107.dat` metadata, coverage and 2022-support checks** in the inner
> script (Step 4). It still writes the diagnostic bundle on every stop.

'''
assert intro.startswith('# IRI-2016 Kaggle Verification (Diagnostic Only)\n')
intro = intro.replace('# IRI-2016 Kaggle Verification (Diagnostic Only)\n', rev_note, 1)
old_env = ('- If Kaggle\'s own Python is not exactly 3.10, this notebook creates an **isolated `venv`** at Python 3.10 (via `apt-get install python3.10` if the kernel image does not already have it)')
assert old_env in intro
intro = intro.replace(old_env, '- If Kaggle\'s own Python is not exactly 3.10, this notebook creates an **isolated environment** at Python 3.10 (revision 2 established on Kaggle that `virtualenv` against the image\'s own `/usr/bin/python3.10` works; `uv`-managed CPython 3.10 and `apt-get` remain as fallbacks)')
set_src(0, intro)

# --- cell 1: helpers: report fields + failure classification in run() -----------------
c1 = src(1)
c1 = c1.replace("report = {\n    'notebook': 'kaggle_iri2016_verification.ipynb',\n",
                "report = {\n    'notebook': 'kaggle_iri2016_verification.ipynb',\n    'notebook_revision': 3,\n"
                "    'note': 'revision 3 has NOT produced the 2026-09-19 evidence bundle; that was revision 2 (sha256 b8399c98...)',\n", 1)
assert "'notebook_revision': 3" in c1
c1 = c1.replace("    entry.update({'returncode': rc, 'stdout_tail': out[-4000:], 'stderr_tail': err[-4000:]})\n",
                "    entry.update({'returncode': rc, 'stdout_tail': out[-4000:], 'stderr_tail': err[-4000:]})\n"
                "    if rc != 0 or entry['timed_out']:\n"
                "        # closed-set class (dns_failure / tls_failure / hash_mismatch / ...) so a reader\n"
                "        # can tell failure kinds apart without the raw log; defined in Step 1b's cell\n"
                "        entry['failure_class'] = classify_command_failure(err, out, rc, entry['timed_out'])\n", 1)
assert "entry['failure_class']" in c1
set_src(1, c1)

# --- new Step 1b cells after the runtime cell (index 3) -------------------------------
step1b_md = md('''## Step 1b — Bounded network preflight (before anything is installed)

Every install path below needs `pypi.org` (index) and `files.pythonhosted.org` (wheels).
This cell probes both, stage by stage — **DNS → TCP → TLS → HTTPS** — each stage under a
10 s timeout, and stops the notebook at the first failing stage with the stage named,
the exception text, and the **possible** causes. Runs 2 and 3 of revision 2 spent three
failed rungs and a 240 s `apt-get` timeout discovering what this cell reports in seconds.
The probe cannot see Kaggle's settings panel, so it never asserts that the Internet
setting is OFF; it lists that as one possible cause of a DNS failure, to check first.
The same cell defines `classify_command_failure`, used by `run()` on every failed command.
''')
step1b_code = code(net_src + '''

report['network_preflight'] = network_preflight(timeout=10.0)
print(json.dumps(report['network_preflight'], indent=2, default=str))
write_bundle()
if not report['network_preflight']['ok']:
    npf = report['network_preflight']
    save_and_stop(
        f"network preflight failed before any install: host {npf['failed_host']!r}, stage "
        f"{npf['failed_stage']!r}, class {npf['failure_class']!r}: {npf['error']}. "
        f"{npf['possible_causes']}. Nothing was installed; see report['network_preflight'] "
        f"for every stage's outcome and timing."
    )
''')
cells[4:4] = [step1b_md, step1b_code]
# indices shift by +2 from here: old 4->6, 5->7, 6->8, 7->9, 8->10, 9->11, 10->12, 11->13, 12->14, 13->15, 14->16, 15->17, 16->18

# --- Step 3 markdown (old 6, now 8): third-revision paragraph -------------------------
c8 = src(8)
assert c8.startswith('## Step 3')
c8 += '''
**Third revision (after the fourth Kaggle run — a PASS — 2026-09-19).** Rung 1 (`virtualenv`
against the image's `/usr/bin/python3.10`, Python 3.10.12) succeeded on Kaggle with Internet
ON; the two earlier stops of this step were network failures at the very first `pip
install`, now caught by Step 1b before this step runs. The ladder is unchanged. What is new:
every failed attempt carries a `failure_class`, and the stop message names it per rung.
'''
set_src(8, c8)

# --- rung cell (old 7, now 9): include failure_class in the stop summary --------------
c9 = src(9)
old_sum = ('        f"  - {e[\'attempt\']}: exit={e[\'returncode\']} timed_out={e.get(\'timed_out\')} "\n'
           '        f"stderr_tail={(e.get(\'stderr_tail\') or e.get(\'stdout_tail\') or \'\')[-400:].strip()!r}"\n')
assert old_sum in c9
c9 = c9.replace(old_sum,
                '        f"  - {e[\'attempt\']}: exit={e[\'returncode\']} timed_out={e.get(\'timed_out\')} "\n'
                '        f"class={e.get(\'failure_class\', \'none\')} "\n'
                '        f"stderr_tail={(e.get(\'stderr_tail\') or e.get(\'stdout_tail\') or \'\')[-400:].strip()!r}"\n')
set_src(9, c9)

# --- pip install cell (old 8, now 10): classified stop message ------------------------
c10 = src(10)
old_stop = ("    save_and_stop(\n        'pip install --require-hashes failed inside the isolated venv (see report[\"installation\"][\"pip_install\"] for the full captured stdout/stderr and the actual exit code); the most likely cause on Kaggle is a manylinux platform tag mismatch (iricore 1.8.0 requires manylinux_2_35, i.e. a fairly recent glibc) -- this is reported exactly, never silently retried with a different version.'\n    )")
assert old_stop in c10
c10 = c10.replace(old_stop,
                  "    save_and_stop(\n"
                  "        f'pip install --require-hashes failed inside the isolated venv: failure_class='\n"
                  "        f'{pip_log.get(\"failure_class\")!r} (dns_failure / tls_failure / connection_failure = network; '\n"
                  "        f'hash_mismatch = downloaded bytes differ from the pinned SHA-256; platform_tag_mismatch = '\n"
                  "        f'the manylinux_2_35 wheel is refused by this glibc; resolution_failure = no matching file). '\n"
                  "        f'See report[\"installation\"][\"pip_install\"] for the captured stdout/stderr and exit code -- '\n"
                  "        f'reported exactly, never silently retried with a different version.'\n    )")
set_src(10, c10)

# --- Step 4 markdown (old 10, now 12) -------------------------------------------------
c12 = src(12)
assert c12.startswith('## Step 4')
c12 += '''
**Revision 3 addition.** After hashing the two index files the inner script parses both
exactly as the compiled Fortran does (`readapf107` format `(3I3,9I3,I3,3F5.1)`;
`read_ig_rz` header + `3-imst+(iyend-iyst)*12+imend` values; `tcon` month indexing) and
records: `apf107.dat` first/last date, row count, contiguity; `ig_rz.dat` update date
(the file's month-day-year header), declared range, value count; and, for **every 2022
target time**, whether the rows/months IRI-2016 reads (`APF` back to UT−39 h, `APF_ONLY`
previous day, `tcon` previous/next month) are present, non-negative, and whether the
centered 81-/365-day and 12-month windows behind them lie inside the file — the
2022 rows' centered columns are recomputed from the same file's daily column as a check.
It reads and reports; it never refreshes or replaces the files.
'''
set_src(12, c12)

# --- inner script (old 11, now 13) ----------------------------------------------------
c13 = src(13)
head = 'OUT = {"ok": False}\n'
assert c13.count(head) == 1
c13 = c13.replace(head, '# ---- embedded verbatim from iri_index_checks.py (same code as the local checks) ----\n'
                  + idx_src + '\n# ---- end of embedded module ----\n\n' + head, 1)
anchor2 = '''    hashes_before = {"apf107.dat": sha256_of(apf107), "ig_rz.dat": sha256_of(ig_rz)}
    OUT["index_files"] = {"directory": str(index_dir), "sha256_before": hashes_before}
'''
assert c13.count(anchor2) == 1
c13 = c13.replace(anchor2, anchor2 + '''
    # --- 2b. metadata, coverage and 2022 support of both files (read-only; D-45) -------
    OUT["_stage"] = "parse_index_metadata_and_2022_support"
    apf_rows = parse_apf107(apf107.read_text(encoding="ascii", errors="strict"))
    ig_parsed = parse_ig_rz(ig_rz.read_text(encoding="ascii", errors="strict"))
    OUT["index_files"]["apf107"] = {
        "summary": apf107_summary(apf_rows),
        "support_2022": apf107_support_check(apf_rows, year=2022),
    }
    ig_slim = {k: v for k, v in ig_parsed.items() if k not in ("months", "ig12", "rz12")}
    OUT["index_files"]["ig_rz"] = {
        "summary": ig_slim,
        "support_2022": ig_rz_support_check(ig_parsed, year=2022),
    }
''', 1)
# cross-check the revision-2 smoke-date regex against the parser's last date
anchor3 = '    last_date = dt.date(last_year, mm, dd)\n'
assert c13.count(anchor3) == 1
c13 = c13.replace(anchor3, anchor3 + '''    if last_date != apf_rows[-1]["date"]:
        raise RuntimeError(
            f"last-line regex date {last_date} != fixed-format parser last date {apf_rows[-1]['date']}"
        )
''', 1)
set_src(13, c13)

# --- reconciliation cell (old 14, now 16) ---------------------------------------------
c16 = src(16)
assert c16.startswith("assert verification['reconciliation']")
c16 = c16.replace("print('Reconciliation checks passed",
                  "assert verification['index_files']['apf107']['support_2022']['ok'], (\n"
                  "    'apf107.dat does not carry every row / window a 2022 target time needs -- see '\n"
                  "    'verification[\"index_files\"][\"apf107\"][\"support_2022\"]'\n)\n"
                  "assert verification['index_files']['ig_rz']['support_2022']['ok'], (\n"
                  "    'ig_rz.dat does not cover every month / window a 2022 target time needs -- see '\n"
                  "    'verification[\"index_files\"][\"ig_rz\"][\"support_2022\"]'\n)\n"
                  "print('Index-file metadata:', json.dumps({\n"
                  "    'apf107': verification['index_files']['apf107']['summary'],\n"
                  "    'ig_rz': verification['index_files']['ig_rz']['summary']}, indent=2, default=str))\n"
                  "print('Reconciliation checks passed", 1)
assert "support_2022" in c16
set_src(16, c16)

assert len(cells) == 19
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('written', OUT, 'sha256', hashlib.sha256(OUT.read_bytes()).hexdigest(), 'cells', len(cells))
