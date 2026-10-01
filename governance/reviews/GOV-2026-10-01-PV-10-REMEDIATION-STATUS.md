# GOV-2026-10-01-PV-10 — remediation status (2026-10-01)

**Review:** `governance/reviews/GOV-2026-10-01-PV-10.md`. That report stays as written; this file records what happened to each recommendation afterwards.

**Rulings:** the Student's third rulings of 2026-10-01 (`governance/CHANGE_RECORD_2026-10-01_GOV-PV-09_rulings.md` § "Third rulings").

**Where the changes live:**
- Revision 8 text: `governance/CHANGE_RECORD_2026-09-29_platform_local_only.md` §A8 items 14–17, "Corrections", "Supervisor countersignature for revision 8", the evidence table and §R5-8 rows 38–43.
- Code commits: `42a1ca1` and `25ad0f7`.

**Board pass:** none has been run on this remediation; §R5-8 row 42 records that one is owed.

| Rec | Finding | Ruled | Status | Evidence |
|---|---|---|---|---|
| 1 | CHAIR-01: countersignature scope | Approve | **Closed** | "Supervisor countersignature for revision 8". The Supervisor's confirmation was verbal and reported by the Student, so no written artifact exists. It covers §A8 items 1–13 as they stood when it was reported. Items 14–17 and the corrections are outside it |
| 2 | Mechanism uncommitted | Approve | **Closed** | `42a1ca1` and `25ad0f7`, cited in items 9, 12, 14 and 17 |
| 3 | IMPL-12: no production caller | Ruled | **Closed** | Item 17. `run_walking_skeleton.compose_tolerances` and `compare_required_outputs` call the module. Tests `test_runtime_routes_a_cross_environment_composition_to_item11` and `test_item11_comparison_runs_through_cross_environment_tolerance` spy on the real path |
| 4 | IMPL-13: two tolerance homes | Ruled | **Closed** | Item 17. `cross_run_variation` is single-environment only and its docstring states it is not item 11. A test fails if the item-11 route reaches it |
| 5 | TEC-01: field-to-unit table | Ruled | **Closed for `plumbing_7day`; OPEN for `scientific_1month`** | Item 16. The table is declared in the identity-declaration ledger. All 680 real elements resolve (648 + 32), and a new field is refused. `scientific_1month`'s units are a Student-owned Q-31 `"TBD — freeze gate"` value that the agent may not fill |
| 6 | ML-08: infinite floor | Approve | **Closed** | Item 17. `±inf` is refused as invalid input. Tests cover `+inf`, `-inf`, a finite value against a non-finite reference, normal floors, and an infinite tolerance at the schema |
| 7 | BENCH-10: no torn faults | Ruled | **Closed** | Item 14. `campaign_kill-torn_20261001T084415Z-95cf3417` is 300/300 PASS and governed: 200 torn records produced and every one detected; receipts were old-or-new with no partials |
| 8 | BENCH-11: `/mnt/c` criterion | Ruled | **Closed: PASS** | Item 15 was fixed before the runs. `campaign_kill_20261001T084637Z-9aaebb13` and `campaign_kill-torn_20261001T085943Z-edad9609` were each 100/100 and governed |
| 9 | VAL-05: stale revision-7 wording | Ruled | **Closed** | Dated annotations beside the §A7 item 6 and D-text item 1(b) wording, plus "Corrections" |
| 10 | ML-09: "per file" | Inspected | **Closed** | "Corrections" now reads "per field" and "across fields", with an annotation beside the D-text bullet |
| 11 | IMPL-14: recording status/reason | Not ruled | **OPEN** | The module refuses. Recording the outcome in the registry is still owed by the caller |
| 12 | TEC-02: offset-dominated fields | Not ruled | **OPEN** | No such field is in the current table. The rule is not yet written |
| 13 | TEC-03: unit spelling | Not ruled | **Implemented** (pending row 42) | One literal, `TECU^2` (item 16) |
| 14 | VAL-06: `os.link` through drvfs | Not ruled | **Implemented** (pending row 42) | Item 15 property (c): 33 `after-link` trials reached `intact_new` through 9P |
| 15 | VAL-07: superseded countersignature lines | Inspected | **Closed** | Annotations beside both revision-7 lines. The adopted D-83 entry carries the §A8 item 2 line verbatim; checked at adoption |
| 16 | BENCH-14 / DATA-14: unlisted campaign | Inspected | **Closed** | `NON_GOVERNED_NOTE.md` for `ba301519`, plus a row in the evidence table. The `3820c087` note gains an appended current-status paragraph |
| 17 | BENCH-12: WSL filesystem identity | Not ruled | **Implemented** (pending row 42) | `/proc/mounts` type and options, backing volume and serial (`42a1ca1`) |
| 18 | BENCH-13: clean-commit check | Not ruled | **Implemented** (pending row 42) | Refusal of a dirty governed tree, including untracked files; CR-only differences recorded and not dirty (`42a1ca1`, `25ad0f7`) |
| 19 | CHAIR-03: adoption scope sentence | Inspected | **Closed** | "Corrections", carried into the D-83 entry |
| 20 | CHAIR-04: reference binding | Not ruled | **Implemented** (pending row 42) | On the runtime path the reference is the frozen manifest's hash-listed artifact (`compare_required_outputs`) |
| 21 | IMPL-17: exact exception types | Not ruled | **OPEN** | — |
| 22 | DATA-15: `b01_iri` as candidate | Not ruled | **Implemented** (pending row 42) | A run from `b01_iri` is refused on the item-11 comparison (`test_item11_comparison_refuses_an_environment_that_showed_no_determinism`) |
| 23 | BENCH-15: `b01_iri` interpreter | Not ruled | **Implemented** (pending row 42) | `GOVERNED_PYTHON` pin, with a negative control |
| 24 | CHAIR-06: item 24 D-number limb | Not ruled | **OPEN** | — |
| 25 | ML-11: `-0.0` disclosure | Not ruled | **OPEN** | — |
| 26 | VAL-09: custody-neutral | — | No action | — |
