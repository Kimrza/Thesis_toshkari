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
```

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
