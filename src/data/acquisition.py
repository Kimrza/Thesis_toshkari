"""Acquisition library: redaction chokepoint, bounded retrieval, provenance manifests.

Purpose
-------
The `acquisition` unit's library surface (Q2 = A, receipted: a NEW module,
`src/data/acquisition.py`). Four responsibilities, each a workflow of the approved
functional design:

1. **The redaction serializer (W-9, R-39, SD-A-02).** One declared chokepoint —
   `guard_egress_value`, with `guard_egress` its recursive form. A **signed request URL**
   and an **auth header** are refused UNCONDITIONALLY on structural detection — the
   allowlist is never consulted for them. Everything else passes an entropy/prefix
   heuristic that **blocks the write and names what it matched**. `CredentialEgressError`
   is integrity tier: the run terminates and the `aborted` registry row is written through
   the stage entry contract's `IntegrityError` catch.

   **What the chokepoint covers, stated exactly** (the claim is pinned by
   `tests/test_acquisition.py`, not left to prose). Every value this unit writes to a
   manifest or notebook output: `write_request_manifest` and `write_sha256_manifest` guard
   their FULL payload before a byte is written, and `RetrievalClient.retrieve` guards each
   provider-file record it returns. On the LOG side the covered surface is the experiment
   registry's operator-composed free-text columns — `notes` and `reason` — routed at
   `experiment_registry.append_registry_event` through
   `experiment_registry.REDACTED_FREE_TEXT_FIELDS`, which is where a live provider
   transport's error text would otherwise reach a permanent artifact. The registry's
   remaining columns are machine-generated from a schema-fixed vocabulary (ids, ISO
   timestamps, hex digests, the derived extension fields) and are OUT of that routing by
   design: they are token-shaped by construction, so routing them would force exactly the
   allowlist growth `REDACTION_ALLOWLIST`'s own rule forbids. Anything else a stage script
   prints to stderr is a transient console line, not an artifact this unit writes.

   **Two tiers, one chokepoint.** `guard_egress_value` (and its recursive form
   `guard_egress`) is a per-VALUE detector: correct for a manifest field, which holds one
   value. `guard_egress_free_text` adds the EMBEDDED tier for prose fields — it runs the
   per-value detector unchanged, then walks the value's tokens for the two STRUCTURAL
   carriers and the published token prefixes, because a caught exception deposits a request
   URL or a response header mid-sentence rather than as the whole field. The entropy
   heuristic is deliberately NOT run per token, for the reason stated on
   `_embedded_carrier_reason`. A credential that is neither a structural carrier nor a
   published prefix and appears only mid-sentence remains undetected on every surface of
   this unit — a stated limit of the design, pinned by a must-not-fire test rather than
   left as an assumption.
2. **The bounded-retry retrieval client (W-1, SD-A-01, TS-A-01/03).** Bounded retry
   with exponential backoff and full jitter on transient transport failure; resumption
   where the transport supports it; the **completeness check runs BEFORE the hash** —
   a partial retrieval never yields a manifest row with a hash, because a truncated
   file hashed at truncation verifies against itself forever. A re-run that observes a
   different hash **records the divergence (both provider filenames including version
   suffixes, both hashes) and refuses to overwrite** (SEC-A-02).
3. **The manifest writers (W-3, W-4, W-7; R-34, R-36, R-37, R-40, R-41, R-42).**
   `request_manifest.json` and `sha256_manifest.json`, carrying full provider
   filenames including version suffixes, retrieval dates and SHA-256 per provider
   file; `suffix_mismatch` recorded machine-readably at retrieval and **refused at
   release**; driver rows carrying a `release_status` grade that is never mixed within
   one series; gaps stored as explicit NaN with the NaN-count conservation invariant
   carried on the manifest; and R-42's derived-release provenance check. Every manifest
   this unit writes carries the three TE 13 definition IDs (`phase_id`, `source_id`,
   `target_definition_id`) through the one `assert_identity_stamped` refusal — added
   2026-09-20 on board finding TEC-05, which found the provenance HEAD of the chain
   unstamped while stage 02 onward stamped thoroughly. `stamps` is a REQUIRED argument
   on all three writers: a default would preserve exactly the silence being closed.
4. **The notebook saved-output check (W-9 limb 2, Q3 = A).** The testable helper the
   pre-commit hook calls: a staged notebook carrying saved outputs or execution counts
   fails closed, and nothing is auto-stripped.

Inputs
------
An injected transport callable (the live provider client is NOT constructed here —
network retrieval is exercised against recorded-response fixtures only while BLK-07
stands, and TE 8.1 permits `requests` only "where provider terms permit"); provider
response metadata; prior `ProviderFileRecord`s for divergence comparison; series
values for gap accounting; notebook JSON for the output check. Credentials reach a
provider client directly from the environment via `foundation`'s resolution
(`src/data/config.py`) — never through this module, which handles credential NAMES
never and credential VALUES only in the sense of refusing to serialize anything
shaped like one.

Re-run behaviour
----------------
Pure functions and writers of new files. `RetrievalClient.retrieve` re-run against an
unchanged provider is byte-identical; against a reissued provider file it records the
divergence and leaves the previously retrieved bytes untouched (SEC-A-02). The
manifest writers overwrite their own target path (a manifest is regenerated per run,
and the run snapshot is the evidence of what a prior run wrote). No function here
reads, logs or persists a credential value, and **no code path constructs a path into
the restricted December evidence root** — restricted access is `governance-guards`'
`src/data/locked_test.py` chokepoint, which this module does not even name (R-32,
R-28).

Governance
----------
* `AcquisitionError` and `CredentialEgressError` derive from `IntegrityError`
  (`foundation` R-01's "any future integrity-related exception" clause), declared
  HERE because this module is their sole raiser (`business-rules.md` § The two tiers;
  Q2 = A receipted 2026-09-05).
* The retry/backoff/timeout values below are OPERATIONAL values, not scientific
  constants (SD-A-01's ⚠ box): approved at the 3.5 plan gate (5 attempts; base 1 s,
  factor 2, cap 60 s, full jitter; 60 s per-request timeout) and recorded in the run
  record and every request manifest via `retrieval_policy()` so a retrieval's
  behaviour is reconstructible.
* `LOCKED_YEAR`/`LOCKED_MONTH` are the D-8/D-15 governance boundary identity
  (December 2022, the locked test month) — a boundary identifier like
  `RESTRICTED_ROOT`, never a scientific constant (TC-03e governs scientific values;
  the locked month is fixed by decision record, not chosen here). Membership is
  derived from RECORD TIMESTAMPS, never from a directory or file name (R-31,
  project.md § Forbidden). **No acquisition run may touch calendar 2022-12 while
  BLK-07 stands** — `assert_no_locked_month_records` is the executable form.
* Record-date attribution is **UTC**, via `parse_record_date_utc` (R-46, added
  2026-09-20). The former `raw[:10]` slice attributed an offset-bearing timestamp to its
  LOCAL date: `2022-11-30T23:30:00-05:00` is `2022-12-01T04:30:00Z`, a December record a
  slice files under November and walks past the BLK-07 bar. All observed data carries
  `+00:00`, so the defect was latent — but this derivation decides locked-month
  membership and the DATA-07 re-acquisition is being written against it. `inventory`
  wraps the SAME parser in its own integrity type, so the rule has one derivation home.
"""

from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import json
import re
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from src.data.config import IntegrityError, ReleaseError
from src.data.release import sha256_of_file

__all__ = [
    "AcquisitionError",
    "CredentialEgressError",
    "RETRY_MAX_ATTEMPTS",
    "RETRY_BACKOFF_BASE_S",
    "RETRY_BACKOFF_FACTOR",
    "RETRY_BACKOFF_CAP_S",
    "RETRY_JITTER",
    "REQUEST_TIMEOUT_S",
    "retrieval_policy",
    "REDACTION_ALLOWLIST",
    "guard_egress_value",
    "guard_egress_free_text",
    "guard_egress",
    "TransportResult",
    "RetrievalClient",
    "PROVENANCE_CLASSES",
    "cited_stations",
    "read_records_csv",
    "select_station_records",
    "select_records_within_window",
    "verify_declared_inputs",
    "write_fixture_read_manifest",
    "FIXTURE_READ_MANIFEST_NAME",
    "DRIVER_INVENTORY_FIELDS",
    "LOCKED_YEAR",
    "LOCKED_MONTH",
    "TEC05_STAMP_FIELDS",
    "assert_identity_stamped",
    "parse_record_date_utc",
    "store_gaps_as_nan",
    "count_gaps",
    "gap_accounting_entry",
    "assert_gap_conservation",
    "assert_madrigalweb_version",
    "assert_driver_inventory",
    "assert_single_release_grade",
    "write_request_manifest",
    "write_sha256_manifest",
    "SHA256_MANIFEST_META_NAME",
    "assert_release_free_of_unresolved_mismatch",
    "assert_derived_release_provenance",
    "partition_by_locked_month",
    "assert_no_locked_month_records",
    "assert_records_within_window",
    "notebook_output_violations",
    "notebook_output_violations_from_text",
]


class AcquisitionError(IntegrityError):
    """An acquisition invariant is violated (integrity tier, two-tier posture).

    Raised for: retry exhaustion on transient transport failure; a driver series
    carrying fewer than TE 5.1's nine inventory fields or a mixed release grade; a
    missing/`"unknown"` `madrigalWeb_version`; a broken NaN-count conservation
    invariant; a record whose timestamp cannot establish locked-month membership; a
    locked-month record reaching an acquisition output while BLK-07 stands.
    Completeness shortfalls (a missing month, a partial retrieval, a suffix mismatch
    at retrieval) are NOT this exception — they are machine-readable manifest fields
    (`team.md` § Code Style, the non-fatal tier).
    """


class CredentialEgressError(IntegrityError):
    """The redaction boundary was handed an unredacted credential-bearing value.

    Sole-raising module: this one (W-9's `RAISES` block). Derives from
    `IntegrityError` under `foundation` R-01's "any future integrity-related
    exception" clause, so the stage entry contract's `except IntegrityError` catch
    writes the `aborted` registry row — outside the hierarchy, a credential-egress
    violation would exit unrecorded, in the unit that owns the redaction boundary.
    """


# =======================================================================================
# Operational retrieval policy (SD-A-01's owed values, approved at the 3.5 plan gate)
# =======================================================================================

#: Maximum transport attempts per file. Bounded so a failing provider cannot become an
#: unbounded loop inside a Kaggle session (SD-A-01). Operational, not scientific.
RETRY_MAX_ATTEMPTS: Final[int] = 5

#: Exponential backoff: base 1 s, factor 2, cap 60 s, FULL jitter (sleep is drawn
#: uniformly from [0, min(cap, base * factor**attempt)]).
RETRY_BACKOFF_BASE_S: Final[float] = 1.0
RETRY_BACKOFF_FACTOR: Final[float] = 2.0
RETRY_BACKOFF_CAP_S: Final[float] = 60.0
RETRY_JITTER: Final[str] = "full"

#: Per-request connect+read timeout, seconds.
REQUEST_TIMEOUT_S: Final[float] = 60.0


def retrieval_policy() -> dict[str, object]:
    """The operational retrieval values, as recorded in the run record and manifests.

    SD-A-01: each value is recorded so a retrieval's behaviour is reconstructible
    after the fact. These are operational values, not scientific constants — TE 18.2's
    freeze-gate rule does not reach them — approved at the 3.5 plan gate (2026-09-05).
    """
    return {
        "retry_max_attempts": RETRY_MAX_ATTEMPTS,
        "retry_backoff_base_s": RETRY_BACKOFF_BASE_S,
        "retry_backoff_factor": RETRY_BACKOFF_FACTOR,
        "retry_backoff_cap_s": RETRY_BACKOFF_CAP_S,
        "retry_jitter": RETRY_JITTER,
        "request_timeout_s": REQUEST_TIMEOUT_S,
    }


# =======================================================================================
# W-9 / R-39 / SD-A-02: the redaction serializer
# =======================================================================================

#: URL schemes whose query string can carry a signature (the "signed request URL"
#: carrier SD-A-02 names). Structural, not heuristic.
_URL_SCHEMES: Final[frozenset[str]] = frozenset({"http", "https", "ftp", "ftps", "s3", "gs"})

#: Query-parameter names that make a URL a SIGNED url structurally. Lower-cased
#: comparison. Membership here is a structural fact about signing schemes (AWS SigV2/
#: SigV4, GCS, Azure SAS, generic token grants), not an entropy guess.
_SIGNED_QUERY_MARKERS: Final[frozenset[str]] = frozenset(
    {
        "sig",
        "signature",
        "x-amz-signature",
        "x-amz-credential",
        "x-amz-security-token",
        "x-goog-signature",
        "x-goog-credential",
        "awsaccesskeyid",
        "token",
        "access_token",
        "id_token",
        "private_token",
        "apikey",
        "api_key",
        "sas_token",
        "sv",  # Azure SAS: storage service version + sig travel together; sig also listed
    }
)

#: Auth-header shapes, refused unconditionally (the second named carrier).
_AUTH_HEADER_RE: Final[re.Pattern[str]] = re.compile(
    r"^\s*(authorization|proxy-authorization|x-api-key|x-auth-token)\s*:", re.IGNORECASE
)
_AUTH_SCHEME_RE: Final[re.Pattern[str]] = re.compile(
    r"^\s*(basic|bearer|digest|token|oauth|aws4-hmac-sha256|negotiate|ntlm)\s+\S+",
    re.IGNORECASE,
)

#: Known credential prefixes, each named so a refusal says what it matched.
#: (name shown in the error, prefix). Prefixes are provider-published token formats,
#: not secrets themselves.
_KNOWN_CREDENTIAL_PREFIXES: Final[tuple[tuple[str, str], ...]] = (
    ("AWS access key id", "AKIA"),
    ("AWS temporary access key id", "ASIA"),
    ("GitHub personal access token", "ghp_"),
    ("GitHub OAuth token", "gho_"),
    ("GitHub fine-grained token", "github_pat_"),
    ("GitLab personal access token", "glpat-"),
    ("Slack bot token", "xoxb-"),
    ("Slack user token", "xoxp-"),
    ("OpenAI-style secret key", "sk-"),
    ("Google API key", "AIza"),
    ("Google OAuth access token", "ya29."),
    ("JSON Web Token", "eyJ"),
)

#: The false-positive ALLOWLIST — a REVIEW SURFACE, and the documented rule is that it
#: is NEVER grown to silence a failure (SD-A-02's ⚠ box: "an exception list widened
#: once per incident eventually misses the thing it was built to catch"). Every entry
#: names WHY the shape is legitimate. Consulted ONLY for the heuristic tier — the two
#: structural carriers (signed URL, auth header) are refused before it is read.
#: Any addition is a reviewed edit, exactly like `governance-guards`'
#: RESTRICTED_LITERAL_EXEMPT_MODULES (SD-G-03's source-constant precedent).
REDACTION_ALLOWLIST: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("sha256 hex digest (W-4 manifests carry one per file)", re.compile(r"^[0-9a-f]{64}$")),
    ("sha256 12-hex prefix (D-29 dataset_version)", re.compile(r"^[0-9a-f]{12}$")),
    (
        "UUID (run and snapshot identifiers)",
        re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        ),
    ),
    ("git commit hex (environment lock code_commit)", re.compile(r"^[0-9a-f]{40}$")),
    # Added 2026-09-18 under the owner's G-2 instruction (CR-2026-09-18-GFZ-DRIVER-PAIR-AUDIT
    # §5.3), NARROWED 2026-09-19 on review (CR-2026-09-19-GATE-PREP-2 § G-2): a PROVIDER
    # DATA FILENAME — a stem of at least two runs joined by `.`/`_`/`-`, a known data-file
    # extension, ≤ 48 characters, where every run is a lower-case word/number, an
    # upper-case acronym/number (`SN`, `F107`, `FULL`), or a capitalised word with at most
    # one further capital (`Hp60ap60doi`, `Kp`). The shape the five recorded false positives
    # share and that no published credential format shares; the run rule is what refuses a
    # secret dressed with a separator and an extension (`Q7r8S9t0U1v2_W3x4Y5z6.txt`,
    # `wJalrXUtnFEMI_K7MDENG_bPxRfiCYEXAMPLEKEY.dat`). Known credential PREFIXES are checked
    # BEFORE the allowlist (see `_heuristic_reason`), so `AKIA…_2022.txt` is still refused.
    # Stated residual: a secret composed ONLY of lower-case+digit runs, joined by
    # separators, under 48 chars, with a data extension, would pass — no known provider
    # issues secrets of that shape, and the two structural carriers (signed URL, auth
    # header) are refused before this list is read.
    (
        "provider data filename (word-shaped runs joined by separators, data extension, <= 48 chars)",
        re.compile(
            r"^(?=.{1,48}$)"
            r"(?:[a-z0-9]+|[A-Z0-9]+|[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)?)"
            r"(?:[._\-](?:[a-z0-9]+|[A-Z0-9]+|[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)?))+"
            r"\.(?:txt|wdc|csv|tsv|json|jsonl|html|htm|hdf5|h5|nc|dat|zip|gz|tar|tgz|"
            r"yaml|yml|md|log|xml|parquet|npy|ipynb|pdf)$"
        ),
    ),
)

#: Heuristic token charset and thresholds. A guess, stated rather than hidden
#: (SD-A-02: "everything else genuinely is a guess — and a guess that BLOCKS is still
#: correct when the artifact is committed and permanent").
_TOKEN_CHARSET_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9+/=_.\-]{20,}$")


def _signed_url_reason(text: str) -> str | None:
    """Structural signed-URL detection. Returns the reason, or None."""
    if "://" not in text:
        return None
    from urllib.parse import parse_qsl, urlsplit  # stdlib; deferred to keep import cost low

    try:
        parts = urlsplit(text.strip())
    except ValueError:
        return None
    if parts.scheme.lower() not in _URL_SCHEMES:
        return None
    if parts.username or parts.password:
        return "URL embeds userinfo credentials (user:password@host)"
    if parts.query:
        names = {name.lower() for name, _ in parse_qsl(parts.query, keep_blank_values=True)}
        hit = sorted(names & _SIGNED_QUERY_MARKERS)
        if hit:
            return f"signed request URL (query parameter(s) {', '.join(hit)})"
    return None


def _auth_header_reason(text: str) -> str | None:
    """Structural auth-header detection. Returns the reason, or None."""
    if _AUTH_HEADER_RE.match(text):
        return "auth header (Authorization/Proxy-Authorization/X-Api-Key/X-Auth-Token)"
    if _AUTH_SCHEME_RE.match(text):
        return "auth header value (Basic/Bearer/Digest/Token/OAuth/AWS4-HMAC-SHA256 scheme)"
    return None


def _heuristic_reason(text: str) -> str | None:
    """The entropy/prefix heuristic. Returns what it matched, or None. Allowlist-gated.

    Tuned width, stated: THREE mixed case+digit classes in one unbroken token is
    refused at length 20+; TWO classes are refused only at length 32+ WITHOUT
    filename-style separators (`.`/`_`/`-`/`/`), because a long lowercase+digit
    token with separators is the shape of a provider filename
    (`dst_provisional_202211.html`), while a long two-class run without any is the
    shape of a hex/base32 secret. A false positive lands on the allowlist under
    review; a false negative is caught by nothing else in-process (SD-A-02).
    """
    candidate = text.strip()
    # Known credential PREFIXES first (2026-09-18, G-2): a published prefix is a positive
    # identification and must not be reachable through any allowlisted shape — the
    # filename entry above could otherwise pass `AKIA…_2022.txt`. The four earlier
    # allowlist shapes (hex digests, UUID, git hex) never start with a listed prefix, so
    # their acceptance is unchanged by the reordering.
    for name, prefix in _KNOWN_CREDENTIAL_PREFIXES:
        if candidate.startswith(prefix):
            return f"known credential prefix {prefix!r} ({name})"
    for _allow_name, pattern in REDACTION_ALLOWLIST:
        if pattern.match(candidate):
            return None  # legitimate high-entropy shape, named on the allowlist
    if _TOKEN_CHARSET_RE.match(candidate):
        classes = sum(
            1
            for probe in (str.islower, str.isupper, str.isdigit)
            if any(probe(ch) for ch in candidate)
        )
        has_separator = any(ch in "._-/" for ch in candidate)
        if classes == 3 or (classes == 2 and len(candidate) >= 32 and not has_separator):
            return (
                f"high-entropy token-shaped value (length {len(candidate)}, "
                f"{classes} character classes{', no separators' if not has_separator else ''})"
            )
    return None


def guard_egress_value(value: object, *, context: str) -> object:
    """The one declared redaction chokepoint for a single value (W-9, R-39, Q1 = A).

    Order is the rule: the two STRUCTURAL carriers — a signed request URL and an auth
    header — are refused UNCONDITIONALLY, before the allowlist is consulted, so the
    certain cases are never exposed to the tuning pressure generated by the uncertain
    ones (SD-A-02). Everything else passes the allowlist (legitimate hashes, UUIDs,
    commit hex), then the prefix/entropy heuristic, which blocks and NAMES what it
    matched.

    Raises
    ------
    CredentialEgressError
        naming the write context and what was detected. Integrity tier: the run
        terminates and the `aborted` row is written through the `IntegrityError`
        catch. Never log the refused value itself — the error carries the DETECTION,
        not the credential.
    """
    if not isinstance(value, str):
        return value
    for detector in (_signed_url_reason, _auth_header_reason):
        reason = detector(value)
        if reason:
            raise CredentialEgressError(
                context,
                f"refused unconditionally: {reason}; a signed URL or auth header is a "
                f"credential carrier and never enters a manifest, log, registry note "
                f"or notebook output (TE 10, NFR-SEC-01, R-39) — the allowlist is "
                f"never consulted for a structural carrier",
            )
    reason = _heuristic_reason(value)
    if reason:
        raise CredentialEgressError(
            context,
            f"blocked by the credential-shape heuristic: {reason}; if this value is "
            f"legitimate, the fix is a REVIEWED addition to REDACTION_ALLOWLIST "
            f"naming why the shape is safe — the allowlist is a review surface, "
            f"never grown to silence a failure (SD-A-02)",
        )
    return value


#: Punctuation stripped from a prose token before the embedded-carrier detectors read it,
#: so `"(ghp_...)"` and a comma-terminated URL are still recognised. The trimmed form is
#: checked IN ADDITION to the raw token, never instead of it: `:` is in this set and an auth
#: header's detection depends on the colon, so trimming alone would hide the very carrier the
#: tier exists to catch. Checking both can only widen detection, never narrow it.
_FREE_TEXT_TRIM: Final[str] = "()[]{}<>\"'`,;:!?"


def _embedded_carrier_reason(token: str) -> str | None:
    """The EMBEDDED-carrier tier: structural carriers and published token prefixes only.

    Deliberately excludes the entropy heuristic, and the exclusion is evidenced rather than
    convenient. Prose legitimately carries run ids (`acquisition-20260910T120000Z-a1b2c3d4`)
    and snapshot directory names, which are three-character-class tokens well over the
    heuristic's length floor: running the entropy tier per token would refuse a legitimate
    `aborted` record — destroying the audit row NFR-AUD-01 exists to keep — and the only
    repair would be growing `REDACTION_ALLOWLIST`, the one act SD-A-02's ⚠ box forbids.
    A structural carrier and a published prefix carry no such ambiguity.
    """
    for detector in (_signed_url_reason, _auth_header_reason):
        reason = detector(token)
        if reason:
            return reason
    for name, prefix in _KNOWN_CREDENTIAL_PREFIXES:
        if token.startswith(prefix):
            return f"known credential prefix {prefix!r} ({name})"
    return None


def guard_egress_free_text(value: object, *, context: str) -> object:
    """The FREE-TEXT form of the chokepoint (W-9, R-39): whole value, then embedded carriers.

    `guard_egress_value` is a per-VALUE detector — correct for a manifest field, which holds
    one value, and insufficient for a prose field, which is where a caught exception's
    `str(exc)` deposits a request URL or a response header MID-SENTENCE. This variant runs
    the declared chokepoint over the whole value first (unchanged semantics, nothing
    weakened), then walks the value's whitespace-separated tokens through
    `_embedded_carrier_reason`.

    Use it for operator-composed prose only — the experiment registry's
    `REDACTED_FREE_TEXT_FIELDS`. Structured payloads keep `guard_egress`: this is a second
    TIER of the same chokepoint, not a second chokepoint (nfr-design c58).

    Raises
    ------
    CredentialEgressError
        naming the write context and what was detected, never the value itself.
    """
    guard_egress_value(value, context=context)
    if not isinstance(value, str):
        return value
    for token in value.split():
        reason = None
        for candidate in (token, token.strip(_FREE_TEXT_TRIM)):
            if not candidate:
                continue
            reason = _embedded_carrier_reason(candidate)
            if reason:
                break
        if reason:
            raise CredentialEgressError(
                context,
                f"refused: {reason} EMBEDDED in a free-text field; prose is where a caught "
                f"exception's message deposits a request URL or a response header, and a "
                f"permanent log never carries a credential carrier (TE 10, NFR-SEC-01, "
                f"R-39) — the embedded tier detects structural carriers and published token "
                f"prefixes, never the entropy heuristic",
            )
    return value


def guard_egress(obj: object, *, context: str) -> object:
    """Recursively apply `guard_egress_value` to every string in a payload.

    Mapping KEYS are guarded as well as values: a credential used as a key is still
    egress. Returns the object unchanged when clean; raises on the first detection.
    """
    if isinstance(obj, str):
        return guard_egress_value(obj, context=context)
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            guard_egress(key, context=f"{context}.{key}" if isinstance(key, str) else context)
            guard_egress(value, context=f"{context}.{key}" if isinstance(key, str) else context)
        return obj
    if isinstance(obj, list | tuple | set | frozenset):
        for index, item in enumerate(obj):
            guard_egress(item, context=f"{context}[{index}]")
        return obj
    return obj


# =======================================================================================
# W-1 / SD-A-01: the bounded-retry retrieval client
# =======================================================================================


@dataclass(frozen=True)
class TransportResult:
    """What one transport call returned.

    `complete` is the transport's own completeness statement (declared length matched,
    terminal chunk seen). `resumable` says whether a follow-up call may pass an
    `offset` to continue rather than restart. `provider_filename` is the FULL provider
    filename including any version suffix (DATA-07: re-acquisition records the
    suffix; `g.002` versus `g.003` drift is observed in this dataset).
    """

    data: bytes
    complete: bool
    provider_filename: str
    resumable: bool = False


class RetrievalClient:
    """Bounded-retry, rate-bounded retrieval against an INJECTED transport (TS-A-01).

    The transport is a callable `(spec, offset, timeout) -> TransportResult`. No live
    provider client is constructed here: network retrieval is exercised against
    recorded-response fixtures only in this environment, and TE 8.1 permits `requests`
    only "where provider terms permit" — the rate bound below (`min_interval_s`) is
    that permission's mechanical form. Exceptions in `retryable` are transient
    transport failures and are retried with full-jitter exponential backoff; retry
    exhaustion is integrity tier.

    `sleep`, `rng` and `monotonic` are injectable so tests are deterministic; the
    defaults are the real clock. `rng` returns a float in [0, 1) — full jitter draws
    the sleep uniformly from [0, min(cap, base * factor**attempt)].
    """

    def __init__(
        self,
        transport: Callable[[Mapping[str, Any], int, float], TransportResult],
        *,
        min_interval_s: float = 0.0,
        retryable: tuple[type[BaseException], ...] = (OSError, TimeoutError),
        sleep: Callable[[float], None] | None = None,
        rng: Callable[[], float] | None = None,
        monotonic: Callable[[], float] | None = None,
    ) -> None:
        import random  # deferred: R-05's module-scope prohibition is transitive
        import time

        self._transport = transport
        self._min_interval_s = min_interval_s
        self._retryable = retryable
        self._sleep = sleep if sleep is not None else time.sleep
        # Full jitter is scheduling, not science or cryptography (operational value).
        self._rng = rng if rng is not None else random.random  # noqa: S311
        self._monotonic = monotonic if monotonic is not None else time.monotonic
        self._last_request_at: float | None = None

    def _respect_rate_bound(self) -> None:
        if self._min_interval_s <= 0 or self._last_request_at is None:
            return
        elapsed = self._monotonic() - self._last_request_at
        remaining = self._min_interval_s - elapsed
        if remaining > 0:
            self._sleep(remaining)

    def _backoff(self, attempt: int) -> None:
        ceiling = min(RETRY_BACKOFF_CAP_S, RETRY_BACKOFF_BASE_S * RETRY_BACKOFF_FACTOR**attempt)
        self._sleep(ceiling * self._rng())

    def retrieve(
        self,
        spec: Mapping[str, Any],
        *,
        dest_dir: Path,
        prior_record: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Retrieve one provider file; return its `ProviderFileRecord` mapping.

        `spec` carries the provider request identity — at minimum `provider`,
        `permanent_citation`, `location_date` and `logical_name` (the destination
        filename). `prior_record` is the previously recorded record for the same
        logical file, if any, read for divergence and suffix comparison (SEC-A-02,
        R-34).

        Ordering that IS the requirement (SD-A-01): the completeness check runs
        BEFORE the hash. An incomplete retrieval returns a record with
        `status = "incomplete"` and NO `sha256` key, and writes NO destination file —
        never a short file that looks whole.

        Divergence (SEC-A-02): when the retrieved bytes hash differently from
        `prior_record["sha256"]`, the record carries a machine-readable `divergence`
        field with BOTH provider filenames (including version suffixes) and BOTH
        hashes, the on-disk file is NOT overwritten, and the record's top-level
        `sha256` remains the recorded (on-disk) one. Provider reissue is a normal
        event; releasing it as though it were the recorded file is what
        `assert_release_free_of_unresolved_mismatch` refuses.

        Raises
        ------
        AcquisitionError
            on retry exhaustion (integrity tier: the transient failure persisted
            beyond the bounded policy) or a spec missing its identity fields.
        CredentialEgressError
            when any recorded value is credential-shaped (every record value passes
            the W-9 chokepoint).
        """
        for required in ("provider", "permanent_citation", "location_date", "logical_name"):
            if not str(spec.get(required, "")).strip():
                raise AcquisitionError(
                    str(spec.get("logical_name", "<unnamed spec>")),
                    f"retrieval spec field {required!r} is missing or empty; the six "
                    f"TE 13.3 source_files items are recorded per retrieved file "
                    f"(R-34, DATA-09) and cannot be recorded from an empty spec",
                )

        logical_name = str(spec["logical_name"])
        buffer = b""
        resumable = False
        result: TransportResult | None = None
        attempts = 0
        for attempt in range(RETRY_MAX_ATTEMPTS):
            attempts = attempt + 1
            self._respect_rate_bound()
            try:
                self._last_request_at = self._monotonic()
                result = self._transport(spec, len(buffer) if resumable else 0, REQUEST_TIMEOUT_S)
            except self._retryable as exc:
                if attempt == RETRY_MAX_ATTEMPTS - 1:
                    raise AcquisitionError(
                        logical_name,
                        f"transient transport failure persisted beyond the bounded "
                        f"retry policy ({RETRY_MAX_ATTEMPTS} attempts, backoff base "
                        f"{RETRY_BACKOFF_BASE_S} s factor {RETRY_BACKOFF_FACTOR} cap "
                        f"{RETRY_BACKOFF_CAP_S} s, full jitter): {exc}",
                    ) from exc
                self._backoff(attempt)
                continue
            if resumable and result.resumable:
                buffer += result.data
            else:
                buffer = result.data
            resumable = result.resumable
            if result.complete:
                break
            if attempt == RETRY_MAX_ATTEMPTS - 1:
                break
            self._backoff(attempt)

        retrieval_date = _dt.datetime.now(_dt.timezone.utc).date().isoformat()
        record: dict[str, Any] = {
            # TE 13.3's six source_files items (R-34 as corrected 2026-08-25, DATA-09):
            "provider": str(spec["provider"]),
            "permanent_citation": str(spec["permanent_citation"]),
            "location_date": str(spec["location_date"]),
            "provider_filename": result.provider_filename if result else "",
            "retrieval_date": retrieval_date,
            # plus the machine-readable completeness/divergence fields:
            "attempts": attempts,
            "suffix_mismatch": None,
            "divergence": None,
        }

        if result is None or not result.complete:
            # Completeness BEFORE hash: no sha256 key, no destination file, target
            # absent — never a short file that looks whole (SD-A-01).
            record["status"] = "incomplete"
            return guard_egress(record, context=f"provider_file_record[{logical_name}]")

        digest = hashlib.sha256(buffer).hexdigest()
        prior = dict(prior_record or {})
        prior_filename = str(prior.get("provider_filename", "") or "")
        prior_sha256 = str(prior.get("sha256", "") or "")

        if prior_filename and prior_filename != result.provider_filename:
            # R-34 step 1-2: non-fatal at retrieval, recorded machine-readably.
            record["suffix_mismatch"] = {
                "recorded_provider_filename": prior_filename,
                "retrieved_provider_filename": result.provider_filename,
                "resolved_by": None,  # a D-number, when the owner resolves it
            }

        target = Path(dest_dir) / logical_name
        if prior_sha256 and prior_sha256 != digest:
            # SEC-A-02: record the divergence — both filenames incl. version
            # suffixes, both hashes — and REFUSE to overwrite. The on-disk bytes and
            # the top-level sha256 stay the recorded ones.
            record["status"] = "divergent-not-overwritten"
            record["sha256"] = prior_sha256
            record["provider_filename"] = prior_filename or result.provider_filename
            record["divergence"] = {
                "recorded_provider_filename": prior_filename,
                "recorded_sha256": prior_sha256,
                "retrieved_provider_filename": result.provider_filename,
                "retrieved_sha256": digest,
            }
            return guard_egress(record, context=f"provider_file_record[{logical_name}]")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(buffer)
        record["status"] = "complete"
        record["sha256"] = digest
        return guard_egress(record, context=f"provider_file_record[{logical_name}]")


# =======================================================================================
# W-3 / W-4 / W-7: provenance, hashing, gaps
# =======================================================================================

#: `ProvenanceClass` (domain-entities 4): `full` marks a month acquired under this
#: contract where the W-4 arithmetic holds; `derived_only` marks one of the twelve
#: pre-TC-06 months whose manifests hash derived artifacts and no provider bytes
#: (DATA-07: provenance unverifiable in principle for those months).
PROVENANCE_CLASSES: Final[frozenset[str]] = frozenset({"full", "derived_only"})

#: TE 5.1's NINE driver-inventory fields (R-40) — all nine, not three. `release_status`
#: is the "version or release status" slot given asserted meaning; the reanalysed-value
#: check reads it together with `provider_product_identity`, `retrieval_date` and
#: `checksum`.
DRIVER_INVENTORY_FIELDS: Final[tuple[str, ...]] = (
    "provider",
    "role",
    "provider_product_identity",
    "coverage",
    "retrieval_date",
    "checksum",
    "release_status",
    "licence_access_notes",
    "consuming_configuration",
)

#: The locked test month (D-8's claim boundary; D-15's restricted relocation; BLK-07).
#: A governance boundary IDENTITY, not a scientific constant: fixed by decision
#: record, cited here so record-date membership (R-31) has one home. Never derived
#: from a directory or file name.
LOCKED_YEAR: Final[int] = 2022
LOCKED_MONTH: Final[int] = 12

#: TE 13's three definition IDs, stamped on every dataset, prediction, mask and
#: comparison (project.md § Mandated, board finding TEC-05; R-70). Named ONCE here, the
#: lowest module in the package, so `acquisition`'s manifests, `inventory`'s audit
#: reports and `prepared`'s row stamps read one vocabulary rather than three copies.
TEC05_STAMP_FIELDS: Final[tuple[str, ...]] = (
    "phase_id",
    "source_id",
    "target_definition_id",
)

_NAN: Final[float] = float("nan")

#: A bare calendar date carries no offset and therefore no local/UTC ambiguity; anything
#: longer must state an explicit zero UTC offset before a date can be read off it (R-46).
_DATE_ONLY: Final[re.Pattern[str]] = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def assert_identity_stamped(
    identity: Mapping[str, object], *, resource: str
) -> dict[str, str]:
    """TEC-05 / R-70: all three definition IDs present and non-empty, or REFUSE.

    The provenance head of the chain (`request_manifest.json`, `sha256_manifest.json`,
    the fixture read manifest, the source inventory and the two December-audit reports)
    carried no stamp at all until 2026-09-20, while stage 02 onward stamped thoroughly
    — so an artifact could reach a gate with no phase, source or target-definition
    identity on it. This is the one refusal both ends share; the empty-stamp shape
    matches `prepared.assert_*`'s existing pattern rather than inventing a second one.

    Returns the three values as a plain `dict[str, str]`, so a caller never has to
    re-read the mapping it just handed in.

    Raises
    ------
    AcquisitionError
        naming the resource and EVERY absent or empty stamp — an artifact that names one
        of the three is no more traceable than one that names none, so all three are
        reported together rather than one raise at a time.
    """
    missing = [
        field
        for field in TEC05_STAMP_FIELDS
        if not str(identity.get(field, "") or "").strip()
    ]
    if missing:
        raise AcquisitionError(
            resource,
            "TE 13 identity stamp(s) absent or empty: "
            + ", ".join(missing)
            + " — every dataset, prediction, mask and comparison carries phase_id, "
            "source_id and target_definition_id (project.md § Mandated, board finding "
            "TEC-05; R-70), and the values are RESOLVED from configuration, never "
            "invented by an implementer (TE 18.2/18.3)",
        )
    return {field: str(identity[field]).strip() for field in TEC05_STAMP_FIELDS}


def parse_record_date_utc(raw: object) -> _dt.date:
    """R-31/R-46: the ONE derivation of a record's observation date, in UTC.

    Until 2026-09-20 both record-date readers in this package sliced `raw[:10]`, which
    attributes a timestamp to its LOCAL date. Every record observed to date carries
    `+00:00`, so the defect was latent — but this derivation decides LOCKED-MONTH
    membership, and `2022-11-30T23:30:00-05:00` is `2022-12-01T04:30:00Z`: a December
    record that a slice files under November and walks past the BLK-07 bar. The
    re-acquisition (DATA-07) is being written against this function, so the latent form
    is fixed before it can be reached.

    Accepted, in order:

    * a bare `YYYY-MM-DD` calendar date — no offset exists to misread, and this is the
      shape the month files' `date` column carries;
    * an ISO-8601 timestamp bearing an EXPLICIT zero UTC offset (`+00:00` or `Z`,
      space- or `T`-separated), whose `.date()` is then the UTC date.

    Refused: a naive timestamp (no offset — unattributable, never assumed to be UTC) and
    a non-zero offset (its local date is not its UTC date, and guessing which the writer
    meant is the failure mode this function exists to close). Refusal rather than silent
    conversion is the fail-closed posture the rest of this module holds; a caller that
    genuinely has offset-bearing data converts it upstream and records that it did.

    Raises
    ------
    ValueError
        carrying the reason as its message. Deliberately the stdlib exception rather
        than an `IntegrityError` subclass: `acquisition` and `inventory` each raise
        their OWN integrity type around this ONE parser, so the derivation has a single
        home (nfr-design c58) without either module inheriting the other's exception.
    """
    text = str(raw if raw is not None else "").strip()
    if not text:
        raise ValueError("record timestamp is missing or empty")
    if _DATE_ONLY.match(text):
        return _dt.date.fromisoformat(text)
    try:
        parsed = _dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(
            f"record timestamp {text!r} is neither a YYYY-MM-DD calendar date nor a "
            f"parseable ISO-8601 timestamp"
        ) from None
    if parsed.tzinfo is None:
        raise ValueError(
            f"record timestamp {text!r} carries no UTC offset; a naive timestamp cannot "
            f"be attributed to a UTC date and is never ASSUMED to be UTC (R-46)"
        )
    offset = parsed.utcoffset()
    if offset != _dt.timedelta(0):
        raise ValueError(
            f"record timestamp {text!r} carries a non-zero UTC offset ({offset}); its "
            f"local date is not its UTC date, and attributing it to the local one is how "
            f"a December observation gets filed under November (R-46) — convert to "
            f"explicit UTC upstream and record that the conversion happened"
        )
    return parsed.date()


def _is_gap(value: object) -> bool:
    if value is None:
        return True
    return isinstance(value, float) and value != value  # NaN


def store_gaps_as_nan(values: Iterable[object]) -> list[object]:
    """D-5 / D-10.2: gaps become explicit NaN; nothing is interpolated, smoothed or filled.

    `None` (a missing retrieval) becomes `float("nan")`; every present value is
    passed through UNTOUCHED — this function performs storage normalisation only and
    applies no scientific transformation (R-30).
    """
    return [_NAN if value is None else value for value in values]


def count_gaps(values: Iterable[object]) -> int:
    """Count of missing values (None or NaN) in a series."""
    return sum(1 for value in values if _is_gap(value))


def gap_accounting_entry(
    series: str, *, gaps_at_retrieval: int, gaps_in_artifact: int
) -> dict[str, object]:
    """One `GapAccounting` manifest entry (domain-entities 5), conservation asserted.

    The invariant IS the rule's carrier (R-37): a fill of any kind — named, aliased
    or vectorised — changes `gaps_in_artifact`, so the equality catches it on
    branches no fixture exercises and no static scan can name. The entry is a
    manifest field because FR-P1-01-9 has no acceptance row: a manifest field is
    evidence that survives the absence of a gate.
    """
    entry = {
        "series": series,
        "gaps_at_retrieval": gaps_at_retrieval,
        "gaps_in_artifact": gaps_in_artifact,
    }
    assert_gap_conservation(entry)
    return entry


def assert_gap_conservation(entry: Mapping[str, object]) -> None:
    """R-37's conservation limb: `gaps_at_retrieval == gaps_in_artifact`, or terminate.

    Raises
    ------
    AcquisitionError
        naming the series and both counts. A lower artifact count means a fill
        happened somewhere; a higher one means values were lost. Neither is a
        completeness shortfall — both are integrity violations.
    """
    series = str(entry.get("series", "<unnamed series>"))
    at_retrieval = entry.get("gaps_at_retrieval")
    in_artifact = entry.get("gaps_in_artifact")
    if at_retrieval != in_artifact:
        raise AcquisitionError(
            series,
            f"NaN-count conservation violated: gaps_at_retrieval={at_retrieval!r} but "
            f"gaps_in_artifact={in_artifact!r}; gaps are stored as explicit NaN at "
            f"acquisition and no interpolation, smoothing or fill occurs (D-5, "
            f"D-10.2, R-37) — a changed count is a fill or a loss, never rounding",
        )


def assert_madrigalweb_version(identity: Mapping[str, object]) -> None:
    """R-35 check 1: a non-empty `madrigalWeb_version`, absent failing AS `"unknown"` fails.

    One raise site for both defects, so the two failure modes are literally
    identical — the requirement's wording ("an absent key fails exactly as 'unknown'
    fails") is satisfied by construction rather than by two matched messages.

    Raises
    ------
    AcquisitionError
        when the key is absent, empty, or the literal `"unknown"`.
    """
    value = str(identity.get("madrigalWeb_version", "") or "").strip()
    if not value or value.lower() == "unknown":
        raise AcquisitionError(
            "request_manifest.json",
            "madrigalWeb_version must be present and non-empty; an absent key fails "
            "exactly as 'unknown' fails (FR-P1-01-3, R-35 — a single string test was "
            "satisfiable by omission, and the FULL manifest in the workspace is the "
            "live instance of that omission)",
        )


def assert_single_release_grade(series: str, rows: Sequence[Mapping[str, object]]) -> None:
    """R-40 / REQ-NFR-A1: exactly ONE release grade per series for calendar 2022.

    Kyoto Dst release grades (real-time, provisional, final) are never mixed within
    one series, and no value is backfilled from a future final or definitive archive
    — a mixed grade is the observable form of that backfill this check can catch.

    Raises
    ------
    AcquisitionError
        when a row's `release_status` is missing/empty, or more than one distinct
        grade appears within the series.
    """
    grades: set[str] = set()
    for index, row in enumerate(rows):
        grade = str(row.get("release_status", "") or "").strip()
        if not grade:
            raise AcquisitionError(
                series,
                f"row {index} carries no release_status; every driver row records its "
                f"release grade, not only its lag (R-40, project.md Forbidden: never "
                f"backfill from future final values; record the release status of "
                f"every driver)",
            )
        grades.add(grade)
    if len(grades) > 1:
        raise AcquisitionError(
            series,
            f"mixed release grades within one series: {sorted(grades)}; grades are "
            f"never mixed within a series and the 2022 grade is recorded before use "
            f"(D-10.1, R-40, REQ-NFR-A1)",
        )


def assert_driver_inventory(inventory: Sequence[Mapping[str, object]]) -> None:
    """R-40: every driver series carries ALL NINE of TE 5.1's inventory fields.

    Raises
    ------
    AcquisitionError
        naming the series and every missing or empty field. A series carrying fewer
        than nine fails.
    """
    for entry in inventory:
        series = str(entry.get("series", "<unnamed series>"))
        missing = [
            field
            for field in DRIVER_INVENTORY_FIELDS
            if not str(entry.get(field, "") or "").strip()
        ]
        if missing:
            raise AcquisitionError(
                series,
                "driver inventory is missing TE 5.1 field(s): "
                + ", ".join(missing)
                + " — all nine fields are required, not three (R-40)",
            )


def _write_json(path: Path, payload: Mapping[str, Any]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def write_request_manifest(
    path: Path,
    *,
    identity: Mapping[str, Any],
    stamps: Mapping[str, Any],
    provider_files: Sequence[Mapping[str, Any]],
    driver_inventory: Sequence[Mapping[str, Any]] = (),
    gap_accounting: Sequence[Mapping[str, Any]] = (),
    provenance_class: str,
    producing_interpreter: str,
    missing_months: Sequence[str] = (),
) -> Path:
    """Write `request_manifest.json` (W-3, domain-entities 2). Every value guarded.

    Validations, in order: `madrigalWeb_version` present and non-empty (R-35); the three
    TE 13 identity stamps present and non-empty (R-70/TEC-05); `provenance_class` in the
    closed set (R-36); all nine TE 5.1 fields per driver series plus a single recorded
    grade (R-40); the NaN-count conservation invariant per gap-accounting entry (R-37);
    then the WHOLE payload through the W-9 redaction chokepoint — nothing is written when
    any check fails.

    `stamps` carries `phase_id`, `source_id` and `target_definition_id`, RESOLVED from
    configuration by the calling stage script and never invented here (R-30, R-70). It is
    required rather than defaulted: a default would let the provenance head of the chain
    go on emitting unstamped artifacts, which is the defect this parameter closes
    (board finding TEC-05, 2026-09-20).

    `gap_accounting` is the W-7 NaN-conservation evidence, one entry per series. It
    defaults to empty for a run that retrieved no series at all; a run that DID retrieve
    one and passes nothing leaves the conservation loop below iterating zero entries,
    which is a silently unenforced invariant rather than a satisfied one — the calling
    script composes an entry per series through `gap_accounting_entry`.

    `missing_months` is the machine-readable completeness-shortfall field
    (`team.md` § Code Style): a missing month is recorded here, never console text
    only, and is non-fatal — the `audit_ec1_drivers.py:184` gap is not reproduced.
    The retrieval policy is embedded so a retrieval's behaviour is reconstructible
    (SD-A-01).
    """
    assert_madrigalweb_version(identity)
    stamped = assert_identity_stamped(stamps, resource=str(path))
    if provenance_class not in PROVENANCE_CLASSES:
        raise AcquisitionError(
            str(path),
            f"provenance_class {provenance_class!r} is not one of "
            f"{sorted(PROVENANCE_CLASSES)}; the field is what keeps the manifest "
            f"format legible across pre- and post-TC-06 months (R-36, Q5=C)",
        )
    if not str(producing_interpreter).strip():
        raise AcquisitionError(
            str(path),
            "producing_interpreter must be recorded: the 2026-08-16 extracts were "
            "produced under Python 3.14, outside the governed 3.11 pin, and without "
            "the field a passing hash reads as evidence the envelope held (R-36)",
        )
    assert_driver_inventory(driver_inventory)
    by_series: dict[str, list[Mapping[str, Any]]] = {}
    for entry in driver_inventory:
        by_series.setdefault(str(entry.get("series", "<unnamed series>")), []).append(entry)
    for series, rows in by_series.items():
        assert_single_release_grade(series, rows)
    for entry in gap_accounting:
        assert_gap_conservation(entry)

    payload: dict[str, Any] = {
        "identity": dict(identity),
        "provider_files": [dict(rec) for rec in provider_files],
        "driver_inventory": [dict(entry) for entry in driver_inventory],
        "gap_accounting": [dict(entry) for entry in gap_accounting],
        "provenance_class": provenance_class,
        "producing_interpreter": producing_interpreter,
        "missing_months": list(missing_months),
        "retrieval_policy": retrieval_policy(),
        **stamped,
    }
    guard_egress(payload, context=f"request_manifest[{Path(path).name}]")
    return _write_json(Path(path), payload)


SHA256_MANIFEST_META_NAME = "sha256_manifest_meta.json"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def write_sha256_manifest(
    path: Path,
    *,
    provider_files: Sequence[Mapping[str, Any]],
    derived_artifacts: Mapping[str, str],
    provenance_class: str,
    producing_interpreter: str,
    stamps: Mapping[str, Any],
) -> Path:
    """Write `sha256_manifest.json` (W-4): one entry per provider file PLUS one per derived
    artifact, in the CANONICAL TE §13.3 representation — a flat `{relative path: sha256}`
    mapping, exactly the shape the twelve pre-TC-06 monthly manifests carry, that
    `src/data/release.py:write_release` emits as `output_files`, and that TA-15's reader
    (`tests/test_release_hashes.py`) verifies. Provider METADATA — the full provider
    filename with its version suffix per file, the provenance class, the producing
    interpreter and W-4's hash-count arithmetic — is written beside it to
    `sha256_manifest_meta.json`, never mixed into the hash mapping (G-1, 2026-09-19,
    `CR-2026-09-19-GATE-PREP-2`; the earlier nested payload failed the governed reader
    on its own metadata keys, observed on the GFZ driver-pair audit).

    Provider entries are keyed by the file's ON-DISK name (`logical_name`, falling back
    to `provider_filename` when no logical name was recorded), so the mapping resolves
    against the directory it sits in.

    `stamps` (`phase_id`, `source_id`, `target_definition_id`, R-70/TEC-05) rides on the
    METADATA sidecar and NEVER on the hash mapping: the mapping is the canonical TE 13.3
    `{relative path: sha256}` document the governed reader parses, and the earlier nested
    payload failed that reader on its own metadata keys (G-1, 2026-09-19). Stamping the
    sidecar is what keeps the artifact traceable without reopening that defect.

    Refusals (all `AcquisitionError`, naming the file and the expectation): a provider
    record without a `sha256` (incomplete or divergent retrieval — admitting it would make
    the month's hash count silently omit a provider file, FR-P1-01-4's negative control);
    an unknown provenance class; an empty `producing_interpreter`; a `full` month with no
    provider entries (the twelve pre-TC-06 months are `derived_only` and say so, R-36,
    Q5=C); a digest that is not 64 lower-case hex characters; an AMBIGUOUS mapping (two
    records or a record and a derived artifact resolving to one path).
    """
    if provenance_class not in PROVENANCE_CLASSES:
        raise AcquisitionError(
            str(path),
            f"provenance_class {provenance_class!r} is not one of "
            f"{sorted(PROVENANCE_CLASSES)} (R-36)",
        )
    if not str(producing_interpreter).strip():
        raise AcquisitionError(str(path), "producing_interpreter must be recorded (R-36)")
    stamped = assert_identity_stamped(stamps, resource=str(path))

    mapping: dict[str, str] = {}
    provider_identity: dict[str, str] = {}
    for record in provider_files:
        name = str(record.get("logical_name", "") or record.get("provider_filename", ""))
        digest = str(record.get("sha256", "") or "")
        if not digest:
            raise AcquisitionError(
                name or str(path),
                "provider file record carries no sha256 (incomplete or divergent "
                "retrieval); admitting it would make the month's manifest hash count "
                "omit a provider file — each month's hash count equals its "
                "provider-file count plus its derived-artifact count (FR-P1-01-4, "
                "R-36), and a partial file is never promoted (SD-A-01)",
            )
        if not name.strip():
            raise AcquisitionError(str(path), "provider file record carries no on-disk name")
        if not _HEX64.match(digest):
            raise AcquisitionError(name, f"sha256 {digest!r} is not 64 lower-case hex characters")
        if name in mapping:
            raise AcquisitionError(
                name, "AMBIGUOUS manifest mapping: two provider records resolve to one path"
            )
        mapping[name] = digest
        provider_identity[name] = str(record.get("provider_filename", "") or name)
    if provenance_class == "full" and not provider_identity:
        raise AcquisitionError(
            str(path),
            "a 'full'-provenance month with zero provider-file hashes contradicts "
            "its own class; the twelve pre-TC-06 months are 'derived_only' and say "
            "so (R-36, Q5=C)",
        )
    for name, digest in derived_artifacts.items():
        name = str(name)
        digest = str(digest)
        if not _HEX64.match(digest):
            raise AcquisitionError(name, f"sha256 {digest!r} is not 64 lower-case hex characters")
        if name in mapping:
            raise AcquisitionError(
                name,
                "AMBIGUOUS manifest mapping: a derived artifact collides with a provider file",
            )
        mapping[name] = digest

    meta: dict[str, Any] = {
        "schema": "TE-13.3 path-to-sha256; metadata sidecar v1",
        "manifest": Path(path).name,
        "hash_count": len(mapping),
        "provider_file_count": len(provider_identity),
        "derived_artifact_count": len(derived_artifacts),
        "provider_files": provider_identity,
        "provenance_class": provenance_class,
        "producing_interpreter": producing_interpreter,
        **stamped,
    }
    guard_egress(mapping, context=f"sha256_manifest[{Path(path).name}]")
    guard_egress(meta, context=f"sha256_manifest_meta[{Path(path).name}]")
    _write_json(Path(path).with_name(SHA256_MANIFEST_META_NAME), meta)
    return _write_json(Path(path), mapping)


def assert_release_free_of_unresolved_mismatch(
    provider_files: Sequence[Mapping[str, Any]],
) -> None:
    """R-34 step 3: the release-side refusal of an UNRESOLVED version-suffix mismatch.

    Boundary split, stated (project.md, nfr-design c58): `foundation`'s
    `write_release` owns the TE 13.3 field contract; THIS function is the acquisition
    guard the release path calls over its source `provider_files` before composing
    `source_files` — the suffix-mismatch field is not among FR-P1-04-11's fourteen
    release fields (Open item for stage 3.2), so the refusal lives with the unit that
    writes the field it reads, and editing `write_release` is an amendment owed, not
    made here.

    A mismatch is RESOLVED by a `resolved_by` D-number recorded on the mismatch —
    the same decision-record currency every other governed disagreement resolves to.

    Raises
    ------
    ReleaseError
        naming each file whose `suffix_mismatch` carries no `resolved_by` D-number.
        Retrieving a reissued file is fine; releasing it as though it were the
        recorded one is not (R-34).
    """
    offenders: list[str] = []
    for record in provider_files:
        mismatch = record.get("suffix_mismatch")
        if isinstance(mismatch, Mapping) and not str(mismatch.get("resolved_by", "") or ""):
            offenders.append(
                str(record.get("provider_filename", "") or record.get("logical_name", "?"))
            )
        divergence = record.get("divergence")
        if isinstance(divergence, Mapping) and not str(divergence.get("resolved_by", "") or ""):
            offenders.append(
                str(record.get("provider_filename", "") or record.get("logical_name", "?"))
                + " (hash divergence)"
            )
    if offenders:
        raise ReleaseError(
            ", ".join(sorted(set(offenders))),
            "release refused: unresolved version-suffix mismatch or hash divergence "
            "on the source files; a mismatch is recorded at retrieval (non-fatal) "
            "and refused at release until a resolved_by D-number covers it "
            "(FR-P1-01-2, R-34: surfaced, never silently accepted)",
        )


def assert_derived_release_provenance(
    release_source_digests: Mapping[str, str],
    current_month_digests: Mapping[str, str],
    *,
    repointing_decision: str | None = None,
) -> None:
    """R-42: a derived release re-merges from current months, or is re-pointed by D-number.

    Compares the digests a derived multi-month release recorded for its source months
    against the CURRENT per-month manifest digests. Any difference means a source
    month was regenerated after the merge; the release then fails rather than being
    relied on, unless an explicit `repointing_decision` D-number covers it (the
    D-18 pattern: re-merge is the first branch, a recorded re-point the second).

    Raises
    ------
    ReleaseError
        naming every stale month, when digests differ and no D-number is supplied.
    """
    stale = sorted(
        month
        for month, digest in release_source_digests.items()
        if current_month_digests.get(month, "") != digest
    )
    if stale and not (repointing_decision or "").strip():
        raise ReleaseError(
            ", ".join(stale),
            "derived release provenance is stale: source-month digest(s) no longer "
            "match the current per-month manifests, and no D-number re-points the "
            "provenance; either re-merge from the current months or record the "
            "re-pointing decision (FR-P1-01-11, R-42; D-18 is the first branch's "
            "precedent)",
        )


# =======================================================================================
# R-31 / BLK-07: locked-month membership from record timestamps, never names
# =======================================================================================


def _record_date(record: Mapping[str, Any], timestamp_key: str) -> _dt.date:
    """The ONE reader of a record's observation date (R-31): shared by the locked-month
    predicate and by the window predicate below, so no second copy of the rule exists.

    Attribution is UTC, via `parse_record_date_utc` (R-46, 2026-09-20): the former
    `raw[:10]` slice attributed an offset-bearing timestamp to its LOCAL date, which on
    a month boundary files a December observation under November and walks it past the
    BLK-07 bar. `inventory._record_date` wraps the SAME parser with its own exception
    type, so the rule has one derivation and two integrity tiers.
    """
    raw = str(record.get(timestamp_key, "") or "")
    try:
        return parse_record_date_utc(raw)
    except ValueError as exc:
        raise AcquisitionError(
            raw or f"<record with no {timestamp_key}>",
            f"record timestamp {timestamp_key!r} cannot establish a UTC observation "
            f"date ({exc}); membership derives from RECORD TIMESTAMPS, never from a "
            f"directory or file name (R-31, project.md Forbidden), and a record whose "
            f"date cannot be established cannot be cleared — fail closed, never guess",
        ) from None


def _record_year_month(record: Mapping[str, Any], timestamp_key: str) -> tuple[int, int]:
    stamp = _record_date(record, timestamp_key)
    return stamp.year, stamp.month


def partition_by_locked_month(
    records: Sequence[Mapping[str, Any]], *, timestamp_key: str = "timestamp"
) -> tuple[list[Mapping[str, Any]], list[Mapping[str, Any]]]:
    """Split records into (kept, locked_month) on RECORD TIMESTAMPS alone (R-31).

    The directory a record was filed under plays NO role: a year-blind predicate
    once filed locked-month records into `audit_evidence_2022-01/`, which is why
    this is asserted on record dates rather than on the folder a file sat in
    (board finding ML-07, TEC-09). A record with a missing or unparseable timestamp
    is an integrity failure, never silently kept.
    """
    kept: list[Mapping[str, Any]] = []
    locked: list[Mapping[str, Any]] = []
    for record in records:
        year, month = _record_year_month(record, timestamp_key)
        if (year, month) == (LOCKED_YEAR, LOCKED_MONTH):
            locked.append(record)
        else:
            kept.append(record)
    return kept, locked


def assert_no_locked_month_records(
    records: Sequence[Mapping[str, Any]], *, timestamp_key: str = "timestamp"
) -> None:
    """BLK-07's acquisition-side bar: no December 2022 record enters this run's outputs.

    Raises
    ------
    AcquisitionError
        naming the count of locked-month records, when any record's TIMESTAMP falls
        in December 2022. No acquisition run may touch calendar 2022-12 while BLK-07
        stands; the authorization limb is the project decision owner's and nothing
        here substitutes for it.
    """
    _, locked = partition_by_locked_month(records, timestamp_key=timestamp_key)
    if locked:
        raise AcquisitionError(
            f"{len(locked)} record(s)",
            f"record timestamp(s) fall in {LOCKED_YEAR}-{LOCKED_MONTH:02d}, the "
            f"locked test month; no acquisition run may touch calendar 2022-12 "
            f"while BLK-07 stands (unit-of-work.md § 3; the authorization limb is "
            f"the project decision owner's)",
        )


def assert_records_within_window(
    records: Sequence[Mapping[str, Any]],
    *,
    start: _dt.date,
    end: _dt.date,
    timestamp_key: str = "timestamp",
) -> int:
    """R-31's window form: every record's OBSERVATION DATE lies in `[start, end]`, inclusive.

    Added additively for `fixtures-and-reproducibility` (Q4/Q5 sibling-edit precedent,
    `governance/CHANGE_RECORD_2026-09-07_R133_fixtures_and_reproducibility.md` § 5):
    the fixture orchestrator asserts every input record against the manifest's CITED window
    with this predicate and the December exclusion with `assert_no_locked_month_records`, so
    the record-date rule has ONE reader (`_record_date`) and no third copy. The directory a
    record was filed under plays no role (TEC-09; ML-07). Returns the record count checked.

    Raises
    ------
    AcquisitionError
        naming the first out-of-window record's date and the window; or a record whose date
        cannot be established (fail closed, never guess).
    """
    if start > end:
        raise AcquisitionError(
            f"window {start.isoformat()}..{end.isoformat()}", "start is after end"
        )
    for index, record in enumerate(records):
        stamp = _record_date(record, timestamp_key)
        if not (start <= stamp <= end):
            raise AcquisitionError(
                f"record {index} ({stamp.isoformat()})",
                f"observation date lies outside the window {start.isoformat()}.."
                f"{end.isoformat()} inclusive; membership is asserted on RECORD dates, "
                f"never on the folder a file was filed under (R-31; FR-WS-3)",
            )
    return len(records)


def select_records_within_window(
    records: Sequence[Mapping[str, Any]],
    *,
    start: _dt.date,
    end: _dt.date,
    timestamp_key: str = "timestamp",
) -> list[Mapping[str, Any]]:
    """R-31's window form as a SELECTION: the records whose OBSERVATION DATE lies in
    `[start, end]`, inclusive, read through the ONE record-date reader (`_record_date`).

    Added additively for `fixtures-and-reproducibility` on the same sibling-edit precedent
    as `assert_records_within_window` (CR-2026-09-20-B01-PREREQS §2): a fixture's cited
    window is a sub-range of the month file it reads (D-11's seven days inside the
    November file; the month files also carry provider edge records dated in the adjacent
    month), so the orchestrator SELECTS the in-window records on record dates and only then
    ASSERTS the assembled set with the predicate above — the Option-B reads-narrowing
    already ruled for 00/01/02/04 (CR-2026-09-13), applied to the orchestrator's own
    assembly. The directory a record was filed under plays no role (TEC-09; ML-07). A record
    whose date cannot be established fails closed inside `_record_date`, never silently
    dropped.

    Raises
    ------
    AcquisitionError
        `start` after `end`; a record whose date cannot be established.
    """
    if start > end:
        raise AcquisitionError(
            f"window {start.isoformat()}..{end.isoformat()}", "start is after end"
        )
    return [r for r in records if start <= _record_date(r, timestamp_key) <= end]


# =======================================================================================
# Fixture-run input: the month's declared derived artifacts, verified at use
# =======================================================================================
# Moved here from scripts/run_walking_skeleton.py under freeze-package item 1, option (a)
# (CR-2026-09-20-B01-PREREQS 2.5; owner ruling 2026-09-20), so the orchestrator and a
# fixture-scoped stage 00 share ONE verification home instead of two copies.


def _month_manifest_entries(payload: Mapping[str, Any]) -> Mapping[str, str]:
    """Accept the flat `{name: sha256}` shape the existing evidence carries, or acquisition's
    `{"derived_artifacts": {...}}` shape."""
    if isinstance(payload.get("derived_artifacts"), Mapping):
        return {str(k): str(v) for k, v in payload["derived_artifacts"].items()}
    return {str(k): str(v) for k, v in payload.items() if isinstance(v, str)}


def verify_declared_inputs(scope: Any, *, workspace: Path) -> dict[str, Any]:
    """R-135 control 12 / limb 2: every declared derived artifact (`inputs.prepared_vtec` of
    a fixture scope) verifies against the month's `sha256_manifest.json` AND against its
    bytes on disk, BEFORE anything reads it. `scope` is a loaded fixture manifest or identity
    declaration (it exposes `.data` and `.path`)."""
    inputs = scope.data.get("inputs")
    declared = inputs.get("prepared_vtec") if isinstance(inputs, Mapping) else None
    if not isinstance(declared, Mapping):
        raise IntegrityError(
            scope.path,
            "inputs.prepared_vtec is required: the month's declared derived artifacts with their "
            "SHA-256 are the eligibility evidence re-verified at use (team.md; R-135 limb 2)",
        )
    evidence_dir = Path(workspace) / str(declared.get("evidence_dir", ""))
    month_manifest = evidence_dir / str(declared.get("sha256_manifest", "sha256_manifest.json"))
    if not month_manifest.is_file():
        raise IntegrityError(
            month_manifest,
            "the month's sha256_manifest.json is absent; eligibility is judged on derived-"
            "artifact verification and cannot be assumed from the selection record",
        )
    try:
        entries = _month_manifest_entries(json.loads(month_manifest.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(month_manifest, f"unreadable ({exc})") from exc
    files = declared.get("files")
    if not isinstance(files, Mapping) or not files:
        raise IntegrityError(scope.path, "inputs.prepared_vtec.files must map artifact -> sha256")
    verified: dict[str, str] = {}
    for name, declared_hash in files.items():
        recorded = entries.get(str(name))
        if recorded is None:
            raise IntegrityError(
                month_manifest, f"declared artifact {name!r} is not hash-listed by the month"
            )
        if str(declared_hash).lower() != recorded.lower():
            raise IntegrityError(
                evidence_dir / str(name),
                f"declared SHA-256 {declared_hash} disagrees with the month's recorded {recorded} "
                f"(R-135 control 12)",
            )
        artifact = evidence_dir / str(name)
        if not artifact.is_file():
            raise IntegrityError(artifact, "declared derived artifact is absent from the evidence")
        actual = sha256_of_file(artifact)
        if actual != recorded.lower():
            raise IntegrityError(
                artifact,
                f"bytes hash to {actual} but the month's sha256_manifest.json records {recorded}; "
                f"the eligibility check re-executed at use FAILS before the fixture runs "
                f"(R-135 control 12; team.md, CHAIR-02)",
            )
        verified[str(name)] = actual
    records_file = str(declared.get("records_file", ""))
    if records_file not in verified:
        raise IntegrityError(
            scope.path,
            f"inputs.prepared_vtec.records_file {records_file!r} is not one of the verified "
            f"declared artifacts {sorted(verified)}",
        )
    return {
        "evidence_dir": str(evidence_dir),
        "sha256_manifest": str(month_manifest),
        "verified": verified,
        "records_file": records_file,
    }


def cited_stations(scope: Any) -> list[str]:
    """The station(s) a fixture scope cites: a single-station `station_citation.station_id`
    (the plumbing fixture, TC-03f) or the all-station `identity.stations` list."""
    identity = scope.identity
    citation = identity.get("station_citation")
    if isinstance(citation, Mapping):
        return [str(citation["station_id"])]
    return [str(st) for st in identity["stations"]]


def select_station_records(
    rows: Sequence[Mapping[str, Any]], stations: Sequence[str], *, station_key: str = "station"
) -> list[Mapping[str, Any]]:
    """Select the cited stations' records -- SELECTION, before the assembled input is asserted."""
    wanted = {str(st) for st in stations}
    return [row for row in rows if str(row.get(station_key, "")) in wanted]


def read_records_csv(path: Path) -> list[dict[str, str]]:
    """The month's raw-records CSV as row dicts (every value a string; no parsing here)."""
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


FIXTURE_READ_MANIFEST_NAME: Final[str] = "fixture_read_manifest.json"


def write_fixture_read_manifest(
    path: Path,
    *,
    identity: Mapping[str, Any],
    stamps: Mapping[str, Any],
    fixture_inputs: Mapping[str, Any],
    month_request_manifest: Path | None,
    producing_interpreter: str,
) -> Path:
    """Write `fixture_read_manifest.json`: what a fixture-scoped stage 00 READ.

    This is NOT a `request_manifest.json`: nothing was requested from a provider, so R-35's
    `madrigalWeb_version` check (a retrieval fact) does not apply and is not imitated. The
    month's own recorded `madrigalWeb_version` is copied VERBATIM from its request manifest
    when one exists (for the pre-TC-06 months that is the literal `"unknown"`, which is the
    recorded state and is never replaced by a plausible value). Every value passes the W-9
    redaction chokepoint.

    `stamps` carries the three TE 13 definition IDs (R-70/TEC-05). A fixture scope already
    declares them as required identity fields, so this writer RESOLVES them from the scope
    through its caller and invents nothing. Named in board finding TEC-05 alongside the
    request and sha256 manifests as a provenance-head artifact carrying no stamp.

    Raises
    ------
    AcquisitionError
        an empty `producing_interpreter`; an absent or empty identity stamp; a
        redaction-chokepoint refusal.
    """
    if not str(producing_interpreter).strip():
        raise AcquisitionError(str(path), "producing_interpreter must be recorded (R-36)")
    stamped = assert_identity_stamped(stamps, resource=str(path))
    recorded_version: str | None = None
    if month_request_manifest is not None and Path(month_request_manifest).is_file():
        try:
            recorded = json.loads(Path(month_request_manifest).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AcquisitionError(str(month_request_manifest), f"unreadable ({exc})") from exc
        value = recorded.get("madrigalWeb_version") if isinstance(recorded, Mapping) else None
        recorded_version = None if value is None else str(value)
    payload: dict[str, Any] = {
        "kind": "fixture_read_manifest",
        "identity": dict(identity),
        "retrieval_performed": False,
        "provenance_class": "derived_only",
        "fixture_inputs": dict(fixture_inputs),
        "month_recorded_madrigalWeb_version": recorded_version,
        "producing_interpreter": producing_interpreter,
        **stamped,
    }
    guard_egress(payload, context=f"fixture_read_manifest[{Path(path).name}]")
    return _write_json(Path(path), payload)


# =======================================================================================
# W-9 limb 2 / Q3 = A: the notebook saved-output check the pre-commit hook calls
# =======================================================================================


def notebook_output_violations(notebook: Mapping[str, Any]) -> list[str]:
    """Every code cell carrying saved outputs or an execution count, named per cell.

    The pre-commit hook fails CLOSED on any violation: the author clears outputs and
    re-commits, and nothing is auto-stripped — a silent rewrite of staged content
    defeats the D-number citation rule, and a credential in committed history needs
    a history rewrite that would rewrite freeze-gate tags (SD-A-02, Q3 = A).
    """
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        raise AcquisitionError(
            "<notebook>",
            "notebook JSON carries no 'cells' list; an unparseable or malformed "
            "notebook cannot be cleared and the check fails closed (R-27's posture)",
        )
    violations: list[str] = []
    for index, cell in enumerate(cells):
        if not isinstance(cell, Mapping) or cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs")
        if outputs:
            violations.append(f"cell[{index}]: {len(outputs)} saved output(s)")
        execution_count = cell.get("execution_count")
        if execution_count is not None:
            violations.append(f"cell[{index}]: execution_count={execution_count}")
    return violations


def notebook_output_violations_from_text(text: str, *, name: str) -> list[str]:
    """Parse notebook JSON text and delegate; unparseable input FAILS CLOSED.

    Raises
    ------
    AcquisitionError
        when the text is not valid notebook JSON — a notebook the check cannot parse
        cannot be cleared for commit.
    """
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AcquisitionError(
            name,
            f"staged notebook is not parseable JSON ({exc}); an unparseable notebook "
            f"cannot be cleared and the commit is blocked (fail closed, Q3=A)",
        ) from exc
    if not isinstance(loaded, Mapping):
        raise AcquisitionError(name, "staged notebook JSON is not an object; fail closed")
    return notebook_output_violations(loaded)


def _cli(argv: Sequence[str]) -> int:
    """Hook entry point: `python -m src.data.acquisition check-notebook-outputs --name X`.

    Reads the STAGED notebook JSON from stdin (the hook pipes `git show :path`), so
    the check covers what is being committed rather than the working tree. Exit 0 on
    clean; exit 1 on violations or unparseable input, printing each violation to
    stderr. Never rewrites anything.
    """
    if not argv or argv[0] != "check-notebook-outputs":
        print(
            "usage: python -m src.data.acquisition check-notebook-outputs [--name NAME]",
            file=sys.stderr,
        )
        return 2
    name = "<stdin>"
    rest = list(argv[1:])
    if rest[:1] == ["--name"] and len(rest) >= 2:
        name = rest[1]
    try:
        violations = notebook_output_violations_from_text(sys.stdin.read(), name=name)
    except IntegrityError as exc:
        print(f"check-notebook-outputs: {exc}", file=sys.stderr)
        return 1
    for violation in violations:
        print(f"check-notebook-outputs: {name}: {violation}", file=sys.stderr)
    return 1 if violations else 0


if __name__ == "__main__":  # pragma: no cover - exercised via the pre-commit hook
    raise SystemExit(_cli(sys.argv[1:]))
