# `tests/fixtures/scientific_1month/` — the one-month all-station scientific fixture

**No MEASURED value in this directory was authored by hand** (TE §15.1: "exact counts,
tolerances, and runtimes are measured from the fixtures and frozen; they are not invented
here"; BLK-02, which stays OPEN).

*Amended 2026-09-20 (Recommendation 37). This paragraph previously read "**No file in this
directory is a fixture manifest.** `fixture_manifest.yaml` does not exist here and may not
be authored by hand". The first clause stopped being true on 2026-09-20.*
`fixture_manifest.yaml` now exists as a `status: candidate` **skeleton**: structural fields
transcribed from `identity_declaration.yaml`, and the literal `TBD — freeze gate` in every
MEASURED field with **no `measuring_run_id` anywhere** — which is precisely what makes
`load_fixture_manifest` refuse it, by name, at the first measured field it reaches. It
exists so the loader can be exercised against a real file. It is not frozen, it produces no
evidence, and the measuring run in step 2 below replaces it wholesale rather than patching
it.

## How a manifest comes to exist

1. The owner authors an **identity declaration** (`kind: identity_declaration`) carrying the
   fixture's identity **by citation, never re-derived**: the window from **D-14** (March 2022,
   2022-03-01 … 2022-03-31 inclusive, all three cells) with D-14's mandatory limitation in
   **both** clauses verbatim — (i) the equinox-month clause and (ii) "It is not representative of
   the locked test month, and no fixture result may be read as evidence about December
   behaviour"; the DATA-07 caveat text; the three TEC-05 stamps; the **apparatus partition
   declaration** (ids outside `F1`…`F4`/`REFIT`/`DEC`, over the March window — R-137, Q4 = A);
   and the **`fixture_bootstrap`** block (`replicates`, `scored_range`, `block_counts`) that TE
   §15.3's reduced-replicate timing bootstrap runs on — apparatus constants (R-122), never
   `experiment.yaml` values. Read only through
   `src.data.fixture_manifest.load_identity_declaration`.
2. A **measuring run** — `python scripts/run_walking_skeleton.py --config configs/ --fixture
   scientific_1month --emit-candidate --identity <declaration>` — runs only after a verified
   `plumbing_7day` receipt exists (TE §9.2 in order; R-140), and emits `fixture_manifest.yaml`
   with `status: candidate`, every measured field carrying that run's registry id (R-134).
3. The **owner's Q-31 freeze act** sets `status: frozen`, writes the sibling
   `fixture_manifest.sha256`, and records the hash under a new D-number in
   `evidence/DECISIONS.md`. Nothing in the codebase performs this step.

## The two states

`candidate` — offered for freeze; validates; no evidence, no receipt. `frozen` — the only
evidence basis; sibling hash required; a post-freeze edit fails and the expectation is never
updated (TE §13.7). A `toleranced` ledger entry declaring TECU units for an output whose
producing path declares no `inverse_route` is **not freezable** (BLK-08 ↓ checked; R-139).

## What every artifact of this fixture carries

`december_representativeness: not_representative` and the `data07_caveat` — this fixture's
outputs MAY serve WS-12/WS-13/WS-16/WS-17 evidence, which is exactly why the prohibition on
reading them as December evidence travels with every number (D-14 clause (ii); Rec 36).

**Neither fixture has ever run. No measured value exists.** Both sentences remain TRUE and
are the operative ones.

*Amended 2026-09-20 (Recommendation 45). The clause that followed them — "`.gitkeep` and
this README are the only files here by design
(`governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md`)" — was already
stale when the owner's `identity_declaration.yaml` landed on 2026-09-13 and is now doubly
so.* The directory holds four files by design:

| File | What it is |
|---|---|
| `.gitkeep` | keeps the tree under version control while it is otherwise empty |
| `README.md` | this file |
| `identity_declaration.yaml` | the owner's Q-31 identity declaration, adopted 2026-09-13 under `CR-2026-09-13-000102-FIXTURE-WINDOW` |
| `fixture_manifest.yaml` | the `status: candidate` structural skeleton written 2026-09-20; every measured field is the literal sentinel and the loader refuses it by name |

A `fixture_manifest.sha256` is deliberately ABSENT: only a FROZEN manifest carries one, and
a candidate carrying one is refused (SD-X-01's negative control).

## The Kaggle in-session sequence (TA-03 / TA-26)

See `tests/fixtures/plumbing_7day/README.md` § "The Kaggle in-session sequence" — the
critical set and BOTH fixtures run inside the Kaggle session before any governed run there,
and the gate result is emitted via `src.data.fixture_gate.emit_in_session_gate_result`
(platform from `ConfigSnapshot`, never asserted). The scientific fixture additionally
requires the verified plumbing receipt (R-140 control 26). Both TA rows stay `Pending`
until a real Kaggle session emits the artifacts.
