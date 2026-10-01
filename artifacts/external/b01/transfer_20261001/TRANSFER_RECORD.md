# B-01 transfer (b) -> (a), 2026-10-01

D-83 revision 6 R6-5 "PV-03 Rec 12 execution plan", steps 7 and 8; Student choice of
2026-10-01 "Re-run B-01 first".

- Source: WSL2 Ubuntu, environment_id `b01_iri` (rebuilt from
  environment/b01_iri-*-linux64.lock by environment/bootstrap_b01.sh), fresh --no-local
  clone at 58139fef59eab75a41b410b1aecb707a3896424a (clean tree), TEC_PLATFORM=local,
  no --code-commit (git tree present).
- Commands: --verify-runtime; --build-validation-report kaggle/b01_validation_samples.json
  (PASSED); --generate-benchmark --months 3,11 (4392 rows, 0 error rows, 1071.2 s);
  --verify-runtime again (index pins identical before and after).
- Smoke: iricore.vtec(2024-01-06T12:00, 40.286, 44.086, hbot=90, htop=2000, hstep=0.5,
  version=16) = 37.373754526924806 twice (bit-identical to the D-45 record).
- November rows: 2160, key set and iri2016_t_plus_1_tecu values bit-identical to the
  superseded legacy receipt b01_iri2016_rows_partial.jsonl (0 mismatches). March: 2232 rows.
- Transferred into artifacts/external/b01/: b01_iri2016_rows_P1A_m03_11.jsonl,
  b01_provenance_P1A_m03_11.json, b01_sha256_manifest_P1A_m03_11.json; into this
  directory: the post-run b01_runtime_identity.json and
  iri_implementation_validation_report.json. SHA-256 on both sides in
  source_sha256_in_b.txt; all equal after copy.
- The legacy receipt (b01_iri2016_rows_partial.jsonl, b01_provenance.json,
  sha256_manifest.json, and the legacy runtime identity / validation report) is left
  untouched in (a). Superseded by D-83 item 12; never consumed by default
  (scripts/04 resolve_b01_receipt).
- b_registry_rows.jsonl: the eight registry rows (4 started, 4 completed) the (b) runs
  appended in the clone, kept here verbatim so the runs stay visible (NFR-AUD-01).
