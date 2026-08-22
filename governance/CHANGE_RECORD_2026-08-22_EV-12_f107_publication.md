# Change Record — `CR-2026-08-22-EV-12`

**Vision §15.2 change-control record. APPROVED AND APPLIED 2026-08-22.**

Supersedes change request `CQ-2026-08-22-EV-12`
(`CHANGE_REQUEST_2026-08-22_EV-12_f107_publication.md`), which is retained as the
record of what was proposed and why.

| Field | Value |
|---|---|
| **Change record ID** | `CR-2026-08-22-EV-12` |
| **Date approved and applied** | 2026-08-22 |
| **Approved by** | Project decision owner, expressly and in advance of application, under the recorded student/supervisor authority equivalence. No separate supervisor signature artifact exists and none is claimed |
| **Origin** | `GOV-2026-08-22-DP-01`; change request `CQ-2026-08-22-EV-12` |
| **Applied to** | TE **EV-12** row; TE **§7.0A stage 4**; `components.md` → `availability.py` |

---

## 1. Previous wording

**EV-12, verbatim before amendment:**

> | EV-12 | External-feature publication latency | Q-16 Option A | Provider release documentation; 2022 availability matrix; Hp60 availability | Feature freeze |

**TE §7.0A stage 4, the amended clause, verbatim before:**

> "Build the space-weather availability matrix with observation and publication timestamps."

**`components.md` → `availability.py`, verbatim before:**

> "The availability matrix: observation timestamp, publication timestamp, release status and
> safe lag per feature. Asserts actual lag ≥ declared safe lag."

## 2. Approved replacement wording

**EV-12, as now written:**

> | EV-12 | External-feature publication latency | Q-16 Option A | Provider release documentation **where the provider supplies it**; 2022 availability matrix; Hp60 availability. **Where a provider archive carries no publication timestamp, the matrix records instead (a) the approved conservative availability convention frozen for that series, (b) the documented absence of a provider publication timestamp, and (c) an explicit statement that actual publication latency is unverified. For F10.7 this is D-25.** | Feature freeze |

**TE §7.0A stage 4, as now written:**

> "Build the space-weather availability matrix with observation and publication timestamps
> **where the provider supplies them; for a series whose archive carries no publication
> timestamp, record the approved conservative availability convention and the documented
> absence in their place, and mark that series' publication latency unverified.**"

**`components.md` → `availability.py`, as now written:**

> "The availability matrix: observation timestamp, publication timestamp **or, where the
> provider supplies no publication timestamp, the approved conservative availability
> convention plus the documented absence and an unverified-latency statement** (amended
> 2026-08-22, `CR-2026-08-22-EV-12`; for F10.7 this is **D-25**), release status and safe
> lag per feature. Asserts actual lag ≥ declared safe lag."

## 3. Reason

The obligation could not be met for F10.7 with the data the project holds, and no
implementation effort would change that. `evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt`
carries exactly seven columns — `fluxdate`, `fluxtime`, `fluxjulian`, `fluxcarrington`,
`fluxobsflux`, `fluxadjflux`, `fluxursi` — with **no publication timestamp** and no
qualifier, revision or provenance column. `EC1-AUDIT.md` records the same limitation
independently.

EV-12's "Provider release documentation" would therefore have to come from NRCan directly
(EC1-R-4), and the owner ruled that project progress must not block on obtaining that
response, approving a conservative convention instead (**D-25**).

Without this amendment the project sat in a stable contradiction: an approved decision
satisfied the scientific need while an unamended evidence obligation demanded a document
that does not exist and may never be obtainable.

## 4. The affected Bolt 5 evidence obligation, stated exactly

**Bolt 5 (`external-products`) owns `scripts/04_build_external_products.py`, which builds
the availability matrix.** That is the artifact EV-12 governs, and it is built well before
G-04, where EV-12 falls due.

**Before this amendment**, Bolt 5 faced an unsatisfiable instruction on the F10.7 row: write
a publication timestamp it cannot obtain. Under TE §18.3 the binding response would have
been to *"stop and report rather than choose a default"* — so Bolt 5 would have halted, or
an implementer would have filled the field by convenience, which `project.md` § Forbidden
prohibits.

**After this amendment**, Bolt 5's F10.7 row of the availability matrix records three
things instead of a publication timestamp:

1. **The approved conservative availability convention** — D-25: a daily F10.7 median
   becomes available no earlier than `00:00 UTC` on the following day.
2. **The documented absence** of a provider publication timestamp in the held archive,
   with the seven-column inventory as its basis.
3. **An explicit statement that actual publication latency is unverified.**

**Bolt 5 is no longer forced to proceed with an incomplete row**, and no field is filled by
convenience.

## 5. Downstream artifacts requiring synchronization

| # | Artifact | Status |
|---|---|---|
| 1 | TE **EV-12** row | **Amended** |
| 2 | TE **§7.0A stage 4** | **Amended** |
| 3 | `components.md` → `availability.py` | **Amended** |
| 4 | `evidence/DECISIONS.md` **D-25** — its "minimum amendment requested — NOT applied" paragraph | **Synchronized** to record the grant |
| 5 | `bolt-plan.md` Bolt 5 Definition of Done | **Synchronized** — the three-part matrix instruction added |
| 6 | `external-dependency-map.md` — item 9 and the § B G-04 row | **Synchronized** — moved from "awaiting decision" to approved and applied |
| 7 | `CHANGE_REQUEST_2026-08-22_EV-12_f107_publication.md` | **Annotated** as approved and superseded by this record |

**Checked and requiring no change:** `FR-P1-04-2`, WS-11 and TA-08 — they govern *lag*
assertion and the trailing-mean anchor, not what the matrix records about *publication*.
`risk-and-sequencing-rationale.md` does not reference EV-12. The §6.2 feature dictionary is
untouched: F10.7's own rows record provenance as *"Approved source"* and never demanded a
publication timestamp, unlike the `kp_safe` / `ap_safe` row.

## 6. Scope discipline — what this amendment did NOT do

- **No unrelated requirement change.** Three loci amended, all named above.
- **No frozen scientific decision altered.** D-10.3's previous-day contract, the trailing
  81-day mean, the observed-not-adjusted flux choice, and D-21/D-22/D-23 all stand as
  written.
- **No leakage control weakened.** D-25 is **strictly more conservative** than the
  observation-completion rule it supplements: measured completion is 22 UT on 120 days and
  23 UT on 245 days of 2022, and the convention delays availability past that by 1–2 hours
  in every case, with `median(D)` never available at any origin on day *D*. The amendment
  additionally *requires* the absence and the unverified status to be recorded where a
  reviewer will see them.
- **No access to locked December data authorized.** This amendment concerns a solar-flux
  predictor archive held outside `evidence/locked_test_restricted/`. It grants no access of
  any kind and touches no December target value or performance quantity.
- **No acceptance criterion added, removed or reworded.** No WS or TA row changes.

## 7. Verification performed

- EV-12 and §7.0A stage 4 read verbatim from TE v3.4 before amendment and quoted in §1.
- Post-amendment greps confirm: the new EV-12 text present (1 match), the new §7.0A clause
  present (1 match), the superseded wording absent (0 matches).
- `fluxtable.txt` column inventory re-confirmed: 7 columns, no publication field.
- F10.7 §6.2 dictionary rows confirmed unchanged and outside the amendment's scope.

**No test was executed for this amendment.** Three test modules exist in `tests/`; none was
run — see `evidence/experiment_registry.md` § "Evidence gap" and the tracked obligation
**RES-04**.
