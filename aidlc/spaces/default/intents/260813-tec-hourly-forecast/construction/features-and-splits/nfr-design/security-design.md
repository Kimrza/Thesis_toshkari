# Security Design — `features-and-splits`

**Unit** `features-and-splits` (Bolt 7) · **Kind** `library` · **Stage** `nfr-design`

> ## ⚠ NOTHING HERE IS BUILT, AND NOTHING HERE IS DISCHARGED
>
> This unit is the **last boundary before training**. Every mechanism below is a design for a
> module that **does not exist**: `src/features/` holds `__init__.py` only, `src/data/splits.py`
> is absent, `scripts/05_build_features_and_splits.py` is absent, and **five of this unit's six
> test modules are absent** (the sixth exists and covers another unit's limb — § SD-F-00).
>
> **`configs/` does not exist**, so every `data.yaml` / `features.yaml` / `experiment.yaml` read
> specified below is a read against a file that is not there. **No Python interpreter is
> reachable in this environment**, so every check designed here is
> **written-but-unexecutable** — an absence of executions, not an absence of failures.
>
> **BLK-04, BLK-08 and BLK-09 are open exit conditions** on this unit. **No implementation is
> authorised** while BLK-04 stands, independently of G-09 (signed 2026-08-28, D-31, with its own
> TE §18.3 preconditions recorded UNMET).
>
> **TA-33, TA-34, TA-35 and TA-36 are `Pending`** — approved, never run. **FR-P1-04-10 has no
> acceptance row.** WS-10, WS-11, WS-12, WS-13, WS-16, WS-18, TA-07, TA-08, TA-11, TA-15 and the
> §18.3 preflight are **undischarged**. **0 rows are claimed satisfied.**
>
> **No scientific value is decided here.** TE §18.2's absolute rule stands.

## Sources

- `../nfr-requirements/security-requirements.md` — **SEC-F-01** (the ML input space closed by name AND by provenance; the forged-stamp and mislabel residuals; the exactly-two-member permitted-importer set), **SEC-F-02** (train-only transforms enforced by check not shape; the three lag limbs; raw longitude; the frozen window; the two carry-forward rules; support fields), **SEC-F-03** (the three identity stamps; exact calendar folds and embargo; both partition bounds; the locked partition's signature precondition; the single comparison-wide mask), **SEC-F-04** (TA-36's enforcement raise; BLK-08 half B narrowed to `ABL-DIFF`), and its **13**-row coverage table.
- `../nfr-requirements/tech-stack-decisions.md` — **TS-F-01** (provenance stamps ride the artifact's own format; the permitted-producer list is a **new, non-existent** artifact; the Parquet-metadata drop hazard), **TS-F-02** (`scikit-learn`, and why the natural idiom *is* the leak), **TS-F-03** (one window definition, `numpy` tensor + `pandas` matrix, no windowing package), **TS-F-04** (splits computed from record timestamps; `scikit-learn` splitters unused; the mask is one stored artifact), **TS-F-05** (two platforms, CPU-complete).
- `../functional-design/business-logic-model.md` — **W-1**/**W-1a** (the availability matrix and the anchor as a third limb), **W-2** (closed-dictionary construction and its raises), **W-3** (BLK-04's fitting contract, ADR-11 identity form), **W-4**/**W-4a**/**W-4b** (one window definition, the three calls per partition, the provenance stamp, the scored range), **W-5** (six partitions, both bounds, the nesting correction), **W-6** (the locked partition's execution guard and the two-guard split), **W-7** (IRI denial's two properties and two owners), **W-8** (the two carry-forward rules), **W-9** (support fields diagnostic by default), **W-10** (what Bolt 7 may build).
- `../functional-design/business-rules.md` — **R-74**…**R-84**, and **R-76a** (TA-36's enforcement raise and primary test are this unit's).
- **`performance-requirements`, `scalability-requirements` and `reliability-requirements` are absent by scope design**, not missing: `produces_kinds` maps all three to `[service]` / `[service, ui]` and this unit is `library`. Their subject matter is assessed in § Scope note below and drawn from `security-requirements.md`'s own § Scope note, which assessed the same five categories at 3.2.
- `../../../inception/requirements-analysis/requirements.md` — the 13 IDs `security-requirements.md` carries, **plus FR-P1-04-2 (WS-11, TA-08), FR-P1-04-5 (WS-12, TA-11) and FR-P1-04-8 (WS-13, TA-11)**, added at this stage (§ Requirement coverage, Derivation 3).
- `../../../inception/units-generation/unit-of-work.md` § 7 — the **11** requirements carried, `Owns`, and **BLK-04**'s exit-condition ruling.
- `../../../inception/application-design/component-methods.md` — **ADR-11**: `FrameSpec`, `Transform`, `FeatureBundle`, `build_features(...) -> FeatureBundle`, `fit_transforms(bundle, *, partition)`, the identity leak check with its one enumerated `REFIT`→`DEC` exception, `Partition`/`build_partitions`, and § Depth's intra-package carve-out.
- `../../../inception/application-design/services.md` — the bundle's on-disk form and address (`<partition_id>__<role>__<transform_id>/`, `untransformed` for `None`), and the nine stage scripts' read/write split.
- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, referenced not restated.
- `../../governance-guards/nfr-design/security-design.md` — the `open_restricted` chokepoint this unit's W-6 read limb routes through.
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§6.2**, **§7.1**, **§8.1**, **§12**, **§13**, **§15.1**, **§16** (WS-10…WS-13, WS-16, WS-18), **§18.2–18.3**, **§19** (TA-07, TA-08, TA-11, TA-15, TA-33…TA-36).
- `../../../../../../../../PreFlight/vision_document(3)(2)(2).md` — **§6**, **§8.1** (*"History length is not a tuned hyperparameter"*), **§8.3**.
- `evidence/DECISIONS.md` — **D-10.3** (the lags), **D-27** (`ABL-DIFF` owns the inverse; no import-boundary change authorised), **D-28** (the G-06 scored set, 2–31 December, 30 days), **D-31** (G-09 signed, preconditions UNMET).
- `nfr-design-questions.md` — **Q1 = A**, **Q2 = A**, **Q3 = C**, **Q4 = A**, **Q5 = A**, three printed derivations, and the receipted Consolidated Summary Confirmation.
- Workspace inspection, 2026-09-04 — recorded in § SD-F-00.

---

## Scope note

`produces_kinds` yields **two** artifacts for a `library` unit — this file and
`logical-components.md`. The three absent categories are assessed anyway, and the assessment is
narrower than 3.2's because this stage designs mechanisms rather than stating requirements:

| Category | Assessment for `features-and-splits` | Where it lands |
|---|---|---|
| **Performance** | No latency target exists. The work is bounded — three cells, calendar 2022, hourly, a closed dictionary. Two costs are **added by design here** and stated so neither is later read as an unexplained slowdown: per-column provenance resolution on every build (§ SD-F-02), and **three `build_features` constructions per partition** rather than one (`services.md`'s M13 counts them in the cost envelope). | § SD-F-02, § SD-F-04 |
| **Scalability** | Bounded and known; no growth projection. Six partitions, one comparison-wide mask, one window length. | — |
| **Reliability** | **Fail-closed, and Q1 = A extends what that means**: the unit now refuses to produce a feature matrix **at all** while the permitted-producer list is unset. It would rather produce nothing than produce a matrix whose provenance cannot be checked. | § SD-F-01 |
| **Security** | This artifact — **leakage containment**. The threat model is not an attacker; it is a value that arrives with a legitimate name and an illegitimate history. | § SD-F-01…§ SD-F-05 |
| **Observability** | Per-column provenance in `spec.json`; the availability matrix's six recorded fields; `Partition`'s **both** bounds; **counted** exclusions rather than silent ones. | § SD-F-02, § SD-F-04 |

---

## SD-F-00 — What is on disk, and the one upstream claim it contradicts

Verified 2026-09-04, before any mechanism below was designed.

| Claim | Verified state |
|---|---|
| `src/features/availability.py`, `build.py`, `transforms.py`, `windows.py` | **Absent.** `src/features/` holds `__init__.py` only. |
| `src/data/splits.py` | **Absent.** `src/data/` holds `config.py`, `locked_test.py`, `release.py`. |
| `scripts/05_build_features_and_splits.py` | **Absent.** `scripts/` holds `audit_ec1_drivers.py` and `merge_coverage_year.py`. |
| `configs/` | **Absent.** |
| A Python interpreter | **Not reachable.** `python` resolves to the zero-byte Windows Store stub; the `py` launcher is absent. A **3.14** interpreter ran here at some point (`src/data/__pycache__/config.cpython-314.pyc`) — **not** the governed 3.11 pin (TE §8.1, TC-03d), so no execution it performed is governed evidence either way. |
| The four exceptions this unit raises | **All present.** Derivation 2: `LeakageError`, `AlignmentError`, `PartitionError`, `LockedTestError` are 4 of the **17** names in `src/data/config.py`'s `__all__`. Set-difference: **0** owed. |

### The contradiction: `tests/test_locked_test_guard.py` exists, and covers the other limb

**W-10 states that all six of this unit's test modules "DO NOT EXIST".** Derivation 1 puts the
intersection of the owned six against `tests/` on disk at **1**: `test_locked_test_guard.py` is
**there**.

**W-6 assigns that module to this unit** on the stated ground that it *"exercises both
limbs"* — this unit's pre-G-05 **execution** block on `materialise_locked_partition`, and
`governance-guards`' **read** chokepoint through `open_restricted` — and that assigning it to
`governance-guards` *"would close a cycle."*

**The module on disk does not exercise both limbs.** Its own docstring scopes it to the read
chokepoint — `open_restricted` writing a durable `AccessRecord` **before** the read, bypass
refusal, a failed log write aborting the read, after-the-fact verifiability from the log — and
states *"No December target value is read, parsed, counted or computed anywhere in this
module."* Its Governance block cites `governance-guards` R-25 and R-28 and nothing of this
unit's. **Limb 1 is not in it.**

**Nothing is broken today**, because `materialise_locked_partition` does not exist either. What
was at stake is where limb 1's cases go, and the answer is **Q3 = C**:

1. **Limb 1's cases are added to the existing module**, keeping §12's mandated name and leaving
   the mandated `tests/` tree **unchanged** — the only option needing no change record.
2. **The two-unit ownership is stated inside the module**, as an explicit block in its docstring
   naming which cases belong to which unit and which rules govern each, so a later reader does
   not attribute limb 1 to `governance-guards`.
3. **A coverage row in this artifact records the same fact**, so the ownership is visible from
   this side too.

**What this answer does not do.** It does not write limb 1 — the cases are unwritten and the
function they would exercise does not exist. It does not discharge **WS-18** or **TA-18**. And
it does not close the better design: **a separate `tests/test_locked_partition_guard.py` (Q3's
option B) gives clean per-unit ownership**, and remains available as an owner-approved change
record to §12's mandated set, which is the same class of act as `CR-2026-08-22-LEAKAGE-TA`. It
is not taken here because this stage may not add to the mandated test tree.

> **Why this matters beyond bookkeeping.** W-10's "six modules do not exist" and W-6's "one
> module, both limbs" were **both** true when written and are **jointly** false now: the file
> exists and covers one limb. A reader checking either claim alone would conclude the guard test
> was either entirely absent or entirely present. This is the failure mode `project.md`
> § Way of Working (`dp-1`) names — a correction sweep that stops at the artifact that stated
> the fact — reached here by workspace inspection rather than by a review finding.

---

## SD-F-01 — While the permitted-producer list is unset, no feature matrix is produced (Q1 = A)

**The channel this closes, and why nothing else closes it.** § SEC-F-01 records the one leakage
path that survives every existing control: a value **computed from IRI**, **renamed** to match a
legitimate §6.2 field, written into the feature path. It passes R-76's name closure (the name is
on the list), passes `tests/test_iri_denial.py` (there is no `iri_*` name), and passes
`external-products`' import boundary (there is no import). **This unit owns the feature matrix
and is the last boundary before training, so the residual is closable here or nowhere.**

**The check needs an artifact that does not exist.** § SEC-F-01's provenance limb resolves each
column's stamp against a **permitted-producer list per §6.2 dictionary row**, keyed per
**(row, producer)** pair rather than per producer — the sharper form the 2026-09-01 reviewer's
third channel forced, since a column *genuinely* produced by a permitted producer but
**mislabelled to the wrong row** passes a per-producer check. TS-F-01 states plainly that the
list **does not exist**, is **not created** at 3.1 or 3.2, and that whether it is governed config
or a code constant is an undecided TC-03e question.

**The design (Q1 = A).** `build_features` **raises and names the unset list. No feature matrix
is produced at all.**

```
build_features(...):
    producers = snapshot.permitted_producers        # configs/features.yaml or a code constant
    if producers is unset or incomplete:
        raise LeakageError(
            resource = "<the config path or constant>",
            expectation = "a permitted-producer entry for every §6.2 dictionary row "
                          "in the requested feature set",
        )
```

The raise carries R-01's constructor contract — **the resource and the violated
expectation** — so the message names *which* rows lack an entry rather than reporting the list
as generally absent.

> ⚠ **`snapshot.permitted_producers` is an OWED interface amendment, not an existing field**
> *(added 2026-09-04 on adversarial finding 1, Major)*. The sketch above reads the list off
> `ConfigSnapshot`, but **`component-methods.md`'s approved `ConfigSnapshot` is frozen and
> carries no `permitted_producers` field** — the exact mechanism-versus-approved-interface
> defect this project has now recorded on three units. The design intent is unchanged: the
> permitted-producer list reaches `build_features` through the config-loading path. **How it
> reaches it is change-control-gated**: either `ConfigSnapshot` gains the field (an amendment
> to an approved application-design shape, needing a change record — the same footing as
> `acquisition`'s `write_restricted`), or the accessor is a separate loader beside it, decided
> with TC-03e's config-versus-code question at the same gate. Until that clears, this sketch
> is a **proposal to that gate**, and the fail-closed raise binds whichever accessor is
> approved.

> ### Why fail-closed, and why this project has already ruled the same way twice
>
> The deciding fact is **what the artifact would be**. `external-products` answered the
> analogous question with **skip-not-pass**, and that was right there: its containment check
> guards **code that does not exist**, so nothing can be wrongly consumed while the check is
> unavailable. `target-standardization` answered **fail-closed**, and that was right there: its
> check guards **a scientific artifact that would exist and be read**.
>
> **This unit is the second case, in its strongest form.** A feature matrix on disk is
> **trained on**, and *"every reported number inherits the fit"* — `unit-of-work.md`'s own words
> about the four downstream units. A skip recorded on a gate report **does not travel with a
> file**; a full-year matrix with one unverifiable column produces a metric that looks exactly
> like a measurement.
>
> **The cost, stated rather than discovered.** This unit **produces nothing** until the
> permitted-producer list is authored and frozen, and **that list is not this stage's to
> write** — it is either governed config under a D-number (if any entry encodes a scientific
> choice) or a build-graph constant, and TC-03e decides which. Bolt 7 is therefore blocked on an
> artifact nobody has been assigned. **That is the point of stating it here rather than at 3.5.**
>
> **What was rejected and why it is recorded.** Q1's option C — run name closure, skip
> provenance, stamp the bundle `provenance_unverified` — is the best of the weaker answers,
> because the stamp travels **with the data** rather than on a report. It was rejected because
> it still emits a trainable matrix whose one uncheckable property is the one that closes the
> rename channel, and because the field's **absence** in a bundle written by any other path
> would be indistinguishable from a verified one. **If C is ever revisited, the
> `provenance_unverified` field must be REQUIRED on every bundle**, so its absence raises rather
> than reads as clean. Recorded so the option is not re-proposed as an obvious improvement.

**What survives this design, stated with the rule and not only in Assumptions.** A **forged**
stamp — written by hand to name a permitted producer — passes. Provenance closes the
**accidental and the casual** rename; it does not close a **deliberate falsification**. And a
**bundle-less frame**, one that never passed through `build_features`, leaves the consumers
nothing to assert (W-4a's residual). **No artifact may describe NFR-IRI-01 as fully enforced.**

**The module-graph limb is not this design's.** § SEC-F-01's permitted-importer assertion —
that `src/external/iri.py` and `src/external/gim.py` have **exactly two** permitted importers,
`scripts/04_build_external_products.py` and `src/evaluation/` — is a **source-tree** property
owned by `external-products` **R-56**'s transitive scan (W-7). This design states the two facts
that make it checkable rather than aspirational and does not re-implement it: **the allowlist is
not a denylist** (an import from `src/data/`, `src/gnss/`, a training script or a notebook
violates TE §12 exactly as one from `src/features/` does), and the assertion is on the set having
**exactly** those two members, in the one-member-exclusion shape `governance-guards` R-19 uses.

---

## SD-F-02 — The provenance stamps live in `spec.json` (Q2 = A)

**Why a column cannot carry this.** `target-standardization` answered its analogous carrier
question with **a column on every row**, because its lineage caveat is a per-**row** fact.
Provenance here is per-**column** — each column names its §6.2 dictionary row and its producing
artifact — so the column form has no referent.

**Why not Parquet field metadata.** TS-F-01 named the hazard and it is decisive: field-level
metadata survives a `pyarrow` round-trip but is *"easy to drop through an intermediate `pandas`
operation that rebuilds the frame"*, producing a matrix that **fails the check for the wrong
reason**, or worse, one whose stamps were **silently regenerated as blank**. A second reason,
specific to this unit: the bundle's **tensor** half (`tensor.npy`) has no field metadata at all,
so the stamps would exist for one representation and not the other — the asymmetry **WS-13**
exists to catch.

**The design (Q2 = A).** The stamps are a **column-keyed map in `spec.json`**, alongside the
bundle's existing identity fields:

```
<partition_id>__<role>__<transform_id>/
    matrix.parquet
    tensor.npy
    spec.json     partition_id, role, scored_start, scored_end, transform_id,
                  phase_id, source_id, target_definition_id,
                  provenance: { <column>: { dictionary_row, producing_artifact }, ... }
```

Three properties follow, and each is a raise rather than a convention:

1. **A dropped stamp is a load failure.** ADR-11 already fixes that loading a bundle **reads all
   three files or raises**, and that a directory name disagreeing with its `spec.json` **raises
   on load**. Putting provenance in `spec.json` inherits that: a stamp cannot go missing without
   the bundle failing to load. This is the exact hazard TS-F-01 raised, closed by a mechanism
   that already exists rather than a new one.
2. **A column without an entry raises.** `build_features` asserts that the emitted matrix's
   column set and `spec.provenance`'s key set are **equal** — not that provenance is a subset.
   A column added without its entry **raises**; an entry without its column **raises**. A
   default or a blank is not a permitted resolution.
3. **The stamp is the same object as the data.** `FeatureBundle`'s own design chose this over a
   side-car *"so the stamp is the same object as the data and cannot drift from it the way a
   side-car manifest can"*, and `Prediction` carries `partition_id` and `transform_id` onward to
   `07` because *"the stamp has to travel the whole way, not just to the first consumer."*
   Provenance rides that same carrier.

**These stamps are additional to the project-wide identity stamps, not a substitute.**
`phase_id`, `source_id` and `target_definition_id` are required on **the feature matrix and on
every mask** this unit produces — two of the four artifact classes **NFR-TDEF-01** names — and a
mask reaching `evaluation-and-comparison` without all three is a **failure**, not a mask with
missing metadata. **TA-15 belongs to `target-standardization`**; citing it here records an
obligation, never a discharge.

**Cost, accepted and stated.** One `spec.json` entry per column per bundle, and a resolution
step per column per build. `services.md`'s M13 counts the **three** constructions per partition
in the cost envelope; provenance adds to each of them.

**What was rejected.** Option D — both `spec.json` and field metadata, `spec.json`
authoritative — keeps the Parquet self-describing to someone who opens it directly. It was not
taken because two carriers need a stated precedence, and a precedence that resolves silently to
`spec.json` converts a **detectable divergence** into an invisible one. **If D is ever adopted,
a disagreement between the two must RAISE**, not resolve.

---

## SD-F-03 — Leakage containment: the fitting identity, the lags, longitude, the window

**The train-only fitting contract (R-74, W-3, NFR-LEAK-01, BLK-04).** Transforms are fitted on
**training partitions only, per fold, never on the full dataset**, and this is **enforced by
check rather than by shape**. TS-F-02 states why the shape cannot carry it: the most natural
`scikit-learn` idiom — fit once, transform everything — **is** the leak, and *"nothing in the API
distinguishes a fold-correct fit from a full-dataset one; both are one line and the wrong one is
shorter."*

The ADR-11 form of the check is an **identity comparison**, not a containment test:

| Check | Raise | Why containment failed |
|---|---|---|
| `spec.partition_id == partition.partition_id` | `PartitionError` | The declared ids must agree before anything else is compared. |
| `role == "train"`, `transform_id is None`, and the scored range **equals** `train_start..train_end` | `LeakageError` | Both bounds are read from the `Partition` (**R-83**, BLK-09) — a single bound leaves the other inferred, *"and an inferred boundary is where an embargo silently disappears."* |
| `transform.partition_id == spec.partition_id`, with **exactly one** enumerated exception, `REFIT` → `DEC` under `role="score"` | `LeakageError` | The five accepted sets are **strictly nested prefixes**, so containment passed F4's transform on April while F4's fit had seen April. Identity does not have that hole. |
| Any consumer receiving a bundle whose `transform_id is None` | `LeakageError` | The fitting bundle is addressable and visible (`<partition_id>__train__untransformed/`) but **never consumable**. |

**Negative controls, each proving the violation is caught rather than the happy path working**
(`team.md`'s mandated construction practice): fit a transform on the **full dataset** and the
check must **raise**; a `train`-role bundle reaching an evaluation comparison **fails**;
partition *j*'s transform scoring partition *k*'s validation month **fails**; an untransformed
bundle reaching **M-06 fails**; and — added by **R-83** — a training range that is a **strict
subset** of the partition's declared bounds **fails**. The test is
**manifest/bundle-based** (`tests/test_train_only_transforms.py`): it reads the persisted
bundles' identity fields and asserts the refusal. It is **not** static analysis of the nine
scripts and **not** a monkeypatch-and-replay — the mechanism five earlier review cycles proved
unimplementable, because `05` writes and `06`/`07` read, so no evaluation site calls the fitting
path at all.

**BLK-04 is not closed by this design.** It is an **exit condition** on this unit and on
`models-and-baselines`, `evaluation-and-comparison`, `statistical-inference` and
`regimes-diagnostics-reporting`. NFR-LEAK-01's evidence is owed to the **Supervisor at G-04 and
G-05**. Designing the mechanism is not approving the contract.

**The availability limbs (R-75, FR-P1-04-2, W-1/W-1a) — three, not two.** Every predictor is
lagged to its actual availability timestamp: Kp/ap3 **≥ 3 h**, Hp60/ap60 **≥ 1 h**, F10.7 at the
**previous-day observed** value with a **trailing** (never centered) 81-day mean. The third limb
is the **anchor**, and it is the one that catches the case the first two miss — *"a trailing
81-day mean ending at day t passes both the not-centered check and the lag assertion while
including same-day F10.7."* The anchor is **asserted and the mean recomputed from it and
compared**, because *"a recorded end date is a claim; the recomputation is the check."* Dst is
**diagnostic/hindcast-only**; **SSN is absent**, and a grep confirms it. **Never backfill from
future final values** — the release status of every driver is recorded, not only its lag.

> **The deliberate overlap with `external-products` R-57 is by property, and both are needed.**
> R-57 is a **series-level** future-independence property of the driver product (perturb a future
> day, the series must not move). The anchor recomputation is a **value-level** property of the
> mean built here, checkable only where it is built, and it catches a **recorded-but-wrong
> anchor** whose values were never computed from it. Two checks over one fact, not a hedge.

**Raw longitude is never a predictor (R-76, FR-P1-04-10).** Longitude enters **only** through
`lst_sin` and `lst_cos`. Introducing a raw-longitude column **raises** — a negative control
required by `project.md`'s NEVER rule and `team.md`'s mandated practice **independently of
§19**, since FR-P1-04-10 has **no acceptance row at all**. That missing row was **proposed** to
the gate at 3.2 and is **not approved**; a passing control therefore evidences nothing at a gate
until it is. **This stage proposes nothing new and approves nothing.**

**The window length is a frozen constant, not a hyperparameter (R-76, Vision §8.1).** One value
per feature-set ID, shared across all model families, the primary history window **24 hours**.
`experiment.yaml`'s window length **equals 24 and appears in no grid**, and **placing it in a
grid fails**. TS-F-03 adds the design consequence: **no windowing or time-series package is
added**, because *"a library that offers configurable windowing invites the constant to become a
parameter."*

**December must not inform feature selection or a threshold (Vision §8.3).** The trigger is
December being **seen**, not the locked test being opened.

---

## SD-F-04 — The partition set: both bounds, counted exclusions, one mask

**Six partitions, five manifest rows, and the two counts kept apart.** `build_partitions`
returns **6** — `F1`…`F4`, `REFIT`, `DEC`. The **split manifest FR-P1-04-5 gates on enumerates
5** (`F1`…`F4`, `REFIT`, each with training range, validation month and excluded count). The
locked partition's record (`DEC`, its evaluated month, its access-gate state) is recorded
**separately**, because it is access-gated and the manifest is not. **A manifest carrying six
rows fails FR-P1-04-5, and so does one carrying four.**

**Exact fixed calendar boundaries (R-80, FR-P1-04-5, TE §7.1).** F1 Jan–Mar/Apr; F2 Jan–Jun/Jul;
F3 Jan–Sep/Oct; F4 Jan–Oct/Nov; **December locked**. Each carries a **24-hour embargo**, and the
first 24 h are **excluded and counted**. **No random or shuffled cross-validation.** TS-F-04's
design consequence: `scikit-learn`'s CV splitters are **not used** — they default to shuffling,
and *"using one and disabling the shuffle would leave the correct behaviour depending on a
keyword argument."*

**Both bounds, read from the `Partition` (R-83, BLK-09).** `train_start` and `train_end` are
both fields of `Partition`, both read from `configs/data.yaml` by `build_partitions(snapshot)`,
so TC-03e holds and no scientific constant sits in source. **`DEC.train_end = 2022-11-30`** makes
a December fit **unrepresentable by the field itself** — a structural bar independent of
§ SD-F-05's signature guard. **BLK-09 is an open exit condition on this unit alone**, and R-83 is
its contract; approving this design is not the amendment's approval.

**Membership derives from record timestamps, never from a directory or file name.**
`assert_membership_from_timestamps` raises on any row whose month or year disagrees with its
partition — the defect that filed locked-month records into `audit_evidence_2022-01/`. It
**validates and derives nothing**: the training ranges **nest**, so no per-row partition label
exists, and any check needing "which partition" compares **declared identities**.

> **The exactly-one-partition assertion runs over evaluation ROLE, not over training ranges.**
> The ranges nest — Jan–Mar ⊂ Jan–Jun ⊂ Jan–Sep ⊂ Jan–Oct ⊂ Jan–Nov — so an exactly-one
> assertion over them would **fail on ordinary 2022 data**. Roles are disjoint by construction:
> Apr (F1), Jul (F2), Oct (F3), Nov (F4), December (**locked**), training-only for the rest.
> **This is a reading of a frozen Vision §8.1 rule, carried to the gate and not adopted here.**

**Two carry-forward rules with opposite behaviour, in one partition (R-77, W-8).** External
driver values carry forward **at most 3 hours, then the row is excluded**; `vtec_lag_*`
carry-forward is **prohibited outright** and the **window is excluded** instead. Three mechanism
parts: the **field class is a required argument** to the carry-forward path and `vtec_lag_*` is
**rejected at that boundary**; the two classes **partition** the feature set, so a field
belonging to neither or to both cannot escape both rules; and **every excluded window is
counted**, because *"a silent exclusion and a counted one are indistinguishable at the
artifact."*

> **Part 1 is a check, not a type, and this unit has the evidence.** W-3 records an interface
> shape claimed to make a leak *"unrepresentable"* that did not. The runtime rejection is
> asserted, not assumed from the signature.

**Support fields are diagnostic by default (R-78, W-9, FR-P1-04-16).** A support field is
**excluded from the feature set unless an approval ID is present** — a default-exclude, so the
failure mode of a field drifting in *by inclusion rather than by decision* is **impossible**
rather than detectable, and G-04 approval becomes the **only** entry path. The approval's
**timestamp must precede the feature-set freeze**, asserted rather than merely present, since
*"a presence check passes an approval recorded afterwards."* Reads are bounded to hours **≤ t**.
**Target-hour quality fields are permanently forbidden.** Rules 1, 2 and 4 are **separate
assertions with separate failures** — several obligations behind one check is the FR-P1-02-8
failure.

**One comparison-wide intersection mask (NFR-FAIR-01, TC-16).** Computed **once per comparison
set** and **stored**, never recomputed per comparison and never pairwise or model-specific —
*"a recomputed mask is a mask that can differ."* Every mask carries the three identity stamps
(§ SD-F-02).

---

## SD-F-05 — The locked partition: two guards, deliberately separate

`materialise_locked_partition(snapshot, *, g05_signature)` materialises the December partition
**only** when `g05_signature` is present **and verifies**, raising `LockedTestError` when it is
`None` or fails verification. That is the pre-G-05 **execution** block **WS-18** evidences, and
the signature is a **precondition**, not a request parameter.

**The two guards are not one mechanism.** A **read** for the required pre-G-05 coverage audit
does **not** come through here — it comes through `governance-guards`'
`locked_test.open_restricted`. **ADR-03 splits them because the coverage audit is a REQUIRED
read while the metrics run is barred until after G-05**, and conflating them would either bar a
mandatory audit or open the lock. `governance-guards` **supports** WS-18 and TA-18; this unit
owns the guard's execution limb.

**The G-06 apply is the one enumerated exception** to § SD-F-03's identity check: `REFIT` → `DEC`
under `role="score"`. **D-28** fixes the scored set as **2–31 December 2022, 30 days**, first
24 h **excluded and counted**, and **discloses rather than resolves** the Vision §8.2 / TE §7.1
authority conflict, carrying it to **G-05**. D-28's own limitation travels with it: **no
supervisor signature artifact exists and none is claimed.**

**No December execution occurs in this Bolt.** The guard is designed here; it is not run against
the locked month.

**Its test placement is § SD-F-00's Q3 = C**, and limb 1 is **unwritten**.

---

## SD-F-06 — WS-13's parity check (Q4 = A)

**What was open.** R-81 states *"one window definition, two representations"* and records that
what evidence proves the matrix and the tensor encode the same window is **not settled**;
TS-F-03 adds that no tooling choice settles it; the story map adopts no reading.

**What ADR-11 changed, and what it did not.** Both representations now travel in **one**
`FeatureBundle`, built by **one** producer from **one** window definition, which
`component-methods.md` says makes FR-P1-04-8's parity *"structural rather than asserted."* But
W-4 records the fact that makes the structural argument insufficient alone: **the tensor carries
no record timestamps**, so no row-level check can reach it.

**The design (Q4 = A), two ordered assertions.**

1. **Shape and ordering first** — the tensor's dimensions, step count and column order are
   asserted against the matrix's. Cheap, needs no tolerance, and it makes a failing value
   comparison **interpretable** rather than ambiguous between a transposition and a wrong-row
   defect. This is Q4's option C, adopted as a **precondition**, not as the alternative it was
   offered as.
2. **Value-level parity** — the flattened matrix rows are **reconstructed from the tensor's
   slices** and asserted element-wise equal, within the fixture manifest's declared
   floating-point tolerance. This tests the property FR-P1-04-8 actually states — *"contain the
   same underlying window values"* — rather than the construction that is supposed to guarantee
   it, and it is the only form that would catch a defect **in `windows.py` itself**.

> **Why the structural argument alone was rejected.** This unit's own W-3 is the standing
> counter-example: an approved interface was claimed to make a leak *"unrepresentable"*, and it
> was not. A structural guarantee with no assertion is the shape that failed there, five review
> cycles running.

**The dependency, stated as owed rather than assumed.** The floating-point tolerance is
**unset**. `team.md` fixes that fixture assertion data — including *"permitted floating-point
tolerances"* — lives in `tests/fixtures/<fixture_id>/fixture_manifest.yaml` (TE §15.2), and
TE §15.1 fixes that tolerances are **measured from the fixtures and frozen, never invented**. So
**this check is designed now and unrunnable until that value is frozen**, and freezing it is not
this stage's act.

**What this does not do.** It **adopts no reading of TE §16's WS-13 criterion**, which stays
open, and it does not discharge **WS-13** or **TA-11**. `test_common_masks.py` is required here
through TA-11 regardless.

---

## SD-F-07 — What this unit does not own, stated so it is not assumed

- **The module-graph limb of NFR-IRI-01** — `external-products` **R-56**'s transitive
  reachability scan (§ SD-F-01). This unit owns the **data-flow** limb only.
- **TA-15** — `target-standardization`'s row. This unit owes the **stamp on its own outputs**.
- **The station registry's sufficient-provenance question** — `inventory-and-registry`
  **R-45/R-46**. Until it is decided, **`station_lat` is blocked and `lst_sin`/`lst_cos` are
  excluded**, which reaches into both this unit's dictionary and its longitude rule.
- **BLK-08 half A** — `evaluation-and-comparison` **R-103**. This unit's **half B** is narrowed
  to **`ABL-DIFF`** on D-27 (**R-84**), and **neither side declares the contract satisfied
  alone**. The `src/evaluation` → `src/features` edge is **owed and unapproved** — D-27 withheld
  authorisation.
- **The permitted-producer list** — assigned to nobody today (§ SD-F-01).
- **The fixture manifest's floating-point tolerance** — fixture-manifest content
  (§ SD-F-06).
- **The read limb of the locked-test guard** — `governance-guards`' `open_restricted`
  (§ SD-F-05).

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-P1-04-1 | SD-F-01 | WS-10, TA-07 | `Pending` — **data-flow limb this unit's**; module limb is `external-products` R-56's |
| **FR-P1-04-2** | SD-F-03 | WS-11, TA-08 | `Pending` — **added at this stage** (Derivation 3) |
| **FR-P1-04-5** | SD-F-04 | WS-12, TA-11 | `Pending` — **added at this stage** (Derivation 3) |
| FR-P1-04-6 | SD-F-03 | TA-11 | `Pending` |
| FR-P1-04-7 | SD-F-04 | WS-16, TA-11 | `Pending` |
| **FR-P1-04-8** | SD-F-06 | WS-13, TA-11 | `Pending` — **added at this stage** (Derivation 3); WS-13's evidence question stays open |
| **FR-P1-04-10** | SD-F-03 | ⚠ **NO ACCEPTANCE ROW** — proposed at 3.2, **not approved** | untested; negative control required regardless |
| FR-P1-04-12 | SD-F-01, SD-F-02 | **TA-33** | ⚠ **`Pending` — nothing implemented, executed or passed** |
| FR-P1-04-13 | SD-F-04 | **TA-34** | ⚠ `Pending` — `CR-2026-08-22-LEAKAGE-TA`, not implemented |
| FR-P1-04-16 | SD-F-04 | **TA-35** | ⚠ `Pending` — `CR-2026-08-22-LEAKAGE-TA`, not implemented |
| FR-P1-04-17 | SD-F-01, SD-F-03 | **TA-36** | ⚠ `Pending` — enforcement raise and primary test **this unit's** (R-76a) |
| NFR-LEAK-01 | SD-F-03 | TA-11 | `Pending` — **BLK-04 open**; evidence owed to the Supervisor at G-04/G-05 |
| NFR-IRI-01 | SD-F-01 | WS-10, TA-07 | `Pending` — test written, **UNEXECUTED**; **never describable as fully enforced** |
| NFR-FAIR-01 | SD-F-04 | WS-16, TC-16 | `Pending` |
| NFR-TDEF-01 | SD-F-02, SD-F-04 | **TA-15** | `Pending` — row owned by `target-standardization` |
| FR-P1-03-3 | SD-F-02 | **TA-15** | `Pending` — row owned by `target-standardization` |

**Derived and printed.** **8** design sections (SD-F-00…SD-F-07). **16** coverage rows, counted
directly from the table above: FR-P1-04-1, -2, -5, -6, -7, -8, -10, -12, -13, -16, -17,
NFR-LEAK-01, NFR-IRI-01, NFR-FAIR-01, NFR-TDEF-01, FR-P1-03-3. **1** requirement with **no
acceptance row** (FR-P1-04-10), re-derived by counting blank acceptance-row cells rather than
read off the map. **0** rows claimed satisfied. **0** new dependencies. **2** artifacts named as
**owed and non-existent** (the permitted-producer list; the fixture manifest's tolerance).
**0** exceptions owed at their declaration site (Derivation 2).

**The arithmetic of 13 → 16, printed.** `nfr-requirements`' `security-requirements.md` carries
**13** rows. `unit-of-work.md` § 7 carries **11** requirement IDs for this unit. Set-differencing
the two ID lists — **not** their totals, per `project.md` § Way of Working (`c21`) — yields
**3** IDs present in the 11 and absent from the 13: **FR-P1-04-2**, **FR-P1-04-5**,
**FR-P1-04-8**. `grep -c` returns **0** for each across both `nfr-requirements` artifacts. All
three are implemented **verbatim** upstream: FR-P1-04-2 is SEC-F-02's lag rule, FR-P1-04-5 is
SEC-F-03's fold-and-embargo rule, FR-P1-04-8 is SEC-F-03's one-window-two-representations rule.
**13 + 3 = 16.** The reverse difference — 5 IDs in the 13 and not in the 11 (FR-P1-04-7,
FR-P1-04-17, NFR-FAIR-01, NFR-TDEF-01, FR-P1-03-3) — is every one a legitimate later addition,
so nothing is removed.

**This is the third recurrence of one defect class on this unit**: substance implemented,
requirement ID missing from every coverage table. The first two were the 2026-09-01 Major
findings that took the count 7 → 11 → 13. **Superseded figures preserved: 7, 11, 13.** The
three IDs are labelled **added at this stage** so they do not read as inherited, and
**`nfr-requirements` is NOT edited** — it is terminal-READY under a frozen receipt, and the
reconciliation is a gate item.

> ⚠ **A second upstream self-contradiction, routed to the gate 2026-09-04** *(adversarial
> finding 2, Minor)*: `nfr-requirements`' `security-requirements.md`'s own "Derived and
> printed" paragraph asserts **11** coverage rows while its table carries **13** — its
> 2026-09-01 NFR-TDEF-01/FR-P1-03-3 repair updated the table and the correction prose but not
> that paragraph's leading figure. This stage's arithmetic is unaffected (it counts the table,
> 13 + 3 = 16); the upstream file stays unedited under its frozen receipt, and the one-line
> annotate-in-place is a gate item.

## Assumptions & Open Questions

- **[Q1 / SD-F-01]** The **permitted-producer list does not exist**, is **assigned to nobody**, and must be keyed per **(row, producer)** pair. Q1 = A makes it **blocking**: no feature matrix is produced until it is authored and frozen. Whether it is governed config or a code constant is an undecided **TC-03e** question (TS-F-01).
- **[assumption / SD-F-01]** A provenance stamp is trustworthy. **A forged stamp passes.** Provenance closes the accidental and casual rename, not a deliberate falsification. Stated in § SD-F-01's body as well as here, because it bounds what NFR-IRI-01 enforcement reaches.
- **[SD-F-01]** The **bundle-less frame** residual survives: a frame that never passed through `build_features` leaves the consumers nothing to assert (W-4a).
- **[Q2 / SD-F-02]** If option D (both carriers) is ever adopted, a disagreement between `spec.json` and field metadata must **RAISE**, not resolve to `spec.json` silently. Recorded so the softer form is not adopted as an obvious convenience.
- **[Q1 / SD-F-01]** If option C is ever revisited, the `provenance_unverified` field must be **REQUIRED** on every bundle, so its absence raises rather than reads as clean.
- **Open — `tests/test_locked_test_guard.py` exists and covers only `governance-guards`' read limb** (§ SD-F-00). W-10's *"all six do not exist"* and W-6's *"one module, both limbs"* were each true when written and are **jointly false** now. Q3 = C keeps §12's mandated tree untouched; **limb 1 is unwritten and `materialise_locked_partition` does not exist**. Option B — a second module — remains the cleaner ownership design and needs an **owner-approved change record** to the mandated test set.
- **Open — the floating-point tolerance § SD-F-06's parity check needs is unset**, and belongs to `tests/fixtures/<fixture_id>/fixture_manifest.yaml`, measured and frozen rather than invented (TE §15.1/§15.2). The check is designed and **unrunnable** until then.
- **Open — WS-13's evidence question** (R-81). § SD-F-06 proposes a check; it **adopts no reading** of TE §16's criterion.
- **Open — Vision §8.1's exactly-one-partition rule is asserted over evaluation ROLE**, not over the nesting training ranges, which would fail on ordinary 2022 data. A reading of a frozen rule, carried to the gate.
- **Open — a Jan–Nov `DEC`-stamped `train` bundle is shape-representable and built by no call** (W-5, R-80). Closing it structurally was board option 3, which was not ruled.
- **Open — BLK-04 is an EXIT condition** on this unit and on `models-and-baselines`, `evaluation-and-comparison`, `statistical-inference` and `regimes-diagnostics-reporting`. **Approving this design is not the contract's approval.**
- **Open — BLK-09 is an EXIT condition on this unit alone**; **R-83** is its contract, and **BLK-08** is an exit condition on this unit and `evaluation-and-comparison` for both owners. The `src/evaluation` → `src/features` edge is **owed and unapproved** (D-27).
- **Open — the station-registry provenance question** is `inventory-and-registry`'s. Until decided, **`station_lat` is blocked and `lst_sin`/`lst_cos` are excluded**.
- **Open — FR-P1-04-10 has no acceptance row.** Proposed at 3.2, **not approved**; the negative control is required regardless, and a passing control evidences nothing at a gate until the row exists.
- **Open, routed to the gate — the three uncited requirement IDs** (FR-P1-04-2, -5, -8) are added to **this stage's** tables and labelled as added here. `nfr-requirements` is terminal-READY under a frozen receipt and is **not edited**; the reconciliation is a gate item, per `project.md`'s never-edit-a-signed-record correction.
- **Open, unchanged — the signed "nine-site sweep" figure** in this unit's `functional-design-questions.md` Consolidated Summary Confirmation is unsupported (derived count: **3**). The record **stays unedited** and one owner ruling is still owed: annotate in place, or carry the correction in the gate record alone.
- **Carried — `foundation`'s TensorFlow pin stays `TBD — freeze gate`.** This unit builds inputs for the model; it constructs none.
- **Carried — D-31's disclosure travels with the G-09 signature**: the §18.3 preflight never ran, the critical tests are unexecuted in this environment, and `aws_ai_dlc_preflight_report` does not exist. **"No failing critical test" is unproven, not proven.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, approves an acceptance row, closes a blocker, or claims a gate or test as discharged.

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-04T17:09:10Z
**Iteration:** 1 (fresh receipt floor — prior iteration-2 READY superseded per the two out-of-order-recovery redo jumps; this is a full adversarial pass, not a repair-verification pass)

### Findings

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Major | `security-design.md` § SD-F-01, lines 143-151 | The mechanism sketch reads `producers = snapshot.permitted_producers`, but the approved `ConfigSnapshot` dataclass in `component-methods.md` (lines 48-57) has exactly eight fields — `data`, `features`, `experiment`, `seeds`, `hashes`, `snapshot_dir`, `resolved_roots`, `platform` — and no `permitted_producers` field. `snapshot` is frozen (`@dataclass(frozen=True)`), so `snapshot.permitted_producers` raises `AttributeError` against the interface this stage's own Sources cite as authoritative. TS-F-01 states the list's storage form (governed config vs. code constant) is an **undecided** TC-03e question, and the Assumptions section discloses that — but it does not disclose that the specific access path in the code sketch is unsupported by the approved snapshot shape under *either* resolution: if it becomes `features.yaml` content, the accessor would have to route through the existing `snapshot.features` mapping (e.g. `snapshot.features.get("permitted_producers")`), not a top-level attribute; if it becomes a code constant, it would not be a `snapshot` attribute at all. This is the project's own named highest-prior failure class — a mechanism that cannot run as written against the interface a shared contract approves — and nothing in the artifact flags this specific sketch as illustrative-only pending that resolution. |  Either mark the code block explicitly as illustrative pseudocode pending TC-03e (stating that `snapshot.permitted_producers` is a placeholder, not a claim about `ConfigSnapshot`'s current shape), or rewrite it to route through `snapshot.features` and note that a `ConfigSnapshot` field addition is one of the two possible TC-03e outcomes and is not yet approved. |
| 2 | Minor | `security-design.md` Sources line 29 and § "The arithmetic of 13 → 16" (line 520) | `security-requirements.md`'s own "Derived and printed" paragraph (its lines 226-229) states its coverage table has **11** rows, but the table it is describing (its lines 212-224) has **13** rows — it omits `NFR-TDEF-01` and `FR-P1-03-3` from its own recorded derivation (7 → +2 → +2 = 11, never adding the two rows visibly present at lines 223-224). `security-design.md` correctly derives and uses **13** (matching the actual table, not the upstream artifact's stale self-count), so this stage's own arithmetic is unaffected — but the artifact cites "its 13-row coverage table" without ever noting that the cited artifact's own prose disagrees with itself on that count. This is the same class of stale-count defect `project.md`'s corrections repeatedly warn about, now found one hop upstream of where this artifact reads it. | Add one clause to the Sources line or the "13 → 16" derivation noting that `security-requirements.md`'s own printed count (11) undercounts its table (13) by omitting NFR-TDEF-01 and FR-P1-03-3, so a future reader who trusts that artifact's stated total rather than its table is not misled. Route to the gate alongside the other frozen-artifact staleness items already carried (per `project.md`'s never-edit-a-signed-record correction) — `security-requirements.md` is not this stage's to edit. |

### Verified — did not break

- **Receipt-floor notes (Focus 1).** Both notes were treated as claims, not context, and checked line-for-line. Neither introduces a new design claim — both are procedural narratives (what was fixed, why two jumps were needed, confirm→write→review ordering) that make no assertion about F-1…F-4's guarantees, the coverage counts, or any requirement's status. Neither contradicts the body text above it: `security-design.md`'s note's claim that "`security-design.md` needed no repair on that finding" is independently confirmed — § SD-F-06 (line 467) already reads "`test_common_masks.py` is required here through TA-11 regardless" pre-dating the note. `logical-components.md`'s note's claim "no design content changed across either recovery" is consistent with the actual diff described: F-2's test-module listing and count derivation were relabelled/re-derived, but the four-component boundary, the guarantees, the failure-domain table and the requirement-coverage table are untouched.
- **The F-2 ownership repair, verified independently against `business-logic-model.md` rather than the artifact's own word (Focus 2).** `business-logic-model.md:937` reads verbatim `"test_common_masks.py — owned by evaluation-and-comparison"`. `unit-of-work.md` § 7's `Owns` line (its own text, confirmed by direct read) lists exactly five modules — `test_feature_availability.py`, `test_iri_denial.py`, `test_split_embargo.py`, `test_train_only_transforms.py`, `test_locked_test_guard.py` — and omits `test_feature_leakage_guards.py`, exactly as SD-F-00 and F-4's row state. `business-logic-model.md`'s W-10 section independently confirms the corrected owned-set is six ("Six, derived: 5 + 1... `unit-of-work.md` § 7's `Owns` names five... and omits `tests/test_feature_leakage_guards.py`, which the story map's § Cross-unit responsibilities assigns here (R-76a)"). `logical-components.md`'s F-2 row's 6-item "owned here" enumeration matches this canonical set name-for-name.
- **The replacement derivation, recounted from the names actually printed (Focus 2).** F-1 → `test_feature_availability.py` (1); F-2 → `test_feature_leakage_guards.py`, `test_iri_denial.py`, `test_common_masks.py` (3); F-3 → `test_split_embargo.py` (1); F-4 → `test_train_only_transforms.py`, `test_locked_test_guard.py` (2). Total distinct = 7; owned-here (excluding `test_common_masks.py`) = 6; of the 6, absent = 5, present = 1 (`test_locked_test_guard.py`, confirmed present on disk in `tests/`, § below). **7 = 6 + 1** and **6 = 5 + 1** both check out against the printed enumeration.
- **`test_locked_test_guard.py`'s existence and scope, confirmed on disk (Focus 4).** `tests/` on disk holds exactly six files: `test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py`. `test_locked_test_guard.py` exists, confirming SD-F-00's Derivation-1 intersection of 1. Read the file directly: its docstring states verbatim "No December target value is read, parsed, counted or computed anywhere in this module," its five test groups (durable-record-before-read, refusal outside the chokepoint, failed-log-write abort, record-shape enforcement, one-door static membership) all exercise `open_restricted` / `AccessRecord`, and no test in the file references `materialise_locked_partition` (which does not exist). This confirms the artifact's claim that the module covers only `governance-guards`' read limb and that limb 1 (this unit's execution guard) is unwritten. W-6 in `business-logic-model.md` independently confirms the same reasoning for assigning the module here ("assigning it there would close a cycle").
- **§12's mandated `tests/` tree, checked directly (Focus 4).** `Technical_Environment_and_Research_Implementation(1)(2).md`'s §12 tree (line 694) names only `test_locked_test_guard.py`; no sibling `test_locked_partition_guard.py` exists in it. Q3=C's rationale — that adding a second module needs an owner-approved change record to the mandated tree — holds.
- **Q1=A / W-4's three-call sequence interaction, traced end to end (Focus 5).** `business-logic-model.md` W-4 shows ADR-11's approved sequence issues `build_features` three times per partition (`raw`, `train`, `score`), all through the same function. SD-F-01's raise is unconditional on `build_features` itself, so a fail-closed producer-list check blocks all three calls identically — the fitting (`raw`) bundle never gets special-cased around the check. No inconsistency found: nothing in `component-methods.md` or `services.md` assumes a bundle can exist independent of a `build_features` call succeeding.
- **Q2=A vs. ADR-11, checked against `services.md` verbatim (Focus 6).** `services.md` (lines 94-96, 119-122) states exactly what the artifact claims: "loading a bundle reads all three or raises" and "a directory whose name disagrees with the `spec.json` inside it is detectable and raises on load." Both quotes are verbatim matches, not paraphrase drift.
- **Q4=A's tolerance dependency (Focus 7).** `team.md`'s fixture convention (fixture assertion data, including "permitted floating-point tolerances," lives in `tests/fixtures/<fixture_id>/fixture_manifest.yaml`, measured and frozen never invented) matches the artifact's claim exactly. `tests/fixtures/` does not exist on disk (confirmed: only the flat `tests/` files above exist, no `fixtures/` subdirectory), consistent with "unset."
- **The three added requirement IDs (Focus 3).** `requirements.md` carries FR-P1-04-2 (line 371, WS-11/TA-08), FR-P1-04-5 (line 374, WS-12/TA-11) and FR-P1-04-8 (line 377, WS-13/TA-11) — all three acceptance-row citations match exactly. Grepped both `nfr-requirements` artifacts for all three IDs: zero occurrences in either, confirming "added at this stage."
- **The 13→16 coverage arithmetic and per-component distribution (Focus 3).** Both files' coverage tables independently counted at 16 rows with identical ID sets. `logical-components.md`'s claimed per-component distribution (F-1:1, F-2:8, F-3:5, F-4:2) recounted directly against its own table and confirmed to sum to 16.
- **Overclaim sweep (Focus 8).** Grepped both files for "is satisfied/closed/discharged/approved/decided/resolved" outside of explicit negations; every hit is a negation ("NOTHING... IS DISCHARGED," "No scientific value is decided," "Until it is decided, ... blocked"). No overclaim found.
- **Mermaid validity (Focus 10).** `logical-components.md`'s diagram: 7 declared nodes, 9 edges, valid `graph TD` syntax with `<br/>`-separated multi-line labels. The text fallback names all 9 edges (CFG→F1, CFG→F3, PPL→F2, F1→F2, F3→F2, F3→F4, F2→F4, F4→DOWN, F2→DOWN) with no omission or addition.
- **Sensor and stage requirements.** Both files carry well over two H2 sections (required-sections sensor). Every `consumes:` artifact named in the dispatch brief is cited in each file's own Sources section with specific claims attributed (upstream-coverage sensor).

### Coverage limits

- Did not read any sibling unit's `construction/<other-unit>/` content; `test_common_masks.py`'s ownership was verified against the shared/consumed `business-logic-model.md` only, and `unit-of-work.md` § 7 (shared inception contract), per the read-scope bound and its stated carve-out.
- Did not re-execute the full cross-reference sweep of the ~30 Sources citations against `business-rules.md` R-74…R-84 individually; spot-checked R-83 and R-76a directly (both exist and match the claimed content) and relied on the prior iteration's spot-checks for the remainder.
- Did not re-derive the "7 across 5 units" vs "8 across 5" open discrepancy or the "nine-site sweep" figure in either file's Assumptions; both are already flagged as unresolved and routed to the gate by the artifacts themselves.
- Did not independently verify whether `test_common_masks.py` is actually absent on disk (it is outside this unit's ownership and outside read-scope for `evaluation-and-comparison`'s tree); the "(absent)" label is a documentation note, not a load-bearing claim of this unit's own contract.
- Finding 1's severity reflects that the mechanism sketch sits inside a section this artifact itself repeatedly labels "written-but-unexecutable" (no interpreter, no `configs/`) — the defect is real and checkable against the approved interface, but it is a code-sketch/interface-binding defect rather than a defect in the security guarantee or the fail-closed decision itself, both of which remain sound.

---

## Receipt-floor note — 2026-09-04

**This is one of the two units a redo jump was taken for.** The prior adversarial pass returned
READY with one Major: `logical-components.md` listed `test_common_masks.py` among this unit's own
test modules when it is `evaluation-and-comparison`'s, making the distinct names printed across
F-1…F-4 total **7** against that file's own "6 test modules owned". The project decision owner
directed that all findings be fixed. A terminal review receipt freezes a `produces[]` artifact,
so the fix needed a jump to clear this stage's receipt floor — which invalidated **every** unit's
receipts, not only this one's.

**The fix is applied** in `logical-components.md`: F-2's listing now separates *owned here* from
*required here but owned elsewhere*, and the bare count is replaced by a printed derivation —
**7 distinct = 6 owned + 1 owned elsewhere**, and **6 owned = 5 absent + 1 present**. The
ownership attribution was verified independently against `business-logic-model.md` rather than
taken from this artifact's own word.

**`security-design.md` needed no repair on that finding** — § SD-F-06 already described
`test_common_masks.py` as *"required here through TA-11 regardless"*, which is why the defect was
confined to one file.

**Ordering, recorded because it cost two jumps.** The first attempt fixed the artifacts, then
re-reviewed, then re-collected the human confirmations — leaving the artifact writes *older* than
the confirmation and wedging the engine against its own freeze. A second jump was taken and the
steps run in the order that terminates: **confirm, then write, then review.** This note is that
write.

**Every other claim, count and open item above stands as recorded**, including the still-open
"nine-site sweep" figure and the "7 across 5 units" versus "8 across 5" discrepancy.

---

## Review — 2026-09-04 confirming pass (fourth floor)

**Reviewer:** aidlc-architecture-reviewer-agent
**Verdict:** READY
**Date:** 2026-09-04T22:22:56Z
**Iteration:** 1 (confirming pass on the fourth receipt floor)

### Findings

None.

### Verified — did not break

- **Fix 1 (prior Major) confirmed against `component-methods.md` directly.** Read the approved `ConfigSnapshot` dataclass verbatim (lines 47-57): `@dataclass(frozen=True)` with exactly eight fields — `data`, `features`, `experiment`, `seeds`, `hashes`, `snapshot_dir`, `resolved_roots`, `platform` — and no `permitted_producers` field anywhere in the class or elsewhere in the file (grepped the whole document for `permitted_producers`: zero hits outside this unit's own artifacts). The dated correction blockquote at § SD-F-01 (lines 157-168) is present, states the accessor is an **owed, change-control-gated interface amendment**, states the two possible resolutions (a `ConfigSnapshot` field addition under change control, or a separate loader decided with TC-03e), and states the design intent is unchanged while the sketch is a proposal to that gate. `logical-components.md`'s F-2 bullet (line 287) carries the matching cross-referencing note, dated and pointing back at this section. No other live text in either file implies `permitted_producers` already exists on `ConfigSnapshot` — every other reference to the list (§ SD-F-01 body, § SD-F-07, Assumptions, Shared resources) states it as non-existent and unassigned.
- **Fix 2 (prior Minor) confirmed against `security-requirements.md` directly.** Its own "Derived and printed" paragraph (line 226) states verbatim "**11** coverage rows," while its own table (lines 210-224) was counted directly and contains **13** distinct requirement rows (FR-P1-04-1, -10, -12, -17, -6, -7, -13, -16, NFR-LEAK-01, NFR-IRI-01, NFR-FAIR-01, NFR-TDEF-01, FR-P1-03-3). The self-contradiction is real: the artifact's later paragraph (line 231, "Corrected again 2026-09-01... 11 → 13") shows the table and that later paragraph were updated for the NFR-TDEF-01/FR-P1-03-3 addition, but the earlier "Derived and printed" paragraph's leading figure was not swept. The routed note added to this artifact (lines 551-557) states this accurately — it names the 11-vs-13 gap, correctly attributes it to the omission of NFR-TDEF-01 and FR-P1-03-3 from that one paragraph's count, confirms this stage's own 13+3=16 arithmetic is unaffected, and explicitly declines to edit the upstream frozen-receipt artifact, routing the one-line fix to the gate per `project.md`'s never-edit-a-signed-record correction. Accurate and appropriately scoped.
- **F-2 test-module derivation (7 = 6 owned + 1 elsewhere; 6 = 5 absent + 1 present) spot-verified unchanged** in both files — the printed decomposition in `security-design.md` (Derivation-1/2 language, § SD-F-00) and `logical-components.md` (lines 267-275) still match name-for-name, and `test_common_masks.py` is still correctly attributed to `evaluation-and-comparison` in both.
- **16-row tables and 13+3 arithmetic unchanged and consistent.** Both files' Requirement coverage tables were recounted directly at 16 rows each with identical ID sets; the "13 → 16" derivation (lines 533-542) still holds: set-differencing `unit-of-work.md` § 7's 11 IDs against `security-requirements.md`'s 13 correctly yields 3 net-new IDs (FR-P1-04-2, -5, -8), 13+3=16.
- **§ SD-F-00's `test_locked_test_guard.py` claim/disk contradiction record is unchanged** and still accurately states the module exists, covers only `governance-guards`' read limb, and that limb 1 (this unit's execution guard) is unwritten — consistent with the prior pass's independent disk verification.
- **Regression grep confirms BLK-04/BLK-08/BLK-09 remain open** (14 occurrences, all framed as open exit conditions, none marked satisfied or closed) and the overclaim sweep (`is satisfied|is closed|is discharged|is approved|is decided|is resolved`) returns only negated hits ("NOTHING... IS DISCHARGED," "No scientific value is decided," "Until it is decided, ... blocked") — no new overclaim introduced by either fix.
- **The permitted-producer list is still stated as non-existent and unassigned** everywhere it is mentioned in both files (§ SD-F-01, § SD-F-07, Assumptions, Shared resources, and the new correction blockquote itself) — the fix for finding 1 clarifies the access-path defect without ever claiming the list itself now exists.

### Coverage limits

- Did not re-verify the ~30 Sources citations against `business-rules.md` R-74…R-84 individually beyond the prior pass's spot-checks (R-83, R-76a); this confirming pass's scope was the two named fixes plus a regression sweep, per the dispatch brief.
- Did not re-read sibling `construction/<other-unit>/` content; `component-methods.md` (shared inception contract) and `security-requirements.md` (this unit's own upstream `nfr-requirements/`) were the only files opened beyond the two primary artifacts, both within the stated read-scope bound.
- Did not re-derive the "7 across 5 units" vs "8 across 5" discrepancy or the "nine-site sweep" figure; both remain flagged as unresolved and routed to the gate by the artifacts themselves, unchanged from the prior pass.

## Review — 2026-09-05 re-affirmation (post-gate receipt refresh)

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-09-05T08:16:41Z

**Prior terminal review quoted verbatim:** "## Review — 2026-09-04 confirming pass (fourth floor) ... **Reviewer:** aidlc-architecture-reviewer-agent ... **Verdict:** READY ... **Date:** 2026-09-04T22:22:56Z ... **Iteration:** 1 (confirming pass on the fourth receipt floor) ... ### Findings ... None."

**Confirmed no edits since that terminal review.** This artifact and `logical-components.md` were named in the dispatch as NOT revised by the gate-rejection round that touched `evaluation-and-comparison`, `statistical-inference`, `regimes-diagnostics-reporting`, and `fixtures-and-reproducibility`. Reading the full file end to end confirms the "2026-09-04 confirming pass (fourth floor)" section is the last content in the file — nothing follows it except this re-affirmation entry being appended now.

**Spot-checked 3 of the prior pass's verified claims, all still hold:**
1. `component-methods.md`'s `ConfigSnapshot` (lines 49-57, `@dataclass(frozen=True)`) still carries exactly the 8 fields quoted by the prior review — `data`, `features`, `experiment`, `seeds`, `hashes`, `snapshot_dir`, `resolved_roots`, `platform` — and still no `permitted_producers` field. § SD-F-01's fail-closed sketch and its dated correction blockquote (lines 157-168) remain internally consistent with this: the sketch is still stated as illustrative/proposal-to-gate, not a claim that the field exists.
2. `security-requirements.md` line 226 still reads "**11** coverage rows" against its own 13-row table — the self-contradiction the prior pass routed to the gate (rather than editing the frozen upstream artifact) is unchanged, and this artifact's own arithmetic (13 + 3 = 16) remains unaffected by it.
3. `tests/` on disk still holds `test_locked_test_guard.py` and no sibling `test_locked_partition_guard.py` — SD-F-00's claim that this unit's execution-guard limb (limb 1) is unwritten, and that the module on disk covers only `governance-guards`' read limb, still matches what is on disk.

No new findings. The standing verdict is re-affirmed as-is; nothing was repaired.

READY
