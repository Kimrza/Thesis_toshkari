# NFR Requirements — Questions — `acquisition`

**Unit** `acquisition` (Bolt 3) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** The credential-egress
mechanism (W-9 / R-39, Q8 = D — one declared redaction serializer refusing unredacted
credential-shaped values, plus notebook outputs cleared as a precondition of commit); the
identity-field agreement check at release (W-5, Q4 = C); the version-suffix mismatch
contract (R-34); `madrigalWeb_version` absent failing exactly as `"unknown"` fails (R-35);
gaps as NaN with the conservation invariant (R-37); the ICTP rejection and its
unreachability (R-43); membership from record timestamps, never a name (R-31).

**Carried, not decided here.** The NFR-SEC-01 / Madrigal-identity conflict is the
**supervisor's**, recorded at `foundation` § SEC-F-02 and `requirements.md` § Known defects
row 13 — **no reading is adopted**. **BLK-07 is open**; W-2's restricted-access contract
does not exist, which is why the FULL-manifest test is deferred against `RES-04`.

---

## Question 1

Nothing in this unit's `functional-design` states a **retrieval-resilience** requirement.
A grep of `business-rules.md` and `business-logic-model.md` for rate limiting, backoff,
retry, resumption or throttling returns **no rule and no workflow step**. The unit
retrieves provider files over HTTPS, on Kaggle, for twelve months of data across three
cells, and TE §8.1 permits `requests` only *"where provider terms permit"*.

A retrieval that fails halfway currently has no stated behaviour: whether it resumes,
restarts, or leaves a partial file that a later hash check catches.

What should `security-requirements.md` require?

A. Resumable, hash-verified retrieval with bounded retry and backoff, and a **partial file never promoted** — an interrupted retrieval leaves its target absent or explicitly marked incomplete, never a short file that looks whole
   > **Impact**: Closes the failure that would be hardest to detect later — a truncated file whose hash is recorded from the truncation and therefore verifies against itself forever. Adds retry and resume logic to a unit that currently has none, and every retry parameter becomes a value someone has to choose.

B. Fail-fast with no retry: any interrupted retrieval terminates the run and is re-run from the start
   > **Impact**: Simplest to reason about and to test, and it matches the project's integrity-tier posture — terminate on a violated expectation rather than continue. On a twelve-month Kaggle acquisition a single transient network error discards the whole run, which is how the existing thirteen runs came to have unreconstructible environment locks.

C. Leave it to stage 3.5 as an implementation concern
   > **Impact**: Avoids specifying ahead of the code. `project.md` § Way of Working records deferring a gating condition's inputs as leaving the condition unmeetable, and re-acquisition is the act that discharges the DATA-07 provenance caveat — so its resilience is not an implementation detail.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the truncated-file failure is silent, survives hashing, and would corrupt exactly the re-acquisition that exists to make provenance verifiable. The retry parameters are ordinary operational values, not scientific constants, so choosing them is not a TE §18.2 freeze-gate act. Option B's cost falls hardest on the twelve-month run this unit is for.

[Answer]: A

---

## Question 2

Provider version drift is **observed in this dataset**, not hypothetical: `g.002` versus
`g.003`. R-34 records a version-suffix mismatch at retrieval and refuses it at release.
`team.md` requires every re-acquired file to record its **full provider filename including
version suffix**, retrieval date and SHA-256, and states that a disagreement between
original and re-acquired bytes would be **uninterpretable** unless the original suffixes
were recorded — which for `2022-04`, `2022-07` and `2022-12` they were not.

What should the artifacts require of a **re-run** of the same retrieval?

A. Byte-identical or explicitly divergent: a re-run recomputes the SHA-256 and, on any difference, **records the divergence with both suffixes and both hashes and refuses to overwrite** — it never silently replaces the earlier bytes
   > **Impact**: Makes drift visible at the moment it happens, which is the only moment both versions are in hand. It means a legitimate provider re-issue also stops the run, so someone must adjudicate each divergence rather than the pipeline absorbing it.

B. Latest-wins: a re-run takes the provider's current file, records the new suffix and hash, and supersedes the old record
   > **Impact**: Keeps the dataset current with the provider's best version with no manual step. It destroys the comparison `team.md` says makes a disagreement interpretable, and it is a silent mutation of a governed input — the class NFR-AUD-01 forbids for registry rows.

C. Refuse re-run entirely once a month is released
   > **Impact**: Strongest immutability, consistent with a release directory never being overwritten. It forbids the `raw_isprint_cache/` re-acquisition that FU-1 = B already sequences and that DATA-07's caveat depends on.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is R-34's existing mismatch contract extended to the re-run case, and it preserves exactly the evidence `team.md` names as the precondition for interpreting a disagreement. Option B discards that evidence; option C blocks the re-acquisition the project has already sequenced.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes performance, scalability and reliability for a `library` unit.
Those categories are still assessed and the assessment is recorded in the security
artifact's scope note.

**Q1 = A — retrieval is resumable and hash-verified, and a partial file is never
promoted.** Bounded retry with backoff; an interrupted retrieval leaves its target absent
or explicitly marked incomplete, never a short file that looks whole. This is a **new
requirement**: the unit's `functional-design` states no retry, backoff, resumption or
throttling rule anywhere. The retry parameters are ordinary operational values, **not**
scientific constants, so choosing them is not a TE §18.2 freeze-gate act — but they are
named as owed at stage 3.5 rather than invented here.

**Q2 = A — a re-run is byte-identical or explicitly divergent.** The re-run recomputes the
SHA-256 and, on any difference, **records the divergence with both provider filenames
including version suffixes and both hashes, and refuses to overwrite**. It never silently
replaces earlier bytes. This extends R-34's existing mismatch contract to the re-run case
and preserves the evidence `team.md` names as the precondition for interpreting a
disagreement — the evidence that is **missing for 2022-04, 2022-07 and 2022-12**, whose
original suffixes were never recorded.

**Carried, not re-decided.** W-9 / R-39's credential-egress mechanism (Q8 = D — one
declared redaction serializer plus notebook outputs cleared before commit); W-5's
identity-field agreement at release (Q4 = C); R-35's absent-`madrigalWeb_version` rule;
R-37's NaN-at-acquisition and conservation invariant; R-31's membership from record
timestamps; R-43's ICTP rejection and unreachability.

**Not decided here, and no reading adopted.** The NFR-SEC-01 / Madrigal-identity conflict
is the **supervisor's** (`requirements.md` § Known defects row 13).

**Status claims made.** None. **BLK-07 is open**; W-2's restricted-access contract does not
exist, so the FULL-manifest test stays deferred against `RES-04`. The twelve pre-TC-06
months' provenance is **unverifiable in principle** — no provider byte stream exists
anywhere in the workspace, and 2022-04, 2022-07 and 2022-12 have no `raw_isprint_cache/`
at all (DATA-07). **FR-P1-01-5 and FR-P1-01-7 carry no acceptance row.** No Python
interpreter exists here, so every test is written-but-unexecuted or unwritten; TA-15,
TA-22, TA-32 and the §18.3 preflight are undischarged; G-09 is signed (D-31) with its
preconditions UNMET; stage 3.1 remains FAIL.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
