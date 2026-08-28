# Change record — G-09 (Agent preflight) signed

**Record ID:** `CR-2026-08-28-G09-SIGNED`
**Filed:** 2026-08-28
**Decision:** `evidence/DECISIONS.md` **D-31**
**Gate:** G-09 Agent preflight — TE §1.2 gate table; TE §18.3

---

## Vision §15.2's six fields

| # | Field | Content |
|---|---|---|
| 1 | **What changed** | **G-09 Agent preflight moves from `Pending` / `Open` to `Signed`.** The gate that blocked creation of any module — every `src/` package, every `configs/` file, every `tests/` module designed in stage 3.1 — is open. |
| 2 | **Why** | The project decision owner exercised their authority to sign it, in session on 2026-08-28, at the `functional-design` remediation gate. The stated purpose is to unblock work that was deferred **solely** on the ground that G-09 barred editing a file — specifically TA-15's §13.3 field coverage and R-13's overwrite-refusal test, and the routing of two unlogged restricted reads through `open_restricted`. |
| 3 | **Superseded text, quoted** | TE §1.2 gate table: *"\| Agent preflight passed \| Student and supervisor \| Any affected component is coded \| **Pending — G-09** \|"*. And, repeated across all twelve stage-3.1 units in substantially this form (`fixtures-and-reproducibility` `business-rules.md`): *"**G-09 is not signed.** No rule here authorises creating `scripts/run_walking_skeleton.py`, either `fixture_manifest.yaml`, `tests/test_clean_run.py`, any receipt or evidence emitter, or a `tests/fixtures/` directory."* The authority-document row is **not edited** (see the sweep below); the unit artifacts are annotated in place. |
| 4 | **Authority** | The project decision owner, 2026-08-28, under the recorded student/supervisor authority equivalence (`evidence/DECISIONS.md` D-1 addendum). TE §1.2 assigns G-09 jointly to "Student and supervisor". **No independent supervisor signature artifact exists and none is claimed.** |
| 5 | **Evidence** | The owner's express instruction in the `functional-design` session, 2026-08-28, recorded as **D-31**. ⚠ **The evidence §18.3 itself requires does NOT exist** — see the precondition table below. This record does not represent the gate's evidentiary conditions as satisfied. |
| 6 | **Consequences** | Module creation is authorised. The two G-09-deferred defects become correctable. G-05, G-06, G-P1A, G-P2, G-P3A, G-P3C and G-07 are **unaffected**. TE §18.2's absolute rule and §18.3's standing stop-and-report obligation are **unchanged**. |

---

## The §18.3 preconditions, recorded as unmet

Derived by direct workspace and environment inspection on 2026-08-28, printed before
assertion. This table is the substance of the record: it makes the gap judgeable instead of
inferable.

| §18.3 requirement | State | How established |
|---|---|---|
| P0 decision-register entries for the affected component resolved | **Partially met.** The register is maintained (D-1…D-31); freeze-gate holes remain open **by design** — D-17's four support thresholds, D-25's requested §15.2 amendment, D-26's `UNRESOLVED` provenance, and the nine unfrozen scientific values stage 3.1 routed to G-04/G-05 rather than defaulting | `evidence/DECISIONS.md`; stage 3.1 gate-item lists |
| Automated preflight asserts no required field in the four configs is `TBD`, every declared source and hash exists, **and all gate tests pass** | **NOT MET — the assertion cannot run.** `configs/`, `src/` and `pyproject.toml` do not exist. There is no preflight and nothing for it to assert over | `ls` of the repository root, 2026-08-28 |
| Supervisor has signed the scientific hierarchy, IRI role, horizons, estimand, seeds, locked-test protocol | **Met only under the recorded equivalence.** No independent signature artifact exists for any of the six | D-1 addendum |
| **Criterion:** zero unresolved P0 fields **and no failing critical test** | **NOT VERIFIABLE.** The ten named critical tests cannot be executed — **no Python interpreter is installed**: `python.exe` resolves to a **zero-byte** Windows Store alias stub, there is no `HKLM`/`HKCU` `PythonCore` registry entry, and no interpreter exists on disk. "No failing critical test" is **unproven, not proven** — an absence of executions, not an absence of failures | Environment inspection 2026-08-28 |
| **Evidence artifact:** `aws_ai_dlc_preflight_report` | **DOES NOT EXIST.** Designed but unwritten; `foundation` owns FR-WS-7/TA-23 which discharge onto it | `GOV-2026-08-28-FD-01` Rec 9 |

**The honest characterisation.** This is the **owner opening the gate by authority**, not a
record that its conditions were met. Both are legitimate; only one is what happened, and a
later reader must not be able to mistake the second for the first.

---

## What is unblocked, and what is not

**Unblocked by G-09:**

- Creation of `src/`, `configs/`, `pyproject.toml`, `tests/fixtures/`, and the modules §12
  mandates. (TE:735 — authority to create a module is not authority to write it; both now
  exist for the modules in scope.)
- `tests/test_release_hashes.py` — extension to cover §13.3's manifest fields and R-13's
  overwrite refusal (TA-15).
- `tests/test_release_hashes.py` and `tests/test_acquisition_window.py` — routing their
  restricted-content reads through `open_restricted`.

**NOT unblocked, and this list is exhaustive of the gates that still bind:**

- **G-05 and G-06 remain `Blocked`.** No locked-test access, no December prediction, no
  metric.
- **G-P1A, G-P2, G-P3A, G-P3C, G-07** are unaffected — G-09 is the coding gate only.
- **TE §18.2's absolute rule stands.** No scientific value may be changed after seeing a
  result; no agent may fill a freeze-gate value by convenience. Every value stage 3.1
  routed to G-04/G-05 **stays routed**.
- **TE §18.3's stop-and-report obligation survives its own gate.** It is a standing rule on
  implementation, not a one-time gate condition.

---

## Propagation sweep — `CHANGE_RECORD_PROCEDURE.md` steps 1–5

**Step 1 — superseded literals named.** `"G-09 is not signed"`, `"G-09 stays unsigned"`,
`"G-09 remains unsigned"`, `"G-09 unsigned"`, `"Pending — G-09"`, and the standing clause
`"no rule here authorises creating"` where its sole stated ground is G-09.

**Step 2 — swept.** Every `*.md` under `PreFlight/`, the intent record, `evidence/`,
`governance/` and `aidlc/spaces/default/memory/`.

**Step 3 — disposition.**

| Site class | Disposition |
|---|---|
| `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` (gate table row, §18.3, TE:735) | **Not edited — authority document.** A Vision §15.2 amendment to the gate-table row is **owed** and recorded here as such. Owner: Supervisor. |
| The twelve stage-3.1 units' `"G-09 is not signed"` clauses | **Edited in-stage**, annotated with D-31 and with the unmet-precondition disclosure carried, never dropped. |
| `evidence/DECISIONS.md` | **D-31 added**; register row added. |
| `governance/reviews/GOV-2026-08-28-FD-01.md` and prior reports | **Correct as-is — historical records** of what was true when written. |
| `aidlc/spaces/default/memory/*.md` | **Not edited — memory layer.** `org.md` reserves it for the practices-affirmation gate. No G-09 claim is carried there. |

**Step 4 — arithmetic.** This record carries one gate transition and states five
precondition rows, each derived from inspection rather than from an adjacent document. No
count is carried.

**Step 5 — re-derived, not decremented.** The precondition states were established by
inspecting the workspace and environment on 2026-08-28, not by adjusting a prior
assessment.

---

## Owed as a consequence of this record

1. **A Vision §15.2 amendment to TE §1.2's gate-table row** for G-09 (`Pending` → signed,
   with the disclosure). Owner: Supervisor. Not taken here — the authority document is not
   edited by a change record.
2. **`aws_ai_dlc_preflight_report`** remains undesigned-and-unwritten (`GOV-2026-08-28-FD-01`
   Rec 9). G-09's signature does not create it, and TA-23 stays uncovered.
3. **The automated zero-TBD preflight** (§18.3 precondition 2) remains unbuilt. When
   `configs/` is created, it is owed before any affected component is implemented.
