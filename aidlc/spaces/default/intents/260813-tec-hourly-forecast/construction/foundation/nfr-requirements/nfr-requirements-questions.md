# NFR Requirements — Questions — `foundation`

**Unit** `foundation` (Bolt 1) · **Kind** `library` · **Stage** `nfr-requirements`

Only two NFR artifacts are produced for this unit — `security-requirements.md` and
`tech-stack-decisions.md`. `performance-requirements.md`, `scalability-requirements.md`
and `reliability-requirements.md` are excluded by the stage's own `produces_kinds`,
which maps them to `[service]` / `[service, ui]`; `foundation` is `kind: library`.

Three of `foundation`'s open items are **not re-asked here** — the `dataset_version`
verify-on-write read-back population, the `IntegrityError` module home, and Kaggle's
unmeasured durability semantics. All three are already routed to the project decision
owner by the approved `functional-design`, and asking again would open a second,
competing route to one ruling. They are carried into the artifacts as stated
dependencies.

---

## Question 1

TA-22 requires a secret scan over the repository **history**, configurations, logs and
artifacts. What was actually performed on 2026-08-28 is narrower: `git ls-files` at one
commit, plus a five-pattern scan over 1158 tracked files, both returning zero hits. A
credential committed and later removed is invisible to that. `requirements.md`
§ Known defects row 13 also records a **live conflict** — NFR-SEC-01 forbids stored PII,
while the Madrigal rules of the road require a real identity on every request, and
`notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2 carries `USER_EMAIL` in every
commit with thirteen committed manifests carrying `user_fullname` and
`user_affiliation`. That conflict is the supervisor's to resolve and **no reading is
adopted** by this stage.

What scan scope should `security-requirements.md` state as the NFR requirement for TA-22?

A. Full TE §10 scope — history, configurations, logs and artifacts — with the identity block recorded as a known, unresolved exception
   > **Impact**: States the requirement as the authority actually writes it, so nothing later has to be widened. The requirement is knowingly unmet on the day it is written, and stays unmet until both the history scan runs and the supervisor rules on the identity conflict. Keeps NFR-SEC-01 and TA-22 unclaimed, which is where `functional-design` already left them.

B. Working-tree scope only, with the history scan deferred to its own later requirement
   > **Impact**: Produces a requirement that is already satisfied, which reads well and tests green today. It narrows TA-22 below what TE §10 requires, and `team.md` records that exact move — reading a mandated obligation as the subset an initiative happens to need — as the failure `GOV-2026-08-15-FE-01` finding `GOV-F-06` warned against.

C. Full scope, and additionally require history remediation before G-05
   > **Impact**: Closes the exposure rather than recording it. It also breaks the audit-trail immutability `team.md` affirms — git history is not rewritable without it — and pre-empts a supervisor decision this stage has no authority to take.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — it is the only option that states TA-22 at the scope its own authority states it, and `functional-design`'s dated clause of 2026-08-28 already took exactly this posture ("the precondition is satisfied; the requirement remains unclaimed"). Option B would make this stage the place the obligation quietly shrank, and option C decides the supervisor's question for them. The cost of A is honest: a requirement that is written red and stays red until two separate acts complete.

[Answer]: A

---

## Question 2

`foundation`'s W-8 resolves platform roots and checks that required credential
**environment-variable names** are present, never reading a value. The concrete
`CredentialNameMap` contents "await the four configs existing". TE §10 requires
credentials to come from **platform secret stores or environment configuration excluded
from version control**. Kaggle offers a first-class secret store (Kaggle Secrets /
`UserSecretsClient`); local development has no equivalent and would use environment
variables or an ignored dotfile.

What mechanism should `security-requirements.md` require for credential provisioning?

A. Platform-appropriate per platform, behind one shared resolution interface
   > **Impact**: Uses each platform's strongest available mechanism — Kaggle Secrets on Kaggle, an ignored file or shell environment locally — and keeps W-8's single `resolve_platform_roots` contract intact, so calling code never branches on platform. Two mechanisms means two ways to misconfigure, so the presence check and its "names present, values unvalidated" caveat carry more weight.

B. Environment variables only on both platforms, with Kaggle Secrets injected at session start
   > **Impact**: One mechanism, one failure mode, and the local and Kaggle code paths become literally identical — which is what TA-03 and the in-Kaggle obligation are easiest to evidence against. It passes secrets through a process environment on Kaggle where a stronger store was available, and a notebook that prints its environment leaks them.

C. Defer the mechanism to the Bolt that first needs authenticated provider access
   > **Impact**: Avoids specifying ahead of a concrete need, and W-8 already states the presence check is stage-specific rather than part of `foundation` initialization. It leaves NFR-SEC-01's provisioning half unspecified at exactly the unit that owns the credential boundary, and `project.md` records deferring a gating condition's inputs as leaving the condition unmeetable.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — TE §10 names both mechanisms disjunctively, so using each platform's own is compliant, and option B's environment-variable path on Kaggle discards a secret store the platform already provides. Option C is the one to avoid: this unit owns the credential boundary, and leaving the mechanism open here is the pattern `project.md` § Way of Working names as making the condition uncheckable.

[Answer]: A

---

## Question 3

TE §8.1 requires `tensorflow` / `tf.keras` and names **2.21.0** as "the current
Python 3.11-compatible candidate", stating that "the exact compatible pin is frozen only
after Kaggle/local fixture installation passes". Neither walking-skeleton fixture has
run, and no Python interpreter exists in this environment. TE §18.2 forbids an
implementer or coding agent from filling a freeze-gate value by convenience.

How should `tech-stack-decisions.md` record the TensorFlow version?

A. `TBD — freeze gate`, with 2.21.0 recorded as the named candidate rather than the decision
   > **Impact**: Matches TE §18.2 exactly and keeps the value visible to the §18.3 zero-TBD preflight, which is what will eventually force it to be frozen. `requirements.txt` cannot be completed until the fixtures install, so TA-03 stays Pending — which it already is.

B. Pin 2.21.0 now and treat a fixture failure as the trigger to change it
   > **Impact**: Gives Bolt 1 a complete `requirements.txt` immediately and unblocks the pinned-environment install TA-03 measures. It fills a freeze-gate value by convenience, which TE §18.2 states as an absolute rule and `project.md` carries as a NEVER — and a pin that installs is not evidence the pin was approved.

X. Other (please specify)
   > **Impact**: Depends on your specific choice.

> **💡 Recommendation**: Option A — TE §8.1 states the freeze condition in the same sentence that names the candidate, so recording 2.21.0 as the pin would contradict the source it came from. This is not a close call; it is the rule the project's own `## Forbidden` list states twice.

[Answer]: A

---

## Consolidated Summary Confirmation

Confirm this reading before the two artifacts are written. Nothing below decides a
scientific value, and nothing claims a gate or acceptance row is discharged.

**Scope of this stage for `foundation`.** Two artifacts only —
`security-requirements.md` and `tech-stack-decisions.md`. The stage's `produces_kinds`
maps `performance-requirements`, `scalability-requirements` and `reliability-requirements`
to `[service]` / `[service, ui]`, and `foundation` is `kind: library`, so those three are
not produced. The categories are still assessed; the assessment is recorded in the stage
diary and in the security artifact's scope note.

**Q1 = A — TA-22 is stated at full TE §10 scope.** History, configurations, logs and
artifacts. The 2026-08-28 evidence (`git ls-files` at one commit; a five-pattern scan
over 1158 tracked files; zero hits both) is recorded for what it is — working-tree
evidence at one commit — and **NFR-SEC-01 and TA-22 stay unclaimed**. The identity block
(`USER_EMAIL` in `notebooks/madrigal_phase1_coverage_audit.ipynb` cell 2; `user_fullname`
and `user_affiliation` in thirteen committed manifests) is recorded as a **known,
unresolved exception**, owner Student + Supervisor per `requirements.md` § Known defects
row 13, and **no reading is adopted** on whether it is a breach or a mandated provider
record.

**Q2 = A — credentials are provisioned platform-appropriately behind one interface.**
Kaggle Secrets on Kaggle; an ignored file or the shell environment locally; one shared
resolution surface so calling code never branches on platform, preserving W-8's contract.
W-8's caveat is carried verbatim in substance: the check proves required **names** are
present, not that a value is non-empty, valid or authorized.

**Q3 = A — the TensorFlow pin is `TBD — freeze gate`.** 2.21.0 is recorded as TE §8.1's
named candidate, not as the decision, because §8.1 freezes the exact pin only after
Kaggle/local fixture installation passes and neither fixture has run. Every other TE §8.1
component is transcribed as approved. TE §18.2's absolute rule is why.

**Carried, not re-decided.** Three `foundation` open items already routed to the project
decision owner by the approved `functional-design` are carried as stated dependencies
rather than re-asked: the release population D-29's verify-on-write must read back (a
TE §18.3 stop-and-report point for stage 3.5); the `IntegrityError` module home
(`src/data/config.py` as declared, versus a §12 amendment for `src/data/exceptions.py`);
and Kaggle's unmeasured durability semantics behind W-6 step 8.

**Status claims made.** None. G-09 is signed (D-31) with its own §18.3 preconditions
UNMET; `configs/` does not exist; no Python interpreter exists in this environment, so
every test remains written-but-unexecuted; TA-03, TA-15, TA-22, TA-23 and the §18.3
zero-TBD preflight all stay Pending or unclaimed.

**One defect observed upstream and not corrected here.** `foundation`'s own approved
`business-logic-model.md` states "module creation is authorised" in its lead G-09 box and
its `§ Assumptions` bullet, while W-9's barred list and the BLK-01 note state creation
stays gated by G-09 and TE §18.3 — the same self-contradiction swept out of
`fixtures-and-reproducibility` on 2026-08-30. Editing a completed stage's artifact is
outside this stage's produces, so it is reported rather than fixed.

Reply `Looks correct` to proceed, or state what to change.

[Answer]: Looks correct
