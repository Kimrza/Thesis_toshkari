# Performance Test Instructions

**Stage:** build-and-test (3.6) · **Lead:** aidlc-quality-agent
**Date:** 2026-09-24 · **Repository commit at authoring:** `41fd109`

"Performance" in this project is **not** load testing, throughput
benchmarking, or latency SLOs — there is no service, no traffic and no
deployment target. The NFR surface that exists (from the units'
`nfr-design` artifacts and the `code-generation-plan.md` /
`code-summary.md` records this stage consumes) is:

1. **CPU completeness** — the full workflow must complete on CPU
   (TC-01; Vision §9.2 "CPU is a complete execution path, not an emergency
   mode"). GPU is an optional accelerator, never a dependency of any result.
2. **Runtime envelopes measured from fixtures, then frozen** — TE §15.1:
   expected CPU runtime ranges are **measured** from the two
   walking-skeleton fixtures and frozen into
   `tests/fixtures/<fixture_id>/fixture_manifest.yaml` (§15.2), never
   invented. A performance "target" that was not measured first is a
   protocol violation here.
3. **Determinism under fixed seeds** — NFR-DET-01 / TC-21: fixed seeds from
   `seeds.yaml`, three-seed element-wise mean as the confirmatory
   prediction, `PYTHONHASHSEED=0` for the whole clean-run sequence.

## How to measure (not assert) runtimes

Runtime evidence comes from the fixture ladder, on CPU, in the governed
environment:

```bash
export PYTHONHASHSEED=0
# each stage script logs its own wall time into the run snapshot / registry
python scripts/run_walking_skeleton.py --config configs/ --fixture plumbing_7day
```

- The measuring run's wall times per stage go into the fixture measurements
  (`fixture_measurements.json` already carries this pattern for WS-13
  parity: *measured, not frozen*).
- Once the student freezes them (a D-number act), the frozen ranges become
  assertions in `fixture_manifest.yaml`, and a later run outside the range
  is a finding rather than a shrug.
- **Status at authoring:** no runtime range is frozen yet; the manifests
  carry `TBD — freeze gate` sentinels. This is correct — the values are
  student freeze acts (Q-31 / §15.1), and no implementer may fill them by
  convenience (TE §1.1).

## Determinism checks (the enforceable performance-adjacent NFR)

```bash
python -m pytest tests/test_determinism.py tests/test_bootstrap.py \
  tests/test_checkpoint_restore.py -q
```

- `test_determinism.py` (46 fns) — seed plumbing, the R-05 re-exec contract
  (including the Windows exit-code repair with its bites-on-pre-repair-HEAD
  control), one-process-per-stage isolation.
- `test_bootstrap.py` (37 fns) — the vector time-block bootstrap: 24-hour
  blocks carrying all three stations together, 10,000 replicates, seed
  20221201 (TC-19, hard); WS-17's exact-reproduction requirement.
- `test_checkpoint_restore.py` (12 fns) — §18.3 critical item "checkpoint
  restore".

## Regression detection

There is no CI service (team.md, Q7=D). Regression detection is:

- the pre-commit hook running the critical set on every commit;
- the full suite before every governed run, captured in that run's evidence
  record and the `aws_ai_dlc_preflight_report`;
- registry rows (append-only, NFR-AUD-01) making any rerun visible with
  status and reason — a silent rerun is prohibited, so a performance
  regression cannot be papered over by re-running until it looks fine.

## Explicit non-goals

- No load/stress/soak testing — nothing serves traffic.
- No GPU benchmarking — prohibited as a dependency (TC-01).
- No 5-minute-resolution claims at NICO — out of reach on this dataset
  (D-7) and therefore never a performance target.
