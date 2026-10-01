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

## Current status (appended 2026-10-01; the text above is unchanged)

The sentence above naming `campaign_kill_20260930T170510Z-ba301519` as "the governed
campaign" was true when written and is superseded. That campaign has no clean-tree record
and is itself marked superseded and not governed (its own `NON_GOVERNED_NOTE.md`;
GOV-2026-10-01-PV-10 Recommendation 16). The governed native-NTFS kill campaign is
`campaign_kill_20260930T212721Z-8054af1f` (clean commit `f9078c4`).
