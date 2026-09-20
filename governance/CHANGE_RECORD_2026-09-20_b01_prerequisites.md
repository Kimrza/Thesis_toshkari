# Change Record — 2026-09-20 — B-01 prerequisites: environment identity (D-49 extension), fixture-ladder repairs and freeze package, official-reference collection, measured tolerance basis, `observable_codes` scope

**Record id:** `CR-2026-09-20-B01-PREREQS`. **Authority:** the project decision owner's
instruction of 2026-09-20 ("Continue from the latest handoff. Complete the following
prerequisites before asking me to rerun Kaggle", six numbered items), quoted where it is relied
on. **Prepared by:** the AI-DLC session; recorded on the owner's authority, no supervisor
signature claimed anywhere in this record.

**Repository state at writing.** HEAD is `4253d51` (owner commit, 2026-09-20 11:35 +0330,
which committed the 2026-09-19 pass's working tree — `.gitignore`, the D-45/D-49 records,
`kaggle/*`, `evidence/iri2016_*`, `evidence/station_registry_sources_2026-09-19/`). Every change
in this record is **uncommitted working tree on top of `4253d51`**; no commit, push, tag or
registration was made by this session. `evidence/test_run_access_log.jsonl` grew by the
access-log lines the guard tests append on every suite run.

**Boundaries held.** No full-year generation, no locked-target access (the locked tree was
neither read nor packaged; the custody scan stays clean), no model training, no producer
release, no `permitted_producers` registration, no commit, no push. Everything under
`evidence/b01_tolerance_basis_2026-09-20/` is diagnostic evidence, never a governed run.

---

## 1 — Environment: the Python 3.10 exception extended to the B-01 fixture runs (D-49 addendum)

**Owner authorization (2026-09-20), quoted:** *"I authorize extending the Python 3.10 exception
to the prerequisite fixture runs specifically required for B-01, provided their required
dependencies and scientific behavior are compatible. Keep the main training/stage environment on
Python 3.11. Preserve the receipt requirement: the B-01 fixtures and benchmark must use the same
applicable environment identity. Do not bypass or weaken receipt checks."*

### 1.1 Compatibility — checked first, before anything was recorded

| Check | Result |
|---|---|
| Every `requirements.txt` pin publishes a cp310 Linux wheel | yes: numpy 1.26.4, pandas 2.1.4, PyYAML 6.0.1, scikit-learn 1.4.2 (`manylinux_2_17`), tensorflow 2.21.0 (`cp310 manylinux_2_27`, requires-python `>=3.10`), pytest 8.2.2 and ruff 0.4.8 (pure/`py3-none-manylinux_2_17`) — PyPI JSON API, 2026-09-20 |
| `iricore==1.8.0` constraints against the pins | `numpy<2.0,>=1.25`, `fortranformat<3.0,>=2.0`, `pymap3d[core]<4.0,>=3.0.1` — all met by `numpy==1.26.4` and the hash-pinned companions |
| Full resolution, cp310 / `manylinux_2_17..2_35` x86-64 | `pip install --dry-run --report` of `requirements.txt` + the three IRI companions + `iricore==1.8.0`: **50 packages, no conflict** (report in the session scratchpad; the resolved set is listed in §1.4) |
| glibc floor | `iricore` wheel `manylinux_2_35`, tensorflow `manylinux_2_27`; the verified Kaggle image has glibc 2.35 (D-49 item 3) |
| Behavioural note | the same TensorFlow/scikit-learn/numpy/pandas releases are used under both interpreters; this is pin-level compatibility, **not** a claim of bit-identical numerics across interpreters — which is exactly why the receipt identity is kept strict (§1.3) |

**Limitation recorded, not hidden.** `requirements.txt` pins no transitive dependency; the cp310
resolution picks `keras==3.12.4` where the local 3.11 environment carries `keras==3.15.1`. The
environment lock's `pip freeze` records what actually ran and every receipt binds to it. No pin
was altered; nothing was silently upgraded or downgraded.

### 1.2 Recorded

- `evidence/DECISIONS.md` **D-49 addendum 2026-09-20**: item 4 resolved by resolution (a);
  scope = the two `run_walking_skeleton.py` fixture runs (measuring and verification, their
  seven stage-script subprocesses and the M10 contract fixture) executed **inside the same B-01
  environment**, which additionally carries `requirements.txt`'s pins; training and every other
  stage stay on 3.11; the compatibility evidence and the two limitations above; the receipt
  requirement preserved.
- `configs/experiment.yaml: benchmark_b01.runtime.interpreter_exception` mirrors it
  (`applies_to` gains the fixture runs with the addendum as authority; `environment_pins` names
  the pin surfaces; `excluded` keeps training, every other stage run, the local environment).

### 1.3 Receipt requirement — preserved by construction

`src/data/fixture_gate.py` is **untouched**. `verify_receipt` still accepts a receipt only when
its recorded TE 13.1 identity (requirements hash, `pip freeze`, runtime versions, code commit,
config hashes, platform, nondeterministic ops) equals the consuming run's lock. Running the
fixtures and `--generate-benchmark` in ONE environment is what makes that identity satisfiable;
a receipt from any other environment — the local 3.11 one included — still refuses.

### 1.4 Workflow updated — `kaggle/kaggle_iri2016_benchmark.ipynb` revision `b01-production-2`

On-disk SHA-256 `0bf879361f450c7884be4b2192b6d885aee6daf50297c34533b434c445097768`, 24 cells,
every code cell `ast.parse`-clean; **not run on Kaggle**. Changes: new **Step 3b** installs
`requirements.txt` into the 3.10 venv after the package unpack and records `pip freeze` after
every install; **Step 6** drops the separate `uv` 3.11 environment and runs the orchestrator with
the venv's interpreter (`--python`) and the package's `--code-commit`, distinguishing a frozen
manifest (verification run) from an identity declaration alone (two measuring runs, §2.4);
**Step 5** no longer stops the notebook when the samples file is absent (it records "not run" and
continues, so one session returns the ladder's diagnosis); **Step 7** stays `RUN_FULL_YEAR =
False` and is additionally guarded on the report's existence. `kaggle/HOW_TO_RUN.md` carries the
revision note. Resolved cp310 set (dry run): absl-py 2.5.0, astunparse 1.6.3, certifi 2026.7.22,
charset-normalizer 3.5.1, cloudpickle 3.1.2, colorama 0.4.6, flatbuffers 25.12.19, fortranformat
2.0.3, gast 0.7.0, google-pasta 0.2.0, grpcio 1.84.0, h5py 3.14.0, idna 3.20, iniconfig 2.3.0,
iricore 1.8.0, joblib 1.6.0, keras 3.12.4, libclang 18.1.1, markdown-it-py 4.2.0, mdurl 0.1.2,
ml_dtypes 0.5.4, namex 0.1.0, numpy 1.26.4, opt_einsum 3.4.0, optree 0.20.0, packaging 26.3,
pandas 2.1.4, pluggy 1.6.0, protobuf 7.36.2, Pygments 2.21.0, pymap3d 3.2.0, pytest 8.2.2,
python-dateutil 2.9.0.post0, pytz 2026.3.post1, PyYAML 6.0.1, requests 2.34.2, rich 15.0.0, ruff
0.4.8, scikit-learn 1.4.2, scipy 1.15.3, setuptools 84.0.0, six 1.17.0, tensorflow 2.21.0,
termcolor 3.3.0, threadpoolctl 3.7.0, typing_extensions 4.16.0, tzdata 2026.4, urllib3 2.8.0,
wheel 0.48.0, wrapt 2.4.1 (transitive versions are what pip resolves on the day; the lock is
authoritative).

---

## 2 — Fixture preparation: the actual walking-skeleton requirements, what was repaired, and the exact freeze package

### 2.1 What the freeze actually requires (read from the code and the fixture READMEs, not assumed)

A frozen `fixture_manifest.yaml` comes to exist in three steps (`tests/fixtures/*/README.md`;
`src/data/fixture_manifest.py`): (1) the owner's **identity declaration** (exists for both
fixtures since 2026-09-13); (2) a **measuring run** — `run_walking_skeleton.py --fixture <id>
--emit-candidate --identity <declaration>` — which runs the seven Phase 1 stage scripts on the
fixture scope, requires **every** TE 15.4 output present (`collect_required_outputs` aborts on any
absence), persists its measurements and composes a `status: candidate` manifest — and, by board
Rec 5, refuses a zero-width runtime/storage range, so **at least two measuring runs** are needed;
(3) the owner's **Q-31 freeze act** (`status: frozen`, the `.sha256` sidecar, a D-number) —
nothing in the code performs it. The scientific fixture's measuring run additionally requires a
**verified plumbing receipt** (R-140), i.e. a frozen plumbing manifest. So the ladder is, at
minimum: plumbing measured ×2 → owner freezes plumbing → plumbing verified + scientific measured
×2 → owner freezes scientific → both verified → receipts. That is the design, and it is why
"BLK-02" is not one blocker but a sequence with two owner acts inside it.

### 2.2 What the first real measuring-run probe found (governed 3.11 environment, isolated copy of the workspace, plumbing scope)

Each row is the first refusal met, in order, after the previous one was repaired:

| # | Where it stopped | Cause | Disposition |
|---|---|---|---|
| a | orchestrator preflight | `REQUIRED_FIELDS_MAP` had no `("fixtures-and-reproducibility", 1)` entry, so `required_fields_for` refused every fixture run before any fixture logic ran (the orchestrator's own docstring names the entry as existing) | **repaired** — minimal entry `("seeds.development",)`, the six siblings' shape (`src/data/config.py`) |
| b | identity agreement | both declarations carried their limitation clauses with a `D-11 mandatory limitation (verbatim): …` label prefix, which the verbatim check (R-135) rightly refuses | **corrected** — prefixes removed; the clause text is unchanged and now verifies verbatim against `## D-11` / `## D-14` (`assert_identity_agrees_with_decisions`: `clauses_verbatim: 2` for both) |
| c | input verification | `inputs.prepared_vtec` (evidence dir, month `sha256_manifest.json`, the four declared artifacts with hashes, `records_file`) was absent from both declarations | **prepared by citation** — the four artifacts and hashes copied from the months' own `sha256_manifest.json` (November for plumbing, March for scientific); verified against the bytes on disk at run time |
| d | record assembly | the orchestrator selected by station and then ASSERTED every record inside the 7-day window; the November month file holds 18,183 records including provider edge records dated 2022-10-31, so the assertion always fired | **repaired** — Option B applied to the orchestrator's own assembly: `select_records_within_window` (new, additive, in `src/data/acquisition.py` beside its assertion twin, same single record-date reader) selects on RECORD dates, then the existing assertion runs. Result on the real file: **1,810 BSHM records, 7/7 days** — D-11's own table figure |
| e | (Kaggle only) stage subprocesses | `00/01/02` accept no `--code-commit` and the orchestrator forwarded none, so on Kaggle (no git tree) all three would refuse at the lock capture | **repaired** — `--code-commit` added to `00/01/02` exactly as `04–07` declare it; `build_phase1_commands` threads the orchestrator's value into every invocation |
| f | **stage 00** | `00_acquire_prepared_vtec.py` constructs a live provider transport on every run and refuses (`_build_transport`: no transport is configured; re-acquisition is deferred DATA-07 work). On a fixture run the input is the month's already-acquired derived artifacts (TE 15.1 "reads prepared provider VTEC only"), which the orchestrator has already verified — but `00` has no fixture-scoped read path | **open — design ruling needed** (§2.5 item 1) |
| g | stage 01 `--build-registry` | `observable_codes` empty | **resolved for Phase 1** (§5) |
| h | stage 02 | `configs/data.yaml: qc_operations` absent — the closed QC list must be frozen under a D-number by the supervisor (FR-P1-03-1, Q2 = A) | **open — supervisor freeze** |
| i | stage 04 | completes its fixture-scoped driver audit, but produces neither `iri_benchmark.parquet` (R-59: no passing validation report; and no fixture-scoped generation path exists yet) nor `gim_comparator.parquet` (Q-15 interpolation rule unset) — both are TE 15.4 required outputs | **open** — R-59 is this workstream (§3–§4); a fixture-window generation path in `04` is implementation work owed once the report passes; Q-15 is a student freeze |
| j | stage 05 | `features.yaml: permitted_producers` lacks the seven driver rows (`kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`, `dst`) — producing-ARTIFACT identities that exist only once the driver releases exist; `feature_set_id`, `feature_dictionary`, `normalization` are `TBD — freeze gate` | **open — student freezes / driver releases** |
| k | stage 06 | `experiment.yaml: horizons` was TBD when probed (TE 2.1 fixes `[1]`); `models.selected` is written by the tuning run, never by hand | **horizons transcribed 2026-09-20 (D-51, §8 addendum); `models.selected` follows tuning** |
| l | stage 07 | no released Phase 1 hourly target manifest (follows from h) | follows h |

Rows f–l were each observed by running that stage script directly on the plumbing scope in
the isolated copy, so the list is measured, not inferred. Ruff: no new finding on any touched
file (the four pre-existing findings in `01`, `02`, `build.py` are unchanged); the pre-existing
`ruff format` drift in untouched regions of `config.py`/`registry.py`/`run_walking_skeleton.py`
was left alone.

### 2.3 Repairs made — files, tests

| File | Change |
|---|---|
| `src/data/config.py` | `REQUIRED_FIELDS_MAP[("fixtures-and-reproducibility", 1)] = ("seeds.development",)` with its rationale |
| `src/data/acquisition.py` | `select_records_within_window` (additive; exported) |
| `scripts/run_walking_skeleton.py` | window selection before assertion (records read from the month file recorded in the assembly assertion); `build_phase1_commands(code_commit=)` threading; `--code-commit` forwarded from the CLI |
| `scripts/00_acquire_prepared_vtec.py`, `01_inventory_and_registry.py`, `02_standardize_prepared_target.py` | `--code-commit` option, passed to `capture_environment_lock` (mirrors `04`) |
| `tests/fixtures/plumbing_7day/identity_declaration.yaml` | clause prefixes removed; `inputs.prepared_vtec` cited from `evidence/audit_evidence_2022-11/sha256_manifest.json`; SHA-256 `d69114c6…` → `d02c31e5…` |
| `tests/fixtures/scientific_1month/identity_declaration.yaml` | same, from `evidence/audit_evidence_2022-03/`; `8f45fcc5…` → `582da002…` |
| `tests/test_clean_run.py` | `test_assembly_selects_the_cited_window_on_record_dates_then_asserts` (selection then assertion; fail-closed on an unreadable date), `test_build_phase1_commands_threads_the_explicit_code_commit` (every invocation carries it; every script in the sequence declares the option) |
| `kaggle/build_b01_package.py` | packages `evidence/audit_evidence_2022-03/` (the scientific fixture's cited input) beside November's |

The two declarations are owner-adopted records (2026-09-13). The corrections change no
cited value — window, station, clauses, stamps, apparatus partitions and bootstrap constants are
byte-for-byte the same — they add the citation block the loader requires and remove a label the
verbatim check refuses. They are listed as **item 0 of the freeze package** so the owner can
confirm or reverse them explicitly rather than find them by diff.

### 2.4 What the fixtures can and cannot do now

The plumbing measuring run now passes its own preflight, identity agreement, input verification
and record assembly, writes `input_manifest.yaml`, `processing_config_snapshot.yaml` and
`registry_entry.json` under the fixture root, and stops at **stage 00** with an honest
`aborted` registry row naming the refusal. **No measurement exists; no candidate exists; no
receipt exists; neither fixture has completed** — the fixture READMEs' "Neither fixture has ever
run. No measured value exists." stays true. The Kaggle notebook (§1.4) will reproduce exactly
this stop and return the stderr; running it before §2.5 is resolved yields a diagnosis, not
receipts.

### 2.5 The freeze package — every decision that stands between today and a frozen manifest

Presented once, in ladder order, so the owner rules on the whole set rather than meeting them one
Kaggle run at a time. Nothing below was decided by this session.

| # | Decision | Owner | What is asked |
|---|---|---|---|
| 0 | The two declaration corrections (§2.3) | student (Q-31 record owner) | **confirm** (or reverse) |
| 1 | Stage 00 on a fixture run: rule that a fixture-scoped `00` READS the declared derived artifacts (already hash-verified by the orchestrator) and writes its request/sha256 manifests from that evidence, with no live transport — OR rule that `00` is exempt from the fixture sequence until the DATA-07 re-acquisition. Both are sequence-defining rulings on `acquisition`'s READY module; neither is an implementer's default | project decision owner | **rule** (implementation follows the ruling) |
| 2 | `configs/data.yaml: qc_operations` — the closed documented-QC operation list (FR-P1-03-1) | **supervisor** (D-number) | freeze |
| 3 | `configs/features.yaml: feature_set_id`, `feature_dictionary`, `normalization` (TE §6.2/§6.4) | student (D-numbers) | freeze |
| 4 | `permitted_producers` for the seven driver rows — the producing-artifact identities, which exist once the Kp/ap, Hp60/ap60, F10.7 and Dst driver releases exist (D-39/D-40/D-41 identities; D-35 policy) | student | freeze after the driver releases |
| 5 | `configs/experiment.yaml: horizons: [1]` — TE 2.1 already fixes it; the config transcription needs the owner's authorization (Vision §1.2: no implementer fills a sentinel). **Note (correction of this record's first draft):** TE §18.3 precondition 3 / D-31 list *horizons* among the supervisor-signed items, so this is a Student + Supervisor item exercised under the workspace's recorded delegation, not an owner-only one | project decision owner (under the D-1-addendum delegation) | **DONE 2026-09-20 — D-51** |
| 6 | Q-15 — the CODE GIM comparator interpolation rule (`src/external/gim.py`; TE 18.2 student item) | student | freeze |
| 7 | R-59 — the B-01 validation report: the eight official values (§3) and the tolerance (§4); then a fixture-window generation path in `04` (implementation) | student (this workstream) | collect + approve |
| 8 | After 1–7: two plumbing measuring runs on Kaggle → **Q-31 freeze act** for `plumbing_7day` (status frozen, `.sha256`, D-number) → plumbing verification + two scientific measuring runs → **Q-31 freeze act** for `scientific_1month` → both verification runs → receipts | student | two freeze acts, each after its measuring runs |

`models.selected` is written by the tuning run and is not a freeze item; it is listed in §2.2 so
the stage-06 stop is not misread as one.

---

## 3 — Official-reference collection (R-59 area 6)

- **Selection preserved and re-verified.** `sample_selection.json` unchanged. All eight cases are
  outside December 2022; every activity claim re-derives from the January–November rows of the
  audited definitive Kp record with December rows skipped before parsing (334 rows; 0 December
  rows) — `evidence/b01_tolerance_basis_2026-09-20/verify_selection.py` →
  `selection_verification.json`. An extremum over a set that excludes December cannot depend on
  December's values: **December did not influence the selection.** One wording nuance recorded:
  the two 6.33 disturbed cases are not the single most disturbed January–November slots (6.67
  on 2022-04-10 and 2022-08-17); the record claims extremes, not maxima; no case is replaced.
- **Access check, bounded.** One `GET` of `https://kauai.ccmc.gsfc.nasa.gov/instantrun/iri` at
  2026-09-20T08:40:40Z: HTTP 200, 7,633 bytes. No run request was sent; the 2026-09-19 HTTP 429
  refusals were not retried.
- **Sheet delivered:** `kaggle/b01_official_reference_collection_sheet.md` revision 2 — URL,
  the per-case fields (all eight rows with every value), every option with its `jf` mapping, the
  save list with filenames, the station-altitude-versus-integration-limit section, the
  comparability table, and two source-backed alternatives if manual access also fails (the
  legacy CCMC form; the official IRI-2016 Fortran reference build with the pinned index files —
  neither executed).
- **Two facts measured on the pinned wheel that the sheet now states:** (i) `iri_tec` starts at
  100 km whatever `tecLower` ≤ 100 is entered, so the form's lower limit changes nothing on the
  server while the adapter includes 90–100 km (≤ 0.078 TECU); (ii) in this wheel IRI-2016 and
  IRI-2020 return bit-identical Ne under the standard switches, so `version=16` is correct but
  not discriminating.

---

## 4 — Tolerance (R-59 area 7): measured basis, recommendation, limits

**Approved 2026-09-20T12:27:01Z, recorded as D-50** (§8 addendum below). At the time this
section was drafted, `configs/experiment.yaml` still carried `tolerance_tecu` /
`tolerance_declared_at_utc` as `TBD — freeze gate`; D-47's sfu tolerance is not reused; no
adapter value for the eight cases and no official value was computed or seen.

**Method.** The exact pinned wheel (hash-verified; index files at the D-45 pins; the Kaggle
smoke-test value reproduced bit-identically) run on Linux x86-64 under WSL2 over **288
non-December profiles that are not the eight cases** (3 stations × 8 days × 12 hours). A
converged reference integral (0.1 km Simpson), the 90–100 km band, and an emulation of IRI's own
`iri_tec` scheme for `istep` 0/1/2 give the quadrature terms; eight configuration mismatches give
the discriminating power. Scripts and results: `evidence/b01_tolerance_basis_2026-09-20/`.

**Measured (adapter − X):** converged reference +0.004 … +0.062 TECU (all of it `iricore`'s
`_clean_ne_for_tec` step; the 0.5 km sum itself is converged); 90–100 km band 0.0015 … 0.078
(daytime max — revision 1's "≤ 0.02" was wrong by 4×); `iri_tec` istep 1/2 are converged to
< 0.01; **adapter − official under istep 1/2: +0.006 … +0.14** (≤ 0.51 %); **under istep 0:
−0.06 … −0.82** at ≤ 38 TECU (−2.2 % mean, −2.6 % max; ≈ −1.3 TECU at 50 TECU). Display
rounding ± 0.05. **The server's `istep` is unknown** — declared as the one unquantified
assumption. Discriminating power: foF2 model, topside option, B0, storm model and ceiling
mismatches move TEC by 1–7 TECU on at least half the profiles; **the hmF2-model mismatch (the
form's default) moves it by at most 0.45 TECU and is caught by no tolerance** — handled
procedurally (Shubin on the form, screenshot) and by recording the output's hmF2 column.

**Recommendation:** `1.0 TECU` absolute per case, all eight must hold. Substantiated with ≥ 5×
margin for the converged server schemes; marginal only for istep 0 at the highest daytime TEC,
for which a **sign-and-proportionality signature is predeclared** (adapter LOWER by 2–3 % on
every case) so it can be recognised without post-hoc reasoning; a failure is still `failed` and the
predeclared follow-up is the Fortran reference build with a known `istep`, never a widened
tolerance. Full derivation and limits:
`governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md` revision 2. **Decision needed:**
approve 1.0 TECU (the approval instant becomes the declaration time), optionally the hmF2 diagnostic.

---

## 5 — `observable_codes`: scope trace and disposition

**Trace.** Vision §6.2 lists "available observable codes" among the registry contents;
`assert_registry_resolved` (R-45, "carries §6.2 in full") refused on the field regardless of
phase, and `features.build` and `01 --build-registry` call it — so a Phase 1 feature run refused
on a field no Phase 1 computation reads. The authoritative provisions that decide the scope:
Vision §3.6's phase table places "observable/cadence checks" and "Raw-file acquisition and
inventory" under **Phase 2**; Vision's step 8 ("Inventory and inspect raw files and metadata →
coverage/observable/cadence report") is Phase 2; Vision §6.2 itself says values must not be
inferred "from a single RINEX header" — and observable codes are read from RINEX headers, which
TE §7.0 bars Phase 1 from touching. The Phase 1 registry consumers use coordinates and the IGRF
pin only (`station_lat`, `lst_sin`/`lst_cos`; B-01 coordinates). No governing record states the
codes, and no site log carries them.

**Disposition: implementation/schema mismatch with the approved Phase 1 scope; corrected
narrowly, Phase 2 unchanged.** `assert_registry_resolved(registry, *, phase=2)`: under `phase=1`
the module constant `PHASE2_ONLY_REGISTRY_FIELDS = ("observable_codes",)` is not required
(presence or provenance); every other 6.2 field, the 2022 interval coverage, the pinned IGRF
version and the provenance limb are checked exactly as before; the **default `phase=2` is the
full, unchanged R-45 check**. `build_features(..., phase=2)` forwards it; `05` passes
`args.phase`; `01` passes its `PHASE = 1`. **No code was invented and no placeholder inserted**:
`configs/data.yaml` still carries no `observable_codes`, and the Phase 2 gate will keep refusing
until a 2022 RINEX header supplies them under the Phase 2 inventory. Tests
(`tests/test_station_registry.py`): Phase 1 resolves with the field empty and un-provenanced and
nothing was filled in; Phase 2 (explicit and default) refuses; every other limb still refuses
under Phase 1; an invalid phase refuses. Observed effect: `01 --build-registry` on the plumbing
scope now resolves all three stations (it refused on `ARUC: observable_codes` before).

R-45's literal "omit any of the seven → raises" is thereby narrowed for Phase 1 on the strength of
the Vision provisions quoted above and the owner's instruction ("implement a narrow scope-aware
correction without weakening Phase-2 validation"); the functional-design text of R-45 is not
edited (a receipted record) — the narrowing is carried here to the next gate.

---

## 6 — Kaggle package, and the records this pass leaves stale

- `kaggle/dist/tec_b01_package.zip` rebuilt: **200 files**, zip SHA-256
  `362a1aa46d5047c0096b15255fd85e6965e4472db1d977058d725331f763522e`, tree SHA-256
  `455828bd04056f4ba547d744fee1b2332051d970a38cdc335513b8747e62f120`, built at
  `4253d51+dirty`. Full-year generation stays disabled (`RUN_FULL_YEAR = False`).
- **Stale code-summaries, carried to the gate (project.md `gf-3`), not rewritten:** `foundation`
  (`config.py` map entry), `acquisition` (`00`, `acquisition.py`), `inventory-and-registry`
  (`01`, `registry.py`), `target-standardization` (`02`), `features-and-splits` (`05`,
  `build.py`), `fixtures-and-reproducibility` (orchestrator, declarations, `test_clean_run.py`),
  `external-products` (notebook, package builder, `experiment.yaml`, the tolerance proposal).
  Each cross-unit edit above is additive and is routed here as its explicit ruling
  (project.md `c32`); the receipted records are untouched.

---

## 7 — Validation performed

- Full suite in the governed 3.11 environment after the source edits, before the new tests:
  **1346 tests, 0 failures, 0 errors, 4 pre-existing skips** (junit-counted). After the new tests:
  see §7.1 (appended when the run completes).
- Targeted: `test_station_registry.py`, the new and neighbouring `test_clean_run.py` controls,
  `test_release_hashes.py` (the new evidence manifest is parametrised in), `test_locked_test_guard.py`
  (custody inventory clean with the new evidence folder).
- The orchestrator's repaired path exercised on the REAL November file in an isolated copy of
  the workspace (never the repository's registry): 18,183 records read, 1,810 selected, 7/7 days,
  identity and inputs verified, stop at stage 00 as §2.2 states. Both declarations validated
  through the real loader and `assert_identity_agrees_with_decisions`.
- The numerical checks (§4) reproduced the Kaggle smoke test bit-for-bit before any other number
  was read from them.

### 7.1 Full suite with the new tests

(appended below)

Full suite in the governed 3.11 environment with every change of this record in place:
**1365 tests, 0 failures, 0 errors, 4 pre-existing skips** (junit-counted; 1346 before, +5 new
tests, +14 rows of the manifest-parametrised release-hash tests over the seven new evidence files).

---

## 8 — What still requires the owner (nothing here repeats an existing supervisor approval)

1. **Tolerance:** approve `1.0 TECU` per case (§4) — the approval instant is the declaration time;
   optionally the hmF2 diagnostic column.
2. **Eight official values:** collect per the sheet (§3) into `kaggle/b01_validation_samples.json`,
   save the eight text outputs, rebuild the package.
3. **Freeze package (§2.5):** item 0 confirm; item 1 rule (stage 00 fixture-run input path);
   items 2–6 the listed freezes/authorizations (2 is the supervisor's); item 8 the two Q-31 freeze
   acts once measuring runs exist.
4. **Kaggle:** a run of revision 2 before items 1–3 are closed returns the ladder's stage-00
   diagnosis and the runtime checks only; it is not required to close any of the above.

### 8.1 Addendum 2026-09-20 (after the owner's reply "1. approved … 3. approved")

**Closed by the reply:**

- **Tolerance — D-50.** `1.0 TECU` absolute per case, `tolerance_declared_at_utc =
  "2026-09-20T12:27:01Z"` (the approval instant, captured at write time, never backdated).
  `configs/experiment.yaml` updated; the tolerance proposal's status line and §6 updated;
  `tests/test_external_drivers.py::test_b01_config_block_is_the_annotated_d45_contract` updated
  from "still TBD" to the frozen value. The optional hmF2 diagnostic column was **not** part of
  the reply and stays open, unimplemented.
- **Freeze package item 0** — the two identity-declaration corrections (§2.3) — **confirmed**.
- **Freeze package item 5 — D-51.** `horizons: [1]` transcribed from TE §2.1; the stage-06 stop
  in §2.2 row k is cleared; `tests/test_models_smoke.py::test_real_experiment_yaml_transcription_is_internally_consistent`
  updated from "not transcribed" to the frozen value. **Correction of this record's first draft:**
  item 5 was presented as owner-only; TE §18.3 precondition 3 / D-31 list *horizons* among the
  supervisor-signed items, so D-51 is exercised under the workspace's recorded
  student/supervisor delegation and says so — no independent supervisor signature exists or is
  claimed (the D-1-addendum / D-31 pattern).

**NOT closed by the reply, and why a bare "approved" cannot close them** (no value was put to
the owner for these, so nothing was written — TE §18.2/§18.3: no implementer fills a
freeze-gate value by convenience):

- **Item 1 (stage 00 on a fixture run):** two mutually exclusive rulings were offered (a
  fixture-scoped read of the already-verified derived artifacts, or exemption of `00` from the
  fixture sequence until DATA-07). "Approved" does not say which; the owner's choice is asked
  for explicitly in the reply to this record. Nothing implemented.
- **Item 2 (`qc_operations`):** the closed list of documented QC operations must be stated and
  frozen under a D-number by the **supervisor** (FR-P1-03-1). No list exists to approve.
- **Item 3 (`feature_set_id`, `feature_dictionary`, `normalization`):** the dictionary rows and
  the normalization rule must be stated; none has a proposed value on record.
- **Item 4 (`permitted_producers`, seven driver rows):** producing-artifact identities that exist
  only once the driver releases exist.
- **Item 6 (Q-15, GIM interpolation rule):** a TE §18.2 student forbidden choice with no proposed
  value on record.
- **Item 7 (R-59 report):** the eight official values are still to be collected (the tolerance
  half is now closed).
- **Item 8 (Q-31 freeze acts):** follow the measuring runs, which follow items 1–7.

**Validation after the addendum:** `test_external_drivers.py` + `test_models_smoke.py` green;
full suite re-run recorded in §8.2 when complete. Package rebuilt (configs changed).

### 8.2 Full suite after the addendum

**1365 tests, 0 failures, 0 errors, 4 pre-existing skips** (junit-counted). Package rebuilt:
zip SHA-256 `62eb9d2ca1bebf9dd23033f2825dacfed6541a76c744f3560548cbdb7736d838`, tree SHA-256
`b01244acd6ab00d00dfaf09e22199cbdeb277c0d504a847d9d352f6be1f4d21c`, 200 files, at `4253d51+dirty`.

---

## 9 — Second pass, 2026-09-20 (after the owner's reply: hmF2 approved; items 3 and 5 "approved by student and supervisor, countersigned"; item 1 = (a); items 4 and 6 "tell me more"; "check and complete my work"; the Kaggle `--verify-runtime` traceback)

### 9.1 The Kaggle refusal: a language-level Python 3.10 incompatibility, closed

The traceback the owner returned (`ImportError: cannot import name 'UTC' from 'datetime'
(/usr/lib/python3.10/datetime.py)` at `src/data/config.py:107`, reached from
`04 --verify-runtime`) is not a pin problem: §1.1's compatibility check covered the
**dependency** level (50-package cp310 resolution) and not the **language** level. Measured
under a CPython 3.10.21 environment (WSL2, diagnostic): **37 of 37** `src` modules failed to
import — 35 through `datetime.UTC` (3.11+; used in 33 files across `src/`, `scripts/`,
`tests/`, `kaggle/build_b01_package.py`), 2 through `enum.StrEnum` (3.11+; `src/data/splits.py`,
`src/features/transforms.py`). Nothing else 3.11-only was found (`hashlib.file_digest`,
`typing.Self`, `except*`, `tomllib`, `contextlib.chdir`: absent; every `fromisoformat` caller
already strips a `Z` suffix itself).

**Closed by a mechanical, behaviour-preserving sweep (D-49 addendum):** `dt.UTC` →
`dt.timezone.utc` (73 sites; on 3.11 the two names are the same object), the two
`from datetime import UTC` sites likewise; `StrEnum` imported from `enum` on 3.11 and backported
in `src/data/config.py` on 3.10 (`str()`/`format()` return the member value as on 3.11 — checked
on 3.10.21: `str(FieldClass.driver) == "driver"`, equality with the string holds). `ruff` UP017
(which rewrites the object back to the alias) is ignored in `pyproject.toml` with the reason
recorded there. Files: 33 modules, one-line-pattern diffs, no logic touched; `src/data/config.py`
exports `StrEnum` and `UTC`. Main environment: still Python 3.11.16. Pins: unchanged. After the
sweep: 0 of 37 import failures on 3.10; suite results in §9.7.

The two alternatives considered and not taken: (b) building `iricore` from its sdist under
Kaggle's 3.11 (would replace the D-49 pinned wheel `iricore-1.8.0-cp310-…` with a
locally-compiled, non-reproducible binary — a new D-49 decision, and the measured tolerance basis
was taken on the wheel); (c) running the fixtures on 3.11 and only B-01 on 3.10 (the environment
mismatch the D-49 extension exists to remove). The sweep is reversible by the same pattern if
the owner prefers (b).

### 9.2 The owner's collection, checked file by file (item 2 of the 8.1 list)

Eight outputs and a screenshot were found under `kaggle/official_reference_outputs/`. Every
file's **server-echoed header** was compared with its case (§3's table); the header, not the
filename, is authoritative. Result — recorded in the sheet's new §9 and reproduced here:

| Case | Header | Finding | Action taken |
|---|---|---|---|
| 1 | `2022/-7/ 0.0UT` in the file named `…T12Z` | wrong hour — this is case 2's run | renamed to `case_2_ARUC_20220107T00Z.txt` |
| 2 | `2022/-7/12.0UT` in the file named `…T0Z` | this is case 1's run | renamed to `case_1_ARUC_20220107T12Z.txt` |
| 3, 4, 6, 8 | agree | — | accepted |
| 5 | `2022/-216/ 0.0UT`; case 5 is **12 UT** | wrong hour, no matching run exists | kept as `rejected_case_5_BSHM_20220804T00Z_wrong_hour.txt`; **re-run required** |
| 7 | agrees | hour token `T2Z` | renamed `…T02Z` (sheet pattern) |
| screenshot | default form page (2012, 10°/110°), optionals collapsed | proves the IRI-2016 selector only | renamed `form_settings_default_page_not_the_filled_form.png`; the per-option evidence is each output's header block (all §2 options echoed: NeQuick, URSI-88, foF2 storm on, **Shubin-2015 hmF2**, ABT-2009, Scotto-97-no-L, foE storm off, IRI-1990 D, TBT-2012, RBV10+TBT15), which is stronger — no retake needed |

Cause: the current form's 12-hour time picker (`0 UT` = 12:00 AM, `12 UT` = 12:00 PM). Two
deviations recorded, both immaterial by §4's measured bands: the form exposes no `tecLower`
(header echoes `from 50 to 2000.0 km`; the 50–100 km band is ≤ 0.08 TECU daytime and the
server-side scheme starts at 100 km regardless), and the screenshot is not of a filled form.

**Assembly without retyping:** `kaggle/official_reference_outputs/parse_official_outputs.py`
parses every `case_*.txt` (TEC column as printed, one decimal; `t/%`; `hmF2`; the header block
verbatim; retrieval instant from the file's mtime, UTC; the interface URL) and matches each to
its predeclared case by echoed date/hour/lat/lon — a mislabelled file can only fail to match.
It wrote `kaggle/b01_validation_samples.DRAFT.json` (**7/8 filled**) and will write the final
`kaggle/b01_validation_samples.json` only when case 5's correct run is added. The seven
official values were read for this assembly; **no adapter value for any of the eight cases was
computed** (the paired comparison runs only inside stage 04 on Kaggle). One adapter *hmF2* (not
TEC) was evaluated on WSL for case 1 while checking `oarr[1]` is the hmF2 slot (227.026 km;
the official header prints 227.03) — a diagnostic quantity outside the tolerance test, recorded
here so it is not later mistaken for an undisclosed comparison.

### 9.3 hmF2 diagnostic (approved) — implemented

D-50 addendum. `build_validation_report` records `official_interface_hmf2_km` (from the
samples), `adapter_hmf2_km` (one `iricore.iri` call, `version=16`, `oarr[1]`) and
`hmf2_diff_km_diagnostic_no_threshold` per sample; nulls when the sample carries no official
hmF2; never part of `within_tolerance`. Test added (`test_external_drivers.py`, stub `iricore`
gained an `iri` function recording its calls); the notebook's Step 5 prints the column.

### 9.4 Freeze-package item 1 — ruled (a), implemented (D-52)

`scripts/00_acquire_prepared_vtec.py` gains `_run_fixture_scoped`: on a fixture run no
transport is built; `verify_declared_inputs` (moved from the orchestrator into
`src/data/acquisition.py` together with `read_records_csv`, `select_station_records` and a new
`cited_stations`, re-imported by the orchestrator — one guard home, R-135) re-verifies the
scope's artifacts; the cited station(s)' in-window records are selected on record dates and
asserted; `fixture_read_manifest.json` (`retrieval_performed: false`; the month's recorded
`madrigalWeb_version` copied verbatim — `"unknown"`) and a `derived_only` `sha256_manifest.json`
(zero provider files, the four verified artifacts) are written; the registry `completed` row
cites the read manifest. No `request_manifest.json` on this path (R-35 is a retrieval check).
Two tests (`test_clean_run.py`, fresh-process): the read path (edge-dated and other-station rows
selected out, not refused; no transport call; `derived_only` meta with 0 provider / 2 derived) and
the tampered-artifact refusal before any write. **Probe (isolated copy, 3.11):** stage 00
completes with 18,183 rows read / **1,810 BSHM in window** (D-11's figure), stage 01 completes,
and the ladder stops at **stage 02 — `qc_operations` (item 2, supervisor)**.

### 9.5 Items 3 and 5 — what the countersignature statement can and cannot attach to

- **Item 5 (`horizons`)** — D-51 addendum records the owner's statement that the supervisor
  countersigned; the value was already transcribed. Nothing else to do.
- **Item 3 (`feature_set_id`, `feature_dictionary`, `normalization`)** — there was **no value on
  record** to approve or countersign (8.1 said so), so nothing was transcribed. TE §6.2 fixes
  most of the dictionary but leaves **six choices open** that no implementer may make (TE §18.2
  "Any feature, its safe lag, or its missing rule — Student + Supervisor"). The proposed D-53
  text below is offered for adoption; the owner answers the six choice points, the supervisor
  countersigns the answered text, and only then is it transcribed. `experiment.window_length_hours`
  (absent today; `read_window_length` refuses) is part of the same freeze because the reader
  asserts it equals the dictionary's `sequence_steps`.

**Proposed D-53 (draft — not recorded; every `CHOICE` needs the owner's answer):**

> `configs/features.yaml: feature_set_id`, `feature_dictionary`, `normalization` and
> `configs/experiment.yaml: window_length_hours` are transcribed from TE §6.2 / §6.4 as follows.
> Primary-track fields (all producers per D-35; every entry names its `dictionary_row`):
> `vtec_lag_1h`, `vtec_lag_2h`, `vtec_lag_3h`, `vtec_lag_24h` (row `vtec_lag`, `lag_hours`
> 1/2/3/24, `source_column: vtec_tecu`, `normalization: train_only_standardize`);
> `vtec_seq_24` (row `vtec_seq_24`, `sequence_steps: 24`, `source_column: vtec_tecu`,
> `train_only_standardize`); `utc_hour_sin/cos`, `doy_sin/cos`, `lst_sin/cos` (`none`);
> `station_onehot_ARUC/BSHM/NICO` (row `station_onehot`, `station_id`, `none`);
> `station_lat` (**CHOICE 1:** `train_only_standardize` or `none` — TE says "train-only *if*
> scaled"); `kp_safe`, `ap_safe`, `hp60_safe`, `ap60_safe`, `f107_safe`, `f107_81_trailing`
> (`source_series` = the series name each released D-41 driver artifact carries — fixed at the
> driver release, item 4; **CHOICE 2:** scaled (`train_only_standardize`) or `none`, one answer
> for all six or per field). **CHOICE 3:** include `dst` as a diagnostic-class field (built,
> barred from model input by `DIAGNOSTIC_ONLY_SERIES`) or omit it from the dictionary.
> **CHOICE 4:** include `target_support` (row `target_support`, `source_column:
> valid_observation_count`, diagnostic by default, model use needs G-04 `approval`) or omit.
> **CHOICE 5:** `feature_set_id` — a stable identifier for this set (proposal:
> `fs-phase1-primary-v1`). **CHOICE 6:** `window_length_hours: 24` (TE §6.4 "one frozen value
> per feature-set ID"; the sequence field has 24 steps — confirm 24). The RF family's
> "no scaling" (TE §6.2/§6.4) is a family representation applied at model time, not a
> dictionary value. `normalization` (the top-level field) records the rule in words:
> "train-only standardization fitted per fold on the training partition; RF receives the
> unscaled representation of the same information set (TE §6.4)".

### 9.6 Items 4 and 6 — what they are, what the owner is asked for

**Item 4 — `permitted_producers` for the seven driver rows.** A `permitted_producers` entry is
the identity of the **released artifact** allowed to supply a row (D-35 limb 3). D-41 froze the
three producer **identities** (`gfz_kp_ap_3h_2022_v1` → `kp_safe`/`ap_safe`;
`gfz_hp60_ap60_1h_2022_v1` → `hp60_safe`/`ap60_safe`; `srmp_f107_observed_daily_2022_v1` →
`f107_safe`, with `f107_81_trailing` derived from it; Dst has no producer artifact — it stays
diagnostic and unlisted) and their source-file hashes, but **no artifact has been released**:
D-41's "Output SHA-256 / dataset_version" column is empty by decision, and no stage script calls
`src/data/release.py:write_release` for a driver today. So item 4 is two steps, in order:
(i) **implementation** — a driver-release path in stage 04 that builds each D-41 artifact from
its hashed source under TE §13.3 (`write_release`: version, source manifest, SHA-256, schema,
row counts, exclusions) — needs the owner's go-ahead to implement, then the owner's approval of
each of the three releases ("in its own owner-approved step", D-41); (ii) **transcription** —
the six entries `kp_safe: ["gfz_kp_ap_3h_2022_v1"]`, … keyed to the released ids, which is then a
copy, not a choice. Not a countersignature item (D-41: "requires no supervisor countersignature
under §18.2"); the availability floors those releases rely on (D-42/D-43/D-46) are the
Q-16 items whose countersignature was requested 2026-09-19. **Ask:** authorise (i); approve each
release when presented with its manifest.

**Item 6 — Q-15, the CODE GIM comparator interpolation rule.** TE §6.3 already states the rule
in words — *"Bilinear space + linear time with longitude-rotation correction"* — but
`src/external/gim.py` reads it from `experiment.yaml: gim_interpolation_rule`, a TE §18.2
**student** forbidden choice that is unset, and refuses generation while it is (obligation 1);
obligation 2 is a **hand-checked sample interpolation with worked arithmetic, timestamped BEFORE
any comparator generation** (EV-11). Two facts bound it: no CODE final IONEX file has been
acquired yet, and `gim_comparator.parquet` is a TE §15.4 required fixture output — so the
fixture ladder needs Q-15 *and* a CODE product. **Proposed D-54 text (draft):** "For each
station coordinate and target hour t: take the two IONEX maps bracketing t (epochs t₁ ≤ t < t₂);
rotate each map in longitude by the Earth's rotation between its epoch and t
(λ′ = λ + 360°·(t − tᵢ)/86400 s, the IONEX 1.0 'rotated maps' scheme, Schaer et al. 1998);
interpolate bilinearly in latitude/longitude on each rotated grid; interpolate linearly in time
between the two results; a missing bracketing map excludes the hour from the GIM comparison
only (TE §6.3)." **Ask:** adopt D-54 (student decision) — then the config key is set, and the
hand-check is produced against the first acquired IONEX file before any generation.

### 9.7 Validation and package

- Governed 3.11 suite and the 3.10 (WSL2, governed pins) suite: counts recorded in §9.8 when
  complete.
- Notebook revision `b01-production-4`: Step 3c runs the whole suite inside the 3.10 venv before
  any stage run (a failing suite stops the session with junit counts); Step 5 prints the hmF2
  column; the note field names this revision. Package rebuilt (hash in §9.8).
- Records touched: `evidence/DECISIONS.md` (D-52; D-49, D-50, D-51 addenda),
  `governance/proposed/B01_TOLERANCE_PROPOSAL_2026-09-19.md` §6, the collection sheet (rev 3,
  §9), `kaggle/HOW_TO_RUN.md`, `pyproject.toml` (UP017), this record.
- Line endings: several files written on 2026-09-20 had acquired CRLF endings in the working
  tree; normalised back to LF (the two identity declarations re-hash to the values §2.3 records,
  `d02c31e5…` / `582da002…`).

