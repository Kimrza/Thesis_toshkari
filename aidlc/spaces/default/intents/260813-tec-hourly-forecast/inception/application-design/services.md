# Services — Hourly VTEC Forecasting (TEC_Project Phase 1)

Stage 2.6 (application-design), intent `260813-tec-hourly-forecast`.

## Sources

- Requirements: `../requirements-analysis/requirements.md` — REQ-ENG-1, REQ-ENG-3,
  REQ-ENG-11, FR-WS-1 through FR-WS-7.
- Affirmed practices: `../practices-discovery/team-practices.md` — two platforms,
  the `NN_verb_noun.py` convention, `--config configs/` on every stage script,
  and "deployment means dataset and model releases".
- Authority: TE v3.3 §7.0 (the P1-00…P1-06 stage table), §9.1–9.3 (platforms and
  the resource envelope), §12 (the nine scripts), §13.1–13.2 (run records and the
  clean-run sequence), §14 (notebooks), §15 (fixtures).
- Stage answers: Q3, Q5, Q6, Q7, FU-1.

## There are no services here, and that is the design

**This pipeline has no deployable service, no network surface, no database and no
user interface.** It is a single-process, CPU-only, offline batch pipeline whose
"deployment" is an immutable dataset or model release (`team-practices.md`
§ Deployment, TE §13.3). So this document does not describe request handling,
sync-versus-async messaging, service discovery, scaling policy or an API gateway
— there is nothing for those to attach to.

What it describes instead: the **nine stage scripts as pipeline stages**, their
ordering contract, the two execution platforms, and what each stage must record.

**UX and interface design: `N/A`.** `aidlc-design-agent` supports this stage in
the framework's default topology. There is no user-facing surface to design:
the five notebooks are review and presentation surfaces for one author and one
supervisor, and their content is fixed by TE §14 rather than by interaction
design. Recorded as not-applicable with that reason rather than left silently
unaddressed, and no wireframe, accessibility or component-spec obligation is
inherited by Construction from this stage.

## The nine stage scripts

Each takes `--config configs/`. Phase-aware stages additionally take
`--phase 1|2`. Each is orchestration only: reusable logic lives in `src/`
(TE §7, quoted, and the affirmed practice that notebooks and scripts do not own
production logic).

| Script | TE §7.0 stage | Phase | Reads | Writes |
|---|---|---|---|---|
| `00_acquire_prepared_vtec.py` | P1-01 | **1 only** | provider API, `configs/data.yaml` | provider files, `request_manifest.json`, `sha256_manifest.json` |
| `01_inventory_and_registry.py` | P1-02 | 1 and 2 | acquired artifacts, site logs | source inventory (§5.1 nine fields), station registry |
| `02_standardize_prepared_target.py` | P1-03 | **1 only** | provider files | Phase 1 target rows, D-17 contract |
| `02_build_vtec_target.py` | P2 target | **2 only** | RINEX, DCB | Phase 2 target rows, ten-field contract |
| `03_verify_processing.py` | P1-03 verification | 1 and 2 | target rows | verification report, uncertainty budget |
| `04_build_external_products.py` | P1-04 | 1 and 2 | IRI, GIM, drivers | benchmark, comparator, driver series |
| `05_build_features_and_splits.py` | P1-04/P1-05 | 1 and 2 | target, drivers, registry | feature matrix, sequence tensor, folds, masks |
| `06_train_and_predict.py` | P1-05 | 1 and 2 | features, folds | per-seed predictions, three-seed mean, checkpoints |
| `07_evaluate_and_report.py` | P1-06 | 1 and 2 | predictions, benchmark, mask | metrics, bootstrap intervals, breakdowns, figures |
| `run_walking_skeleton.py` | orchestrator | 1 and 2 | `--fixture` | fixture run log |

**The `02` ordinal collision is a §12 defect, not a design choice.**
`02_standardize_prepared_target.py` (Phase 1) and `02_build_vtec_target.py`
(Phase 2) share the ordinal in §12's tree. Reading adopted here: the ordinal
denotes the **pipeline position**, and the two scripts are the Phase 1 and Phase 2
realisations of the same position — never both run in one execution, because
`--phase` selects exactly one. The clean-run sequence therefore contains one `02`
per phase. This is recorded as a defect in the source rather than resolved:
renaming either script is a §12 amendment this stage does not make, and
`code-generation` must not invent a `02a`/`02b` convention without one.

## Stage entry contract

Every stage script's `main()` performs these steps **in this order**, before any
domain work:

1. `ensure_process_determinism(argv)` — FU-1 = D. Re-exec with `PYTHONHASHSEED`
   set if unset. **First statement, before any framework import**, since a
   re-exec after TensorFlow loads is pointless.
2. `load_configs(config_dir, phase=phase)` — the only read of `configs/`.
3. `assert_no_tbd(...)` and `assert_declared_sources_exist(...)` — the §18.3
   preconditions, including the source-and-hash clause `DATA-13` restored.
4. `assert_phase_boundary(phase, loaded_modules=sys.modules)` — Q3 = B. Under
   `--phase 1`, refuses to proceed if any `src.gnss` module is loaded.
5. `seed_everything(snapshot, stage=...)` — Q6. TensorFlow op determinism before
   any graph construction.
6. Open the run record: write the environment lock (§13.1's eight items) and the
   experiment-registry `started` row **before** domain work, so an aborted run is
   already visible.

Steps 1–6 are identical in all nine scripts and are the reason `config.py` exists
as a module rather than as nine copies. Step 4 is skipped only by
`02_build_vtec_target.py`, which is Phase 2 by definition and asserts
`phase == 2` instead.

**On failure in steps 1–5**, the script exits non-zero with a message naming the
file and the violated expectation, and writes an experiment-registry row with
status `aborted` and the reason. It does not proceed with a warning: these are
integrity violations under the team's affirmed two-tier posture.

## Ordering contract

```
ensure_process_determinism
        ↓
plumbing_7day fixture  ──►  scientific_1month fixture  ──►  any full-year job
        ↓                            ↓
   smoke only                  scientific evidence
```

**Both fixtures must pass, in order, before any full-year job** (TE §9.2,
TC-03f, FR-WS-1). The seven-day fixture is a **smoke test and never scientific
evidence** — it may not be cited, plotted as a result, or interpreted as skill.
`run_walking_skeleton.py` enforces the ordering; it does not merely document it.

Within a phase, the nine stages run in ordinal order, and §13.2's clean-run
sequence is the authority on the exact commands. Each stage reads only artifacts a
prior stage released, identified by release ID and verified by hash — never by
path convention, so a stage cannot silently consume a stale artifact.

**Precondition currently unmet.** § Known defects row 12 in `requirements.md`
records the `plumbing_7day` station count as contested: TE §15.1 mandates one
station, D-11 froze the window across all three cells, and no reading is adopted.
`tests/fixtures/plumbing_7day/fixture_manifest.yaml` **cannot state its identity**
until that is resolved, and `run_walking_skeleton.py` reads that manifest. This
design names the dependency rather than picking a station count — that choice is
supervisor-owned.

## Execution platforms

Exactly two, and no third is authorised (TC-03c). Google Colab and Google Drive
are removed as governed platforms.

| | Kaggle | Local |
|---|---|---|
| Role | Primary compute; the Phase 1 acquisition and audit host | Development, small tests, fixture runs, review |
| Roots | `/kaggle/working`, `/kaggle/input` | a local tree |
| Credentials | platform secret store | environment configuration excluded from version control |
| Governed runs | yes | yes |
| git working tree | **no** | yes |

**Q7 = C in practice.** Roots are resolved at runtime by
`resolve_platform_roots(env)` and the resolved values are written into the run's
environment lock. Credentials come from the environment and reach the provider
client directly — never through a config file, a log, a registry note or a
notebook (§10, NFR-SEC-01). No machine path enters the four governed configs, so
moving a directory never changes a governed hash and never trips §13.7's
exact-equality check.

**The Kaggle session has no git working tree**, which is why `project.md`
§ Mandated requires the critical test set and both fixtures to run **inside the
Kaggle session** before any governed run executed there: a commit hook cannot
fire, and a local suite run proves nothing about the environment the governed run
actually executes in. This is also why Q3 = B put the phase-boundary guard at run
time rather than leaving it to the test suite.

**Cross-platform transfer** (TE §9.1): every artifact crossing between the two
carries a SHA-256 manifest and the transfer itself is recorded. `platform` is a
required field of every registry row, and a run whose recorded platform is
neither Kaggle nor local **fails** — the falsifiable form `BENCH-09` asked for,
since the absence of a third-platform record is not itself evidence none was
used.

## Resource envelope

TE §9.3's **10.0 GB** hard planning envelope, with TC-03, TC-03a, TC-03b and
TC-03g all `binding: hard`. Every run records CPU/GPU type, runtime, peak memory,
platform and environment hash (TE §9.2, REQ-ENG-11). **CPU is a complete
execution path, not an emergency mode** — GPU is an optional accelerator and
never a dependency of any result. `07_evaluate_and_report.py` carries the heaviest
CPU cost: 10,000 bootstrap replicates over 24-hour vector blocks.

## Run record and registry

Q5 = C. Two artifacts, one authoritative:

| Artifact | Status | Written by | Shape |
|---|---|---|---|
| `experiment_registry.jsonl` | **authoritative** | every stage script | append-only, one line per run event |
| `experiment_registry.csv` | **derived** | `07_evaluate_and_report.py` and on demand | regenerated by folding the JSONL; hashed; marked derived |

Append-only is what satisfies NFR-AUD-01 by construction: a failed or aborted run
stays visible with its status and reason because removing its line would require
rewriting a file nothing rewrites. Status transitions **append a new row**
referencing the run ID rather than mutating the original. Silent reruns are
therefore impossible to hide — two `started` rows with one `completed` is visible
in the log.

The derived CSV exists because §13.4 and TA-10 assume a human reviews the registry
at a gate, and folding JSONL by eye does not scale. It is marked derived and
hashed, so a corrupted CSV is never data loss — it is regenerated. Under the
affirmed two-tier posture, a stale CSV is a completeness shortfall recorded in the
run manifest, not a fatal error.

## Assumptions & Open Questions

- **[assumption]** `run_walking_skeleton.py` is the only script that invokes other
  scripts. The nine stages are invoked directly by §13.2's sequence, which is why
  FU-1 = D put the re-exec in every script rather than only in the orchestrator.
- **[Q7]** The environment-variable names for roots and credentials are not fixed
  here. `README.md` documents them (REQ-ENG-1 lists it in the §12 tree); naming
  them is `functional-design` or `code-generation` work.
- **Open.** The `02` ordinal collision is recorded, not resolved.
- **Open.** `plumbing_7day`'s station count blocks its fixture manifest. Supervisor.
- **Open.** Whether `03_verify_processing.py` has meaningful Phase 1 work is
  undecided: its §12 responsibility is "6 station-days, 2 references,
  sensitivities, uncertainty budget", and four of Vision §6.9's six uncertainty
  contents are Phase 2 quantities barred from Phase 1 (§ Known defects row 11).
  The script exists in both phases; its Phase 1 scope is thinner than its
  description implies, and `functional-design` should settle exactly what it runs.
- **None** of the above adopts a reading on a supervisor-owned value.
