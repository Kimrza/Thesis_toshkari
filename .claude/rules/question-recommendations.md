# MANDATORY: recommendations and impact analysis in every question file

Applies to ANY question file created during the AI-DLC workflow — stage question
sets, `requirement-verification-questions.md`, clarification questions, design
questions, interview files, and any other file that asks the human to choose.

Every question must carry:

1. A `> **Impact**:` line under **each** option — 1-3 sentences on the
   consequences of choosing it, including under the mandatory
   `X. Other (please specify)` option.
2. A single `> **💡 Recommendation**:` line naming the suggested option and why,
   placed after all options but **before** the `[Answer]:` tag.

## Format

```markdown
## Question 1
What architectural pattern should be used?

A) Monolithic architecture
   > **Impact**: Simpler to develop and deploy initially. Lower operational overhead. Harder to scale individual components independently. Risk of becoming a "big ball of mud" as complexity grows.

B) Microservices architecture
   > **Impact**: Independent scaling and deployment per service. Higher operational complexity (service discovery, distributed tracing, network latency). Better for large teams working in parallel.

C) Serverless architecture
   > **Impact**: Zero infrastructure management. Pay-per-use cost model. Cold start latency. Vendor lock-in risk. Best for event-driven, variable-load workloads.

D) Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — Given the project's multi-team structure and need for independent deployability, microservices provide the best long-term scalability while allowing teams to work autonomously.

[Answer]:
```

## Rules

- The recommendation goes after all options and before the `[Answer]:` tag.
- Use `> **💡 Recommendation**:` and `> **Impact**:` exactly, for visibility.
- Keep each impact analysis to 1-3 sentences.
- Base the recommendation on this project's context, its governing documents,
  and the memory layers — not generic best practice.
- If no clear winner exists, say so and explain the trade-offs.
- Never hide or downplay the risks of the recommended option.
- Preserve the literal `[Answer]:` tag and the mandatory
  `X. Other (please specify)` option exactly as written — both are fixed
  English tokens the engine matches (`org.md` § "Conversation language —
  preserved tokens").
