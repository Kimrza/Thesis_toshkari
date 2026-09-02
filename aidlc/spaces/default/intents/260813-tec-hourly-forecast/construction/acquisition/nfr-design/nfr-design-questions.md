# NFR Design — Questions — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-design`

Two artifacts only — `security-design.md` and `logical-components.md`. `produces_kinds`
maps the other three to `[service]` / `[service, ui]`, and this unit is `library`.

**Nothing below decides a scientific value.** TE §18.2's absolute rule stands.

> ## ⚠ UPSTREAM STATUS CLAIMS CHECKED AGAINST THE WORKSPACE, 2026-09-01
>
> `nfr-requirements` was written when much less existed. Verified before drafting these
> questions, per the owner's 2026-09-01 ruling that designs are written against **current
> state** while `nfr-requirements` itself stays unchanged:
>
> | Upstream claim | Actual state |
> |---|---|
> | SEC-A-04: *"BLK-07 is open… **neither accessor exists**"* | **Half stale.** The **read** side exists — `open_restricted` (`src/data/locked_test.py:147`) and `scripts/merge_coverage_year.py:98`'s `guarded()` helper, which routes through it. The **write** contract (R-33) still does **not** exist. |
> | SEC-A-04: the FULL-manifest test is blocked on the artifact | `evidence/locked_test_restricted/audit_evidence_2022-FULL/request_manifest.json` **exists**, alongside `sha256_manifest.json`, the three CSVs and `PROVENANCE_NOTICE.md`. |
> | SEC-A-03 limb 1: one declared redaction serializer | **Entirely unbuilt** — grep across `src/`, `scripts/` and `tests/` returns **no** `CredentialEgressError` and **no** redaction helper of any name. |
>
> **The redaction serializer being absent is the live gap in this unit**, and it is the one
> limb of SEC-A-03 that a sibling's gate cannot cover.

**What is already fixed upstream and is not re-asked.** Retrieval is **resumable and
hash-verified**, with **bounded retry and backoff**, and **a partial file is never
promoted** — the hash is computed **over the completed file**, after the completeness
check (SEC-A-01, Q1 = A). A re-run is **byte-identical or explicitly divergent**, recording
**both provider filenames including version suffixes and both hashes**, and **refusing to
overwrite** (SEC-A-02, Q2 = A). Credentials reach the provider client **from the
environment via `foundation`'s resolution**, never through a config, log, registry note or
notebook. Gaps are **explicit NaN at acquisition**, never interpolated or filled.

---

## Question 1

SEC-A-03 limb 1 requires **one declared redaction serializer** through which every value
this unit writes to a manifest, log or notebook output passes, refusing unredacted
credential-shaped values with `CredentialEgressError`. It **does not exist**, and the
requirement itself concedes that *"the definition of 'credential-shaped' is heuristic, and
that is accepted rather than hidden."*

A heuristic that is too narrow misses a token; too broad, and it fires on legitimate
values until someone widens the exception list until it misses a token. **How the
heuristic fails matters more than how it succeeds.**

What should the serializer do when it cannot decide?

A. **Fail closed on the two named carriers, heuristic elsewhere** — refuse **any** value matching a signed-request-URL or auth-header shape unconditionally, and apply the broader entropy/prefix heuristic to everything else as a **warning that blocks the write** but names what it matched
   > **Impact**: The two carriers SEC-A-03 names as realistic get an unconditional rule, not a guess, so the common case cannot be tuned away. The broader heuristic still blocks, so a novel token shape is caught by the general net. False positives on legitimate high-entropy values (a hash, a UUID) will occur and need an **allowlist that is itself reviewed** — the same trap `foundation` § SD-01 records for the secret scanner.

B. **Fail closed on everything the heuristic flags, no distinction** — one rule, one refusal
   > **Impact**: Simplest to reason about and to test. It treats a definite match and a maybe-match identically, which means the first false positive on a hash column pressures someone to weaken the single rule that also covers the definite cases.

C. **Warn and proceed**, recording what was flagged
   > **Impact**: Never blocks legitimate work. It converts SEC-A-03's "refuses unredacted credential-shaped values" into a log line, on the one chokepoint standing between a credential and a committed manifest — and this unit already writes thirteen committed manifests.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the asymmetry is the point. A signed URL and an auth
> header are **structurally identifiable**, so treating them as a heuristic result
> understates what the check knows; everything else genuinely is a guess, and a guess that
> blocks is still the right default when the artifact is committed and permanent. What A
> costs is honest: an allowlist, and the discipline that it is reviewed rather than grown.
> B's weakness is specific — a single rule covering both certain and uncertain cases is
> weakened by the pressure of its own false positives.

[Answer]: A

---

## Question 2

SEC-A-04 R-33 requires a restricted **write** to **log before it writes** — the write-side
counterpart of `governance-guards` R-25's durable-append-before-read. Upstream records it
as blocked on BLK-07; **the read side now exists** (`open_restricted`), and the write side
still does not.

`open_restricted` **refuses any path outside the restricted root** by contract, and returns
a path for the caller to read. It is a **read** chokepoint by construction.

How should the write contract relate to it?

A. **A sibling function in the same module, sharing the append-and-fsync helper** — `write_restricted` logs durably, then writes, reusing `_append_and_flush` and the same boundary derivation
   > **Impact**: One module owns the boundary, one helper owns durability, and the ordering rule is implemented once for both directions. It keeps `governance-guards`' module as the single place the restricted root is named — consistent with the one-door property and with the exempt list living there. It grows a `governance-guards`-owned module with an `acquisition` concern, so ownership of that file must be stated.
B. **A separate write path in this unit**, calling `governance-guards`' logging primitive but owning its own contract
   > **Impact**: Ownership matches the unit that does the writing, and `acquisition`'s contract can differ where writing genuinely differs from reading. Two modules then name the restricted root — which **widens the exempt list to eight** and weakens the one-door property that D-15 says *"does not weaken slightly; it ends."*

C. **Defer** — record the contract and build it when BLK-07's blocker clears
   > **Impact**: Nothing is designed on a foundation that may move. It also leaves the write side undesigned while the read side is built and in use, and this unit already writes to the restricted root today via `merge_coverage_year.py`.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the decisive argument is the exempt list. B adds an
> eighth holder of the restricted-root literal, and this project has already learned
> (DISC-1 at `governance-guards`) that every new holder is a real cost caught only because
> an assertion fires. Keeping both directions in one module keeps the door count at one and
> the durability implementation single. The ownership question A raises is real and should
> be stated in the design: the module is `governance-guards`', and `acquisition` is its
> caller, not its co-owner.

[Answer]: A

---

## Question 3

SEC-A-03 limb 2 requires **notebook outputs cleared as a precondition of commit** — the one
egress an in-process serializer cannot reach, because saved output cells are committed
artifacts. `notebooks/madrigal_phase1_coverage_audit.ipynb` exists today, and `team.md`
already commits this project to a pre-commit hook.

What should the hook do with a notebook carrying saved outputs?

A. **Refuse the commit** — a notebook with non-empty output cells fails the hook, and the author clears and re-commits
   > **Impact**: The artifact never enters history with outputs, which matters because a credential in a committed notebook needs a **history rewrite** to remove — and this repository tags its freeze gates. It will block legitimate commits where the author wanted outputs preserved for review, and there is no exception mechanism unless one is designed.

B. **Strip outputs automatically** on commit
   > **Impact**: Frictionless, and the author never has to remember. It **modifies what the author staged**, which means the working tree and the commit disagree — and a tool that silently rewrites content is a poor fit for a project whose whole discipline is that artifacts say what they are.

C. **Warn only**
   > **Impact**: No friction and no protection. It is the same posture as Q1 option C, on the egress path the design explicitly says a serializer cannot cover.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — refusing is the only option that keeps the guarantee,
> and the cost is one command for the author. B's silent rewrite is the wrong shape for
> this project specifically: `team.md` requires commits that change a governed artifact to
> cite a D-number, which presumes the author knows exactly what they are committing. If
> outputs genuinely need preserving for review, that is an exported artifact with its own
> provenance, not a committed notebook cell.

[Answer]: A

---

## Question 4

`logical-components.md` needs boundaries. This unit holds: **retrieval** (resumable,
backoff, completeness check), **hashing and manifest writing**, **provenance recording**
(including version suffixes), **the redaction serializer**, **restricted-root access**, and
**the notebook/script equivalence** TS-A-04 governs.

A. **On egress direction** — everything that **fetches** (retrieval, completeness, hashing) as one component; everything that **emits** (manifests, logs, provenance, redaction) as a second; **restricted-root access** as a third
   > **Impact**: Puts the boundary where this unit's actual security property sits — SEC-A-03 says *"the live risk in this unit is egress"*. The redaction serializer then sits inside the component whose whole job is emitting, which is where every value it must inspect already passes. It splits hashing (fetch side) from manifest writing (emit side), which are adjacent in the code but fail differently.
B. **On artifact lifecycle** — acquire, verify, publish
   > **Impact**: Reads naturally and maps to how someone would describe the work. "Verify" spans both a fetch-side completeness check and an emit-side hash comparison, so the component boundary would cut across the egress property rather than along it.

C. **One component** — the acquisition library
   > **Impact**: Matches how callers import it. Says nothing about egress, which is the one thing this unit's design is about.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — `foundation` split on write-integrity and
> `governance-guards` on enforcement timing, each choosing the axis its own failures run
> along. This unit's failures run along **egress**: a truncated fetch fails a run, a leaked
> credential in a manifest is permanent. A boundary on that axis puts the redaction
> chokepoint inside the component that emits, and makes the restricted-root path visibly
> separate from both.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. **Nothing below decides a
scientific value**, and nothing claims a gate, acceptance row, install or test as
discharged.

**How these answers were given.** The owner directed the recommended options as an
**explicit decision**, not as agent defaults.

**Written against the workspace, not against upstream's status claims** — per the owner's
2026-09-01 ruling, with `nfr-requirements` left unchanged. The three divergences are in
the box at the head of this file and are restated in `security-design.md`.

**Q1 = A — the redaction serializer fails closed on two named carriers, and blocks on the
rest.** A **signed request URL** and an **auth header** are refused **unconditionally** —
they are structurally identifiable, so treating them as a heuristic result understates what
the check knows. Everything else goes through the broader entropy/prefix heuristic, which
**blocks the write** and **names what it matched**. Refusal raises `CredentialEgressError`
at integrity tier: the run terminates and an `aborted` row is written through the
`IntegrityError` catch.

**The cost is stated, not discovered later.** False positives on legitimate high-entropy
values — a hash, a UUID — **will** occur, and they need an **allowlist that is itself
reviewed**, never grown to silence a failure. This is the same trap `foundation` § SD-01
records for the secret scanner, and it is the same answer: the allowlist is a review
surface.

> **⚠ None of this exists.** Grep across `src/`, `scripts/` and `tests/` returns **no**
> `CredentialEgressError` and **no** redaction helper of any name. **This is the live gap
> in this unit** — and it is the one limb of SEC-A-03 that **no sibling's gate can cover**,
> because TA-22's scan is detection *after* the artifact exists and is `foundation`'s.

**Q2 = A — the restricted-write contract is a sibling function in `governance-guards`'
module**, sharing `_append_and_flush` and the same boundary derivation. `write_restricted`
**logs durably, then writes** — R-33's write-side counterpart to R-25's
durable-append-before-read.

**The decisive argument is the exempt list.** A separate write path in this unit would make
a **second module name the restricted-root literal**, widening the exempt list to **eight**.
`governance-guards` DISC-1 has just shown what each new holder costs: the seventh was
caught only because a membership assertion fired. D-15's boundary *"does not weaken
slightly; it ends."* One module, one door, one durability implementation.

> **Ownership is stated rather than blurred.** The module is **`governance-guards`'**;
> `acquisition` is its **caller, not its co-owner**. A function added there for this unit's
> concern does not transfer ownership of the boundary.

**Q3 = A — a notebook with saved output cells fails the pre-commit hook.** The author clears
and re-commits. This is the egress an in-process serializer **cannot** reach, because saved
output cells are committed artifacts.

**Why refusing rather than auto-stripping.** A credential in committed history needs a
**history rewrite** to remove, and this repository **tags its freeze gates** — the rewrite
would rewrite tagged commits. Auto-stripping is the wrong shape for this project
specifically: `team.md` requires a commit changing a governed artifact to **cite a
D-number**, which presumes the author knows exactly what they are committing. A tool that
silently rewrites staged content defeats that. Where outputs genuinely need preserving for
review, that is an **exported artifact with its own provenance**, not a committed cell.

**Q4 = A — components split on egress direction.** Everything that **fetches** (retrieval,
backoff, completeness, hashing) as one; everything that **emits** (manifests, logs,
provenance, the redaction serializer) as a second; **restricted-root access** as a third.

SEC-A-03 states it plainly: *"the live risk in this unit is egress."* The boundary follows
that axis, which puts the redaction chokepoint **inside the component whose whole job is
emitting** — where every value it must inspect already passes. `foundation` split on
write-integrity and `governance-guards` on enforcement timing; each unit uses the axis its
own failures run along, rather than a shared template.

**Carried, not re-decided.** Retrieval is **resumable and hash-verified** with **bounded
retry and backoff**; **a partial file is never promoted**, and **the hash is computed over
the completed file** after the completeness check — a truncated file hashed at truncation
**verifies against itself forever**, which is the one acquisition failure that survives the
project's entire verification chain. A re-run is **byte-identical or explicitly divergent**,
recording **both provider filenames including version suffixes and both hashes**, and
**refusing to overwrite**. Provider terms bound the rate. Credentials reach the client
**from the environment via `foundation`'s resolution** only. Gaps are **explicit NaN at
acquisition**. Membership is derived from **record timestamps, never a directory name**.

**Status claims made. None.** **The redaction serializer, `write_restricted`, and the
pre-commit hook are all unbuilt.** The **DATA-07 provenance caveat stands**: the twelve
pre-TC-06 months are **unverifiable in principle** — no provider byte stream exists
anywhere in the workspace, and **2022-04, 2022-07 and 2022-12** hold no `raw_isprint_cache/`
at all. Re-acquisition must record **full provider filename including version suffix**,
retrieval date and SHA-256, surfacing any mismatch rather than accepting it silently.
**The NFR-SEC-01 / Madrigal-identity conflict is the supervisor's and no reading is
adopted.** `configs/`, `pyproject.toml` and `requirements.txt` are absent, so **TC-06's
scaffold precondition is unmet**. **G-09 is signed (D-31) with preconditions UNMET**;
**stage 3.1 remains FAIL**. The suite runs **off-pin** (Python 3.14.7 against the governed
3.11) and is **not governed evidence**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
