# NFR Design — Questions — `external-products`

**Unit** `external-products` (Bolt 5) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps the other three to `[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands. The `iricore`
pin with its switch set, topside option and 2000 km ceiling, and the CODE final GIM product
version, both stay `TBD — freeze gate` (TS-E-01, TS-E-02). No question here fills either.

> ## ⚠ UPSTREAM STATUS CLAIMS CHECKED AGAINST THE WORKSPACE, 2026-09-02
>
> Verified before drafting these questions, per the owner's current-state ruling. **One of
> the three corrections does NOT run in this unit's favour**, and it is the one that matters
> most:
>
> | Upstream claim | Actual state |
> |---|---|
> | Banner and coverage table: *"`tests/test_iri_denial.py` is **written but UNEXECUTED**"*, and FR-P1-04-1 / NFR-IRI-01 marked *"`Pending` — test written, UNEXECUTED"* | **False, and against this unit.** `tests/test_iri_denial.py` **does not exist.** `tests/` holds six modules: `test_acquisition_window.py`, `test_locked_test_guard.py`, `test_merge_script_restricted_reads.py`, `test_phase_boundary.py`, `test_release_contract.py`, `test_release_hashes.py`. **NFR-IRI-01's negative control is not written at all**, not merely unrun. |
> | Banner: *"No Python interpreter exists in this environment"* | **Stale.** `python --version` returns **Python 3.14.7** — present, and **off the governed 3.11 pin (TE §8.1)**, so anything it runs is **not governed evidence**. |
> | `src/external`'s three modules | **None exists.** `src/external/` holds `__init__.py` only (24 bytes). `src/features/`, `src/models/`, `src/evaluation/` and `src/gnss/` each hold `__init__.py` only. `scripts/` holds `audit_ec1_drivers.py` and `merge_coverage_year.py`. R-55's amendment is still owed. |
> | W-8: `audit_ec1_drivers.py`'s exit-code gap | **Open, confirmed.** `scripts/audit_ec1_drivers.py:184` is an unconditional `return 0` at the end of `main()`, reached whether or not months are missing — line 181 prints `missing=` to stdout and nothing changes the exit code. |
>
> **The consequence for this stage, stated up front:** neither the modules the import
> allowlist protects nor any module that could violate it exists today. Question 1 is about
> exactly that.

**What is already fixed upstream and is not re-asked.** The allowlist is enforced
**transitively**, with the **static check authoritative** for this unit, using stdlib `ast`
and no new dependency (R-56, W-3, TS-E-03). Its two disclosed gaps stand as stated: dynamic
imports get a **grep-class visibility check** plus review, and a run-time-computed module
path is an **uncovered residual**. IRI generation is **blocked** until R-59's pre-declared
validation passes (SEC-E-03). GIM is **evaluation-time-only** and no independence claim
precedes the `gim_network_overlap_flag` audit (SEC-E-02). A revised product is
**byte-identical or explicitly divergent**, refusing to overwrite (SEC-E-05). Driver rules —
trailing F10.7 mean proven as a property, ≤3 h carry-forward then exclude, per-predictor
lags, time-indexed-only series, Dst's three restrictions, never backfill from final values —
are all fixed (SEC-E-04). None of that is reopened here.

---

## Question 1

**The import allowlist cannot fail today, because nothing it governs exists.** R-56's static
check asks whether any module outside `scripts/04_build_external_products.py` and
`src/evaluation/` can reach `src/external/iri.py` or `gim.py`. Verified this session:
**neither target module exists**, and every package that could import one holds only
`__init__.py`. The check as specified returns **pass**.

A pass that means *"the thing I protect is not there"* is not evidence of containment, and
this is the project's most safety-critical rule — Vision §7.1 calls it *binding
architectural*. It is also **not** a hypothetical: TE §18.3's preflight gate criterion is
*"zero unresolved P0 fields and **no failing critical test**"*, and a vacuous pass satisfies
that criterion while proving nothing.

What should the check do when its subject is absent?

A. **Skip with a stated reason in the ordinary suite, and let the §18.3 preflight treat a
   skipped critical check as UNMET** — `pytest.skip("src/external/iri.py absent: containment
   is unverifiable, not verified")`, so the run record says `skipped`, never `passed`; the
   preflight's *"no failing critical test"* is read as *"no critical check unmet"*, and a
   skipped one is unmet
   > **Impact**: The ordinary suite stays honest and green while the unit is legitimately unbuilt, and the **gate** — the place the distinction actually matters — refuses to accept an unverified containment rule. It requires the §18.3 preflight to distinguish skipped from passed, which is a definition this stage would be fixing rather than inheriting. Risk named: a skip is easy to normalise, and a permanently-skipped critical check is how a control quietly stops being one — the preflight coupling is what stops that here.

B. **Fail closed, always** — the check asserts the allowlist **and** that `iri.py` and
   `gim.py` exist; a missing target fails
   > **Impact**: A vacuous pass becomes impossible, with no new gate semantics to define. It turns a legitimate scaffolding state into a **red suite today and until the modules are written**, on a unit whose own upstream says IRI generation is blocked anyway. A permanently-red suite trains people to ignore red, which is the same failure as a normalised skip arriving by the opposite road.

C. **Skip with a reason, and no preflight consequence**
   > **Impact**: Honest in the run record and cheap. It leaves TE §18.3's gate able to pass with NFR-IRI-01's containment unverified, which is precisely the reading the gate exists to prevent.

D. **Pass, and record the vacuity as a machine-readable field** in the run manifest
   > **Impact**: Green suite, and the fact is at least captured. It puts `passed` next to the project's binding architectural rule when nothing was checked, and this project's own evidence records that a caveat attached to a figure is how a caveated figure becomes a relied-on figure.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the distinction that matters is between *verified* and
> *unverifiable*, and only A puts that distinction where a decision is made. B is defensible
> and I would take it if the preflight could not be made to read a skip, but it imposes a red
> suite on a state the project's own plan calls correct. What A costs is honest: it makes this
> stage responsible for a §18.3 reading — *"no failing critical test"* means *"no critical
> check unmet"* — and that reading should be stated in the design rather than assumed, because
> it is the load-bearing half of the option.

[Answer]: A

---

## Question 2

`business-logic-model.md` records **`FeatureAvailabilityError`'s declaration site as open**,
with two candidates named: *"a cross-unit agreement into `src/data/config.py`, or the
`src/data/exceptions.py` §12 amendment."* W-3 additionally raises **`ImportBoundaryError`**.
Neither exists — `src/data/config.py`'s `__all__` holds 17 names and neither is among them.

**The owner answered this exact question one unit ago.** At `inventory-and-registry`, Q2 = A
placed `InventoryError` and `AuditScopeError` in `src/data/config.py`, deriving from
`IntegrityError`, **riding R-01's *"any future integrity-related exception"* clause** rather
than being promoted into its enumeration. This unit's upstream reaches the same reading
independently: `FeatureAvailabilityError` *"derives from `foundation` R-01's `IntegrityError`
base under the any-future clause and is **not** claimed as one of R-01's named fifteen."*

What differs here is the second candidate: an `src/data/exceptions.py` **§12 amendment**,
which `inventory-and-registry` did not have on the table.

Where do these two exceptions live?

A. **`src/data/config.py`, riding R-01's any-future clause** — the same disposition as
   `inventory-and-registry`'s Q2 = A, extended to `ImportBoundaryError` and
   `FeatureAvailabilityError`
   > **Impact**: One declaration site across every unit, consistent with the 2026-08-28 owner ruling that moved `PartitionError`'s site *into* `config.py`. No §12 amendment, no change record. It keeps growing a module whose docstring already carries a named-subset disclaimer, and `config.py` becomes the place every unit's exceptions land regardless of which unit owns their meaning.

B. **The `src/data/exceptions.py` §12 amendment** — move unit-local exceptions to a dedicated
   module
   > **Impact**: A cleaner end state, and the option this unit's own upstream names first among equals. It is a **§12 amendment** — a change record against the mandated repository tree — and it would leave `config.py`'s existing 17 declarations either split across two modules or needing a migration, which is a larger move than this stage should make on its own.

C. **Declare in this unit's own modules** — `ImportBoundaryError` in the boundary check,
   `FeatureAvailabilityError` beside the availability resolver
   > **Impact**: Ownership matches the raiser. It contradicts R-01's declaration-site rule and the 2026-08-28 ruling, and it fails on its own terms here: `ImportBoundaryError` is raised by a **test** over modules that must not import each other, so a leaf declaration site is exactly the wrong shape.

D. **Defer both to 3.5**
   > **Impact**: Nothing is decided against modules that do not exist. It leaves two exceptions with no home while the upstream has already carried the question open through `functional-design` and `nfr-requirements` — a third deferral.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — consistency across units is the decisive argument, and it
> is not merely tidiness: splitting declaration sites between `config.py` and
> `exceptions.py` would defeat the stated reason `config.py` was ruled the site, which is that
> a package forbidden from importing a leaf module must still be able to catch what it raises.
> B is the better end state and should be raised as a §12 amendment on its own merits, with
> **all** existing declarations migrating together — not as a side effect of placing two new
> ones.

[Answer]: A

---

## Question 3

SEC-E-01 states, in the rule body, the residual that survives **both** IRI-containment limbs:

> *"A value numerically derived from IRI, renamed so it carries no `iri_*` name, and stripped
> of its provenance stamp, defeats BOTH limbs… What bounds it is not a mechanism but a
> **person**."*

That is honest, and it is stated as a residual rather than a gap being closed. But the
residual is a **conjunction of two independent acts** — renaming, *and* stripping provenance
— and a design can address them separately.

Limb 2 as specified asserts *"no `iri_*` column, no IRI-derived residual, no IRI-computed
value"*: detection by **name** or by **provenance saying IRI**. A column whose provenance is
**absent** satisfies that assertion today.

Should the design narrow the residual, and how?

A. **Flip the provenance default: absent provenance FAILS** — every value
   `04_build_external_products.py` writes carries a provenance stamp, and the feature-matrix
   assertion admits a column only if its provenance is **present and not IRI**, rather than
   rejecting only columns whose provenance says IRI
   > **Impact**: Closes the **stripping** half of the residual outright: a laundered value must now forge a provenance stamp rather than merely delete one, which is a different and more deliberate act. It does **not** close the rename-and-recompute-from-scratch case, and saying so is part of the design. Cost: every column in the feature matrix needs a provenance value, including ones no unit currently stamps — a real obligation on `features-and-splits`, whose surface this is, and therefore an addition to the two-half contract already owed.

B. **Add a numeric fingerprint** — correlate candidate feature columns against the IRI
   benchmark table at evaluation time and flag high agreement
   > **Impact**: Reaches the rename-and-recompute case that A cannot. It is a statistical test on a quantity that **correlates with IRI by construction** — VTEC and an IRI VTEC estimate of the same cell and hour are supposed to agree — so its false-positive rate is high and its threshold would be a new number invented beside frozen ones. It would also require the IRI benchmark table to exist, and it is blocked.

C. **Accept the residual as stated, add no mechanism** — carry it as a reporting-discipline
   obligation: no artifact may describe NFR-IRI-01 as fully enforced
   > **Impact**: Exactly what SEC-E-01 already commits to, and it costs nothing. It leaves the cheaper half of the residual — deleting a stamp — uncovered when a design change closes it, and "a person is what bounds it" is a weaker statement than it needs to be while an unclaimed mechanism exists.

D. **Defer to `features-and-splits`**, since the feature matrix is that unit's surface
   > **Impact**: Correct about ownership. It also hands the other unit a question this unit is better placed to answer, because this unit is where the values originate and where the stamp would be written.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it converts *"absence of evidence is admissible"* into
> *"absence of evidence fails"*, which is the same fail-closed shape this project already uses
> for an absent IGRF version and an absent `madrigalWeb_version`, and it closes the cheaper of
> the residual's two acts. The honest limits: it does not close the residual, the rename case
> survives, and it adds an obligation to the `features-and-splits` half of a contract that is
> already owed rather than agreed. B should be declined explicitly rather than left unmentioned
> — a correlation test against a benchmark the data is supposed to resemble is a threshold this
> project has no basis to set.

[Answer]: A

---

## Question 4

`logical-components.md` needs a boundary criterion. The three sibling units each chose a
different one and each said why: `foundation` used **failure consequence**;
`governance-guards` used **enforcement timing**; `inventory-and-registry` used **how the
failure reaches a human**.

This unit's material has a shape none of those fits well. Everything here is a **boundary
against something getting in**, and the three things are unrelated to each other: IRI and GIM
getting into the model; the **future** getting into a forecast origin; an **unvalidated
benchmark** getting into the comparison.

What criterion should the decomposition use?

A. **What the component keeps out** — three components: (E-1) **containment**, keeping
   IRI/GIM out of training and inference (W-3, SEC-E-01's two limbs); (E-2) **forecast
   safety**, keeping the future out of a forecast origin (W-4, W-5, W-9 — the trailing mean,
   the lags, carry-forward, release grades, never backfilling from final values); (E-3)
   **benchmark and comparator integrity**, keeping an unvalidated benchmark or an
   unaudited-independence comparator out of the comparison (W-6, W-7)
   > **Impact**: Names the property that actually distinguishes this unit's three concerns, and each component has a different adversary — a module graph, a clock, and a gate. It groups the trailing-mean property test with the carry-forward bound and the lag rules, which is right because all three are one rule about time. W-8's exit-code work and W-10's build boundary sit across all three and need placing explicitly rather than being left implicit.

B. **By workflow grouping** — W-3/W-4/W-5, W-6/W-7, W-8/W-9
   > **Impact**: Traceable straight back to `functional-design` and easy to verify. It groups W-9 (Dst's three restrictions) with W-8 (an exit-code gap) purely by adjacency, and separates W-9 from W-4/W-5 despite Dst's restrictions being the same class of forecast-safety rule as the lags.

C. **By module** — `iri.py`, `gim.py`, `spaceweather.py`
   > **Impact**: Matches `src/external/`'s own structure and is the easiest to check against the tree — except that none of the three exists. It is a module listing rather than a decomposition, rejected on that ground by all three siblings, and it would split the import allowlist across all three boxes since the allowlist is a property of the graph, not of a module.

D. **By enforcement mechanism** — static scan, property test, gate
   > **Impact**: Mirrors `governance-guards`' criterion, which has the virtue of a working precedent. It would split the F10.7 trailing-mean property test from the carry-forward bound and the lag assertions, which are one rule about time enforced three ways — the same conflation `governance-guards` itself rejected when it declined to group a static scan with a run-time assertion.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — this unit is a set of boundaries, and the useful question
> about a boundary is what is on the other side of it. It also makes the blast radii legible
> and different from one another: a containment failure invalidates the confirmatory result, a
> forecast-safety failure is *"invisible in validation, fatal on discovery"* in the artifact's
> own words, and a benchmark-integrity failure changes what the thesis reports a comparison
> against. D's precedent is real, and it would break the one rule this unit most needs kept
> whole.

[Answer]: A

---

## Consolidated Summary Confirmation

All four answered with the recommended option, on the owner's instruction of 2026-09-02
("apply your recommendations"). Recorded as a **one-time instruction for this unit's question
set**, not a standing autonomy grant.

**Q1 — the vacuous import-allowlist pass**: **A. Skip with a stated reason in the ordinary
suite; the §18.3 preflight treats a skipped critical check as UNMET.** The run record says
`skipped`, never `passed`, while `src/external/iri.py` and `gim.py` are absent. **This stage
fixes a §18.3 reading** — *"no failing critical test"* is read as *"no critical check
unmet"* — and that reading is stated in the design rather than assumed, because it is the
load-bearing half of the option. Risk carried: a normalised skip is how a control quietly
stops being one; the preflight coupling is what stops that.

**Q2 — `ImportBoundaryError` and `FeatureAvailabilityError`**: **A. Declared in
`src/data/config.py`**, deriving from `IntegrityError`, riding R-01's *"any future
integrity-related exception"* clause; neither claimed as an enumeration entry. Consistent
with the owner's `inventory-and-registry` Q2 = A ruling and with the 2026-08-28 ruling that
moved `PartitionError`'s declaration site into `config.py`. **The `src/data/exceptions.py`
§12 amendment is not taken** and is named as the better end state to raise on its own merits,
with all existing declarations migrating together.

**Q3 — the residual surviving both IRI limbs**: **A. Flip the provenance default — absent
provenance FAILS.** The feature-matrix assertion admits a column only if its provenance is
**present and not IRI**, rather than rejecting only columns whose provenance says IRI. This
closes the **stripping** act; **it does not close the residual** — a value renamed and
recomputed from scratch still survives, and no artifact may describe NFR-IRI-01 as fully
enforced. **Option B (a numeric fingerprint against the IRI benchmark) is declined
explicitly**, because the data is supposed to resemble the benchmark and the threshold would
be a number this project has no basis to set. Cost accepted: every feature-matrix column now
needs a provenance value, which **adds to the `features-and-splits` half of the two-half
contract that is already owed rather than agreed**.

**Q4 — the component boundary criterion**: **A. What the component keeps out.** Three
components — **E-1 containment** (IRI/GIM out of training and inference), **E-2 forecast
safety** (the future out of a forecast origin), **E-3 benchmark and comparator integrity**
(an unvalidated benchmark or an unaudited-independence comparator out of the comparison).
W-8's exit-code work and W-10's build boundary cross all three and are placed explicitly.

**Unchanged by these answers.** No scientific value is decided. The `iricore` pin with its
switch set, topside option and 2000 km ceiling, and the CODE final GIM product version, both
stay `TBD — freeze gate`. IRI generation stays blocked on R-59's validation. The
`gim_network_overlap_flag` audit has not run and no independence claim precedes it.
**`tests/test_iri_denial.py` does not exist**, and nothing here claims otherwise. No module is
written by this stage.

- Looks correct
- Request changes

[Answer]: Looks correct
