# Non-governed campaign — sidecar note (added 2026-10-01)

This campaign (`20260930T164532Z-3820c087`, 300/300 PASS) ran under Python 3.14 on PATH,
not the governed `tec-thesis-311` interpreter (Python 3.11). Its `campaign.json` labels
`environment_id` as `tec-thesis-311`; that label is wrong. The harness took the id from
the `TEC_ENVIRONMENT_ID` variable without checking the interpreter.

Disposition: retained unaltered as evidence of what ran (nothing here is deleted or
edited). It is NOT D-83 W-6 acceptance evidence. The governed campaign is
`campaign_kill_20260930T170510Z-ba301519` (Python 3.11.16, 300/300 PASS).

Source: GOV-2026-09-30-PV-09 findings ML-03 and DATA-05. The harness now labels a run on a
non-governed interpreter `undeclared` (`_campaign_environment_id`), with a negative
control in `tests/test_durability_harness.py`.
