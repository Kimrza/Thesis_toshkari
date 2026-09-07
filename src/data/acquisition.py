"""Acquisition library: redaction chokepoint, bounded retrieval, provenance manifests.

Purpose
-------
The `acquisition` unit's library surface (Q2 = A, receipted: a NEW module,
`src/data/acquisition.py`). Four responsibilities, each a workflow of the approved
functional design:

1. **The redaction serializer (W-9, R-39, SD-A-02).** One declared chokepoint every
   value this unit writes to a manifest, log or notebook output passes through.
   A **signed request URL** and an **auth header** are refused UNCONDITIONALLY on
   structural detection — the allowlist is never consulted for them. Everything else
   passes an entropy/prefix heuristic that **blocks the write and names what it
   matched**. `CredentialEgressError` is integrity tier: the run terminates and the
   `aborted` registry row is written through the stage entry contract's
   `IntegrityError` catch.
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
   carried on the manifest; and R-42's derived-release provenance check.
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
"""

from __future__ import annotations

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
    "guard_egress",
    "TransportResult",
    "RetrievalClient",
    "PROVENANCE_CLASSES",
    "DRIVER_INVENTORY_FIELDS",
    "LOCKED_YEAR",
    "LOCKED_MONTH",
    "store_gaps_as_nan",
    "count_gaps",
    "gap_accounting_entry",
    "assert_gap_conservation",
    "assert_madrigalweb_version",
    "assert_driver_inventory",
    "assert_single_release_grade",
    "write_request_manifest",
    "write_sha256_manifest",
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
    for _allow_name, pattern in REDACTION_ALLOWLIST:
        if pattern.match(candidate):
            return None  # legitimate high-entropy shape, named on the allowlist
    for name, prefix in _KNOWN_CREDENTIAL_PREFIXES:
        if candidate.startswith(prefix):
            return f"known credential prefix {prefix!r} ({name})"
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

        retrieval_date = _dt.datetime.now(_dt.UTC).date().isoformat()
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

_NAN: Final[float] = float("nan")


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
    provider_files: Sequence[Mapping[str, Any]],
    driver_inventory: Sequence[Mapping[str, Any]] = (),
    gap_accounting: Sequence[Mapping[str, Any]] = (),
    provenance_class: str,
    producing_interpreter: str,
    missing_months: Sequence[str] = (),
) -> Path:
    """Write `request_manifest.json` (W-3, domain-entities 2). Every value guarded.

    Validations, in order: `madrigalWeb_version` present and non-empty (R-35);
    `provenance_class` in the closed set (R-36); all nine TE 5.1 fields per driver
    series plus a single recorded grade (R-40); the NaN-count conservation invariant
    per gap-accounting entry (R-37); then the WHOLE payload through the W-9 redaction
    chokepoint — nothing is written when any check fails.

    `missing_months` is the machine-readable completeness-shortfall field
    (`team.md` § Code Style): a missing month is recorded here, never console text
    only, and is non-fatal — the `audit_ec1_drivers.py:184` gap is not reproduced.
    The retrieval policy is embedded so a retrieval's behaviour is reconstructible
    (SD-A-01).
    """
    assert_madrigalweb_version(identity)
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
    }
    guard_egress(payload, context=f"request_manifest[{Path(path).name}]")
    return _write_json(Path(path), payload)


def write_sha256_manifest(
    path: Path,
    *,
    provider_files: Sequence[Mapping[str, Any]],
    derived_artifacts: Mapping[str, str],
    provenance_class: str,
    producing_interpreter: str,
) -> Path:
    """Write `sha256_manifest.json` (W-4): one entry per provider file PLUS one per
    derived artifact, and the arithmetic holds by construction.

    A provider record without a `sha256` (an incomplete retrieval) is REFUSED here:
    admitting it would make the month's hash count silently omit a provider file,
    which is FR-P1-01-4's negative control. `derived_only` months honestly carry an
    empty provider list (DATA-07: no provider byte stream exists for the twelve
    pre-TC-06 months); a `full` month with zero provider entries is refused.

    Raises
    ------
    AcquisitionError
        on a hash-less provider record, an unknown provenance class, an empty
        `producing_interpreter`, or a `full` month with no provider entries.
    """
    if provenance_class not in PROVENANCE_CLASSES:
        raise AcquisitionError(
            str(path),
            f"provenance_class {provenance_class!r} is not one of "
            f"{sorted(PROVENANCE_CLASSES)} (R-36)",
        )
    if not str(producing_interpreter).strip():
        raise AcquisitionError(str(path), "producing_interpreter must be recorded (R-36)")

    provider_entries: dict[str, str] = {}
    for record in provider_files:
        name = str(record.get("provider_filename", "") or record.get("logical_name", ""))
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
        provider_entries[name] = digest
    if provenance_class == "full" and not provider_entries:
        raise AcquisitionError(
            str(path),
            "a 'full'-provenance month with zero provider-file hashes contradicts "
            "its own class; the twelve pre-TC-06 months are 'derived_only' and say "
            "so (R-36, Q5=C)",
        )

    payload: dict[str, Any] = {
        "provider_files": provider_entries,
        "derived_artifacts": dict(derived_artifacts),
        "hash_count": len(provider_entries) + len(derived_artifacts),
        "provenance_class": provenance_class,
        "producing_interpreter": producing_interpreter,
    }
    guard_egress(payload, context=f"sha256_manifest[{Path(path).name}]")
    return _write_json(Path(path), payload)


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
    predicate and by the window predicate below, so no second copy of the rule exists."""
    raw = str(record.get(timestamp_key, "") or "")
    try:
        return _dt.date.fromisoformat(raw[:10])
    except ValueError:
        raise AcquisitionError(
            raw or f"<record with no {timestamp_key}>",
            f"record timestamp {timestamp_key!r} is missing or unparseable; "
            f"membership derives from RECORD TIMESTAMPS, never from a directory or "
            f"file name (R-31, project.md Forbidden), and a record whose date cannot "
            f"be established cannot be cleared — fail closed, never guess",
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
