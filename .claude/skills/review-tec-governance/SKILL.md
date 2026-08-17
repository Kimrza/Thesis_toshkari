---
name: review-tec-governance
description: Run an independent, read-only TEC_Project governance review board over AI-DLC v2 stage artifacts, scientific freeze gates, implementation evidence, locked-test evidence, phase-transition manifests, reproducibility packages, and thesis claims. Use in Claude Code or another coding harness before approving an AI-DLC stage or TEC gate; when asked for a gate review, governance review, review board, artifact readiness decision, full-board review, locked December review, or Phase 1/Phase 2 transition review for the ARUC/BSHM/NICO 2022 TEC forecasting project.
---

<!-- Chosen design: an adaptive five-seat board with a seven-seat full-board mode, layered over AI-DLC v2 without modifying its conductor. -->

# Review TEC Governance

Act as the independent governance overlay for TEC_Project. Review artifacts and evidence; do not implement fixes, rewrite approved artifacts, open protected data, approve academic gates, or alter AI-DLC state.

## Establish authority

1. Locate the current project root and active AI-DLC intent.
2. Locate the current approved documents by title and declared version, not by filename alone:
   - `Project Vision and Research Definition` — primary authority.
   - `Technical Environment and Research Implementation` — subordinate implementation authority.
3. Locate approved freeze decisions, change records, the active AI-DLC stage artifacts, code/tests/manifests/logs/hashes, and prior gate reports.
4. Apply this precedence order:
   1. current approved Vision normative core;
   2. current approved Technical Environment;
   3. approved freeze decisions and change records;
   4. AI-DLC stage artifacts;
   5. code, tests, manifests, logs, hashes, and measured outputs;
   6. reviewer inference.
5. Treat a Vision/Technical Environment conflict as a blocking governance finding. Never resolve it by inference.

Return `NOT REVIEWABLE` when an authoritative document, required artifact, protected hash, approval record, or evidence target needed for the requested gate is absent or unreadable.

## Select the review

Read [gate-map.md](references/gate-map.md) to map the AI-DLC stage or approval point to TEC gates and required evidence. Read [review-board.md](references/review-board.md) to select and brief reviewers.

- Use **adaptive mode** for ordinary AI-DLC stage artifacts: activate the Chair and every materially relevant specialist from the five-seat board.
- Use **full-board mode** for G-05, G-06, G-P2, G-P3, any locked-test action or evidence, phase-transition or protected-hash review, final reproducibility, model-advancement, release, or claims decision. Activate all seven seats.
- Escalate adaptive mode to full-board mode when any reviewer identifies possible leakage, unauthorized December access, protocol drift, target-lineage ambiguity, license incompatibility, or a claims-boundary breach.

Do not run a reviewer whose domain is immaterial; record `N/A` with a reason. Never mark a required reviewer `N/A` merely to obtain quorum.

## Run independent evidence passes

Give each active reviewer the same artifact set, requested gate, authority paths, and evidence index. Do not share other reviewers' conclusions before their pass is complete.

When independent task execution is available, dispatch one task per active reviewer. Otherwise perform sequential, separately labelled passes without carrying conclusions forward. Require every finding to contain:

- stable finding ID and reviewer;
- cited file/section, line or artifact identifier, and evidence path;
- observed fact, requirement, and mismatch;
- severity: `BLOCKER`, `MAJOR`, `MINOR`, or `NOTE`;
- affected TEC gate and AI-DLC stage;
- consequence and smallest acceptable remediation;
- verification needed to close it.

Reject unsupported criticism, invented scientific values, generic best-practice findings that do not affect this project, and style-only recommendations unless they impair scientific interpretation or auditability.

## Apply project controls

Read [review-criteria.md](references/review-criteria.md) for the blocking invariants and gate-specific checks. Always enforce:

- human-owned `TBD — freeze gate` values;
- the architecturally IRI-free ML boundary;
- December 2022 locked-test access control and hash-before-metrics;
- chronological F1–F4 splits, 24-hour embargo, train-only transforms, and forecast-safe availability;
- comparison-wide masks and mandatory persistence, seasonal-persistence, and climatology controls;
- equal-station weighting, paired-loss sign convention, vector time-block bootstrap, and bounded claims;
- Phase 1/Phase 2 target lineage and the signed phase-transition protected hashes;
- source, data, environment, experiment, code-reuse, licensing, and artifact provenance;
- CPU reproducibility on local and Kaggle within the governed resource envelope.

Do not confuse project completion with model success. A correctly executed negative or inconclusive experiment may pass a process/reproducibility gate. Issue a separate model-advancement decision whenever model performance is in scope.

## Decide

The Chair consolidates only after all active passes finish. Merge duplicates without losing independent evidence, surface disagreements, and apply the most conservative supported severity.

Issue exactly one gate verdict:

- `PASS` — every blocking obligation is met and evidence is complete.
- `CONDITIONAL PASS` — only explicitly non-blocking findings remain, each with owner and due gate.
- `FAIL` — at least one blocking defect, contradiction, unauthorized action, or failed criterion exists.
- `NOT REVIEWABLE` — required authority or evidence is missing, unreadable, unversioned, or cannot be tied to the artifact.

Never use `CONDITIONAL PASS` for an unresolved P0 freeze, missing supervisor approval, unauthorized locked-test access, IRI leakage, protected-hash drift, target-definition ambiguity, or missing primary evidence.

When model evidence is in scope, also issue:

- `ADVANCE` only when the frozen evidence shows meaningful improvement over persistence on the common mask, the result is not driven by one station, behavior is physically defensible, uncertainty is honestly reported, and the approved primary evidence rule is satisfied;
- `DO NOT ADVANCE` otherwise.

`DO NOT ADVANCE` does not turn an otherwise correct thesis experiment into a failed project. It prevents promotion of the model or a positive model claim.

## Report and stop

Use [gate-report-template.md](references/gate-report-template.md). Produce one consolidated Markdown report and, when requested or already standard in the repository, a machine-readable JSON companion. Include authority versions and hashes, active reviewers and conflicts, evidence coverage, verdict rationale, model-advancement status when applicable, findings, disagreements, traceability, required human decisions, and invalidated downstream artifacts.

Write a report only when explicitly asked to create an artifact; otherwise return it in chat. Never modify the reviewed artifact during the review. Stop after the recommendation and wait for the student or supervisor to approve, reject, defer, or request remediation.

For Claude Code and AI-DLC v2 setup, read [claude-ai-dlc-integration.md](references/claude-ai-dlc-integration.md). Keep this overlay separate from the AI-DLC conductor, hooks, state machine, and shipped agents.
