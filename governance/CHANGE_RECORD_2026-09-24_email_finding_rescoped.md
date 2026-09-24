# Change record — 2026-09-24 — DATA-16 / Recommendation 39 rescoped into three findings

**Purpose.** The original `RULING_REQUEST_2026-09-21...` §1 treated "the personal email
finding" as one problem with one remediation (a single `.gitleaks.toml` allowlist entry). The
2026-09-24 session measured that this conflates three structurally different things that do
not share a mechanism. This record splits them and re-verifies every factual claim against
`git log`/`git grep` directly — shown below, not restated from the prior session's summary.
**Draft only.** Nothing is written to `evidence/DECISIONS.md`, `.gitleaks.toml`, any G-09
gate record, or any live markdown file. **Repository state:** working tree as left by the
prior session, nothing further committed.

---

## Verification run for this record (raw output, not restated)

```
$ git log --format="%H %ad %s" --date=short -- notebooks/madrigal_phase1_coverage_audit.ipynb
4cdd54941802538d98581c9f23faa1e6561ebef1 2026-09-20 Remediate GOV-2026-09-20-CG-01: all agent-doable limbs of the sixty findings, static only
33d231b5ea83265ef26a9c8eb0e51b4431ea96ce 2026-08-17 Initial commit: TEC forecasting thesis workspace

$ for c in 4cdd549... 33d231b...; do git show "$c:notebooks/madrigal_phase1_coverage_audit.ipynb" | grep -c "kiimiiarezaee2025@gmail.com"; done
4cdd549: 0
33d231b: 1

$ git grep -n "kiimiiarezaee2025@gmail.com" HEAD
aidlc/.../construction/features-and-splits/code-generation/code-summary.md:77   (quotes `git show` commit-AUTHOR output)
aidlc/.../construction/features-and-splits/code-generation/code-summary.md:142  (quotes `git show` commit-AUTHOR output)
aidlc/.../inception/requirements-analysis/requirements.md:268                   (quotes the notebook FINDING, DATA-16 origin)
governance/reviews/GOV-2026-08-20-RA-01.md:294                                  (states the notebook FINDING, DATA-16 itself)
governance/reviews/GOV-2026-09-20-CG-01.md:869                                  (restates the notebook FINDING with a line cite)

$ git log --all --format="%ae" | sort | uniq -c
    101 kiimiiarezaee2025@gmail.com
      1 s_inv@trade.local

$ git log --all --format="%H" --author="kiimiiarezaee2025@gmail.com" | wc -l
101
$ git log --all --format="%H" | wc -l
102
```

**What this changes from the prior session's numbers.** The commit count for the notebook
(1, not 4) and the "live at HEAD" finding are unchanged from the 2026-09-24 investigation.
New this pass: the exact split of the 5 live occurrences — **2 are commit-author-metadata
quotes (§B-3's territory), 3 are file-content leak documentation (§B-1's territory)** — and
the precise commit-author count for §B-3 (**101 of 102** commits, i.e. effectively the whole
history, all under the email this session's own environment context identifies as the
Student's own).

---

## §B-1 — Email literal in file content

**What is live, precisely.**

- **1 historical commit**, `33d231b` (2026-08-17), carries the literal inside
  `notebooks/madrigal_phase1_coverage_audit.ipynb`'s tracked content. The next (and only
  other) commit touching that file, `4cdd549` (2026-09-20), removed it — confirmed by
  reading both blobs directly, above. **Not "four commits"** — the DATA-16 finding's own
  count does not match measured history and should be treated as superseded by this
  re-derivation.
- **3 files currently live at HEAD** quote or restate the notebook finding, each
  reproducing the literal as part of describing the finding itself:
  `aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/requirements-analysis/requirements.md:268`,
  `governance/reviews/GOV-2026-08-20-RA-01.md:294`,
  `governance/reviews/GOV-2026-09-20-CG-01.md:869`.
  This is the circular-exposure shape you flagged: documenting the leak, in a file that
  stays tracked and readable, re-leaks it every time the repository is read from now on,
  independent of whether the original historical commit is ever touched.

**Sub-options.**

**(a) Redact-in-place for the 3 live files + a `.gitleaks.toml` entry for the 1 historical
commit.** Replace the literal with `<redacted-personal-email>` in the three markdown files
above — an ordinary content edit to files that are live right now, not a history rewrite, so
none of the `code_commit`-reference cost that ruled out rewriting `33d231b` applies. Pair it
with a `.gitleaks.toml` allowlist entry scoped to exactly commit `33d231b` and the notebook
path, closing TA-22's tree-and-history scan as "clean, with one disclosed, dated, narrowly
scoped historical exception."
> **Impact**: Removes the only *forward-looking* exposure (every future clone, every future
> reader of these three docs) at zero cost — nothing frozen, signed, or D-numbered is
> touched, and no `code_commit` reference breaks, since none of the three files is cited by
> its own commit hash for provenance. The one exception the allowlist still has to carry is
> exactly the immutable, irreversible case (history), which is the case the original ruling
> already correctly declined to rewrite.

**(b) Accept-and-disclose everywhere**, unchanged from the original §B proposal in substance,
just corrected to name **1 commit**, not 4, and to explicitly list the 3 live files as
"disclosed, not redacted."
> **Impact**: Simpler (one disposition, no file edits), but leaves the email readable in three
> actively-maintained documents indefinitely, for no benefit — nothing is gained by leaving a
> reversible, costless exposure in place merely because a harder, irreversible one exists
> alongside it.

**Recommend (a).** The historical commit and the live markdown files are not the same kind of
problem: one is truly stuck (rewriting breaks provenance project-wide, already correctly
rejected), the other is an ordinary edit to ordinary files that happens to cost nothing.
Treating them identically under "accept-and-disclose" extends the *history* argument to
material the *history* argument does not apply to.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-24 — option (a) approved by the owner, executed
>
> **Redacted, 3 files, re-confirmed unchanged before editing** (`git grep` re-run first;
> line numbers matched this record exactly):
> `aidlc/spaces/default/intents/260813-tec-hourly-forecast/inception/requirements-analysis/requirements.md:268`,
> `governance/reviews/GOV-2026-08-20-RA-01.md:294`,
> `governance/reviews/GOV-2026-09-20-CG-01.md:869`. Each edit replaces only the literal
> (`'<redacted-personal-email>'`) and adds an inline note dating the redaction and citing
> this record — the finding's substance, routing and Owner/gate citation are otherwise
> byte-identical. The 2 correctly-excluded occurrences in
> `features-and-splits/code-generation/code-summary.md` (quoting `git show` commit-author
> output, §B-3's territory) were **not** touched.
>
> **`.gitleaks.toml` updated**, one new `commits` field on the existing `[allowlist]`
> table (TOML forbids a second `[[allowlist]]` once a single table already exists —
> discovered by a failed parse, corrected; see the file's own comment for the full
> account), scoped to exactly commit `33d231b5ea83265ef26a9c8eb0e51b4431ea96ce`. Does not
> touch or widen the existing `paths`/`regexes` entries.
>
> **Verified with the real pinned scanner, not grep alone.** `gitleaks detect --source .
> --config .gitleaks.toml` (binary present at `/c/Users/LOTUS/bin/gitleaks`, version
> `8.18.4` — matches the pin) ran clean of this finding: **11 real leaks reported,
> none referencing the notebook, the email, or commit `33d231b`.** Gitleaks' default
> ruleset does not carry an email-address rule — it targets credential-shaped secrets
> (API keys, tokens), so this specific finding was never something the scanner itself
> would flag; the `.gitleaks.toml` entry is disclosure/documentation in the reviewed
> allowlist, not a suppression of an active finding. The 11 real leaks found
> (`aws-access-token`/`github-pat` in `tests/test_acquisition.py`, `generic-api-key`
> entropy hits in `graphify-out/cache/stat-index.json`) are unrelated to this task and
> not investigated further here.
>
> **Full working-tree scan for the raw literal** (`grep -rl`, not git-index-dependent):
> exactly **2** files still carry it —
> `features-and-splits/code-generation/code-summary.md` (§B-3, correctly untouched) and
> this change record itself (quoting verification command output, e.g. the `git grep`
> and `git log --author` results above). The latter is a findings-document describing
> the finding via its own verification transcript, not an operational leak — flagged per
> your own instruction to use judgement here; no further redaction applied to this file.
>
> **Nothing committed.** All edits are unstaged working-tree changes.

---

## §B-2 — Personal name/affiliation in the thirteen manifests

**What is live.** `user_fullname: "Kimia Rezaei"` and
`user_affiliation: "Amirkabir University of Technology"` appear in the request manifests
under `evidence/` (verified in the prior session: `grep -h "user_fullname\|user_affiliation"
evidence/audit_evidence_2022-01/request_manifest.json` returns both fields with real values).

**This is very likely not an NFR-SEC-01 concern.** A named thesis author's own name and
institutional affiliation, recorded as part of a data-acquisition identity requirement (the
Madrigal rules-of-the-road require a real identity on every request — the same requirement
DATA-16 itself cites as the reason an email had to be supplied at all), is standard academic
attribution, not a leaked secret, credential, or contact channel that enables spam or
impersonation the way an email address does. NFR-SEC-01's concern (credentials, keys,
contact-enabling PII) does not extend naturally to "the author's own name is visible in their
own data-request records."

**Recommend: no action.** Recorded here explicitly so a future reviewer does not re-flag this
as the same finding as §B-1 — it is a different kind of data, on a different footing, and the
original DATA-16 wording ("thirteen committed manifests carry `user_fullname`/
`user_affiliation`") should be read as a lower-severity, closed-as-non-issue item from here on,
distinct from the email.

**Decision required — Approve / Reject / Modify / Postpone.** *(Expected: fast approve —
recorded for completeness, not because a real risk is in question.)*

> ## ✅ RULED 2026-09-24 — approved by the owner, closed as a non-issue
>
> **Closure text**, recorded here as the canonical disposition (this change record is the
> closure record; no D-number applies — `evidence/DECISIONS.md` carries scientific/config
> freezes only, and this is a governance-finding disposition, not a scientific value, so it
> follows this project's actual convention for that class of item rather than being forced
> into the D-number register):
>
> *"The `user_fullname`/`user_affiliation` fields in the thirteen `request_manifest.json`
> files under `evidence/` (`Kimia Rezaei` / `Amirkabir University of Technology`) were
> investigated 2026-09-24 and are closed as a non-issue, distinct from the DATA-16/§B-1
> email finding. This is standard academic attribution — the thesis author's own name and
> institution, recorded as part of the Madrigal acquisition identity requirement that also
> necessitated the email field — not a leaked secret, credential, or contact-enabling PII
> value the way an email address is. No remediation is required. A future reviewer should
> not re-flag this as the same class of finding as the redacted email."*
>
> **Also recorded inline at the finding's original sites** (part of the §B-1 redaction
> edits above, so this disposition travels with the finding rather than living only here):
> `requirements.md:268` and both GOV review file entries now each carry a parenthetical
> pointing back to this §B-2 closure.
>
> **No file edit beyond the inline pointers already made under §B-1.** No `.gitleaks.toml`
> entry (nothing to allowlist — this was never a scanner finding). No D-number written.

---

## §B-3 — Email in git commit author metadata

**What is live, precisely.** `kiimiiarezaee2025@gmail.com` is the commit-author email on
**101 of the repository's 102 total commits** across all refs (measured above) — effectively
the entire project history, not a bounded handful. This is a structurally different surface
from §B-1: it lives in each commit object's `author`/`committer` fields, not in any tracked
file's content, so **no `.gitleaks.toml` mechanism reaches it** — that tool scans blobs, not
commit metadata. The only way to change it is rewriting commit metadata across effectively
the whole history (`git filter-repo` with a mailmap, or equivalent), which is exactly the
class of fix the original §B ruling already rejected, for the same reason: every `code_commit`
reference recorded in the experiment registry, environment locks, and change records
project-wide would go dangling. That rejection is **not** re-litigated here — it applies with
equal or greater force to 101 commits than it did to the 4 (really 1) the original finding
named for §B-1.

**Whose email this is.** This is the Student's own email — the commit author identity
configured for this repository's git user matches the account under which this whole project
is authored (confirmed by cross-reference: it is the same address as the notebook's
`USER_EMAIL` literal in §B-1, and the same address DATA-16 itself traces to the Madrigal
acquisition identity requirement). **This is self-disclosure of one's own authorship
identity as commit author — not exposure of a third party's contact information.** That
materially lowers this finding's severity: a git repository disclosing who wrote it, under
their own name/email, is closer to normal authorship attribution (the same category as
§B-2's name/affiliation) than to a genuine PII leak, even though the surface (git metadata
vs. manifest field) differs.

**No rewrite proposed.** Given the above, drafting an accept-and-disclose option scoped
narrowly to this surface, distinct from §B-1's file-content exception:

> **Proposed gate-record note (G-09).** *"The repository's git history discloses the
> Student's own name and email as commit author on the substantial majority of commits
> (101/102, measured 2026-09-24). This is self-disclosure of the author's own identity as
> committer, not third-party PII exposure, and is analogous to §B-2's manifest
> attribution rather than to §B-1's file-content leak. No `.gitleaks.toml` mechanism applies
> to commit metadata; the only remediation would be a full-history rewrite
> (`git filter-repo`/mailmap), which is rejected for the same reason §B-1's historical commit
> rewrite was rejected — it would invalidate every `code_commit` reference recorded in the
> experiment registry, environment locks, and change records project-wide. Accepted and
> disclosed as a known, permanent condition of this project's git history."*

**Recommend: accept-and-disclose**, worded as above, with the self-disclosure point stated
explicitly so a future reviewer reads this as a materially lower-severity item than §B-1.

**Decision required — Approve / Reject / Modify / Postpone.**

> ## ✅ RULED 2026-09-24 — approved by the owner, accepted and disclosed
>
> **Gate-record note, recorded verbatim as drafted** (canonical home: this change record,
> for the same reason as §B-2 — a governance-finding disposition, not a D-numbered
> scientific/config value):
>
> *"The repository's git history discloses the Student's own name and email as commit
> author on the substantial majority of commits (101/102, measured 2026-09-24). This is
> self-disclosure of the author's own identity as committer, not third-party PII exposure,
> and is analogous to §B-2's manifest attribution rather than to §B-1's file-content leak.
> No `.gitleaks.toml` mechanism applies to commit metadata; the only remediation would be a
> full-history rewrite (`git filter-repo`/mailmap), which is rejected for the same reason
> §B-1's historical commit rewrite was rejected — it would invalidate every `code_commit`
> reference recorded in the experiment registry, environment locks, and change records
> project-wide. Accepted and disclosed as a known, permanent condition of this project's
> git history."*
>
> **No rewrite attempted or proposed** — no `git filter-repo`, mailmap, or any history
> mutation was run. No file edit (nothing in tracked file content to edit — this surface is
> commit metadata only). No `.gitleaks.toml` entry (confirmed inapplicable: gitleaks scans
> blob content, not commit `author`/`committer` fields).

---

## What happens on approval (stated, not executed)

- **§B-1(a)**: replace the literal with `<redacted-personal-email>` in the three named
  markdown files; add a `.gitleaks.toml` allowlist entry naming exactly commit `33d231b` and
  `notebooks/madrigal_phase1_coverage_audit.ipynb`; write the TA-22 gate-record note.
- **§B-2**: write a one-line "investigated, no action, distinct from §B-1" note into the G-09
  gate record. No file edit.
- **§B-3**: write the drafted gate-record note above into the G-09 record verbatim (or as
  modified). No file edit, no `.gitleaks.toml` entry (none applies).

**STOP.** No file is edited, no allowlist entry is added, and no gate-record note is written
beyond this draft until the owner rules on each of §B-1/§B-2/§B-3 above.
