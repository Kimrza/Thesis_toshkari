---
inclusion: always
---
# MANDATORY: Add Recommendations and Impact Analysis to All Questions

**CRITICAL**: When creating ANY question file during the AI-DLC workflow (e.g., requirement-verification-questions.md, clarification questions, design questions, etc.), you MUST include your recommendation and a short impact analysis for every question and every option.

## Format

For each question, add:
1. **A recommendation** indicating which option you suggest and why
2. **A short impact analysis** for each option explaining the consequences of choosing it

## Example Format

```markdown
## Question 1
What architectural pattern should be used?

A) Monolithic architecture
   > **Impact**: Simpler to develop and deploy initially. Lower operational overhead. Harder to scale individual components independently. Risk of becoming a "big ball of mud" as complexity grows.

B) Microservices architecture
   > **Impact**: Independent scaling and deployment per service. Higher operational complexity (service discovery, distributed tracing, network latency). Better for large teams working in parallel.

C) Serverless architecture
   > **Impact**: Zero infrastructure management. Pay-per-use cost model. Cold start latency. Vendor lock-in risk. Best for event-driven, variable-load workloads.

D) Other (please describe after [Answer]: tag below)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — Given the project's multi-team structure and need for independent deployability, microservices provide the best long-term scalability while allowing teams to work autonomously.

[Answer]: 
```

## Rules

- The recommendation MUST appear after all options but before the [Answer]: tag
- Use the `> **💡 Recommendation**:` format for visibility
- Use the `> **Impact**:` format indented under each option
- Keep impact analysis concise (1-3 sentences per option)
- Base recommendations on the project context, requirements, and best practices
- If no clear winner exists, state that and explain the trade-offs
- Never hide or downplay risks of the recommended option — be honest about trade-offs
