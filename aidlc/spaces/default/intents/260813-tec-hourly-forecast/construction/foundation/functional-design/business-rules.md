# Business Rules — `foundation`

> ## ✳ G-09 IS SIGNED — 2026-08-28, **D-31** (read this before any G-09 statement below)
>
> The project decision owner **signed and approved G-09 (Agent preflight)** on 2026-08-28,
> recorded as **D-31** in `evidence/DECISIONS.md` with change record
> `governance/CHANGE_RECORD_2026-08-28_G09_signed.md`. **Every statement below of the form
> "G-09 is not signed" / "G-09 stays unsigned" is superseded as to the gate's status**, and
> is left standing as the accurate record of the constraint that applied when it was
> written.
>
> ⚠ **D-31 records the gate's own TE §18.3 preconditions as UNMET, and that disclosure
> travels with the signature.** `configs/`, and until 2026-08-28 `src/`, did not exist, so
> the mandated automated zero-TBD preflight **could not run**; the ten named critical tests
> **cannot be executed in this environment** (no Python interpreter is installed — a
> zero-byte Windows Store stub, no registry entry, no interpreter on disk); and the evidence
> artifact `aws_ai_dlc_preflight_report` **does not exist**. "No failing critical test" is
> therefore **unproven, not proven** — an absence of executions, not an absence of failures.
> This is the owner **opening the gate by authority**, not a record that its evidentiary
> conditions were satisfied, and no reader may infer the second from the first.
>
> **What the signature changes here:** module creation is authorised, and any defect this
> unit deferred *solely* because G-09 barred editing a file is now correctable.
> **What it does NOT change:** G-05 and G-06 remain `Blocked`; G-P1A, G-P2, G-P3A, G-P3C
> and G-07 are unaffected; **TE §18.2's absolute rule stands** — every scientific value this
> unit routed to G-04/G-05 **stays routed**, and no agent may fill a freeze-gate value by
> convenience; and **§18.3's stop-and-report obligation survives its own gate**, being a
> standing rule on implementation rather than a one-time gate condition.

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Depends on** — (dependency root)

> ## ⛔ D-29 RULES THE `dataset_version` ENCODING — 2026-08-28 (read this before any encoding statement below, INCLUDING R-12's own Rule statement)
>
> *(Banner added 2026-08-30, after two adversarial iterations found the D-29 correction had landed
> in `§ Assumptions` while **R-12's own Rule statement 37 lines above its AMENDED box** still read
> that the encoding is "NOT specified here". Modelled on the G-09 banner above. Superseded text is
> left standing everywhere, never deleted.)*
>
> **D-29 (2026-08-28) fixes the encoding**: `dataset_version` is the **first 12 hex characters of
> `content_hash`**, with a **verify-on-write** uniqueness check. **Every statement below of the
> form "the encoding is unspecified / NOT specified here / still unruled / no approved artifact
> specifies one", and every instruction that stage 3.5 must stop and report ON THE ENCODING, is
> superseded as to the encoding's status** and is left standing as the accurate record of the
> constraint that applied when it was written. **This governs R-12's Rule statement, its
> Constraint sub-items, its negative controls' rationale, and this file's § Assumptions alike.**
>
> **What D-29 settles:** the encoding, and with it **injectivity in substance** — the
> verify-on-write check is what establishes it — so the **never-reuse** obligation Q6=D′ retains is
> **no longer open on the encoding**, and `verify_release` is discharged in substance.
>
> ⚠ **What D-29 does NOT settle, and what remains a §18.3 stop-and-report point for stage 3.5:**
> **where the existing release population that verify-on-write must read back actually lives, and
> how it is enumerated.** The ledger that would have answered this was **declined as drafted at
> Amendment C** and `ReleaseLedgerEntry` withdrawn with it, so the mechanism is **specified but
> not yet implementable**. Three candidate surfaces are named at § Assumptions and **none is
> chosen here**. Owner decision; per TE §18.3 stage 3.5 must **stop and report**.
>
> **Nothing else changes.** No scientific value becomes fillable, **TA-15 is NOT discharged**, and
> TE §18.2's absolute rule stands.

> ## ✳ AMENDED 2026-08-28 — GOVERNANCE REMEDIATION, `GOV-2026-08-28-FD-01` (verdict FAIL)
>
> The project decision owner ruled on governance report
> `governance/reviews/GOV-2026-08-28-FD-01.md` (49 findings; Critical 6, High 25, Medium 13, Low 5).
> Nine of its recommendations reach this unit and were applied on 2026-08-28. **Every edit carries a
> dated note citing its Recommendation number at the site it changes**, and **no dated box, superseded
> record or `## Review` section was deleted or rewritten** — this unit's annotate-in-place convention
> is unchanged.
>
> | Rec | What changed here | Where |
> |---|---|---|
> | **8** | `PartitionError` promoted to a **fifteenth** project exception; the `PartitionError`/`LeakageError` discriminating rule stated; `InverseTransformError` explicitly left on the any-future clause with its reason; **R-01's count restated as DERIVED** | R-01; § Assumptions |
> | **9** | **FR-WS-7** named as this unit's requirement discharging onto **TA-23**; `aws_ai_dlc_preflight_report` added to the artifact family with **G-09** as its gate | R-02 |
> | **10** | **R-18** added — TE §13.4's **twenty columns**, the schema assertion, `prediction_hash` and `locked_test_accessed`; **R-19** added — the `run_id` join with orphan detection both ways | R-18, R-19 |
> | **1**/**3** | The prediction-hash receipt's **destination** is the registry row; `07`/the bootstrap **may not be the writer**; `prior_period_exposure` carried | R-18 |
> | **12** | **R-20** added — `exploratory` **derived** in the registry writer, with the G-06 carve-out and its negative control | R-20 |
> | **39** | **R-08** gains §13.4's write mechanism — single newline-terminated append plus durability confirmation, **at no read**; trailing-versus-interior malformed-row distinction; controls. Citation corrected | R-08; the count/citation box after R-20 |
> | **34** | **WS-17 re-labelled supporting**; the trailing *Superseded* annotation resolved | R-05 |
> | **49** | Dated clause: the `.gitignore` deny-list precondition **satisfied** 2026-08-28; **NFR-SEC-01 and TA-22 stay unclaimed** pending TA-22's full-scope scan | R-14 |
> | **42** | The board's encoding recommendation **recorded, not adopted**; the OPEN never-reuse posture left intact; the encoding remains **the owner's D-number decision** | § Assumptions |
>
> **The rule count moved 17 → 20** (R-01…R-20), derived after every edit; no other project count
> moved. **G-09 remains unsigned and nothing added here authorises creating a module.** No scientific
> value, governed constant, config field or approved signature is decided.
>
> **One item in the brief did not match the disk and is corrected rather than adapted around:**
> Recommendation 39's *"verification table at `business-logic-model.md:1748`"* is a **reviewer's**
> dated spot-check inside a preserved `## Review` section, not this unit's own live table. The
> citation correction is therefore stated in live rule text (R-08's Acceptance line and the box after
> R-20) instead of by editing a reviewer's sentence.

> **Addendum re-confirmed 2026-08-24, and this box was itself wrong — corrected 2026-08-25
> on adversarial reviewer finding M-3 (Major).** Sites **9–11** of
> `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md` § Addendum corrected three
> statements elsewhere in this unit that still asserted a superseded amendment status.
>
> **Superseded wording, preserved:** *"**None of them is in this file** — its
> acceptance-status table and its "This label is now permanent, 2026-08-24" box already read
> correctly, which is what made the three missed sites visible by comparison."*
>
> **Why that was false when written.** This file carried **four** further sites asserting a
> superseded amendment status, none of which the 2026-08-24 sweep reached: § Assumptions'
> all-three-pending bullet (finding M-2), R-06's acceptance reason *"because they are not yet
> in the contract"* (M-4), the *"until the amendment is approved"* condition near the
> acceptance-coverage note (m-1), and R-06's *"NOT FULLY ENFORCEABLE"* heading standing above
> its own *"Amendment B APPROVED"* line (m-2). The two clean sites this box named are clean;
> the generalisation from them to the whole file is what failed, and that self-certification
> is why the file was never swept. **None of the four carries a numeral**, which is why a
> sweep keyed to `DeterminismRecord` *"six fields"* and `services.md` *"two artifacts"* could
> not see them — the failure mode `project.md` § Way of Working already names.
>
> **No rule of this unit changed**, no count moved, and no scientific value was touched by
> either the 2026-08-24 addendum or this correction.

> **Re-established a fifth time 2026-08-23**, after a redo aimed at four stale
> cross-references in `target-standardization`'s question file. **No rule of this unit
> changed.**

> **Re-established three times on 2026-08-23, after three stage-wide redo jumps** — aimed
> respectively at a correction in `acquisition`, corrections in `external-products`, and a
> misread depth policy in `component-methods.md`, and — fourth — a sweep of two question
> files that had fallen stale against their own corrected artifacts. **No rule of this unit
> changed on any of the four occasions.**

The decision rules, validation logic, constraints and invariants this unit
enforces. Each rule states what it rejects, what it raises, and what evidence
proves the rejection actually happens.

**This project's affirmed testing methodology is a negative control paired with
every hard rule** — a test that proves the violation is *caught*, not only that the
happy path works. Every rule below therefore carries its negative control, and
where no acceptance row exists to accept that control, it says so.

## Sources

- `../../../inception/requirements-analysis/requirements.md` — REQ-ENG-1, -2, -3, -4, -6, -7, -8, -10, -11; FR-P1-01-10; FR-P1-04-11; FR-P1-05-13; FR-WS-7; NFR-AUD-01; NFR-SEC-01; NFR-DET-01.
- `../../../inception/units-generation/unit-of-work.md` § 1 `foundation` — the `Owns` list, the boundary, the two-tier error posture, and the `ensure_process_determinism`-first constraint.
- `../../../inception/units-generation/unit-of-work-story-map.md` — the acceptance mapping; 2 of 16 requirements carry no row.
- `../../../inception/application-design/component-methods.md` — the raise-contracts for every function named below.
- `../../../inception/application-design/components.md` and `component-dependency.md` — the import boundaries and § Shared resources' carve-out.
- `../../../inception/application-design/services.md` — § Stage entry contract, § Run record and registry.
- `../../../inception/practices-discovery/team-practices.md` — § Code Style (two-tier error posture, docstring rule), § Testing Posture (§18.3 as the real gate).
- `functional-design-questions.md` — Q1–Q8, FU-1–FU-3, the TA-03 verification, the three amendments — A **declined** and B **approved** (2026-08-24), C **declined as drafted** (2026-08-25, reversing its 2026-08-24 approval). Q6 re-answered as **D′** and FU-2 rendered moot, 2026-08-25.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **the Technical Environment document**, cited throughout these rules (§7.0, §9.1–9.2, §12, §13.1, §13.3, §13.4, §18.2–18.3, §19). *(Added 2026-08-25 on an adversarial residual raised twice: the document was cited ten times here and listed in no § Sources entry, and its derivations used an unresolved `<TE>` placeholder. **The placeholder was resolvable** — the file is at `PreFlight/`, 1158 lines — and the three figures it had blocked now derive and agree: **7** §13.1 bullets, **0** file-level entries under `artifacts/` in the §12 tree, and **36** distinct TA rows, TA-01…TA-36, confirming the §19-at-36 figure these rules had been carrying rather than deriving.)*
- `domain-entities.md` and `business-logic-model.md` — the shapes and workflows these rules constrain.
- `../../../../../../../../governance/reviews/GOV-2026-08-28-FD-01.md` — **the governance report this unit was remediated against on 2026-08-28** (verdict **FAIL**; 49 findings). Recommendations reaching this unit: **1**, **3**, **8**, **9**, **10**, **12**, **34**, **39**, **42**, **49**. *(Added 2026-08-28 with the remediation, per this unit's standing practice that an operatively cited document appears in § Sources — the omission `external-products` was faulted for at Recommendation 46.)*
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **the Vision document**, § 13.1's gate table, read 2026-08-28 for **G-09**'s evidence artifact (`aws_ai_dlc_preflight_report`, owner Supervisor, status **Open**) as distinct from **G-07**'s (`environment_and_cpu_preflight_report`), and for §8.3's exploratory label. *(Added 2026-08-28 with Recommendations 9 and 12, which turn on the G-07/G-09 distinction this document fixes.)*
- `../../governance-guards/functional-design/` — `AccessRecord`'s approved field set and **R-25**'s durable-append pattern, the comparator R-08's write mechanism and R-19's join are specified against. *(Added 2026-08-28 with Recommendations 10 and 39. **Two levels up, not one** — a sibling unit sits at `construction/<unit>/functional-design/`, so `../<unit>/…` would resolve inside this unit's own directory. Verified with `test -f`; noted because two sibling artifacts carry the one-level form and it does not resolve.)*
- `../../models-and-baselines/functional-design/` — § 12's `IntegrityError` subclasses (`SeedError`, `AlignmentError`, **`PartitionError`**, `LeakageError`) and R-92's raise condition, the authority for R-01's fifteenth entry; and the `PredictionHashReceipt` half of Recommendation 1. *(Added 2026-08-28.)*

---

## The two tiers, stated once

`team-practices.md` § Code Style fixes a two-tier posture and every rule below
belongs to exactly one tier:

| Tier | Behaviour | Shape |
|---|---|---|
| **Integrity violation** | Terminate the run non-zero with a message naming **the file and the violated expectation** | Raised as an `IntegrityError` subclass |
| **Completeness shortfall** | Non-fatal, but recorded as a **machine-readable field** in the output manifest — never console text only — with the artifact marked derived and/or partial | Return value or manifest field, **never raised** |

**Q5 = B makes tier membership structural rather than remembered.** A shortfall
cannot accidentally be raised as fatal because it is not in the exception
hierarchy at all.

---

## R-01 — `IntegrityError` is the single catchable base

**Rule (amended 2026-08-28 — the enumeration is FIFTEEN, and the operative obligation is the base
class, not the numeral).** **Every project-defined exception derives from `IntegrityError`**, and so
does any future integrity-related exception. **Fifteen are named in the enumeration below.**
`foundation` owns the base class and **raises six** of them — `ConfigError`, `PreflightError`,
`PlatformError`, `DeterminismError`, `ReleaseError`, `RegistryError`. The other **nine are raised by
other units and derive from the same base**: `PhaseBoundaryError` and `LockedTestError`
(`governance-guards`), `LeakageError` and `AlignmentError`, `SeedError`, `FairnessError`,
`BootstrapError`, `RegimeError`, and — **added 2026-08-28** — **`PartitionError`**
(`models-and-baselines`, declared in **`src/models/`** ⚠ **RULED 2026-08-28 — `PartitionError` is declared in `src/data/config.py`.** *(Project decision owner, on the `functional-design` gate, amending the wording of the Rec 8 ruling. **Superseded wording, preserved: declared in `src/models/`.**)* The reason is the one `features-and-splits` raised and the Rec 8 ruling could not have known: `component-dependency.md` marks **`src/features` → `src/models`** and **`src/data` → `src/models`** both as **`—`**, while every `PartitionError` raise in that unit lives in `src/data/splits.py` or `src/features/*` — so on the approved matrix that unit could not have raised the exception at all. `src/data/config.py` is where R-01 already declares `IntegrityError` and the base every unit already imports, so **no dependency-matrix amendment is needed and none is taken**. `models-and-baselines` remains the exceptions **semantic owner** — R-92s discriminating rule is unchanged — but is no longer its declaration site. , which that unit's `Owns` list carries:
`src/models/persistence.py`, `climatology.py`, `ridge.py`, `random_forest.py`, `lstm.py`,
`train.py`, `checkpoint.py`).

> ## ✳ AMENDED 2026-08-28 — `PartitionError` PROMOTED TO A FIFTEENTH, AND THE COUNT IS NOW DERIVED
>
> *(Applied on the project decision owner's ruling on governance report
> `governance/reviews/GOV-2026-08-28-FD-01.md` **Recommendation 8**, where the owner selected
> **option 1** — promote `PartitionError` into the enumeration, formally amended. The three seats
> that raised the finding split on the remedy and the Chair recorded the choice as the owner's
> architectural call; the owner made it. **Superseded rule wording, preserved verbatim:** *"**All
> fourteen project-defined exceptions derive from `IntegrityError`**, and so does any future
> integrity-related exception. … The other **eight are raised by other units and derive from the
> same base**: `PhaseBoundaryError` and `LockedTestError` (`governance-guards`), `LeakageError` and
> `AlignmentError`, `SeedError`, `FairnessError`, `BootstrapError`, `RegimeError`."*)*
>
> **This is R-01's SECOND staleness**, and the reason the count is no longer asserted. The
> enumeration was corrected from six to fourteen on 2026-08-25, for exactly the reason this rule's
> own rationale gives — *"a hand-maintained catch list means a seventh subclass added later is
> silently uncaught"* — and it went stale again within three days. A hand-maintained **enumeration**
> fails the same way a hand-maintained **catch list** does. So the rule's operative obligation is
> restated as the base-class relation (*every* project-defined exception derives from
> `IntegrityError`), the fifteen are a **named subset** rather than a completeness claim, and the
> total is **derived and printed** below rather than carried in prose.
>
> ### The derivation, run 2026-08-28 over all twelve units' 48 `functional-design` artifacts
>
> ```
> bun: match /\b([A-Z][A-Za-z0-9]*Error)\b/g over
>      construction/*/functional-design/*.md      (12 units, 48 artifacts)
>
> raw distinct *Error tokens ........................... 36
>   of which Python builtins (NotImplementedError,
>   TypeError) ........................................   2
> distinct PROJECT-DEFINED *Error names ...............  34
>   of which the base IntegrityError ..................   1
> distinct project-defined SUBCLASS names ............   33
>   named in R-01's enumeration (this amendment) ......  15
>   riding R-01's any-future clause ...................  18
> ```
>
> **The governance report's "36 distinct `*Error` names" and "19 outside R-01's fourteen" both
> reproduce**, once the two figures are read against the right population: 36 is the **raw token**
> count including two Python builtins, and 19 is the project-defined subclass count outside the
> **fourteen** — which becomes **18** outside the **fifteen** this amendment names. Both agree with
> the derivation above. **The eighteen riding the any-future clause, enumerated so the residue is
> visible rather than counted:** `AcquisitionError`, `AuditScopeError`, `BenchmarkError`,
> `BudgetError`, `ComparatorError`, `CredentialEgressError`, `DriverError`, `EvidenceScanError`,
> `FixtureError`, `GateError`, `ImportBoundaryError`, `InventoryError`, `InverseTransformError`,
> `ManifestError`, `ReuseError`, `SchemaError`, `StandardizationError`, `TargetQualityError`.
>
> **Standing obligation, so the numeral cannot go stale a third time.** Whoever revisits this
> hierarchy **re-runs the derivation above and prints its output** rather than trusting "fifteen".
> The base-class relation is what the stage-entry catch in R-10 depends on, and it holds whatever
> the census returns. The governance report's closure evidence asks for exactly this: *"one
> programmatic derivation of every `*Error` raised across the twelve units, reconciled against
> R-01's list and printed in `foundation`'s artifact."*
>
> ### One correction to the finding's evidence, stated rather than silently adapted
>
> The report's evidence reads *"`PartitionError` … reaches **10 of 12 units** (23 hits in
> `models-and-baselines`, 15 in `features-and-splits`)"*, and its Comparison rests option 1 partly
> on that reach — *"ten units, which resembles R-01's eight 'raised by other units' far more than
> the two genuinely narrow unit-local additions"*. **Ten is the raw token reach; the DESIGN reach is
> two.** Derived 2026-08-28, separating live design prose from text inside a preserved `## Review`
> section or inside the quoted 2026-08-24 re-save note (*"R-96's `PartitionError` mechanism and
> R-95's field label are carried to the stage"*):
>
> ```
> PartitionError, units with LIVE design-prose occurrences .............. 2
>   models-and-baselines (live 10, review 6, quoted note 1)
>   features-and-splits  (live  5, review 3, quoted note 3)
> PartitionError, units carrying it ONLY in a preserved review or the
>   quoted re-save note ................................................ 8
>   acquisition, evaluation-and-comparison, external-products, foundation,
>   governance-guards, inventory-and-registry, statistical-inference,
>   target-standardization
> ```
>
> `governance-guards`' own artifact records the same fact independently: *"`PartitionError`'s three
> hits are all inside the 2026-08-24 re-save note quoting `models-and-baselines`' R-96 residual …
> no sixth exception exists anywhere in the artifact set."* **`foundation`'s own three hits are that
> same quoted sentence** — this unit does not raise `PartitionError` and does not begin to.
>
> **The ruling stands on the argument that survives.** Reach is not what forced the promotion; the
> **cross-unit taxonomy disagreement** is, and it is real and unaffected by this correction:
> `models-and-baselines` R-92 raises `PartitionError` for a `partition_id` mismatch,
> `evaluation-and-comparison` R-105 raises `LeakageError` for the same condition while claiming to
> *"mirror R-92"*, and `statistical-inference` R-113 imports R-105 *"as written"*, so a third unit
> inherits it. Two units' designs must agree on the discriminating rule, which is why it belongs in
> the shared enumeration rather than in one unit's private vocabulary. R-01's own anti-stale-list
> rationale reaches the same conclusion independently of how many units raise it.
>
> ### The discriminating rule, stated because two units' designs must agree on it
>
> The owner's ruling promotes `PartitionError` **and keeps `LeakageError`**, so the boundary between
> them is a rule rather than a preference. It is stated here, in the artifact that owns the
> hierarchy, so neither unit has to infer it:
>
> | Raise | When | Test |
> |---|---|---|
> | **`PartitionError`** | A **declared-identity disagreement** — a `partition_id` mismatch across inputs, or a training partition where one is barred — **regardless of whether any information actually moved** | Would the fault be a fault even if the disagreeing partitions held identical rows? If yes → `PartitionError` |
> | **`LeakageError`** | The disagreement **implies information flow** — future or out-of-partition rows reached a fit, a transform, or a scoring path | Does the fault mean a value from outside the permitted partition entered a computation? If yes → `LeakageError` |
>
> **Where both are literally true, `LeakageError` wins**, because it is the stronger claim and the
> one §18.3's critical set names (*"train-only transforms"*, *"comparison-wide masks"*). This
> tie-break is stated because the governance report's option 4 was refused partly on the ground that
> *"the boundary is genuinely hard to draw for a comparison whose members disagree on partition — it
> is simultaneously both"*. It is: and the tie-break resolves it deterministically rather than
> leaving the site that prompted the finding unapplicable. **This is not option 4 adopted by the
> back door** — option 4 was *keep both unit-local and state the rule*; option 1 promotes
> `PartitionError` into the shared hierarchy, and the rule above exists because the promotion leaves
> two live exception types on one path, not as an alternative to the promotion.
>
> **What this rule does NOT decide.** Whether `evaluation-and-comparison` R-105 changes its raise
> from `LeakageError` to `PartitionError` is **that unit's** call against the table above, and
> `statistical-inference` R-113 inherits whatever R-105 settles on. The governance report assigns
> the taxonomy choice to those two units (*"Owner / due gate: `foundation` (hierarchy),
> `models-and-baselines` + `evaluation-and-comparison` (taxonomy choice)"*). **This unit owns the
> hierarchy and the discriminating rule; it does not reach into a sibling unit's raise site**, and
> it does not close `evaluation-and-comparison`'s or `statistical-inference`'s side of
> Recommendation 8.
>
> ### `InverseTransformError` — it RIDES the any-future clause, and here is why the treatment differs
>
> `InverseTransformError` is **not** promoted, and is **not** a sixteenth. It rides R-01's *"any
> future integrity-related exception"* clause, exactly as `statistical-inference` already discloses
> it and as `fixtures-and-reproducibility` discloses `FixtureError`. Three reasons, and the first is
> the one the reach argument cannot supply:
>
> 1. **No cross-unit disagreement exists.** Derived 2026-08-28: `InverseTransformError` occurs in
>    live design prose in exactly **two** units — `evaluation-and-comparison` (13) and
>    `statistical-inference` (7) — and **both raise it for the same condition with the same
>    meaning**. Nothing has to be reconciled, so nothing has to be centralised. `PartitionError`
>    was promoted because two units disagreed about which exception a single condition raises; that
>    is the whole discriminator, and it is absent here. **Reach cannot be the discriminator**: the
>    derivation above puts both at two units of live design prose, so an argument from reach would
>    promote both or neither.
> 2. **It sits entirely inside one package.** The inverse-before-metric path is `src/evaluation/`,
>    and both units that raise it depend on `foundation` already, so the base class is importable
>    without any new edge. `PartitionError` spans `src/models/` and `src/features/`.
> 3. **The owner ruled on `PartitionError` and on nothing else.** Recommendation 8's ruling names one
>    promotion. Adding a sixteenth on this stage's own initiative would be the change-an-approved-
>    contract-by-assertion move this unit has refused throughout — the same standard that sent
>    `ensure_process_determinism`'s signature and `write_release`'s raise-contract to the owner.
>
> **The obligation this creates, and it is not nothing.** Because `InverseTransformError` is not
> enumerated, the two units raising it **must** declare it as an `IntegrityError` subclass on their
> own side, or R-10's stage-entry catch will let it exit with no `aborted` registry row — the
> NFR-AUD-01 failure this rule was corrected once to prevent. That is recorded as a cross-unit open
> item in § Assumptions alongside the nine, not left to inference.

**Where the hierarchy is declared** *(decided 2026-08-25 on adversarial finding M-1 of the
ninth-redo iteration 1 — **the enumeration above named fourteen subclasses and no module to hold
the base**, which stops stage 3.5 rather than misleading it)*. `IntegrityError` and the six
subclasses this unit raises are declared in **`src/data/config.py`**.

**Why there and not a new module.** TE §12's `src/data/` tree names **nine** modules and **none for
exceptions**, so a dedicated `src/data/exceptions.py` would be a **§12 amendment** — and this stage
has refused throughout to change an approved contract by assertion. `config.py` is already in this
unit's `Owns`, already the module every stage script imports first for `load_configs` and
`ensure_process_determinism`, and already where W-1's abort path lives; declaring the base there
adds no import that the stage-entry contract does not already make. **The eight exceptions raised by
other units import the base from `src/data/config.py`**, which is a legal direction — every one of
those units already depends on `foundation` — and `component-dependency.md` confirms
`src/features`, `src/models`, `src/evaluation`, `src/gnss` and `src/external` may all import
`data`, so no boundary is crossed and no cycle created.

**What was decided and what was not.** This fixes a **declaration site**, which is what
`component-methods.md` § Assumptions defers to 3.1 — *"they are declared where raised until 3.1
places them"*. It decides **no** scientific value, **no** governed constant and **no** signature, and
**G-09 still forbids writing the module.** A dedicated exceptions module would read better and is
recorded as an open item for the owner, because it needs a §12 amendment this stage may not make.

> **Why the enumeration grew from six to fourteen, and on whose authority** *(corrected 2026-08-25
> on adversarial finding m-1 of the eighth-redo iteration 2 — **the one finding in this unit's review
> history that would have made stage 3.5 build the wrong thing**)*. `component-methods.md`
> § Assumptions states that all fourteen *"are project-defined exceptions **in a shared base**. §12
> names no exceptions module; they are declared where raised **until 3.1 places them**."* **This
> stage is 3.1**, and placing them is therefore its job — but R-01 enumerated only the six this unit
> raises, and `domain-entities.md` § 9 mirrored the same six.
>
> **What that omission would have caused.** W-1 step 4 raises `PhaseBoundaryError`, and R-10 has the
> stage entry contract catch `IntegrityError` to write the `aborted` registry row. With
> `PhaseBoundaryError` outside the enumerated hierarchy, an implementer writing `except
> IntegrityError` would let a **phase-boundary violation exit with no `aborted` row** — precisely
> the event **NFR-PHASE-01** and **NFR-AUD-01** most require recorded, and the one failure this
> unit's two-tier posture exists to make impossible. Six consecutive adversarial passes did not
> examine it: `grep -rn "PhaseBoundaryError"` over this unit returned **one** hit, the diagram edge.
>
> **This is exactly the failure R-01's own rationale predicts** — *"a hand-maintained catch list
> means a seventh subclass added later is silently uncaught"* — arriving as a **missing enumeration
> entry** rather than a missing catch clause. The rule was right and its list was not.
>
> **Cross-unit obligation, recorded rather than assumed.** `foundation` owns `IntegrityError` and
> the stage-entry catch, so it fixes the hierarchy from its own side. The eight exceptions above are
> **raised by other units**, and each of those units' `functional-design` must declare its
> exceptions as `IntegrityError` subclasses. `governance-guards` owns `phase_contract.py` and
> therefore `PhaseBoundaryError`; that unit depends on `foundation`, so importing the base is a
> legal dependency direction and creates no cycle. Listed as an open cross-unit item in
> § Assumptions.
>
> **⟶ Annotated 2026-08-28, not rewritten: this box's "eight" is now NINE.** The box above is the
> dated record of the 2026-08-25 six-to-fourteen correction and its sentences stand as written.
> `PartitionError` was promoted to a fifteenth on 2026-08-28 per Recommendation 8, so the
> exceptions raised by other units are **nine**, and the cross-unit declaration obligation this
> paragraph states now binds `models-and-baselines` for `PartitionError` as well — plus, under the
> any-future clause rather than the enumeration, `evaluation-and-comparison` and
> `statistical-inference` for `InverseTransformError`. § Assumptions carries all of them. The
> annotate-in-place form follows the `GOV-2026-08-22-INC-01` Rec 7 precedent this unit has used
> throughout: no dated sentence is rewritten, and the current state is stated beside it.

**Constraint.** Every `IntegrityError` **must** carry the affected file or resource
and the violated expectation. The constructor requires both, so the two-tier
message format is enforced by construction rather than by convention.

**Why a base and not a fixed number of independents** *(numeral removed from this heading 2026-08-28
per Recommendation 8 — it read "fourteen", and before that "six", and this rule has now gone stale
on its own count twice; the heading no longer carries one. Prior correction note preserved: "count
corrected 2026-08-25 with R-01's enumeration; it read 'six', which was this unit's own raises rather
than the hierarchy")*. The stage entry contract must catch *any*
of them to write the `aborted` registry row. A hand-maintained catch list means a
seventh subclass added later is silently uncaught — the same list-versus-rule
failure `DP-DATA-01` already caught in this project, where an obligation written as
a list silently exempted whatever was not anticipated. **The same failure reaches a
hand-maintained enumeration**, which is what happened here twice, and why the count above is derived
and the base-class relation is the operative obligation.

**Negative control.** A test defines a fresh `IntegrityError` subclass not named in
any catch list and asserts the stage entry contract still catches it and still
writes the `aborted` row.

**Negative control — the enumeration itself, added 2026-08-28 per Recommendation 8.** A test
**re-derives** the distinct project-defined `*Error` names raised across the twelve units'
`functional-design` artifacts and **fails when a name is neither in R-01's fifteen nor disclosed by
its raising unit under the any-future clause**. This is the control that catches the failure R-01
suffered twice: a subclass added later with nobody updating the enumeration. It asserts a
**reconciliation**, not a number, so it does not itself go stale when the census legitimately grows.

**Negative control — the taxonomy boundary, added 2026-08-28 per Recommendation 8.** One control per
raising unit, on the discriminating table above: assert that a `partition_id` mismatch over
*identical* rows raises **`PartitionError`** and not `LeakageError`, and that an out-of-partition row
reaching a fit raises **`LeakageError`** and not `PartitionError`. This is the control that stops
`pytest.raises(PartitionError)` passing at `06` and failing at `07`. **The per-unit controls are
owned by the raising units** — this unit owns the boundary rule they assert against and states the
obligation; it does not author another unit's test.

**Acceptance.** Contributes to TA-10 (registry records failed as well as
successful runs). **No new acceptance row is sought** for the 2026-08-28 amendment: Amendment A was
declined and §19 is held at 36 rows, so the enumeration control's enforcement rides §18.3's
gate-test list and TA-10 rather than a row of its own.

## R-02 — Preflight rejects both a missing field and a `TBD` field

**Rule (Q1 = B).** `assert_no_tbd` rejects a required field that is **absent** from
the configuration *and* a required field whose value is the `TBD — freeze gate`
sentinel. Both are failures.

**Constraint.** The error names **every** offending field, so a run reports all of
them rather than the first — `component-methods.md`'s stated raise-contract.

**Why both conditions.** REQ-ENG-2 wants both caught. A sentinel-only check is a
tautology: it can only find fields already marked `TBD`, so a required field simply
missing from the config passes.

**Negative control.** Two fixtures, one with a `TBD` field and one with the field
absent; both must raise `PreflightError`, and the message must name the field in
each case.

**Acceptance.** TA-02, and TA-23 as §18.3's preflight gate.

> ## ✳ FR-WS-7 IS THIS UNIT'S OWN REQUIREMENT DISCHARGING ONTO TA-23 — NAMED 2026-08-28
>
> *(Added on the owner's ruling on `GOV-2026-08-28-FD-01` **Recommendation 9**, option 1. The
> finding: TA-23 was cited as an acceptance row across this unit's artifacts with **neither its
> evidence artifact designed nor its discharging requirement named**, while the structurally
> identical REQ-ENG-4/TA-09 discharge gets an explicit callout in every artifact of the unit that
> carries it. The asymmetry was the tell.)*
>
> **FR-WS-7 is `foundation`'s requirement whose acceptance row is TA-23 — and TA-23 is this unit's
> PRIMARY row, not a supporting one.** Both halves derived rather than asserted:
>
> ```
> unit-of-work-story-map.md:127        ->  | FR-WS-7 | `foundation` | TA-23 |
> story-map Table 2, primary == foundation
>   ->  TA-01 TA-02 TA-03 TA-10 TA-15 TA-22 TA-23        (count 7, TA-23 among them)
> ```
>
> This mirrors the callout pattern `fixtures-and-reproducibility` already carries for the same
> discharge shape — *"**REQ-ENG-4 is `foundation`'s requirement whose acceptance row is TA-09 — this
> unit's primary row**"* — with the difference that here **both sides are ours**: this unit owns the
> requirement *and* owns the row, so nothing is being discharged across a unit boundary.
>
> **The evidence artifact is `aws_ai_dlc_preflight_report`, and its gate is G-09.** Derived from the
> authorities rather than inferred:
>
> | Source | States |
> |---|---|
> | TE:1083 (§18.3) | *"**Decision criterion:** zero unresolved P0 fields and no failing critical test. The evidence artifact is `aws_ai_dlc_preflight_report`."* |
> | TE:1119 (§19, TA-23 row) | Evidence column = `aws_ai_dlc_preflight_report`; status **Pending** |
> | Vision gate table, **G-09 Agent preflight** | Owner **Supervisor**; evidence `aws_ai_dlc_preflight_report`; due *"Before any affected component is coded"*; status **Open** |
> | Vision gate table, **G-07 Reproducibility** | evidence `environment_and_cpu_preflight_report` — **a different artifact serving a different gate** |
> | TE:530 | defines `environment_and_cpu_preflight_report` (install-from-pins on both platforms, completed skeleton run, measured CPU runtime/RAM/storage) |
>
> **The two reports are NOT aliases**, and this design does not treat them as one. Option 2 of
> Recommendation 9 — declare them one artifact under two names — was **not** taken: they serve
> different gates with different content and no basis for an alias was found. `foundation` produces
> `aws_ai_dlc_preflight_report` for G-09/TA-23; `fixtures-and-reproducibility` produces
> `environment_and_cpu_preflight_report` for G-07. **Nothing here reaches into that unit's
> artifacts** — its TA-23 supporting claim is its own to reconcile, and Recommendation 9's owner
> column assigns the fix here.
>
> **What `aws_ai_dlc_preflight_report` must show, quoted from FR-WS-7's criterion**, so 3.5 does not
> have to reconstruct it: *"`aws_ai_dlc_preflight_report` shows all four preconditions met — zero
> `TBD` fields, every declared source and hash resolving, all ten named tests passing, and the
> sign-off present. A declared hash that does not resolve fails the gate rather than being reported
> as a warning."* The four preconditions map onto rules already in this file: **zero `TBD`** →
> **R-02** and **R-03**; **every declared source and hash resolves** → `assert_declared_sources_exist`
> (W-3), whose failure is a raise and never a warning; **all ten named critical tests pass** → the
> §18.3 set enumerated in `team-practices.md` § Testing Posture, which this unit does not own end to
> end and therefore **aggregates rather than asserts**; **supervisor sign-off recorded** → a
> supervisor act this unit records and never synthesises.
>
> **The report is an aggregation surface, and it must not become a self-certifying one.** Two limbs
> of the gate — the ten critical tests and the supervisor sign-off — are **not this unit's to
> produce**. `foundation` emits the report by collecting evidence produced elsewhere; a limb with no
> evidence is rendered **absent**, never **passed**, and the report **refuses to render a green
> overall verdict while any limb is absent**. Stated because the cheapest wrong implementation is a
> report that treats an uncollected limb as satisfied, which is precisely how a gate control becomes
> a formality.
>
> **Negative control.** Render the report with each limb withheld in turn — a `TBD` field present, a
> declared hash that does not resolve, one named critical test failing, the sign-off absent — and
> assert the overall verdict is **not** green in each of the four cases, and that the withheld limb
> is reported **absent or failed by name** rather than omitted. A fifth case: a limb whose evidence
> was never collected must render **absent**, not **passed**.
>
> **G-09 is Open and unsigned.** Designing this report's contents authorises nothing: it does not
> fill a `TBD`, does not create a module, and does not satisfy the gate it evidences.

## R-03 — The required-fields map is keyed by `(stage, phase)`

**Rule (FU-1 = C).** Required fields are declared per `(stage_slug, phase)` pair.
Fields that legitimately remain `TBD` in Phase 1 **do not block Phase 1**;
Phase-2-required fields **are enforced in Phase 2**.

**Constraint — the completeness assertion is the rule, not the map.** A test walks
the parsed configuration structure and **fails** when a governed required field
appears in no map entry. The map alone is a list; the test is what makes it a rule.

**Why the phase is in the key.** TE §7.0's Phase 1 hard prohibition makes a
Phase-2 field legitimately unset during Phase 1. A stage-only key forces either
failing Phase 1 on fields it must not fill — which `project.md` § Forbidden
prohibits filling — or weakening the check to the intersection, which silently
drops every Phase-2-only field. A `(stage, phase)` key cannot be forgotten the way
a per-field annotation can be omitted.

**Negative control.** Remove one governed required field from the map; the
completeness test must fail. Run a Phase-1 stage whose Phase-2-only fields are
`TBD`; preflight must **pass**. Run the Phase-2 counterpart with the same fields
`TBD`; preflight must **fail**.

**Acceptance.** TA-02, TA-23.

## R-04 — Authorized `TBD` in Bolt 1 is expected evidence, not a failure

**Rule (Q2 = B).** During Bolt 1 the real governed configs **do** contain
`TBD — freeze gate` sentinels — REQ-ENG-2 requires exactly that, and Gate 0's
permitted list allows creating them before G-09. Their presence is **expected test
evidence, not a foundation-stage failure.**

**Constraint — the real-config test asserts a raise, and asserts *which* fields.**
It asserts that `assert_no_tbd` raises **and** that the error identifies **exactly**
the required fields still carrying the sentinel. The expected set is kept explicit
and updated as each freeze gate closes.

**Why this is worth the maintenance.** It turns the sentinels into positive
evidence: the test states which freeze gates are still open, so closing one becomes
a visible event rather than a silent edit.

**Constraint — synthetic fixtures cover both branches.** Fixtures must cover
failure on `TBD` **and** on a missing required field, **and** successful execution
when all required fields are present and finalized. Without the passing fixture the
clean path stays unexercised until every gate closes.

**Negative control.** The real-config test *is* the negative control. Its inverse —
a fixture with everything resolved — is the positive control that stops the test
passing for the wrong reason.

**Acceptance.** TA-02, TA-23.

## R-05 — Determinism is applied before any graph construction, and re-exec comes first

**Rule (NFR-DET-01, `unit-of-work.md` § 1).** `ensure_process_determinism(argv)` is
the **first statement** of every stage script's `main()`, **before any framework
import**. `seed_everything` enables TensorFlow op determinism **before any graph
construction**.

**Constraint.** `seed_everything` **raises** `DeterminismError` when TensorFlow has
already been initialised — **observed as `"tensorflow" in sys.modules`, evaluated BEFORE `seed_everything` performs its own deferred import** *(defined 2026-08-25, final-pass m-7: the phrase was used four times and defined nowhere, and with the TensorFlow import now deferred into this function, a guard checking after its own import would trip on itself)*. Enabling op determinism afterwards is not equivalent, and
a re-exec after TensorFlow loads is pointless.

**Constraint.** The re-exec is **recorded** in `DeterminismRecord.reexec_performed`
and in the run log, so it is never mistaken for a double run.

**Constraint (added 2026-08-25, reviewer finding m-3, owner-decided).** `reexec_performed` is
read from a **sentinel environment variable** that the parent sets immediately before
`os.execv` and the child reads once: present → `True`, absent → `False`. This carrier is
required for the negative control below to discriminate at all —
`ensure_process_determinism(argv)` returns `None`, so nothing crosses the `exec` boundary in
its return value, and a child cannot otherwise distinguish a re-exec from an externally
exported `PYTHONHASHSEED`. **The variable's name is an implementation identifier**, not a
scientific constant or a governed config field, so it is not subject to TC-03e and lives in
`src/data/config.py`; the approved stage-2.6 `-> None` signature is **unchanged**.

**Constraint — the sentinel is READ ONCE AND UNSET** *(added 2026-08-25 on adversarial reviewer
finding m-3, second pass)*. The child **must remove the sentinel from its environment
immediately after reading it**. The reader is `ensure_process_determinism` itself, at W-1 step 1 —
the first statement of every stage script's `main()` — so the pop happens before any stage logic
runs and therefore before any subprocess this script could launch. *(The earlier phrasing "before
any subprocess is launched" named no actor and was unsatisfiable as a standalone requirement:
corrected 2026-08-25 on adversarial finding m-3 of the restored budget. `reexec_performed` is
held **in module-level state inside `src/data/config.py`** — set by `ensure_process_determinism`
at the moment it pops the sentinel, read when the `DeterminismRecord` is constructed. *(Added
2026-08-25 on adversarial finding m-1 of the restored budget, which found this the **only
implementability gap no open item covered**: the sentinel's journey across the `exec` boundary was
specified, but nothing said where the bit lived **in-process** between the pop at W-1 step 1 and
the record at W-4 step 4. `ensure_process_determinism` returns `None`, `seed_everything(snapshot,
*, stage)` takes no such argument, and `ConfigSnapshot`'s eight approved fields carry no re-exec
bit — so stage 3.5 would have had to invent a holder, which is exactly what naming the sentinel
was meant to prevent.)*

**Why module-level state and not the alternatives.** Both the setter and the reader live in
`src/data/config.py`, which `unit-of-work.md` § 1 gives to this unit, so the hand-off is
**intra-module** and creates no cross-module coupling and no new parameter. The alternatives each
change an **approved stage-2.6 contract** and would need the same amendment this stage demanded
elsewhere: returning `bool` from `ensure_process_determinism` alters its `-> None` signature;
adding a field to `ConfigSnapshot` alters an approved dataclass, and `ConfigSnapshot` is built at
W-1 step 2 — *after* the pop at step 1 — so it cannot receive the bit without reordering the
contract; adding a parameter to `seed_everything` alters its signature. **This is an engineering
decision with no scientific content, no governed value and no config field**, and it is recorded
here as a decision rather than left to 3.5.

The value is then **recorded** into `DeterminismRecord` at W-4 step 4, which reads the value
`ensure_process_determinism` captured rather than re-reading the environment — the variable is
already gone by then, which is the point.)* Without that pop the carrier
is wrong rather than merely imprecise: environment variables are inherited by descendants, and
after a re-exec `PYTHONHASHSEED` is already set, so a subprocess launched from a re-exec'd stage
script does **not** re-exec and yet still sees the sentinel. It would record
`reexec_performed = True` for a process that never re-exec'd, and **this rule's negative control
below would pass for the wrong reason** — the failure mode this project's testing posture exists
to catch. With the pop, the bit that crosses is *this process is a re-exec child*; without it,
the bit that crosses is *some ancestor was*.

**Constraint — `config.py` must not import a framework at module scope** *(stated 2026-08-25 on
adversarial residual r-4, raised in two consecutive passes and derivable but unstated)*.
`seed_everything` lives in `src/data/config.py` and needs TensorFlow, while
`ensure_process_determinism` — in the **same module** — must run *before any framework import*
(FU-1 = D). A module-scope `import tensorflow` would therefore load the framework **at the moment
the stage script imports `config.py`**, which is before `main()`'s first statement executes, and
would defeat the re-exec guarantee the rule exists to provide. **TensorFlow is imported inside
`seed_everything`**, not at module scope. **The same rule binds every stage script** *(added 2026-08-25, final-pass m-6)*: a stage script importing a framework at module scope loads it before `main()`'s first statement, so `ensure_process_determinism` would re-exec after TensorFlow loads — pointless per FU-1=D — and W-4's already-initialised guard would abort every run. Stage scripts import frameworks inside functions or after the entry contract's step 1. **The prohibition is transitive** *(limb restored 2026-08-25 on confirming-pass finding F-2: binding only the script's own imports leaves the by-construction case open — a script importing `src/models/train.py` at module scope complies with the letter while `train.py`'s own module-scope `import tensorflow` aborts every run)*: **no module a stage script imports at module scope may itself import a framework at module scope.** Framework imports live inside the functions that need them, throughout `src/`. This is a consequence of the approved stage-2.6 contract
placing both functions in one module rather than a choice made here, and it is stated because an
implementer following the module layout without noticing the ordering would silently break FU-1 = D.

**Constraint.** `seed_everything` **does not** touch the bootstrap seed. That
carve-out is `src/evaluation/bootstrap.py` by ADR-05 — a design decision, not an
oversight.

**Negative control.** Import TensorFlow, then call `seed_everything`; it must raise
`DeterminismError`. Invoke a stage script with `PYTHONHASHSEED` unset and assert
`reexec_performed` is `True` and exactly one run is recorded.

**Acceptance.** **WS-17 (supporting — process determinism precondition only; the replicate hash is
`statistical-inference`'s)**, **TA-13** (NFR-DET-01) and **TA-10** (FR-P1-05-13), derived from
story-map Table 1.

> ## ✳ WS-17 RE-LABELLED SUPPORTING, 2026-08-28 — AND THE TRAILING SUPERSEDED ANNOTATION RESOLVED
>
> *(Applied on the owner's ruling on `GOV-2026-08-28-FD-01` **Recommendation 34**, option 2. The
> finding: R-05's Acceptance claimed **WS-17** while R-05's own Constraint carves the bootstrap seed
> out of `seed_everything` — *"`seed_everything` **does not** touch the bootstrap seed. That
> carve-out is `src/evaluation/bootstrap.py` by ADR-05"* — so the rule claimed a row it cannot
> evidence by its own constraint. **Superseded Acceptance line, preserved verbatim:** *"**WS-17,
> TA-13** (NFR-DET-01) and **TA-10** (FR-P1-05-13), both derived from story-map Table 1. *Superseded:
> `TA-13, TA-26`.*"*)*
>
> **Why supporting and not deleted.** The dependency is real and worth keeping visible: **no
> replicate hash reproduces without `PYTHONHASHSEED=0` and the re-exec**, which is exactly what this
> rule guarantees. Option 1 (delete WS-17 outright) would have made the ledger cleaner and rendered
> that contribution invisible; the owner took option 2, and the label is written in full so a
> supporting claim cannot be read as coverage.
>
> **WS-17's single primary owner is `statistical-inference`**, and its evidence is not ours. Derived
> from the authority:
>
> ```
> TE §16, line 969:
>   | WS-17 | Vector time-block bootstrap carries all stations together and
>            reproduces exactly from seed 20221201
>          | `test_bootstrap.py`
>          | Synthetic-correlation test and replicate output |
> ```
>
> `statistical-inference` R-117 claims **"WS-17 (primary)"** and reciprocally returns **TA-13** and
> **TA-26** to `foundation` and `models-and-baselines`. Its `BootstrapResult` records *"the seed key
> consumed, the generator identity, and the replicate hash"* — the artifact fact TE §16 names as
> WS-17's evidence. **This rule produces none of that**, by ADR-05's deliberate carve-out.
>
> **What this rule's supporting contribution actually is**, stated so a 3.2 verification planner
> cannot substitute it for the replicate hash: `reexec_performed = True` with `PYTHONHASHSEED=0`
> established before any framework import. It is a **precondition of exact reproduction, never
> evidence of it.** A WS-17 row marked `PASS` on this unit's determinism record rather than on
> `test_bootstrap.py`'s replicate hash is a row passed on evidence that does not test the thing —
> the risk Recommendation 34 names, and the reason the label carries its full qualification here
> rather than the bare word "supporting".
>
> **The trailing "*Superseded: `TA-13, TA-26`*" annotation — resolved, not merely deleted.** It was
> terse to the point of suggesting unsettled churn, which is what the finding flagged. In full: this
> Acceptance line **previously cited `TA-13, TA-26`** for NFR-DET-01, and that citation was replaced
> on 2026-08-22 when every acceptance line in this file was re-derived from story-map Table 1.
> Table 1 gives **NFR-DET-01 → WS-17, TA-13**; **TA-26's primary owner is `models-and-baselines`**,
> and `foundation` is only a *supporting* unit on it — one of exactly two such rows (TA-13, TA-26),
> derived in `domain-entities.md` § Requirement coverage. So TA-26 was dropped from this line because
> it is another unit's row, and WS-17 was added because Table 1 names it. **There is no open churn
> here**; the citation has been stable since 2026-08-22 and the only change on 2026-08-28 is WS-17's
> primary-to-supporting re-label.



## R-06 — An empty `nondeterministic_ops` is never proof of determinism

**Rule (Q3 = C).** `nondeterministic_ops` is populated from **runtime
observation**, cross-checked against any expected set declared in configuration.
The framework version, determinism settings, probe scope and detected mismatches
are all recorded. A mismatch between declared and observed is an **integrity
finding**.

**Constraint.** Where the framework cannot give a complete assessment, the result
is explicitly marked **`partial`**. Where the relevant operations have not yet
executed, they are marked **`not-yet-measured`**. **An empty list is never treated
as proof of determinism.**

> ## ✅ THIS RULE IS ENFORCEABLE UNDER THE APPROVED CONTRACT
>
> *(Heading corrected 2026-08-25 on adversarial reviewer finding m-2. **Superseded heading,
> preserved:** "⚠ THIS RULE IS NOT FULLY ENFORCEABLE UNDER THE APPROVED CONTRACT". It was
> true when written and contradicted its own first line from the moment Amendment B was
> approved on 2026-08-24 — the body below was rewritten then and the heading was not. The
> enforceability conclusion is not being weakened or strengthened to match the heading: it is
> the conclusion the body already reaches and evidences, namely that the three fields exist,
> so the rule's condition is checkable. The equivalent heading in both sibling artifacts was
> rewritten on 2026-08-24; this one was missed, the same heading-versus-body class the change
> record's § Sweep result already reported once.)*
>
> **✅ Amendment B APPROVED 2026-08-24** (`CR-2026-08-24-FOUNDATION-AMENDMENTS`).
> `probe_scope`, `measurement_status` and `declared_vs_observed_mismatches` now exist
> in `DeterminismRecord` — the contract carries **nine** fields, derived:
> `awk '/class DeterminismRecord/,/^$/' component-methods.md | grep -cE "^ +[a-z_]+: "` → `9`.
>
> *Superseded status, preserved:* the three fields *"**do not exist** in
> `DeterminismRecord` as approved at stage 2.6 — the contract carries **six** fields"*,
> and **Amendment B was PENDING and NOT approved**, so the record could carry a probe
> *result* with no recorded *scope* and no measurement *status* — exactly the ambiguity
> Q3 = C was chosen to eliminate. That ambiguity is now closed.
>
> **The prohibition this box carried is now DISCHARGED, because its condition has
> ended.** It read: *"binding now and not deferred: no artifact, manifest, registry
> row or report produced by this unit may state or imply that determinism has been
> measured for any operation class, **while the fields that would record the scope and
> status of that measurement do not exist**. Silence is the correct output, not an
> empty list presented as a clean result."* The fields now exist, so the condition no
> longer holds.
>
> **What replaces it is narrower, not nothing.** A statement that determinism was
> measured is permitted **only** where `probe_scope` records what was examined and
> `measurement_status` is `complete`. Where the status is `partial` or
> `not-yet-measured`, the output says so — it does not fall silent, and it does not
> present an empty list as a clean result. **R-06 is untouched**: an empty
> `nondeterministic_ops` remains no proof of determinism.

**Negative control.** Declare an operation as expected-nondeterministic in
configuration that the probe does not observe, and the inverse; both must surface
as mismatches rather than being silently reconciled.

**Acceptance.** **WS-17, TA-13** — **for the probe result only** (*superseded: `TA-13, TA-26`*). No row accepts the
scope or status fields, because no §16 or §19 row was added or amended to cover them: they are
uncovered **by design and permanently**, not pending.

> *(Reason corrected 2026-08-25 on adversarial reviewer finding M-4 (Major). **Superseded
> reason, preserved:** "because they are not yet in the contract." That was refuted by
> Amendment B, approved 2026-08-24 — `probe_scope` and `measurement_status` **are** in the
> contract, as the box above this rule states and derives (`DeterminismRecord` carries nine
> fields). **The conclusion is unchanged and still holds:** the two field names appear in no
> acceptance-row table anywhere in this workspace — only in `component-methods.md` and
> `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`. What changed is why: adding
> a covering row would require a new §19 row, and Amendment A — the only proposal to add rows
> for this unit — was **declined**, with §19 held at 36 rows and TA-37/TA-38 explicitly not to
> be added. So the gap is settled rather than provisional. This site carries no numeral, which
> is why the 2026-08-24 sweep — keyed to "six fields" and "two artifacts" — could not see it.)*

## R-07 — Registry status vocabulary is closed and validated at write time

**Rule (Q4 = D).** `status` is one of exactly **`started`**, **`completed`**,
**`aborted`**, **`failed`**. The writer rejects anything else.

**Constraint.** `aborted` and `failed` **require a non-empty `reason`**.

**Constraint — semantics are not interchangeable.** `aborted` is an intentional or
preflight-triggered stop; `failed` is an execution failure. They carry different
diagnostic stories and must not be collapsed.

**Why validated at write time.** Enum validation needs no read of prior rows, so it
costs nothing against the append-only guarantee. An unenforced vocabulary lets a
typo produce a row no reader groups correctly — and in an append-only file that
corruption is permanent.

**Negative control.** Attempt a write with an unknown status; it must be rejected.
Attempt `aborted` with an empty reason; rejected.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*

## R-08 — Registry writes never read the run history

**Rule (Q4 = D, explicit).** Registry writes are **append-only and do not require a
prior read of the run history.**

**Constraint.** The status **transition graph** is therefore enforced by a
**separate registry-integrity test**, not at write time.

**Why the separation matters.** A log whose write path depends on reading is no
longer a pure append — and that purity is the only reason append-only is
trustworthy. Q4 chose D over C precisely to keep it.

**Legal transitions per `run_id`:** `started → completed`, `started → aborted`,
`started → failed`.

**Rejected by the integrity test:** duplicate `started` rows, repeated terminal
statuses, any transition out of a terminal status, and unknown or malformed rows.

**Constraint — the WRITE MECHANISM, added 2026-08-28. §13.4's *atomic or append-safe* is a
requirement on how the row reaches disk, and it was specified nowhere.** Each registry row is
written as **one single write of one newline-terminated record, under append mode**, followed by a
**durability confirmation** before the writer returns. A durability failure is a
**`RegistryError`** naming the registry file and the violated expectation — never a warning
alongside a write reported as successful.

**Why this shape and no other, and why it costs R-08 nothing.** It is `governance-guards` R-25's
already-accepted pattern — *"`open_restricted` writes the `AccessRecord` **and flushes it**"*, with
*"a **durability failure** must **prevent the read**"* and a negative control asserting *"the log row
is **durable on disk**"*. Reusing it keeps one durability mechanism in the project instead of two.
Critically, **it costs no read**: a single append plus a flush consults no prior row, so R-08's
purity — *"append-only and do not require a prior read of the run history"* — survives **exactly**,
which is why **Q4 chose D over C** and why the temp-file-and-atomic-rename alternative is refused.
That alternative rewrites the whole file on every row, contradicts this rule's append-only design and
its stated rationale, scales badly, and reintroduces the overwrite risk **R-09** exists to exclude.
Recommendation 39 records it as *"not compatible with the accepted design"*, and this rule rejects it
on the same ground.

**Constraint — a TRAILING malformed row is a torn write, not corruption. Added 2026-08-28, and this
is the limb that matters most.** The integrity test **distinguishes position**:

| Where the malformed row sits | Read as | Reported as |
|---|---|---|
| **Last line of the file**, with no newline terminator, or truncated mid-record | A **torn write** — the process died during the append | **Reported, not rejected**: the test names it a torn final record and **names the run it belongs to**, recovered from whatever prefix of the record is legible (`run_id` is the first field for exactly this reason). The run **stays visible**, which is the NFR-AUD-01 obligation |
| **Any interior line**, or a trailing line that is newline-terminated and still unparseable | **Corruption or an illegal row** | **Rejected**, as this rule already specifies |

**Why the distinction is load-bearing rather than pedantic.** An `aborted` row is written *while the
process is dying* — which is precisely when a non-atomic append tears. This rule already lists
*"unknown or malformed rows"* among what the integrity test **rejects**, so **without this clause a
torn `aborted` row would fail the integrity test rather than preserve that run's visibility**: the
registry's own audit check would red-flag the file at the exact moment NFR-AUD-01 most needs the run
recorded, and the recovery path would be undefined. That is the asymmetry Recommendation 39 found —
flush and durability confirmation specified for the access log, nothing for the experiment registry —
and this unit's own artifacts had already identified the missing-`aborted`-row scenario as *"the
event **NFR-PHASE-01** and **NFR-AUD-01** most require recorded"* while adding *"Six adversarial
passes did not examine it."* A seventh did not either; a governance board did.

**Disclosed limit, not absorbed.** Durability semantics differ between the two governed platforms and
**Kaggle's are characterised nowhere in this design**. The confirmation step is therefore specified
as an obligation whose platform behaviour needs its own measured evidence before it is relied on at a
freeze gate. Recommendation 39 raises this against option 1 and it is recorded here rather than left
for 3.5 to discover.

**Constraint — when it runs.** Before TA-10 / G-09 acceptance, and **before
registry contents are relied on as audit evidence.**

**Negative control.** Synthesise each rejected sequence and assert the integrity
test fails on each.

**Negative control — the torn write, added 2026-08-28 per Recommendation 39.** Three cases, because
the clause has three outcomes. (1) **Truncate the final record mid-line** and assert the integrity
test **reports a torn final record and names its `run_id`**, does **not** reject the file, and leaves
that run visible. (2) Insert the **same malformed bytes as an interior line** and assert the test
**rejects**. (3) Kill the writer between the append and the durability confirmation and assert the
outcome is one of exactly two states — the record fully present, or reported as torn — and **never a
row reported written that is not on disk**, which is R-10's *"without claiming that an aborted record
was successfully written"* obligation reaching the durability layer.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*
**R-08 is the rule that carries §13.4's *atomic or append-safe* clause** *(citation fixed 2026-08-28;
see the correction note under R-20 for where it was previously mis-cited to R-07 and R-09)*.

## R-09 — A failed or aborted run stays visible

**Rule (NFR-AUD-01).** No registry entry is deleted, overwritten, or silently
re-run. A failed or aborted run **stays visible with its status and reason.**

**Constraint.** Status transitions **append a new row** referencing the run ID
rather than mutating the original.

**Why this holds by construction.** Removing a line would require rewriting a file
nothing rewrites. Two `started` rows with one `completed` is visible in the log, so
a silent rerun cannot hide.

**Negative control.** Attempt an in-place status mutation; it must be impossible
through the API. Assert an aborted run's row survives a subsequent successful run
of the same stage.

**Acceptance.** **TA-10, TA-21** — NFR-AUD-01 per story-map Table 1. *Superseded: `TA-10` alone.*

## R-10 — On an integrity failure, report honestly even when reporting fails

**Rule (Q5 = B).** The stage entry contract catches `IntegrityError`, **attempts**
to append an `aborted` registry row carrying the failure reason, and exits
non-zero.

**Constraint — the part that must not be simplified.** If the registry write
**itself** fails, the original exception is **preserved**, **both** the original
failure and the registry-write failure are reported to stderr, and the process
exits non-zero **without claiming that an aborted record was successfully
written.**

**Why this is a rule and not an implementation detail.** A handler that swallows
its own write failure produces the worst possible artifact: a run that failed, was
not recorded, and reported that it had been recorded. Every downstream audit would
read the absence as "no such run".

**Constraint.** On failure in steps 1–5 of the stage entry contract, the script
exits non-zero with a message naming the file and the violated expectation. **It
does not proceed with a warning** — these are integrity violations.

**Negative control.** Force a preflight raise with the registry path unwritable;
assert both failures reach stderr, the exit is non-zero, and no success is claimed.

**Acceptance.** TA-10, TA-23.

## R-11 — Release identity is the content hash; the label is not authoritative

**Rule (Q6 = D′, re-answered 2026-08-25).** The **content-derived SHA-256 is the authoritative
release identity.** The human-readable `dataset_version` label exists for review and citation
and is **explicitly not authoritative.**

> *(Rule text corrected 2026-08-25 on adversarial reviewer finding M-1, which was Major.
> **Superseded rule, preserved verbatim:** *"**Rule (Q6 = D).** The **content-derived SHA-256 is
> the authoritative release identity.** The **monotonic** human-readable label exists for review
> and citation and is **explicitly not authoritative.**"* Both halves were refuted by this
> stage's own current authority: Q6 was re-answered as **D′**, which states verbatim *"Drop
> 'monotonic.'"*, and R-12 twelve lines below already cited `Q6 = D′` — so two adjacent rules in
> one file cited different authorities for the same decision, and the earlier cited an answer
> that no longer said what it was cited for.
>
> **Why the 2026-08-25 sweep missed it.** Three sites asserted *"**R-11 is unchanged**"*. That
> was true of R-11's **substance** — the hash stays authoritative — and false of its **text**,
> and the assertion stood where the check should have been. Structurally the same
> self-certification as iteration-1's M-3, which this same file had already been corrected for.
> All three sites are now qualified to say substance-unchanged, text-amended.)*

**Constraint.** The authoritative hash is derived from a canonical manifest or
content representation that **excludes** the human-readable label, volatile
metadata, and any self-referential hash field.

**The canonical representation, specified** *(decided 2026-08-25 on adversarial finding M-1 of the
final confirming pass — the one finding of that pass that would mislead stage 3.5: four sites named
the exclusions and none enumerated what is included, whether `created_at_utc` is excluded, or the
serialization, so 3.5 would have had to invent the identity of every release. An engineering
decision with no scientific content, decided on the same basis as the sentinel and the
`IntegrityError` placement; `components.md` sets the precedent by deferring the phase-contract's
canonical set to 3.1 explicitly, and this stage is 3.1)*:

- **Included — twelve of the thirteen caller-supplied §13.3 fields:** `source_manifest_id`;
  `source_files` (its six FR-P1-01-2 items); the whole `processing` group; `schema_version`;
  `units`; `row_counts`; `exclusions_qc_summary`; `fold_ids`; `mask_ids`; `feature_set_ids`;
  `output_files`; `change_record_id`.
- **Excluded — exactly the three categories Q6's answer named, now bound to fields:**
  `dataset_version` (the human-readable label — derived *from* the hash, so including it would be
  circular); `created_at_utc` (**the volatile metadata** — re-releasing identical content at a
  different time MUST reproduce the same identity, or the idempotence property W-7 and R-12 assert
  is silently false); and `content_hash` itself (the self-referential hash field).
- **Serialization:** canonical JSON — UTF-8, lexicographically sorted keys at every level, no
  insignificant whitespace (RFC 8785 profile) — then SHA-256 over those bytes. Chosen because it is
  platform-independent byte-for-byte, which WS-20/TA-17's two-platform reproduction requires of the
  authoritative identity.
- **Array element order** *(added 2026-08-25 on confirming-pass finding F-1, which was Major and
  correct: RFC 8785 canonicalizes object keys and numbers but does NOT reorder arrays, and five of
  the twelve included fields are arrays — `source_files`, `output_files`, `fold_ids`, `mask_ids`,
  `feature_set_ids`. Unordered, a directory listing on Kaggle versus local yields two different
  canonical documents for byte-identical content, which is exactly the failure this specification
  exists to prevent)*: **before serialization, every array-valued included field is sorted
  lexicographically by the RFC 8785 serialization of its elements.** These five fields are
  set-valued in substance — collections of file records and identifiers whose order carries no
  meaning — so sorting loses nothing and removes the only platform-dependent input. A future
  genuinely order-bearing field must be declared as such at the freeze gate before it may join the
  included set unsorted.
- **The determinism control runs across two processes** *(same finding)*: control (1) is executed as
  serialize-in-one-process, re-serialize-in-a-fresh-process (and on the second platform where
  available), comparing bytes — an in-process double serialization cannot detect
  environment-dependent ordering, which is the defect it exists to catch.
- **Negative controls, content→hash** *(the direction R-12's existing controls did not cover)*:
  (1) serialize the same manifest twice → **byte-identical** hash; (2) change any included field →
  **different** hash; (3) change **only** `created_at_utc` → **same** hash, proving the idempotence
  claim rather than asserting it.

**Constraint.** A label/hash mismatch is an **integrity violation** — not a
discrepancy to reconcile.

**Why the hash wins.** Every integrity guarantee in this project is hash-based.
Making the label authoritative would put the weaker identifier in charge. The
project's gates are human-reviewed, so a citable label is needed; stating which one
wins is the part that must not be left implicit.

**Negative control**, owned by `tests/test_release_hashes.py` (TA-15) — **which already exists and
must be EXTENDED, not created** *(recorded 2026-08-25 on adversarial residual r-2 of the restored
budget)*. The file is present at 12,281 bytes and today covers `evidence/audit_evidence_2022-*`
byte integrity; `grep -c dataset_version` over it returns **0**. Its ownership is nonetheless
correct — TE §12's tree names it, TA-15's evidence column is *"Release manifest and
mutation-protection test"*, and `unit-of-work.md` § 1 places it in this unit's `Owns` — so the
control belongs here; what changes is that stage 3.5 adds to an existing module rather than
writing a new one. **A related upstream statement is now stale and is NOT edited here:**
`team-practices.md` § Testing Posture asserts *"No `tests/` directory exists yet in the
workspace"*, which is false. `org.md` reserves that file for the practices-affirmation gate, so it
is reported rather than corrected. Present a manifest binding
a `dataset_version` to a `content_hash` it does not correspond to; the check must reject it.

> **Where this check lives, stated because relocating it orphaned it** *(adversarial finding M-5,
> restored budget, 2026-08-25)*. The previous pass moved this control from the write path to "a
> presented manifest" without naming what performs it. `verify_release(manifest_path) ->
> Sequence[str]` is the only candidate in the approved contracts, and it **does not fit as
> written**: it returns the names of files whose *file hash* does not match and **never raises**,
> so it neither covers label/hash correspondence nor signals failure the way this control
> requires. Rather than invent a contract — which TE §18.3 forbids stage 3.5 from doing — the
> control is specified as a **test** obligation on `tests/test_release_hashes.py`, which is where
> TA-15 already lives and where a negative control needs no production entry point. **If runtime
> enforcement is wanted**, `verify_release` must be amended to check correspondence and to signal
> it; that is recorded as an amendment need in § Assumptions rather than assumed here.

> *(Control corrected 2026-08-25 on reviewer finding m-2. **Superseded control, preserved:**
> *"Bind a label to two different content hashes, and a content hash to two labels; both must
> raise."* Under Q6=D′ the label is a **function** of the content hash, so the second limb — one
> hash bound to two labels — is **unconstructable on the write path**: a function cannot produce
> two outputs for one input. What remains testable, and is what this control now asserts, is a
> **presented** manifest whose label and hash do not correspond, which is the case that actually
> arises when a manifest is read back or hand-edited. The first limb — one label on two different
> hashes — is subsumed by R-12's injectivity obligation and is testable only once the encoding is
> specified; see the open item in § Assumptions. ⛔ **Superseded 2026-08-30 by D-29** *(adversarial
> finding 3, Minor)*: **the encoding IS specified** — first 12 hex of `content_hash`,
> verify-on-write — so this limb is **testable now**. The open item it points at is no longer the
> encoding but the **release-population read-back mechanism**.)*

**Acceptance.** TA-15.

## R-12 — `dataset_version` is derived from the release `content_hash`

**Rule (Q6 = D′, re-answered 2026-08-25 — supersedes Q6 = D and moots FU-2 = D).** `dataset_version` is
**derived from the release's `content_hash`**. There is **no release ledger**, no allocation
step and no `ReleaseLedgerEntry`. ⛔ **AMENDED BY D-29 (2026-08-28) — the encoding IS specified.**
*(Corrected 2026-08-30 on adversarial finding 1, Critical: this Rule statement — R-12's canonical
definition, and the first thing an implementer reads — still carried the pre-D-29 text while the
AMENDED box **37 lines below it** already recorded the ruling, so the rule contradicted itself
within a single rule.)* **`dataset_version` is the FIRST 12 HEX CHARACTERS of `content_hash`,
with a verify-on-write uniqueness check.** That check is what establishes **injectivity in
substance**, so never-reuse is no longer open on the encoding and `verify_release` is discharged
in substance. ⚠ **The §18.3 stop-and-report obligation has MOVED, not lapsed**: stage 3.5 must
stop and report on **where the existing release population that verify-on-write reads back
lives** — the ledger that would have answered was declined at Amendment C, so the mechanism is
specified but not yet implementable, and three candidate surfaces are named at § Assumptions with
none chosen. **Superseded text preserved:** ~~"**The exact hash-to-label encoding is NOT
specified here**, because no approved artifact specifies one — and stage 3.5 must **not** choose
one either: per TE §18.3 it must stop and report rather than pick a default."~~

**Constraint.** `dataset_version` is never authoritative. Release identity is the
`content_hash` (R-11, unchanged). A `dataset_version` that does not match its release's
`content_hash` is an integrity violation — **rejected on the write path** by `write_release`, and
**detected on read-back by the test control only**, because no approved runtime contract performs
it: `verify_release` returns `Sequence[str]` and never raises. *(Scoped 2026-08-25 on adversarial
finding m-2 of the restored budget; the superseded wording — "…`content_hash` raises" — asserted
an unscoped raise that is true on the write path and unavailable on read-back, contradicting
§ Assumptions item 4, which records exactly that. Closing the read-back hole requires the
`verify_release` amendment listed there.)*

**Constraint — what determinism does and does not replace.** The derivation is a **pure function
of `content_hash`**: there is no allocation step and no state to consult. State exactly what that
buys, because the difference decides whether "never reused" holds:

1. **Idempotence — PROVIDED.** Identical content yields an identical `dataset_version`, by
   construction. This does dispose of the failure the superseded R-12 rejected a derived index
   for: that failure required *allocation from an index* — delete a release directory, the
   rebuilt index forgets the label, the next allocation hands it out again — and a pure
   derivation allocates nothing, so there is no index to forget. Deleting and rebuilding a
   release from the same content reproduces the same label, which is correct behaviour rather
   than a collision.
2. **Injectivity — NOT YET ESTABLISHED, and it is what "never reused" actually requires.**
   Never-reuse is *different content → different label*, which is injectivity, not idempotence,
   and a pure function is not injective in general. The reduction to a SHA-256 collision holds
   **only if the encoding preserves all 256 bits** — and Q6=D′ deliberately keeps the label
   **human-readable and citable**, so any label short enough to cite at a gate is a **lossy**
   encoding of the hash whose collisions are birthday-bounded on the bits it retains, not on 256.
   Since **the encoding is not specified here and stage 3.5 is forbidden to choose one**, the
   property never-reuse depends on is deferred to a decision no artifact is yet permitted to
   make. ⛔ **SUPERSEDED 2026-08-30 by D-29** *(marker added on adversarial finding 1, Critical —
   a live site the two prior repair passes did not reach)*: **the encoding IS specified** — the
   first 12 hex of `content_hash` with a **verify-on-write** uniqueness check — and that check
   is what establishes **injectivity in substance**, so never-reuse is **no longer deferred to an
   unmade decision**. The birthday-bound reasoning above remains correct about a *bare* lossy
   label; what it could not anticipate is that verify-on-write closes the gap at write time
   rather than in the encoding's bit-width. **What IS still deferred**: where the existing release
   population the check reads back lives — see § Assumptions.

> ## ✳ AMENDED 2026-08-28 — **D-29 SETTLES THE ENCODING AND ESTABLISHES INJECTIVITY**
>
> *(Project decision owner, 2026-08-28, under the recorded authority equivalence, on
> `GOV-2026-08-28-FD-01` **Recommendation 42**, board option 2 — the board's own
> recommendation. Recorded as **D-29** in `evidence/DECISIONS.md`.)*
>
> **`dataset_version` is the first 12 hexadecimal characters of the release's `content_hash`,
> and `write_release` verifies on write that the prefix is not already in use**, raising
> `ReleaseError` if it names a different `content_hash`. Three binding parts:
>
> 1. **Encoding — 12 hex characters** (48 bits) from the front of the SHA-256 `content_hash`
>    R-11 already makes the release's identity. Derived, never allocated. **No release ledger
>    is introduced** — the Amendment C reversal stands.
> 2. **A recorded collision bound**, so it can be checked rather than relied on: at 48 bits the
>    probability that any two of *n* releases share a prefix is approximately n² / 2⁴⁹ — about
>    **1.8 × 10⁻⁹** at n = 1,000 and **1.8 × 10⁻⁷** at n = 10,000. The bound says how rarely the
>    check below is expected to fire; it is **not** what establishes never-reuse.
> 3. **Verify-on-write.** `write_release` reads back the existing release population and
>    **refuses** a write whose 12-hex prefix already names a different `content_hash`. A
>    collision is **surfaced, never silently accepted** — the integrity-violation tier of
>    `team.md` § Code Style's two-tier posture.
>
> **What this changes in the numbered constraint above.** Item 2's **"Injectivity — NOT YET
> ESTABLISHED"** is **superseded**: injectivity is now **established by verify-on-write**, not
> by the encoding. The analysis in item 2 was correct and is preserved — a 12-hex label *is* a
> lossy encoding whose collisions are birthday-bounded on 48 bits, not on 256 — and D-29 does
> not pretend otherwise. It closes the gap by **checking** rather than by **arguing**, which is
> exactly the distinction item 2 was written to draw. The characterisation of the label as *"a
> citation device with idempotence, not an identity guarantee"* is likewise superseded: it is
> now a citation device with idempotence **and verified injectivity within the release
> population**.
>
> **Two of this rule's three open items close.** The **encoding** is specified; **injectivity**
> is established. The **`verify_release` amendment** (§ Assumptions item 4) is discharged **in
> substance**: the read-back hole is closed on the write path by the prefix check, so
> correspondence enforcement no longer depends on amending a function that never raises.
> `verify_release`'s own signature is unchanged and **no amendment to it is claimed** — what
> changed is that R-12 no longer *needs* one.
>
> **What is NOT changed, stated plainly.** Release **immutability** never depended on
> `dataset_version` and is untouched — it rests on R-13's directory-level overwrite refusal and
> R-11's identity-equals-`content_hash`. What was open, and is now closed, is **citation
> uniqueness**: a traceability property, not a mutation property.
>
> ⚠ **TA-15 is still NOT covered, and D-29 does not cover it.** Derived 2026-08-28:
> `tests/test_release_hashes.py` exists and its name matches §12's mandated module, but it
> exercises **none** of §13.3's manifest fields and does not test R-13's overwrite refusal. The
> closure evidence owed is that module extended to assert `write_release` refuses a second write
> to an occupied directory and leaves the original bytes unchanged; every §13.3 field present
> including `mask_ids`, `feature_set_ids`, `row_counts` and `exclusions_qc_summary`; and
> `dataset_version` corresponding to its release's `content_hash` under this encoding. **No
> artifact may read TA-15 as satisfied until that lands.**
>
> **Negative controls added by D-29, four.** A release whose `dataset_version` is not the first
> 12 hex of its own `content_hash` → **`ReleaseError` on the write path**. A write whose 12-hex
> prefix already names a **different** `content_hash` → **`ReleaseError`, refused**. A write
> whose prefix matches an existing release with the **same** `content_hash` → that is
> idempotence, and **R-13's directory-level refusal** is what fires, not a prefix collision. A
> `dataset_version` of any length other than 12 → **`ReleaseError`**.
>
> **Limitation.** The collision bound is arithmetic, not measurement: no release exists yet, so
> the population is projected rather than observed. If it ever approaches those figures, the
> prefix length is the parameter to revisit, and revisiting it is a **fresh D-number**, not an
> implementation choice (TE §18.2).


> *(Corrected 2026-08-25 on adversarial reviewer finding M-3, which was Major and which refuted
> a claim this design had been asserting as settled. **Superseded text, preserved verbatim:**
> *"**Constraint — determinism, which is what replaces the ledger's guarantee.** … Two
> consequences follow, and they are the reason the never-reused obligation survives the
> reversal: … 2. **A label bound to two different contents reduces to a SHA-256 collision.** It
> is not reachable by any bookkeeping error, because the label is a function of the hash."*
>
> **Why that was wrong.** It proved idempotence and then claimed never-reuse, which is the
> converse. The error was load-bearing rather than cosmetic: this argument was the **sole**
> stated reason Q6=D′ could drop *"monotonic"* while keeping *"never reused"*. The honest
> position is the one this design already takes about monotonicity — state what the mechanism
> provides, and record what it does not as an obligation on whoever specifies the encoding. That
> obligation is now an explicit open item in § Assumptions.)*

**Negative controls.** Three, replacing the ledger-specific set. **None of them establishes
injectivity**, and that limit is stated rather than left for a reader to notice:

- **Correspondence.** Present a manifest whose `dataset_version` does not correspond to its
  `content_hash`; it must be refused. *(This is what discharges FU-2's inconsistent-mapping
  obligation in the form Q6=D′ leaves available.)*
- **Determinism.** Derive twice from the same `content_hash` and require **byte-identical**
  results — asserted, not assumed, the posture NFR-DET-01 takes everywhere else.
- **Non-degeneracy.** Derive from two different `content_hash` values and require **different**
  results. **This catches a degenerate (constant) encoding and nothing more.** It is a
  two-sample test: a **truncating** encoding passes it for essentially every pair while still
  admitting collisions, so it must not be cited as evidence of never-reuse. **Name it
  "non-degeneracy", never "injectivity"** — three earlier sites called it the latter, which is
  the claim it cannot support (adversarial finding m-1, restored budget, 2026-08-25).

**Obligation on whoever specifies the encoding**, recorded here so it travels with the rule: the
encoding must be **injective over the release population in scope**, or its collision bound must
be stated and accepted at a gate. Until then `dataset_version` is a **citation device with
correspondence and determinism guarantees only**, and no artifact, manifest or report produced by
this unit may state or imply that release labels are never reused.

> ## ⚠ WHAT THIS RULE GIVES UP — ONE CAPABILITY DROPPED, AND ONE OBLIGATION STILL OPEN
>
> *(Heading corrected 2026-08-25 on adversarial finding M-1 of the eighth-redo iteration 2.
> **Superseded heading, preserved:** "⚠ WHAT THIS RULE GIVES UP — ONE CAPABILITY, NO LONGER AN
> UNMET OBLIGATION". True when written, above an item 1 that then read "SATISFIED", and stale from
> the moment that item was corrected to "NOT ESTABLISHED" — refuted twenty-six to eighty-three lines
> below by this rule's own body and by § Assumptions' OPEN items. **Why the previous sweep reported
> zero live sites: it matched the words *never-reuse*, and this heading contains neither.** That is
> the seventh appearance of this class in this unit, and the durable remedy applied throughout is to
> name what is open rather than count or characterise it.)*
>
> This rule was **rewritten on 2026-08-25** when the project decision owner **declined
> Amendment C as drafted**, reversing its 2026-08-24 approval. **Superseded rule, preserved
> verbatim:**
>
> > *"**R-12 — Labels are allocated from a durable ledger and never reused.** **Rule (Q6 = D,
> > FU-2 = D).** Human-readable labels are allocated from a **durable, append-only release
> > history**, not solely by scanning existing directories. **A previously assigned label is
> > never reused.** **Constraint.** The ledger is **separate from `experiment_registry.jsonl`**.
> > **Why not a derived index.** Q6 ruled out directory scanning by name. A derived index has
> > the same defect: delete a release directory and the rebuilt index forgets the label, so the
> > next allocation reuses it. **Why not folded into the registry.** Q4's transition graph would
> > have to filter by row kind before applying its rules, and a rule whose readers must filter
> > first is a rule that quietly stops applying to the rows it was written for. **Negative
> > control.** Delete a release directory and attempt a fresh allocation; the previously used
> > label must still be refused."*
>
> **Read that superseded text against the replacement — and note where its objection does not
> transfer.** The superseded rule rejects a *derived index*, and its stated defect is that a
> rebuilt index forgets a label so **the next allocation reuses it**. That defect is a property
> of **allocation from state**, not of derivation: a pure function of `content_hash` allocates
> nothing and consults nothing, so there is no index to forget. The objection was sound against
> the mechanism it was written about and **does not carry** to this one. Of the two Q6=D
> obligations, therefore:
>
> 1. **Never-reused — NOT ESTABLISHED. Contingent on an encoding that does not yet exist.**
>    ⛔ **SUPERSEDED 2026-08-30 by D-29 — never-reuse IS established in substance.** *(Marker
>    added on adversarial finding 1, Critical: a live site the two prior repair passes did not
>    reach.)* The encoding now exists — first 12 hex of `content_hash` — and its **verify-on-write**
>    uniqueness check is what establishes **injectivity**, so this item reads **ESTABLISHED IN
>    SUBSTANCE**, not "NOT ESTABLISHED". `verify_release` is discharged in substance with no
>    signature change claimed. ⚠ **Still open, and now the §18.3 stop-and-report point:** where
>    the existing release population the check reads back lives — the ledger that would have
>    answered was declined at Amendment C. **TA-15 remains NOT covered** regardless.
>    *(Corrected 2026-08-25 on reviewer finding M-3. **Superseded claim, preserved:** *"**Never-reused
>    — SATISFIED, by a different mechanism.** Not by durable state but by determinism: identical
>    content derives an identical label by construction, and a label bound to two genuinely
>    different contents reduces to a **SHA-256 collision**, unreachable by any bookkeeping
>    error … Three replacement negative controls are stated above, and they are **stronger than a
>    correspondence check alone**: correspondence, derivation determinism, and injectivity against
>    a degenerate encoding."*)* That argument proved **idempotence** and claimed **injectivity**,
>    which is its converse. The collision reduction needs an encoding faithful to all 256 bits,
>    and Q6=D′ keeps the label human-readable and citable — necessarily lossy. The third control
>    catches only a **degenerate** encoding, never a **truncating** one. What *is* true: the
>    superseded negative control (delete a directory, attempt a fresh allocation, expect refusal)
>    is **inapplicable** rather than failed, because nothing allocates, and reproducing the same
>    label from the same content is now correct. **Never-reuse is recorded as an obligation on
>    whoever specifies the encoding**, listed as an open item in § Assumptions, and nothing this
>    unit produces may claim it holds until then.
> 2. **Monotonicity — NO LONGER REQUIRED, and deliberately given up.** A content-addressed
>    label cannot express ordering, and no test recovers it: monotonicity is information about
>    *sequence*, which a function of content alone does not carry. Because that is a property of
>    the mechanism rather than of its implementation, it could be resolved only by restoring
>    durable state — which the ruling forbids — or by changing the requirement. **The
>    requirement was changed: Q6 was re-answered on 2026-08-25 as D′, dropping "monotonic"**,
>    put to the owner explicitly rather than assumed. So this is **not an unmet obligation** and
>    **not an open gap against an answered question** *on monotonicity*; the rule is compliant with Q6=D′ **on monotonicity, which D′ dropped — but NOT on never-reuse, which D′ retains and this design does not establish** *(narrowed 2026-08-25 on adversarial finding M-1/M-3 of the restored budget; the unqualified claim "fully compliant with Q6=D′" appeared at five sites and was false at all five)*.
>
>    **What it costs, disclosed rather than absorbed:** release labels can no longer be
>    **ordered**. A reviewer citing two labels at a human-reviewed gate cannot tell from the
>    labels alone which release came first — that must be read from the run record or the
>    experiment registry, both of which carry timestamps and `run_id`. Nothing else in the
>    design depended on label ordering.
>
> **FU-2's integrity obligation is discharged, and FU-2 itself is moot.** FU-2 existed only to
> locate the ledger Q6=D required; with Q6=D′ there is no ledger to place. Its
> inconsistent-mapping obligation is carried by the three negative controls above. Its
> duplicate-and-reused-label obligation is **vacuous**: with no rows there is nothing to
> duplicate, and with the label a function of the hash, reuse across genuinely different
> content would reduce to a SHA-256 collision **only under a 256-bit-faithful encoding, which a citable label is not — this clause is the withdrawn reduction and is retained only as the superseded record** *(disarmed 2026-08-25 on adversarial residual r-1 of the restored budget; R-12 disarms its own instance of the same sentence, and this one was left armed. The conclusion below is independently supported and unaffected.)*. **So FU-2's obligations are covered — but Q6=D′'s
> never-reuse obligation is NOT**, and this sentence previously said otherwise. *(Corrected
> 2026-08-25 on adversarial finding M-3 of the restored budget; superseded wording preserved: "So
> no obligation of either question is left uncovered.")* The SHA-256-collision reduction quoted
> just above is itself the withdrawn argument — it needs a 256-bit-faithful encoding, and a
> citable label is lossy. **Never-reuse is open**, on whoever specifies the encoding.
>
> **This is a deliberate owner override, not an oversight.** The ruling was given after the
> full conflict was put to them: that `ReleaseLedgerEntry` predated Amendment C, that its
> authority was their own **Q6=D** and **FU-2=D** answers, that a `content_hash`-derived
> `dataset_version` is **Q6 option C which they had read and declined** on exactly the
> monotonicity reasoning above, and that executing the reversal would delete an entity and
> amend a workflow. They chose the full reversal with those consequences stated.
>
> **The two loose ends this paragraph named have since been closed — but the reversal did not leave this rule clean.** *(Corrected 2026-08-25 on adversarial finding M-2 of the restored budget; superseded wording preserved: "**Both loose ends have since been closed, and neither by this stage's own choice.**")* Two OPEN items in this file's own § Assumptions exist **because** of this reversal — the `dataset_version` encoding and its injectivity — and this rule's own box states plainly that never-reuse is open.
> Monotonicity was unresolvable here by construction, so **Q6 was re-presented and re-answered
> as D′ on 2026-08-25**, dropping the requirement — the owner's decision, taken explicitly, not
> a silent amendment. And the **upstream correction is no longer owed**: `unit-of-work.md` § 1
> `Owns` and `services.md` were first *reported* rather than edited, because this stage's scope
> control forbade touching an approved Inception artifact; the owner authorised the edits
> explicitly and both were corrected on 2026-08-25 with their superseded wording preserved.
> **What still stands open against this rule, from that reversal — three items, not two** *(count corrected 2026-08-25 on adversarial finding m-3 of the eighth-redo iteration 2: this roll-up named two while this rule's own Constraint names a third, "Closing the read-back hole requires the `verify_release` amendment" — a roll-up narrower than the body it summarises)*: the `dataset_version` **encoding** (unspecified, and stage 3.5 forbidden to choose one), its **injectivity**, and the **`verify_release` amendment** that would close the read-back hole, on which never-reuse depends. ⚠ **SUPERSEDED 2026-08-28 by D-29** (`GOV-2026-08-28-FD-01` Rec 42, board option 2, owner-approved): the **encoding** is specified — the first **12 hex** of `content_hash` — and **injectivity is established by verify-on-write**, `write_release` refusing a prefix that already names a different `content_hash`. The **`verify_release` amendment** is discharged in substance (the read-back hole closes on the write path) with **no change to that functions signature claimed**. **No release ledger is introduced.** Release immutability never depended on any of this. ⚠ **TA-15 remains NOT covered** — `tests/test_release_hashes.py` still exercises none of §13.3s manifest fields and not R-13s overwrite refusal. *(Corrected 2026-08-25 on adversarial finding M-2 of the restored budget. **Superseded wording, preserved:** "Nothing about the Amendment C reversal now stands open against this rule." It was false when written and sat eighteen lines below this rule's own "**Never-reuse is open**, on whoever specifies the encoding" — the same sentence had already been superseded in the Q&A and was left standing here.)*
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-12 was amended, not removed.

> **⛔ Amendment C DECLINED AS DRAFTED 2026-08-25.** The box below records the 2026-08-24
> approval that ruling reversed. It is preserved as the dated record and is **not** the current
> state — in particular its *"three artifacts, one authoritative"* reading of `services.md` is
> now wrong at two. **That correction has since been made** — `services.md` reads "Two artifacts, one authoritative" and the ledger row is removed, superseded wording preserved.
>
> **✅ Amendment C APPROVED 2026-08-24** *(superseded 2026-08-25)* (`CR-2026-08-24-FOUNDATION-AMENDMENTS`).
> *Superseded status, preserved:* *"Amendment C is PENDING and NOT approved. The ledger
> is absent from `unit-of-work.md` § 1 `Owns` and from `services.md` § Run record and
> registry ("Two artifacts, one authoritative"). Both approved artifacts are
> unedited."* Both have been annotated in place on the owner's approval;
> `services.md` now reads **three artifacts, one authoritative**.
>
> **Authority: Q6=D and FU-2=D.** Q6=D requires a *monotonic, human-readable* label
> alongside the authoritative hash — chosen over option C's *"version derived from the
> manifest hash"* — and FU-2=D names the durable append-only ledger with its ownership
> and append behaviour. A monotonic label needs durable state, which is why the
> directory scan R-12 rejects cannot serve.
>
> **No TE §12 amendment was needed** — `artifacts/registry/` is already enumerated and
> the tree carries zero file-level entries inside `artifacts/`.

**Acceptance.** TA-15 for the release. **No §16/§19 row accepts `dataset_version` derivation**
— and none is sought: Amendment A, which would have added acceptance rows for this unit's
uncovered obligations, was **declined** on 2026-08-24, with §19 held at 36 rows and TA-37/TA-38
explicitly not to be added. *(Superseded 2026-08-25: "**No §16/§19 row accepts the ledger
itself** … The ledger's own integrity is asserted by the independent test FU-2=D requires, not
by an acceptance row." There is no ledger, so the independent ledger integrity test FU-2=D
required does not exist. **Its inconsistent-mapping obligation is carried** by this rule's
correspondence control; its duplicate-row obligation is **vacuous** with no rows to duplicate.
What is **not** carried is never-reuse, which needs injectivity over the label encoding — recorded
as an open item in § Assumptions rather than as coverage. *(This sentence itself was corrected
2026-08-25 on reviewer finding M-2, second pass: it previously read "no longer exists either — a
loss of coverage this reversal creates and does not replace, and one more item for the stage
gate", which contradicted § Assumptions' own RESOLVED finding on the same obligation.)*)*

## R-13 — A release directory is never overwritten

**Rule (TE §13.3, TA-15).** `write_release` **rejects an output directory that
already contains a release** and **never overwrites existing release content.**

**Constraint.** Repeated writes are **not** silently treated as successful. That
behaviour would require explicit authorisation through the project's change-control
process, and none has been sought.

**Negative control.** The mutation-protection test: write a release, attempt a
second write to the same directory, assert `ReleaseError` and assert the original
bytes are unchanged.

**Acceptance.** TA-15.

## R-14 — `foundation` declares credential names and never touches a value

**Rule (Q8 = D, FU-3 = A).** Required credential environment-variable **names**
live in one centrally reviewed stage/provider mapping. `foundation` **owns or hosts**
that mapping and **does not read, return, log, serialize, interpolate, or persist
any credential value** — not in `resolve_platform_roots`, not in any
foundation-layer diagnostic.

**Constraint — scope of the precondition.** Only stages that **actually require
authenticated provider access** apply the credential-presence check. Credentials
are **not** required for unrelated stages, for public providers, or for
`foundation` initialization itself.

**Constraint — what a presence check does and does not prove.** Checking that an
environment-variable **name** is present **does not** prove its value is non-empty,
valid, or authorized. The provider client performs value validation **without
exposing the secret.** This is stated because a presence check that is mistaken for
a validity check is worse than no check: it reports readiness that does not exist.

**Negative control.** Synthetic canary secrets in the environment, in a config, in
a log line and in an artifact; the secret scan must find each. Assert no
foundation-layer return value or log line contains a canary. Remove a required name
and assert the failing message identifies it by name.

**Constraint — a precondition, not a claim.** The `.gitignore` credential deny-list
**must exist before the first relevant commit.** `NFR-SEC-01` and `TA-22`
compliance is **not claimed until the required checks have actually passed** — and
`evidence.md` records NFR-SEC-01 as **not satisfied in this workspace today**, so
this is a rule being built rather than one being ratified.

> ## ✳ DATED CLAUSE, 2026-08-28 — THE DENY-LIST PRECONDITION IS NOW SATISFIED; THE REQUIREMENT IS NOT
>
> *(Added on the owner's ruling on `GOV-2026-08-28-FD-01` **Recommendation 49**, option 1. **The
> precondition framing above is preserved unchanged and is not weakened**, and **NFR-SEC-01 and
> TA-22 remain unclaimed** — the board asked explicitly for the conservative half to stand. What was
> dated is the attached status sentence.)*
>
> **The deny-list precondition was satisfied as of 2026-08-28.** Re-verified independently by this
> unit on that date, not carried from the finding's text:
>
> ```
> .gitignore § "Credentials and secrets" (lines 62-89) carries:
>   .env  .env.*  (!.env.example)  *.key  *.pem  *.p12  *.keystore
>   kaggle.json  .netrc  _netrc  credentials  credentials.*
>   .aws/credentials  id_rsa*  secrets.yaml  secrets.yml  .madrigal_auth
>
> git ls-files filtered for credential-shaped names ...............  0 files
>
> bun scan over every tracked file, 5 patterns
>   (AKIA[0-9A-Z]{16}; PEM private-key headers; xox[baprs]-;
>    ghp_[0-9A-Za-z]{36}; AIza[0-9A-Za-z_-]{35}):
>   tracked files listed ......................................... 1158
>   tracked files read as text ................................... 1158
>   pattern hits .................................................    0
> ```
>
> So the §10 mechanism the rule above names as a precondition — *"environment configuration excluded
> from version control"* — **now exists**, and the exposures the superseded status sentence was
> written against are **not visible in the tracked tree today**.
>
> **NFR-SEC-01 and TA-22 stay UNCLAIMED, and this clause does not advance either.** TA-22's scope is
> wider than the tracked working tree: it additionally requires a secret scan over the repository
> **history**, configurations, logs and artifacts. **None of that was scanned** — the derivation above
> is `git ls-files` at one commit, so a credential committed and later removed would be invisible to
> it. The board stated the same limit and *"explicitly does not conclude NFR-SEC-01 is satisfied"*.
> **The requirement therefore remains unclaimed pending the full-scope scan**, which is scheduled work
> for TA-22 and not this stage's to run: a history scan needs tooling and an owner decision, and
> Recommendation 49 records the two acts as *"sequential, not competing"*.
>
> **This clause carries its own date because it will itself go stale if the tree changes.** It is
> tied to the **deny-list's existence** rather than to a scan result, which is the durable half; the
> zero-hit scan is evidence as of 2026-08-28 and nothing more. `evidence.md`'s own NFR-SEC-01 status
> line is the **project owner's** to refresh or reaffirm — this stage may not edit `evidence/`, so the
> attribution in the sentence above stands and is corrected here rather than there.

**Acceptance.** TA-22 — **and TA-22 is NOT claimed as satisfied**, per the dated clause above.

## R-15 — Only `foundation` reads `configs/`, and nothing reads the restricted root

**Rule (`unit-of-work.md` § 1 boundary).** `foundation` is the **only** unit that
reads `configs/`. Everything downstream receives resolved values, never a path into
`configs/`.

**Rule (§ Shared resources, unqualified).** `foundation` is, with `acquisition`,
one of two units permitted to construct a path into `evidence/` — **except
`evidence/locked_test_restricted/`, which only `src/data/locked_test.py` may
reach.** *"Nothing else may construct a path into it."*

**Why the carve-out is absolute.** D-15 records that the restricted root is a
**governance boundary, not an access control** — it holds only while exactly one
code path reaches it. A second path does not weaken it slightly; it ends it.

**Negative control.** A static check asserting no `foundation` module constructs a
path containing `locked_test_restricted`.

**Acceptance.** Contributes to TA-18 via `governance-guards`; **`foundation`'s own
side is the absence of a path**, which the check above proves.

## R-16 — No machine path enters a governed config

**Rule (REQ-ENG-3, ADR-07).** No machine path may enter any of the four governed
configs, so **moving a directory never changes a governed hash.**

**Constraint.** Machine paths live in `ConfigSnapshot.resolved_roots`, resolved
from the environment at run time.

**Negative control.** A test asserting no value in any of the four configs parses
as an absolute path, and that relocating the workspace leaves all four config
hashes unchanged.

**Acceptance.** **TA-03, TA-26** — REQ-ENG-3 per story-map Table 1. *Superseded: `TA-02`.*

## R-17 — Every module and script carries a purpose/inputs/re-run docstring

**Rule (`project.md` § Mandated, affirmed practice).** Every script and module has
a docstring stating its **purpose**, its **inputs**, and its **re-run /
reproducibility behaviour.**

**Negative control.** A test asserting each module in this unit has a module-level
docstring containing all three elements.

**Acceptance.** **No acceptance row.** The docstring rule is an affirmed practice (`project.md` § Mandated, interview Q12-C), not one of this unit's sixteen requirements, so it is outside the "2 of 16" count and has no §16/§19 row to cite. *Superseded: `TA-01`, which accepts the repository skeleton and does not check docstrings.*

## R-18 — The registry row is TE §13.4's twenty columns, asserted at write time

*(Rule ADDED 2026-08-28 on the owner's ruling on `GOV-2026-08-28-FD-01` **Recommendation 10**,
option 1, and **Recommendation 1**/**Recommendation 3** for the two destination columns. Before this
rule the registry schema was **TE §13.1's environment lock** — twelve designed fields — while
`requirements.md` FR-P1-05-13's pass/fail criterion is TE **§13.4**'s twenty columns. Two different
sections of the Technical Environment, and the requirement's criterion had **no design at all**.)*

**Rule (FR-P1-05-13, TE §13.4).** Every `RegistryEvent` row carries **TE §13.4's twenty columns**.
The set is **derived from the authority and printed**, never transcribed from prose:

```
TE:821-826, the §13.4 column block, split on comma and newline  ->  20

 1 run_id                    11 feature_set_id
 2 started_at_utc            12 model_id
 3 completed_at_utc          13 hyperparameters_json
 4 status                    14 seed
 5 code_commit               15 validation_metric_name
 6 environment_lock_hash     16 validation_metric_value
 7 platform                  17 artifact_manifest_path
 8 dataset_version           18 prediction_hash
 9 fold_id                   19 locked_test_accessed
10 mask_id                   20 notes
```

`requirements.md` FR-P1-05-13 enumerates the identical twenty and states the criterion verbatim:
*"a schema assertion confirms all twenty columns exist and that `code_commit` and
`environment_lock_hash` are populated on every row."*

**Constraint — the twenty are a FLOOR, not a closed set.** TE §13.4 reads *"CSV or JSONL,
**including**:"*, so the twenty are a minimum. Three further fields are required by authorities
outside the column block and are **named as extensions rather than smuggled into the twenty**, so the
twenty-column assertion stays literally checkable:

| Extension field | Required by | Why it is not one of the twenty |
|---|---|---|
| `reason` | §13.4's own prose — *"Failed and aborted runs remain visible with **status and reason**"* — and **R-07**, which requires it non-empty on `aborted` and `failed` | The prose states it; the column block does not list it. `notes` is a free-text column and **must not be repurposed** to carry it, or R-07's non-empty check has nothing to bind to |
| `prior_period_exposure` | **TE §7.0B** — *"The locked-test guard **shall record** `prior_period_exposure=true`"* — a positive obligation, and `requirements.md` FR-P1-05-12 repeats it | Named in §7.0B, absent from §13.4's block |
| `exploratory` | **Vision §8.3** / FR-P1-05-14, and **R-20** below, which derives it | Named in Vision, absent from §13.4's block |

**Constraint — `prediction_hash`'s DESTINATION is this row, and `07` may not be its writer.**
`prediction_hash` (column 18) is where the one-shot locked-test prediction receipt lands.
`models-and-baselines` is being amended in parallel to make **`scripts/06_train_and_predict.py`** the
writer of a `PredictionHashReceipt` (`prediction_path`, `sha256`, `recorded_at_utc`, `run_id`,
`partition_id`), **durably flushed before `06` exits**, with `06` refusing to exit holding a `DEC`
prediction file and no receipt. **This unit's side of that contract is stated here:**

1. The receipt's **destination is the registry row** — its `sha256` becomes column 18
   `prediction_hash`, joined by `run_id`;
2. **neither `scripts/07_evaluate_and_report.py` nor the bootstrap may be the writer.** The registry
   writer **refuses** a `prediction_hash` presented by the process that computes a metric over that
   prediction. Writer and reader stay in **different processes**, which is the only thing that makes
   *"the receipt precedes the metric"* mean anything;
3. `prior_period_exposure` is likewise **recorded by the locked-test guard** (TE §7.0B names the
   guard, and `governance-guards` owns it) and **carried** by this row. This unit is the destination,
   not the source.

**Why limb 2 is a rule and not an implementation note.** Recommendation 1's stated hazard is not the
deadlock — a `DEC` metric that raises forever is fail-closed and not itself a breach — it is **the
repair**: *"the cheapest way to clear the deadlock at implementation time is to write the receipt
inside `07_evaluate_and_report.py`, in the same process that computes the metric, which makes 'the
receipt precedes the metric' self-certifying and turns the control into a formality that passes its
own test."* A refusal in the registry writer is what makes that repair unavailable.

**Constraint — Phase 1's value of `prior_period_exposure` is `false`, and that is not a defect.**
TE §7.0B's `true` is about the **Phase 2** December run, which replicates a fixed protocol over
timestamps Phase 1 has already exposed. Phase 1 **is** the first exposure, so its rows carry `false`.
The column is designed now because the field must exist before Phase 2 can populate it and because
the phase-transition hash freeze forbids adding one later; **stating the Phase 1 value explicitly
stops an implementer writing `true` on a Phase 1 row to satisfy §7.0B's *"shall record"*.**

**Constraint — what happens to §13.1's eight-field environment lock.** It is **not displaced**.
§13.4 column 6 is `environment_lock_hash` — a **hash over** the lock, not the lock itself — so the
eight fields **R-09**/`RunRecord` already specify remain the lock's content and the hash is computed
over them. **REQ-ENG-10's criterion is unchanged** (*"A registry row exists carrying all eight
fields"*), and it stays **untested by design** under the declined Amendment A. Both readings coexist:
the `started` row carries the eight fields **and** their hash, and the schema assertion below checks
the twenty columns plus the extensions, not the eight.

**Negative controls — four.** (1) Present a row missing any one of the twenty columns and assert the
schema assertion **fails, naming the absent column** — run once per column, so the assertion cannot
pass by checking a subset. (2) Present a row whose `code_commit` or `environment_lock_hash` is empty
and assert it **fails**, FR-P1-05-13's second criterion being population and not mere presence.
(3) Present a `prediction_hash` from the process that computes the metric over that prediction and
assert the writer **refuses** — the limb-2 control, which must fail *at the write*, not later at an
audit. (4) Present a Phase 1 row carrying `prior_period_exposure = true` and assert it is
**rejected**, so §7.0B's obligation cannot be discharged in the wrong phase.

**Acceptance.** **TA-10** — FR-P1-05-13 per story-map Table 1, whose *"schema assertion confirms all
twenty columns exist"* criterion this rule is the design for. **TA-21** for the traceability limb.
**No new §19 row is sought**: Amendment A was declined and §19 is held at 36 rows.

## R-19 — `AccessRecord` and `RegistryEvent` join on `run_id`, with orphan detection both ways

*(Rule ADDED 2026-08-28 per **Recommendation 10**'s closure evidence — *"a stated `run_id` join"*.
The finding derived that **zero of the 48 `functional-design` artifacts names both `AccessRecord` and
`RegistryEvent`**: the intersection was empty, so two record surfaces existed with **no stated
relationship at all**.)*

**Rule (Vision §8.3, TE §13.4).** `AccessRecord` — owned by **`governance-guards`**, fields
`run_id`, `retrieved_at_utc`, `scope`, `purpose`, `performance_inspected`, `locked_test_accessed`,
`authorization` — and `RegistryEvent` **join on `run_id`**, which both already carry. `run_id` is the
only key: neither timestamps nor file paths are used, because both are reconstructable-looking and
neither is stable.

**Constraint — orphan detection runs in BOTH directions, and each direction means something
different:**

| Orphan | Reads as | Treatment |
|---|---|---|
| An `AccessRecord` under `RESTRICTED_ROOT` whose `run_id` matches **no** `RegistryEvent` | A December access by a run the experiment registry does not know about | **Integrity violation.** `RegistryError`, naming the `run_id` and the access record. This is the unregistered-access case, and it is the one the audit exists to find |
| A `RegistryEvent` with `locked_test_accessed = true` whose `run_id` matches **no** `AccessRecord` | A run claiming December access with no logged access — either the flag is wrong or the log-then-read ordering of `governance-guards` R-25 was bypassed | **Integrity violation.** `RegistryError`, naming the `run_id` |

**Why both directions, and why a derived flag would have been weaker.** Recommendation 10 permits a
join-only design (option 2) *"**only** with orphan detection in both directions; without it a derived
flag is weaker than the column it replaces."* This design takes **option 1** — `locked_test_accessed`
is a real column on the row (R-18, column 19) — **and** the join, so the two surfaces are
**reconciled** rather than one being derived from the other. A single-direction check would catch a
missing registry row and miss a fabricated flag, or the reverse.

**Constraint — the reconciliation is a test, not a write-path read.** It runs with the
registry-integrity test of **R-08**, at the same times: before TA-10 / G-09 acceptance and **before
registry contents are relied on as audit evidence**. It is emphatically **not** a write-time check —
that would make the registry write depend on reading the access log and destroy **R-08**'s purity,
which **Q4 = D** exists to protect.

**Constraint — the five retrospective access rows are expected orphans and must not be laundered.**
`governance-guards` R-25 records that the access log already holds **five retrospective rows**
predating the guard (`evidence/experiment_registry.md` rows 3, 4, 5, 8 and 9), and
`GOV-2026-08-28-FD-01` **Recommendation 31** records *one possible unauthorized access as expressly
unresolved*. The reconciliation **reports these as known pre-guard orphans with their reason**, and
**never suppresses them and never back-fills a registry row to clear them** — a fabricated row would
be the `evidence/experiment_registry.md:39-41` reconstruction failure repeated deliberately, where
*"a reviewer reconstructing custody from this log found two events while the manifests showed four."*
**Recommendation 31 is `governance-guards`' and the owner's to close, not this rule's**; this rule
only guarantees the orphans stay visible.

**Negative controls — three.** (1) Synthesise an `AccessRecord` under `RESTRICTED_ROOT` with a
`run_id` absent from the registry and assert **`RegistryError`** naming that `run_id`. (2) Synthesise
a `RegistryEvent` with `locked_test_accessed = true` and no matching `AccessRecord` and assert
**`RegistryError`**. (3) Run the reconciliation over the **five known retrospective rows** and assert
they are **reported with their pre-guard reason and not cleared**, so a future clean run cannot be
achieved by hiding them.

**Acceptance.** **TA-10** (registry integrity) and **TA-18** via `governance-guards` — the
*"guard test and access-log sample"* evidence. **`foundation`'s side is the registry half of the
join**; the access-log half is `governance-guards`'.

## R-20 — `exploratory` is DERIVED in the registry writer, never passed by a caller

*(Rule ADDED 2026-08-28 on the owner's ruling on `GOV-2026-08-28-FD-01` **Recommendation 12**,
option 1. The finding: Vision §8.3's exploratory label *"has a reader in one unit and a writer in
none"* — `regimes-diagnostics-reporting` R-128 asserts the label's presence, states that *"a
post-access run reported without it **fails**"*, and explicitly routes the **writer** to the gate:
*"Which surface **writes** the label is the registry writer's design
(`foundation`/`inventory-and-registry`) and is **routed to the gate rather than annexed**."*
**This unit is the registry writer.** Derived in the finding: "exploratory" appears in **1 of 12
units** and **0** times in either named writer candidate.)*

**Rule (Vision §8.3, FR-P1-05-14).** `RegistryEvent.exploratory` is **computed by the registry
writer** from the run's own `started_at_utc` against the access log, and is **never a caller
argument**. The writer sets it `true` when `started_at_utc` **postdates the earliest `AccessRecord`
under `RESTRICTED_ROOT`**, joined per **R-19**; `false` otherwise.

**Why derived and not passed.** A caller argument distributes a governed fact across nine stage
scripts, each of them a chance to pass `false` — the *"remembered, not checked"* pattern this stage
has refused throughout. Derived, it **cannot be forgotten or suppressed by a caller**, and one place
computes it. Recommendation 12's option 2 (every stage script passes `exploratory: bool`, preflight
refusing an unset value) was **not** taken for exactly that reason; option 3 (leave the label
human-written in the change record) was refused because it removes the only executable check, and
`team.md` § Testing Posture fixes locked-test discipline as *"an executable guard, not only a
signature."*

**Constraint — THE CARVE-OUT, stated explicitly because the cheap wrong answer is to label
everything.** The **G-06 confirmatory run is NOT exploratory**, notwithstanding that it postdates the
earliest access record. It is the run whose access **is** the locked evaluation. The carve-out is
keyed to the run's own identity, not to a caller's assertion:

> A run is exempt from the derivation **iff** its own `AccessRecord` carries
> `purpose = locked_evaluation` **and** it is the run G-06 authorises. It is then recorded
> **`exploratory = false`, with the carve-out recorded on the row** — never left unset, never blank.

**Why the carve-out is written this narrowly.** Recommendation 12's stated risk is that *"an
unimplementable state resolves under pressure and both cheap resolutions are wrong: label every run,
which is meaningless and would mark the G-06 confirmatory run itself exploratory, or relax the
assertion."* A carve-out keyed to the caller saying *"this is the confirmatory run"* would be the
first failure wearing the second's clothes. Keyed to `purpose = locked_evaluation` on the access
record — a field `governance-guards` sets **structurally, not by caller choice** (`AccessRecord`'s
`purpose` enum is `coverage_audit` | `regime_audit` | `locked_evaluation`) — it cannot be claimed by a
run that is not it.

**Constraint — the pre-G-05 coverage audit does NOT start the exploratory clock in the wrong place,
and does not escape it either.** The required pre-G-05 December coverage and regime audit is a
**legitimate access** (Vision §8.3; it is a precondition of G-05) and it **writes an `AccessRecord`**
with `purpose = coverage_audit`. So the *"earliest `AccessRecord` under `RESTRICTED_ROOT`"* will
normally be that audit, **not** the locked evaluation — which is correct and is the conservative
direction: `project.md` § Forbidden fixes that *"the trigger is December being **seen**, not the
locked test being opened."* The derivation therefore reads December-seen, exactly as the rule
intends, and it must **not** be narrowed to `purpose = locked_evaluation` records only.

**Constraint — the reader-side assertion stays broader than §8.3's literal text, deliberately.**
Vision §8.3 says *"any **test-driven** change"*; R-128 asserts the label on **every** reported
post-access run. That is broader, it is the conservative direction, and this rule **does not narrow
it to match**. A change of scientific intent is not machine-detectable; the timestamp relation is.
Recommendation 12 records the same judgement.

**Negative controls — four.** (1) A run whose `started_at_utc` postdates the earliest restricted
`AccessRecord` → assert `exploratory = true` **on the row**, not merely reported. (2) A run predating
it → `false`. (3) **The carve-out's own control, which Recommendation 12 requires by name:** the G-06
confirmatory run → assert `exploratory = false` **and** that the carve-out is recorded on the row;
then present a run that postdates the access log and **claims** the carve-out **without** an
`AccessRecord` carrying `purpose = locked_evaluation`, and assert the carve-out is **refused** and the
run labelled `true`. (4) A caller passing `exploratory` explicitly → **rejected**, so the derived-only
rule is enforced by signature rather than by discipline.

**Acceptance.** **⚠ No §16/§19 row.** FR-P1-05-14 is recorded `UNTESTED` in `requirements.md` with no
§16/§19 row, and **none is sought** — Amendment A was declined and §19 is held at 36 rows with
TA-37/TA-38 explicitly not to be added. Enforcement rides R-128's reader-side assertion in
`regimes-diagnostics-reporting`, which **fails** a post-access run reported without the label, plus
this rule's four controls. **This is a rule whose acceptance gap is stated, not buried** — see the
table below, which it joins.

---

> ## ✳ THE RULE COUNT MOVED 2026-08-28: 17 → 20 (R-01…R-20)
>
> *(Three rules added — **R-18**, **R-19**, **R-20** — on the owner's ruling on
> `GOV-2026-08-28-FD-01` Recommendations **10**, **1**/**3** and **12**. Derived, not asserted:)*
>
> ```
> grep -cE '^## R-[0-9]+' business-rules.md          ->  20   (R-01…R-20, contiguous)
> grep -cE '^## R-'       business-logic-model.md    ->   0   (rules live in this file only)
> grep -cE '^## W-[0-9]+' business-logic-model.md    ->  10   (W-1…W-10, unchanged)
> grep -cE '^## [0-9]+\.' domain-entities.md         ->   9 sections, § 8 withdrawn -> 8 live
> ```
>
> **What did NOT move.** 16 requirements; 2 untested by design (REQ-ENG-7, REQ-ENG-10); 7 acceptance
> rows owned (TA-01 TA-02 TA-03 TA-10 TA-15 TA-22 TA-23); 2 supporting rows (TA-13, TA-26); §19 held
> at **36** rows with no TA-37/TA-38; 10 workflows; 8 live entities. **No scientific value, governed
> constant, config field or approved signature is decided by any of the three new rules.**
>
> **Every prior "17 rules" statement in this file and in `business-logic-model.md` remains true as a
> DATED record and is not rewritten.** They are scoped claims about specific earlier events — *"R-12
> was amended, not removed"*, *"Neither correction moves a project count"* — and each was correct
> when written. The current count is the derived one above. Sweeping them would rewrite dated
> reviewer and remediation text, which this unit's annotate-in-place convention forbids.
>
> ### Citation correction — §13.4's atomicity clause, per Recommendation 39
>
> Recommendation 39 found §13.4's *"Registry writes must be **atomic or append-safe**"* requirement
> *"checked off against two rules that do not carry it"*. The mis-citation reads
> **"§13.4's atomic/append-safe registry with failed and aborted runs visible (TE:829) ✓ — R-07,
> R-09"**, and **R-07 is the status enum** while **R-09 is stays-visible**; neither states a write
> mechanism.
>
> | Clause of TE:829 | Rule that actually carries it |
> |---|---|
> | *"Registry writes must be **atomic or append-safe**"* | **R-08** — the single-write newline-terminated append under append mode plus durability confirmation, added 2026-08-28, with the trailing-versus-interior malformed-row distinction and its three controls |
> | *"Failed and aborted runs remain visible **with status and reason**"* | **R-07** (the closed status enum and the non-empty `reason`) and **R-09** (no delete, no overwrite, no silent re-run) |
> | *"silent reruns are prohibited"* | **R-09** |
> | the twenty-column schema | **R-18** |
>
> So the correct citation for TE:829 is **R-07, R-08, R-09** — R-08 being the one that was missing and
> the one the clause turns on.
>
> **⚠ Where the mis-citation lives, and why it is corrected HERE rather than at that line.** The
> remediation brief located it as *"your verification table at `business-logic-model.md:1748`"*. On
> disk that line is **not this unit's own verification table**: it sits inside
> `## Review — 2026-08-25 post-redo pass, restored budget iteration 1`, under
> `### What reproduced exactly — the refutations that failed`, and it is a **reviewer's** dated
> spot-check of TE section citations. Preserved `## Review` sections are not editable, and rewriting a
> reviewer's sentence would break this unit's annotate-in-place convention. **The correction is
> therefore stated here, in live rule text, and on R-08's own Acceptance line** — the two places a
> reader at the gate and an implementer at 3.5 will actually look. The reviewer's line stands as the
> dated record of what that reviewer checked; it was accurate about *"failed and aborted runs
> visible"* and incomplete about *atomicity*, which is precisely the finding.

## Rules with no acceptance row — stated, not buried

| Rule | Requirement | Status |
|---|---|---|
| Freeze-gate tagging; D-number on every governed change | **REQ-ENG-7** | ⚠ **No §16/§19 row — and none will be added.** Amendment A **DECLINED 2026-08-24**; untested **by design**, permanently *(superseded status: "Amendment A pending")* |
| Per-run environment lock, eight fields populated | **REQ-ENG-10** | ⚠ **No §16/§19 row.** TA-03 verified against all seven §13.1 bullets and covers **none fully**; two partially, both install-time rather than per-run. `requirements.md` records the same conclusion. Amendment A **DECLINED 2026-08-24**; untested **by design**, permanently *(superseded status: "Amendment A pending")* |
| Probe scope, measurement status, declared-vs-observed mismatches | Q3 = C / NFR-DET-01 | ✅ **Fields now in the approved contract** — `DeterminismRecord` carries nine. Amendment B **APPROVED 2026-08-24** *(superseded status: "Fields not in the approved contract. Amendment B pending")* |
| **R-17** — every module and script carries a purpose/inputs/re-run docstring | Human-selected candidate rule, interview Q12-C | ⚠ **No §16/§19 row accepts it.** The convention is observed in both existing scripts and is mandated in `project.md` § Mandated, but no acceptance row tests it; enforcement rides review rather than a gate *(row added 2026-08-25 on adversarial residual r-2 of the eighth-redo iteration 2: R-17 is the other rule in this file declaring no acceptance row, and this table — whose whole purpose is to state them rather than bury them — omitted it)* |
| `dataset_version` derivation integrity — **correspondence and determinism covered** by two of R-12's negative controls; **never-reuse NOT covered** — its third control detects only a *degenerate* encoding, never a *truncating* one, so injectivity is an **OPEN** obligation on the encoding *(corrected 2026-08-25, adversarial finding M-3 of the restored budget; superseded: "**covered by three negative controls** in R-12 (derivation correspondence, derivation determinism, injectivity against a degenerate encoding)")* | **Q6 = D′** (re-answered 2026-08-25); FU-2 moot | ⚠ **Amendment C DECLINED AS DRAFTED 2026-08-25**, so there is no ledger and no `ReleaseLedgerEntry`. *(Glyph corrected 2026-08-25 on adversarial residual r-1 of the eighth-redo iteration 2: this row carried ✅ while its obligation is partly **uncovered**, and rows 1–2 of this table use ⚠ for exactly that state.)* FU-2's inconsistent-mapping obligation is carried by the correspondence control; its **duplicate-row** obligation is **vacuous** — with no ledger there are no rows to duplicate. Its **reused-label** obligation is **NOT** vacuous: that *is* never-reuse, and it **remains uncovered**, pending the encoding's injectivity. *(Corrected 2026-08-25 on adversarial finding of the eighth-redo iteration 1. **Superseded wording, preserved:** "its duplicate-and-reused-label obligation is **vacuous** — no rows to duplicate, and reuse across genuinely different content reduces to a SHA-256 collision." Two defects in one clause: it deployed the **withdrawn** SHA-256-collision reduction as live fact, where R-12 refutes it and preserves it only as superseded — the r-1 sweep removed one deployment and left this one — and it bundled *duplicate-row* with *reused-label* as jointly vacuous when the second is exactly the open obligation the next sentence concedes.)* *(Corrected 2026-08-25 on adversarial finding M-3 of the restored budget; superseded wording preserved: "Nothing is left uncovered." The third control is non-degeneracy, not injectivity, so it cannot cover never-reuse — an OPEN obligation on the label encoding.)* Both upstream sites were **corrected on 2026-08-25** on the owner's explicit authorisation after this stage first reported rather than edited them: `unit-of-work.md` § 1 `Owns` no longer lists the ledger and `services.md` reads *"Two artifacts, one authoritative"* *(superseded statuses, all preserved: "~~Release-label ledger integrity~~ — obligation withdrawn; `dataset_version` derivation carries no integrity test … uncovered, and not replaced"; "✅ **Artifact now in `unit-of-work.md` § 1 `Owns` and `services.md`.** Amendment C **APPROVED 2026-08-24** on the authority of Q6=D and FU-2=D"; and "Artifact not in any approved `Owns` list. Amendment C pending")* |

| **R-20** — `exploratory` derived in the registry writer | **FR-P1-05-14** (Vision §8.3) | ⚠ **No §16/§19 row accepts it**, and none is sought. `requirements.md` records FR-P1-05-14 as `UNTESTED`; Amendment A was declined and §19 is held at 36 rows. Enforcement rides `regimes-diagnostics-reporting` R-128's reader-side assertion — which **fails** a post-access run reported without the label — plus R-20's four negative controls, including the carve-out's own control *(row added 2026-08-28 with R-20, per Recommendation 12: this table's whole purpose is to state acceptance gaps rather than bury them, and a new rule with no row belongs in it on the day it is written)* |
| **R-18** — the twenty-column registry schema; **R-19** — the `run_id` join | **FR-P1-05-13** / **NFR-AUD-01** | ✅ **Covered — TA-10**, whose FR-P1-05-13 criterion is *"a schema assertion confirms all twenty columns exist"*, plus **TA-21** for the traceability limb. Listed here for completeness of the 2026-08-28 additions, **not** as a gap: R-18 and R-19 are the design the existing criterion had been missing, so they close a gap rather than opening one |

**Test specifications for REQ-ENG-7 and REQ-ENG-10**, labelled exactly as Q7 = X
directs:

> **Test specification only — not an approved acceptance row and not evidence of a
> passing result.**
>
> **This label is now permanent, 2026-08-24.** It was provisional while Amendment A —
> the Vision §15.2 request Q7=X directed be raised — was pending. The owner **declined**
> that request, so no §19 row will cover REQ-ENG-7 or REQ-ENG-10. These specifications
> remain what they say they are: design targets for stage 3.5, never acceptance
> evidence, and their absence from §19 is the approved *"Open by design"* state rather
> than an outstanding gap.

- **REQ-ENG-7.** Reject a change to a governed scientific constant or governed
  configuration file when the required decision identifier is **missing or
  invalid**; verify the applicable freeze-gate tagging requirements.
- **REQ-ENG-10.** Derive the required environment-lock fields **directly from TE
  §13.1** and fail when any required item is **missing, malformed, or not captured**
  for the applicable run. The eight fields and their seven-bullet provenance are
  enumerated in `domain-entities.md` § 5.

Per Q7, design and implementation planning proceeded while Amendment A was pending.
**Amendment A was DECLINED on 2026-08-24**, so REQ-ENG-7 and REQ-ENG-10 are **untested by
design and permanently** — 2 of this unit's 16 requirements. **Formal acceptance coverage and
gate satisfaction are never claimed for these two**: their negative-path specifications above
are test specifications only, a settled state rather than a provisional one, and their
enforcement rides §18.3's gate-test list and TA-11 rather than a row of their own.

> *(Condition corrected 2026-08-25 on adversarial reviewer finding m-1. **Superseded wording,
> preserved:** "Per Q7, design and implementation planning proceed while Amendment A is
> pending. **Formal acceptance coverage and gate satisfaction are not claimed** until the
> amendment is approved and the tests have executed successfully." Amendment A was declined,
> not approved, so that condition can never be met and the sentence read as deferral where the
> state is permanent — contradicting the acceptance-status box above it. **No new conditional
> dependency on Amendment A is created, and A is not reopened.** No count moved: 16
> requirements, 2 untested, 7 acceptance rows, §19 at 36 rows.)*

## Assumptions & Open Questions

- **[assumption]** The `RequiredFieldsMap` and `CredentialNameMap` are declarative structures **inside `src/data/config.py`**, not governed config files. They name field and variable *identities*, never values, so they carry no scientific constant and TE §12's "exactly four" is untouched. FU-3's stronger form — a seventh module — has no legal home, since TE §12 fixes six `src/` packages.
- **[assumption]** `foundation` hosting `CredentialNameMap` without consuming it is within the boundary. Stated explicitly in R-14 because, unstated, it reads as a boundary violation.
- **Amendments A, B and C — all three ruled, none pending.** **A: DECLINED** (2026-08-24) — REQ-ENG-7 and REQ-ENG-10 untested by design, permanently; §19 held at 36 rows; TA-37/TA-38 not to be added. **B: APPROVED** (2026-08-24) — the three `DeterminismRecord` fields exist, nine in total. **C: DECLINED AS DRAFTED** (2026-08-25, reversing its 2026-08-24 approval) — no release ledger, `ReleaseLedgerEntry` withdrawn, `dataset_version` derived from `content_hash` with no encoding specified here. **Neither A nor C was approved; no amendment authorises execution of anything, and G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

  *(Corrected 2026-08-25 on adversarial reviewer finding M-2, which was Major. **Superseded wording, preserved:** "**Open — Amendments A, B and C.** All three **PENDING and NOT approved.** Enumerated at this stage's approval gate." That was refuted in the passed contracts at the time it was read, and both sibling artifacts had swept this same bullet while this file's § Assumptions was not — the omission finding M-3 traces to this file's own self-certification. The bullet carried **no numeral**, which is why the 2026-08-24 sweep, keyed to `DeterminismRecord` "six fields" and `services.md` "two artifacts", could not see it.)*

- **OPEN — a cross-unit obligation on the eight exceptions this unit does not raise.** `foundation` owns `IntegrityError` and the stage-entry catch, and R-01 now places **all fourteen** project-defined exceptions in that hierarchy on the authority of `component-methods.md` § Assumptions. Eight of them are **raised by other units** — `PhaseBoundaryError` and `LockedTestError` (`governance-guards`), `LeakageError`, `AlignmentError`, `SeedError`, `FairnessError`, `BootstrapError`, `RegimeError` — and **each of those units' `functional-design` must declare its own exceptions as `IntegrityError` subclasses**. This unit cannot do it for them, and it is recorded here rather than assumed because the omission it replaces would have let a phase-boundary violation exit with **no `aborted` registry row**, against NFR-PHASE-01 and NFR-AUD-01 *(added 2026-08-25 on adversarial finding m-1 of the eighth-redo iteration 2)*. No cycle is created: every one of those units already depends on `foundation`.

  *(**Amended 2026-08-28 per Recommendation 8 — the bullet above says eight and fourteen; it is now NINE and FIFTEEN.** The dated sentences stand; the current state is stated here. `PartitionError` was promoted into R-01's enumeration on the owner's ruling, so the exceptions raised by other units are **nine**, adding `PartitionError` → **`models-and-baselines`**, which declares it in `src/models/`. The declaration obligation this bullet states binds that unit for `PartitionError` on the same terms as the other eight, and it already depends on `foundation`, so no cycle is created.)*

- **OPEN — the same declaration obligation on the eighteen exceptions riding R-01's any-future clause, and it is NOT a formality.** *(Added 2026-08-28 per Recommendation 8.)* Derived 2026-08-28: **33** distinct project-defined `*Error` subclass names exist across the twelve units' 48 artifacts, **15** named in R-01's enumeration and **18** riding its *"any future integrity-related exception"* clause — `AcquisitionError`, `AuditScopeError`, `BenchmarkError`, `BudgetError`, `ComparatorError`, `CredentialEgressError`, `DriverError`, `EvidenceScanError`, `FixtureError`, `GateError`, `ImportBoundaryError`, `InventoryError`, `InverseTransformError`, `ManifestError`, `ReuseError`, `SchemaError`, `StandardizationError`, `TargetQualityError`. **Riding the clause is not the same as being in the hierarchy**: each raising unit must still declare its own as an `IntegrityError` subclass, or R-10's stage-entry catch lets it exit with **no `aborted` row** — the NFR-AUD-01 failure R-01 was corrected once to prevent, reaching the residue instead of the enumeration. **Named specifically because the governance report examined them: `InverseTransformError`** is on the inverse-before-metric path in `evaluation-and-comparison` (13 live occurrences) and `statistical-inference` (7), both of which must declare it; **`FixtureError`** is `fixtures-and-reproducibility`', already disclosed by that unit as *"a fifteenth, named at the gate"* — a label that now needs its own numeral corrected, which is **that unit's** to do, not this one's. This unit cannot declare any of the eighteen for their owners; R-01's enumeration-reconciliation negative control is what makes an undeclared one visible rather than silent.

- **OPEN — `evaluation-and-comparison`'s and `statistical-inference`'s side of Recommendation 8, which this unit does NOT close.** *(Added 2026-08-28.)* `models-and-baselines` R-92 raises `PartitionError` for a `partition_id` mismatch; `evaluation-and-comparison` R-105 raises **`LeakageError`** for the same condition while claiming to *"mirror R-92"*; `statistical-inference` R-113 imports R-105 *"as written"*, so a third unit inherits it. R-01 now states the **discriminating rule** those units must agree against — declared-identity disagreement → `PartitionError`; disagreement implying information flow → `LeakageError`; both true → `LeakageError` wins. **Whether R-105 changes its raise is that unit's decision**, and the governance report assigns the taxonomy choice to `models-and-baselines` + `evaluation-and-comparison`. Recorded here so the promotion is not mistaken for having settled the sibling units' raise sites: a test asserting `pytest.raises(PartitionError)` still passes at `06` and fails at `07` until they do.
- **OPEN — whether `IntegrityError` should move to a dedicated `src/data/exceptions.py`.** This stage declared the hierarchy in **`src/data/config.py`** because TE §12's `src/data/` tree names **nine** modules and **none for exceptions**, so a dedicated module is a **§12 amendment** this stage may not make by assertion. `config.py` works and crosses no import boundary — every unit raising one of the other eight already depends on `foundation`. But a module whose §12 comment reads *"config load, per-run snapshot, hashes, determinism helper"* is not an obvious home for the project-wide exception base, and the fourteen-subclass hierarchy is now project-wide rather than `foundation`-local. **The owner's decision: accept `config.py`, or amend §12 for `src/data/exceptions.py`** *(added 2026-08-25 on adversarial finding M-1 of the ninth-redo iteration 1, whose fix names this item as recorded here — so not creating it would have been the same claim-without-the-thing defect the last three passes each caught)*.
- **OPEN — the `dataset_version` hash-to-label encoding.** *(Added 2026-08-25 on adversarial reviewer finding M-4, which was Major: this decision was stated as unspecified in all three artifacts while appearing as an open item in none of them, and the Q&A simultaneously asserted "Nothing carried to the stage gate as an open item.")* Q6=D′ requires `dataset_version` to be **derived from the release `content_hash`** and human-readable, and **no approved artifact specifies the encoding**. Per TE §18.3 stage 3.5 must **stop and report** rather than choose one. **This blocks concrete work**, which is why it belongs here rather than in a narrative: `dataset_version` is a §13.3 manifest field, W-7 step 5 must produce it, and `src/data/release.py` plus the §18.3-critical `tests/test_release_hashes.py` cannot be completed without it. **The encoding also carries the never-reuse obligation** below. Resolution is a freeze-gate decision, not an implementation choice.
- **OPEN — injectivity of that encoding, and with it the never-reuse property.** Never-reuse is *different content → different label*. The derivation gives idempotence, not injectivity, and a human-readable label is a lossy encoding of a 256-bit hash. Whoever specifies the encoding must make it **injective over the release population in scope**, or state and have accepted its collision bound. Until then `dataset_version` carries **correspondence and determinism guarantees only**, and nothing this unit produces may claim labels are never reused.

  > ⛔ **SUPERSEDED 2026-08-29 — D-29 RULED THE ENCODING ON 2026-08-28. The heading and body below
  > are the dated record of the pre-D-29 state, preserved, not the current one.** *(Marked on
  > adversarial finding 1 of the re-confirmation pass: this box and the OPEN injectivity bullet
  > immediately above it still asserted the encoding unruled while `R-12` — in this same file —
  > already carried D-29's ruling. The `project.md` "sweep every representation of a corrected
  > fact" defect class.)* **D-29 adopts the board's option 2**: `dataset_version` = the **first 12
  > hex characters of `content_hash`**, with a **verify-on-write** uniqueness check. **Injectivity
  > is thereby established in substance and `verify_release` is discharged**, so the OPEN
  > injectivity bullet above and the never-reuse obligation it carries are **CLOSED as to the
  > encoding**. What is **NOT** closed, and is now its own item: **where the existing release
  > population that verify-on-write reads back actually lives** — the ledger that would have
  > answered it was declined at Amendment C and `ReleaseLedgerEntry` withdrawn with it. That
  > remains an **owner decision**, and per TE §18.3 stage 3.5 must stop and report rather than
  > choose an enumeration surface.
  >
  > **✳ THE BOARD'S RECOMMENDATION ON THE ENCODING, RECORDED 2026-08-28 — AND STILL NOT RULED.**
  >
  > *(Added per `GOV-2026-08-28-FD-01` **Recommendation 42**. **The two OPEN items above are left
  > exactly as they stand** — the posture is correct and the board agrees with it. What is added is
  > the board's recommendation, so the owner has it in hand when the decision is taken. **No encoding
  > is invented here, and none is adopted.**)*
  >
  > The board recommended **option 2**: a **fixed-length prefix of the `content_hash`** (its example:
  > 12 hex) **plus a recorded collision bound** and a **verify-on-write uniqueness check** that the
  > prefix is unused. Its stated reason: it is *"the only option delivering both a citable label and
  > an established never-reuse property"*, and its cost *"is exactly the `verify_release` amendment
  > R-12 has already identified as needed, so it closes two of three open items in one act"* — the
  > third open item against R-12, the `verify_release` amendment listed below, being the one it would
  > also discharge. The named alternatives: **option 1**, `dataset_version` = the **full 64-hex
  > `content_hash`**, injectivity inherited from SHA-256 with no ledger, no allocation state and no
  > new failure mode, at the cost of being unreadable as the human citation label R-12 says the field
  > exists for — the board calls it *"a sound fallback if hash-string citations are acceptable"*; and
  > **option 3**, keep the label explicitly non-unique, mandate `content_hash` in every citation and
  > **formally withdraw the never-reuse claim**, which the board would accept *"only if the supervisor
  > prefers withdrawing the obligation to engineering it, and then by an explicit act rather than
  > silence."*
  >
  > **The trade-off this unit is obliged to flag, since option 2 reintroduces what Q6 removed.** A
  > verify-on-write uniqueness check is **a read back over existing releases** — a light form of the
  > ledger the owner declined at Amendment C, and a departure from **R-08**-style purity on the
  > release path (though not on the registry path, which R-08 governs and which is untouched). That is
  > not an objection to option 2; it is the fact the ruling should be made with, because the owner
  > declined durable release state once already and this reaches part of the way back to it.
  >
  > **The board's assessment of the current risk, recorded because it bounds the urgency**:
  > *"**release immutability is not compromised.** It rests on R-13's directory-level overwrite
  > refusal and R-11's identity-equals-`content_hash`, neither of which depends on `dataset_version`
  > injectivity. What is open is **citation uniqueness** … a traceability defect rather than a
  > mutation defect, and the design says so precisely and forbids claiming otherwise."*
  >
  > **⛔ THE ENCODING REMAINS A D-NUMBER DECISION THE OWNER MUST TAKE BEFORE 3.5 TOUCHES
  > `write_release`.** It is unruled as of 2026-08-28. `dataset_version` is a §13.3 manifest field,
  > W-7 step 5 must produce it, and `src/data/release.py` plus the §18.3-critical
  > `tests/test_release_hashes.py` cannot be completed without it. Per **TE §18.3** stage 3.5 must
  > **stop and report** rather than choose one, and per `team.md` a decision is not real until it has
  > a **D-number**. **Nothing above is a choice made by this stage**, and the never-reuse posture in
  > the two OPEN items stands unchanged: injectivity is **not established**, and no artifact this unit
  > produces may claim labels are never reused. ⛔ **SUPERSEDED 2026-08-30 by D-29** *(marker added
  > on adversarial finding 1, Critical — a live site the two prior repair passes did not reach)*:
  > **injectivity IS established in substance** by D-29's verify-on-write check, so this unit's
  > artifacts **may** state never-reuse holds on the encoding. What no artifact may yet claim is
  > that the check is **implementable**, because the release population it reads back is
  > unspecified — that is the surviving open item and the §18.3 stop-and-report point.
  >
  > **One related fact the board verified, and it is this unit's to know rather than to fix**: the
  > existing `tests/test_release_hashes.py` (267 lines) tests hash verification and mutation
  > *detection* over existing evidence manifests, and a grep for
  > `dataset_version|mask_id|feature_set_id|row_count|exclusion` in it returns **0** — so **none of
  > §13.3's required manifest fields is covered today**, and it does not exercise **R-13**'s overwrite
  > refusal. The module's name matches the mandated one, which invites a reader to believe TA-15 is
  > covered when the §13.3 field contract is untested. Recorded as a **naming hazard against TA-15**,
  > not as coverage.
- **OPEN — an amendment need on `write_release`'s approved raise-contract.** `component-methods.md` has `write_release` raise `ReleaseError` *"when a field is absent"* over **all fourteen** §13.3 fields. Deriving `dataset_version` inside `write_release` (Q6=D′) narrows the **caller** precondition to thirteen while leaving the **output** obligation at fourteen. The release still carries all fourteen fields, so what the function writes is unchanged — but the caller contract does change, and this stage demanded a formal amendment for exactly this class when it declined to alter `ensure_process_determinism`'s `-> None` signature. Applying a looser standard here would be inconsistent, so this is **the owner's decision, not a settled contract** *(added 2026-08-25 on adversarial finding m-2 of the restored budget; the rule text claimed it was listed here and it was not)*.
- **OPEN — an amendment need on `verify_release`, or acceptance that the correspondence check is test-only.** R-11's and R-12's correspondence negative control was relocated to *"a presented manifest"* without naming what performs it. The only candidate in the approved contracts, `verify_release(manifest_path) -> Sequence[str]`, **does not fit**: it reports files whose *file hash* mismatches and **never raises**, so it covers neither label/hash correspondence nor failure signalling. The control is therefore specified as a **test** obligation on `tests/test_release_hashes.py` (TA-15), which needs no production entry point. **If runtime enforcement is wanted, `verify_release` must be amended** — the owner's decision *(added 2026-08-25 on adversarial finding M-5 of the restored budget; likewise claimed as listed here and not)*.
- **Closed — the three consequences the Amendment C reversal first appeared to carry.** Two closed on analysis and one on an owner ruling; a fourth, listed above, was missed by that analysis and is now open:
  - **The delete-and-rebuild failure — CLOSED.** The superseded R-12's objection was to *allocation from an index*; a pure function of `content_hash` allocates nothing, so that failure cannot arise. *(Superseded 2026-08-25 on finding M-3: this bullet previously read "**Never-reused — RESOLVED, satisfied by determinism**", which overclaimed — determinism disposes of the delete-and-rebuild failure but does not establish never-reuse. See the **encoding** and **injectivity** items above — named rather than counted, because the list grew to four and "the two open items above" would now mislead *(2026-08-25)*.)*
  - **FU-2's inconsistent-mapping obligation — CLOSED**, carried by R-12's correspondence control; its duplicate-row obligation is **vacuous** with no rows to duplicate. *(Superseded on M-3: previously "discharged by three negative controls … stronger than a correspondence check alone". The third control catches only a **degenerate** encoding, never a truncating one, so it cannot stand in for injectivity.)*
  - **Monotonicity — RESOLVED by re-answering the question, not by a mechanism.** Ordering is information about *sequence*, which a function of content alone cannot carry, so no test recovers it and no implementation choice reaches it. **Q6 was therefore re-presented and re-answered as D′ on 2026-08-25**, dropping "monotonic" — the owner's explicit decision, not an assumed amendment, with the original Q6=D answer preserved verbatim beside it. R-12 is compliant with Q6=D′ **on monotonicity — but NOT on never-reuse, which D′ retains and this design does not establish** *(narrowed 2026-08-25 on adversarial finding M-1/M-3 of the restored budget; this was the fifth and last unqualified "fully compliant with Q6=D′")*. **What was given up on the ordering side, and it is a capability rather than an unmet obligation:** release labels can no longer be ordered, so a reviewer comparing two labels at a gate must read sequence from the run record or the experiment registry instead. Nothing else in this design depended on label ordering. **FU-2 is moot** — it existed only to locate the ledger Q6=D required.
  - **The two upstream artifacts are no longer open.** `unit-of-work.md` § 1 `Owns` and `services.md` both named a ledger this design no longer has; they were first **reported** rather than edited, because this stage's scope control forbade editing an approved Inception artifact, and the owner then authorised the edits explicitly on 2026-08-25. Both were corrected the same day, superseded wordings preserved, and a search across `construction/` confirmed no other unit referenced the ledger.
- **Open** — the concrete contents of both maps cannot be enumerated until the four configs exist. This stage fixes the mechanism; the populated maps are Bolt 1 work products.
- **OPEN — a cross-unit dependency on `models-and-baselines` for `PredictionHashReceipt`.** *(Added 2026-08-28 per Recommendations 1 and 3.)* **R-18** designs the registry row as the receipt's **destination** and forbids `07`/the bootstrap from being its writer, but the **producer** is `scripts/06_train_and_predict.py`, which `models-and-baselines` owns. That unit is being amended in parallel to name `06` as the writer with the refusal-to-exit control. **`foundation` cannot supply the producing half**, and until it exists column 18 `prediction_hash` has a designed destination and no designed source — which is fail-closed rather than a breach, since every `DEC` metric entry point already refuses without a verified receipt. Recorded so the two halves are known to be two: the governance report's adoption vehicle for this is the **R-103/BLK-08 two-half contract pattern**, registered as an exit condition on 3.1 for both owners, and **this unit does not declare that pattern satisfied from one side.**
- **OPEN — a cross-unit dependency on `governance-guards` for the `run_id` join and for `prior_period_exposure`.** *(Added 2026-08-28 per Recommendation 10.)* **R-19**'s reconciliation reads `AccessRecord`, which `governance-guards` owns; `prior_period_exposure` is recorded by the locked-test guard per TE §7.0B and merely **carried** by the registry row. Both keys already exist on both entities (`run_id`), so no contract change is needed on either side — but the reconciliation is a **joint** obligation and this unit designs only the registry half. **Zero of the 48 artifacts named both entities before 2026-08-28**; R-19 is the first statement of the relationship and `governance-guards` has not yet stated its side.
- **OPEN — Kaggle's durability semantics are characterised nowhere in this design.** *(Added 2026-08-28 per Recommendation 39.)* **R-08**'s durability confirmation is specified on `governance-guards` R-25's accepted pattern, and platform durability behaviour **differs between the two governed platforms**. Kaggle's is unmeasured here, so the confirmation step needs its own measured evidence before registry rows written inside a Kaggle session are relied on at a freeze gate. This is a **measurement obligation on Bolt 1's in-Kaggle work**, not an implementation choice, and it is not this stage's to measure.
- **G-09 is not signed.** ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged. No rule here authorises creating any module — including the three rules added 2026-08-28, which decide a schema, a join and a derivation and create nothing. Vision's gate table records **G-09 Agent preflight** as **Open**, owner **Supervisor**, evidence `aws_ai_dlc_preflight_report`, due *"Before any affected component is coded"*.
- **None** of the above adopts a reading on a supervisor-owned value, and none decides a scientific constant. **This holds for the 2026-08-28 amendments specifically**: R-01's promotion is a taxonomy decision, R-18/R-19/R-20 are schema and derivation decisions, R-08's is a write mechanism, R-05's is an acceptance-row label, R-14's is a dated status clause, and the `dataset_version` encoding is **explicitly left to the owner's D-number decision** rather than chosen.

## Review history

| Pass | Verdict | Effect on this file |
|---|---|---|
| Iteration 1 (adversarial) | **NOT-READY** | Not reached by the finding. Its critical finding was against the two traceability tables in `business-logic-model.md` and `domain-entities.md` |
| Between passes | — | **This file was found to carry the same defect class** in its per-rule `**Acceptance.**` lines and was corrected: R-05, R-06, R-07, R-08, R-09, R-16 and R-17. Every superseded citation preserved inline |
| Iteration 2 (adversarial) | **NOT-READY** | Re-derived this file's acceptance lines cell by cell against story-map Table 1 and **confirmed all now match the source**. Its two new findings were against `domain-entities.md` only |
| Redo jump, 2026-08-22 | — | Budget was exhausted at 2 of 2 with post-review corrections outstanding. The project decision owner directed a re-review of `foundation` before any further unit; the jump reset the iteration budget and the receipt floor |
| Iteration 1 of the fresh budget | ~~*pending*~~ → **NOT-READY**, completed 2026-08-24 | *(Row corrected 2026-08-25 on reviewer finding m-4 — iteration-1 of the 2026-08-25 pass had named this same row's class explicitly and it was left un-swept. Superseded effect cell: "This file is unchanged in substance since iteration 2 cleared its acceptance lines.")* **Four passes have run since**: 2026-08-24 iteration 1 (NOT-READY) and 2 (READY), then 2026-08-25 iteration 1 (NOT-READY, seven findings) and 2 (NOT-READY, five Major). This file is **no longer unchanged in substance**: R-11's rule text, R-12 in full, R-06's heading and acceptance reason, R-05's sentinel constraint, and § Assumptions all changed |

**What iteration 2 explicitly cleared here.** The per-rule acceptance citations, the
two-tier posture, R-14's credential-boundary statement, and the pending-amendment
discipline in R-06 and R-12 — all checked against source and found correct.

---

## Finalized 2026-08-24 — the three amendments are settled

Recorded under `governance/CHANGE_RECORD_2026-08-24_foundation_amendments.md`, after
an independent challenge of each amendment against the approved artifacts.

- **Amendment A — DECLINED.** No project rule requires universal §19 coverage, and the approved position dispositions uncovered requirements as *"Open by design"*. **REQ-ENG-7 and REQ-ENG-10 are untested by design, permanently rather than pending.** No count moved: untested stays 36, this unit's stays 2 of 16, its acceptance rows stay 7, TE §19 stays at 36 rows.
- **Amendment B — APPROVED.** `DeterminismRecord` carries **nine** fields. R-05's prohibition on stating that determinism was measured is **discharged** and replaced by a narrower rule: a measured claim requires `probe_scope` recorded and `measurement_status` = `complete`. **R-06 is unchanged** — an empty `nondeterministic_ops` is never proof of determinism.
- **Amendment C — DECLINED AS DRAFTED 2026-08-25**, reversing its 2026-08-24 approval. No release ledger; `ReleaseLedgerEntry` withdrawn; `dataset_version` derived from `content_hash`, encoding unspecified here. **R-11 is unchanged in substance** — the content hash remains authoritative — though its **rule text was amended 2026-08-25** to cite Q6=D′ and strike "monotonic" (reviewer finding M-1; the earlier blanket "R-11 is unchanged" is exactly what hid that). **R-12 is amended, not deleted**, and records what the derivation provides and what it does not. *(Superseded status, preserved: "**Amendment C — APPROVED**, on the authority of **Q6=D** and **FU-2=D** rather than as an engineering preference. A draft of the change record proposed rejecting it and deriving the label from the content hash; that is Q6 option C, which the owner had read and declined, and it cannot yield the *monotonic* label Q6=D requires. The rejection was withdrawn.")*

  **The withdrawn rejection is now the ruling.** What the superseded text describes as a proposal the owner had already declined — deriving the label from the content hash, Q6 option C — is what the 2026-08-25 ruling mandates. That ruling was given after this exact reasoning, and the owner's own Q6=D and FU-2=D answers, were put to them in full. It is a deliberate override with its consequences stated. **Both items that reasoning left open are now closed**: monotonicity by the Q6=D′ re-answer, and the upstream contradiction by the two authorised corrections of 2026-08-25. **What replaced them as open is narrower and more concrete** — the hash-to-label encoding, and the injectivity that never-reuse depends on; both are listed in § Assumptions.

The negative-path test specifications for REQ-ENG-7 and REQ-ENG-10 keep their
*"Test specification only — not an approved acceptance row"* label as a **settled**
state rather than a provisional one.

**G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.** Nothing in this document authorises creating a module, and
no scientific value is decided here.

---

> **Re-saved 2026-08-24 under the post-redo receipt floor.** The project decision owner
> authorised a redo jump on `functional-design` at 2026-08-24T14:57:07Z so that three
> standing reviewer findings on `models-and-baselines` could be fixed and re-reviewed;
> a redo resets the receipt floor for **every** unit of the stage. **No content of this unit
> changed** — not a question, answer, amendment, rule, entity, workflow, count or scientific
> value. The only artifacts edited after the redo were `models-and-baselines`'s, whose
> three fixes are confined to its own files. That unit returned **READY** on the second pass of
> the restored budget, which is what the redo was authorised for. The two residuals riding that
> verdict — R-96's `PartitionError` mechanism and R-95's field label — are carried to the stage
> gate rather than applied, per the rule that a suggestion riding a READY verdict is gate input.

---

> **Re-saved 2026-08-25 under the sixth post-redo receipt floor.** The stage wedged on
> `models-and-baselines`: its artifacts were written and the adversarial reviewer returned
> READY on iteration 2 of 2 (2026-08-24T15:16:47Z) *before* its summary confirmation was
> recorded (15:32:45Z). The engine requires a produces-artifact write after the confirmation
> receipt, the write-freeze hook refused the re-save because a fresh READY receipt covered the
> unit, and the 2-iteration adversarial budget was spent — a deadlock whose only sanctioned
> exit is a redo jump. The project decision owner authorised one at **2026-08-25T06:30:05Z**,
> which reset the receipt floor for every unit of the stage.
>
> **No rule in this document changed.** The owner directed **evidence-driven revision** for
> this recovery — keep the adversarially-verified text as the baseline and edit only where a
> real defect is found — rather than a blanket re-derive, on the finding that all eight built
> units already carry a READY `## Review` section and that a blanket rewrite would discard
> verified corrections. The unit's figures were re-derived programmatically from the current
> `unit-of-work.md` § 1 — **16** requirements, **2** untested (REQ-ENG-7, REQ-ENG-10), **7**
> acceptance rows — each agreeing with the per-rule acceptance lines below.
>
> **Upstream provenance, enumerated per file** *(corrected 2026-08-25 on reviewer finding m-5;
> **superseded wording, preserved:** "Every consumed upstream file was last modified at 12:26
> UTC, three hours before this unit's 15:27 UTC artifacts and committed unchanged at
> `9c7afd9`" — true of three of the six, and the derivation had never enumerated its scope)*:
>
> | Consumed artifact | Last modified | Commit |
> |---|---|---|
> | `unit-of-work.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `component-methods.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `services.md` | 2026-08-24 12:26 UTC | `9c7afd9` |
> | `unit-of-work-story-map.md` | 2026-08-23 20:40 UTC | `45796f5` |
> | `components.md` | 2026-08-23 19:05 UTC | `45796f5` |
> | `requirements.md` | 2026-08-22 12:37 UTC | `89674b6` |
>
> **The no-drift conclusion is unchanged**: every one of the six predates this unit's 15:27 UTC
> artifacts, so none of them moved under this unit's design.
>
> **The seventeen rules R-01–R-17**, their IDs and their acceptance citations are unchanged.
> *(Count corrected 2026-08-25 on reviewer finding M-1, which was Major. **Superseded wording,
> preserved:** "The thirteen rules, their IDs and their acceptance citations are unchanged."
> Thirteen was carried from the prose of an earlier section rather than derived;
> `grep -cE "^## R-[0-9]+" business-rules.md` returns **17**, and
> `business-logic-model.md` § Implementability already read "the seventeen rules (R-01–R-17)"
> correctly, so the two artifacts contradicted each other. **The rule set did not change — the
> figure was misreported.** No requirement, acceptance or §19 total moved because of this
> correction: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36 rows.)*
>
> **G-09 remains unsigned**, so no rule here authorises creating a module.

---

> **Re-saved 2026-08-25 after the remediation of the iteration-1 findings**, under the receipt
> recorded for this unit at the sixth post-redo floor.
>
> **Rules changed in this file, and only these:**
>
> - **R-12 rewritten.** `dataset_version` is now **derived from the release `content_hash`**, on
>   the authority of **Q6 = D′** (re-answered 2026-08-25; the original Q6 = D is preserved
>   verbatim in the Q&A file). No ledger, no allocation step, no `ReleaseLedgerEntry`, and **no
>   hash-to-label encoding invented here** — none is specified by any approved artifact, and per
>   TE §18.3 stage 3.5 must stop and report rather than choose one. The superseded rule is
>   preserved verbatim in the box beneath it, together with the analysis of which of its
>   objections transfers to a derivation and which does not. **Three negative controls** replace
>   the ledger's: derivation correspondence, derivation determinism, and injectivity against a
>   a degenerate encoding — **not** injectivity, and so **not** never-reuse. **R-11 is unchanged in substance** (the content hash remains authoritative); its rule text was amended 2026-08-25 to cite Q6=D′ and strike "monotonic".
> - **R-05 gained one constraint**, naming the sentinel environment variable that carries
>   `reexec_performed` across the `exec` boundary (reviewer finding m-3, owner-decided). Without
>   it R-05's own negative control could not discriminate.
> - **R-06's heading and acceptance reason corrected** (m-2, M-4); its conclusion is unchanged
>   and re-evidenced.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-12 was amended, never removed, and no
> rule was added. Derived, not carried: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no scientific value was decided
> by any rule in this file.

---

> **Re-saved 2026-08-25 after the iteration-2 remediation**, under the receipt recorded for this
> unit at the **seventh** post-redo floor. That redo was authorised because iteration 2 returned
> NOT-READY with five Major findings and a spent budget, which the terminal receipt would
> otherwise have frozen in place.
>
> **Rules changed in this file, and only these:**
>
> - **R-11 — rule text corrected (Major finding M-1).** It cited `Q6 = D` and required a
>   **monotonic** label; both were refuted by Q6=D′, which states verbatim *"Drop 'monotonic.'"*,
>   while R-12 twelve lines below already cited D′ — two adjacent rules citing different
>   authorities for one decision. Now `Q6 = D′` with "monotonic" struck, superseded rule preserved
>   verbatim. Its **negative control** was corrected too (m-2): the limb binding one hash to two
>   labels is **unconstructable** once the label is a function of the hash, and is replaced by a
>   check on a **presented** manifest. The three earlier assertions that *"R-11 is unchanged"* —
>   true of its substance, false of its text, and standing exactly where the check should have
>   been — are all qualified.
> - **R-12 — the never-reuse claim corrected (Major finding M-3).** The rule had argued that
>   determinism replaced the ledger's never-reuse guarantee. It does not: purity gives
>   **idempotence**, and never-reuse is its converse, **injectivity**. The collision reduction
>   needs an encoding faithful to all 256 bits, and D′ keeps the label human-readable and citable
>   — necessarily lossy — with the encoding unspecified and 3.5 forbidden to choose one. The rule
>   now states plainly what the derivation provides and what it does not; its third negative
>   control is labelled as catching only a **degenerate** encoding rather than a truncating one;
>   and never-reuse is carried as an **obligation on whoever specifies the encoding**. Nothing
>   this unit produces may claim release labels are never reused.
> - **R-05 — one constraint added (m-3), and it fixes a correctness bug.** The sentinel carrying
>   `reexec_performed` must be **unset by the child immediately after reading**. Environment
>   variables are inherited and `PYTHONHASHSEED` is already set after a re-exec, so without the
>   pop a subprocess of a re-exec'd stage script would record `True` without ever re-execing —
>   making this rule's own negative control pass for the wrong reason.
> - **§ Assumptions — two open items added at that time (Major finding M-4); the section carried four as of that pass — it now carries **five** *(the word "now" corrected 2026-08-25 on adversarial finding m-3 of the ninth-redo iteration 1: a dated record may state what was true then, but "now" asserts the present, so the historical-record defence did not hold)*:** the hash-to-label encoding, and
>   its injectivity. Both had been stated as unresolved in the prose of all three artifacts while
>   appearing as an open item in none of them.
> - **§ Sources — the Technical Environment document added.** Cited ten times in these rules and
>   listed in no source entry across two adversarial passes, with an unresolved `<TE>` placeholder
>   in its printed derivations. The path resolves; the three figures it blocked now derive and
>   agree, including **36** §19 rows — a figure this unit had been carrying rather than deriving.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05, R-11 and R-12 were amended, none added
> or removed. Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no rule here decides a scientific
> value.

---

> **Re-saved 2026-08-25 after remediating the restored budget's iteration-1 findings**, under the
> receipt recorded for this unit at that iteration's floor.
>
> **What changed in these rules:**
>
> - **R-11 — the compliance claim narrowed (M-1/M-3).** It read *"the rule is fully compliant with
>   Q6=D′"* without qualification. Compliance holds **on monotonicity**, which D′ dropped, and
>   **fails on never-reuse**, which D′ retains and this design does not establish. That unqualified
>   sentence appeared at **five** sites across the unit and was false at all five; every one is now
>   narrowed. Its **negative control** also names its owner: `tests/test_release_hashes.py`
>   (TA-15), because relocating the correspondence check to *"a presented manifest"* had left it
>   with **no owning function** — `verify_release` returns `Sequence[str]` and never raises, so it
>   does not fit (M-5).
> - **R-12 — the never-reuse residue swept (M-3).** Two roll-ups in this file still declared
>   *"Nothing is left uncovered"* and *"no obligation of either question is left uncovered"*, both
>   contradicting this rule's own box. Corrected, superseded wording preserved. The third negative
>   control is renamed **non-degeneracy**: calling it *"injectivity against a degenerate **or
>   truncating** encoding"* was **affirmatively false**, since this rule states plainly that a
>   truncating encoding **passes** the two-sample check (m-1).
> - **R-05 — the sentinel's reader and timing named (m-3).** The pop is performed by
>   `ensure_process_determinism` itself at W-1 step 1, the first statement of every stage script's
>   `main()`, so it precedes any stage logic and therefore any subprocess. The earlier *"before any
>   subprocess is launched"* named no actor and was unsatisfiable standing alone.
> - **§ Assumptions — two further open items (m-2, M-5).** An **amendment need on
>   `write_release`**'s approved raise-contract, since deriving `dataset_version` narrows the caller
>   precondition from fourteen fields to thirteen while leaving the output obligation at fourteen;
>   and an **amendment need on `verify_release`**, or acceptance that the correspondence check is
>   test-only. Both had been asserted in the rule text as *"recorded in § Assumptions"* while being
>   absent from it — the same defect class this pass was fixing. This section now carries **four**
>   OPEN items, equal to both sibling artifacts, verified rather than assumed.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05, R-11 and R-12 amended, none added or
> removed. Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows with no TA-37/TA-38 added. **G-09 remains unsigned**, and no rule here decides a scientific
> value.

---

> **Re-saved 2026-08-25 after remediating the restored budget's iteration-2 findings**, under the
> receipt recorded at the **eighth** post-redo floor.
>
> **What changed in these rules:**
>
> - **R-05 — the in-process carrier named (m-1), the one finding that blocked implementation.** The
>   sentinel's journey across the `exec` boundary was specified; **where the bit lives between the
>   pop at W-1 step 1 and the record at W-4 step 4 was not.** Nothing available could hold it —
>   `ensure_process_determinism` returns `None`, `seed_everything(snapshot, *, stage)` takes no such
>   argument, and `ConfigSnapshot` is built at step 2, *after* the pop at step 1. Resolved as
>   **module-level state inside `src/data/config.py`**: setter and reader in the same owned module,
>   so the hand-off is intra-module and **no approved stage-2.6 signature changes**. Every
>   alternative alters an approved contract.
> - **R-12 — the mismatch constraint scoped (m-2).** It asserted an unscoped *"raises"* while
>   § Assumptions item 4 records that `verify_release` never raises. Now **rejected on the write
>   path** and **detected on read-back by the test control only**, with that hole named as requiring
>   the `verify_release` amendment. Its **negative control** further records that
>   `tests/test_release_hashes.py` **already exists** — 12,281 bytes, zero `dataset_version`
>   references, verified directly — so stage 3.5 **extends** rather than creates; and that
>   `team-practices.md`'s *"No `tests/` directory exists yet in the workspace"* is consequently
>   **stale, reported here rather than corrected**, because `org.md` reserves that file for the
>   practices-affirmation gate.
> - **Two live sentences corrected (M-2).** *"Both loose ends have since been closed"* and
>   *"**Nothing about the Amendment C reversal now stands open against this rule**"* — the second
>   standing eighteen lines below this rule's own *"Never-reuse is open"*, in a file whose
>   § Assumptions lists two OPEN items created by that very reversal. Both superseded in place, and
>   the second now names what **does** stand open.
> - **One surplus justification disarmed (r-1).** The withdrawn SHA-256-collision reduction was
>   still deployed as support in one place, where R-12 disarms its own instance of the same
>   sentence. The conclusion it decorated is independently supported and unaffected.
>
> **The rule count is unchanged at 17 (R-01–R-17)** — R-05 and R-12 amended, none added or removed.
> Derived: `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. **§ Assumptions carries four OPEN
> items**, equal to both siblings and verified rather than assumed.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.

---

> **Re-saved 2026-08-25 after remediating the eighth-redo iteration-1 findings.** That pass returned
> **zero Majors** — the first on this unit — and confirmed **R-05's module-level carrier sound** on
> four independent angles, including that it is set in the child rather than the parent and that it
> improves testability over an inherited environment variable.
>
> **Two corrections land in this file, both on the same subject:**
>
> - **The r-1 sweep was half-done.** § Rules with no acceptance row still asserted the **withdrawn**
>   SHA-256-collision reduction **as live fact**, in the row a human reads at the gate, while R-12
>   refutes it and preserves it only as superseded. The reviewer derived the half-sweep as
>   `git show HEAD | grep -c` → **3** against a working tree of **2**. The same cell also
>   **self-contradicted**: it called the *duplicate-row* and *reused-label* obligations jointly
>   *"vacuous"* when a **reused label *is* never-reuse**, which its own next sentence concedes as
>   uncovered. Now split — duplicate-row **is** vacuous with no ledger and no rows; reused-label is
>   **not**, and remains uncovered pending the encoding's injectivity. The collision clause is
>   preserved as superseded.
> - **Three stale count-in-prose references, fixed by naming.** *"See the two open items above"* now
>   names the **encoding** and **injectivity** items, and the two dated records of *"two open items
>   added"* now read **added at that time; the section carried four as of that pass — it now carries **five** *(the word "now" corrected 2026-08-25 on adversarial finding m-3 of the ninth-redo iteration 1: a dated record may state what was true then, but "now" asserts the present, so the historical-record defence did not hold)***. Each was accurate when
>   written and went stale silently when the list grew from two to four. **A count embedded in prose
>   cannot be swept reliably; a name can** — which is the actual remedy for the class that has
>   recurred through six passes on this unit.
>
> **No rule changed.** The count stays **17 (R-01–R-17)**; derived:
> `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. § Assumptions still carries **four** OPEN
> items, equal to both siblings.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.

---

> **Re-saved 2026-08-25 after remediating the eighth-redo iteration-2 findings**, under the receipt
> recorded at the **ninth** post-redo floor. *(A further re-save the same day, under the final
> acceptance receipt, follows in the box at the end of this file.)*
>
> **R-01's enumeration was wrong, and it was the one defect in this unit that would have propagated
> into code.** It named **six** `IntegrityError` subclasses. W-1 step 4 raises `PhaseBoundaryError`,
> and R-10 has the stage entry contract catch `IntegrityError` to write the `aborted` registry row —
> so with `PhaseBoundaryError` outside the enumerated hierarchy, an `except IntegrityError` would let
> a **phase-boundary violation exit with no `aborted` row**, precisely the event **NFR-PHASE-01** and
> **NFR-AUD-01** most require recorded. Six adversarial passes did not examine it.
>
> **Settled from upstream authority, not judgement.** `component-methods.md` § Assumptions places
> **fourteen** project-defined exceptions in a shared base and defers placement *"until 3.1 places
> them"* — and this stage **is** 3.1. R-01 now names all fourteen: **six raised here**
> (`ConfigError`, `PreflightError`, `PlatformError`, `DeterminismError`, `ReleaseError`,
> `RegistryError`) and **eight raised by other units on the same base** (`PhaseBoundaryError`,
> `LockedTestError`, `LeakageError`, `AlignmentError`, `SeedError`, `FairnessError`,
> `BootstrapError`, `RegimeError`). Its *"why a base and not six independents"* rationale — which had
> inherited the wrong count — now reads **fourteen**. **This is the failure R-01's own rationale
> predicted**, arriving as a missing **enumeration entry** rather than a missing catch clause.
>
> **Four further corrections in this file:**
>
> - **R-12's box heading** read *"ONE CAPABILITY, NO LONGER AN UNMET OBLIGATION"*, refuted by its own
>   body twenty-six lines below. The previous sweep reported zero live sites because **it matched the
>   words *never-reuse* and this heading contains neither** — the seventh appearance of this class,
>   and the reason the durable remedy is to **name** what is open rather than characterise it.
> - **R-12's roll-up** named two open items where its own Constraint names a third, the
>   `verify_release` read-back hole. Now three.
> - **§ Rules with no acceptance row** gained **R-17**, the other rule in this file declaring no
>   acceptance row, which a table whose stated purpose is *"stated, not buried"* had omitted; and the
>   ⚠ glyph now marks the row whose obligation is uncovered, matching rows 1–2.
> - **§ Assumptions gained a fifth OPEN item**: the cross-unit obligation that the eight exceptions
>   other units raise must be declared as `IntegrityError` subclasses **by those units**. This unit
>   cannot do it for them, and `governance-guards` owns `PhaseBoundaryError`. No cycle — each of those
>   units already depends on `foundation`.
>
> **No rule was added or removed.** The count stays **17 (R-01–R-17)**; derived:
> `grep -cE "^## R-[0-9]+" business-rules.md` → **17**. R-01 and R-12 were amended.
> **§ Assumptions now carries five OPEN items (5/5/5 across the artifacts)** — the boxes above say
> *"four"*, which was true when each was written and is not a current-state claim.
>
> **Every other figure is untouched**: 16 requirements, 2 untested, 7 acceptance rows, §19 at 36
> rows, no TA-37/TA-38. **G-09 remains unsigned**, and no rule here decides a scientific value.


---

> **Re-saved 2026-08-25 under the final acceptance receipt.** The project decision owner ruled to
> accept this unit with its defects disclosed and move to unit 2; one confirming reviewer pass
> records the final state. **Six OPEN items stand in § Assumptions (6/6/6 across the artifacts)**,
> including the two decided-here engineering placements (`IntegrityError` declared in
> `src/data/config.py`; the sentinel and its module-level in-process carrier) and the four that
> await the owner or another unit. The rule count is unchanged at **17 (R-01–R-17)**. A reader at
> the stage gate should treat § Assumptions and this box as authoritative and any count embedded in
> older prose as historical. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.** *(This box was first appended by a script
> write and is re-saved here with the native tooling so the acceptance state carries its audit
> event — the same discipline `project.md` § Corrections records for shell-written artifacts.)*

---

> **Re-saved 2026-08-25 under the tenth-redo receipt.** The final confirming pass found one genuine
> specification gap — the canonical representation `content_hash` is computed over — and the owner
> ruled to fix it alone. **R-11 now specifies it in full**: twelve included caller-supplied fields;
> `dataset_version`, `created_at_utc` and `content_hash` itself excluded; RFC 8785 canonical JSON
> then SHA-256; three content→hash negative controls, including change-only-`created_at_utc` → same
> hash, which proves the idempotence claim. **R-05/W-4's guard is now observable**
> (`"tensorflow" in sys.modules`, checked before `seed_everything`'s own deferred import) and the
> **module-scope framework-import prohibition binds every stage script**, not only `config.py`. The
> rule count is unchanged at **17**; the final pass's documentation findings stand unfixed per the
> ruling, recorded in `business-logic-model.md`'s final `## Review`. **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-25 under the twelfth receipt** (eleventh redo, taken for
> `acquisition`; floor reset mechanical). Byte-identical to the terminal-READY state.
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the thirteenth receipt** (twelfth redo, taken for
> `inventory-and-registry`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-saved unchanged 2026-08-26 under the fourteenth-redo re-confirmation receipt** (redo taken
> for `external-products`; floor reset mechanical). **No content of this unit changed.**
> **G-09 remains unsigned. ⚠ **G-09 IS SIGNED as of 2026-08-28 (D-31)** — this prohibition's stated ground no longer holds, and module creation is authorised. **The other grounds stated alongside it, if any, are untouched**, and D-31's disclosure travels with the signature: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **No scientific value becomes fillable** — TE §18.2 and §18.3's stop-and-report rule are unchanged.**

---

> **Re-confirmation receipt, 2026-08-29.** The 2026-08-27T21:49:36Z REDO jump reset every
> unit's receipt floor. This unit's content had already changed after that floor — the G-09
> pass edited `business-logic-model.md` at 2026-08-27T22:19 (D-29 through D-32; G-09 signed
> under D-31 with its §18.3 preconditions disclosed unmet) — so the owner re-confirmed the
> unchanged post-G-09-pass content via the Consolidated Summary Confirmation at the foot of
> `functional-design-questions.md`, receipted `2026-08-29`. No line above this marker was
> touched by this pass.