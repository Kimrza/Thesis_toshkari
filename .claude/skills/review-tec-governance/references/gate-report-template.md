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

## Findings

### `<FINDING-ID>` — `<short title>`

- Reviewer: `<seat>`
- Severity: `BLOCKER` / `MAJOR` / `MINOR` / `NOTE`
- TEC gate / AI-DLC stage: `<...>`
- Requirement: `<authority section or stable ID>`
- Evidence: `<artifact path, section/line, test/log/hash>`
- Observed mismatch: `<fact, not inference>`
- Consequence: `<...>`
- Smallest acceptable remediation: `<...>`
- Closure evidence: `<test, manifest, approval or rerun>`
- Owner / due gate: `<...>`

## Reviewer disagreements

Record each disagreement, both evidence bases, the governing authority clause, and whether it remains unresolved. Write `None` only after checking.

## Traceability and downstream impact

List affected requirement, decision, test, dataset, feature, mask, experiment, and artifact IDs. Name every downstream artifact invalidated or requiring regeneration.

## Human decisions required

1. `<Approve / reject / freeze a value / authorize remediation / declare exploratory>`

The board recommendation does not grant academic approval or authorize locked-test access.
