# Phase Boundary Verification — Construction → Operation

Intent `260813-tec-hourly-forecast`. Run 2026-09-29, after `build-and-test`
(3.6) was approved and before the first Operation stage (`performance-validation`,
4.6) produces anything.

Method: `.claude/knowledge/aidlc-shared/verification.md`. The Construction →
Operation boundary checks three things: all units built and tested, the CI
pipeline configured, and the infrastructure designed.

**Every count below was derived programmatically from the artifact and printed
before being asserted** (per `project.md` § Way of Working, count-derivation rule).

## Artifacts checked

- `../inception/units-generation/unit-of-work-dependency.md`: the unit list and each unit's `kind`.
- `../construction/<unit>/{functional-design,nfr-requirements,nfr-design,code-generation}/`: one directory per unit per per-unit stage.
- `../construction/<unit>/code-generation/code-generation-plan.md` and `code-summary.md`: the two artifacts `build-and-test` consumes.
- `../construction/build-and-test/`: the seven `build-and-test` outputs.
- `../aidlc-state.md` § Stage progress: the Construction checkboxes.

## Check 1 — All units built and tested: PASS

| Derivation | Result |
|---|---|
| `grep -cE "^    kind: library" unit-of-work-dependency.md` | **12** |
| Unit names parsed from the same file's units block | **12** |
| Units missing any of the four per-unit stage directories | **0** |
| Units missing `code-generation-plan.md` | **0** |
| Units missing `code-summary.md` | **0** |
| `build-and-test` state checkbox | `[x]`, approved 2026-09-29 |

Latest execution evidence: `build-test-results.md` § "2026-09-29 post-commit
re-run at `391a319`":
- §18.3 selection (b): 1426/1426 passed.
- Full suite: 2455 passed, 0 failed, 4 skipped, of 2459.

## Check 2 — CI pipeline configured: NOT APPLICABLE BY SCOPE, with one inconsistency surfaced

`ci-pipeline` (3.7) is `SKIP` in `research-pipeline-governed`. `team.md` §
Testing Posture (Q7=D) replaces "tests run in CI before merge" with a pre-commit
hook plus local full-suite runs, and says "No CI service is used."

**Inconsistency surfaced, not resolved here.** A GitHub Actions workflow exists at
`.github/workflows/verify.yml`. `git log --format="%h %ad" --date=short` on that path
shows **five** commits:

| Commit | Date |
|---|---|
| `b844a4d` | 2026-08-21 |
| `4cdd549` | 2026-09-20 |
| `6c96c42` | 2026-09-25 |
| `70bb651` | 2026-09-27 |
| `391a319` | 2026-09-29 (the P2 sparse-checkout change) |

*(Corrected 2026-09-29 under `GOV-2026-09-29-PV-01` Rec 15 / DQR-10. The first issue listed
three commits although it claimed every count was derived.)*
`GOV-2026-09-29-BT-03` Recommendation 14 (BENCH-03, VAL-02) named CI as a third
execution surface. The Student ruled P2, which has been applied: sparse checkout
excludes `evidence/locked_test_restricted/`. Two items are still open:
- the Supervisor countersignature on the platform authorization (Rec 47);
- observation of the new custody step on a GitHub runner.

`team.md`'s "No CI service is used" is therefore stale against the repository.
Correcting it is a memory-file write, which is allowed only through the §13
ritual. This record does not edit `team.md`.

## Check 3 — Infrastructure designed: NOT APPLICABLE BY SCOPE

`infrastructure-design` (3.4) is `SKIP`. The scope file gives the reason: "the
pipeline runs on existing local/lab compute with no new infrastructure surface."
`team.md` § Deployment fixes exactly two execution platforms, Kaggle and local
(TC-03c). No infrastructure artifact is expected.

## Carried into Operation

- All 12 units are `kind: library`. `nfr-requirements` declares
  `performance-requirements` and `scalability-requirements` only for `service`/`ui`
  kinds (`produces_kinds`), so neither exists for any unit. The same holds
  downstream for `performance-design` and `scalability-design`.
  `performance-validation` consumes all four as `required: true`, so all four are
  **absent by design**. `dashboards` is absent by scope design
  (`observability-setup` is `SKIP`). The first Operation stage has to settle what
  it validates in place of those inputs, and that question goes to the human in
  its questions file.
- Open Supervisor and Student acts that Operation cannot close:
  - Supervisor countersignatures on D-82 and on P2;
  - the `plumbing_7day` manifest promotion from `candidate` to `frozen`
    (Q-31, Student);
  - the `scientific_1month` manifest (never run, all measured fields
    `TBD — freeze gate`);
  - TC-03g Kaggle-session runs;
  - the open TEC gates. The first issue listed only G-05, G-06 and G-07. Corrected 2026-09-29
    under `GOV-2026-09-29-PV-01` Rec 15, per `project.md` approval-handoff:c1.

**Every open gate, quoted from Vision §13.1 (Gate Ownership), l.1115–1126.** None is closed.
Derivation: `grep -nE "^\| \**G-(0[1-9]|P[123])"` over the Vision, giving 12 rows.

| Gate | Approver | Required evidence (abridged; the Vision governs) | Due | Status (Vision §13.1) |
|---|---|---|---|---|
| G-01 Scientific framing | Supervisor | Sections 2, 4, 5 and decision log | Before implementation freeze | Pending sign-off |
| G-02 Station/data viability | Supervisor consulted | `station_registry_and_coverage_report`, `constellation_observable_cadence_report` | Before package freeze | Open |
| G-03 GNSS target | Supervisor | Processor trial, DCB sign, sensitivities, target uncertainty budget | Before full-year processing | Open |
| G-04 Feature safety | Supervisor for ambiguous inputs | Leakage checks, lag assertions, IRI-denial test, feature manifest | Before model tuning | Open |
| G-05 Experiment freeze | Supervisor | Signed config bundle, traceability table, December regime-count audit report | Before December access | Open |
| G-06 Locked evaluation | Student | Registry entry, prediction hash, metrics, artifact hashes | After G-05 | Blocked |
| G-07 Reproducibility | Supervisor/reviewer | `environment_and_cpu_preflight_report`, clean-run log, matched artifacts | Before thesis submission | Blocked |
| G-08 Claims | Supervisor | Claims checklist, limitations, target uncertainty budget | Before thesis submission | Blocked |
| G-09 Agent preflight | Supervisor | `aws_ai_dlc_preflight_report` | Before any affected component is coded | Open |
| G-P1 Prepared-data MVP | Supervisor | ICTP rejection evidence, replacement approval, prepared-source manifest, … MVP decision | Before the phase transition | Blocked (ICTP failed; replacement pending) |
| G-P2 Phase transition | Supervisor | Signed `phase_transition_manifest`, Phase 1 evidence package, source-reuse register | Before Phase 2 raw processing | Blocked |
| G-P3 Raw-target acceptance | Supervisor | Processor tests, two-reference matched comparison, target uncertainty budget, coverage/mask report | Before Phase 2 model training | Blocked |

These statuses are the Vision's own. Evidence produced since (for example D-number freezes)
advances some of these gates. Only the approver named above can record a gate as closed.

## Verdict

**PASS with one surfaced inconsistency (Check 2).** The inconsistency does not
block Operation, because no Operation stage configures CI. It is recorded so the
stale `team.md` line is not read as current.
