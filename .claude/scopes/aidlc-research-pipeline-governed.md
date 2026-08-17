---
name: research-pipeline-governed
depth: Comprehensive
keywords: []
description: Governed research pipeline on a frozen data contract
skeleton: off
---

# research-pipeline-governed scope

A composed scope for reproducible research/forecasting pipeline work that
runs under an external governance overlay (TEC gate reviews) on top of a
frozen data contract. Seventeen stages execute; fifteen are folded or
skipped. Comprehensive depth applies to the stages that do run — the grid
is lean, but each surviving artifact is written to audit standard, because
the governance board reads them and evidence quality, not stage count, is
what a gate verdict turns on.

Composed via `/aidlc compose`, approved verbatim by the human. Ships with
`keywords: []` — this scope is resolvable only by explicit
`--scope research-pipeline-governed` and never participates in inference.

## Why these stages, why skip those

**Ideation (3 of 7).** `intent-capture` and `feasibility` execute: the
research intent carries real ambiguity and the viability of the modelling
approach must be settled before design commits to it. `approval-handoff`
executes as the ideation→inception phase gate. `market-research`,
`scope-definition`, `team-formation`, and `rough-mockups` skip — there is
no market to research, no UX surface, no multi-team coordination, and the
scope boundary is fixed by the frozen data contract rather than
negotiated.

**Inception (4 of 6).** `practices-discovery` executes (verification
practice for a research pipeline is not yet established and drives the
testing posture downstream). `requirements-analysis` executes for its
unique outputs — functional decomposition, constraints, and the
out-of-scope boundary — all of which downstream design consumes.
`application-design` and `units-generation` execute to establish the
pipeline architecture and its decomposition; `delivery-planning` executes
to sequence the units. `reverse-engineering` skips: CodeKB is the
structural evidence source for this composition, which leaves the local
reverse-engineering artifact store unwritten — downstream design stages
run from requirements plus existing code instead. `user-stories` and
`refined-mockups` skip — no personas with divergent journeys, no UI.

**Construction (6 of 7).** `functional-design`, `nfr-requirements`,
`nfr-design`, `code-generation`, and `build-and-test` execute. The NFR
pair is kept intact rather than folded because reproducibility,
determinism, and evaluation correctness are interacting non-functional
properties whose implementation approach is not obvious and which the
governance board reviews as evidence. `infrastructure-design` and
`ci-pipeline` skip — the pipeline runs on existing local/lab compute with
no new infrastructure surface.

**Operation (1 of 6).** `performance-validation` executes: measured model
and pipeline performance against the locked evaluation protocol is the
deliverable, not an afterthought. `deployment-pipeline`,
`environment-provisioning`, `deployment-execution`,
`observability-setup`, `incident-response`, and `feedback-optimization`
all skip — there is no deployed production service to operate.

## Walking skeleton

`skeleton: off`. The data contract is frozen and the pipeline stages
attach to an existing, known input surface, so there is nothing to
bootstrap end-to-end first. The first unit runs like any other; the
ladder prompt does not fire.

## Governance interaction

This scope does not encode the TEC governance overlay — that overlay is a
project-level rule that gates human approval of each stage independently
of AI-DLC's own completion signal. Comprehensive depth exists here so the
artifacts each stage produces are reviewable at that board.
