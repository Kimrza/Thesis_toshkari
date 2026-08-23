# Functional Design Questions — `acquisition`

**Unit** `acquisition` — the producer of every raw input the pipeline consumes.
**Kind** `library` · **Complexity** L · **Deployment** standalone · **Depends on**
`foundation`, `governance-guards`.

Unit **3 of 12**, and the only one that talks to a provider. It owns
`scripts/00_acquire_prepared_vtec.py`, the D-144-approved self-contained notebook
`notebooks/00_acquire_phase1_vtec.ipynb`, the `request_manifest.json` and
`sha256_manifest.json` writers, and `tests/test_acquisition_window.py` — one of the
three test modules that already exist.

**15 requirements, 7 with no §16/§19 acceptance row** — FR-P1-01-5, FR-P1-01-7,
FR-P1-01-8, FR-P1-01-9, FR-P1-01-11, REQ-NFR-A1, REQ-NFR-A2.

> **Corrected 2026-08-23 after an adversarial pass.** Superseded text, preserved: *"This
> unit carries the largest untested share in the plan."* The story map's own § Per-unit
> coverage summary contradicts it — **`acquisition` 7/15, `models-and-baselines` 7/9,
> `regimes-diagnostics-reporting` 7/11**: a **three-way tie on the raw count of 7**, and by
> *share* `acquisition` is the **smallest** of the three at 46.7%. A superlative built on a
> correct numeral, which is the failure `project.md` § Corrections records. Derived from story-map Table 1 and cross-checked
against § Per-unit coverage summary, which reads `acquisition (7)` with exactly those
IDs. It **owns** TA-32 and **supports** TA-15, TA-16, TA-22 and TA-25.

**BLK-07 is an EXIT condition on this stage.** `acquisition` may enter functional
design; it may not complete or exit without the approved routing contract, and **no
acquisition run may touch calendar 2022-12 while it stands.** Question 1 authors that
contract's *mechanism*.

**G-09 is not signed.** `scripts/00_acquire_prepared_vtec.py` does not exist; neither
does `src/`, `configs/`, nor any `src/data/locked_test.py` for this unit to call. What
*does* exist and matters here: `evidence/` with twelve months of derived audit
evidence (all pre-TC-06), `scripts/audit_ec1_drivers.py`, `scripts/merge_coverage_year.py`,
`notebooks/madrigal_phase1_coverage_audit.ipynb`, and `tests/test_acquisition_window.py`.

## Sources

- `../../../inception/units-generation/unit-of-work.md` § 3 `acquisition` — the `Owns` list, the boundary, the 15 requirements, and **BLK-07** with its full register entry.
- `../../../inception/units-generation/unit-of-work-story-map.md` — Tables 1 and 2 plus § Per-unit coverage summary. **Derived by reading the rows:** 15 requirements, **7** with no acceptance row; **owns** TA-32; **supports** TA-15, TA-16, TA-22, TA-25.
- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-13; FR-P1-00-1, -2; FR-P1-01-1 through -9 and -11; REQ-NFR-A1, REQ-NFR-A2; and FR-P1-04-11 for the release manifest this unit's manifests feed.
- `../../../inception/application-design/component-methods.md` — `src/data/locked_test.py` (`RESTRICTED_ROOT`, `AccessRecord`, `open_restricted`), `src/data/release.py` (`sha256_file`, `write_release`, `verify_release`), and the §10 credential rule.
- `../../../inception/application-design/services.md` § The nine stage scripts — `00_acquire_prepared_vtec.py`, phase **1 only**, inputs *provider API* + `configs/data.yaml`, outputs *provider files*, `request_manifest.json`, `sha256_manifest.json`; § Stage entry contract; § Execution platforms.
- `../../../inception/application-design/component-dependency.md` § Shared resources — *"nothing else may construct a path into it."*
- `../governance-guards/functional-design/business-rules.md` — **R-25** (durable log before read), **R-26** (what counts as a December hit, and the bounded driver exclusion), **R-27** (the per-artifact-class walk), **R-28** (one path in, and BLK-07 as a precondition of Bolt 3). This unit is the first consumer of all four.
- `../foundation/functional-design/` — the stage entry contract, `ConfigSnapshot`, the two-tier error posture, and credential resolution.
- `evidence/DECISIONS.md` — **D-5** (NaN at acquisition), **D-9** (the Phase 1 acquisition input), **D-10.1/.2/.3** (driver grades and lags), **D-15** (the restricted-root relocation), **D-18** (FULL's re-merge), **D-21/D-22/D-23** (the three frozen F10.7 selection choices), **D-143** (ICTP rejected), **D-144** (the approved product and notebook).
- Workspace inspection, 2026-08-23: `tests/test_acquisition_window.py`, `scripts/audit_ec1_drivers.py`, `scripts/merge_coverage_year.py`, read directly rather than described from a citation.
- Absent by scope design: `stories` (2.4 `SKIP`), `mockups` (1.6 and 2.5 `SKIP`). `kind: library`, no user-facing surface, so `frontend-components.md` is not produced.

## What this stage may and may not settle about BLK-07

BLK-07 has two limbs, and they belong to different authorities:

| Limb | Authority | Settled here? |
|---|---|---|
| **The routing mechanism** — how `acquisition` reaches anything under the restricted root | `functional-design` (3.1), per the blocker register's `Approval authority` row | **Yes — Question 1** |
| **The authorization** — which units may reach the locked month, and when | The project decision owner | **No.** Nothing in this file grants, implies or substitutes for it |

This split is not new: it is the same one recorded at `governance-guards`, whose R-28
states that the static check enforces *how many* paths exist, never *who* may use one.
**Answering Question 1 does not authorize a December read.**

---

## Question 1

BLK-07's required resolution, quoted from the register: *"A governed contract routing
**every** `acquisition` read or write under `evidence/locked_test_restricted/` through
`governance-guards.open_restricted`, so the access-log row carrying
`locked_test_accessed = true` is written **before** the first December record is read.
`acquisition` constructs no path into the restricted root directly."*

Two facts constrain the shape. `governance-guards` **R-28** now asserts, by static
check, that **no module outside `locked_test.py` contains the restricted-root
literal** — so `acquisition` cannot hold its own path string at all. And `acquisition`
is `standalone` deployment with an approved **self-contained notebook** (D-144) that
imports nothing from `src/` — so whatever the script does, the notebook cannot do it
by importing `locked_test.py`.

How does `acquisition` reach `audit_evidence_2022-FULL/`?

A) `acquisition` calls `open_restricted` directly, passing its own `AccessRecord`
   > **Impact**: The most literal reading of the register's wording, and it keeps the log row adjacent to the read that owes it. But it puts the *construction* of the sub-path in `acquisition` — it must name `audit_evidence_2022-FULL/` relative to something — and under R-28's static check the only literal it may not hold is the root itself, so this works only if `locked_test.py` also exposes the root-relative join. Leaves the notebook with no sanctioned route at all.

B) `foundation` resolves every input path, and hands `acquisition` an already-opened, already-logged path
   > **Impact**: `acquisition` names nothing under the root and needs no restricted-root awareness, which is the strongest form of "constructs no path into it". But it moves a locked-test obligation into `foundation`'s resolution layer, and `foundation` is the one unit every other unit depends on — an access-log concern there is reachable from everywhere, which is the opposite of a chokepoint.

C) `locked_test.py` exposes a **named-artifact accessor** (`open_d9_input(record)` and a re-acquisition writer), and `acquisition` calls it by name
   > **Impact**: `acquisition` holds no path fragment at all — only an artifact *name* — so R-28's static check is satisfied by construction rather than by care. The accessor owns the join, the record, and the ordering. Costs one named accessor per restricted artifact, which is the intended friction: adding a new restricted artifact becomes a visible change to `governance-guards` rather than a new string in a consumer.

D) C, plus the notebook reaching the same accessor through a **declared, tested
   notebook–script equivalence** rather than through an import
   > **Impact**: Closes the gap the other three leave. D-144 exempts the notebook from importing `src/`, so under A, B or C the notebook has *no* sanctioned route to the D-9 input and would either duplicate the path or silently go unlogged — the exact breach BLK-07 exists to prevent, arriving through the one file that is exempt from the rules. REQ-ENG-13 already requires the notebook–script equivalence test, so this reuses a mandated mechanism rather than inventing one. Costs stating explicitly that the notebook's copy of the access step is covered by that test.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. Options A and B both leave `notebooks/00_acquire_phase1_vtec.ipynb` — the file D-144 exempts from importing `src/`, and the file that actually performs acquisition — with no logged route to a restricted artifact, which makes the guard's one exempt caller its most likely breach. C is the right mechanism for the script: a named accessor satisfies R-28's static check by construction rather than by discipline. D adds the only limb that makes the contract complete, and it does so through REQ-ENG-13's already-mandated equivalence test rather than a new one. **Answering this does not authorize any December read** — it fixes how such a read would be routed if one is ever authorized.

[Answer]: D

---

## Question 2

`AccessRecord.purpose` is an approved enum with **three** values:
`"coverage_audit" | "regime_audit" | "locked_evaluation"`. Read against this unit's
two restricted operations, **none of them fits**:

1. **Reading the D-9 input** `audit_evidence_2022-FULL/` — a read of an acquisition
   artifact, not an audit and not an evaluation.
2. **Writing re-acquired December bytes** — a *write* under the root. The enum has no
   write purpose at all, and `open_restricted`'s contract is written around *"before
   the read"*.

`authorization` is likewise typed as *"the G-05 signature reference, or the audit
authority"* — and an acquisition read has neither.

What does an acquisition access record carry?

A) Reuse `"coverage_audit"` and cite the acquisition decision as the authority
   > **Impact**: No contract change, and the row is still written. But it records a false purpose: a G-05 reviewer reading the access log would see a coverage audit that never happened, and `performance_inspected = false` would be the only thing distinguishing it. The log's value is that its rows mean what they say.

B) Extend the enum with `"acquisition_read"` and `"acquisition_write"`, and widen `authorization` to name a D-number
   > **Impact**: The log stays truthful and the two operations are distinguishable in it, which matters because one is a read of an existing artifact and the other creates new December bytes. Requires amending an approved stage-2.6 contract, which is a change record rather than a design choice — but the alternative is a knowingly wrong value in a governance log.

C) B, and additionally make `open_restricted`'s write path a **separate function** with its own ordering contract
   > **Impact**: A write under the root is not the same act as a read: the ordering obligation for a write is log-before-*write*, and the failure mode is different — a partially written December artifact with no log row is worse than a blocked read. A separate entry point makes the write path's contract statable rather than borrowed. Costs a second function in `locked_test.py` and a second pair of negative controls.

D) C, plus a test asserting the enum has **exactly** the declared members, so a future value cannot be added silently
   > **Impact**: Same list-plus-completeness-test shape used three times already in `governance-guards`. It makes an enum extension a visible, failing change rather than a quiet one — and this enum is the vocabulary a G-05 reviewer reads the access log in. Costs one more test and the friction of updating it deliberately.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A is ruled out by what the log is for. B is necessary and not sufficient: the write path genuinely has a different ordering obligation and a different failure mode, and borrowing the read contract for it would leave the worse of the two failures unspecified. D's completeness test is attractive and consistent with the pattern, but this enum lives in `governance-guards`' approved contract, not in this unit — adding a test that pins a sibling unit's enum from here inverts ownership. Recommend C, with the enum-membership test raised as a note for `governance-guards` rather than built here.

[Answer]: C

---

## Question 3

FR-P1-01-2: every retrieved file records provider, permanent citation, **full provider
filename including its version suffix** (`g.002` versus `g.003`), retrieval date and
SHA-256 — and *"a mismatch against a previously recorded suffix is surfaced, never
silently accepted."*

"Surfaced" is not a behaviour. This unit's inherited posture (`team.md` § Code Style,
`foundation` R-01) is two-tier: **integrity violations terminate the run**;
**completeness shortfalls are non-fatal but must be recorded as machine-readable
fields**, never console text. A version-suffix mismatch is not obviously either one —
the provider legitimately reissues files, and a mismatch may mean the archive moved on
rather than that anything is wrong.

What happens on a suffix mismatch?

A) Terminate the run — treat it as an integrity violation
   > **Impact**: Unambiguous, and it makes silent acceptance impossible. But provider version drift is *expected* in this dataset — `g.002` versus `g.003` is already observed — so this halts a legitimate re-acquisition on a normal event, and the pressure to work around it is exactly how a guard gets disabled.

B) Record it as a machine-readable field on the manifest and continue
   > **Impact**: Matches the completeness-shortfall tier: the run finishes, the fact is in the manifest rather than in a log, and a downstream reader can act on it. But "surfaced" then means "present in a field nobody is required to read", and no gate is named that reads it.

C) B, plus the mismatch field being a **blocking input to release**: `write_release` refuses a release carrying an unresolved suffix mismatch
   > **Impact**: Keeps acquisition non-fatal where drift is normal, and puts the stop at the point where the artifact would become citable evidence. The distinction is meaningful: retrieving a reissued file is fine; *releasing* it as though it were the recorded one is not. Requires the mismatch field to be part of the release manifest's input contract, which FR-P1-04-11's fourteen fields do not currently name.

D) C, with the mismatch resolvable only by a recorded decision (a D-number) that names both suffixes
   > **Impact**: The strongest, and it matches how this project resolves every other governed disagreement. Provider drift becomes a decision with a record rather than a field someone cleared. Costs a D-number per drift event, which is real friction on a re-acquisition touching many files — and the re-acquisition is expected to touch twelve months.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A is ruled out by the observed reality of provider reissue. B satisfies the words and not the purpose. D's per-file D-number is right in principle but would generate a decision per file across a twelve-month re-acquisition, and a ritual that heavy gets batched, which defeats it. C puts the refusal exactly where the consequence is — a release is what a later reader cites — and leaves ordinary retrieval unblocked. Recommend also stating that the mismatch field must be added to the release manifest's input contract, since FR-P1-04-11's fourteen fields do not currently carry it; that is a note for stage 3.2, not a change made here.

[Answer]: C

---

## Question 4

FR-P1-01-3 requires **two** checks, and the requirement says why: *"a single string
test was satisfiable by omission."*

1. Every `request_manifest.json` carries a **non-empty** `madrigalWeb_version`, and an
   **absent** key fails exactly as `"unknown"` fails. The live case:
   `evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json`
   has no such key, because `merge_coverage_year.py` copies eight identity fields and
   drops that one.
2. A derived release **verifies** that its identity fields agree across every source
   manifest rather than asserting they do. The eight fields do agree across the twelve
   months — but nothing checked it.

Check 1 is clearly this unit's. **Check 2 is a property of a derived release**, and
`write_release` / `verify_release` live in `foundation`'s `src/data/release.py`.

Where does the identity-field agreement check live?

A) In `acquisition`, run over the source manifests before a merge
   > **Impact**: Adjacent to the code that knows what a source manifest is, and this unit owns the manifest writers. But the artifact it protects is a *release*, produced by `foundation`, and a check that lives upstream of the thing it guards can be bypassed by any other path to `write_release`.

B) In `foundation`'s `write_release`, as a precondition of writing a derived release
   > **Impact**: Guards the artifact at the moment it is created, so no caller can route around it. But it puts acquisition-specific knowledge (which eight fields are identity fields, and that they come from per-month manifests) into the shared release API, which every unit depends on.

C) B, with the identity-field set supplied by the caller as a declared parameter
   > **Impact**: The enforcement sits where it cannot be bypassed and the domain knowledge stays with the caller that has it. `write_release` asserts agreement over whatever field set it is given and refuses an empty set — so a caller cannot satisfy the check by passing nothing. Costs one parameter on an approved contract.

D) C, plus the absent-key case tested explicitly against the known-bad FULL manifest
   > **Impact**: The only option that proves the check catches the failure that actually happened, rather than a synthetic one. The FULL manifest is the real artifact with the real missing key, and it is in the workspace today. ⚠ Reading it is a **restricted-root read** and therefore owes an access-log row under Question 1's contract — so this test is unavailable until that contract exists, and it is exactly the shape of `RES-04`'s deferred rerun.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. D is the more honest test and its instinct is right — a check verified only against a synthetic fixture is weaker evidence than one verified against the artifact that produced the defect — but the FULL manifest sits under the restricted root, so building D here would either need December access this stage cannot authorize or would quietly read the root unlogged, which is the breach BLK-07 exists to prevent. Recommend C, with D recorded as an obligation that becomes available once Question 1's contract exists, and explicitly attached to `RES-04` rather than treated as new.

[Answer]: C

---

## Question 5

FR-P1-01-4: native provider byte streams are retained, and `sha256_manifest.json`
hashes **one entry per provider file**, not only the four derived artifacts. The
acceptance evidence is *"each month's manifest hash count equals its provider-file
count plus its derived-artifact count."*

**What the workspace actually holds.** Every `sha256_manifest.json` hashes exactly
**four** derived files and never the contents of `raw_isprint_cache/` — and that cache
holds isprint **text extractions**, not provider `.hdf5` bytes. **No provider byte
stream exists anywhere in the workspace.** Three of the twelve months — 2022-04,
2022-07 and 2022-12 — have no `raw_isprint_cache/` at all.

So the requirement's arithmetic cannot be satisfied for any existing month: the
provider-file count is zero. TC-06 places the test suite before further acquisition,
and `team.md` affirms the twelve existing months are **re-verified under the new
suite rather than re-acquired from scratch**.

What does the per-file hashing contract do about the twelve pre-TC-06 months?

A) Apply the contract only to newly acquired months; leave the twelve as they are
   > **Impact**: Honest about what re-verification can and cannot recover, and it avoids pretending a hash count means something it does not. But it leaves the manifest format meaning two different things depending on when a month was acquired, with nothing in the artifact saying which.

B) A, with every pre-TC-06 month's manifest carrying an explicit `provenance_class` field marking it as derived-only
   > **Impact**: Same scope, but the distinction is machine-readable and travels with the artifact instead of living in a document. A downstream consumer — G-P1A, a release, a freeze gate — can refuse a derived-only month where full provenance is required, rather than discovering the gap by reading history. Costs one field and the rule that reads it.

C) B, plus the re-verification recording the **producing interpreter**, so an out-of-envelope artifact is flagged rather than silently re-verified
   > **Impact**: Closes a second, separate gap the requirement names: `evidence/experiment_registry.md` records the 2026-08-16 corrected extracts as produced under **Python 3.14, local** — outside the 3.11 pin. Under A or B a passing hash on those files would read as evidence the envelope held. Costs recording an extra field and defining what "out of envelope" refuses.

D) C, plus a manifest-level assertion that a month marked derived-only may never be cited at a freeze gate
   > **Impact**: Turns `team.md`'s standing caveat — *"FULL must not be relied on at a freeze gate while its provenance chain points at superseded per-month hashes"* — from prose into an enforced refusal. ⚠ But the caveat's own scope moved: **D-18 re-merged FULL on 2026-08-21**, discharging the superseded-hash limb; what remains is the *provenance* limb. An assertion written against the wrong limb would refuse the wrong thing.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. The `provenance_class` field is what makes the pre-TC-06 evidence legible to every later consumer without re-litigating it, and the producing-interpreter record closes a gap the requirement states explicitly and that nothing currently catches. D is the right destination and the wrong moment: its assertion has to distinguish D-18's discharged superseded-hash limb from the still-open provenance limb, and FR-P1-01-11 already owns that distinction — writing a second, coarser version of it here would create two rules about one fact. Recommend C, with D's freeze-gate refusal recorded as belonging to FR-P1-01-11's criterion rather than to this unit's manifest writer.

[Answer]: C

---

## Question 6

D-5, extended to driver series by D-10.2: **data gaps are stored as explicit `NaN` at
acquisition time; no interpolation, smoothing or fill occurs at acquisition.**
FR-P1-01-9's acceptance criterion is *"an injected gap survives acquisition as
`NaN`"* — and FR-P1-01-9 is one of this unit's **seven requirements with no §16/§19
acceptance row**.

The difficulty is that "no fill occurred" is a negative about the whole pipeline
segment, and the obvious test — inject a gap, assert `NaN` at the output — proves only
that *this* path preserved it.

How is no-fill-at-acquisition proven?

A) The injected-gap round trip: inject, acquire, assert `NaN` at the output
   > **Impact**: Exactly what the criterion asks for, cheap, and it catches the realistic regression (someone adds a `fillna` for convenience). But it is a single positive path, and a fill introduced on a branch the fixture does not exercise passes.

B) A, plus a static assertion that no fill, interpolate, resample-with-fill or ffill call appears in this unit's modules
   > **Impact**: Covers the branches a fixture misses, and it is the same static-scan shape `governance-guards` R-24 declares subordinate-but-kept. Cheap to write. But it is a name-based check, defeated by an alias or a vectorised expression that fills without naming a fill function.

C) B, plus a NaN-count invariant carried in the manifest: gaps counted at retrieval must equal gaps present in the written artifact
   > **Impact**: A conservation law rather than a spot check — it catches a fill on any branch, including one no test exercises and one no static scan can name, because a filled gap changes the count. Machine-readable, and it lands in the manifest where a downstream consumer can assert on it. Costs counting gaps at two points and defining what counts as a gap for a driver series versus a binned product.

D) C, with the gap count broken down per series and per calendar day
   > **Impact**: Turns the invariant into a diagnostic: a per-day breakdown would have made the F10.7 outage window visible as data rather than as a suspicion, and TC-20 bars imputation until the measured gap is *recorded*. But per-day granularity across four series and a year is a large manifest addition, and most of it is never read.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C. A alone is the criterion's literal wording and the weakest thing that satisfies it; B's static limb is worth keeping but is defeated by exactly the cleverness that would motivate a fill. C's conservation invariant is the only limb that holds on branches nobody tested, and it produces a machine-readable field rather than a passing test — which matters here specifically, because FR-P1-01-9 **has no acceptance row**, so a manifest field is evidence that survives the absence of a §19 gate. D's per-day breakdown is genuinely useful for TC-20's measured-gap obligation, but that obligation belongs to FR-P1-01-7's audit report, which already exists and already carries exact dates.

[Answer]: C

---

## Question 7

REQ-ENG-13 requires that **behavioral equivalence between the notebook and
`scripts/00_acquire_prepared_vtec.py` is tested** — *"the test is scoped to that named
pair, not to acquisition logic at large."* TA-16's evidence column reads
*"notebook header declarations + acquisition-notebook/script diff."*

D-144 exempts the notebook from importing `src/`, so the pair genuinely holds two
copies of the same logic. That is the approved arrangement, and it is also exactly the
condition under which the two drift.

What is "behavioral equivalence" tested as?

A) A textual diff of the notebook's code cells against the script
   > **Impact**: What TA-16's evidence column literally names, and trivially automatable. But two implementations can be behaviourally identical and textually different — the notebook has cell structure and display calls the script does not — so this either fails constantly or is relaxed until it passes, and a relaxed diff proves nothing.

B) Run both against a fixture and assert the produced manifests and hashes are identical
   > **Impact**: Tests the thing the requirement actually names — behaviour — against the artifacts that matter, which are precisely `request_manifest.json`, `sha256_manifest.json` and the file hashes. Needs a fixture that does not hit the provider, which means a recorded provider response. Costs building that fixture.

C) B, with the shared logic extracted to a single source the notebook inlines at build time
   > **Impact**: Removes the drift rather than detecting it, which is the stronger fix. But it makes the notebook a generated artifact, and D-144 approved a *self-contained* notebook — a generated one arguably is not, and reopening D-144 is not this stage's to do.

D) B, plus a declared **equivalence scope** naming which behaviours must match (manifests, hashes, NaN handling, refusal paths) and which need not (display, progress output, cell structure)
   > **Impact**: Makes the test statable and stable: without a declared scope, "behaviourally equivalent" is renegotiated every time the test fails, which is how it ends up relaxed. The scope is also where Question 1's notebook access-step equivalence is recorded, so the two answers meet in one place. Costs writing the scope down and keeping it current.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A is the evidence column's literal wording and cannot carry the requirement's meaning. C would genuinely eliminate the drift but requires reinterpreting D-144's "self-contained", which is the owner's call and not a design decision. B is the right mechanism, and D is B with the one addition that keeps it honest over time — a declared scope is what stops a failing equivalence test from being negotiated away. D is also where Question 1's notebook limb has to be recorded, so choosing anything else leaves that limb without a home.

[Answer]: D

---

## Question 8

§10 and NFR-SEC-01: credentials and secrets are supplied through platform secret stores
or environment configuration excluded from version control, and **none may appear in a
notebook, configuration snapshot, log, registry note or committed script.**
`unit-of-work.md` § 3 states this unit's side: credentials *"reach the provider client
directly from the environment via `foundation`'s resolution — never through a config
file, log, registry note or notebook."* TA-22 is a secret-scan over tree, history,
configs, logs **and artifacts**, owned by `foundation` with this unit supporting.

The live risk is not the credential's *source* — that is settled — but its
**egress**: this unit writes manifests, logs a run record, and runs inside a notebook
whose outputs are saved.

What keeps a credential out of this unit's outputs?

A) The environment-resolution rule alone, plus TA-22's scan
   > **Impact**: The rule is already binding and the scan already covers tree, history, configs, logs and artifacts. But a scan is a detection after the fact, and its owner is `foundation` — this unit would rely on a sibling's gate to catch its own leak, discovered once the artifact already exists.

B) A, plus this unit never placing a provider response header, request URL or client repr into any manifest or log
   > **Impact**: Names the actual egress paths rather than the abstract rule — a signed URL and an auth header are the two realistic carriers, and both are things an acquisition client naturally has in hand. But it is a prohibition without a mechanism, and a prohibition nobody can check is a hope.

C) B, with a redaction boundary: every value this unit writes to a manifest, log or notebook output passes through one declared serializer that refuses unredacted credential-shaped values
   > **Impact**: One checkable chokepoint instead of a rule repeated at every write site, and it is testable directly — feed it a token-shaped value and assert it refuses. Same one-path shape as `governance-guards` R-28. Costs defining "credential-shaped" and accepting that the definition is heuristic.

D) C, plus the notebook's **outputs cleared as a precondition of commit**
   > **Impact**: Closes the one egress a serializer cannot reach: a notebook's *saved output cells*, which are committed artifacts and are exactly where §10's "never in a notebook" would be breached in practice. `notebooks/madrigal_phase1_coverage_audit.ipynb` exists in the workspace today. Costs a commit-time hook, which `team.md` § Way of Working already anticipates for the critical test set once git exists.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A leaves this unit depending on a sibling's after-the-fact scan; B states the right prohibition with nothing to enforce it; C is the mechanism and is genuinely checkable. D adds the limb that matters most here specifically: the approved acquisition *notebook* is the one artifact whose saved output is committed and whose cells hold the provider interaction, and a redaction serializer inside the process cannot reach an output cell already written to disk. `team.md` already commits this project to a pre-commit hook for the critical test set, so the mechanism has a home rather than being invented.

[Answer]: D

---

## Question 9

Seven of this unit's fifteen requirements have **no §16/§19 acceptance row**:
FR-P1-01-5, FR-P1-01-7, FR-P1-01-8, FR-P1-01-9, FR-P1-01-11, REQ-NFR-A1, REQ-NFR-A2.
Derived from story-map § Per-unit coverage summary, which reads `acquisition (7)`.
**Corrected 2026-08-23:** the first issue called this *"the largest untested share of any
unit in the plan"*, which that same table contradicts — **`acquisition` 7/15,
`models-and-baselines` 7/9, `regimes-diagnostics-reporting` 7/11**, a three-way tie on the
raw count and, by share, `acquisition` the **smallest** of the three.

Two of the seven are not untested in the ordinary sense: **FR-P1-01-5 and REQ-NFR-A2**
are both discharged by `tests/test_acquisition_window.py`, which **exists and is
green**. They lack a row, not a test. The other five lack both.

`governance-guards`' precedent, on the owner's explicit direction, was to preserve its
one untested requirement as an **explicitly untested obligation until an approved
acceptance row exists AND its test has passed** — both conditions.

What does this stage do about the seven?

A) Apply the `governance-guards` precedent unchanged to all seven
   > **Impact**: Consistent, and it keeps a single rule about what "untested" means across units. But it flattens a real distinction: two of the seven have passing tests and five have nothing, and treating them identically loses the information a reader most needs.

B) A, but split the seven into **two named classes** — *tested-without-a-row* (FR-P1-01-5, REQ-NFR-A2) and *untested-and-unrowed* (the other five)
   > **Impact**: Preserves the precedent's discipline while recording the difference that matters for closing them: the first class needs a §15.2 change record and nothing else; the second needs a test written first. Costs stating the split in every artifact that cites the count, and keeping both numbers right.

C) B, plus a candidate acceptance criterion drafted for each of the five
   > **Impact**: Turns a list of gaps into a list of proposals the owner can route through Vision §15.2 in one pass, which is how RES-01's own remediation is framed. But drafting a criterion is close to authoring a §19 row, and §19 rows are owned by stage 3.2 and the change-control process — this stage would be producing something that looks like an approved row and is not.

D) B, plus each of the five stating **what evidence would close it**, without proposing a row
   > **Impact**: Gives the owner and stage 3.2 the input they need — what a passing test would have to show — while staying inside this stage's authority. It is the same shape the residual-obligations table already uses: each row names its closure evidence rather than its acceptance criterion. Costs five short evidence statements.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option D. A loses the one distinction a reader needs. C trespasses: a drafted criterion in a functional-design artifact is indistinguishable, three months later, from an approved one, and this project has already been bitten by an artifact whose superseded text outlived its correction. D matches the residual-obligations table's existing shape — closure evidence, not criteria — and keeps the authority boundary intact while still handing stage 3.2 something it can act on. Recommend also that the two-class split be stated wherever the count "7" appears, so a later sweep keyed to the numeral does not miss the qualitative claim.

[Answer]: D

---

## Assumptions & Open Questions

- **[assumption]** Rule IDs continue the single sequence: `foundation` ran R-01…R-17 and `governance-guards` R-18…R-29, so this unit opens at **R-30**. If per-unit numbering was intended, say so at the gate and the artifacts restart.
- **[assumption]** `tests/test_acquisition_window.py` **is** this unit's, per `unit-of-work.md` § 3 `Owns`. It exists and is green, and this stage designs around it rather than proposing to rewrite it.
- **[assumption]** The `AccessRecord` enum extension in Question 2 is a change to `governance-guards`' approved stage-2.6 contract and therefore needs a change record. This stage states the requirement; it does not edit `component-methods.md`.
- **[assumption]** `write_release` and `verify_release` remain `foundation`'s. Question 4's parameterised agreement check adds a parameter to an approved contract and is likewise stated, not applied.
- **[assumption]** The re-acquisition itself is **not** in this unit's functional-design scope — it is future work this design must not block, and its December limb is barred while BLK-07 stands.
- **[assumption]** `scripts/audit_ec1_drivers.py` and `scripts/merge_coverage_year.py` migrate onto the §12 structure here and in the sibling units respectively; `audit_ec1_drivers.py:184` returning `0` regardless of missing months is a known gap against the two-tier posture, fixed at migration. This stage designs the target shape, not the migration commit.
- **Open — BLK-07 is an EXIT condition on this stage**, and Question 1 authors only its **mechanism** limb. The **authorization** limb — which units may reach the locked month, and when — is the project decision owner's, and nothing in this file grants, implies or substitutes for it.
- **Open — `RES-04`.** The documented rerun of the three existing test modules under `open_restricted` is not started and is deliberately not attempted; all three reach the restricted root by recursive traversal, and running them before the chokepoint exists would manufacture the breach. Question 4's option D is the same shape and is deferred to it.
- **Open — `RES-01`**, permitted-read access logging is NOT TESTED, owned by stage 3.2. Carried forward from `governance-guards`; this unit is a consumer of the untested contract.
- **Open — FULL's provenance is unverifiable in principle**, not merely unverified: no provider byte stream exists in the workspace, and three of the twelve months have no `raw_isprint_cache/`. D-18 discharged the **superseded-hash** limb on 2026-08-21; the **provenance** limb stands and is FR-P1-01-11's.
- **Open — two of D-144's four attached freezes remain open**, per `requirements.md` § Known defects row 5. This stage designs to D-144 as approved and does not resolve them.
- **Open — the F10.7 outage window from 2022-03-18.** No missing calendar day was observed, and the three selection choices are frozen as D-21, D-22 and D-23; the measured gap must be recorded and governed before any imputation, substitution or reconstruction. Not this stage's to decide.
- **Open — the Kyoto non-commercial-use notice and the CEDAR rules-of-the-road** must be recorded **verbatim**, not by reference, before G-P1A. Named here because this unit performs the retrieval that incurs them.
- **G-09 is not signed.** No answer here authorises creating `scripts/00_acquire_prepared_vtec.py` or any module.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant.

---

## Consolidated Summary Confirmation

Questions 1–9 are answered above as the recommended option in each case, on the
owner's instruction to apply the recommendations. Consolidated:

| Q | Answer | What it settles |
|---|--------|-----------------|
| 1 | D | **BLK-07's mechanism limb.** `locked_test.py` exposes named-artifact accessors; `acquisition` holds no path fragment, only an artifact name; the D-144 notebook reaches the same accessor through the REQ-ENG-13 equivalence test rather than an import. **Not the authorization limb** |
| 2 | C | `AccessRecord.purpose` extended with acquisition read/write values, `authorization` widened to name a D-number, and the restricted **write** path given its own function and ordering contract (log-before-write). The enum-membership test is raised as a note for `governance-guards`, not built here |
| 3 | C | A provider version-suffix mismatch is a machine-readable manifest field, non-fatal at retrieval; `write_release` **refuses** a release carrying an unresolved mismatch. The mismatch field's absence from FR-P1-04-11's fourteen fields is noted for stage 3.2 |
| 4 | C | Identity-field agreement is enforced inside `write_release` with the field set supplied as a declared parameter, and an empty set refused. Testing it against the real FULL manifest is deferred and attached to `RES-04` |
| 5 | C | The per-file hashing contract applies to newly acquired months; every pre-TC-06 month carries an explicit `provenance_class` marking it derived-only; re-verification records the **producing interpreter** so out-of-envelope artifacts are flagged. The freeze-gate refusal stays with FR-P1-01-11 |
| 6 | C | No-fill-at-acquisition proven three ways: the injected-gap round trip, a static scan for fill-class calls, and a **NaN-count conservation invariant** carried in the manifest — the last mattering most, since FR-P1-01-9 has no acceptance row |
| 7 | D | Notebook–script equivalence tested on produced manifests and hashes against a recorded-response fixture, with a **declared equivalence scope** naming what must match and what need not. Question 1's notebook access step is recorded in that scope |
| 8 | D | Credential egress closed at a single declared redaction serializer, plus notebook **outputs cleared as a precondition of commit** — the one egress a serializer cannot reach |
| 9 | D | The seven unrowed requirements split into two named classes — *tested-without-a-row* (FR-P1-01-5, REQ-NFR-A2, both green under `test_acquisition_window.py`) and *untested-and-unrowed* (the other five) — each of the five stating **what evidence would close it**, without drafting a §19 row |

**Two answers create obligations on approved stage-2.6 contracts, stated here rather
than applied.** Q2 extends `AccessRecord.purpose` and adds a restricted-write function
to `component-methods.md`'s `src/data/locked_test.py`; Q4 adds a parameter to
`src/data/release.py`'s `write_release`. Both are amendments to approved artifacts and
need change records; this stage records the requirement and edits neither file.

Carried to the gate, unchanged by these answers: **BLK-07's authorization limb is not
closed** and no acquisition run may touch calendar 2022-12; `RES-04` not started and
deliberately not attempted; `RES-01` untested and owned by stage 3.2; FULL's
provenance limb unverifiable in principle (D-18 discharged only the superseded-hash
limb); two of D-144's four attached freezes open; the F10.7 measured gap still to be
recorded before any imputation; the Kyoto and CEDAR notices to be recorded verbatim
before G-P1A; rule numbering assumed to continue at R-30; G-09 unsigned.

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

### Re-confirmation, 2026-08-23 — after a stage-wide redo jump, and one applied correction

A redo jump on `functional-design` reset the receipt floor for every unit of this stage.
No question, option or answer above changed. **One correction was applied to the artifacts
under this cleared receipt**, at the project decision owner’s explicit direction: the
FR-P1-01-6 / TA-08 row had been corrected once (primary owner) and the correction itself
introduced the opposite error, adding this unit to TA-08’s supporting list — a claim
story-map Table 2 does not make. Both superseded readings are recorded in place. A fresh
adversarial pass reviews the corrected text.

### Re-confirmation, 2026-08-23 (second) — after a second stage-wide redo jump, and one applied correction

A redo jump aimed at correcting `external-products` reset the receipt floor for every unit.
**No question, option or answer above changed.** One correction was applied to **this file**
under the cleared receipt: the **"largest untested share in the plan"** superlative, which
the story map contradicts — **`acquisition` 7/15, `models-and-baselines` 7/9,
`regimes-diagnostics-reporting` 7/11**: a three-way tie on the raw count of 7, and by share
this unit is the **smallest** of the three. Both occurrences are corrected with the
superseded text preserved.

The three artifacts had already been corrected on this point; **this file had been left
carrying the superseded claim because its confirmation receipt was locked.** The redo
cleared it.

### Re-confirmation, 2026-08-23 (third) — after a third stage-wide redo jump

**No question, option, answer or amendment on this unit changed.** The depth-policy
re-reading that prompted this redo **confirms** all three of this unit's owed amendments:
the named accessors are new symbols in a boundary block that exists and omits them, and both
the `AccessRecord.purpose` extension and `write_release`'s `identity_fields` parameter
modify existing boundary contracts. `scripts/` to `src/data` is genuinely cross-package.

### Re-confirmation, 2026-08-23 (fourth) — after a fourth stage-wide redo jump

A redo jump aimed at sweeping two **question files** that had fallen stale against their
own corrected artifacts reset the receipt floor for every unit of this stage. **No
question, option, answer or amendment on this unit changed.**

### Re-confirmation, 2026-08-23 (fifth) — after a fifth stage-wide redo jump

A redo jump aimed at correcting four stale cross-references in `target-standardization`'s
question file reset the receipt floor for every unit of this stage. **No question, option,
answer or amendment on this unit changed.**

[Answer]: Looks correct
