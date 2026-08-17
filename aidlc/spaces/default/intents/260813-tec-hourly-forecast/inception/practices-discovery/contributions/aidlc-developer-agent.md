**Collaborator:** aidlc-developer-agent

## Contribution

Scope of this pass: code style and structure — naming, layer boundaries (`src/` vs. notebooks vs. the
nine phase-aware stage scripts), error handling, file organisation, the four governed config files,
Python version pinning, the duplicated hashing helpers, and the `Languages: TypeScript` field. I read
both scripts in full, opened `notebooks/madrigal_phase1_coverage_audit.ipynb` (which the lead's
`evidence.md` records as not opened), and re-read
`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §1.3, §7, §7.0, §8.1, §8.3,
§10, §10.1, §11, §12, §13.1, §13.2, §14, §18.2, §18.3, §19.

The Code Style section is accurate in everything it asserts, but it is drawn from about half the
available evidence. Nine additions and corrections follow, ordered by how much they change what
Construction will build.

### 1. The notebook holds frozen scientific values and production logic — this is the largest gap

`evidence.md` states the notebook "was not opened" and that "its actual code style was not inspected
and is not claimed as evidence for the Code Style section." Opening it changes the layer-boundary
picture materially. `notebooks/madrigal_phase1_coverage_audit.ipynb` (19 cells, 14 code cells, ~455
source lines, kernelspec `python3`, `language_info.version` 3.11, outputs stripped) contains:

- **Cell 4 — the frozen station registry as an inline literal.** `STATIONS = {'ARUC': {'lat': 40.286,
  'lon': 44.086, ...}, 'BSHM': {...32.778987, 35.022987...}, 'NICO': {...35.140989, 33.396450...}}`,
  self-labelled in its own comment as "PROVISIONAL until validated against the official site-log PDF
  for each station".
- **Cell 4 — the coordinate-to-cell convention as inline logic.** `def cell_bounds(lat, lon)` floors to
  a 1°×1° lower-left-corner cell, under a comment reading "DEFAULT convention adopted here" and
  "CONFIRM this matches the real bin edges Madrigal returns ... before treating it as frozen."
- **Cells 6–onward — retrieval and parsing logic**: `fetch_isprint`, `parse_isprint`,
  `looks_like_isprint_error`, `cache_path`, plus `MADRIGAL_URL_CANDIDATES` and the instrument-code
  discovery heuristic.

Four governing rules bear on this:

- §7 (line 300): "Reusable logic belongs in `src/`; the nine phase-aware stage scripts orchestrate it;
  notebooks do not own production logic."
- §12: the station registry belongs in `src/data/registry.py` ("station registry, IGRF coordinates,
  coverage"); stations and year are "Fixed in `data.yaml`" (§2.1 table row **Stations / year**).
- TC-03e (`constraint-register.md`): "Exactly four governed config files; **no scientific constant
  hidden in source or notebooks**."
- §18.2 forbidden-choice table: "Any station coordinate, DOMES ID, or hardware interval" (Student) and
  "Prepared-data provider, target product/physical definition, **cell-selection rule**, hourly
  aggregation, or coverage threshold" (Student + Supervisor, D-143/D-144/G-P1). §18.2's rule is that
  the agent may not "choose, invent, default, or silently change" these. The notebook's own comments
  concede it has adopted a default for one and a provisional value for the other.

To be fair to the current state: this notebook is the pre-scaffold coverage-audit notebook, not one of
the five production notebooks of §12/§14, so it is not itself in breach of §14 today. But its contents
are exactly the material §18.2 reserves to human freeze, and they are currently the project's only
copy. I recommend the Code Style section state this as a **named migration obligation on the
repository-scaffold work (TA-01/TC-06)**, not as an open question:

> The station coordinates and the coordinate-to-cell rule currently live only as literals and a
> function in `notebooks/madrigal_phase1_coverage_audit.ipynb` (cell 4). Both are §18.2 forbidden-choice
> items and TC-03e scientific constants. When the scaffold is built they move to `configs/data.yaml`
> (values) and `src/data/registry.py` (logic), and the coordinates are validated against the official
> IGS site logs (§10 "Official site logs — Station registry ground truth"; §7.0 P1-02) before any
> value is treated as frozen.

### 2. The import-boundary rule is missing from both artifacts

§12 states, immediately after the repository tree: "**Import-boundary rule, enforced by test.**
`src/external/iri.py` and `src/external/gim.py` must never be imported, directly or transitively, by
any module under `src/features/` or `src/models/`. They are imported only by
`scripts/04_build_external_products.py` and `src/evaluation/`." §12's tree repeats it inline on both
files ("BENCHMARK ONLY - never imported by src/features or src/models"), and TA-07 (§19) makes it an
approval item: "`test_iri_denial.py` fails on deliberate `iri_*` injection, **and no module under
`src/features` or `src/models` imports `src/external/iri.py`**".

This is a *module-graph* rule, distinct from the *data-flow* rule already captured in
`discovered-rules.md` ("NEVER let an `iri_*` field ... reach ML training or inference"). A pipeline can
satisfy the data-flow rule and still violate the import rule. It belongs in the Code Style section as a
structural constraint and in `discovered-rules.md` § Forbidden as its own entry, for example:

> - NEVER import `src/external/iri.py` or `src/external/gim.py`, directly or transitively, from any
>   module under `src/features/` or `src/models/`; the only permitted importers are
>   `scripts/04_build_external_products.py` and `src/evaluation/`. (Technical Environment §12
>   import-boundary rule; §19 TA-07.)

### 3. The four config files have a mandated location and a preflight contract, both omitted

The draft names `data.yaml`, `features.yaml`, `experiment.yaml`, `seeds.yaml` but not where they live
or how they are consumed. §12 places them under `configs/` ("`configs/` # exactly four files"); §13.5
refers to `configs/seeds.yaml`; §13.2's clean-run contract passes `--config configs/` to every stage
script. §18.3 adds a hard precondition the draft does not mention: "An automated preflight asserts that
no required field in `data.yaml`, `features.yaml`, `experiment.yaml`, or `seeds.yaml` is `TBD`, that
every declared source and hash exists, and that all gate tests pass," with decision criterion "zero
unresolved P0 fields and no failing critical test" and evidence artifact `aws_ai_dlc_preflight_report`.
§13.1 further requires each run to capture "configuration snapshot hashes for all four config files".

Suggested replacement for the draft's config bullet:

> Exactly four governed config files under `configs/` — `data.yaml`, `features.yaml`, `experiment.yaml`,
> `seeds.yaml` — with no scientific constant in source or notebooks (§12; §1.3 change row; TC-03e).
> Every stage script receives them as `--config configs/` (§13.2). Each run snapshots and hashes all
> four (§13.1). Before an affected component is implemented, an automated preflight must assert no
> required field in any of the four is `TBD` (§18.3).

### 4. Script naming and CLI convention are unstated

Naming conventions are in this section's remit and the governing documents fix them exactly. §12 and
§13.2 give a uniform contract the draft never mentions:

- Stage scripts are `NN_verb_noun.py` with a two-digit ordinal prefix: `00_acquire_prepared_vtec.py`,
  `01_inventory_and_registry.py`, `02_standardize_prepared_target.py`, `02_build_vtec_target.py`,
  `03_verify_processing.py`, `04_build_external_products.py`, `05_build_features_and_splits.py`,
  `06_train_and_predict.py`, `07_evaluate_and_report.py`; plus the non-numbered orchestrator
  `run_walking_skeleton.py`.
- Every stage script takes `--config configs/`; phase-aware stages additionally take `--phase 1` or
  `--phase 2` (§13.2; §7.0 P1-02 shows `01_inventory_and_registry.py --phase 1`).
- The walking-skeleton orchestrator takes `--fixture plumbing_7day` / `--fixture scientific_1month`,
  matching the fixture directory names under `tests/fixtures/` (§12, §13.2).
- Test files are `test_<subject>.py` and are enumerated exhaustively in §12 (17 files); notebooks are
  `NN_topic.ipynb` (five files).

This matters now rather than at Construction: it is the interface contract that makes NFR-REP-01's
"one documented ordered command sequence" reproducible, and it is fully specified, so it should be
recorded as discovered rather than left for code-generation to reinvent.

### 5. The two observed scripts are **not** the same style family — correct `evidence.md`

`evidence.md` records `scripts/merge_coverage_year.py` as "Same style family" as
`scripts/audit_ec1_drivers.py`. They diverge on four axes, every one of which a formatter or linter
config would have to settle:

| Axis | `audit_ec1_drivers.py` | `merge_coverage_year.py` |
|---|---|---|
| Typing | `from __future__ import annotations` (:14), PEP 604 hints (`dict[dt.date, list[dict]]` :100, `-> str` :33, `-> int` :168) | No `__future__` import, no annotation anywhere |
| Paths | `pathlib.Path` throughout (:22–:27) | `os.path.join` throughout (:33–:34, :52, :98) |
| Strings | double quotes, f-strings (:53, :180) | single quotes, `%`-formatting (:34, :79, :113, :221) |
| Fatal exit | `raise SystemExit(...)` (:53, :98) plus `sys.exit(main())` (:188) | `sys.exit('message')` (:67, :79, :118, :145); `main()` returns `None` and is called bare (:229) |

The draft's own bullets are individually accurate — it correctly scopes `from __future__` and PEP 604
to `audit_ec1_drivers.py` — but the surrounding framing ("Observed style conventions in the two scripts
present", "an inferred pattern from two files") reads as though a convention exists to affirm. It does
not. The honest finding is stronger and more useful at the interview: **the only two Python files in
the workspace disagree on typing, path handling, quoting, and the fatal-exit idiom, so there is no
convention to affirm — there is a choice to make, and it must be made before the nine stage scripts and
six `src/` packages are generated.** What the two files genuinely share is the module-level docstring
naming purpose, inputs, and re-run behaviour (both, lines 1–23 / 1–23) and `snake_case` naming.

### 6. `pyproject.toml` is a mandated deliverable, not merely absent

The draft says "No `.prettierrc`, `pyproject.toml`, `setup.cfg`, or `ruff`/`black` configuration file
was found ... contrary to `org.md`'s instruction to check project-level configs first." The absence is
confirmed (I re-verified: no `pyproject.toml`, `setup.cfg`, `ruff.toml`, `.flake8`, `tox.ini`,
`requirements.txt`, `.python-version`, and no `src/`, `configs/`, or `tests/` directory). What the
draft omits is that §12's repository tree **mandates `pyproject.toml` at the repository root**, and
TA-01 (§19) makes the skeleton an approval item: "Repository skeleton exists with four configs, six
packages, nine phase-aware stage scripts, five notebooks, tests, and artifacts". TC-06 places
"Repository structure, pinned environment and test suite ... **before** any acquisition work, inside
this initiative."

So `org.md`'s defer-to-project-config instruction is not permanently unsatisfiable here — the config
file has a mandated home and a scheduled build. Reframe the open question accordingly: not "whether to
adopt `black`/`ruff` now" in the abstract, but **"what formatter and linter does `pyproject.toml`
record, decided as part of the TA-01 scaffold and before the nine stage scripts exist."** Deciding it
after code generation would mean reformatting code whose commit hashes §13.1 requires each run to
capture.

### 7. The hashing helper is triplicated, and the consolidation target is constrained

The draft names two copies. There are three:

- `sha256(path: Path) -> str` — `scripts/audit_ec1_drivers.py:33`, 1 MiB chunks (`1 << 20`).
- `sha256_of_file(path)` — `scripts/merge_coverage_year.py:41`, 8 KiB chunks.
- `sha256_of_file` — `notebooks/madrigal_phase1_coverage_audit.ipynb`, a third copy inside the notebook.

They produce identical digests; only chunk size and signature differ. The draft's remedy — "a candidate
for consolidation into a shared module once `src/` exists" — is under-specified in a way that could
breach the structure it is meant to serve: §12 fixes `src/` at **six domain packages** (`data`, `gnss`,
`external`, `features`, `models`, `evaluation`) and TA-01 approves against that count, so a seventh
`src/utils/` package is not available. The natural homes inside the six are `src/data/release.py`
(which owns release hashes and is covered by `tests/test_release_hashes.py`) or
`src/data/phase_contract.py` ("boundary and transition-manifest hashes"). Recommend the draft name one
rather than leaving "a shared module" open, and note that the notebook copy must go too — a notebook
holding the only copy of hashing logic is precisely what §14 forbids ("must not contain the only copy
of parsing, calibration, feature, split, training, evaluation, or bootstrap logic").

### 8. The observed error-handling convention is two-tier, and only one tier is captured

The draft records "explicit, narrated `sys.exit(...)` ... on integrity failure, rather than silent
continuation". That is the fatal tier. The observed code actually runs a coherent **two-tier** posture
that is more distinctive and worth affirming as a team practice:

- **Integrity violations are fatal.** `merge_coverage_year.py:79` refuses to merge a month with no
  `sha256_manifest.json` ("refusing to merge unverified evidence"); `:85`/`:87` exit on a listed-but-
  missing file and on a failed hash check ("evidence altered since the run"); `:145` exits on a
  self-check invariant (coverage above 100% ⇒ "dedup or year guard failed").
- **Completeness shortfalls are non-fatal but must be stamped into the artifact.** Missing months warn
  at `:73` and `:225` and are recorded in the manifest as `months_missing`, `partial_run: bool(missing)`,
  `rows_outside_audit_year_excluded`, and `artifact_kind: 'MERGED -- derived from per-month runs, NOT a
  fresh retrieval'` (`:186`–`:196`). `audit_ec1_drivers.py:59` takes the same softer path for a missing
  monthly file (`{"error": "file not retrieved"}`) and continues.

This maps directly onto NFR-AUD-01 ("failed runs remain visible") and §13.3's immutable release
manifest. Proposed as a Code Style rule to affirm:

> Integrity failures (hash mismatch, missing manifest, violated invariant) terminate the run with a
> message naming the file and the violated expectation. Completeness shortfalls do not terminate the
> run but must be recorded as machine-readable fields in the output manifest — never only as console
> text — and the artifact must state that it is derived and/or partial.

One gap in the observed code worth carrying as a caveat: `audit_ec1_drivers.py:184` returns `0` whether
or not months were missing, so a partial audit is indistinguishable from a complete one by exit code.
Under §18.3 ("no failing critical test") anything wired into an automated preflight needs a
machine-checkable completion status, not console prose.

### 9. One integrity gap in the observed code, reported as evidence (not fixed)

`scripts/merge_coverage_year.py:182`–`:208` takes `request_manifest.json` from the *first* month as a
template and copies eight provenance fields (`madrigal_url`, `instrument_code`, `kindat_code`,
`parameters_requested`, `stations`, `coordinate_to_cell_convention`, `user_fullname`,
`user_affiliation`) into the merged manifest under the comment "carried unchanged from the source runs
-- identical across all of them". Nothing asserts that identity. In a script that otherwise verifies
every hash before trusting any data, this is the one place a claim is stamped into an evidence manifest
as fact without a check. Two of those fields — `stations` and `coordinate_to_cell_convention` — are
§18.2 forbidden-choice items, so a silent divergence between monthly runs would be exactly the class of
error the governance regime exists to catch. Suggested team rule: *assert cross-source field identity
before carrying a field forward into a derived manifest; a provenance field copied from one source and
labelled as common to all must be verified, not asserted in a comment.* I have made no edit to this
file.

### 10. `Languages: TypeScript` — the correction is stronger than a mismatch flag

The draft's diagnosis is right (the TypeScript traces to AI-DLC's own `.ts` tooling) and it is right to
surface rather than silently resolve it. Two things should be added.

First, the Python evidence is now four-fold, not two-fold: `scripts/audit_ec1_drivers.py`,
`scripts/merge_coverage_year.py`, and `notebooks/madrigal_phase1_coverage_audit.ipynb` whose notebook
metadata declares `kernelspec.name = python3` and `language_info.version = 3.11` — matching the §8.1
pin exactly — plus §8.1 itself ("Python 3.11 | Required, exact version | All implementation and
orchestration").

Second, and not mentioned in the draft: §8.3 makes Python-only a **hard normative rule**, not merely an
observation. R is "Prohibited for the pipeline — Avoids a second language/runtime"; Julia is
"Prohibited — Unnecessary runtime"; MATLAB is "Prohibited — Conflicts with the reproducible
Python-centered environment"; PyTorch is prohibited to avoid "a second deep-learning stack". A stage
that read `Languages: TypeScript` as licence to generate TypeScript research code would breach §8.3
directly. Per `phases/inception.md` (requirements testable, no unresolved contradictions carried
forward), this should not be left as a flag. Suggested resolution to put to the human:

> `aidlc-state.md` → `Languages` reads `Python 3.11` (the governed pipeline, §8.1, TC-03d). AI-DLC's own
> TypeScript tooling under `.claude/`, `hooks/`, `tools/`, `sensors/` is workflow infrastructure and not
> a project deliverable; it is recorded as such rather than as a project language.

### 11. Two unresolved items the draft carries forward without surfacing

**(a) An internal contradiction in the governing document about script and notebook counts.** §1.3's
v2.0 change table states "Scripts 18 → **7**" and "Notebooks 11 → **4**". §7 (line 300), §12, and §19
TA-01 all state **nine** phase-aware stage scripts (the §12 tree lists nine numbered stages plus
`run_walking_skeleton.py`), and §12/§14 state **five** notebooks ("Five production notebooks: one
replacement acquisition notebook and four analysis/review notebooks"). The config count (4) is
consistent across both; the script and notebook counts are not. `evidence.md` cites §1.3 as the source
for "script/notebook/config counts" while `team-practices.md` uses the nine-script figure from §7,
so the draft has both numbers in hand without reconciling them. `phases/inception.md` forbids carrying
an unresolved contradiction forward. The likely reading is that §1.3 records the v1.0→v2.0 reduction
before the Phase 1 split added `00_acquire_prepared_vtec.py`, `02_standardize_prepared_target.py`, and
the acquisition notebook — but that is my inference, and §1.1/§18.2 forbid an agent resolving it by
convenience. It should be listed as a documentation-resolution item for the student/supervisor, with
the note that §12/§14/§19 are the operative counts because TA-01 approves against them.

**(b) Neither existing script has a home in the mandated tree.** §12 enumerates `scripts/`
exhaustively; `audit_ec1_drivers.py` and `merge_coverage_year.py` appear nowhere in it, and neither
takes `--config configs/`. They are legitimate pre-scaffold evidence tooling (they produced the EC-1
and G-P1A coverage evidence), but their disposition once the scaffold exists — retained outside the
governed tree, ported to the stage-script contract, or archived under `artifacts/source_audits/`
alongside the other retained failure/audit evidence — is unresolved and should be an explicit interview
item rather than an assumption.

### 12. Adjacent to my scope, but it corrects a stated assumption: version control is required

`team-practices.md` § Assumptions states: "none of the governing documents (Vision, Technical
Environment, constraint register) mandate or forbid version control tooling — they govern the
scientific pipeline, not the software engineering practice around it." This is contradicted by the
Technical Environment document. §13.1's environment lock requires each run to capture, among other
items, "**code commit**"; NFR-AUD-01 requires that "datasets, configs, **commit**, models, predictions,
metrics, and figures are immutable or versioned"; §12's tree mandates a repository root; TA-01's
evidence column is "**Repository tree and code commit**". A run cannot record a code commit without a
version-controlled repository, so initialising one is a reproducibility prerequisite (NFR-REP-01,
NFR-AUD-01, TA-01), not an open preference. The interview question that survives is the org-default
one the draft already raises — whether trunk-based/squash-merge applies to a single-author thesis with
supervisor countersign gates instead of PR review — but *whether* to have version control at all is
already answered by the governing document. Flagging for the lead to route into § Way of Working; I
have not edited that section.

### What the draft got right and should keep verbatim

- Python 3.11 as the governed exact pin (§8.1, TC-03d) — confirmed, and now corroborated by the
  notebook's own `language_info.version`.
- `src/` ownership of reusable logic with scripts orchestrating (§7) — the correct rule, though the
  draft's phrasing "notebooks **and** the nine phase-aware stage scripts orchestrate it" softens §7's
  actual sentence, which separates the two: "the nine phase-aware stage scripts orchestrate it;
  **notebooks do not own production logic**." Recommend quoting §7 exactly, because §14's notebook rule
  ("must not contain the only copy of parsing, calibration, feature, split, training, evaluation, or
  bootstrap logic") depends on that separation.
- Refusing to invent an 80% coverage figure for a research pipeline where none is stated — correct, and
  consistent with the project rule against filling a governed blank by convenience.
- Recording the `Languages` mismatch as a discrepancy for the human rather than silently overriding
  `aidlc-state.md` — correct handling, needing only the §8.3 reinforcement above.
- Naming the module-level docstring and the narrated fatal exit as candidate conventions — both real,
  both worth affirming, once the two-tier framing in item 8 is added.

### One rule missing from `discovered-rules.md` that is squarely structural

§10.1 (External Method and Code-Reuse Register) fixes a code-organisation rule with an enforcing test
and an NFR, and neither artifact mentions it: "Copied code lives behind a project-owned adapter;
upstream functions are not pasted into notebooks." Every copied or adapted fragment needs a register
record with fourteen named fields (`reuse_id`, repository URL, immutable commit/tag, upstream
file/line, retrieval date, license/SPDX ID, copied-vs-adapted, destination file, purpose,
modifications, tests, citation, notice location, reviewer, approval date), implemented at
`src/data/reuse_registry.py`, tested by `tests/test_reuse_registry.py`, required by NFR-LIC-01, and
approved at TA-01's sibling items. Given §10.1 approves direct copying from an **AGPLv3** repository
(the Global TEC forecasting project), this is a live licensing exposure, not a formality. Proposed
addition to § Mandated:

> - ALWAYS place copied or materially adapted external code behind a project-owned adapter with a
>   `src/data/reuse_registry.py` record carrying provenance, immutable commit, license/SPDX ID,
>   modifications, tests, citation, and notice location; never paste an upstream function into a
>   notebook. (Technical Environment §10.1; NFR-LIC-01; `tests/test_reuse_registry.py`.)

## Positions

- AGREE: Python, not TypeScript, is the project's implementation language and the mismatch must be surfaced rather than silently resolved — corroborated by four artifacts and by §8.1's exact-version requirement.
- AGREE: refusing to invent a numeric coverage floor where the governing documents state named required tests instead — inventing one would fill a governed blank by convenience.
- AGREE: the four governed config files are a hard structural constraint on the future codebase, not a formatting preference — §12 and TC-03e both state it as such.
- AGREE: the duplicated SHA-256 helpers are a real consolidation candidate — the draft identified the right smell, and item 7 only sharpens the count and the destination.
- OBJECT: the notebook was never opened, so the Code Style section misses that the frozen station coordinates and the coordinate-to-cell rule — both §18.2 forbidden-choice items and TC-03e scientific constants — currently exist only as literals and a function inside `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 4.
- OBJECT: §12's import-boundary rule (`src/external/iri.py`/`gim.py` never imported by `src/features/` or `src/models/`, enforced by test, approved at TA-07) is absent from both artifacts and is not implied by the data-flow IRI rule already captured.
- OBJECT: `evidence.md` calls `merge_coverage_year.py` the "same style family" as `audit_ec1_drivers.py`; they diverge on typing, path handling, quoting, and the fatal-exit idiom, so there is no observed convention to affirm — only a decision to make.
- OBJECT: the draft treats the absent `pyproject.toml` as a gap in `org.md`'s defer-to-config instruction, omitting that §12 mandates `pyproject.toml` and TA-01/TC-06 schedule it before acquisition — which converts the open question from "whether to adopt a linter" into "what the mandated scaffold file records, decided before code generation".
- OBJECT: §1.3's "Scripts 18 → 7 / Notebooks 11 → 4" contradicts §7/§12/§14/§19's nine stage scripts and five notebooks; the draft cites both figures without reconciling them, which `phases/inception.md` forbids.
- OBJECT: script naming (`NN_verb_noun.py`), the uniform `--config configs/` CLI, the `--phase 1|2` flag, and the `configs/` directory location are fully specified in §12/§13.2 and absent from the Code Style section, despite naming conventions being in its remit.
- OBJECT: `team-practices.md` § Assumptions asserts that no governing document mandates version control; §13.1 ("code commit"), NFR-AUD-01, and TA-01's "Repository tree and code commit" evidence column all require it.
- OBJECT: §10.1's structural rule — copied code lives behind a project-owned adapter, never pasted into a notebook, with a `reuse_registry` record under NFR-LIC-01 — is missing from `discovered-rules.md`, and it governs an approved AGPLv3 copy source.
