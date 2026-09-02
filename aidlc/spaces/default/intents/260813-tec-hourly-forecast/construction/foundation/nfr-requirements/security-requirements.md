# Security Requirements — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Depends on** — (dependency root)
· **Stage** `nfr-requirements`

> ## ⚠ NOTHING HERE IS CLAIMED SATISFIED
>
> **NFR-SEC-01 and TA-22 are UNCLAIMED.** So are TA-03, TA-15, TA-23 and the TE §18.3
> zero-TBD preflight. **G-09 is signed (D-31, 2026-08-28) with its own §18.3 preconditions
> UNMET** — the preflight never ran, `aws_ai_dlc_preflight_report` does not exist, and the
> ten named critical tests **cannot be executed in this environment** (no Python
> interpreter is installed). Every test named below is **written-but-unexecuted** or not
> yet written. An absence of executions is not an absence of failures.
>
> **No scientific value is decided here**, and TE §18.2's absolute rule stands: no
> implementer or coding agent may fill a `TBD — freeze gate` value by convenience.

## Sources

- `../functional-design/business-logic-model.md` — **W-8** (`resolve_platform_roots` and the credential precondition, its dated clause of 2026-08-28), **W-9** (the permitted/barred Bolt 1 boundary and the credential deny-list as a permitted item), **W-10** (December protection and the in-Kaggle obligation), **W-6** (the registry append), **W-5** (the run record), § Requirement-to-workflow map (REQ-ENG-6, FR-P1-01-10, NFR-SEC-01 → W-8 → TA-22), § Assumptions.
- `../functional-design/business-rules.md` — **R-14** (`foundation` declares credential names and never touches a value), **R-15** (only `foundation` reads `configs/`, and nothing reads the restricted root), **R-16** (no machine path enters a governed config), **R-10** (report honestly on an integrity failure), **R-13** (a release directory is never overwritten), **R-18**/**R-19**/**R-20** (the twenty-column registry row, the `AccessRecord` join, the derived `exploratory` label).
- `../../../inception/requirements-analysis/requirements.md` — **REQ-ENG-6**, **REQ-ENG-8**, **FR-P1-01-10**, **FR-P1-05-13**, **NFR-SEC-01**, **NFR-AUD-01**, **NFR-DET-01**, and § Known defects **row 13** (the NFR-SEC-01 / Madrigal-identity conflict, **no reading adopted**, owner Student + Supervisor at G-09).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§10** (credentials and secrets; the code-reuse register), **§9.1** (exactly two platforms), **§12** (repository tree), **§13.3** (release manifest), **§13.4** (the twenty-column registry), **§18.2–18.3** (forbidden choices; the preflight gate), **§19** (TA-01, TA-03, TA-10, TA-15, TA-16, TA-21, **TA-22**, TA-23).
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, Q3 = A, and the Consolidated Summary Confirmation the human receipted before this artifact was written.

---

## Scope note — why this unit has three fewer NFR artifacts

The stage's `produces_kinds` maps `performance-requirements`, `scalability-requirements`
and `reliability-requirements` to `[service]` / `[service, ui]`. `foundation` is
`kind: library`, so those three artifacts are **not produced** for this unit. The
categories were still assessed:

| Category | Assessment for `foundation` | Where it lives instead |
|---|---|---|
| **Performance** | No latency or throughput target applies. `foundation` loads configs, hashes them, seeds, records and releases; it computes no scientific quantity and serves no request. The one measurable quantity is the **environment install**, which TA-03 owns. | `tech-stack-decisions.md`; TA-03 |
| **Scalability** | No load projection applies. There are exactly two execution environments (TE §9.1) and one user. | — |
| **Reliability** | Two obligations exist and are **security-adjacent**, so they are stated in this artifact rather than dropped: registry **durability** (W-6 step 8, and Kaggle's unmeasured semantics) and release **immutability** (R-13). | § SEC-F-05, § SEC-F-06 below |
| **Security** | This artifact. | — |
| **Observability** | The run record (W-5) and the twenty-column registry (W-6) are the observability surface; NFR-AUD-01 governs them. | § SEC-F-05 |

---

## SEC-F-01 — Secret scan scope is TE §10's, not the working tree's

**Requirement.** A secret scan covering the repository **history**, **configurations**,
**logs** and **artifacts** returns clean. This is TA-22's own scope and REQ-ENG-6's and
FR-P1-01-10's acceptance criterion, stated here at full width.

**Status: NOT MET.** What exists is narrower and is recorded for exactly what it is.
Independently re-derived by `functional-design` on 2026-08-28 and carried here without
re-running it:

- `.gitignore` carries the credential deny-list at lines 62–89 — `.env`, `.env.*`,
  `*.key`, `*.pem`, `*.p12`, `*.keystore`, `kaggle.json`, `.netrc`, `_netrc`,
  `credentials`, `credentials.*`, `.aws/credentials`, `id_rsa*`, `secrets.yaml`,
  `secrets.yml`, `.madrigal_auth`.
- `git ls-files` filtered for credential-shaped names returns **0**.
- A scan of **all 1158 tracked files** for `AKIA[0-9A-Z]{16}`, PEM private-key headers,
  `xox[baprs]-`, `ghp_…` and `AIza…` returns **0 hits across 5 patterns**.

**Why that is not TA-22.** All three are `git ls-files` at **one commit**. A credential
committed and later removed is invisible to every one of them. The history,
configuration, log and artifact limbs have **not been scanned**, and no tooling for them
is selected yet.

**Acceptance.** A history-inclusive scan (tooling to be selected — `gitleaks`,
`trufflehog` or equivalent, pinned) over history, configs, logs and artifacts returns
clean, **and** § SEC-F-02's exception is resolved by the supervisor. Evidence: the scan
report plus its tool version and commit range. **Neither has happened; TA-22 remains
`Pending` and NFR-SEC-01 remains unclaimed.**

**Why the wider scope was chosen** (Q1 = A). `team.md` § Corrections records that reading
a mandated obligation as the subset an initiative happens to need is the failure
`GOV-2026-08-15-FE-01` finding `GOV-F-06` warned against, and applies that logic to TC-06
by name. Narrowing TA-22 to the working tree would have made this stage the place the
obligation quietly shrank. The cost is accepted and visible: this requirement is written
red and stays red.

**This clause will go stale.** Its durable half is the deny-list's **existence**; the
zero-hit scan is evidence as of 2026-08-28 and nothing more.

## SEC-F-02 — The acquisition identity block is a known, unresolved exception

**The conflict, stated without adopting a reading.** NFR-SEC-01 forbids stored PII. The
Madrigal rules of the road require a real identity on every request. Both are binding,
and the already-performed acquisition ran under the second:

- `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2 carries `USER_EMAIL` in **every
  commit**;
- **thirteen** committed manifests carry `user_fullname` and `user_affiliation`;
- git history is **not rewritable** without breaking the audit-trail immutability
  `team.md` affirms.

**Requirement.** The exception is **recorded**, not resolved, by this stage. Whether the
retained manifest identity fields constitute an NFR-SEC-01 breach or a mandated provider
record is the **supervisor's call** — `requirements.md` § Known defects row 13, owner
Student + Supervisor, gate G-09, recorded 2026-08-21 per `GOV-2026-08-20-RA-01`
`DATA-16`. **No reading is adopted here.**

**What is decided, and is narrower than the conflict.** REQ-ENG-6 tests **prospective**
cleanliness over the working tree; the **historical** breach is recorded with its chosen
remediation; REQ-ENG-8 migrates the identity block out of notebook source into platform
secret or environment configuration. None of the three requires choosing which obligation
yields.

**Acceptance.** The exception appears in the scan report as a named, dated allowance with
its owner and its gate — never as a clean result, and never suppressed by an
ignore-pattern that would also hide a future occurrence.

## SEC-F-03 — Credentials are provisioned per platform, resolved through one interface

**Requirement** (Q2 = A). Credentials reach the process from a **platform secret store or
environment configuration excluded from version control** (TE §10), chosen per platform:

| Platform | Mechanism |
|---|---|
| **Kaggle** | Kaggle Secrets (`UserSecretsClient`) — the platform's own store |
| **Local** | Shell environment, or a file matched by the `.gitignore` deny-list |

**One resolution interface.** Calling code **never branches on platform** to obtain a
credential. This preserves W-8's contract: `resolve_platform_roots` identifies the
platform as exactly one of `kaggle` or `local` (TC-03c; `PlatformError` otherwise) and
returns a label and roots — **no credential value is read, returned, logged, serialized,
interpolated or persisted**, there or in any foundation-layer diagnostic (R-14).

**The presence check is a separate, stage-specific precondition**, applied only by stages
that actually require authenticated provider access. It is **not** required for unrelated
stages, public providers, or `foundation` initialization itself.

**What the presence check proves, and what it does not.** It checks that required
environment-variable **names** are present and fails early naming any that are missing.
It does **not** prove a value is non-empty, valid or authorized — the provider client
performs value validation **without exposing the secret**. Stated because a presence
check mistaken for a validity check reports a readiness that does not exist.

**Accepted cost of two mechanisms.** Two provisioning paths are two ways to
misconfigure, which is why the caveat above is stated rather than assumed, and why a
missing name must fail early and by name rather than surfacing as a provider auth error.

**Open, and not this stage's to close.** The concrete `CredentialNameMap` contents await
the four governed configs existing. This stage fixes the **mechanism**; the names are
filled when `configs/` exists.

## SEC-F-04 — The restricted root is unreachable from this unit

**Requirement.** No `foundation` code path constructs a path into
`evidence/locked_test_restricted/` (R-15). Only `src/data/locked_test.py`, owned by
`governance-guards`, may reach it, and every access records `locked_test_accessed = true`
in the registry.

**Requirement.** Only `foundation` reads `configs/` (R-15). No machine-specific path
enters a governed config (R-16).

**Status.** Design-level only. `src/data/config.py`, `src/data/release.py` and
`tests/test_determinism.py` **do not exist**; BLK-01 closed 2026-08-22 granting
**authority only**, and authority to name a module is not authority to write one. The
executable guard is `tests/test_locked_test_guard.py`, which is `governance-guards`',
**written but unexecuted** — **WS-18 and TA-18 are not discharged**.

**Note on Bolt 1's boundary.** Bolt 1 performs no governed run, so the in-Kaggle
obligation does not bind it — but that obligation is a **condition on the execution
session, not a Bolt number**, and binds any Bolt that performs a governed run inside a
Kaggle session.

## SEC-F-05 — Audit integrity is a security property, not only a record

**Requirement (NFR-AUD-01, FR-P1-05-13).** The experiment registry is **append-safe and
atomic**; failed and aborted runs remain visible with **status and reason**; **no entry is
deleted, overwritten or silently re-run**. Its schema is TE §13.4's **twenty** columns,
asserted at write time (R-18): `run_id`, `started_at_utc`, `completed_at_utc`, `status`,
`code_commit`, `environment_lock_hash`, `platform`, `dataset_version`, `fold_id`,
`mask_id`, `feature_set_id`, `model_id`, `hyperparameters_json`, `seed`,
`validation_metric_name`, `validation_metric_value`, `artifact_manifest_path`,
`prediction_hash`, `locked_test_accessed`, `notes`.

**Requirement.** Registry writes **never read the run history** (R-08) — the mechanism
that makes the append safe under concurrency and the reason no row can be rewritten to
match a later belief. The status vocabulary is **closed and validated at write time**
(R-07).

**Requirement.** `exploratory` is **derived in the registry writer, never passed by a
caller** (R-20). A caller that could set it could suppress it.

**Requirement.** `AccessRecord` and `RegistryEvent` join on `run_id` with **orphan
detection both ways** (R-19). The five retrospectively logged December accesses and the
**one possible unauthorized access `GOV-2026-08-28-FD-01` Recommendation 31 records as
expressly unresolved** are reported as **known pre-guard orphans** — no registry row is
ever back-filled to clear them.

**Requirement.** On an integrity failure, report honestly **even when reporting fails**
(R-10): terminate with a message naming the file and the violated expectation, never
continue silently past a failed hash or integrity check.

**Carried dependency — Kaggle durability is unmeasured.** W-6 step 8's durability
confirmation reuses `governance-guards` R-25's accepted pattern. Platform durability
behaviour differs between the two governed platforms and **Kaggle's is characterised
nowhere in this design**. Step 8 needs its own **measured** evidence before rows written
inside a Kaggle session are relied on at a freeze gate. This is a measurement obligation
on Bolt 1's in-Kaggle work, **not an implementation choice**, and not this stage's to
measure.

**Status.** TA-10 and TA-21 are `Pending`; the registry tests are unwritten.

## SEC-F-06 — Releases are immutable, and their integrity is unverifiable today

**Requirement (TE §13.3, R-13).** A release directory is **never overwritten**. Every
immutable dataset release records version, source manifest, SHA-256 hashes, schema, row
counts, exclusions and fold/mask identifiers, and is write-protected or stored under a
**new version**. Release identity is the **content hash**; the label is **not
authoritative** (R-11).

**Requirement.** `dataset_version` is the **first 12 hex characters of `content_hash`**
with a **verify-on-write** uniqueness check — **D-29**, 2026-08-28. Injectivity is
established by that check, so the never-reuse obligation Q6 = D′ retains is no longer
open on the encoding.

**Carried dependency, and a TE §18.3 stop-and-report point.** D-29 does **not** settle
**where the existing release population that verify-on-write must read back lives, or how
it is enumerated**. The release-history ledger that would have answered it was **declined
as drafted at Amendment C** and `ReleaseLedgerEntry` withdrawn with it, so the mechanism
is **specified but not yet implementable**: `write_release` cannot perform D-29's check
without an enumeration surface. Three candidate surfaces are named at `functional-design`
§ Assumptions — a release-root directory scan, the experiment registry's release columns,
or a narrower re-proposal of the declined ledger — and **none is chosen here or there**.
Owner decision; **stage 3.5 must stop and report rather than pick one.**

**Status: TA-15 is NOT covered.** `tests/test_release_hashes.py` exists and its name
matches the mandated module, but it exercises **none** of §13.3's required manifest fields
and does **not** exercise R-13's overwrite refusal. TA-15 must not be read as covered.

## SEC-F-07 — Third-party code carries a licence record before it is used

**Requirement (TE §10.1, NFR-LIC-01, gate G-P2).** Any reused or materially adapted
third-party source is recorded in the §10.1 register **before the code is used** — with
`reuse_id`, repository URL, immutable commit or tag, upstream file and line or function,
retrieval date, licence and SPDX ID, copied-versus-adapted status, destination file,
scientific purpose, modifications, tests, original citation, notice location, reviewer and
approval date. Enforced by `tests/test_reuse_registry.py`.

**Standing default while the AGPLv3 question is open.** Third-party source whose licence
is absent, ambiguous or incompatible is **not copied or materially adapted** —
reimplement the published method from the paper with a citation instead. The AGPLv3
Global-TEC-forecasting repository is the one approved direct-copy source today, and
whether its repository-distribution obligations permit that copying is a **governance
dependency this project does not resolve on its own**.

**Status.** `src/data/reuse_registry.py` and `tests/test_reuse_registry.py` do not exist.
G-P2 is unaffected by G-09's signature.

---

## Requirement coverage

| Requirement | Section here | Workflow | Acceptance row | Status |
|---|---|---|---|---|
| REQ-ENG-6 | SEC-F-01, SEC-F-02 | W-8 | **TA-22** | `Pending` — unclaimed |
| FR-P1-01-10 | SEC-F-01, SEC-F-03 | W-8 | **TA-22** | `Pending` — unclaimed |
| NFR-SEC-01 | SEC-F-01, SEC-F-02, SEC-F-03 | W-8 | **TA-22** | **not claimed as satisfied** |
| NFR-AUD-01 | SEC-F-05 | W-6 | **TA-10, TA-21** | `Pending` |
| FR-P1-05-13 | SEC-F-05 | **W-6** | **TA-10** | `Pending` |
| FR-P1-04-11 | SEC-F-06 | W-2, W-3 | **TA-15** | `Pending` — **TA-15 NOT covered** |
| REQ-ENG-8 | SEC-F-02 (identity-block limb only) | W-9 | **TA-16** | `Pending` |
| NFR-LIC-01 | SEC-F-07 | — (cross-unit) | G-P2 | `Pending` |

**Derived and printed**: 7 requirement sections (SEC-F-01…SEC-F-07); 8 coverage rows,
because NFR-SEC-01's three sections are one row and SEC-F-04's obligations are
`governance-guards`' requirements rather than this unit's. **0** rows are claimed
satisfied.

## Assumptions & Open Questions

- **[Q1]** TA-22's stated scope is TE §10's full scope — history, configurations, logs and artifacts. The scanning **tooling** is not selected here; that is stage 3.5's choice constrained by the pinned-environment rule, and no tool is named as approved.
- **[Q2]** The credential mechanism is fixed; the concrete `CredentialNameMap` **contents** are not, and await the four governed configs existing.
- **[assumption]** Kaggle Secrets is available to this project's Kaggle sessions. TE §9.1 authorises Kaggle as a platform and TE §10 permits "platform secret stores" generically, but **no artifact states that this account has Secrets enabled**. If it does not, Q2's Kaggle limb falls back to environment configuration and the mechanism decision needs re-taking.
- **Carried, not decided here — the release population D-29's verify-on-write must read back.** Owner decision; TE §18.3 stop-and-report for stage 3.5. See SEC-F-06.
- **Carried, not decided here — the `IntegrityError` module home.** Declared in `src/data/config.py` because TE §12's `src/data/` tree names nine modules and none for exceptions, so a dedicated `src/data/exceptions.py` is a **§12 amendment this stage may not make by assertion**. The owner's decision.
- **Carried, not decided here — Kaggle's durability semantics.** See SEC-F-05.
- **Observed upstream, not corrected here.** `../functional-design/business-logic-model.md` states "module creation is authorised" in its lead G-09 box and in its `§ Assumptions` G-09 bullet, while **W-9's barred list** and the BLK-01 note state creation stays gated by G-09, TE §18.3 and stage 3.5. These are opposite conclusions in one artifact — the same self-contradiction swept out of `fixtures-and-reproducibility` on 2026-08-30. **Editing a completed stage's artifact is outside this stage's produces**, so it is reported rather than fixed. The reading this artifact takes throughout is the conservative one: **D-31 lifts G-09 as a ground for the bar; it does not authorise creating anything this unit's own workflows bar.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-08-31T00:00:00Z
**Iteration:** 1

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | `tech-stack-decisions.md` TS-07 "eight items" | The per-run environment lock is printed as an 8-bullet list, but the semicolon-joined text bundles "requirements.txt hash and a per-run pip freeze" and "Python, OS, CPU and key library versions" ambiguously — a literal semicolon-split of the sentence yields 7 clauses, not 8, depending where a reader draws item boundaries. TE §13.1 was not independently re-derived in this pass to confirm the count is exactly 8. | Re-derive the 8-item list as an explicit enumerated (not prose) list against TE §13.1 so the count is unambiguous on inspection, matching the discipline already applied to the 20-column registry and the 21-module test set. |
| 2 | Minor | `tech-stack-decisions.md` TS-04 | The Docker/container "Gate closed" classification and its stated rationale were not independently spot-checked against TE §8.3 in this pass (the grep excerpt pulled did not include that row); the rest of the prohibited-stack table was checked and matches verbatim. | Low risk given the rest of the table's fidelity, but worth a follow-up spot-check before this artifact is relied on as the sole record of that classification. |

### Verification performed

- **Scope exclusion (Critical risk, cleared):** Stage frontmatter `produces_kinds` maps `performance-requirements`→`[service, ui]`, `scalability-requirements`→`[service]`, `reliability-requirements`→`[service]`; `foundation` is `kind: library`, which is in none of those lists. The two-artifact output is correct per the stage file, not a missing-artifact defect. `security-requirements.md`'s own § "Scope note" states this accurately and assesses all five NFR categories rather than silently dropping three.
- **Undischarged-claim posture:** Grepped for satisfied/complete/passes/verified/covered language across both artifacts. Every status cell reads `Pending`, `NOT MET`, `NOT covered`, `unclaimed`, or `UNTESTED by design`; both artifacts open with an explicit "NOTHING HERE IS CLAIMED SATISFIED" / "NOTHING IS CLAIMED INSTALLED" banner naming TA-03, TA-15, TA-22, TA-23, WS-18, TA-18, `aws_ai_dlc_preflight_report`, `configs/`, the §18.3 preflight, and the no-Python-interpreter fact. No claim of discharge found anywhere in either file.
- **Freeze-gate discipline:** The TensorFlow pin is correctly left `TBD — freeze gate` (TS-02), with 2.21.0 recorded and quoted **verbatim** against TE §8.1's actual sentence (confirmed by direct read of the source file, line 437) as the named candidate, not the decision — this is the one value TE §8 leaves open and it is handled exactly as TE §18.2 requires. No other frozen value (seeds, fixture window, other pins) is presented as open; D-11's November fixture window and the D-122 seed set are referenced as already-frozen without being re-opened.
- **Fidelity to authority — spot-checks against the source PDF-derived Markdown:** TE §8.1's TensorFlow row and TE §8.3's prohibited-stack table (IRI-derived features, IRI-residual RF/LSTM, GRU, GLONASS, Galileo, Transformer/attention/BiLSTM/GNN, PyTorch, Theano, MATLAB, R, Julia, GPS-TEC/Seemala) were read directly from the authority document and compared against TS-03/TS-04. No component found moved between Required/Preferred/Conditional or Prohibited; no misquote found.
- **Counts, re-derived rather than trusted:** `security-requirements.md`'s requirement-coverage table has 8 rows (REQ-ENG-6, FR-P1-01-10, NFR-SEC-01, NFR-AUD-01, FR-P1-05-13, FR-P1-04-11, REQ-ENG-8, NFR-LIC-01) against its printed "8 coverage rows" claim — matches. `tech-stack-decisions.md`'s table likewise has 8 rows (REQ-ENG-1, -2, -3, -8, -10, -11, -12, NFR-DET-01) against its printed claim — matches. SEC-F-05's registry schema lists exactly 20 named columns against the printed "twenty" — matches. TS-06's "21 modules, not 17" claim matches `team.md` § Corrections' superseding figure (the 17-module figure in § Testing Posture is explicitly named as stale) — the artifact used the corrected figure, not the stale one.
- **Upstream defect (G-09 authorisation contradiction):** Confirmed both halves by direct grep of `business-logic-model.md`. Line 22–23 states, under the "G-09 IS SIGNED" banner, "module creation is authorised"; line 861 states "creation stays gated by G-09" as part of W-9's barred list; the two are in tension in the source artifact. Neither `security-requirements.md` nor `tech-stack-decisions.md` edits `business-logic-model.md` — both report the contradiction under "Observed upstream, not corrected here" and take the conservative reading (nothing here authorises creating a module), consistent with `project.md` § Corrections' rule against editing a completed stage's artifact and with `units-generation:c4`'s rule that an advisory finding is reported at the gate rather than applied unilaterally.
- **Q1/Q2/Q3 fidelity to the receipted answers:** SEC-F-01 correctly widens TA-22's scope to TE §10's full scope per Q1=A and states the notebook-identity exception as unresolved (SEC-F-02) rather than adopting a reading, matching the brief's stated Q1 outcome. SEC-F-03 implements the platform-appropriate, one-interface credential model per Q2=A. TS-02 implements the TBD-freeze-gate reading per Q3=A. All three match the dispatch's stated human answers.

### Coverage limits of this pass

Eight-tool-call budget was spent on: stage frontmatter, both PRIMARY artifacts in full, a targeted grep of `business-logic-model.md` for the G-09 contradiction, and a targeted grep of the TE authority document for the TensorFlow/prohibited-stack rows. Not independently re-verified in this pass: the "thirteen committed manifests carry `user_fullname`" count in SEC-F-02, the full TE §13.1 environment-lock item enumeration (finding #1 above), the Docker/container TE §8.3 row (finding #2), and the `.gitignore` line-range / zero-hit-scan figures in SEC-F-01 (all carried from a prior stage's independent re-derivation per the artifact's own citation, not fabricated here). None of these gaps rise to Critical or Major on the evidence available.

### Summary

Both artifacts are unusually disciplined for this checkpoint: the reduced two-artifact scope is correctly derived from the stage's own `produces_kinds` gating, every status cell is honestly `Pending`/unclaimed, the one open freeze-gate value (TensorFlow) is left `TBD` and quoted verbatim against its source rather than filled by convenience, derived counts check out against direct re-derivation, and the upstream G-09 authorisation contradiction is correctly reported rather than silently fixed or silently adopted. No Critical or Major finding surfaced; the two Minor findings above are follow-up hygiene, not blockers.

READY

## Review — 2026-09-01 confirming pass

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-01T00:00:00Z
**Iteration:** 1 (fresh budget after human gate rejection; artifacts unchanged since prior READY)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor | security-requirements.md, tech-stack-decisions.md coverage tables | Independently re-derived the requirement-ID set cited across both PRIMARY artifacts by grep against `requirements.md`'s full ID space: union = **16** distinct IDs (`REQ-ENG-1,6,8` + `REQ-ENG-1,2,3,8,10,11,12` from tech-stack, `FR-P1-01-10, FR-P1-04-11, FR-P1-05-13`, `NFR-AUD-01, NFR-DET-01, NFR-LIC-01, NFR-SEC-01, NFR-PHASE-01`). This matches the dispatch's own printed figure exactly — no requirement whose text these two artifacts reproduce was found cited without an ID, and no printed "7 sections / 8 rows" claim in either file (`security-requirements.md` line 267-270, `tech-stack-decisions.md` line 242-244) diverges from a direct re-derivation. No new completeness defect found this pass. |
| 2 | Minor | tech-stack-decisions.md § TS-02 | Re-verified independently: TensorFlow stays `TBD — freeze gate`, `2.21.0` is stated only as TE §8.1's named candidate quoted verbatim ("the exact compatible pin is frozen only after Kaggle/local fixture installation passes"), and no version is adopted anywhere in either artifact's coverage tables. Confirmed clean. |
| 3 | Minor | security-requirements.md § SEC-F-01, coverage row NFR-SEC-01/TA-22 | Re-verified: TA-22's scope is stated at full TE §10 width (history, configurations, logs, artifacts), the 2026-08-28 evidence is explicitly scoped as working-tree-at-one-commit only, and NFR-SEC-01/TA-22 are recorded `Pending`/**not claimed as satisfied**. Nothing softens this. The notebook identity-block exception (SEC-F-02, `REQ-ENG-8` row) remains a stated open question with no reading adopted. Confirmed clean. |
| 4 | Minor | security-requirements.md § Assumptions; tech-stack-decisions.md § Assumptions | Re-verified the G-09 contradiction report against `../functional-design/business-logic-model.md` directly (single-file spot-check on a named integration point, per read-scope carve-out): that file's own lead box still reads "module creation is authorised" (line 22-23) alongside later ⚠-annotated text asserting the conservative reading and W-9's barred list. Both PRIMARY artifacts correctly report this as an unresolved upstream contradiction, take the conservative reading throughout, and do not edit the upstream file (confirmed unmodified — the same contradictory text stands in both places). Confirmed clean. |

No Critical or Major findings. This is a confirming pass: the artifacts are unchanged since the prior READY verdict recorded above, and independent re-derivation of the highest-risk claims in the dispatch brief (coverage-ID completeness, section/row counts, TA-22 scope, the TensorFlow TBD, and the G-09 contradiction handling) reproduces the artifacts' own figures and claims without exception. No defect the prior pass missed was found.

### Validation Tool Results

No stage-declared validation tools were run (none listed for this stage); verification performed via targeted `grep`/set-reconciliation against `requirements.md` and the named upstream file, per the dispatch brief's required checks.

### Summary

Independent re-verification of the dispatch's highest-risk items — the 16-ID coverage set, the printed section/row counts, TA-22's full-scope/unclaimed status, the TensorFlow TBD, and the reported-not-fixed G-09 contradiction — confirms the artifacts as accurate and unchanged. No new Critical or Major finding surfaced.

READY
