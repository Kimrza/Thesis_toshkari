# Runbook — CODE final GIM acquisition + Q-15 exploration (internet-connected system)

**Date:** 2026-09-26. **Operator: the Student**, on the internet-connected system. This
prepares the R-60 gate inputs; it generates NO comparator (the repo's
`gim.generate_comparator` refuses by design until Q-15 is frozen and the gates hold, and
the production path is then built in-repo as its own change).

## 1. Acquire — CODE final GIM, calendar 2022

- **Source: AIUB anonymous archive** (`http(s)://ftp.aiub.unibe.ch/CODE/2022/`) —
  preferred over CDDIS because it needs NO credentials, so nothing touches Earthdata
  auth. If CDDIS is used anyway: credentials via `.netrc`/environment only, never
  committed (NFR-SEC-01; the `.gitignore` deny-list already covers `.netrc`).
- Product: CODE FINAL global ionosphere maps (IONEX), all days of 2022. **Record every
  file's provider filename VERBATIM** — 2022 straddles the IGS switch from short names
  (`CODGddd0.22I.Z`) to long product names (`COD0OPSFIN_...INX.gz`); whichever the
  archive serves for a given day is the identity you record, never normalised.
- Per file, into a manifest (`sha256_manifest.json` beside the files, same shape the
  month-evidence dirs use): verbatim filename (with any version suffix), source URL,
  retrieval date (UTC), SHA-256 of the retrieved bytes. Provider version drift is an
  observed fact in this project (team.md § Walking Skeleton) — a later mismatch is only
  interpretable if today's identities are recorded.
- Suggested landing dir when brought back: `evidence/gim_code_final_2022/` (new; sits
  beside the month-evidence dirs; final home is the Student's call).

## 2. December discipline

Acquire the December files (bytes + hashes — completeness of the release), but **do not
open, parse, plot or summarise them during exploration**. The December-never-informs rule
triggers on December being SEEN; exploration below is January–November only. State this
in your session notes rather than leaving it implicit.

## 3. Q-15 exploration (informs the freeze; decides nothing by itself)

- Work OUTSIDE the repo, labeled exploratory.
- Compare candidate rules (see `Q15_DECISION_OPTIONS_2026-09-26_gim_interpolation.md`:
  nearest / bilinear+linear / bilinear on rotated maps) at ARUC, BSHM, NICO coordinates,
  January–November 2022.
- Allowed comparisons: rule-vs-rule differences, internal consistency, magnitude of the
  rotation correction. **Not allowed:** anything where model predictions or model-vs-GIM
  skill enters the loop (GIM is an evaluation-time comparator; TC-08 bars presuming
  independence before the overlap audit, and no performance signal may pick the rule).
- Output worth keeping: a one-page note of the measured rule-vs-rule differences — it
  becomes rationale inside the Q-15 D-number, not a decision by itself.

## 4. The two R-60 gate inputs to produce

1. **Hand-check**: ONE worked interpolation example, on paper/notebook — grid corner
   values quoted from a named IONEX file, the arithmetic shown to the final station
   value, under the rule you intend to freeze. This is the artifact the generation gate
   consumes; date it.
2. **Overlap audit input**: the CODE station list for 2022 (the IONEX header's
   contributing-stations info and/or CODE's published network list), retrieved and
   hashed — the input to the `gim_network_overlap_flag` audit against ARUC/BSHM/NICO,
   whose result must be DISCLOSED once the audit runs (mandated; no independence claim
   before it).

## 5. Hand-back checklist

- [ ] IONEX files + `sha256_manifest.json` (verbatim names, URLs, dates, hashes)
- [ ] December files present but unopened (stated in notes)
- [ ] Exploration note (rule-vs-rule differences, Jan–Nov only)
- [ ] Hand-check document (dated, names its IONEX file)
- [ ] Network-list artifact for the overlap audit
- [ ] Q-15 answered in `Q15_DECISION_OPTIONS_...md` and adopted as a D-number in
      `evidence/DECISIONS.md` (your act)

Then the in-repo work becomes buildable, in order: transcribe Q-15 into config under its
D-number citation; implement the gated generation path (mirroring B-01's pattern:
generate → provenance + hashes → bridge/parquet emission); overlap audit + mandatory
flag disclosure; fixture-scale wiring. That is agent-lane work once the checklist is on
disk.
