# Change record — `.dst_summary.json` custody relocation

**Record ID:** `CR-2026-08-28-DST-RELOC`
**Filed:** 2026-08-28
**Decision:** `evidence/DECISIONS.md` **D-30**
**Precedent:** `evidence/DECISIONS.md` **D-15** (locked-month custody relocation) and
`governance/CHANGE_RECORD_PROCEDURE.md`

---

## Vision §15.2's six fields

| # | Field | Content |
|---|---|---|
| 1 | **What changed** | `.dst_summary.json` moved from the repository root to `evidence/audit_ec1_2026-08-15/kyoto_dst/.dst_summary.json`. **Only the path changed.** No byte of the file's content was altered. |
| 2 | **Why** | The file carries December 2022 material (twelve month keys; the `"12"` entry holds `days_parsed: 31`, `hours: 744`, `min: -68`, `storm50: [7, 27]`, `storm30` with 15 days, `daily_min` with 31 entries). At the repository root it sat **outside** the `evidence/` scan root of `governance-guards` R-27 — the recursive December guard designed to catch exactly this class of artifact. The guard could not reach it. `governance-guards` identified relocation as the fix, expressly declined to perform it without a decision, and made R-26's driver-exclusion class 4 **conditional** on the move so no unearned closure was claimed. |
| 3 | **Superseded text, quoted** | `governance-guards/functional-design/business-rules.md` R-26 class 4 row: *"`.dst_summary.json` — **class 4 applies only once Recommendation 44(b)'s relocation has happened**; see R-27"*. And its Open item: *"the move to `evidence/audit_ec1_2026-08-15/kyoto_dst/` owes a **D-number and a change record** on the D-15 precedent, and neither exists. **This stage does not perform the move and claims no closure from it.**"* Both are preserved in place, struck through and annotated rather than deleted. |
| 4 | **Authority** | The project decision owner, 2026-08-28, under the recorded student/supervisor authority equivalence (`evidence/DECISIONS.md` D-1 addendum), ruling on governance report `GOV-2026-08-28-FD-01` Recommendation 44(b), board option 2. **No supervisor signature artifact exists and none is claimed.** |
| 5 | **Evidence** | SHA-256 computed before and after the move and compared for equality: `410927a4ff620b6f7597b18e07746f74233cf5aa87bc84d6f5b0ec25b3e9c064`, **5,653 bytes**, identical. The repository-root path no longer exists (verified). Locked-month access-log **row 12** in `evidence/experiment_registry.md`, **written BEFORE the read**, records the operation, its bytes-only scope, and its authorisation. |
| 6 | **Consequences** | `governance-guards` R-26 driver-exclusion **class 4 becomes unconditional**; the corresponding OPEN item closes in all three of that unit's artifacts. The file is now inside R-27's scan root without the scan root being widened. |

---

## Why relocation rather than widening the scan root

Board option 1 was to widen R-27's scan root to the repository root. `governance-guards`
rejected it, and this record adopts that reasoning: a root-wide scan pulls every unrelated
file at the repository top level into the guard's reach and makes its exclusion list
unbounded — trading a known, single gap for an open-ended one. Moving one file into the
tree the guard already walks is the narrower act, and it places the derived Dst summary
beside the twelve `dst_provisional_YYYYMM.html` captures it derives from, all twelve
verified present.

## What this change does NOT do

- **It is not a December read.** The file was opened as bytes only, for hashing. No month
  key was parsed, no day count, storm list or `daily_min` value inspected, no statistic
  computed — the same scope and method as access-log rows 6, 7 and 11 and as D-15's
  relocation. The access row was written first, as FR-P1-02-3 requires.
- **It changes no scientific value**, reclassifies nothing, and approves no new input. Dst
  remains diagnostic/hindcast-only and never a confirmatory ML feature
  (`project.md` § Mandated; TC-11). D-11's bar on provisional Dst becoming a G-05 regime
  count is unaffected.
- **It does not make the file a locked-test access.** Its existing classification stands
  and is reasoned at `evidence/experiment_registry.md:119–123`: Dst is a public driver
  series, not a target value, and no December *target* record is touched. Neither the board
  nor the owning unit called the file a breach, and neither does this record.

---

## Propagation sweep — `CHANGE_RECORD_PROCEDURE.md` steps 1–5

**Step 1 — superseded literals named.** `"repository root"` and `"root"` used *of this
file's location*; `"conditional on the Recommendation 44(b) relocation"`; `"class 4 applies
only once"`; `"owes a D-number and a change record … neither exists"`; `"this stage does not
perform the move"`.

**Step 2 — swept.** Every `*.md`, `*.py` and `*.json` under the repository, excluding
`node_modules/`, `.git/`, `graphify-out/` caches and `.claude/worktrees/`.

**Step 3 — every site found, with disposition.**

| Site | Count | Disposition |
|---|---|---|
| `<record>/construction/governance-guards/.../business-rules.md` | 8 | **Edited in-stage.** Class-4 row annotated unconditional; the live-instance and fix paragraphs annotated as describing the pre-move state with the reasoning preserved; the OPEN item struck through and closed with the executed evidence. |
| `<record>/construction/governance-guards/.../business-logic-model.md` | 8 | **Edited in-stage.** Same treatment. |
| `<record>/construction/governance-guards/.../domain-entities.md` | 4 | **Edited in-stage.** Same treatment. |
| `<record>/construction/regimes-diagnostics-reporting/.../*` | 12 | **Correct as-is.** References are to the file by name as a Dst-summary artifact, never to its path or its location relative to a scan root. |
| `<record>/inception/requirements-analysis/requirements.md` | 5 | **Not edited — completed-stage artifact.** References are by name, not by path; no statement about location is made, so nothing there is falsified. Recorded here so the check is visible rather than assumed. |
| `evidence/DECISIONS.md` | 7 (+D-30's own) | **Correct as-is.** Prior mentions are by name within frozen decision text; D-30 itself carries the new path. |
| `evidence/experiment_registry.md` | 2 (+row 12) | **Correct as-is**, plus row 12 added. The `:119–123` classification passage is by name and remains accurate. |
| `governance/reviews/GOV-2026-08-28-FD-01.md`, `GOV-2026-08-20-RA-01.md` | 6 | **Correct as-is — governance reports are historical records** of what was true when written. |
| `governance/CHANGE_RECORD_2026-08-21_RA_audit.md`, `CHANGE_RECORD_2026-08-21_freezes.md`, `COUNTERSIGNATURE_REQUEST_2026-08-21.md` | 4 | **Correct as-is** — historical records. |
| `governance/reviews/GOV-2026-08-28-FD-01-REMEDIATION-STATUS.md` | 1 | **Correct as-is** — a dated resume note; its "owes a D-number and a change record" line was true when written and this record is what discharges it. |
| `graphify-out/**` | 15 | **Not edited — generated cache.** Regenerated by `graphify update .`, never hand-maintained. |

**Step 4 — arithmetic checked.** This record carries one change and states four figures,
each derived and printed before assertion: SHA-256 `410927a4…c064`; **5,653** bytes;
**12** month keys; and R-26's driver-exclusion classes now **4**, all unconditional. The
before-and-after hashes are equal, which is the whole of the byte-identity claim.

**Step 5 — re-derived, not decremented.** The class count was re-derived by reading R-26's
enumeration after the edit rather than by adjusting the prior number.

---

## Residual, stated rather than left silent

`.dst_summary.json` is a **derived** driver summary whose own §13.1 environment capture was
never taken. It inherits the standing pre-git provenance limitation
`evidence/experiment_registry.md` § Acquisition runs records for every artifact of that era
(`code_commit: unavailable-pre-git`, environment not captured). **This relocation closes a
reachability gap and asserts nothing about that provenance.** Whether the artifact should
exist in its present form, and under whose provenance record, is not decided here.
