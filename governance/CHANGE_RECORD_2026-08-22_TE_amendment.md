# Vision §15.2 change record — `CR-2026-08-22-TE-AMEND`

| Field | Value |
|---|---|
| Change record ID | `CR-2026-08-22-TE-AMEND` |
| Date | 2026-08-22 |
| Approver | Kimia Rezaei, project owner, acting under the recorded student/supervisor authority equivalence |
| Governance basis | `governance/reviews/GOV-2026-08-22-REM-01.md`, Recommendations 1, 4, 5, 6 and 7 |
| Effective version | Technical Environment **v3.4**; Vision unchanged in version (§14.2 status cell only) |
| Locked test accessed | **No** — see §4 |

Vision §15.2 requires six fields of every material change. They are §1 through §6 below.

---

## 1. Requested change and reason

Six changes to authority documents, in **two distinct authority classes**. The
classes are kept separate throughout this record because conflating them would
misrepresent when each was approved and by what act.

### Class A — an already-approved historical amendment, applied late

| # | Change | Why |
|---|---|---|
| A1 | Add `tests/test_acquisition_window.py` to TE §12's tree | The amendment was **countersigned by the supervisor on 2026-08-16** (`governance/COUNTERSIGNATURE_REQUEST_2026-08-16.md` item 1) and was **never written into the Technical Environment**. Direct inspection on 2026-08-22 found zero occurrences of `test_acquisition_window` in the document while the module exists on disk and is cited by FR-P1-01-5 and FR-WS-3. TE §12's tree is exhaustive, so a repository containing the module *failed* TA-01's "matches the §12 layout item for item" test against the unamended tree. **No new approval was sought or granted for A1; only its application is new.** Raised as `REM-01` |

### Class B — new amendments expressly approved 2026-08-22

Approved by the project owner on 2026-08-22 under the recorded student/supervisor
authority equivalence. TE §18.2 classes a §12 tree amendment as a Student + Supervisor
choice; the supervisor role is exercised under the delegation documented in
`evidence/DECISIONS.md` D-1 addendum. **No supervisor signature artifact exists and none
is claimed.**

| # | Change | Why |
|---|---|---|
| B1 | Add `src/data/config.py` to TE §12 | ADR-10. Config load, per-run snapshot, hashes, determinism helper — the six-step stage entry contract every unit calls |
| B2 | Add `src/data/locked_test.py` to TE §12 | ADR-10. December path guard and access log |
| B3 | Add `tests/test_determinism.py` to TE §12 | ADR-10. Determinism coverage; TA-26's deterministic seed utility and serialization restore |
| B4 | Add `PYTHONHASHSEED=0` to TE §13.2's clean-run sequence | ADR-10. `test_clean_run.py`, WS-20 and TA-17 test the sequence **as written**, so the setting must be in the contract |
| B5 | Annotate TE §6.1 with D-16/D-17/D-19 governance | `REM-05`. §6.1's provisional minima are Phase 2-shaped; D-19 measured that `valid_observation_count >= 20` retains **zero** Phase 1 cell-hours. Applying decisions already approved 2026-08-21 |
| B6 | Clarify TE §19 TA-09's Phase 1 bound; record §13.2's phase-scoped ordinals | `REM-06`, `REM-07`. TA-09's "all 20" restated against approved FR-WS-4; the duplicate `02` ordinal recorded as phase-scoped |
| B7 | Close D-122's pending supervisor sign-off (Vision §14.2 status cell) | `REM-04`. Authority hold only; seed values unchanged and independently verified before closure |

**B5, B6 and B7 apply decisions that were already approved** (D-16, D-17, D-19 on
2026-08-21; FR-WS-4's WS-01 exception on 2026-08-21). What is new in each is the
application to the authority text, not the underlying decision. B7 is the one exception
within this group: the *authority hold* on D-122 is newly released here.

---

## 2. Alternatives

| Change | Alternatives considered | Rejected because |
|---|---|---|
| A1 | (i) Apply separately from Class B; (ii) leave the text and read §12 as "tree plus its countersigned amendments" | (i) remains the approved fallback and is **not** rejected — the instruction directs it if the combined action cannot complete. The combined action did complete, so it was unnecessary. (ii) institutionalises drift between the document and its own approved amendments, and leaves TA-01's "item for item" untestable |
| B1–B4 | (i) Four separate change records; (ii) avoid the amendment by widening existing modules | (i) four countersignatures for one coherent design decision (ADR-10 § Alternatives rejected). (ii) rejected in ADR-06 and FU-2 on the merits |
| B5 | (i) Full §15.2 replacement of the §6.1 rows; (ii) leave the text and rely on D-19's precedence | (i) destroys the provisional-versus-frozen history and implies a fresh scientific decision where none occurred. (ii) technically sound under the authority order, but leaves a value in the document an implementer reads first that would drop every Phase 1 row |
| B6 (TA-09) | Register as a separate follow-up instead | Not required: all four conditions the approval set were met — the clarification is supported by approved FR-WS-4, broadens no scope, is identified explicitly here, and creates no new acceptance policy |
| B7 | Defer to stage 3.1 alongside the seed contract | The contract work benefits from a settled seed source; the hold was pure authority with fully specified content |

---

## 3. Affected requirements, data, code, experiments, schedule and claims

**Requirements.** `REQ-ENG-4` — mandated test-module count **18 → 19**, re-derived from the
amended tree (§4 below), not carried from prose. `REQ-ENG-1`'s §12 tree reference now
resolves against the corrected tree. `FR-WS-1` and `FR-WS-4` unchanged in content;
Known defects **row 8** corrected to state FR-WS-4's 13-row Phase 1 set. Known defects
**row 12** superseded on the §15.1-versus-D-11 reading by the D-11 clarification.
`FR-P1-06-1` **not touched** — it remains the approved candidate list BLK-06 must validate.

**Data.** None. No dataset, manifest, hash, coverage figure, threshold or measured value
was created, altered or recomputed.

**Code.** None. **No module was created.** B1–B3 grant authority for three modules that do
not exist; creating them remains gated by **G-09** and by stage 3.5 `code-generation`.
`PYTHONHASHSEED` changes a documented command sequence, not any source file.

**Experiments.** None. No experiment-registry row was written, and no run occurred.

**Schedule.** BLK-01 discharged. BLK-03's seed-authority limb discharged; its contract limb
remains open to stage 3.1. BLK-02's reading limb discharged; station identity remains open.
No stage advanced: stage 2.8 `delivery-planning` remains Running and stage 3.1 was not
entered.

**Claims.** None. No scientific, performance, coverage or provenance claim is created,
strengthened or weakened. §6.1's annotation records which approved decision governs each
field and introduces no new rule.

---

## 4. Whether the locked test has been accessed

**No.** No December 2022 record was read, parsed, hashed, copied, merged or otherwise
accessed during this change or the review that produced it.
`evidence/locked_test_restricted/` was checked for directory existence only; no file
inside it was opened. **No access-log entry was created, and none was required, because no
access occurred.** No locked-month data was re-acquired and no locked-test restriction was
weakened.

D-19's measured values, cited in B5's annotation, were measured over **January–November
2022 only, December excluded by construction** — that measurement was performed on
2026-08-21 and is not a locked-test access.

---

## 5. Required regeneration or invalidation

**Nothing is invalidated and nothing requires regeneration.** No unit definition, DAG edge,
requirement assignment, acceptance-row owner, dataset, manifest or measured value changed.

Two derived counts were **re-derived rather than assumed**, each by enumerating its source
list and counting the enumeration:

| Count | Source | Method | Result |
|---|---|---|---|
| Mandated test modules | TE §12 tree, **after** amendment | listed every `test_*.py` entry in the tree, deduplicated, counted | **19** |
| Phase 1 WS acceptance rows | TE §16 + FR-WS-4 | enumerated WS-01 ∪ WS-09…WS-20 | **13** (of 20 total; 7 deferred) |

The nineteen modules, enumerated: `test_acquisition_window`, `test_bootstrap`,
`test_checkpoint_restore`, `test_clean_run`, `test_common_masks`, `test_dcb_sign`,
`test_determinism`, `test_feature_availability`, `test_hourly_target`, `test_iri_denial`,
`test_locked_test_guard`, `test_models_smoke`, `test_phase_boundary`,
`test_release_hashes`, `test_reuse_registry`, `test_rinex_schema`, `test_split_embargo`,
`test_station_registry`, `test_train_only_transforms`.

**Three of the nineteen exist on disk** (`test_acquisition_window.py`,
`test_phase_boundary.py`, `test_release_hashes.py`). The remaining sixteen are mandated and
unwritten. TA-01 may now be assessed against a correct tree; **it is not asserted to pass.**

---

## 6. Approver, date and effective version

| Item | Value |
|---|---|
| Approver | **Kimia Rezaei, project owner**, under the recorded student/supervisor authority equivalence (`evidence/DECISIONS.md` D-1 addendum) |
| Approval act | Written instruction to the governance board, 2026-08-22, approving `GOV-2026-08-22-REM-01` Recommendations 1, 2, 3 (option C), 4, 5, 6, 7 and 8 |
| Date | 2026-08-22 |
| Effective version | Technical Environment **v3.4** (§1.2 Change History row added). Vision version **unchanged** — only §14.2's D-122 status cell was edited |
| Supervisor signature | **None exists and none is claimed.** The equivalence is the documented delegation under which the TE §18.2 supervisor role is exercised. If an examining committee requires an independent supervisor signature distinct from that delegation, satisfying it is outside this repository's control |
| Independent review | **None.** The board that raised these findings also applied them. This record exists so a later reviewer can check the work rather than take it on trust |

---

## Files modified under this record

| File | Change |
|---|---|
| `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` | §1.2 v3.4 row; §12 tree +4 entries and provenance table; §6.1 annotation; §13.2 `PYTHONHASHSEED` + ordinal clarification; §19 TA-09 Phase 1 bound |
| `PreFlight/vision_document(3)(2)(2).md` | §14.2 D-122 status cell only |
| `evidence/DECISIONS.md` | D-11 clarification appended; D-11's own decision text unchanged |
| `.../requirements-analysis/requirements.md` | REQ-ENG-4 count 18 → 19; Known defects row 8 corrected |
| `.../units-generation/unit-of-work.md` | BLK-01 status; BLK-02 required resolution/authority/status; BLK-03 authority + status; BLK-04 status |
| `governance/reviews/GOV-2026-08-22-REM-01.md` | Review report persisted (new file) |
| `governance/CHANGE_RECORD_2026-08-22_TE_amendment.md` | This record (new file) |

**Deliberately not modified.** `team-practices.md` — reserved to its practices-affirmation
gate (RES-02). `requirements.md` FR-P1-06-1 — approved; BLK-06 records the tension without
editing it. Vision §14.2 rows **D-126** and **D-128**, which also read "Approved —
supervisor sign-off pending": **not in the approved scope of this record and left open.**
All prior governance reports and § Review sections — historical records. Git history.
`evidence/locked_test_restricted/**` — not opened.
