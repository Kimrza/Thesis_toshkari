# Validation scripts, as run on 2026-09-19

Kept for traceability, exactly as executed from the session scratchpad
(`…/scratchpad/`), so their relative paths (`wheel/apf107.dat`, `wheel/apf107_hist.dat`,
`rev3_inner.py`, the absolute repository path in `test_rev3.py`) refer to that directory,
not to this one. Inputs they read are the same bytes filed here: `wheel/apf107.dat` and
`wheel/ig_rz.dat` = `../index_files/installed_iricore-1.8.0_wheel/`; `wheel/*_hist.dat` =
`../index_files/historical_master-92c6d8c7_and_1.9.0-sdist/`.

- `iri_net_preflight.py` — the network preflight + failure classifier embedded in notebook
  revision 3 (Step 1b cell), verbatim.
- `test_modules.py` — real preflight + synthetic DNS / TCP-refused / TLS / HTTP-status
  failures; 10 classifier cases; index parsers on the real files; 5 synthetic index
  failures. Result: `ALL MODULE CHECKS PASSED`.
- `build_rev3.py` — builds revision 3 from the preserved revision 2 (asserts its hash
  `b8399c98…` first). Output hash `0e4d4478…`.
- `test_rev3.py` — revision-3 checks A–D (failure path; end to end on a stub `iricore`
  with the real index bytes; outer `run()` classes and preflight stop path with the bundle
  redirected; Step 5 asserts). Result: `ALL REVISION-3 CHECKS PASSED`.

Not run: a Kaggle execution of revision 3.
