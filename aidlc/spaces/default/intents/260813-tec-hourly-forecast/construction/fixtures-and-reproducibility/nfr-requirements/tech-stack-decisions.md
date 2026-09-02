# Tech Stack Decisions — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12) · **Kind** `library` · **Stage** `nfr-requirements`

> ## ⚠ NO NEW DEPENDENCY, AND EVERY NUMBER IS A PLACEHOLDER
>
> The governed stack is fixed by **TE §8** and transcribed at
> `../../foundation/nfr-requirements/tech-stack-decisions.md`. This unit adds **none**.
>
> **Neither fixture has ever run.** Every runtime, tolerance, row-count range and storage figure
> is **measured on the fixtures and frozen** (TE §15.1) — **none is measured**, so **none is
> stated**. **The two freeze acts are the project owner's under Q-31.**
>
> **This unit cannot execute at all today**: **`configs/` does not exist**, so there are no four
> configuration hashes to lock; **no Python interpreter exists** in this environment; and
> **`foundation`'s TensorFlow pin is `TBD — freeze gate`**, so the pinned environment TA-03
> measures cannot be installed.
>
> **G-09** is signed (D-31) with preconditions UNMET; stage 3.1 remains **FAIL**.

## Sources

- `../../foundation/nfr-requirements/tech-stack-decisions.md` — the governed stack, the `TBD — freeze gate` TensorFlow pin, and the platform rules. Referenced, not restated.
- `../functional-design/business-rules.md` — **R-133** (one schema, one validating loader, the only read path), **R-134**, **R-138** (the §13.2 sequence on CPU, no GPU visible), **R-139** (the comparison ledger), **R-140**, **R-141**, **R-142**.
- `../functional-design/business-logic-model.md` — **W-1** (the manifest schema and the loader), **W-6** (`test_clean_run.py`), **W-7** (the receipts and the exported check), **W-8** (the in-session gate), **W-9** (the three generated evidence artifacts).
- `../../../../../../../../PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — **§8.1** (`pyyaml` required for configuration; `pytest` required; `pandas`, `pyarrow`, stdlib `hashlib` required), **§9.1–9.2**, **§12** (`tests/fixtures/<fixture_id>/fixture_manifest.yaml`), **§13.1**, **§13.2**, **§13.7**, **§15.1–15.3**, **§18.2**.
- `nfr-requirements-questions.md` — Q1 = A, Q2 = A, and the receipted Consolidated Summary Confirmation.

---

## TS-X-01 — The manifest is YAML, validated by one loader, and hash-checked there

**Decision (R-133, W-1, TE §12/§15.2).** Fixture assertion data lives in
**`tests/fixtures/<fixture_id>/fixture_manifest.yaml`** — identity, input hashes, expected
schema, row-count ranges, support/missingness limits, timestamp tolerances, required outputs,
expected CPU runtime range measured before freeze, and permitted floating-point tolerances —
**never hardcoded inside test bodies**. Parsed with **`pyyaml`** (TE §8.1, required).

**Decision (Q2 = A).** The **manifest hash check lives in the same loader**. R-133 already makes
the loader **the only read path**, so the hash comparison costs one operation at a place every
read passes, and needs **no new dependency**: stdlib **`hashlib`**, which TE §8.1 already
requires.

**Where the reference hash lives is owed at 3.5**, with one constraint that is not negotiable:
**a hash recorded inside the file it protects protects nothing**. It must sit outside the
manifest — a sibling file, the repository's own record, or the freeze act's D-number entry — and
choosing among those is the owner's, since **Q-31 makes the freeze an owner act**.

> **⚠ The chokepoint is not enforced.** R-133 states the loader is the only read path;
> **nothing enforces that today**, and a test calling **`yaml.safe_load`** directly bypasses
> **both** the schema validation **and** the hash check. The mechanism is therefore **as strong
> as an unenforced convention** — it closes every read the design intends and nothing that goes
> around it. **The check that would catch that is R-132's convention, and it is unwritten.**
> *(Stated in this decision body 2026-09-01 on adversarial finding 2, Major — it had appeared
> in neither this artifact nor `security-requirements.md`'s rule body.)*

**No schema-validation package is added.** `pandera`, `jsonschema` or an equivalent would be a
**new dependency**, a §10.1 reuse-register entry, and a version to pin on two platforms — inside
the unit whose entire purpose is to make the environment reproducible. **The validation is a
fixed field set against a fixed schema**, which stdlib and `pyyaml` handle.

## TS-X-02 — The comparison ledger needs exactness, and that constrains the format

**Decision (R-139, TE §13.7).** Comparisons are **`exact`** for §13.7's five classes — **hashes,
schemas, partition membership, IDs, deterministic CPU transformations** — using **equality, not
tolerance**; and **`toleranced`** otherwise against the manifest's declared floating-point
tolerance **with its units**.

**A format consequence, stated because it caused a real failure.** **Byte-identity is asserted
where §13.7 demands it**, and byte-identity is a property of **how an artifact is written**, not
only of its contents. **D-18's re-merge hashed differently from an artifact holding the identical
record set** because **output order followed directory traversal**; only a **sort on the dedup
key** made two consecutive runs agree (`DATA-17`). So:

- **every artifact whose hash is compared `exact` must be written in a deterministic order**,
  with the ordering key **declared**, not incidental;
- **`pyarrow`/Parquet writes must not depend on dictionary iteration order or file-system
  traversal order** for row or column sequence.

**This is a stack decision because a library default can break it.** A writer that parallelises
or preserves insertion order will produce hash-unstable artifacts that are semantically
identical — and the manifest would then record an expectation no re-run reproduces.

**No diffing or comparison package is added.** `pandas` compares frames; `hashlib` compares
bytes.

## TS-X-03 — The clean run drives real scripts on CPU, with no GPU visible

**Decision (R-138, W-6, TE §13.2, §9.2).** `tests/test_clean_run.py` executes the **amended
§13.2 sequence verbatim** — beginning
`python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day`, then
`--fixture scientific_1month`, then the **seven Phase 1 stage-script invocations**, with **Phase
2 deferred to G-P2** — **on CPU**.

**"No GPU visible" is an environment decision, not an assertion.** The clean run executes with
the GPU **made invisible to the process**, so a path that silently required an accelerator
**fails** rather than succeeding on hardware the CPU-completeness rule says no result may depend
on (TC-01, TE §9.2). Asserting "we used CPU" while a GPU was present proves nothing.

**The scripts are driven as scripts.** They take `--config configs/` and, where phase-aware,
`--phase 1|2` — invoked as the §13.2 sequence writes them, **not** imported and called, because
the thing under test is the **documented sequence**, not a set of functions.

**`pytest` is the harness** (TE §8.1, required). **No test-orchestration, snapshot-testing or
subprocess-management package is added** — stdlib handles process invocation.

## TS-X-04 — The three evidence artifacts are generated, and refuse

**Decision (R-142, W-9).** The **matrix**, the **bounded acceptance table** and the
**`environment_and_cpu_preflight_report`** are **generated paths that refuse** — never
hand-maintained documents. The acceptance table is **bounded to 13 rows by construction**
(WS-01 plus WS-09…WS-20), and a **deferral is a raise**.

**Why generated rather than written.** A hand-maintained acceptance table **cannot refuse**. The
bound and the deferral raise only exist if the table is a code path — the same reasoning
`regimes-diagnostics-reporting` applies to the primary results table.

**One distinction this unit must not blur.** This unit's `environment_and_cpu_preflight_report`
evidences **G-07 Reproducibility**. **`foundation`'s `aws_ai_dlc_preflight_report` evidences
G-09** and **does not exist**. They are different artifacts for different gates, and the names
are close enough to conflate.

## TS-X-05 — Platform posture, and the gate this unit owns

Unchanged from `foundation`: **exactly two platforms**; **CPU is a complete execution path**;
artifacts move between platforms **with a SHA-256 manifest** and the transfer is recorded.

**This unit owns the in-session gate** (R-141, § SEC-X-04) — the mechanism that makes the
platform rule enforceable rather than aspirational. **Q1 = A binds gate reuse to the run's own
§13.1 lock**, so the comparison the gate performs is **hash and identity equality**, which is
stdlib work.

**A dependency the gate cannot avoid.** It reads **`ConfigSnapshot.platform`, resolved by
`foundation`'s `resolve_platform_roots`** — **never asserted by the caller**. That detection does
not exist, so **the gate is specified and unrunnable today**, and its correctness rests on a
sibling's detection being right.

**The measured total runtime is recorded, not checked.** **No session or wall-clock ceiling
exists in any authority** — the only quota is the ~30 Kaggle **GPU** hours per week at Vision
§4.4, which *"are available but not required"* and **does not bind the CPU path**. **No ceiling
is invented here.**

---

## Requirement coverage

| Requirement | Section here | Acceptance row | Status |
|---|---|---|---|
| FR-WS-1 | TS-X-01, TS-X-02 | WS-20, TA-09 (primary) | `Pending` |
| FR-WS-4 | TS-X-04 | WS-01, WS-09…WS-20 — 13 rows | `Pending` |
| FR-WS-5 | TS-X-03 | WS-20, TA-17 (primary) | `Pending` |
| FR-WS-6 | TS-X-05 | TA-03, TA-26 (supporting) | `Pending` |
| **NFR-REP-01** | TS-X-02, TS-X-03 | WS-20, TA-17 (primary) | `Pending` |
| **REQ-NFR-A3** | TS-X-05 | TA-03 (supporting) | `Pending` |
| NFR-PHASE-01 | TS-X-03 | TA-27 — row owned by `governance-guards` | `Pending` |

**Derived and printed**: 5 decision sections (TS-X-01…TS-X-05); **7** coverage rows — **seven
fewer** than `security-requirements.md`'s **fourteen**, because FR-WS-2, FR-WS-3, FR-WS-7,
FR-P1-03-5, REQ-ENG-4, REQ-ENG-5 and REQ-ENG-10 raise **no technology choice** in this unit;
**0** rows claimed satisfied; **0** new dependencies; **0** values left `TBD — freeze gate` by
this unit — **every measured figure is owed as a fixture measurement**, and `foundation`'s
TensorFlow pin is the one unfrozen value this unit **waits on**.

## Assumptions & Open Questions

- **[Q2 / TS-X-01]** **Where the reference manifest hash lives is owed at 3.5.** The one fixed constraint: **it must not live inside the manifest it protects**. The choice is the owner's, since Q-31 makes the freeze an owner act.
- **[TS-X-02]** **Deterministic write order is a precondition of `exact` comparison**, and **D-18 shows it fails by default**. The ordering key must be **declared**, not incidental — and this constrains every artifact whose hash is compared, not only this unit's.
- **[assumption]** `pyarrow` can be made to write deterministically for the artifacts compared `exact`. **Unverified** — nothing has been written or hashed. If it cannot, the affected artifacts' comparison class must change, which is a **manifest freeze decision**, not an implementation choice.
- **[assumption]** Making the GPU invisible to the clean-run process is achievable on both platforms. **Unverified on Kaggle**, where the session's device visibility is the platform's to grant.
- **[TS-X-05]** The gate reads a detection that **does not exist** (`foundation`'s `resolve_platform_roots`), so it is **specified and unrunnable today**, and its correctness **rests on a sibling's detection being right**.
- **Carried — `foundation`'s TensorFlow pin is `TBD — freeze gate`**, so **the pinned environment TA-03 measures cannot be installed**, and **neither fixture can run until it is frozen**. This unit is downstream of that freeze in the most literal sense.
- **Carried, and the owner's — the two manifest freeze acts under Q-31.**
- **None** of the above decides a scientific value, fills a `TBD — freeze gate` field, or claims a gate, acceptance row, install or test as discharged.
