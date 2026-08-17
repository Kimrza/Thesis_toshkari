**Collaborator:** aidlc-devsecops-agent

## Contribution

Scope of this review: lint/format rules, static analysis, secret handling, dependency and
supply-chain controls, dataset integrity, and the tamper controls that protect the
scientific result. In this project, data-integrity and leakage-prevention controls are
security controls, so the locked-test guard, the phase-transition hash freeze and the
provenance chain are all inside this scope.

The draft's overall framing is right — this is a governed research pipeline, not a
service, and the org defaults do not transfer mechanically. But the draft describes the
security posture from the two policy sentences it found (§10 credential handling,
NFR-SEC-01) and never scans the workspace against them. The workspace currently violates
NFR-SEC-01, the mandated detection controls are missing from all three artifacts, and one
Way-of-Working claim contradicts the normative core. Details below, each with the file
and section the lead can cite directly.

### A. Live NFR-SEC-01 violations in the workspace (not currently reported anywhere)

NFR-SEC-01 (`PreFlight/Technical_Environment_and_Research_Implementation(1)(2).md` §11)
reads: "No secrets in notebooks, source, configs, logs, or artifacts; **no personally
identifiable information is required or stored**." Its evidence column is "Repository
scan/checklist". Running that scan finds three current breaches:

1. **PII hardcoded in a committed notebook.**
   `notebooks/madrigal_phase1_coverage_audit.ipynb`, Cell 2, assigns `USER_FULLNAME`,
   `USER_EMAIL` (a personal Gmail address, written literally) and `USER_AFFILIATION` as
   in-source constants. An email address is PII under NFR-SEC-01's second clause, and §10
   forbids identity material of this kind appearing in a notebook.
2. **PII persisted into 13 committed artifacts.**
   `user_fullname` and `user_affiliation` are written into
   `evidence/audit_evidence_2022-{01..12,FULL}/request_manifest.json`. NFR-SEC-01 names
   artifacts explicitly. The email is not in the manifests — only the notebook — but the
   name and affiliation are in every one.
3. **A genuine, unresolved conflict sits underneath this**, and the inception guardrail
   ("Never carry forward unresolved contradictions … surface and resolve them
   explicitly", `aidlc/spaces/default/memory/phases/inception.md` § Requirements Quality)
   requires it be named rather than left implicit: §10's Madrigal row mandates CEDAR
   rules-of-the-road compliance, and CEDAR requires a real identity on every request
   (the notebook's own Cell 2 comment says so). So identity **must** be supplied and
   **must not** be stored. The resolvable form — which the lead should put to the human
   at the affirmation gate, not decide here — is: identity is injected at runtime from
   Kaggle Secrets / an environment variable on both platforms, the notebook carries no
   default and fails closed if the variable is unset, and the manifest records an
   identity-supplied boolean plus the provider's own request ID rather than the person's
   name, email and affiliation.

None of this appears in `team-practices.md`, `discovered-rules.md` or `evidence.md`.
`team-practices.md` § Deployment instead says the §10 credential rule "maps directly onto
conventional practice and should be affirmed as-is" — affirming a rule the workspace is
already breaking, without the breach recorded, is the specific failure mode the
project-level rule "ALWAYS check the drafted artifact against the governing normative core
before the approval gate" exists to catch.

### B. The mandated detection controls are absent from the draft

The normative core does not only state prohibitions; it names the checks that evidence
them. Three whole control families are missing:

- **Repository secret/PII scan.** NFR-SEC-01's evidence is "Repository scan/checklist".
  No artifact mentions a scan. Recommend `discovered-rules.md` gain: ALWAYS run the
  NFR-SEC-01 repository scan for secrets and PII before any commit, notebook export, or
  evidence release, and record its result as the NFR-SEC-01 evidence item.
- **Source-reuse register and licence scan (NFR-LIC-01) — entirely absent.** This is the
  project's whole supply-chain control and no artifact mentions it. It comprises
  §10.1 (the External Method and Code-Reuse Register, with a mandatory 15-field record
  per copied or adapted fragment: `reuse_id`, repository URL, immutable commit/tag,
  upstream file and function, retrieval date, SPDX ID, copied-versus-adapted status,
  destination, modifications, tests, citation, notice location, reviewer, approval date),
  the module `src/data/reuse_registry.py` and test `tests/test_reuse_registry.py` (§12),
  evidence obligation EV-20 "before copied code is committed" (§17), and gate **G-P2**,
  which will not pass without "reuse/license register complete" (§16.1). Two hard rules
  fall out of §10.1 and belong in `discovered-rules.md`:
  - NEVER paste an upstream function into a notebook; copied code lives behind a
    project-owned adapter with its own tests (§10.1, closing paragraph).
  - NEVER copy directly from a source whose licence is absent, ambiguous, or
    incompatible; only the published method may be reimplemented from the paper, with a
    citation (§10.1).
  There is also a named **governance dependency owned outside this project** — per the
  project-level rule requiring assumptions to be split into verification obligations
  versus external governance dependencies: §10.1's AGPLv3 candidate
  (Global-TEC-forecasting) carries repository-distribution obligations, and the document
  itself says to "obtain institutional advice if repository-distribution obligations are
  unclear"; §18.2 assigns "whether an external licence permits direct copying" to
  Student + Supervisor/institutional policy. That is not a check this project performs on
  itself, and it should be listed with the other open supervisor gates rather than as a
  project verification obligation.
- **Grep-evidence static-analysis gates.** §19 makes two acceptance items depend on
  static absence checks: TA-08 requires "grep evidence" that SSN is absent from the
  codebase and that F10.7 is trailing / Dst diagnostic-only; TA-12 requires grep evidence
  that "residual and GRU modules are absent from the codebase". §12 adds a third, enforced
  by test: `src/external/iri.py` and `src/external/gim.py` must never be imported,
  directly or transitively, by any module under `src/features/` or `src/models/`. These
  are static-analysis obligations on the codebase, and they are the closest thing this
  project has to SAST. The draft's § Code Style discusses only formatting.

### C. Dependency and supply-chain pinning — one measurable gap already in the evidence

`team-practices.md` § Code Style treats environment pinning correctly in outline but
understates it, and misses a breach already sitting in the evidence tree:

- **`madrigalWeb_version` is recorded as `"unknown"` in all twelve monthly
  `request_manifest.json` files** (`evidence/audit_evidence_2022-{01..12}/`). §10's
  Madrigal row requires "a **pinned** `madrigalWeb` API/command"; §8.1 requires "pin the
  client or record the exact web-service interface"; §13.3 requires the acquisition
  provenance. The coverage audit that produced the D-144 evidence therefore ran on an
  unpinned client, and that is not reproducible under NFR-REP-01. This is a concrete,
  checkable finding and belongs in `evidence.md` § Key facts, with the corresponding rule
  in `discovered-rules.md`: ALWAYS record the exact client/package version in the request
  manifest of any provider retrieval; `unknown` is a failed pin, not a placeholder.
- §13.1 requires exact pins **including transitive dependencies**, plus a per-run capture
  of: `requirements.txt` hash and `pip freeze`, Python/OS/CPU (and GPU if used) and key
  library versions, **code commit**, configuration-snapshot hashes for all four config
  files, input dataset and manifest versions, platform, and known nondeterministic
  operations. The draft cites only requirements.txt and `pip freeze`.
- **The container gate is closed** (§13.1 and §8.3): a container is added only if
  lock-based clean reproduction on both platforms demonstrably fails. That is a frozen
  supply-chain decision and belongs under Forbidden: NEVER introduce Docker or a
  container as a required deliverable while the gate is closed.
- **§8.3 is a dependency deny-list** and `discovered-rules.md` has no rule reflecting it:
  PyTorch, Theano, MATLAB, R, Julia are prohibited in the governed pipeline; GRU is
  removed with the gate closed; GLONASS is prohibited in the primary product; GPS-TEC
  (Seemala) is prohibited as a production processor. §8.1 is the matching allow-list.
  Adding a dependency outside §8.1 is a scope change, not an implementation choice.
- The **TensorFlow pin is explicitly unresolved** (§8.1: "TensorFlow 2.21.0 is the current
  Python 3.11-compatible candidate; the exact compatible pin is frozen only after
  Kaggle/local fixture installation passes"; EV-18). It should sit with the other
  TBD-freeze-gate items in `discovered-rules.md` § Assumptions & Open Questions, since
  §18.2 makes "forecasting framework" a Student + Supervisor choice the agent may not
  make.

### D. Dataset integrity — the chain of custody starts one step too late

`team-practices.md` § Deployment describes immutable dataset releases correctly but cites
**§6.13, which does not exist**; the immutable dataset release manifest is
**§13.3**. Please correct the citation in both the Deployment section and § Sources.

More substantively, the hash chain in the existing evidence does not reach the provider
bytes:

- Each `evidence/audit_evidence_2022-*/sha256_manifest.json` hashes exactly four files —
  the three derived coverage CSVs and `request_manifest.json`. The **native provider files
  under `raw_isprint_cache/` are not hashed in any month.** §10's Madrigal row requires
  "retain native files"; §13.3's `source_files` field requires provider, permanent
  citation, filename, retrieval date and **SHA-256** per source file.
- `raw_isprint_cache/` is **absent entirely from 2022-04, 2022-07 and 2022-12** — including
  December, the locked-test month.
- The consequence is that `scripts/merge_coverage_year.py`'s otherwise-good
  refuse-to-merge-unverified-evidence check (it exits on a missing manifest or a hash
  mismatch) verifies only derived artifacts. Nothing in the workspace can currently
  demonstrate that the derived CSVs correspond to the bytes the provider served.
  `evidence.md`'s row for that script should say so, rather than presenting the
  hash-verification pattern as covering the retrieval.
- The related contrast is worth naming as the rule: `scripts/audit_ec1_drivers.py`
  *computes* SHA-256 over whatever is on disk at run time and writes it into the report;
  it does not verify against a retrieval-time manifest (there is no `sha256_manifest.json`
  under `evidence/audit_ec1_2026-08-15/`, only `EC1-AUDIT.md` and
  `ec1-audit-report.json`). Proposed rule: hashes are recorded by the retrieving step at
  retrieval time, and every later step verifies against that record — a hash computed
  after the fact attests to the current bytes, not to provenance.
- §13.3 also requires that "the final-results dataset is write-protected or stored under a
  new version rather than overwritten", with TA-15 gating on a **mutation-protection
  test** and `tests/test_release_hashes.py` (§12). Not mentioned in the draft.

### E. Locked-test access control is missing — the highest-value control in the project

`team-practices.md` § Testing Posture describes G-06 as "hash predictions before any
metric", which is correct but is the *procedure*, not the *control*. The normative core
specifies an enforced technical access control that no artifact mentions:

- §12: "Locked-test artifacts use **restricted paths** until G-05 is complete and must
  include `locked_test_accessed = true` in the registry."
- §13.4: `locked_test_accessed` is a required column of every experiment-registry row.
- §12 / §18.3: `tests/test_locked_test_guard.py` is a required gate test; WS-18 makes it a
  pass/fail walking-skeleton row — "Locked-test guard blocks December performance
  execution before G-05 and records access", evidenced by "guard test and access-log
  sample".
- §7.0B: the Phase 2 December run must record `prior_period_exposure=true`, and reports
  "must not describe Phase 2 as a second independent blind holdout" — a mandatory
  disclosure control, absent from `discovered-rules.md`.

Recommend a Mandated rule: ALWAYS keep locked-test artifacts behind restricted paths and
the locked-test guard until G-05 is signed, and record every access in the registry via
`locked_test_accessed`.

### F. Registry and audit integrity (NFR-AUD-01) — absent

§13.4: "Registry writes must be atomic or append-safe. **Failed and aborted runs remain
visible with status and reason; silent reruns are prohibited.**" This is the project's
anti-tamper control over its own result history and it has no rule in the draft. TA-10
gates on it. Proposed Forbidden rule: NEVER delete, overwrite, or silently re-run an
experiment-registry entry; a failed or aborted run stays visible with its status and
reason.

### G. Phase-transition freeze — right idea, missing the enforcement

`team-practices.md` § Deployment describes §7.0B well. Two omissions:

- The freeze is enforced by a **test**, not only by a manifest: NFR-PHASE-01's evidence is
  "`test_phase_boundary.py`, **transition-manifest hash test**", and G-P3C requires
  "protected hashes unchanged" with a hash-diff report (§16.1). The draft mentions
  `test_phase_boundary.py` for the import boundary but not the hash-diff test.
- §7.0B also fixes: Phase 2 retrains from newly initialized weights and does **not** carry
  Phase 1 fitted weights forward unless a separately approved transfer-learning experiment
  is labelled exploratory; and "**No Phase 1 result may motivate a Phase 2 model or
  evaluation change.**" Both are hard rules missing from `discovered-rules.md`.

### H. §18 — the project's authorization model, omitted

`discovered-rules.md` reduces §18 to one line about TBD-freeze-gate values. §18 is a
least-privilege model for exactly the agents this stage's output will govern in
Construction, and two parts of it must be carried forward verbatim in force:

- **§18.2's absolute rule**: "the agent may never change a scientific value after seeing
  any result, validation or otherwise." This is stronger and broader than the TBD rule the
  draft captured, and it is the rule most likely to be breached in practice.
- **§18.3's preflight gate**, with a testable decision criterion — zero unresolved P0
  fields and no failing critical test — an automated assertion that no required field in
  the four configs is `TBD`, that every declared source and hash exists, and that all ten
  named gate tests pass (target contract and DCB sign; availability lags; IRI-free denial;
  split embargo; train-only transforms; comparison-wide masks and matched windows;
  checkpoint restore; vector bootstrap; release hashes; locked-test access guard). Evidence
  artifact: `aws_ai_dlc_preflight_report`. This satisfies the phase requirement that
  requirements be testable with clear pass/fail criteria, and it satisfies the
  project-level rule that a gating condition's inputs be specified in the same stage that
  records the condition — the draft records gates without their inputs.

### I. Provenance and integrity of externally fetched driver data

Three §10 controls in scope here are missing from `discovered-rules.md`:

- NOAA/GFZ Kp/ap/Hp60/ap60: preserve **observation time, publication time, release status,
  retrieval time and units**, and "**never backfill from future final values**". The draft
  has the safe-lag rule but not the release-status/publication-time preservation and not
  the no-backfill prohibition — which is the leakage vector the lag rule alone does not
  close. This is live: the retained Kyoto data is `dst_provisional_*` (grade recorded in
  `evidence/audit_ec1_2026-08-15/EC1-AUDIT.md`), and if a final-grade release appears
  later, the no-backfill rule is what prevents it silently replacing the provisional
  series.
- NASA CDDIS: "**Do not substitute an undocumented mirror**; record outage and retry." A
  supply-chain provenance rule with no equivalent in the draft.
- Every §10 row has a **failure behaviour** column, and several are hard stops ("Any
  attempt to train from ICTP is a hard failure; no retry can waive the measured
  three-location/December coverage failure"; "do not switch to `los`, interpolate missing
  cells, or treat grid values as receiver observations"; "No automatic fallback" for
  IONOLAB-TEC). Fail-closed behaviour on external integrations is a discovered practice in
  its own right and none of it is in the draft.

**Transport downgrade.** `notebooks/madrigal_phase1_coverage_audit.ipynb` Cell 3 lists
`'http://cedar.openmadrigal.org'` as a "plain-http fallback if TLS is blocked", after the
https entry. §8.1 authorises `urllib`/`requests` for "**HTTPS** retrieval". A silent
downgrade to cleartext on the acquisition path is both an identity-exposure issue (the
CEDAR identity travels with the request) and a provenance issue: a SHA-256 taken over
bytes fetched without TLS attests to what arrived, not to what the provider published.
Proposed rule: NEVER downgrade a governed acquisition to plain HTTP; record the TLS
failure as an outage and stop.

### J. Version control is mandated by the normative core — correction to § Way of Working

`team-practices.md` § Way of Working states that the workspace is not a git repository and
leaves initialization as an open question, and `discovered-rules.md`'s companion
assumption says "none of the governing documents … mandate or forbid version control
tooling — they govern the scientific pipeline, not the software engineering practice
around it." That is not correct, and it matters:

- §13.1 requires each run to capture **`code commit`** as part of the environment lock.
- §13.4 makes **`code_commit`** a required column of every experiment-registry row.
- §19 TA-01 evidences the repository skeleton by "Repository tree and **code commit**".
- §10 credential handling is defined as "environment configuration **excluded from version
  control**", which presupposes version control exists.

So a version-control system is a normative-core requirement of the reproducibility and
audit chain, not a team preference. Under the project-level rule that a stage answer
cannot relocate a requirement the governing normative core fixes, the open question must
narrow: not *whether* to initialize git, but *when* (before the first registry-recorded
run) and *which* branch/merge convention applies on top. The absence of `.git` should be
recorded in `evidence.md` as a gap against §13.1/§13.4/TA-01, not as neutral context.

Two consequences follow immediately:

- The workspace's `.gitignore` is the AI-DLC framework's file and contains **no rule that
  would exclude a credential or environment file** — no `.env`, `*.key`, `kaggle.json`,
  `.netrc`, `credentials*`, no `__pycache__` or `.ipynb_checkpoints`. §10's "excluded from
  version control" mechanism therefore does not exist yet. The affirmation gate should
  produce the deny-list alongside the rule, per "ALWAYS specify the inputs a gating
  condition depends on in the same stage that records the condition".
- §9.1 requires saving and downloading the **executed** Kaggle notebook as evidence.
  Executed notebooks carry outputs, and outputs are the classic leak path for identity
  strings and tokens. (The one notebook present has zero stored outputs today, which is
  the correct state.) Recommend a rule: strip or review outputs before an executed
  notebook is committed or released as evidence, and never commit an executed notebook
  whose outputs have not passed the NFR-SEC-01 scan.

### K. Lint/format — narrow the open question rather than leaving it open-ended

`team-practices.md` § Code Style and `evidence.md` fact 5 both record the absence of
`pyproject.toml` as "no linter config to defer to". Both miss that **§12 mandates
`pyproject.toml` at the repository root** as part of the required tree, and TA-01 gates
acceptance on that skeleton existing. So `pyproject.toml` is a not-yet-built deliverable
in exactly the same sense `evidence.md` fact 6 already correctly records for
`requirements.txt` — the two facts should be stated the same way. The interview question
then narrows usefully: the file is already required; what remains is which formatter and
linter to configure inside it, and whether the linter is a blocking check.

I endorse the draft's refusal to invent an 80% coverage floor. The corresponding
suggestion for this project is not a coverage percentage but a required-checks gate: the
ten §18.3 gate tests plus the twenty §16 walking-skeleton rows, each pass/fail with a
named evidence link — which is what §16 already says ("Acceptance occurs only when all 20
rows are `PASS`, each evidence target exists, hashes match, and no unresolved failure is
waived informally"). That satisfies the inception guardrail on testable pass/fail criteria
without importing a metric the normative core never states.

## Positions

- AGREE: Treating this as a governed research pipeline where deployment means dataset and model releases, and refusing to force the org staging/production template onto it — the §13.3 release manifest and the §7.0B freeze genuinely are the release and rollback controls here.
- AGREE: Declining to invent an 80% coverage floor the normative documents never state, and grounding testing posture in named required tests instead.
- AGREE: Recognising `evidence/DECISIONS.md` as the project's real unit of auditable change, and the hash-verify-before-trust pattern in `scripts/merge_coverage_year.py` as a practice worth affirming.
- AGREE: Citing the normative documents as the authority and `constraint-register.md` as a cross-check rather than as an independent source.
- OBJECT: NFR-SEC-01 is affirmed "as-is" without a repository scan, while the workspace breaches it now — a personal email hardcoded in `notebooks/madrigal_phase1_coverage_audit.ipynb` Cell 2, and name plus affiliation persisted into all 13 `evidence/audit_evidence_2022-*/request_manifest.json` files.
- OBJECT: NFR-LIC-01 and the entire §10.1 source-reuse register — the project's only supply-chain control, gating G-P2 and evidenced by EV-20, `src/data/reuse_registry.py` and `tests/test_reuse_registry.py` — appear in none of the four artifacts.
- OBJECT: § Way of Working claims the governing documents neither mandate nor forbid version control; §13.1, §13.4 and TA-01 all require a `code commit` per run, so version control is fixed by the normative core and the open question must narrow to when, not whether.
- OBJECT: The locked-test access control is missing — §12's restricted paths, §13.4's `locked_test_accessed` field, `tests/test_locked_test_guard.py` and WS-18 are the enforcement behind G-06, and only the hashing procedure is described.
- OBJECT: §18.2's absolute rule ("the agent may never change a scientific value after seeing any result") and the §18.3 preflight gate with its ten named gate tests are omitted, though they are the authorization model governing the very agents this stage's output will bind in Construction.
- OBJECT: The dataset-release citation is wrong — the immutable release manifest is §13.3, not §6.13 — and the hash chain it describes does not in fact reach the provider bytes: `raw_isprint_cache/` is unhashed in every month and absent entirely from 2022-04, 2022-07 and 2022-12, the locked-test month included.
- OBJECT: Dependency and supply-chain pinning is understated — `madrigalWeb_version` is `"unknown"` in all twelve monthly request manifests despite §10's pinning requirement, §8.3's prohibited-stack deny-list has no rule, the closed container gate is unrecorded, and §13.1's transitive-pin and per-run capture list is reduced to `requirements.txt` plus `pip freeze`.
- OBJECT: `pyproject.toml` is presented as merely absent, when §12 mandates it in the required repository tree and TA-01 gates on it; the lint/format open question should be narrowed accordingly rather than left open-ended.
- OBJECT: The §10 driver-provenance controls are incompletely carried — the "never backfill from future final values" prohibition, the publication-time/release-status preservation requirement, the CDDIS no-undocumented-mirror rule, and the fail-closed failure behaviours are all absent, and the notebook's `http://` fallback contradicts §8.1's HTTPS retrieval.
