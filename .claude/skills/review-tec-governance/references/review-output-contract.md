# Review output contract

Binding on every `/review-tec-governance` run. The board's judgement is set by
[review-criteria.md](review-criteria.md); this file fixes how that judgement is
delivered, what the board may never do, and what happens after the report.

## Consent before review

Never start a review the human did not ask for, and never review an unfinished
draft without permission. Both are covered by one rule.

- **Invoked with an explicit target** (paths, a stage, a gate) — proceed. The
  invocation is the permission.
- **Invoked with no target**, or reached through the `CLAUDE.md` governance
  overlay because a stage artifact just reached a finalized state — name the
  documents you are about to review and ask first:

  > These documents appear finalized: `<paths>`.
  > Should the Enterprise Governance Review Board perform a full governance
  > review of them?

  On `No`, stop. Do nothing else. On `Yes`, run the complete review.
- **Target exists but is visibly incomplete** (open `TBD`, unwritten sections,
  a stage still mid-run) — say what is incomplete and ask whether to review it
  as-is or wait. Do not review it silently, and do not fill the gaps yourself.

Reviewing without permission is a defect even when the findings are correct.

## Standard output

One consolidated Markdown report per run — never a stream of separate reviewer
memos. Order:

1. The **Decision**, **Authority and evidence**, **Board**, and **Gate
   criteria** tables from [gate-report-template.md](gate-report-template.md).
   These carry the gate verdict, authority versions and hashes, seat activation,
   and criterion-level results. They are not optional and are not replaced by
   the sections below.
2. **Executive Summary** — see below.
3. **Findings**, rendered as numbered `### Recommendation X` blocks — see below.
4. **Reviewer disagreements**, **Traceability and downstream impact**, and
   **Human decisions required**, per the template.

### Executive Summary

- Overall quality assessment.
- Readiness: `Approve` / `Needs Review` / `Major Revision`. This is the
  editorial readiness of the artifact and is **not** a substitute for the gate
  verdict (`PASS` / `CONDITIONAL PASS` / `FAIL` / `NOT REVIEWABLE`) in the
  Decision table. State both; when they diverge, say why in one sentence.
- Overall score, if one is applicable. Omit the line rather than inventing a
  number.
- Findings count by severity: Critical, High, Medium, Low — each stated
  explicitly, including zeros.

Derive every count programmatically from the finding blocks and print it;
never carry a count from earlier prose or an earlier revision.

### Recommendation blocks

Each finding is one block. Every field is mandatory.

```markdown
### Recommendation X

**Category**: one of Functional, Architecture, Design, Security, Performance,
UX, QA, Requirements, Documentation, API, Database, Testing, Maintainability,
Operations, Compliance, AI-DLC, Other.

**Severity**: Critical / High / Medium / Low.

**Issue** — the problem, as observed fact with its citation.

**Importance** — why it matters here.

**Risk** — what happens if it is left unchanged.

**Possible Solutions** — one or more genuinely valid options.

**Comparison** — advantages and disadvantages of each option.

**Recommendation** — the preferred option, with justification.

**Decision Required** — Approve / Reject / Modify / Postpone.
```

Keep the board's evidence spine inside the block: finding ID, reviewing seat,
cited authority section, evidence path with section/line/hash, affected TEC gate
and AI-DLC stage, smallest acceptable remediation, closure evidence, owner and
due gate. The Recommendation format replaces the presentation of the finding
list, not its substance.

**Severity mapping.** Reviewers grade findings `BLOCKER` / `MAJOR` / `MINOR` /
`NOTE` during their passes; the report renders them as Critical / High / Medium /
Low respectively. Carry the reviewer grade in the block so the mapping stays
auditable.

Never assume approval. A stated Recommendation is a proposal awaiting a human
decision, not a decision.

## Review principles

- Stay objective; keep personal preference out of it.
- Do not propose redesign the evidence does not require.
- Preserve approved business, scientific, and scope decisions. A frozen value is
  not a finding merely because a reviewer would have chosen differently.
- Separate fact from opinion, and mandatory obligations from optional
  improvements. Label which is which.
- State assumptions explicitly. State uncertainty explicitly rather than
  rounding it to confidence.
- Separate MVP-necessary work from future enhancement.
- When several solutions are equally valid, present every reasonable option and
  let the human choose. Do not pick automatically, and say plainly that the
  choice is open.

## Forbidden

Never, in any review:

- rewrite a document automatically, or modify any file silently;
- invent a business rule, API, workflow, persona, requirement, architecture, or
  scientific value;
- remove approved content;
- change terminology without saying so and why;
- ignore a project constraint recorded in the constraint register or the memory
  layers;
- review an incomplete draft without permission (see **Consent before review**);
- apply a finding as an edit before the human decides on it. The finding is the
  deliverable.

## Cross-artifact governance checks

Every review also checks the artifact against the rest of the project, not only
against itself. Flag every inconsistency as a finding — never as an aside.

- Consistency between documents; shared terminology; consistent naming; aligned
  and non-colliding IDs.
- Complete traceability, both upstream to the authority documents and downstream
  to dependent artifacts.
- No duplicated requirements; no contradictory requirements.
- Architecture, API, database, testing, and NFR consistency.
- MVP/scope consistency; implementation feasibility; maintainability;
  extensibility; auditability.

## AI-DLC coverage

Check alignment with each AI-DLC artifact class the active scope actually
produces: Vision, Scope, Personas, Stories, Requirements, NFRs, Architecture,
ADRs, APIs, Data Model, UX, Tasks, Tests, Acceptance Criteria, Traceability,
Definition of Ready, Definition of Done.

Record `N/A` with the reason for every class the active scope marks `SKIP` —
this project's scope skips several, and a skipped class is not a gap. Never
manufacture a finding out of an artifact the scope deliberately does not
produce, and never let a skipped class hide an obligation the authority
documents place elsewhere: when a scope skip removes the usual carrier of a
requirement, name where the requirement now lives.

## Approval workflow

After the report: **STOP.** Wait for instructions.

The human may approve, reject, or modify one or more recommendations, ask
questions, request another review, or request implementation. Only after
explicit approval may any document be updated — and remediation is a separate
run from the review that recommended it.

`FAIL` or `NOT REVIEWABLE` returns control to remediation. It does not change
AI-DLC state, and it does not authorise you to fix anything.

## Governance-approved

An artifact is governance-approved only when it is internally consistent,
complete, technically feasible, aligned with every existing project artifact,
compliant with the approved architecture and research goals, testable,
maintainable, traceable, implementation-ready — **and** approved by the human.
The board's verdict is the recommendation; the human's acceptance is the
approval. The board never grants academic approval and never authorises
locked-test access.
