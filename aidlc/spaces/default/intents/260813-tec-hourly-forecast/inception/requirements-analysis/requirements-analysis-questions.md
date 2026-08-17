# Requirements Analysis — Questions

Stage 2.3 (requirements-analysis), intent `260813-tec-hourly-forecast`.
Depth: Comprehensive.

These questions do **not** re-ask what Vision v4.2 or Technical Environment v3.2
already fix. The research question, estimand, feature contract, lag rules,
evaluation protocol, claim boundary and NFRs are settled and traceable; asking
again would breach the inception traceability rule. What follows targets what
those documents leave open, leave un-decomposed, or leave to you.

Answer each by filling the `[Answer]:` tag with the option letter.

---

## Q1 — What the requirements artifact is for

`user-stories` (2.4) is SKIP in this scope, so §16's WS-09–WS-20 and §19's
TA-01–TA-32 rows are the only acceptance vocabulary Construction will inherit.

- A. Write `requirements.md` as a decomposition layer: each requirement carries a stable ID, a pass/fail criterion, and an explicit link to the WS or TA row that tests it. Requirements with no testing row are flagged rather than invented.
- B. Write it as a restatement of the Vision and TE requirements in one place, without adding the WS/TA mapping (that mapping happens at functional-design).
- C. Write it as a thin index pointing into Vision and TE by section, with no restated content.
- X. Other (please specify)

[Answer]: A

---

## Q2 — Decomposition unit

Technical Environment §7.0 describes Phase 1 as stages P1-00 through P1-06, and
§12/§14/§19 describe nine stage scripts and five notebooks.

- A. Decompose requirements by the P1-00..P1-06 stage table — acquisition, alignment, target build, feature build, splits, model, evaluation — so requirements map onto the pipeline's own stages.
- B. Decompose by the six `src/` packages instead, so requirements map onto the code structure that Construction will build.
- C. Decompose by the six completeness dimensions (functional, non-functional, user scenarios, business context, technical context, quality attributes) and cross-reference the pipeline stages.
- X. Other (please specify)

[Answer]: A

---

## Q3 — The unfrozen coverage minimum

Vision §6.1B's numerical minimum for acceptable coverage is `TBD — supervisor
freeze gate` and is one of the two values D-144's approval was meant to freeze.
A G-P1A acceptance requirement would normally cite it.

- A. Write the requirement with the threshold as an explicit named hole (`REQ cites Vision §6.1B, value pending supervisor freeze`), so the requirement is complete in form and blocked in value.
- B. Write the requirement against D-2's existing interim rule (≥95% of calendar days per month, 100% of December) and note that it is superseded once the supervisor freezes §6.1B.
- C. Omit any coverage-acceptance requirement until the value is frozen.
- X. Other (please specify)

[Answer]: X — i have my supervisors approval do not ask again

---

## Q4 — Requirements for work that is currently blocked

FU-1=B sequences the `raw_isprint_cache/` re-acquisition after this stage, and
DATA-03/DATA-04 remain open (no client version pin; no provider bytes anywhere).

- A. Write requirements for the re-acquisition now, including the provider-version-suffix recording obligation, so the deferred work has a specification when it runs.
- B. Record the re-acquisition as an out-of-scope item for this requirements pass, to be specified when it is unblocked.
- C. Write requirements now and additionally specify the acceptance evidence that will close DATA-03 and DATA-04.
- X. Other (please specify)

[Answer]: C

---

## Q5 — Non-functional requirements

Technical Environment §11 already carries NFR-IRI-01, NFR-LEAK-01, NFR-FAIR-01,
NFR-REP-01, NFR-DET-01, NFR-PHASE-01, NFR-SEC-01, NFR-LIC-01 and NFR-AUD-01.

- A. Adopt the §11 NFRs by reference with their existing IDs, adding only a pass/fail criterion and test mapping for each. Do not renumber or restate.
- B. Restate them in `requirements.md` with project-local IDs, cross-referenced to the §11 IDs.
- C. Adopt by reference and additionally add NFRs the §11 set does not cover, if any are found.
- X. Other (please specify)

[Answer]: C

---

## Q6 — Out-of-scope boundary

Vision §3.5 places operations, real-time ingestion, monitoring and service
deployment under Future. D-8 bounds claims to three cells, 2022, December test.
Phase 2 raw GNSS processing is barred from Phase 1 by §7.0.

- A. State the out-of-scope boundary as three explicit lists — Future (Vision §3.5), Phase 2 (§7.0 prohibition), and out-of-claim (D-8) — since they are excluded for three different reasons and conflating them would hide why.
- B. State it as one consolidated out-of-scope list.
- C. State it as A, and additionally list the specific things a reader might expect but will not get (5-minute resolution at NICO per D-7, receiver-specific station VTEC per §6.6).
- X. Other (please specify)

[Answer]: C

---

## Q7 — Requirements traceability format

`phases/inception.md` requires every requirement to trace back to an ideation
artifact and forbids introducing untraced requirements.

- A. Each requirement carries an inline source tag naming its authority (`[Vision §6.2]`, `[TE §13.6]`, `[D-10.3]`, `[TC-19]`), matching the source-register convention already used in this workflow's ideation artifacts.
- B. A separate traceability table at the end of the document mapping requirement ID to source.
- C. Both — inline tags for reading, and a table for auditing.
- X. Other (please specify)

[Answer]: C

---

## Q8 — How much of the governance state to carry

This workflow has accumulated substantial governance state: 58 affirmed hard
rules, open supervisor items 3 and 4, the D-11 fixture freeze, and the interim
caveat on `audit_evidence_2022-FULL/`.

- A. `requirements.md` carries only what constrains the requirements themselves, and cross-references `discovered-rules.md`, `team-practices.md` and the correction record for the rest.
- B. `requirements.md` restates all binding constraints inline so it is readable standalone.
- C. As A, plus an explicit "constraints inherited, not restated" section naming where each lives.
- X. Other (please specify)

[Answer]: C

---

## Q9 — Success metrics

Vision §5 defines the success layers and §2.4 the comparison hierarchy with its
three mandatory difficulty controls.

- A. Adopt Vision's success framework by reference; state in `requirements.md` only the measurable acceptance criteria that Construction must satisfy, not the scientific success criteria the thesis is judged on.
- B. Restate both the scientific success framework and the engineering acceptance criteria.
- C. As A, and explicitly record that engineering acceptance (does the pipeline run correctly) is independent of scientific outcome (does the model beat the baselines) — a correctly executed negative result passes engineering acceptance.
- X. Other (please specify)

[Answer]: C

---

## Q10 — Anything the authority documents get wrong or leave dangerous

The governance board found several defects in the authority chain: the §16/§16.1
contradiction, §1.3's stale counts, OC-03's over-broad wording, and Vision §14.2
D-130's supersession pointers that carry no counts.

- A. `requirements.md` records each known authority-document defect it relies on, with the reading adopted and its status, so a later reader is not misled by the source.
- B. Keep authority-document defects out of `requirements.md`; they live in `evidence.md` and the governance records.
- C. As A, but only for defects that materially affect a requirement written here.
- X. Other (please specify)

[Answer]: A

---

## Consolidated Summary Confirmation

Answers as recorded:

- **Q1 = A** — `requirements.md` is a decomposition layer: every requirement gets a stable ID, a pass/fail criterion, and an explicit link to the WS or TA row that tests it. A requirement with no testing row is flagged, never invented.
- **Q2 = A** — Decomposition follows the Technical Environment §7.0 stage table P1-00..P1-06 (acquisition, alignment, target build, feature build, splits, model, evaluation), so requirements map onto the pipeline's own stages.
- **Q3 = X** — Verbatim: `i have my supervisors approval do not ask again`. **Reading adopted, and not re-asked:** the student states supervisor approval is held, so the G-P1A coverage-acceptance requirement is written rather than omitted (Q3-C rejected). No numeric value was supplied with that approval, and `project.md` § Forbidden bars any agent from filling a `TBD — freeze gate` value by convenience, so the requirement is written in Q3-A form — an explicit named hole citing Vision §6.1B — and operates on D-2's existing interim rule (≥95% of calendar days per month, 100% of December) until the frozen number is recorded under its own D-number in `evidence/DECISIONS.md`. Recording that D-number is the student's action, not this stage's.
- **Q4 = C** — Requirements for the deferred `raw_isprint_cache/` re-acquisition are written now, including the provider-file-version-suffix recording obligation, **plus** the acceptance evidence that closes DATA-03 (client version pin) and DATA-04 (no provider bytes).
- **Q5 = C** — The Technical Environment §11 NFRs (NFR-IRI-01, NFR-LEAK-01, NFR-FAIR-01, NFR-REP-01, NFR-DET-01, NFR-PHASE-01, NFR-SEC-01, NFR-LIC-01, NFR-AUD-01) are adopted by reference with their existing IDs — not renumbered, not restated — each gaining a pass/fail criterion and test mapping, **plus** any NFR the §11 set does not cover is added.
- **Q6 = C** — Three separate out-of-scope lists (Future per Vision §3.5; Phase 2 per the §7.0 prohibition; out-of-claim per D-8), **plus** an explicit list of things a reader might expect but will not get: 5-minute resolution at NICO (D-7) and receiver-specific station VTEC (§6.6).
- **Q7 = C** — Both traceability forms: inline source tags on each requirement (`[Vision §6.2]`, `[TE §13.6]`, `[D-10.3]`, `[TC-19]`) and a traceability table at the end for auditing.
- **Q8 = C** — `requirements.md` carries only what constrains the requirements themselves and cross-references `discovered-rules.md`, `team-practices.md` and the correction record for the rest, **plus** an explicit "constraints inherited, not restated" section naming where each lives.
- **Q9 = C** — Vision's success framework is adopted by reference; only the measurable engineering acceptance criteria are stated here, **plus** an explicit record that engineering acceptance (does the pipeline run correctly) is independent of scientific outcome (does the model beat the baselines) — a correctly executed negative result passes engineering acceptance.
- **Q10 = A** — Every known authority-document defect that `requirements.md` relies on is recorded with the reading adopted and its status: the §16/§16.1 contradiction, §1.3's stale script/notebook counts, OC-03's over-broad "unexamined" wording, and Vision §14.2 D-130's supersession pointers that carry no counts.

Does this all look correct before I generate the requirements artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
