# R-60 overlap-audit input — CODE network vs. ARUC/BSHM/NICO

Prepared 2026-09-26. This is the **input** to the `gim_network_overlap_flag` audit
(TE §5.2), not the audit's disclosed result. `src/external/gim.py` and
`src/evaluation/metrics.py` both refuse to emit a comparison unless an
`overlap_audit` mapping containing `gim_network_overlap_flag` is supplied — that
refusal gate exists in-repo today; the computation that would produce the flag
value does not. This document supplies the input; running the audit and
disclosing the flag is the next, separate, in-repo step (blocked here, see below).

## Method

Every one of the 334 acquired CODE final GIM IONEX files for January 1 –
November 30, 2022 (day-of-year 1–334; December excluded, sealed) carries a
header block `List of stations:` — a `COMMENT`-typed section listing the
IGS 4-character station codes whose data CODE ingested for that day's
combination solution (documented in the same header's `DESCRIPTION` block:
"...using data from about 300 GNSS sites of the IGS and other institutions").
This is header metadata about which receivers contributed to the solution,
not a TEC/VTEC value — reading it is not covered by the December-sealed
restriction, and no December file's header was read to build this list
regardless.

For each of the 334 files: decompress (`gzip -dc`, works uniformly for both
the `.Z` legacy-compress and `.gz` files in this acquisition — 2022 spans
both filename generations), extract the `List of stations:` comment block,
lowercase and union across all days. Result: **275 unique station codes**
appear in CODE's contributing network somewhere across Jan–Nov 2022.

## Result

| Station | 4-char code | In CODE Jan–Nov 2022 network? |
|---|---|---|
| ARUC | `aruc` | **No** — absent from all 334 unioned station lists |
| BSHM | `bshm` | **Yes** — present |
| NICO | `nico` | **Yes** — present |

Station code confirmed against `configs/data.yaml`'s site-log filenames
(`aruc00arm_20260317.log`, etc. — the 4-char prefix is the IGS station ID).
No near-miss variant of `aru*` appears anywhere in the union list either.

## What this does and doesn't establish

This shows BSHM's and NICO's own GNSS receivers are among the ~300 sites
whose observations CODE combines into the GIM solution — a structural
overlap between "station being evaluated" and "network that produced the
comparator." It does **not** by itself compute or disclose
`gim_network_overlap_flag`, which is a defined audit output per TE §5.2 with
its own rule (not reproduced or approximated here) for what counts as
disclosure-triggering overlap, how partial-year presence is handled, and how
the flag interacts with independence claims. That rule and its
implementation do not exist in this repository yet.

## Status: BLOCKED / PENDING

- **Input**: delivered — `code_network_stations_2022_jan-nov_union.txt`
  (275 codes, SHA-256 `e7a51c37a5661ccd9e9356747a070e7f19f58acf2e0d2b06d8e304d76802d61b`),
  reproducible from the acquired IONEX headers by the method above.
- **Audit rule + computation**: not implemented in-repo. `gim.py`'s refusal
  gate is a placeholder for a caller-supplied `overlap_audit` dict; nothing
  in the repository computes that dict's `gim_network_overlap_flag` value
  from a station list.
- **Disclosure**: not made. No independence claim is implied or should be
  drawn from the table above pending the real audit (TC-08; TE §5.2
  mandates disclosure is unconditional once the audit runs — it has not).

Building the audit computation itself is agent-lane, in-repo work, sequenced
after Q-15's freeze per the runbook's own ordering.
