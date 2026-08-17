# Requirements Analysis — Stage Memory

Observation diary for stage 2.3 (requirements-analysis). Maintained while the
stage runs; read by the §13 learnings ritual before the approval gate.

## Interpretations

- 2026-08-16T16:20:00Z — Treated this stage as decomposition and traceability rather than elicitation. Vision v4.2 §§1-17 and Technical Environment v3.2 already fix the research question, estimand, feature contract, evaluation protocol, claim boundary and NFRs; `constraint-register.md` carries TC/OC/PC rows and `discovered-rules.md` carries 58 affirmed hard rules. Inventing new requirements here would breach `phases/inception.md` § Traceability ("do not introduce new requirements in inception without documenting their origin"). Questions therefore target what the authority documents leave genuinely open or leave un-decomposed, not what they already settle.
- 2026-08-16T16:20:00Z — `user-stories` (2.4) is SKIP in this scope, so §16's WS-09-WS-20 and §19's TA rows are the only acceptance vocabulary Construction will receive. Requirements written here must carry pass/fail criteria that map onto those rows, or Construction inherits requirements it cannot test against.

## Deviations

- 2026-08-17T00:00:00Z — Q3 was answered with free text ("i have my supervisors approval do not ask again") rather than an option letter, and the answer barred a follow-up. Step 9 would normally raise a targeted follow-up on exactly this kind of ambiguity. Honoured the instruction instead: did not re-ask, adopted a stated reading (write the requirement, threshold as a named hole citing Vision 6.1B, operating on D-2's interim rule), and surfaced that reading at the Consolidated Summary Confirmation, which is a separate human stop where it could still be corrected. The human answered "Looks correct".
- 2026-08-17T00:00:00Z — Q10 arrived unanswered in the batch (the user supplied Q1-Q9 for a ten-question file). Asked Q10 alone as a structured question rather than proceeding on partial answers, per Step 8 item 2. Answered A.

## Tradeoffs

- 2026-08-17T00:00:00Z — Q2=A decomposes by the P1-00..P1-06 pipeline stages. That leaves the repository scaffold, pins and test suite without a home, since TC-06 places them before P1-01 and no P1 row covers them. Added a REQ-ENG-* group ahead of FR-P1-00 rather than forcing the scaffold into P1-00 (which is the ICTP audit closure) or dropping it. Alternative considered and rejected: decompose by the six src/ packages (Q2=B), which would have housed the scaffold naturally but would have detached requirements from the stage table that Construction actually executes.
- 2026-08-17T00:00:00Z — Chose to list untested requirements explicitly (18 of them) in their own section rather than silently omitting them or inventing WS/TA rows. Q1=A mandates flagging over inventing; the section doubles as concrete input for NFR Requirements (3.2) when it assembles the G-05 freeze manifest.

## Open questions

- 2026-08-16T16:20:00Z — Two supervisor gates remain open that bear on requirements: the §1.3 script/notebook count (affects how the pipeline decomposes into units) and D-144's two unfrozen sub-values, the coordinate-to-cell rule and the numerical coverage minimum. The coverage minimum in particular is a `TBD — supervisor freeze gate` that a G-P1A acceptance requirement would otherwise need to cite.
- 2026-08-17T00:00:00Z — The question file's Q5 enumerated nine TE section-11 NFRs; the document carries twelve (NFR-DQ-01 and NFR-TDEF-01 were omitted, and the practices artifacts under-cite them too). Adopted all twelve and recorded the under-enumeration as authority-chain defect 6. Worth checking whether the nine-item list has propagated elsewhere in the workflow.
- 2026-08-17T00:00:00Z — FR-P1-05-7, the confirmatory estimand itself, has no WS or TA row. TA-14 tests the bootstrap that carries it, not its definition. This is the most consequential of the eighteen untested requirements and is a candidate for a new TA row through Vision section 15.2 change control.
