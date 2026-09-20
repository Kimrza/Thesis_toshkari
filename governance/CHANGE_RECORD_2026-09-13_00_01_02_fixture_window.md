# Change Record — 2026-09-13 — Scope-derived fixture windows in 00/01/02 (Option B) + D-144 acquisition-trio transcription

**Change ID:** `CR-2026-09-13-000102-FIXTURE-WINDOW`
**Authority:** the project decision owner's **FINAL OWNER RULING** of 2026-09-13, in-session,
implementing the owner-review package delivered the same day: **Option B** selected for the
fixture-window mechanism (extend Stage-04's scope-derived windowing to scripts 00/01/02);
the **five-parameter executed identity** selected for `data.acquisition.parameters`
(`ut1_unix, gdlat, glon, tec, dtec` — NOT D-4's nine); the Q-31 fixture declarations
authorized with the owner-supplied apparatus values (§6–§7 of the ruling). This record is
the sanctioned owner instruction `project.md` (`code-generation:c32`) requires for edits to
READY-reviewed units' modules.
**Repository state:** drafted from `HEAD = 8d4297d` (the pre-repair baseline every mutation
probe in §7 is measured against). **Shipped state, re-derived from git 2026-09-15:** the
work this record governs was committed by the student as
`615a367665523c56b922bbe2a05e222ddd291850` (`615a367`, 2026-09-13, parent `8d4297d`),
13 files, and this record was committed inside that same commit. `615a367` is an ancestor
of the current `HEAD = 18843aa7b5da1bf28c903c54155b4187910bbe43` (`18843aa`), which equals
`origin/main` — so the change is shipped and pushed. The drafting-time sentence "No commit
is made by this pass" (§7 carried the same claim) described the authoring pass and was
falsified by the student's own commit act; both statements are corrected here rather than
left standing, per `project.md` (`code-generation:c30`).
**Register discipline:** no agent writes `evidence/DECISIONS.md`. **No new D-number** —
the transcription cites D-144 (with D-4/D-10 as the rationale for the executed five); the
window mechanism decides no scientific value; the fixture apparatus values (§5 below) are
Q-31 student/owner fixture-design choices, explicitly "NOT changes to the scientific thesis
model specification … the reproducibility fixture harness only" (ruling §5). No supervisor
countersignature (Q-31 is student-owned per `team.md`; D-3/D-144 already countersigned).

This record is written FIRST, before any code, config, test, or declaration edit.

---

## 1. What this pass changes, and why

**The deadlock's remainder.** `CR-2026-09-13-04-FIXTURE-WINDOW` repaired stage 04. Scripts
00/01/02 carried the sibling defect in config form: their fixture-run declaration reads
`acquisition.window_start/window_end` from `configs/data.yaml` — fields that do not exist —
so every fixture run refuses at `_declared_data_window`. Worse, no single static pair can
ever serve both fixtures: **D-11 (2022-11-01..07) and D-14 (2022-03-01..31) are disjoint**,
and TE §13.2's clean run executes both fixtures in one ordered command sequence, which a
per-campaign config edit would interrupt mid-fence. The owner therefore selected Option B:
on fixture runs, 00/01/02 derive the effective window **from the fixture scope**, exactly as
04 now does, and the ACTUAL reads/processing are restricted to it — the declaration is made
true by narrowing the reads, never the report. The `acquisition.window_start/window_end`
pair is **deliberately NOT added**: it stays reserved for the future real re-acquisition
window (DATA-07 work), keeping the field's meaning clean.

## 2. D-144 acquisition-trio transcription (`configs/data.yaml`)

New governed block, register-derived values only:
`acquisition.experiment: 8000` (D-3/D-144: Madrigal instrument 8000, World-wide GNSS
Receiver Network); `acquisition.kindat: 3500` (D-3/D-144: "TEC binned 1 degree by 1 degree
by 5 min"; kindat 3505/3506 excluded by the same decision);
`acquisition.parameters: [ut1_unix, gdlat, glon, tec, dtec]` — **owner ruling**: the
executed five, per D-17's recorded request identity ("confirmed identical across all twelve
monthly request manifests") and D-10's correction routing the four drivers to their governed
external sources; D-4's nine-parameter list is NOT used. Unlocks
`REQUIRED_FIELDS_MAP[("acquisition", 1)]`'s §18.3 preflight on script 00.

## 3. Option B — exact control points (Stage-04 precedent)

| Script | Declaration seam | Reads-narrowing (the load-bearing half) |
|---|---|---|
| `00_acquire_prepared_vtec.py` | `_stage_entry`: fixture branch loads the scope via the one loader (`load_fixture_scope`), declares `scope.window`, carries `audit_window`/`fixture_scope_id` in the entry; non-fixture unchanged (`declared_window=None`) | `_run`: on fixture runs, after the R-31 locked-month screen, **every retrieved/read record is asserted within the window** (`assert_records_within_window`, R-31's helper consumed, never copied) — an out-of-window record REFUSES |
| `01_inventory_and_registry.py` | same seam | **Structural, not a window assertion** — corrected 2026-09-15 against the shipped diff. This script's ONLY month-record reading path is the December audit, and the pre-existing `_refuse_fixture_audit` refuses it under ANY fixture scope, so on a fixture run no month directory is read, counted, or required at all; the inventory path consumes release manifests by ID and hash, never records. 01 imports no `assert_records_within_window` |
| `02_standardize_prepared_target.py` | same seam | `_run_standardize`: on fixture runs the **standardized rows** are asserted within-window — `load_released_provider_rows` → `standardize_hourly_target` → `assert_records_within_window(result.rows, timestamp_key="interval_start_utc")` → `write_target_rows_csv`. The bound sits AFTER standardization and BEFORE the first destination write. The `qc_operations` refuse-to-RUN stays first and untouched |

### 3a. Correction to §3 — documentation only, 2026-09-15

The two rows above were rewritten because the drafted text described an intended shape that
the shipped commit `615a367` does not implement. Verified line-by-line against the working
tree at `HEAD = 18843aa` (no source file differs from `615a367` for these three scripts):

- **01 — the drafted claim was false in two limbs.** It said `_month_dirs` enumeration is
  "bounded to months intersecting the window on fixture runs" and that "merged records
  [are] additionally asserted within-window before `attribute_records_by_month`". Neither
  shipped. `scripts/01_inventory_and_registry.py` imports no `assert_records_within_window`;
  `_month_dirs` (def line 472, sole call line 618) is unchanged from the pre-repair form;
  and there is no window assertion before `attribute_records_by_month` (line 640). What the
  shipped script actually relies on is `_refuse_fixture_audit`, which was already present
  before this pass. The row now states that mechanism. Note the consequence honestly: on a
  fixture run 01 **refuses** its only record path outright rather than **narrowing** it —
  §1's framing ("the declaration is made true by narrowing the reads") holds for 00 and 02
  but not for 01, where truth comes from the path not executing at all.
- **02 — the control point was misplaced.** The drafted claim put the assertion on raw
  provider rows *before* `standardize_hourly_target`. It shipped *after*, on
  `result.rows`. The reason is in the code comment and is a real constraint, not an
  oversight: provider rows carry unix-second stamps, while the bound is asserted through
  R-31's ONE date reader, which needs the standardized rows' ISO `interval_start_utc` —
  adding a second parser for the provider form would have duplicated that reader. The
  guarantee that matters is unaffected: the assertion still precedes
  `write_target_rows_csv`, so no out-of-window row reaches a destination artifact and the
  aborted registry row stays honest.

### 3b. Follow-up observation — dead entry fields in 01 (NOT repaired in this pass)

Recorded rather than fixed: repairing it would be a code change outside the shipped repair,
and this is a documentation-only pass. Read/write trace over `scripts/`, `src/` and
`tests/`:

| Symbol | 00 | 01 | 02 |
|---|---|---|---|
| local `audit_window` in `_stage_entry` | live | **live** — bound to `declared_window` (line 318), which feeds `require_receipts_for_snapshot`; also pinned by `test_clean_run.py::_assert_entry_passes_declared_window` | live |
| local `fixture_scope_id` | assigned only | **assigned only** | assigned only |
| entry key `"audit_window"` | read (00 line 379) | **never read** | read (02 line 374) |
| entry key `"fixture_scope_id"` | no production read; asserted by `test_clean_run.py:2331` | **never read** | no production read, no test read |

So in 01 the local `audit_window` IS load-bearing and must not be removed, while
`fixture_scope_id` and both entry-dict keys (lines 317, 321, 338–339) are genuinely dead:
no production reader (`_run_inventory`, `_run_registry`, `_run_audit` and `main` read only
`snapshot` and `lock`) and no test reader — the entry-dict assertions in `test_clean_run.py`
target module 00, not 01. They are best read as structural parity with 00/02/04 rather than
as controls, and **this record does not describe them as active controls**. `fixture_scope_id`
is likewise unread in 02. Disposition owed to the owner at the next gate: keep for parity
with an explicit comment saying so, or remove. No code was changed here either way.

`_declared_data_window(snapshot)` is **kept in all three scripts** (docstring updated as
04's was): it remains the config-based declaration for the future real-acquisition window;
the fixture path never consults it. **Untouched by this pass:** `src/data/fixture_gate.py`,
`scripts/run_walking_skeleton.py`, `PHASE1_SEQUENCE`, every frozen decision, every refusal
gate, datasets, the locked test, the main experiment configuration.

**ML-01 / Rec-2 preservation.** The endpoint check in `fixture_gate.py` still runs against
every declared window; what changes is that 00/01/02's fixture-run declarations become true
by construction because the reads themselves are bounded — and the protection's teeth move
DOWN to record level. Stated per script, corrected 2026-09-15 to match the shipped diff:
in **00** an out-of-window retrieved record REFUSES; in **02** an out-of-window standardized
row REFUSES before the first write; in **01** there is no record-level bound at all, because
the only record-reading path is refused wholesale on a fixture run (§3a). The drafted phrase
"records/rows/month-dirs … excluded at the point of processing" overstated 01: no month
directory is filtered, because none is enumerated on that path. No control is deleted; the
config-refusal controls are migrated to the new truth (§4).

## 4. Tests — migrated and added

Existing window controls live in exactly three modules (derived by grep, not assumed):
`tests/test_clean_run.py` (fixtures unit), `tests/test_december_audit.py` (inventory unit),
`tests/test_external_drivers.py` (04 — already migrated under the 04 CR). Controls in the
first two asserting "fixture exemption refuses while `acquisition.window_*` is undeclared"
are **re-pointed** (CR-2026-09-10 pin-guard precedent), never deleted. New controls per
script (04's pattern): (1) load-bearing out-of-window control, mutation-proven to FAIL
against pre-repair HEAD; (2) AST/declaration-truth pin — the fixture branch consumes
`scope.window`, never `_declared_data_window`; (3) non-fixture invariance. Homes:
`tests/test_acquisition.py` (00), `tests/test_december_audit.py` (01),
`tests/test_prepared_target_schema.py` (02).

**Correction to (1), 2026-09-15 — 01 is the exception.** The shipped 01 control,
`test_december_audit.py::test_optionb_01_fixture_runs_read_no_month_records` (line 829), is
not an out-of-window control, because 01 carries no window bound (§3a). It pins the three
legs that make the declaration true instead: the audit limb raises under any fixture scope
(behavioural), `_run_inventory`'s source contains neither `_month_dirs` nor
`_read_month_records` (structural), and `_stage_entry`'s fixture branch derives from
`load_fixture_scope`/`scope.window` and never mentions `_declared_data_window` (structural).
Two of the three legs are source-text assertions, so they pin the shape rather than the
behaviour — weaker than 00's and 02's runtime bounds, and stated here rather than counted
as equivalent. 00's and 02's controls are out-of-window controls as drafted; the §7 mutation
probes confirm all of them bite against the pre-repair baseline.

## 5. Q-31 fixture identity declarations (owner-authorized values)

Written to `tests/fixtures/plumbing_7day/identity_declaration.yaml` and
`tests/fixtures/scientific_1month/identity_declaration.yaml`, with **no placeholders**:
windows/stations/citations from D-11/D-20/D-14; limitation clauses and the DATA-07 caveat
verbatim from the register/`team.md`; `creator: Kimia Rezaei`; TE §13 stamps per the ruling
(`phase_id: P1A`, `source_id: GNSS_VTEC`, `target_definition_id: GRIDDed_VTEC_1H` — distinct
from IRI/GIM identifiers, representing the D-17 gridded VTEC target); scientific apparatus
partitions **FIX-MAR-FOLD-01** (train 2022-03-01..14, validation 2022-03-15) and
**FIX-MAR-FOLD-02** (train 2022-03-01..21, validation 2022-03-22) — chronological folds,
ids outside the six frozen, no refit; fixture bootstrap `replicates: 1000`,
`scored_range.hours: 336`, `block_counts {24h: 14, 48h: 7}` (336 = 14 days, divisible by
both block lengths; deliberately reduced from the governed 10,000 and never presentable as
the final scientific bootstrap result; **no new seed** — seed semantics stay with
`seeds.yaml`'s governed bootstrap seed). **Literature boundary (ruling §8):** these are
literature-informed fixture-design choices, not claims that any cited paper prescribes these
exact values; no literature reference or thesis methodology changes because of them.
Both declarations are validated against the real validator (`load_fixture_scope`) before
this record's results section is filled.

## 6. Stage-record / READY carry-forward (gf-3)

`00`/`01`/`02`, `test_acquisition.py`, `test_december_audit.py`,
`test_prepared_target_schema.py`, `test_clean_run.py` and `configs/data.yaml` belong to
`acquisition`, `inventory-and-registry`, `target-standardization` and
`fixtures-and-reproducibility` — READY-receipted units whose code-summaries become stale
under this ruling. **No receipt is rewritten**; the staleness is carried here and in the
`build-and-test` stage diary to the next gate, per `project.md` (`gf-3`).

## 7. Results — appended 2026-09-13 after execution

**Evidence classes, labelled per the ruling:** everything below is **local real-CPython
evidence** (the governed pin 3.11.16) executed under the **stdlib-only stand-in runner**
(NOT pytest) — **smoke evidence only, never governed** (TC-03g: governed runs are
in-Kaggle; no real pytest exists on this clone). **No governed evidence exists or is
claimed.**

**Module regressions + migrated/new controls (stand-in, real 3.11.16):**

```
tests/test_acquisition.py               57 fn  57 pass  0 fail   (56 -> 57: +optionb_00 record-bound control)
tests/test_december_audit.py            63 fn  63 pass  0 fail   (62 -> 63: +optionb_01 no-month-reads control)
tests/test_prepared_target_schema.py    56 fn  63 cases 0 fail   (55 -> 56: +optionb_02 row-bound control)
tests/test_clean_run.py                 64 fn  61 pass  3 skip 0 fail  (same profile as pre-migration;
                                        the Option-B helper passes against ALL FOUR scripts 00/01/02/04)
```

The `test_clean_run` migration also REPAIRS a latent breakage: the 04 fixture-window
commit (`8d4297d`) had invalidated the old single-binding AST helper for script 04, and
`test_clean_run.py` had not been run since — the migrated helper is green against 04's
repaired shape (`nonfixture_full_year=True`).

**Mutation probes — pre-repair 00/01/02 extracted from `HEAD = 8d4297d` into the session
scratchpad (repository untouched): 5/5 checks show the defect → CONTROLS BITE:**

```
pre-repair 00::_run has the record bound: False
pre-repair 00::_stage_entry derives from scope: False
pre-repair 01::_stage_entry derives from scope: False
pre-repair 02::_run_standardize has the row bound: False
pre-repair 00 declaration on undeclared config REFUSES: IntegrityError (the deadlock)
```

**Q-31 declarations — written and validated.** Both
`tests/fixtures/plumbing_7day/identity_declaration.yaml` and
`tests/fixtures/scientific_1month/identity_declaration.yaml` validate through THE one
loader (`load_fixture_scope`) from their repo paths, on their own file bytes
(`parsed=json.loads(<file bytes>)` — the files are JSON text, which YAML 1.2 parses
identically; this module's own apparatus convention). No placeholders; every governed
value register-cited (D-11/D-20/D-14 windows, stations, verbatim limitation clauses, the
canonical `DATA07_CAVEAT` constant from `src.data.inventory`, on-disk-verified
eligibility sources); the owner-ruled §5–§7 values (stamps `P1A`/`GNSS_VTEC`/
`GRIDDed_VTEC_1H`; folds `FIX-MAR-FOLD-01/-02`; bootstrap 1000/336h/{24h:14, 48h:7})
transcribed exactly. Residual, disclosed: a pyyaml round-trip parse of the files is owed
on a pyyaml-bearing host (json.loads is the exact parse of this text; the production
loader refuses by name without pyyaml on this clone).

**Compile/format:** all eight edited/created code+test files `py_compile` clean; max line
length ≤ 98 (bound 99); scoped `git diff --check` clean. `ruff` remains uninstallable —
owed with the suite's first real-pytest run.

**Environment limitations (unchanged):** pyyaml/pytest/numpy/pandas/TF uninstallable
(PyPI blocked); the fixture ladder itself was NOT run (measuring runs need a
pyyaml-bearing host — realistically Kaggle — plus the remaining freeze chain: stations,
qc_operations, features/folds); no candidate manifest, no freeze act, no
`fixture_manifest.sha256` (HARD STOP honoured).

**Commit state — corrected 2026-09-15 from git, superseding the drafted "No commit was made
by this pass."** The student committed the work as `615a367` on 2026-09-13 (parent
`8d4297d`, 13 files), including this record, and its message cites
`CR-2026-09-13-000102-FIXTURE-WINDOW` together with D-144/D-4/D-10 for the transcription and
D-11/D-14/D-20 for the declarations, as the drafted sentence anticipated. `615a367` is an
ancestor of `HEAD = 18843aa`, which equals `origin/main`: shipped and pushed. The drafted
claim was true when written and false once committed; it is corrected rather than deleted so
the record shows what changed (`project.md`, `code-generation:c30`).

The evidence classes above are unchanged by this correction and are **not** upgraded by the
commit: the runs remain local stdlib stand-in on CPython 3.11.16, **smoke evidence only**.
No governed Kaggle execution, no real pytest run, and no build-and-test artifact set exists
or is claimed.

---

## 8. Documentation-repair pass — 2026-09-15 (no code, config, test or decision changed)

Scope of this pass: the header's repository-state block, §3's 01 and 02 rows, new §3a/§3b,
§3's ML-01 paragraph, §4's correction note, and §7's commit-state paragraph. Nothing else.

Verified before editing, from git rather than from any earlier report:
`HEAD = 18843aa7b5da1bf28c903c54155b4187910bbe43`; `origin/main` identical;
`git merge-base --is-ancestor 615a367 HEAD` returns true; `615a367` changed 13 files; the
three scripts' current bytes match `615a367`.

Not done, deliberately: `615a367` was not reverted, amended or altered; no production code,
test, config or fixture declaration was touched; no frozen decision, D-number or scientific
value was changed; the append-only audit shard was not cleaned or rewritten; nothing was
staged, committed or pushed. The §3b dead-field disposition is left open for the owner.
