# NFR Design Questions — `regimes-diagnostics-reporting`

**Unit** `regimes-diagnostics-reporting` (Bolt 11) · **Kind** `library` · **Stage** `nfr-design`

Construction-stage questions are exceptional. The scientific values (regime thresholds,
event window, D-13 threshold, D-28 scored window) are frozen and merely encoded; the
underdetermined items already routed to gates (coverage notebook's home, §15.2 row
proposals, exploratory label's writer) stay routed — no question below re-asks one. Two
engineering gaps that `nfr-requirements` raised and did not resolve are this stage's to
design. Per `produces_kinds`, this `library` unit gets `security-design.md` and
`logical-components.md`.

## Question 1

`nfr-requirements` § Assumptions raises, unresolved: **"which locations count as
thesis-level is not fixed anywhere, and a location added later is not automatically
inspected."** The claims checklist (R-126, W-4) performs presence checks at *named*
locations, and Q2 = A extended it to citation checks — but the location list itself has no
owner. How does the checklist's location enumeration stay complete?

A) The registered conclusion surface IS the enumeration — W-4 already registers a
   `ConclusionSurfaceArtifact` as the checked text's declared subject (fail-closed when
   absent). Extend it: a location is thesis-level **iff registered there**, the checklist
   inspects exactly the registered set, and producing a conclusion-bearing artifact
   without registering it is itself a refusal at the producing path (the same
   emit-from-the-producing-path pattern R-110/R-60 use everywhere else).
   > **Impact**: One enumeration, owned by an artifact that already exists in the design and is already fail-closed. A location added later must register to be rendered at all, so the checklist's scope grows with the surface automatically. Residual stated honestly: text written entirely outside the pipeline (hand-authored thesis prose) still escapes — the registry bounds what the pipeline produces, not what a human types elsewhere. That residual already exists in Q2 = A's prose-check weakness and is not widened.

B) A hardcoded location list in `configs/experiment.yaml`, maintained by hand.
   > **Impact**: Simple, but the list is exactly the thing that goes stale — a new notebook or report section silently escapes until someone remembers to add it. Puts a maintenance obligation where the raised assumption says maintenance fails.

C) Convention-based discovery — the checklist globs known output directories
   (`artifacts/`, `notebooks/`) and inspects everything found.
   > **Impact**: No registration step, but "known directories" is a hardcoded list one level up, and a conclusion-bearing artifact written elsewhere escapes silently. Also inspects non-conclusion artifacts, generating noise findings that train readers to ignore the checklist.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it converts the unowned location list into a property of an artifact the design already registers fail-closed, using the emit-from-the-producing-path pattern this unit applies to every other obligation. B and C both reintroduce the exact staleness the assumption raises.

[Answer]: A

## Question 2

§ SEC-R-02's two consumer refusals (estimand orientation/weighting; lineage caveat) and
§ SEC-R-01's refusals (units check, missing-member, D-17 bound) need a home in the
rendering path — `nfr-requirements` records "where the refusal sits in the rendering path
is owed at 3.5", but the *shape* is a design choice. Sibling units just settled the same
question with a single guard module plus per-entry negative controls. Where do this unit's
rendering refusals live?

A) One render-guard set at the table/breakdown producing boundary — a single local guard
   component in this unit's reporting module owns all rendering refusals (field presence,
   units, lineage caveat, D-17 bound, missing member); every producing path (primary
   table W-3, breakdown family W-5, plots manifest W-7) calls it before emitting; one
   negative control per producing path proves an unguarded emission raises. Cross-cutting
   metric-entry checks stay the sibling's shared guard module — this set guards
   *rendering*, a boundary the sibling's module does not own.
   > **Impact**: Mirrors the settled sibling pattern (single copy + per-entry controls) at the one boundary this unit owns. Clean split: metric entry = shared module (evaluation-and-comparison), rendering = this unit's guard set. Cost: one more guard component, and the split line (metric vs rendering) must be stated so no check is homeless or double-owned.

B) Refusals inline in each producing function (table, breakdowns, plots, checklist).
   > **Impact**: No new component, but four copies of the field-presence and units checks that drift independently — the exact mechanism behind the R-105-vs-R-92 divergence and this project's most-repeated defect class.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — the drift risk of B is not hypothetical in this project, and A's boundary split (metric-entry checks shared and sibling-owned; rendering checks local and this-unit-owned) gives every refusal exactly one home. The homeless-check risk A carries is addressed by stating the split explicitly in `logical-components.md`.

[Answer]: A

## Consolidated Summary Confirmation

Does this all look correct before I generate the artifact?

- Looks correct
- Request changes

[Answer]: Looks correct
