# NFR Design Questions — `fixtures-and-reproducibility`

**Unit** `fixtures-and-reproducibility` (Bolt 12) · **Kind** `library` · **Stage** `nfr-design`

Construction-stage questions are exceptional. Every measured figure stays a placeholder
(TE §15.1, neither fixture has run) and the two freeze acts stay the owner's under Q-31 —
nothing below touches either. Two gaps `nfr-requirements` raised and did not resolve are
put here: one it explicitly routed to the owner (the reference-hash location), one it left
as a raised assumption (receipt validity across sessions). Per `produces_kinds`, this
`library` unit gets `security-design.md` and `logical-components.md`.

## Question 1

TS-X-01 fixes the constraint — **a hash recorded inside the file it protects protects
nothing** — and routes the choice of where the frozen manifest's reference hash lives to
the owner, naming three candidates. Since the freeze is an owner act (Q-31), your choice
here is that ruling. Where does the reference hash live?

A) A sibling file beside each manifest (`tests/fixtures/<fixture_id>/fixture_manifest.sha256`),
   written only by the freeze act, read only by the validating loader.
   > **Impact**: Simplest read path (loader reads two adjacent files), diffable, and the freeze act's two-step friction is preserved — editing the manifest without re-freezing breaks the load immediately. Weakness: both files sit in the same directory under the same permissions, so an attacker-with-intent edits both; the design's threat is the author's own convenience edit, which this still catches (two deliberate edits ≠ one reasonable fix).

B) The freeze act's D-number entry in `evidence/DECISIONS.md` carries the hash; the loader
   reads it from there.
   > **Impact**: Strongest provenance — the hash lives inside the human-signed decision record, so re-freezing without a new D-number is structurally visible. Cost: the loader now parses a prose evidence file at every test run, coupling test apparatus to a governance document's format; a reformat of DECISIONS.md breaks fixture loading.

C) Both — the sibling file is what the loader checks (mechanical path), and the freeze
   act's D-number entry also records the hash (governance record). The loader checks the
   sibling only; agreement between the two is asserted by one test, not by the loader.
   > **Impact**: A's clean mechanical path plus B's provenance, at the cost of one more representation of the same fact to keep in agreement — mitigated by making the agreement itself a tested assertion rather than a convention. Two writes per freeze act, both already inside the owner's deliberate two-step.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option C — the mechanical check stays cheap and format-stable (A's property), the hash still lands in the signed decision record where this project keeps its scientific provenance (B's property), and the known cost — a second representation — is closed by a test asserting agreement, which is this project's negative-control idiom. A alone leaves the hash outside the governance record; B alone couples the loader to prose.

[Answer]: C

## Question 2

`nfr-requirements` raises, unresolved: fixture-pass receipts must survive the session that
wrote them (Kaggle durability unmeasured), and the two-receipt check for any full-year job
depends on earlier-session receipts still being there. Separately, SEC-X-04's Q1 = A
already binds in-session **gate** reuse to §13.1 lock identity. What makes a fixture-pass
receipt valid for the two-receipt check?

A) Lock-bound validity, same discriminator as the gate: each receipt records the §13.1
   environment-lock items in force when its fixture passed, and the two-receipt check
   accepts a receipt only if its recorded lock matches the full-year job's own. A receipt
   from a changed environment is stale regardless of where it survived; a receipt from an
   unchanged environment is valid regardless of session age.
   > **Impact**: One staleness rule for gate and receipts (same mechanism, already designed), and the durability question becomes self-answering — a receipt that failed to survive simply fails the check and the fixtures re-run, fail-closed. Cost: fixtures re-run whenever the lock changes (a config edit invalidates receipts), which is correct by the same argument that invalidates the gate, but makes fixture runs more frequent. Limit inherited from the gate: invisible to changes the §13.1 items do not cover.

B) Same-session only — receipts are valid only within the session that produced them; every
   full-year job re-runs both fixtures first.
   > **Impact**: Simplest and strictest; durability is moot. But it deletes the reuse the ordering contract permits (R-140's receipts exist precisely so passing fixtures once per environment suffices), and on local hardware it makes every full-year job pay two fixture runs even when nothing changed.

C) Trust persisted receipts — receipts live in the versioned artifact store under the
   SHA-256 transfer manifest and are trusted wherever found.
   > **Impact**: Cheapest reuse, but a receipt from a stale environment (config edited since) passes the check — exactly the invalidation the gate's lock-binding exists to catch, reintroduced one artifact over.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it reuses the staleness discriminator the design already fixed for the gate (changed environment, not elapsed time or surviving bytes), turns the unmeasured-durability assumption from a risk into a non-issue, and keeps R-140's reuse where it is legitimate. B over-pays; C reopens the hole the gate closed.

[Answer]: A

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
