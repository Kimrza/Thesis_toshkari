<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-08-15T00:00:00Z — Q12 is a single-select question but was answered `C,D,B`; read as a ranked ordering (C highest, then D, then B) rather than three co-equal top risks, and surfaced for confirmation at the summary checkpoint before artifact generation.
- 2026-08-15T00:00:00Z — Q7 omits option D (university/supervisor requirements on data handling, authorship or publication) while the intent statement records supervisor countersign authority at G-05/G-07; read as governance gating over decisions rather than a data-handling or publication licensing obligation, so the two are not treated as contradictory.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-08-15T18:41:13Z — the human asked to keep "no capability ceiling on the design" against Vision §4.4; recorded the clause as binding-until-changed and preserved their reasoning verbatim as evidence for a §15.2 change request, rather than either writing the contradiction or discarding their intent. Alternative considered: pause the stage entirely until the supervisor rules, rejected because the clause is workable in the meantime and pausing would have cost a semester-bounded schedule for no gain.
- 2026-08-15T18:41:13Z — checked the drafted artifacts against the Vision normative core directly rather than only against the questions; that check is what found the §4.4 contradiction, the missing 10 GB storage envelope, and the omitted IRI validation-report obligation. None of the three was visible from the answers alone.

## Open questions
<!-- 2026-08-15 additions below -->
- 2026-08-15T18:41:13Z — whether the supervisor amends Vision §4.4 (change request D-09) or retains the beginner-to-intermediate capacity clause; downstream design stages inherit whichever answer lands.
- 2026-08-15T18:41:13Z — the three intent-capture board reports (IC-01/02/03) are still unpersisted under `governance/reviews/`; only the two feasibility reports are filed, so GOV-25 is partly open.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
