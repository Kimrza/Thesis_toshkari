# `tests/fixtures/plumbing_7day/` — the seven-day single-station plumbing fixture

**No file in this directory is a fixture manifest.** `fixture_manifest.yaml` does not exist
here and may not be authored by hand (TE §15.1: "exact counts, tolerances, and runtimes are
measured from the fixtures and frozen; they are not invented here"; BLK-02).

## How a manifest comes to exist

1. The owner authors an **identity declaration** (`kind: identity_declaration`) carrying the
   fixture's identity **by citation, never re-derived**: the window from **D-11**
   (2022-11-01 … 2022-11-07 inclusive) with D-11's mandatory not-representative-of-December
   limitation and its provisional-Dst restriction **verbatim**; the station from **D-20**
   (BSHM 32/35, TE §15.1's "One station"); `aruc_shortfall_status: dormant` with its
   reactivation condition; the DATA-07 caveat text; the three TEC-05 stamps; and, when the
   plumbing fixture's minimal M-06 needs a fit, an apparatus partition declaration (ids outside
   `F1`…`F4`/`REFIT`/`DEC`; R-137). It is read only through
   `src.data.fixture_manifest.load_identity_declaration`.
2. A **measuring run** — `python scripts/run_walking_skeleton.py --config configs/ --fixture
   plumbing_7day --emit-candidate --identity <declaration>` — emits `fixture_manifest.yaml` with
   `status: candidate`, every measured field carrying that run's registry id (R-134).
3. The **owner's Q-31 freeze act** sets `status: frozen`, writes the sibling
   `fixture_manifest.sha256`, and records the same hash under a new D-number in
   `evidence/DECISIONS.md` (`fixture_manifest_sha256: <hex>`). Nothing in the codebase performs
   this step (`src.data.fixture_manifest.write_candidate_manifest` refuses `frozen`).

## The two states

`candidate` — offered for freeze; validates; produces **no** WS-20/TA-09/TA-17 evidence and
**no** receipt. `frozen` — the only evidence basis; requires the sibling hash; a post-freeze
edit fails and the expectation is never updated (TE §13.7).

## The only read path

`src.data.fixture_manifest.load_fixture_manifest(path)` — the one schema (the twelve TE §15.2
areas by name), the one validating loader. A second YAML parse of a fixture manifest anywhere
under `src/`, `scripts/` or `tests/` fails `tests/test_clean_run.py`'s only-copy check.

## What every artifact of this fixture carries

`evidence_class: smoke_only` — the seven-day result is a smoke test, **never scientific
evidence**: it may not be cited, plotted as a result, or interpreted as skill (TE §15.1;
TC-03f). Every evidence surface asserts its absence.

Neither fixture has ever run. No measured value exists. `.gitkeep` and this README are the only
files here by design (`governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md`).
