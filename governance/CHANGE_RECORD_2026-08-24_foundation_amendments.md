# CR-2026-08-24-FOUNDATION-AMENDMENTS — EXECUTED

**Status:** **EXECUTED 2026-08-24.** Sites 1–6 applied. Execution results, the derived
post-change figures and the completed sweep are recorded at the foot of this record.

**Execution authorized** by the project decision owner, 2026-08-24, after reviewing
revision 2 — *"apply what you think is best"*, the judgment delegated on a record whose
three decisions the owner had already fixed (A rejected, B approved, C reinstated).

**Revision 2, 2026-08-24.** Revision 1 proposed three amendments and a 26-site
propagation sweep. It was challenged by the project decision owner before execution;
the challenge changed two of the three outcomes, and this revision replaces it in
full.

---

## Approval status — stated precisely, because revision 1 conflated two acts

Revision 1's header read *"Approved by: the project decision owner… 'A, B and C are
approved'"* while also carrying an unchecked execution box. That was inconsistent, and
the inconsistency was the record's fault: **approval of an amendment in principle is
not authorization to execute a scope the owner has not seen.**

| Act | Status | Date |
|---|---|---|
| Amendments A, B and C approved **in principle** | Superseded by the decisions below | 2026-08-24 |
| Owner directs that the change record be reviewed before execution | Honoured — nothing executed | 2026-08-24 |
| Independent challenge of A, B and C against the approved artifacts | Complete | 2026-08-24 |
| **Amendment A — REJECTED** | Decided | 2026-08-24 |
| **Amendment B — APPROVED** | Decided | 2026-08-24 |
| **Amendment C — REINSTATED and APPROVED** on the authority of Q6=D and FU-2=D | Decided | 2026-08-24 |
| **Execution of this revised record** | **PENDING — not granted** | — |

Nothing in this record may be read as execution authority. Sites are proposed only.

---

## Amendment A — REJECTED

**Proposed:** two new §19 acceptance rows, TA-37 for REQ-ENG-7 and TA-38 for
REQ-ENG-10, via a Vision §15.2 amendment.

**Rejected 2026-08-24.** The evidence against requiring it:

- **No project rule mandates universal §19 coverage.** The requirements, all memory layers and both authority documents were searched for any rule requiring every requirement to carry an acceptance row. **No such rule exists.**
- **The approved position is the opposite.** `unit-of-work-story-map.md` dispositions the uncovered requirements as **"Open by design; enumerated per unit above"**, and `bolt-plan.md` records that the balance *"stay in the ordinary set handed to NFR requirements."* A maintained list of uncovered requirements is the project's accepted state, not a defect awaiting correction.
- **`foundation`'s functional design already satisfies both requirements** without the rows. It designs each as an enforceable obligation and specifies negative-path tests labelled *"Test specification only — not an approved acceptance row"*, claiming no coverage. That is what **Q7=X** directed.
- **TA-37 would pass vacuously.** Its subject is tags on G-05, G-06 and the phase transitions, none of which has occurred. A row that passes on an empty tag list is weaker evidence than a recorded, visible gap.
- **The cost was disproportionate**: 23 sites across four completed stages plus an authority document, and it would have widened an already-stale figure — `team.md` § Testing Posture states the checklist as *"TA-01 through TA-32"* against today's TA-36 — in the one file a sweep is forbidden to edit (`RES-02`).

**This resolves Q7=X rather than contradicting it.** Q7=X directed that a §15.2 change
request be *raised*. Amendment A was that request. The owner has now **declined** it.
Raising a request never obliged its approval.

**Consequences of the rejection — nothing changes:**

- `PreFlight/Technical_Environment…md` §19 is **not** amended. It stays at **36** rows.
- `requirements.md` is **not** edited. REQ-ENG-7 and REQ-ENG-10 keep `` `UNTESTED` ``.
- **No count propagates.** Untested stays **36**; `foundation`'s untested stays **2 of 16**; its acceptance rows stay **7**; the twelve-unit acceptance total stays **43**.
- No historical record, memory layer or audit shard is touched.

**Standing gap, recorded not closed.** REQ-ENG-7 and REQ-ENG-10 remain untested, in
the ordinary set handed forward. `foundation`'s artifacts must record Amendment A as
**raised and declined**, not as pending.

---

## Amendment B — APPROVED

**Authority class:** approved-AI-DLC-artifact annotation, under the
`GOV-2026-08-22-INC-01` Rec 7 precedent. **Not** a Vision §15.2 change — no
requirement fixes this field set (`DeterminismRecord` appears **0 times** in
`requirements.md`; NFR-DET-01 requires only *"nondeterministic ops recorded"*).

**Why it is required.** The owner's **Q3=C** answer mandates recording *"the framework
version, determinism settings, **probe scope**, and any detected **mismatches**… mark
the result as **'partial'**"*. Framework version and determinism settings already have
fields. The other three have none, so the approved contract **cannot record what the
approved answer requires**.

**Why the alternative home is unavailable.** The obvious candidate is `RunRecord` — but
its field set is fixed by **TE §13.1's eight items**, an authority document. Housing
them there would require amending TE; housing them on `DeterminismRecord` amends a
stage artifact. It is also the structurally correct home: the probe runs inside
`seed_everything`, whose only output is `DeterminismRecord`.

**The three fields, each tested for removal:**

| Field | Type | Why it cannot be dropped |
|---|---|---|
| `probe_scope` | `Sequence[str]` | Without it an empty `nondeterministic_ops` is ambiguous between "probed and found none" and "probed nothing" — which is exactly what **R-06** exists to prevent |
| `measurement_status` | `str` — `complete` \| `partial` \| `not-yet-measured` | Not derivable from scope. *"Partial"* means the framework could not give a full assessment, a fact about the framework rather than about coverage |
| `declared_vs_observed_mismatches` | `Sequence[str]` | Challenged hardest: could a mismatch be raised as an integrity finding instead of stored? **No** — W-4 step 6 says *"**record** mismatches rather than reconciling them"*. A raise terminates the run, leaving no record to carry it |

**Superseded literal:** `DeterminismRecord` has **six** fields → **nine**.

**Bounded.** B adds three fields and nothing else. No requirement, DoD, workflow or
downstream interface changes; the additions are purely additive and break no consumer.
**R-06 is unchanged** — an empty `nondeterministic_ops` is still never proof of
determinism.

---

## Amendment C — REINSTATED and APPROVED

**Revision 1 proposed rejecting C. That proposal was wrong, and the error is recorded
here rather than quietly dropped.**

Revision 1 searched `requirements.md` and the eight approved upstream artifacts for
*"ledger"*, found zero occurrences, and concluded no approved decision mandated one.
That search was incomplete: **it never checked this stage's own answered questions**,
where the owner mandated it directly.

| Answer | What it says | Effect |
|---|---|---|
| **Q6 = D** | *"Use a content-derived SHA-256 hash as the authoritative release identity **and assign a separate monotonic, human-readable release label** for review and citation."* | Requires a monotonic, human-readable label **in addition to** the hash |
| **FU-2 = D** | *"Define a separate, foundation-owned, **durable, append-only release-history ledger** for human-readable release labels and their authoritative content hashes. Keep it separate from `experiment_registry.jsonl`. Specify its approved location, ownership, schema, append-only behavior, label-allocation rules, and an independent [integrity test]."* | Mandates the ledger by name, with its location, ownership, schema, append rules and integrity test |

**The replacement revision 1 proposed was an option the owner had already declined.**
Deriving `dataset_version` from `content_hash` is **Q6 option C** — *"Content-addressed
— the version is derived from the manifest hash"* — read and rejected in favour of D,
for a stated reason: a human-readable label for citation at a gate review.

**And it is not achievable.** A **monotonic** label requires remembering what was last
allocated. That is durable state, which is what the ledger is. Q6=D entails FU-2=D;
the two are consistent with each other and inconsistent with hash-derivation.

**C is required on exactly the same logic as B**: an approved stage answer mandates
something the upstream artifacts do not express. The difference between them is only
which answer — Q3=C for B, Q6=D and FU-2=D for C.

**The authority is corrected.** Revision 1 framed C as *"a defensible engineering
choice… approved on that basis rather than compelled by a requirement."* That framing
is withdrawn. C is compelled by two approved owner answers. It remains true that no
*requirement* names a ledger and that **R-11** keeps the content hash authoritative —
the label is for citation, not identity — and both facts stay recorded.

**Superseded literal:** `services.md` § Run record and registry opens *"Q5 = C. Two
artifacts, one authoritative"* → **three artifacts**, one authoritative.

**No TE §12 amendment is required** — derived, not assumed: `artifacts/registry/` is
already an enumerated directory in the §12 tree, and the tree carries **zero
file-level entries** inside any `artifacts/` subdirectory.

**No entity-count change in `foundation`.** `ReleaseLedgerEntry` is already entity 8 of
9 in `domain-entities.md`; approving C annotates the **upstream** artifacts that lack
it. The nine-entity count stands.

---

## Execution scope — recalculated

Revision 1's 26 sites are void. Removing A eliminates every count-propagation site.
**Six sites remain.**

### Amendment B — one site

| # | File | Section | Change |
|---|---|---|---|
| 1 | `inception/application-design/component-methods.md` | § `src/data/config.py`, `class DeterminismRecord` | Add `probe_scope`, `measurement_status`, `declared_vs_observed_mismatches`. Six fields → nine, with the superseded six-field definition preserved inline |

### Amendment C — two sites

| # | File | Section | Change |
|---|---|---|---|
| 2 | `inception/application-design/services.md` | § Run record and registry, line 273 | *"Q5 = C. Two artifacts, one authoritative"* → **three artifacts**, one authoritative; add the release-history ledger with its FU-2=D properties. Superseded text preserved |
| 3 | `inception/units-generation/unit-of-work.md` | § 1 `foundation` → `Owns`, line 120 | Add the durable append-only release-history ledger beside *"the run record and `experiment_registry.jsonl` append-only writer"* |

### `foundation`'s own artifacts — three sites

| # | File | Change |
|---|---|---|
| 4 | `construction/foundation/functional-design/business-logic-model.md` | **A:** the § Assumptions bullet and W-5's box → **raised and declined**; the gap stays recorded, no coverage claimed. **B:** W-4's ⚠ box removed; the *"no output may state or imply determinism has been measured"* prohibition **lifted**, and the six-field derivation updated to nine. **C:** W-7's *"Amendment C pending"* box → approved, citing FU-2=D |
| 5 | `construction/foundation/functional-design/business-rules.md` | **A:** the REQ-ENG-7/-10 rows → **declined**; their test specifications keep the *"Test specification only — not an approved acceptance row"* label, which is now permanent rather than provisional. **B:** the six-field derivation at line 188 → nine. **C:** R-12's PENDING box → approved; the ledger-integrity acceptance row note updated |
| 6 | `construction/foundation/functional-design/domain-entities.md` | **B:** § 4 `DeterminismRecord` — three fields lose `⚠ PENDING`; header *"approved contract, plus three fields pending approval"* → nine-field approved contract; the six-field derivation updated. **C:** § 8 `ReleaseLedgerEntry` PENDING box → approved. **A:** the REQ-ENG-7 coverage row and § Assumptions bullet → declined |

### Sites that would have changed under A, and now do not

`PreFlight/Technical_Environment…md` §19 · `requirements.md` (×7) ·
`application-design/components.md` · `units-generation/unit-of-work.md` untested and
acceptance figures (×5) · `unit-of-work-story-map.md` (×4) · `bolt-plan.md` (×5) ·
`risk-and-sequencing-rationale.md` (×4) · `verification/phase-check-inception.md` (×2).
**None is touched.**

---

## Propagation sweep — planned

Two superseded literals, both narrow. Results recorded at execution; an unrecorded
sweep counts as no sweep.

| Literal | Superseded | New | Sites to sweep |
|---|---|---|---|
| `DeterminismRecord` field count | **six** | **nine** | `component-methods.md`; `foundation`'s `business-logic-model.md` (179), `business-rules.md` (188), `domain-entities.md` (157, 178) |
| Release artifacts in `services.md` | **"Two artifacts, one authoritative"** | **three artifacts** | `services.md` (273); any `foundation` restatement |

**No count is decremented by hand.** Each is re-derived from the artifact and the
command printed, per `project.md` § Way of Working.

### Report-only — never edited by a sweep

| File | Why | Disposition |
|---|---|---|
| `aidlc/spaces/default/memory/team.md` | `org.md` reserves the memory layers for the practices-affirmation gate | Its *"TA-01 through TA-32"* is stale against TA-36 — **and Amendment A's rejection means this record does not worsen it.** Reported; stays `RES-02` |
| `governance/CHANGE_RECORD_2026-08-22_*.md`, `governance/reviews/*` | Records of past acts | Reported, not edited |
| `aidlc/.../audit/*.md` | Append-only audit shards | Reported, not edited |

---

## Arithmetic check against this record's own scope

Procedure step 4 — every total must be computed over **all** of this record's
amendments.

- **A is rejected**, so it contributes no count change. Untested stays 36; acceptance stays 43; §19 stays 36 rows.
- **B** changes one field count inside one artifact: 6 → 9. It touches no cross-artifact total.
- **C** changes one artifact count inside one sentence: two → three. `foundation`'s entity count is unchanged at nine, because `ReleaseLedgerEntry` already exists in its design.
- **Therefore this record changes no shared count.** That is the material difference from revision 1, and it is why the scope fell from 26 sites to 6.

---

## What this record does NOT do

- **Creates no test coverage and no acceptance row.** REQ-ENG-7 and REQ-ENG-10 stay untested by design.
- **Authorises no module creation.** G-09 remains unsigned.
- **Decides no scientific value.** No constant, threshold, window, seed or grid.
- **Reopens nothing.** ADR-11, D-27, and BLK-02 through BLK-09 are untouched.
- **Edits no authority document.** `PreFlight/` is not modified.
- **Edits no memory layer.** `team.md`'s stale figures remain `RES-02`'s.

---

## Approval

- [x] **Project decision owner** — approved revision 2 and authorised execution of sites 1–6, 2026-08-24.

---

# Execution results — 2026-08-24

## Sites applied

| # | File | Applied | Note |
|---|---|---|---|
| 1 | `application-design/component-methods.md` | ✅ | `DeterminismRecord` +3 fields; superseded six-field definition preserved in a marked box with the authority, the alternative-home reasoning and the per-field removal test |
| 2 | `application-design/services.md` | ✅ | Third row added; *"Two artifacts"* → **three artifacts, one authoritative**; Q6=D / FU-2=D quoted as the authority; R-11's hash-authoritative rule restated |
| 3 | `units-generation/unit-of-work.md` § 1 `Owns` | ✅ | Ledger named, with its authority, the monotonicity argument and the no-§12-amendment derivation |
| 4 | `foundation/business-logic-model.md` | ✅ | W-4 box: prohibition **lifted**, six → nine. W-5 box: Amendment A **declined**, coverage permanently not claimed. W-7 box: C **approved**. § Assumptions: all three closed |
| 5 | `foundation/business-rules.md` | ✅ | R-05 box six → nine and the determinism prohibition replaced by its narrower successor; R-12 box C **approved**; the acceptance-status table's three rows updated; the *"Test specification only"* label made **permanent** |
| 6 | `foundation/domain-entities.md` | ✅ | § 4 header and field table → nine approved fields; the PENDING box **and its heading** corrected; § 8 ledger **approved** with the withdrawn-rejection reasoning recorded; coverage rows and § Assumptions updated |

**Two sites beyond the planned six**, both found by the sweep and both in
`foundation/functional-design-questions.md` — the stage's own question file, whose
Amendment A, B and C sections still read as live requests:

| # | Site | Applied | Note |
|---|---|---|---|
| 7 | § Amendment A | ✅ | Annotated **RAISED AND DECLINED**, with the reasons and the explicit statement that no count propagated. The request as raised is preserved |
| 8 | §§ Amendment B and C | ✅ | Annotated **APPLIED** / **APPROVED AND APPLIED**. C's note records that a draft of this record proposed rejecting it, why that was withdrawn, and that the proposed replacement was Q6 option C — read and declined by the owner |

## Derived post-change figures

Re-derived from the artifacts, commands printed, nothing decremented by hand:

| Figure | Command | Before | After |
|---|---|---|---|
| `DeterminismRecord` fields | `awk '/class DeterminismRecord/,/^$/' component-methods.md \| grep -cE "^ +[a-z_]+: "` | 6 | **9** |
| Release artifacts in `services.md` | read of § Run record and registry's table | 2 | **3** |

## Sweep result — every site found, with disposition

**Literal 1 — `DeterminismRecord` "six fields".** Six live sites found; **all six
corrected**: `component-methods.md` (the definition), `business-logic-model.md` W-4,
`business-rules.md` R-05, `domain-entities.md` § 4 (header, table **and** box
heading), and `functional-design-questions.md` § Amendment B. Remaining occurrences
were verified individually to sit inside *"Superseded, preserved"* quotations and are
correct survivals.

**Literal 2 — `services.md` "Two artifacts, one authoritative".** Two live sites
found; **both corrected** (`services.md` itself; `functional-design-questions.md`
§ Amendment C). The occurrences in `business-rules.md` R-12 and
`domain-entities.md` § 8 were verified to sit inside preserved-supersession
quotations.

**One defect found by the sweep that the plan had not anticipated**, and it is the
recurring class: `domain-entities.md`'s box **heading** still read *"⚠ THE LAST THREE
FIELDS DO NOT EXIST IN THE APPROVED CONTRACT"* while its body already said superseded.
A reader scanning headings would have taken the false claim. Corrected.

**One defect introduced during execution and caught before completion:** a duplicate
*"Open — `RequiredFieldsMap` and `CredentialNameMap` contents await the four
configs"* bullet was added to `business-logic-model.md` § Assumptions where the item
already existed. Removed.

## Sites that would have changed under Amendment A — confirmed untouched

Verified unmodified: `PreFlight/Technical_Environment…md` §19 (**still 36 rows**) ·
`requirements.md` (**untested still 36**; REQ-ENG-7 and REQ-ENG-10 keep
`` `UNTESTED` ``) · `application-design/components.md` · `unit-of-work.md`'s untested
and acceptance figures (**still 2 of 16 and 7**) · `unit-of-work-story-map.md` ·
`bolt-plan.md` (**acceptance total still 43**) · `risk-and-sequencing-rationale.md` ·
`verification/phase-check-inception.md`.

## Report-only files — reported, not edited

`aidlc/spaces/default/memory/team.md` (its *"TA-01 through TA-32"* remains stale
against TA-36 — **this record did not worsen it**, because Amendment A was declined;
stays `RES-02`) · `governance/CHANGE_RECORD_2026-08-22_*.md` and `governance/reviews/*`
· the audit shards · other units' `functional-design/` artifacts, verified unaffected.

## Standing consequences

- **REQ-ENG-7 and REQ-ENG-10 are untested by design, permanently.** Their negative-path test specifications remain design targets for stage 3.5 and never acceptance evidence.
- **G-09 remains unsigned.** Nothing here authorises creating a module.
- **No scientific value was decided.** No constant, threshold, window, seed or grid.
- **ADR-11, D-27 and BLK-02…BLK-09 are untouched.**
