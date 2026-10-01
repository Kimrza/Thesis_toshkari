#!/usr/bin/env bash
# scripts/archive_fixture_outputs.sh -- move a fixture run's live outputs aside before the next run.
#
# Purpose: a fixture output is written exactly once per run and never overwritten (TE 13.3), so
#   consecutive runs in one tree need the previous run's outputs moved aside first. This is the
#   procedure used by hand between P-6's A9 and A10 (suffix `.archived-<tag>`), made repeatable.
# Inputs: <fixture-root> (artifacts/walking_skeleton/<fixture_id>), <tag> (the suffix, e.g.
#   p7a11), <short> (the archived_releases/ short name suffix, e.g. p7a11).
# Re-run behaviour: moves only what exists; never deletes; refuses if a target exists. Keeps
#   measuring_result_*.json and every release except the GIM comparator's in place, as P-6 did.
set -euo pipefail
ROOT=${1:?fixture root}
TAG=${2:?archive tag}
SHORT=${3:?short tag}
cd "$ROOT"
move() {
  [ -e "$1" ] || return 0
  if [ -e "$2" ]; then echo "archive_fixture_outputs: refusing: $2 exists" >&2; exit 2; fi
  mv "$1" "$2"
}
for f in artifact_manifest.json bootstrap_summary.json checkpoint_manifest.json clean_run_log.json \
  feature_table.parquet feature_table.parquet.denial_evidence.json gim_comparator.parquet \
  hourly_vtec.parquet input_manifest.yaml iri_benchmark.parquet mask_manifest.json metrics.json \
  predictions.parquet split_manifest.json test_report.json processing_config_snapshot.yaml \
  registry_entry.json target_uncertainty_budget.json plots stage_measurements; do
  move "$f" "$f.archived-$TAG"
done
mkdir -p archived_releases
for pair in ev:evaluation ex:external fe:features mr:mask_registry pr:predictions; do
  move "${pair#*:}" "archived_releases/${pair%%:*}.$SHORT"
  if [ -e "archived_releases/${pair%%:*}.$SHORT" ]; then
    printf '%s.%s\t%s (moved aside: %s)\n' "${pair%%:*}" "$SHORT" "${pair#*:}" "$TAG" \
      >> archived_releases/ARCHIVE_NAME_MAP.tsv
  fi
done
move releases/gim_comparator_C-01_2022 "releases/gim_comparator_C-01_2022.archived-$TAG"
echo "archive_fixture_outputs: $ROOT moved aside as $TAG"
