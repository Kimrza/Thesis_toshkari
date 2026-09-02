# NFR Requirements — Questions — `models-and-baselines`

**Unit** `models-and-baselines` (Bolt 8) · **Kind** `library` · **Stage** `nfr-requirements`

Two artifacts only — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit.

**Not re-asked, because `functional-design` already decided them.** The stamp match before
every scoring path (R-90, W-1); the **three-seed mean** as the confirmatory prediction with
nothing substitutable for it (R-91, W-3); a confirmatory mean whose inputs disagree on
provenance **failing** (R-92); the seed **never selected**, and never on December (R-93);
M-06 restoring its **lowest-validation-RMSE checkpoint**, not its last epoch (R-94, W-4);
tuning reading **January–November only** with its **three mechanisms** (R-95, W-5, Q3 = D);
**grid content asserted, not only immutability** — ridge 6, RF 18, LSTM 16 (D-121) and the
seven fixed LSTM settings (R-96, W-6); ablations **predeclared, five named, four reachable in
Phase 1** (R-97, W-7); M-03 fitted on **training partitions only** (R-98, W-9); the **+24 h
horizon needing no code change** (R-99, W-8); **RF importance diagnostic and never a
selection input** (R-100); selection on **mean per-fold skill score** with the refit changing
no hyperparameter (R-101); the **model set closed, with two absences as evidence** (R-102);
`06` writing the **prediction-hash receipt** and refusing to exit without it (R-102a, W-12).

**Carried, not decided here.** Two evidence obligations belong to siblings (W-10).
**`PartitionError` is declared in `src/data/config.py`**, not `src/models/` — this unit is the
**semantic owner** but not the declaration site.

---

## Question 1

This unit's own derivation, printed in `functional-design`: **9 requirements, 7 with no §16
or §19 acceptance row.** That is FR-P1-04-14, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5,
FR-P1-05-6, FR-P1-05-21 and FR-P1-05-22 — **the largest untested share of any unit in this
project.**

Several are rules the project lists under `## Forbidden` or `## Mandated`: RF importance never
a selection input; tuning never informed by December; grids exact and committed before G-05;
ablations predeclared; M-03 fitted on training partitions only.

`features-and-splits` faced the same shape for one requirement and answered it: **the negative
control is required regardless of §19, and the missing row is proposed to the gate.**

What should this unit's artifacts require, at seven?

A. Apply the same rule at scale — **every one of the seven gets its negative control**, required by the affirmed every-hard-rule-gets-a-test practice, and **all seven missing rows are proposed to the gate** as one Vision §15.2 request
   > **Impact**: Consistent with the answer already given for `features-and-splits`, and it puts the project's largest evidence gap in front of the owner as a single decision rather than seven scattered ones. It is a substantial ask: seven rows at once, and seven controls to write for a unit whose tests do not exist yet.

B. Require the controls, and propose rows **only for the subset that maps to a `## Forbidden` or `## Mandated` rule**
   > **Impact**: Puts the smaller, better-justified request to the owner and keeps the rest as recorded gaps. Drawing that subset is a judgement this stage would be making about which project rules deserve gate evidence, and the requirements left out stay untested with no route to a row.

C. Record the seven as an acceptance-coverage gap owned outside this unit, and require no new controls here
   > **Impact**: Accurate about ownership — §19's composition is not this unit's to change — and adds nothing unbudgeted. It leaves seven requirements, several of them hard rules, with neither a test nor a route to one, which is the posture `GOV-F-06` warned against.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the same question was answered this way one unit ago, and answering it differently here because the number is larger would make the rule depend on how expensive it is to follow. Presenting seven rows as one §15.2 request is also the honest shape: they are one gap, not seven. D-32's precedent — eight rows approved in a single decision — shows the route carries that volume.

[Answer]: A

---

## Question 2

R-95's mechanism 3 reads `governance-guards` R-25's durable access log and requires a tuning
run whose record post-dates a December coverage-audit access to **state it**. The design is
explicit about what that achieves:

> *"A choice informed by a December **figure a human carries in their head** leaves no trace in
> any of the three. Mechanism 3 makes the overlap **visible for review**; it does not eliminate
> it, and no mechanism can."*

So the mechanism currently **flags** an overlap. It does not stop the run.

What should `security-requirements.md` require when a tuning run falls inside that window?

A. **Flag and record** — the run proceeds, states the overlap in its `TuningRecord`, and the overlap is a required input to the G-05 review
   > **Impact**: Matches what the design already says the mechanism does, and keeps the evidence where a reviewer will meet it. The run that may have been informed by December still happens and its outputs still enter selection; the control is entirely retrospective.

B. **Block pending attestation** — a tuning run inside the window does not proceed until a human attests, on the record, that no December figure informed the criterion
   > **Impact**: Converts a retrospective flag into a gate at the moment the risk is live, and creates a dated human statement that G-05 can rest on. It puts a person in the loop on what may be a routine sequence, and an attestation about one's own knowledge is the weakest kind of evidence — though it is the only kind available for a figure held in someone's head.

C. **Forbid the sequence** — no tuning run may post-date a December audit access within the same freeze cycle
   > **Impact**: Eliminates the channel outright rather than observing it. The pre-G-05 December coverage audit is **required** and its timing is not this unit's to control, so this could make a mandatory audit block a mandatory tuning run — the two obligations would collide with no rule to resolve them.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option B — the residual is the one channel the project cannot close mechanically, and an attestation at the moment of exposure is worth more than a flag read weeks later at G-05, because the person still remembers what they knew. Its weakness should be stated plainly in the artifact rather than glossed: a self-attestation about one's own knowledge proves nothing on its own; what it buys is a dated, named record that a specific person considered the question at the time. Option C is the one to avoid — it would set a required audit against a required tuning run.

[Answer]: B

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope.** Two artifacts — `security-requirements.md` and `tech-stack-decisions.md`;
`produces_kinds` excludes the other three for a `library` unit. Those categories are still
assessed in the security artifact's scope note.

**Q1 = A — all seven untested requirements get negative controls, and all seven missing rows
are proposed as one §15.2 request.** This unit's own derivation is **9 requirements, 7 with no
§16 or §19 acceptance row** — FR-P1-04-14, FR-P1-05-3, FR-P1-05-4, FR-P1-05-5, FR-P1-05-6,
FR-P1-05-21, FR-P1-05-22 — **the largest untested share of any unit in this project**. Each
gets a control proving the violation is caught, required by the affirmed practice
**independently of §19**. The seven missing rows go to the gate as **one** request, because
they are one gap rather than seven. **This stage proposes; it does not approve.** D-32's
approval of eight rows in a single decision is cited as precedent for the **route**, not as
approval of these.

**Q2 = B — a tuning run inside the December-audit window blocks pending human attestation.**
R-95 mechanism 3 currently **flags** a tuning run whose record post-dates a December
coverage-audit access. It will now **block** until a human attests, on the record, that no
December figure informed the criterion. **The weakness is stated, not glossed:** a
self-attestation about one's own knowledge **proves nothing on its own** — what it buys is a
**dated, named record that a specific person considered the question at the time**, which is
worth more than a flag read weeks later at G-05 because the person still remembers what they
knew. **No mechanism can eliminate this residual**, and none is claimed to.

**The sequence is not forbidden.** The pre-G-05 December coverage and regime audit is
**required** and its timing is not this unit's to control; forbidding the sequence would set a
mandatory audit against a mandatory tuning run.

**Carried, not re-decided.** R-90's stamp match; R-91's three-seed mean with nothing
substitutable; R-92's provenance-disagreement failure; R-93's never-selected seed; R-94's
lowest-validation-RMSE checkpoint restore; R-95's three mechanisms and the stated join to
`governance-guards` R-25's log; R-96's asserted grid **content** — ridge 6, RF 18, LSTM 16
(D-121) and the seven fixed LSTM settings; R-97's five predeclared ablations, four reachable
in Phase 1; R-98's training-partitions-only M-03; R-99's config-only +24 h horizon; R-100's
**diagnostic-only RF importance**; R-101's mean per-fold skill selection with a
hyperparameter-preserving refit; R-102's closed model set with **two absences as evidence**;
R-102a's prediction-hash receipt and `06`'s refusal to exit without it.

**Status claims made.** None. WS-14, WS-15, TA-12, TA-13, TA-26 are **owned and undischarged**;
TA-20 is supported. **`PartitionError` is declared in `src/data/config.py`**, not `src/models/`
— this unit is the **semantic owner but not the declaration site**. Two evidence obligations
belong to siblings (W-10). G-09 is signed (D-31) with preconditions UNMET; stage 3.1 remains
FAIL; `configs/` does not exist; **no Python interpreter exists here**, so every test is
written-but-unexecuted or unwritten and **no model has ever been trained**.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
