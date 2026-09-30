# Environment identity snapshot: native-Windows `tec-thesis-311` (2026-09-30)

**Purpose.** This record implements the Student's ruling on `GOV-2026-09-29-PV-02`
Recommendation 7, option 2: keep `tec-thesis-311` as environment (a) and record its complete
freeze and conda list as its governed identity, instead of rebuilding it from the locks. The
authority is `governance/CHANGE_RECORD_2026-09-30_GOV-PV-02_rulings.md`.

**Status: pre-restore baseline, NOT the governed identity yet.**
- Under the proposed D-83 (revision 4, §R4-4 item 1(a); §R3-4 item 3), the governed identity of
  environment (a) is the snapshot taken **after** `ml_dtypes==0.5.3` is restored (§R5-4 item 8),
  hashed and cited by that hash. *(Section references corrected 2026-09-30, `GOV-2026-09-30-PV-03`
  Rec 25. They previously read "§R4 item 1(a)" and "§R5 item 8", which are revision-2 numbering.)*
- **What the record permits** *(added 2026-09-30, PV-03 Rec 8)*:
  - **Conformance, yes.** It can **verify** that an installed environment matches, by comparing
    the installed state with this record.
  - **A rebuild, no.** It cannot rebuild environment (a):
    - `pip freeze` carries no artifact hashes;
    - it includes a non-resolvable `pip @ file:///home/task_…` line;
    - the conda list carries md5 digests of Anaconda `pkgs/main` URLs, so a rebuild depends on that
      channel still serving those builds.
- This snapshot records the state before that restore. It is the evidence for the full-drift
  disclosure.

**Captured:**
- **When:** 2026-09-30, read-only. The commands only list and freeze; they install and remove
  nothing.
- **Interpreter:** `C:\Users\LOTUS\anaconda3\envs\tec-thesis-311\python.exe`.
- **Host:** `LAPTOP-TV4UGFBC`.

| File | What | SHA-256 |
|---|---|---|
| `pip_freeze_all.txt` | `python -m pip freeze --all` | `16d54cce68f1936e3a1f1b501f5d2039f768b97d1ebd4c7efaeed7f86b705cc6` |
| `conda_list_explicit_md5.txt` | `conda list -p <env> --explicit --md5` | `0f91d00b5bf157895e556677e5d25fe8c5bfba967a0e510c77226aa4f30254de` |
| `conda_list.txt` | `conda list -p <env>` | `9789f551e3a399d5ce4481f185b7334d39331dc05384482521e723e61cc44688` |
| `interpreter.txt` | `sys.version`, `platform.platform()`, `platform.processor()` | `14e5025f15d0df7ea308f7126052bce524dc1bb205c021d6041b405b1b0f679b` |

## Drift against the committed pins

These figures were derived by script from the files above and printed before being written here.

**Against `requirements.txt`:** 1 of 10 exact pins drifts.
- `ml_dtypes`: pinned 0.5.3, installed 0.5.4.

**Against `environment/wheels-win64.lock`:** 3 of 32 entries drift.

| Package | Pinned | Installed |
|---|---|---|
| `ml_dtypes` | 0.5.3 | 0.5.4 |
| `setuptools` | 84.0.0 | 83.0.0 |
| `wheel` | 0.48.0 | 0.47.0 |

**Pip-installed packages in neither lock:** 22 of the 61 pip-installed packages.
- `cloudpickle`, `colorama`, `contourpy`, `cycler`, `distlib`, `filelock`, `fonttools`, `iniconfig`,
  `joblib`, `kiwisolver`, `pillow`, `platformdirs`, `pluggy`, `pyparsing`, `python-dateutil`,
  `python-discovery`, `pytz`, `scipy`, `threadpoolctl`, `tzdata`, `uv`, `virtualenv`.
- Their versions are therefore not governed by any committed lock. For example, `scipy` is
  1.17.1.

> **Correction (2026-09-30, `GOV-2026-09-30-PV-03` Rec 1).** The paragraph above is left as first
> written, and it is **wrong**. The first derivation compared the 22 packages against
> `wheels-win64.lock` and `requirements.txt` only; it never checked `conda-win64.lock`.
>
> **Re-derived against both locks.** The script name-normalises each package, and maps the pip
> `tzdata` to the conda `python-tzdata`, since the conda `tzdata` package is the system
> time-zone database. The result was printed before this correction was written.
>
> **Where the 22 packages actually sit:**
> - 22 pip packages lie outside the wheel lock and `requirements.txt`.
> - **16 of them are pinned in `conda-win64.lock`.** That includes `scipy` 1.17.1, which matches
>   the lock.
> - **Only 6 are in neither lock:** `distlib`, `filelock`, `platformdirs`, `python-discovery`,
>   `uv`, `virtualenv`.
>
> **Version drift against the conda lock**, which the paragraph above did not disclose:
> - `fonttools` is installed at 4.65.0; the lock pins 4.66.0.
> - `pytz` is installed at 2026.3.post1; the lock pins 2026.4.
>
> **Conda layer:** of the 20 installed conda packages, **none has a build string matching the
> lock**.

**Conda layer:** 20 packages installed, against 119 entries in `environment/conda-win64.lock`.
- The Python build is `python-3.11.16-hb00fc5c_0` from Anaconda `pkgs/main`.
- The lock pins conda-forge `python-3.11.16-hb12b558_2_cpython`.

## What this means

- **Environment (a) was not built from the committed locks.** The D-71 offline rebuild produced
  the locked environment on another host; `%LOCALAPPDATA%\tec-envs\tec311` does not exist on this
  laptop.
- Under Recommendation 7 option 2, this is **accepted and disclosed**: environment (a) is
  identified by its recorded freeze and conda list, **not** by the committed locks.
- Consequence for G-07: the environment is reproducible from this record, not from the committed
  locks. The Student accepted this trade-off when ruling option 2.
  > **Correction (2026-09-30, `GOV-2026-09-30-PV-04` Rec 22).** The bullet above is wrong, and is
  > left as first written. This record supports **verification only, not a rebuild**. See "What
  > the record permits" near the top of this file, and PV-03 Rec 8.
- The Student's Recommendation 9 ruling (disclose only, for past runs) is untouched.
  *"Recommendation 7" and "Recommendation 9" in this file refer to `GOV-2026-09-29-PV-02` Rec 7
  and PV-01 Rec 9 respectively (prefix note added under PV-04 Rec 24).*

## Full conda-layer drift *(added 2026-09-30, `GOV-2026-09-30-PV-04` Rec 23)*

**How it was derived.** A script compared `conda_list_explicit_md5.txt` with
`environment/conda-win64.lock`, taking the package name, version and build from each URL. The
result was printed before this table was written.

**Result.**
- 20 packages are installed.
- **10** differ in **version** from the lock.
- **7** match the lock's version but differ in **build**.
- **3** are **absent** from the lock.
- **0** match the lock exactly.
- The PV-04 Data seat reported 13 version drifts. This derivation finds 10; the difference is
  the name mapping. The figure given here is the one printed by the script above.

> **Correction (2026-09-30, `GOV-2026-09-30-PV-05` Rec 3).** The explanation above is wrong, and
> is left as first written.
>
> - **Where 13 came from.** It is **10 version + 3 absent**, with the absent packages counted as
>   version drift. Name mapping is not the cause.
> - **Name-mapped view.** Mapping the three Anaconda names to their conda-forge counterparts
>   (`sqlite`→`libsqlite` 3.53.4, `xz`→`liblzma` 5.8.3, `zlib`→`libzlib` 1.3.2) gives
>   **11 version / 9 build-only / 0 absent**.
> - **What that view exposes.** One further version drift, which the name-only table hides:
>   `xz` 5.8.2 against `liblzma` 5.8.3.
>
> Both views were confirmed independently by the PV-05 Data seat.

| Package | Installed | Lock | Kind |
|---|---|---|---|
| `ca-certificates` | 2026.8.13 | 2026.7.22 | version |
| `libffi` | 3.4.8 | 3.7.0 | version |
| `openssl` | 3.5.8 | 3.6.4 | version |
| `setuptools` | 83.0.0 | 84.0.0 | version |
| `tk` | 8.6.15 | 8.6.13 | version |
| `ucrt` | 10.0.22621.0 | 10.0.26100.0 | version |
| `vc` | 14.3 | 14.5 | version |
| `vc14_runtime` | 14.44.35208 | 14.51.36247 | version |
| `vs2015_runtime` | 14.44.35208 | 14.51.36247 | version |
| `wheel` | 0.47.0 | 0.48.0 | version |
| `bzip2` | 1.0.8 `h2bbff1b_6` | 1.0.8 `h0ad9c76_10` | build only |
| `libexpat` | 2.8.4 `hd7fb8db_0` | 2.8.4 `hac47afa_0` | build only |
| `libzlib` | 1.3.2 `h1c6eee0_0` | 1.3.2 `hfd05255_3` | build only |
| `packaging` | 26.3 `py311haa95532_0` | 26.3 `pyhc364b38_0` | build only |
| `pip` | 26.2.1 `pyhc872135_0` | 26.2.1 `pyh8b19718_0` | build only |
| `python` | 3.11.16 `hb00fc5c_0` | 3.11.16 `hb12b558_2_cpython` | build only |
| `tzdata` (system) | 2026c `he532380_0` | 2026c `h151e31d_0` | build only |
| `sqlite` | 3.53.4 | — | absent from lock (by name; see the note below) |
| `xz` | 5.8.2 | — | absent from lock |
| `zlib` | 1.3.2 | — | absent from lock |

**About the pip freeze** *(PV-04 Rec 29)*. `pip_freeze_all.txt` has **62 lines**: 61 versioned
`name==version` lines and 1 `pip @ file:///…` line. Every "of 61" figure in this record counts
the 61 versioned lines only.
