# TEC_Project governance gate report

## Decision

| Field | Value |
|---|---|
| Report ID | `<GOV-...>` |
| Review timestamp (UTC) | `<...>` |
| AI-DLC intent / stage / gate | `<...>` |
| TEC gate(s) | `<...>` |
| Review mode | `ADAPTIVE` / `FULL BOARD` |
| Gate verdict | `PASS` / `CONDITIONAL PASS` / `FAIL` / `NOT REVIEWABLE` |
| Model advancement | `ADVANCE` / `DO NOT ADVANCE` / `N/A` |
| Human approver required | `<student / supervisor / both>` |

### Rationale

State the evidence-backed reason for the verdict in no more than five sentences. Distinguish process validity from model success.

## Authority and evidence

| Item | Version / ID / hash | Path | Status |
|---|---|---|---|
| Vision | `<...>` | `<...>` | `READ` / `MISSING` / `CONFLICT` |
| Technical Environment | `<...>` | `<...>` | `<...>` |
| Freeze/change record | `<...>` | `<...>` | `<...>` |
| Reviewed artifact set | `<...>` | `<...>` | `<...>` |
| Evidence index/manifests | `<...>` | `<...>` | `<...>` |

List missing evidence explicitly. Never infer a version or hash.

## Board

| Reviewer | Active / N/A | Conflict | Pass completed | Position |
|---|---|---|---|---|
| Review Chair / Decision Owner | `<...>` | `<...>` | `<...>` | `<...>` |
| TEC & Space-Weather Expert | `<...>` | `<...>` | `<...>` | `<...>` |
| ML & Statistical Methods Reviewer | `<...>` | `<...>` | `<...>` | `<...>` |
| Data Quality & Reproducibility Reviewer | `<...>` | `<...>` | `<...>` | `<...>` |
| Benchmark & Deployment Reviewer | `<...>` | `<...>` | `<...>` | `<...>` |
| Validation Auditor | `<...>` | `<...>` | `<...>` | `<...>` |
| Implementation Reviewer | `<...>` | `<...>` | `<...>` | `<...>` |

## Gate criteria

| Criterion ID | Requirement | Evidence | Result | Finding ID |
|---|---|---|---|---|
| `<...>` | `<...>` | `<path/section/hash>` | `PASS` / `FAIL` / `MISSING` / `N/A` | `<...>` |

## Executive Summary

- **Overall quality assessment**: `<...>`
- **Readiness**: `Approve` / `Needs Review` / `Major Revision` — editorial readiness, stated alongside the gate verdict above, never in place of it. If the two diverge, say why in one sentence.
- **Overall score**: `<...>` — omit this line entirely when no score applies; never invent a number.
- **Findings**: Critical `<n>` · High `<n>` · Medium `<n>` · Low `<n>`

Derive every count from the Recommendation blocks below and print it. Never carry a count from adjacent prose or an earlier revision.

## Findings

One numbered block per finding, most severe first. Severity is the reviewer grade rendered as `BLOCKER`→Critical, `MAJOR`→High, `MINOR`→Medium, `NOTE`→Low.

### Recommendation `<X>` — `<short title>`

- **Category**: `Functional` / `Architecture` / `Design` / `Security` / `Performance` / `UX` / `QA` / `Requirements` / `Documentation` / `API` / `Database` / `Testing` / `Maintainability` / `Operations` / `Compliance` / `AI-DLC` / `Other`
- **Severity**: `Critical` / `High` / `Medium` / `Low` (reviewer grade: `<BLOCKER / MAJOR / MINOR / NOTE>`)
- **Finding ID / reviewer**: `<FINDING-ID>` — `<seat>`
- **TEC gate / AI-DLC stage**: `<...>`
- **Requirement**: `<authority section or stable ID>`
- **Evidence**: `<artifact path, section/line, test/log/hash>`

**Issue** — `<observed mismatch: fact, not inference>`

**Importance** — `<why it matters in this project>`

**Risk** — `<what happens if left unchanged>`

**Possible Solutions**

1. `<option>`
2. `<option, where a second genuinely valid one exists>`

**Comparison** — `<advantages and disadvantages of each option; say plainly when two are equally valid>`

**Recommendation** — `<preferred option with justification; smallest acceptable remediation>`

- **Closure evidence**: `<test, manifest, approval or rerun>`
- **Owner / due gate**: `<...>`

**Decision Required** — `Approve` / `Reject` / `Modify` / `Postpone`. Never assume approval.

## Reviewer disagreements

Record each disagreement, both evidence bases, the governing authority clause, and whether it remains unresolved. Write `None` only after checking.

## Traceability and downstream impact

List affected requirement, decision, test, dataset, feature, mask, experiment, and artifact IDs. Name every downstream artifact invalidated or requiring regeneration.

## Human decisions required

1. `<Approve / reject / freeze a value / authorize remediation / declare exploratory>`

The board recommendation does not grant academic approval or authorize locked-test access.

**STOP here.** Wait for the student or supervisor to approve, reject, modify, postpone, ask questions, request another review, or request implementation. No document may be updated, and no finding applied, before that explicit instruction.
