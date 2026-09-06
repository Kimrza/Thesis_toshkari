# NFR Design Questions — `evaluation-and-comparison`

**Unit** `evaluation-and-comparison` (Bolt 9) · **Kind** `library` · **Stage** `nfr-design`

Construction-stage questions are exceptional, not routine. Two genuine gaps remain
that `nfr-requirements` raised and did not resolve; everything else this stage needs
is already fixed upstream (the mask contract R-106/R-107, the estimand contract R-108,
the G-06 path R-109, the honesty mechanics R-110, and the fail-closed refusals of
SEC-C-01…SEC-C-04). Per `produces_kinds`, this `library` unit gets `security-design.md`
and `logical-components.md` only.

## Question 1

SEC-C-01's freeze-precedes-access refusal compares a mask-registration timestamp
against a locked-test access timestamp. `nfr-requirements` raised (and did not
resolve) that the two may be written by **different hosts** — on Kaggle the mask
registry and the access log are not guaranteed one clock domain, and no skew bound
is stated anywhere. How should the ordering check be designed so the refusal means
what it says?

A) Causal containment instead of clock comparison — the access-log entry records,
   at access time, the identity of the frozen mask bundle it found (the `mask_id`s
   and the registry's content hash). Ordering is then proven by containment: the
   access record *contains* the registration evidence, so registration necessarily
   preceded access, on any clocks.
   > **Impact**: Removes the cross-clock comparison entirely — no skew bound needed, no same-host constraint. The access path gains one read (the registry state) and the access record gains two fields. The check becomes verifiable after the fact from the two artifacts alone. Cross-unit: the access log is `governance-guards`' (R-25); this unit can only state its half of the field contract, exactly as it already does for the hash receipt.

B) Same-host constraint — require that the mask registry and the access log be
   written by the same host in any governed run, and have the refusal assert host
   identity before trusting the timestamp comparison.
   > **Impact**: Keeps the timestamp design but adds an operational constraint on every governed run and a new failure mode (host-identity mismatch) that is spurious when clocks are actually fine. On Kaggle, "same host" is satisfiable within one session but unverifiable across sessions — the constraint narrows where the check may run rather than fixing the comparison.

C) Keep two timestamps and declare a skew bound — pick a bound (e.g. 60 s), record
   it in the design, and have the refusal require `registration + bound < access`.
   > **Impact**: Smallest change, but the bound is a new constant with no measured basis (Kaggle's clock behaviour is unmeasured — that is the raised problem), and a value chosen by convenience sits uncomfortably close to the §18.2 posture even though it is not a scientific value. A too-small bound gives false refusals at the one event that can never be re-run (G-06).

D) Defer the mechanism wholly to code-generation (3.5) — this stage records only
   that the ordering must be machine-enforced, and 3.5 chooses how.
   > **Impact**: Keeps this stage small, but `nfr-requirements` already deferred "where the timestamp is read from" to 3.5; deferring the *mechanism* too leaves 3.5 choosing a security design without a design stage behind it, which is what this stage exists to prevent.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it dissolves the raised clock-domain problem instead of bounding it: containment proves order on any clocks, needs no invented constant, and fails closed exactly like the unit's other refusals. The cost is two fields on the access record, whose owning unit (`governance-guards`) gets the obligation stated as a half-contract — the same pattern this unit already uses twice.

[Answer]: A

## Question 2

`logical-components.md` must map where the refusal logic lives. This unit enforces
five distinguishable refusals (stamp/`LeakageError`, partition/`PartitionError`,
mask/`FairnessError`, inverse/`InverseTransformError`, receipt-and-ordering/
`LockedTestError`). Where should they live inside `src/evaluation`?

A) One guard module — a single `src/evaluation/guards.py` owns all five checks;
   every entry point (mask construction, estimand pipeline, G-06 path) calls it.
   > **Impact**: One failure domain, one place to test, and the negative controls all target one module. Risk: an entry point that forgets to call the guard fails open — the guard existing does not prove it is invoked.

B) Checks inline at each entry point — every workflow (W-1, W-2, W-3, W-5) carries
   its own refusal code where it bites.
   > **Impact**: No forget-to-call risk at the workflow level, but five copies of overlapping logic drift independently — exactly the mechanism behind the R-105-vs-R-92 exception mismatch the governance board caught. Blast radius of a defect is one workflow, but the same defect must be fixed five times.

C) Guard module plus a wired-in negative control — checks live in one guard module
   (as A), and the test plan adds one control per entry point proving an unguarded
   call path fails: a stamp-less/receipt-less input pushed through each public
   entry point must raise. The control catches the forget-to-call failure A leaves open.
   > **Impact**: A's single failure domain and testability, with A's fail-open risk closed by construction — matching the project's affirmed practice that every hard rule gets a test proving the violation is caught. Cost: one additional negative control per public entry point in the (already specified, unwritten) test plan.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — it is A hardened by the project's own negative-control methodology (WS-10's pattern: prove the denial fires, not just that it exists), and it directly addresses the drift failure mode B has already produced once in this unit's history.

[Answer]: C

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
