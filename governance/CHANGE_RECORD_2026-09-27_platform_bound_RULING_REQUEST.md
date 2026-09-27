# RULING REQUEST — consolidated platform bound (GitHub Actions, locked-root materialisation, retrieval hosts)

**Status: DRAFT awaiting Student + Supervisor signature. Nothing below is in
force until signed; the interim executed steps are listed in § 4 and stand on
their own approvals.**

**Origin:** GOV-2026-09-27-BT-02 Recommendations 2, 3 (durable half) and 18,
approved by the Student 2026-09-27 for drafting and routing. The Rec 47 bound
annotation in `.github/workflows/verify.yml` records this change record as OWED
(Student + Supervisor, due G-07); the recurring December materialisation argues
for G-05. This draft consolidates the three open platform questions into ONE
ruling so TC-03c's actual boundary is stated once.

## 1. The question

TC-03c / TE §9.1 authorise **exactly two execution platforms** (Kaggle, local).
Three surfaces now exist that are neither, each with different properties:

| Surface | What it does | Current state |
|---|---|---|
| GitHub Actions runners | Execute the verification suite on push; `actions/checkout` materialises the 29 tracked files of `evidence/locked_test_restricted/` | Live (49+ runs); restricted-reader modules deselected 2026-09-27; authorization record owed |
| The Student's internet-connected retrieval host | Human-operated provider retrieval (the GIM bundle `evidence/gim_code_final_2022/`, 367 files, full DATA-07-shaped provenance, December bytes acquired-never-opened) | Un-ruled; feeds a governed release |
| Any unrecognised environment | Previously inherited `local` silently from `resolve_platform_roots`'s else-branch | Refused as of 2026-09-27 (R3 code fix) when `GITHUB_ACTIONS`/`CI` markers present; the durable fix is § 3.3 |

## 2. Proposed ruling (for signature)

1. **GitHub Actions is an authorised NON-SCIENTIFIC verification surface**,
   bound exactly as the Rec 47 annotation states: nothing it does is evidence
   for any TEC gate, WS/TA row, or claim; it may not produce, hash, or attest a
   governed artifact (structural guard enforces); a green run is never §18.3,
   TC-03g, or G-07 evidence; a red run is a mandatory-triage signal.
2. **CI never reads the locked December root.** The restricted-reader modules
   stay deselected from every CI pytest invocation. The remaining
   materialisation question — `actions/checkout` still copies the tracked
   restricted files onto the runner — is decided here as ONE of:
   - (a) accept materialisation under the bound (bytes copied, never read;
     mutation still visible in git), OR
   - (b) un-track `evidence/locked_test_restricted/` from the public remote
     (interacts with the G-09 history-immutability question; weakens the
     git-visibility mutation control), OR
   - (c) make the repository private / restrict Actions.
   The 2026-09-27 board recommended deciding (a) vs (b) explicitly rather than
   letting the default persist silently; it did not pick one — both are
   genuinely valid and trade governance properties.
3. **Fail-closed platform resolution is the durable rule** (R3 option 2, put to
   the owner here): `resolve_platform_roots` refuses any environment it cannot
   positively identify — CI markers already refuse (code, 2026-09-27); this
   ruling decides whether to go further and require an explicit `TEC_PLATFORM`
   on every host (breaking change: every local invocation must set it once).
4. **Human-operated provider retrieval is data acquisition, not pipeline
   execution** (R18): a retrieval host is authorised per-acquisition when the
   retrieval is Student-operated and records full DATA-07-shaped provenance
   (verbatim provider filenames with version suffixes, URLs, UTC retrieval
   dates, SHA-256, and — for December-bearing bundles — the acquired-never-
   opened discipline with its checklist). The GIM bundle retrieval of
   2026-09-26 is ratified retroactively under this clause.
5. **CI-runner access records** (the residual GOV-2026-09-24's exposure ruling
   did not reach): with clause 2 in force no CI December read exists to record;
   if clause 2 is ever relaxed, every runner read must land in a durable log
   (artifact upload or equivalent) before the job ends — ephemeral sidecar rows
   destroyed with the runner are not records (Vision §8.3; FR-P1-02-3).

## 3. team.md correction (drafted for the §13 learnings ritual — the ONLY sanctioned write path; NOT applied here)

> ALWAYS treat CI (GitHub Actions `verify.yml`) as an advisory, non-governed
> verification surface, never a governed platform and never gate evidence.
> team.md § Testing Posture's "No CI service is used" (Q7=D) was true when
> affirmed and is superseded on the tree since 2026-09-25: the workflow is
> live under the Rec 47 bound. Governed evidence remains local + in-Kaggle
> (TC-03c, TC-03g). A CI failure is a mandatory-triage signal; a CI pass
> satisfies no obligation. (learned 2026-09-27)

## 4. Interim steps already executed (stand on the Student's 2026-09-27 approval of GOV-2026-09-27-BT-02)

- Restricted-reader modules deselected from `verify.yml` (R2 immediate step).
- `resolve_platform_roots` refuses CI-marked environments; `verify.yml`
  declares `TEC_PLATFORM: local` explicitly under the bound (R3 immediate step).
- Rec 47 relabelled two-limb in the stage artifacts (R2).

## 5. Signature block

| Role | Name | Decision (clause 2: a/b/c; clause 3: markers-only / explicit-everywhere) | Date | Signature |
|---|---|---|---|---|
| Student | Kimia Rezaei | | | |
| Supervisor | Dr. Reza Saraf Shirazi | | | |
