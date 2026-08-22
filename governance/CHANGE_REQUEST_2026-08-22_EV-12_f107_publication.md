# Change Request — `CQ-2026-08-22-EV-12` — F10.7 publication-latency evidence

**Status: APPROVED 2026-08-22 AND APPLIED. Superseded by `CR-2026-08-22-EV-12`**
(`CHANGE_RECORD_2026-08-22_EV-12_f107_publication.md`), which carries the before/after
wording, the reason, the Bolt 5 evidence obligation and the synchronization list.

This file is retained unchanged below as the record of what was **proposed** and why,
so the proposal and the approved amendment stay separately auditable.

*As written when raised, and preserved:* "This is a **change request**, not a change record.
No document has been amended under it. The distinction is deliberate: every
`CHANGE_RECORD_*` file in this directory records an amendment already approved and applied;
this file records one proposed and pending."

*That was true when raised. The amendment was approved and applied later the same day; the
documents were amended under `CR-2026-08-22-EV-12`, not under this request.*

| Field | Value |
|---|---|
| **Request ID** | `CQ-2026-08-22-EV-12` |
| **Raised** | 2026-08-22 |
| **Raised by** | Governance re-review of AI-DLC stage 2.8 (`GOV-2026-08-22-DP-01`), on the project owner's instruction to raise it now rather than defer |
| **Decision owner** | Project decision owner, under the recorded student/supervisor authority equivalence |
| **Procedure** | Vision §15.2 change control |
| **Due gate** | **G-04 (Feature freeze)** — but see § Pre-G-04 dependency: dependent work starts earlier |
| **Documents that would be amended** | `PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` — the **EV-12** row and **§7.0A stage 4**; `aidlc/.../application-design/components.md` — the `availability.py` responsibility line |

---

## 1. Exact current wording

**EV-12, TE evidence register** (table columns: ID · Evidence obligation · Decision already
fixed · Required evidence · Must be frozen before):

> | EV-12 | External-feature publication latency | Q-16 Option A | Provider release documentation; 2022 availability matrix; Hp60 availability | Feature freeze |

**TE §7.0A stage 4**, the stage that builds the matrix:

> "Build the space-weather availability matrix with observation and publication timestamps."

**`components.md`**, `availability.py` responsibility:

> "The availability matrix: observation timestamp, publication timestamp, release status and
> safe lag per feature. Asserts actual lag ≥ declared safe lag."

**Not in conflict, and deliberately left alone.** F10.7's own §6.2 dictionary rows
(`f107_safe`, `f107_81_trailing`) record provenance as *"Approved source"* and demand no
publication timestamp — unlike `kp_safe` / `ap_safe`, whose row explicitly requires
*"observation + publication timestamps"*. **This request does not touch the §6.2 feature
contract.**

## 2. Proposed amendment

**EV-12 — proposed replacement row:**

> | EV-12 | External-feature publication latency | Q-16 Option A | Provider release documentation **where the provider supplies it**; 2022 availability matrix; Hp60 availability. **Where a provider archive carries no publication timestamp, the matrix records instead (a) the approved conservative availability convention frozen for that series, (b) the documented absence of a provider publication timestamp, and (c) an explicit statement that actual publication latency is unverified. For F10.7 this is D-25.** | Feature freeze |

**TE §7.0A stage 4 — proposed replacement sentence:**

> "Build the space-weather availability matrix with observation and publication timestamps
> **where the provider supplies them; for a series whose archive carries no publication
> timestamp, record the approved conservative availability convention and the documented
> absence in their place, and mark the series' publication latency unverified.**"

**`components.md` — proposed replacement responsibility:**

> "The availability matrix: observation timestamp, publication timestamp **or the approved
> conservative availability convention where the provider supplies no publication
> timestamp**, release status and safe lag per feature. Asserts actual lag ≥ declared safe
> lag."

## 3. Why the amendment is needed

**The obligation cannot be met for F10.7 with the data the project holds, and no amount of
implementation effort changes that.** The held archive
`evidence/audit_ec1_2026-08-15/nrcan_f107/fluxtable.txt` carries exactly seven columns —
`fluxdate`, `fluxtime`, `fluxjulian`, `fluxcarrington`, `fluxobsflux`, `fluxadjflux`,
`fluxursi`. There is **no publication timestamp, and no qualifier, revision or provenance
column**. `EC1-AUDIT.md` records the same limitation independently.

So EV-12's "Provider release documentation" would have to come from NRCan directly
(EC1-R-4). The owner has ruled that **project progress does not block on obtaining an NRCan
response**, and approved a conservative convention instead (**D-25**): a daily F10.7 median
becomes available no earlier than `00:00 UTC` on the following day.

Without this amendment the project is in a stable contradiction: an approved decision
(D-25) satisfies the scientific need, while an unamended evidence obligation (EV-12)
demands a document that does not exist and may not be obtainable. **EV-12's F10.7 limb
stands unmet at G-04 until this is resolved**, and leaving it unmet silently is the failure
mode this project has already corrected twice.

**What the amendment does not do.** It does not weaken the leakage protection. D-25's
convention is **strictly more conservative** than the observation-completion rule it
supplements: measured observation completion is 22 UT on 120 days and 23 UT on 245 days of
2022, and the convention delays availability past that by 1–2 hours in every case, with
`median(D)` never available at any origin on day *D*. It also does not permit an
unevidenced claim — it *requires* the absence and the unverified status to be recorded in
the matrix, where a reviewer will see them.

## 4. What it affects

| Affected | Effect |
|---|---|
| **EV-12** | Evidence definition widened to admit a declared convention where no provider timestamp exists |
| **TE §7.0A stage 4** | The matrix-building stage gains the same carve-out |
| **`components.md` → `availability.py`** | Design responsibility restated to match |
| **D-25** | Becomes sufficient for EV-12's F10.7 limb. Unchanged in substance either way |
| **Bolt 5 (`external-products`)** | Builds the availability matrix — **the dependent work**, see §5 |
| **Bolt 7 (`features-and-splits`)** | Consumes the matrix; `availability.py` asserts actual lag ≥ declared safe lag. Unaffected in mechanism |
| **FR-P1-04-2 / WS-11 / TA-08** | **Unaffected.** The lag assertion and the trailing-mean anchor check are untouched; this concerns what the matrix records about *publication*, not what it asserts about *lag* |
| **G-04** | Its EV-12 input becomes satisfiable for F10.7 |
| **Acceptance criteria** | **None added, removed or reworded.** No WS or TA row changes |
| **Frozen decisions** | **None changed.** D-10.3, D-21, D-22, D-23, D-25 all stand as written |

## 5. Pre-G-04 dependency — this is why it is raised now

**Yes, work before G-04 depends on the amended wording.**

EV-12 is due at Feature freeze, but the artifact it governs is **built earlier**: the
availability matrix is produced by `scripts/04_build_external_products.py`, owned by
**Bolt 5 (`external-products`)**, and consumed by **Bolt 7**. Under the current wording,
Bolt 5 must write a publication timestamp into the F10.7 row that it does not have and
cannot obtain. Under the amendment it writes the convention plus the documented absence.

**The implementer would otherwise face exactly the situation §18.3 forbids** — an
unresolved field with no sanctioned way to fill it, where the binding instruction is to
*"stop and report rather than choose a default."* Raising this at G-04 would mean Bolt 5
either stops, or fills a publication timestamp by convenience, which is prohibited.

**Sufficient evidence exists to decide now:** the file's column inventory is verified, the
convention is frozen under D-25, and the measured observation-completion distribution is
derived. Nothing further is expected to arrive before Bolt 5 starts.

## 6. Verification performed

- EV-12 row and §7.0A stage 4 sentence read verbatim from TE v3.4 and quoted above.
- `fluxtable.txt` column inventory: **7 columns**, enumerated; no publication, qualifier,
  revision or provenance field.
- F10.7's §6.2 dictionary rows checked and confirmed **not** to demand a publication
  timestamp, unlike the `kp_safe` / `ap_safe` row — so the conflict is scoped to the
  matrix-level and evidence-register obligations.
- D-25's convention confirmed strictly more conservative than observation completion
  (22 UT on 120 days, 23 UT on 245 days of 2022).

**No test was executed for this request.** The three existing test modules were not run —
see `evidence/experiment_registry.md` § "Evidence gap" for why.

## 7. Decision required

**Approve / Reject / Modify / Postpone** the amendment in §2.

- **Approve** → the three documents are amended under a change record, and Bolt 5 has a
  sanctioned instruction for the F10.7 row.
- **Reject** → EV-12 stands as written; F10.7's limb remains unmet, and Bolt 5 must stop
  and report on reaching the F10.7 row rather than fill it.
- **Modify** → alternative wording.
- **Postpone to G-04** → accepted only with the consequence stated: Bolt 5 cannot complete
  the F10.7 row of the availability matrix before the decision, so either Bolt 5 waits or
  the matrix ships incomplete on that row.

**Outcome: APPROVED by the project decision owner, 2026-08-22, and applied the same day under `CR-2026-08-22-EV-12`.** The text above is preserved as written at the time of the request.
