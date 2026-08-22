# Claude Code and AI-DLC v2 integration

## Placement

Install AI-DLC v2 for Claude Code using its maintained distribution. Place this skill at:

```text
<project>/.claude/skills/review-tec-governance/SKILL.md
<project>/.claude/skills/review-tec-governance/references/*.md
```

Keep the current Vision and Technical Environment in the repository. Do not copy them into the skill; the review must read their current approved versions.

Do not edit AI-DLC's shipped conductor, hooks, stage files, agents, or state machine to embed this overlay. Reapply this skill independently when AI-DLC is upgraded.

## Project instruction

Add the following policy to the project's existing `CLAUDE.md` without overwriting AI-DLC instructions:

```markdown
## TEC_Project governance overlay

Before asking the human to approve any completed AI-DLC stage, run
`/review-tec-governance` against that stage's artifact set. Use adaptive mode
unless the skill requires full-board mode. Do not approve, advance, or mutate
the reviewed artifact while a governance verdict is FAIL or NOT REVIEWABLE.

Full-board review is mandatory for G-05, G-06, G-P2, G-P3, locked-test access
or evidence, phase-transition hashes, model advancement, final reproducibility,
release, and claims. AI-DLC approval and TEC governance are separate: AI-DLC
may say the stage is complete, but only the human student/supervisor may accept
the TEC gate after reading the governance report.

When a project Markdown document reaches a finalized state and no review was
explicitly requested, do not review it automatically. Ask first, and stop on
`No`. Every review is delivered in the format fixed by
`.claude/skills/review-tec-governance/references/review-output-contract.md`,
then STOP and wait.
```

## Porting a Kiro steering setup

Kiro's document-finalized hook has no direct Claude Code equivalent, and it does
not need one. Its two halves land in different places:

| Kiro construct | Claude Code equivalent |
|---|---|
| Hook trigger on a finalized Markdown document | The `CLAUDE.md` governance-overlay policy above, which tells the session to run the board before a stage approval |
| The hook's "would you like a review?" prompt | [review-output-contract.md](review-output-contract.md) § **Consent before review** — asked at the start of the run |
| Review output format, principles, forbidden behaviour, approval workflow | [review-output-contract.md](review-output-contract.md), read at the start of every run |
| A steering file with `inclusion: always` | A project rule under `.claude/rules/`, imported by an `@`-line at the top of `.claude/CLAUDE.md` — for example `.claude/rules/question-recommendations.md` |

Do not build a `PostToolUse` hook that offers a review on every Markdown write.
AI-DLC writes Markdown constantly, so the prompt would fire on drafts, memory
files, and diaries, and the noise trains the human to dismiss it. The
policy-plus-consent path keeps the ask at the approval gate where the decision
actually is.

## Invocation pattern

At an AI-DLC approval prompt, invoke:

```text
/review-tec-governance Review the current AI-DLC stage artifacts before approval.
Stage: <stage number and name>
TEC gate: <known gate, or determine from the gate map>
Artifacts: <paths>
Evidence index: <path>
Mode: adaptive | full-board
```

Store requested durable reports under a project-controlled path such as:

```text
governance/reviews/<gate>/<UTC-date>-<artifact-id>.md
```

Use a new report ID for every review. Never overwrite a prior gate report; supersede it with an explicit link.

## AI-DLC interaction rules

- Run after the stage artifact exists and before the human stage approval.
- Run after AI-DLC phase-boundary verification and before handoff.
- Always review the first Construction Bolt/walking skeleton.
- AI-DLC Construction autonomous mode may skip later Bolt gates, but it may not skip TEC gates or full-board triggers.
- A governance `FAIL` or `NOT REVIEWABLE` returns control to remediation; it does not change AI-DLC state by itself.
- After remediation, rerun the board against the new artifact/version and preserve the previous report.
