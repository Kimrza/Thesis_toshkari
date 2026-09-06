# Stage Diary — code-generation

## Interpretations

- 2026-09-05T08:44:06Z — Human ruling received on resume (verbatim): "fix : four one-line Minors ride READY verdicts as recorded input for 3.5; Recommendations 10–14 are checklist lines for G-05/G-07 and the next practices gate (including the stale team.md D-14 line).& (adaptive, 3 seats + Chair): CONDITIONAL PASS with 5 High / 4 Medium / 5 Low findings." Interpreted as the disposition on the nfr-design governance review delivered in the 2026-09-04 session: (1) the Minor findings riding the terminal READY reviewer verdicts of the nfr-design units are recorded input for each unit's code-generation (3.5) run — each unit's plan lists and addresses the Minors recorded in that unit's own nfr-design `## Review` sections; (2) Recommendations 10–14 of that review become checklist lines for gates G-05, G-07, and the next practices-affirmation gate, one of which is the stale `team.md` § Walking Skeleton line "The one-month all-station scientific window remains open under Q-31" — superseded by `evidence/DECISIONS.md` D-14, which froze that window. Ruling recorded at `governance/RULING_2026-09-05_nfr-design_governance_dispositions.md`.
- 2026-09-05T08:44:06Z — The governance report itself (adaptive, 3 seats + Chair, CONDITIONAL PASS, 5 High / 4 Medium / 5 Low) was delivered in-session on 2026-09-04 and is not on disk; per project rule (delivery-planning:c12) it is not reconstructed. The Minor findings are durably recorded in the unit artifacts' `## Review` sections and the audit shards; the full Recommendation 10–14 texts must be restated from the report at the gates they now gate.

## Deviations

- 2026-09-05T11:20:00Z — graphify CLI not on PATH in this environment; the CLAUDE.md pre-exploration query and post-modification `graphify update .` could not run for foundation's generation; orientation was by direct reads of the unit's design artifacts. Graph is stale for `src/data/*` and `tests/*` until graphify is available.
- 2026-09-05T11:20:00Z — The brief's "local interpreter is 3.14.7" was stale for this machine (no Python at all; Store stubs). The developer bootstrapped Python 3.11.9 + exact pinned deps from conda-forge (micromamba) into `Temp\26\tec311`; all suite runs are smoke evidence only, and the summary states so. Nothing installed into the repo.

## Tradeoffs

## Open questions

- 2026-09-05T08:44:06Z — statistical-inference's terminal nfr-design review states its 1 Major (mask-vs-member `FairnessError` check homeless across both units' designs) "should be closed — by an explicit carried-dependency statement or a local fallback check — before 3.5 builds from this design"; confirm closure when that unit's 3.5 iteration starts.
