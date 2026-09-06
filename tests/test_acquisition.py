"""Negative controls for the `acquisition` unit: every hard rule's violation is CAUGHT.

Purpose
-------
The affirmed methodology is a negative control paired with every hard rule (team.md
§ Testing Posture): each test below proves a violation is refused, not only that the
happy path works. Covered, by plan step:

* Step 1 (W-9, R-39, SD-A-02): the redaction serializer — a token-shaped value is
  refused naming its match; a signed URL is refused even when its components are
  allowlisted-shaped (structural detection is never allowlist-gated); an auth header
  is refused; a legitimate hash and UUID pass via the named allowlist;
  `CredentialEgressError` derives from `IntegrityError` (R-01 any-future clause).
* Step 2 (SD-A-01, SEC-A-02): the bounded-retry client — a truncated stream never
  yields a manifest row with a hash (completeness BEFORE hash); a divergent re-run
  records both provider filenames and both hashes and refuses to overwrite; retry is
  bounded at the approved policy (5 attempts, base 1 s, factor 2, cap 60 s, full
  jitter, 60 s timeout) with exhaustion integrity-tier.
* Step 3 (R-34/35/36/37/40/41/42): manifest writers — absent `madrigalWeb_version`
  fails exactly as `"unknown"` fails; a sub-nine-field driver inventory fails; a
  mixed release grade within one series fails (REQ-NFR-A1's control); an injected
  gap survives as NaN and any fill breaks the conservation invariant; a hash-less
  provider record cannot enter `sha256_manifest.json`; an unresolved suffix mismatch
  is refused at release; a stale derived release fails without a re-pointing D-number.
* Step 4 (R-33, SD-A-03, Q1=A/Q2=C): `write_restricted` — a failed log append aborts
  the write with NO byte written; an ordinary path is refused; an uncharacterised
  platform is refused before any row; a read purpose is refused on the write path;
  the target-exists overwrite is refused. Exercised against `tmp_path` roots through
  the module's SUPPORTED TEST SEAM (`locked_test._repo_root`) only — no December
  content, no real restricted path, and this module holds no restricted-root literal
  (R-28: the boundary is composed from the imported constant, never spelled here).
* R-31 reaffirmed: locked-month membership derives from RECORD TIMESTAMPS — a
  December-dated record is excluded even when its own metadata names another month's
  folder, and an undatable record fails closed.
* Step 6 (Q3=A): the notebook saved-output check the pre-commit hook calls — saved
  outputs and execution counts are violations; an unparseable notebook fails closed.

Inputs
------
`tmp_path`, synthetic transports, synthetic records and notebook JSON. No network, no
December content, no restricted path, no scientific value. The real access log and
registry are never written.

Re-run behaviour
----------------
Deterministic and self-contained: injected sleep/rng/clock, tmp_path-only writes.
"""

from __future__ import annotations

import ast
import hashlib
import math
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import src.data.locked_test as locked_test  # noqa: E402
from src.data.acquisition import (  # noqa: E402
    LOCKED_MONTH,
    LOCKED_YEAR,
    RETRY_MAX_ATTEMPTS,
    AcquisitionError,
    CredentialEgressError,
    RetrievalClient,
    TransportResult,
    assert_derived_release_provenance,
    assert_gap_conservation,
    assert_madrigalweb_version,
    assert_no_locked_month_records,
    assert_release_free_of_unresolved_mismatch,
    count_gaps,
    gap_accounting_entry,
    guard_egress,
    guard_egress_value,
    notebook_output_violations,
    notebook_output_violations_from_text,
    partition_by_locked_month,
    retrieval_policy,
    store_gaps_as_nan,
    write_request_manifest,
    write_sha256_manifest,
)
from src.data.config import IntegrityError, ReleaseError  # noqa: E402
from src.data.locked_test import (  # noqa: E402
    PURPOSES,
    RESTRICTED_ROOT,
    AccessRecord,
    write_restricted,
)

SHA64 = hashlib.sha256(b"legitimate artifact bytes").hexdigest()


# =======================================================================================
# Step 1 — the redaction serializer (W-9, R-39, SD-A-02)
# =======================================================================================


def test_credential_egress_error_derives_from_the_one_base() -> None:
    """R-01's any-future clause: the stage entry contract's catch must see both."""
    assert issubclass(CredentialEgressError, IntegrityError)
    assert issubclass(AcquisitionError, IntegrityError)


def test_token_shaped_value_is_refused_and_the_match_is_named() -> None:
    with pytest.raises(CredentialEgressError) as excinfo:
        guard_egress_value("ghp_abcdefghijklmnopqrstuvwxyz0123456789", context="manifest.notes")
    assert "ghp_" in str(excinfo.value)
    assert "manifest.notes" in str(excinfo.value)


def test_generic_high_entropy_token_is_refused_naming_the_heuristic() -> None:
    with pytest.raises(CredentialEgressError) as excinfo:
        guard_egress_value("A1b2C3d4E5f6G7h8J9k0LmNoPqRsTuVw", context="log.value")
    assert "high-entropy" in str(excinfo.value)
    assert "REDACTION_ALLOWLIST" in str(excinfo.value)


def test_signed_url_is_refused_even_when_allowlisted_shaped() -> None:
    """Structural detection is UNCONDITIONAL: the allowlist is never consulted for a
    signed URL, so a signature that happens to be a 64-hex (allowlisted) shape is
    still refused."""
    url = f"https://provider.example.org/file.hdf5?X-Amz-Signature={SHA64}"
    with pytest.raises(CredentialEgressError) as excinfo:
        guard_egress_value(url, context="request_manifest.identity.url")
    assert "refused unconditionally" in str(excinfo.value)
    assert "signed request URL" in str(excinfo.value)


def test_url_with_userinfo_credentials_is_refused() -> None:
    with pytest.raises(CredentialEgressError):
        guard_egress_value("https://user:secretpass@provider.example.org/x", context="c")


def test_auth_header_is_refused_unconditionally() -> None:
    with pytest.raises(CredentialEgressError) as excinfo:
        guard_egress_value("Authorization: Bearer abc", context="c")
    assert "refused unconditionally" in str(excinfo.value)
    with pytest.raises(CredentialEgressError):
        guard_egress_value("Bearer eyJhbGciOiJIUzI1NiJ9.payload.sig", context="c")


def test_legitimate_hash_uuid_and_prose_pass_via_the_allowlist() -> None:
    assert guard_egress_value(SHA64, context="c") == SHA64
    uuid_text = "123e4567-e89b-12d3-a456-426614174000"
    assert guard_egress_value(uuid_text, context="c") == uuid_text
    assert guard_egress_value("hourly VTEC forecasting, calendar 2022", context="c")
    assert guard_egress_value("2026-09-05T12:00:00+00:00", context="c")
    assert guard_egress_value("aruc011a.22g.002", context="c") == "aruc011a.22g.002"


def test_guard_egress_walks_nested_payloads() -> None:
    clean = {"meta": {"files": ["a.hdf5"], "sha256": SHA64}}
    assert guard_egress(clean, context="manifest") is clean
    dirty = {"meta": {"url": f"https://x.example.org/f?sig={SHA64}"}}
    with pytest.raises(CredentialEgressError):
        guard_egress(dirty, context="manifest")


# =======================================================================================
# Step 2 — the bounded-retry retrieval client (SD-A-01, SEC-A-02)
# =======================================================================================


def _spec(name: str = "aruc011a.hdf5") -> dict[str, str]:
    return {
        "provider": "Madrigal (CEDAR)",
        "permanent_citation": "https://cedar.openmadrigal.org/",
        "location_date": "Haystack Madrigal archive, 2022",
        "logical_name": name,
    }


def _client(transport, **kwargs) -> RetrievalClient:
    kwargs.setdefault("sleep", lambda seconds: None)
    kwargs.setdefault("rng", lambda: 1.0)
    kwargs.setdefault("monotonic", lambda: 0.0)
    return RetrievalClient(transport, **kwargs)


def test_policy_is_the_approved_operational_values() -> None:
    policy = retrieval_policy()
    assert policy["retry_max_attempts"] == 5
    assert policy["retry_backoff_base_s"] == 1.0
    assert policy["retry_backoff_factor"] == 2.0
    assert policy["retry_backoff_cap_s"] == 60.0
    assert policy["retry_jitter"] == "full"
    assert policy["request_timeout_s"] == 60.0


def test_transient_failures_are_retried_within_the_bound(tmp_path: Path) -> None:
    calls: list[float] = []
    sleeps: list[float] = []

    def transport(spec, offset, timeout):
        calls.append(timeout)
        if len(calls) < 3:
            raise TimeoutError("provider stalled")
        return TransportResult(data=b"payload", complete=True, provider_filename="f.22g.002")

    client = _client(transport, sleep=sleeps.append)
    record = client.retrieve(_spec(), dest_dir=tmp_path)
    assert record["status"] == "complete"
    assert record["attempts"] == 3
    assert record["sha256"] == hashlib.sha256(b"payload").hexdigest()
    assert (tmp_path / "aruc011a.hdf5").read_bytes() == b"payload"
    assert all(timeout == 60.0 for timeout in calls)
    # Full jitter with rng()=1.0: the two backoffs are the ceilings 1 s and 2 s.
    assert sleeps == [1.0, 2.0]


def test_retry_exhaustion_is_integrity_tier_and_writes_nothing(tmp_path: Path) -> None:
    attempts: list[int] = []

    def transport(spec, offset, timeout):
        attempts.append(offset)
        raise OSError("connection reset")

    with pytest.raises(AcquisitionError) as excinfo:
        _client(transport).retrieve(_spec(), dest_dir=tmp_path)
    assert len(attempts) == RETRY_MAX_ATTEMPTS
    assert "bounded" in str(excinfo.value)
    assert not any(tmp_path.iterdir()), "an exhausted retrieval left bytes behind"


def test_backoff_follows_the_approved_schedule_and_stays_under_the_cap() -> None:
    """Base 1 s, factor 2: ceilings 1/2/4/8 s across the four backoffs five attempts
    allow — the 60 s cap bounds the formula and is never exceeded (with rng()=1.0 the
    sleep IS the ceiling, so the schedule is asserted exactly)."""
    sleeps: list[float] = []

    def transport(spec, offset, timeout):
        raise TimeoutError("stalled")

    with pytest.raises(AcquisitionError):
        _client(transport, sleep=sleeps.append).retrieve(_spec(), dest_dir=Path("."))
    assert sleeps == [1.0, 2.0, 4.0, 8.0]  # 4 backoffs between 5 attempts, none > 60
    assert all(value <= 60.0 for value in sleeps)


def test_truncated_stream_never_yields_a_manifest_row_with_a_hash(tmp_path: Path) -> None:
    """SD-A-01's ordering: completeness BEFORE hash. A partial file is never promoted:
    the target is ABSENT and the record carries no sha256 key at all."""

    def transport(spec, offset, timeout):
        return TransportResult(data=b"trunc", complete=False, provider_filename="f.22g.002")

    record = _client(transport).retrieve(_spec(), dest_dir=tmp_path)
    assert record["status"] == "incomplete"
    assert "sha256" not in record
    assert not (tmp_path / "aruc011a.hdf5").exists(), "a short file that looks whole"


def test_divergent_rerun_records_both_and_refuses_to_overwrite(tmp_path: Path) -> None:
    """SEC-A-02: both provider filenames incl. version suffixes, both hashes; the
    on-disk bytes stay the recorded ones."""
    original = b"original bytes"
    (tmp_path / "aruc011a.hdf5").write_bytes(original)
    prior = {
        "provider_filename": "f.22g.002",
        "sha256": hashlib.sha256(original).hexdigest(),
    }

    def transport(spec, offset, timeout):
        return TransportResult(
            data=b"reissued bytes", complete=True, provider_filename="f.22g.003"
        )

    record = _client(transport).retrieve(_spec(), dest_dir=tmp_path, prior_record=prior)
    assert record["status"] == "divergent-not-overwritten"
    divergence = record["divergence"]
    assert divergence["recorded_provider_filename"] == "f.22g.002"
    assert divergence["retrieved_provider_filename"] == "f.22g.003"
    assert divergence["recorded_sha256"] == prior["sha256"]
    assert divergence["retrieved_sha256"] == hashlib.sha256(b"reissued bytes").hexdigest()
    assert (tmp_path / "aruc011a.hdf5").read_bytes() == original, "the overwrite happened"
    # And the release-side guard refuses the unresolved divergence (R-34's shape):
    with pytest.raises(ReleaseError):
        assert_release_free_of_unresolved_mismatch([record])


def test_suffix_mismatch_is_recorded_nonfatally_at_retrieval(tmp_path: Path) -> None:
    """R-34 steps 1-2: provider reissue is a NORMAL event; the run continues and the
    manifest carries the machine-readable field."""
    payload = b"same bytes"
    prior = {"provider_filename": "f.22g.002", "sha256": hashlib.sha256(payload).hexdigest()}

    def transport(spec, offset, timeout):
        return TransportResult(data=payload, complete=True, provider_filename="f.22g.003")

    record = _client(transport).retrieve(_spec(), dest_dir=tmp_path, prior_record=prior)
    assert record["status"] == "complete"
    assert record["suffix_mismatch"] == {
        "recorded_provider_filename": "f.22g.002",
        "retrieved_provider_filename": "f.22g.003",
        "resolved_by": None,
    }
    # Refused at release while unresolved (R-34 step 3)...
    with pytest.raises(ReleaseError) as excinfo:
        assert_release_free_of_unresolved_mismatch([record])
    assert "suffix" in str(excinfo.value)
    # ...and admitted once a D-number resolves it.
    record["suffix_mismatch"]["resolved_by"] = "D-99"
    assert_release_free_of_unresolved_mismatch([record])


def test_resumption_passes_the_offset_where_the_transport_supports_it(tmp_path: Path) -> None:
    offsets: list[int] = []
    chunks = [
        TransportResult(data=b"ab", complete=False, provider_filename="f.22g.002", resumable=True),
        TransportResult(data=b"cd", complete=True, provider_filename="f.22g.002", resumable=True),
    ]

    def transport(spec, offset, timeout):
        offsets.append(offset)
        return chunks[len(offsets) - 1]

    record = _client(transport).retrieve(_spec(), dest_dir=tmp_path)
    assert offsets == [0, 2], "the second call must resume at the received length"
    assert record["sha256"] == hashlib.sha256(b"abcd").hexdigest()
    assert (tmp_path / "aruc011a.hdf5").read_bytes() == b"abcd"


def test_rate_bound_sleeps_between_requests(tmp_path: Path) -> None:
    """TE 8.1: provider terms bound the rate; the client enforces a minimum interval."""
    sleeps: list[float] = []
    clock = iter([0.0, 0.1, 5.1])  # stamp req 1; check before req 2; stamp req 2

    def transport(spec, offset, timeout):
        return TransportResult(data=b"x", complete=True, provider_filename="f.22g.002")

    client = _client(
        transport, sleep=sleeps.append, monotonic=lambda: next(clock), min_interval_s=5.0
    )
    client.retrieve(_spec("a.hdf5"), dest_dir=tmp_path)
    client.retrieve(_spec("b.hdf5"), dest_dir=tmp_path)
    assert len(sleeps) == 1 and sleeps[0] == pytest.approx(4.9)


def test_a_spec_missing_an_identity_field_is_refused(tmp_path: Path) -> None:
    def transport(spec, offset, timeout):  # pragma: no cover - never reached
        raise AssertionError("transport must not be called for a malformed spec")

    spec = _spec()
    spec["permanent_citation"] = ""
    with pytest.raises(AcquisitionError) as excinfo:
        _client(transport).retrieve(spec, dest_dir=tmp_path)
    assert "permanent_citation" in str(excinfo.value)


# =======================================================================================
# Step 3 — manifest writers (R-34, R-35, R-36, R-37, R-40, R-42)
# =======================================================================================


def _identity(**overrides: object) -> dict[str, object]:
    identity: dict[str, object] = {
        "experiment": "MAPGPS gps binned VTEC",
        "kindat": "3505",
        "parameters": "gdlat,glon,tec,dtec",
        "madrigalWeb_version": "3.3.3",
    }
    identity.update(overrides)
    return identity


def _provider_record(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "provider": "Madrigal (CEDAR)",
        "permanent_citation": "https://cedar.openmadrigal.org/",
        "location_date": "Haystack Madrigal archive, 2022",
        "provider_filename": "aruc011a.22g.002",
        "retrieval_date": "2026-09-05",
        "sha256": SHA64,
        "suffix_mismatch": None,
        "divergence": None,
        "status": "complete",
        "attempts": 1,
    }
    record.update(overrides)
    return record


def _driver_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "series": "kyoto_dst",
        "provider": "Kyoto WDC",
        "role": "diagnostic/hindcast-only (TC-11)",
        "provider_product_identity": "dst_provisional_202211.html",
        "coverage": "calendar 2022, hourly",
        "retrieval_date": "2026-09-05",
        "checksum": SHA64,
        "release_status": "provisional",
        "licence_access_notes": "Kyoto non-commercial-use notice recorded verbatim (D-6)",
        "consuming_configuration": "configs/features.yaml drivers.dst",
    }
    entry.update(overrides)
    return entry


def test_request_manifest_happy_path_carries_policy_and_fields(tmp_path: Path) -> None:
    path = write_request_manifest(
        tmp_path / "request_manifest.json",
        identity=_identity(),
        provider_files=[_provider_record()],
        driver_inventory=[_driver_entry()],
        gap_accounting=[
            gap_accounting_entry("kyoto_dst", gaps_at_retrieval=2, gaps_in_artifact=2)
        ],
        provenance_class="full",
        producing_interpreter="Python 3.11.9 (smoke environment)",
        missing_months=["2022-04"],
    )
    import json

    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["retrieval_policy"] == retrieval_policy()
    assert manifest["missing_months"] == ["2022-04"], "shortfalls are manifest fields"
    assert manifest["provenance_class"] == "full"
    assert manifest["producing_interpreter"].startswith("Python 3.11")
    assert manifest["provider_files"][0]["provider_filename"] == "aruc011a.22g.002"


def test_absent_madrigalweb_version_fails_exactly_as_unknown_fails(tmp_path: Path) -> None:
    """R-35: one raise site, so the two failures are literally identical."""
    identity_absent = _identity()
    del identity_absent["madrigalWeb_version"]
    with pytest.raises(AcquisitionError) as absent_info:
        assert_madrigalweb_version(identity_absent)
    with pytest.raises(AcquisitionError) as unknown_info:
        assert_madrigalweb_version(_identity(madrigalWeb_version="unknown"))
    assert str(absent_info.value) == str(unknown_info.value)
    # And the writer enforces it — nothing is written on refusal.
    target = tmp_path / "request_manifest.json"
    with pytest.raises(AcquisitionError):
        write_request_manifest(
            target,
            identity=identity_absent,
            provider_files=[],
            provenance_class="derived_only",
            producing_interpreter="Python 3.11.9",
        )
    assert not target.exists()


def test_driver_inventory_with_fewer_than_nine_fields_fails(tmp_path: Path) -> None:
    entry = _driver_entry()
    del entry["licence_access_notes"]
    del entry["consuming_configuration"]
    with pytest.raises(AcquisitionError) as excinfo:
        write_request_manifest(
            tmp_path / "m.json",
            identity=_identity(),
            provider_files=[],
            driver_inventory=[entry],
            provenance_class="derived_only",
            producing_interpreter="Python 3.11.9",
        )
    message = str(excinfo.value)
    assert "licence_access_notes" in message and "consuming_configuration" in message


def test_mixed_release_grade_within_one_series_fails(tmp_path: Path) -> None:
    """REQ-NFR-A1's negative control: grades are never mixed within a series."""
    with pytest.raises(AcquisitionError) as excinfo:
        write_request_manifest(
            tmp_path / "m.json",
            identity=_identity(),
            provider_files=[],
            driver_inventory=[
                _driver_entry(release_status="provisional"),
                _driver_entry(release_status="final"),
            ],
            provenance_class="derived_only",
            producing_interpreter="Python 3.11.9",
        )
    assert "mixed release grades" in str(excinfo.value)


def test_empty_release_status_fails() -> None:
    with pytest.raises(AcquisitionError) as excinfo:
        write_request_manifest(
            Path("unused.json"),
            identity=_identity(),
            provider_files=[],
            driver_inventory=[_driver_entry(release_status="")],
            provenance_class="derived_only",
            producing_interpreter="Python 3.11.9",
        )
    assert "release" in str(excinfo.value).lower()


def test_injected_gap_survives_acquisition_as_nan() -> None:
    """R-37's round trip: the gap survives as NaN and nothing else changes."""
    stored = store_gaps_as_nan([12.5, None, 13.0])
    assert stored[0] == 12.5 and stored[2] == 13.0
    assert math.isnan(stored[1])
    assert count_gaps(stored) == 1


def test_any_fill_breaks_the_conservation_invariant() -> None:
    """R-37's carrying limb: a fill (simulated as a lower artifact count) terminates."""
    raw = [12.5, None, 13.0]
    filled = [12.5, 12.75, 13.0]  # what a convenience fillna would produce
    with pytest.raises(AcquisitionError) as excinfo:
        gap_accounting_entry(
            "kyoto_dst",
            gaps_at_retrieval=count_gaps(raw),
            gaps_in_artifact=count_gaps(filled),
        )
    assert "conservation" in str(excinfo.value)
    # The equal case is the pass condition, carried as a manifest field.
    entry = gap_accounting_entry("kyoto_dst", gaps_at_retrieval=1, gaps_in_artifact=1)
    assert_gap_conservation(entry)


def test_sha256_manifest_arithmetic_holds_and_refuses_a_hashless_provider_row(
    tmp_path: Path,
) -> None:
    """FR-P1-01-4: the month's hash count equals provider files plus derived artifacts,
    and a provider record without a hash (incomplete/divergent) cannot enter."""
    import json

    path = write_sha256_manifest(
        tmp_path / "sha256_manifest.json",
        provider_files=[_provider_record()],
        derived_artifacts={"coverage_summary.csv": SHA64},
        provenance_class="full",
        producing_interpreter="Python 3.11.9",
    )
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert (
        manifest["hash_count"]
        == 2
        == len(manifest["provider_files"]) + len(manifest["derived_artifacts"])
    )
    incomplete = _provider_record(status="incomplete")
    del incomplete["sha256"]
    with pytest.raises(AcquisitionError) as excinfo:
        write_sha256_manifest(
            tmp_path / "s2.json",
            provider_files=[incomplete],
            derived_artifacts={},
            provenance_class="full",
            producing_interpreter="Python 3.11.9",
        )
    assert "omit a provider file" in str(excinfo.value)


def test_full_class_with_zero_provider_hashes_is_refused_and_derived_only_is_honest(
    tmp_path: Path,
) -> None:
    with pytest.raises(AcquisitionError):
        write_sha256_manifest(
            tmp_path / "s.json",
            provider_files=[],
            derived_artifacts={"a.csv": SHA64},
            provenance_class="full",
            producing_interpreter="Python 3.11.9",
        )
    # The twelve pre-TC-06 months' honest state: derived artifacts only, marked so.
    path = write_sha256_manifest(
        tmp_path / "s.json",
        provider_files=[],
        derived_artifacts={"a.csv": SHA64},
        provenance_class="derived_only",
        producing_interpreter="Python 3.14.0 (out-of-envelope, recorded not hidden)",
    )
    assert path.is_file()


def test_unknown_provenance_class_is_refused(tmp_path: Path) -> None:
    with pytest.raises(AcquisitionError):
        write_sha256_manifest(
            tmp_path / "s.json",
            provider_files=[],
            derived_artifacts={},
            provenance_class="mostly_full",
            producing_interpreter="Python 3.11.9",
        )


def test_manifest_writer_refuses_a_credential_and_writes_nothing(tmp_path: Path) -> None:
    """W-9 wired into W-3: the serializer guards every manifest value; on refusal the
    manifest does not exist."""
    target = tmp_path / "request_manifest.json"
    with pytest.raises(CredentialEgressError):
        write_request_manifest(
            target,
            identity=_identity(source_url=f"https://x.example.org/f?token={SHA64}"),
            provider_files=[],
            provenance_class="derived_only",
            producing_interpreter="Python 3.11.9",
        )
    assert not target.exists()


def test_stale_derived_release_fails_without_a_repointing_dnumber() -> None:
    """R-42: digest equality or a D-number; D-18's re-merge is the first branch."""
    recorded = {"2022-01": "aaa", "2022-02": "bbb"}
    current_equal = {"2022-01": "aaa", "2022-02": "bbb"}
    assert_derived_release_provenance(recorded, current_equal)  # first branch holds
    current_regenerated = {"2022-01": "aaa", "2022-02": "REGENERATED"}
    with pytest.raises(ReleaseError) as excinfo:
        assert_derived_release_provenance(recorded, current_regenerated)
    assert "2022-02" in str(excinfo.value)
    # Second branch: an explicit re-pointing decision covers the difference.
    assert_derived_release_provenance(recorded, current_regenerated, repointing_decision="D-18")


# =======================================================================================
# R-31 reaffirmed — membership from record timestamps, never names (BLK-07's bar)
# =======================================================================================


def test_locked_month_membership_derives_from_record_timestamps_not_names() -> None:
    """The year-blind-predicate defect class (ML-07/TEC-09): a December-dated record
    is excluded even when its own metadata claims another month's folder, and a
    November record filed under a December-looking name is kept."""
    december_misfiled = {
        "timestamp": f"{LOCKED_YEAR}-{LOCKED_MONTH:02d}-31T23:00:00Z",
        "folder": f"audit_evidence_{LOCKED_YEAR}-01",  # the name lies; the date rules
    }
    november_scary_name = {
        "timestamp": f"{LOCKED_YEAR}-11-30T23:00:00Z",
        "folder": f"audit_evidence_{LOCKED_YEAR}-{LOCKED_MONTH:02d}",
    }
    kept, locked = partition_by_locked_month([december_misfiled, november_scary_name])
    assert locked == [december_misfiled]
    assert kept == [november_scary_name]


def test_locked_month_records_are_refused_while_blk07_stands() -> None:
    with pytest.raises(AcquisitionError) as excinfo:
        assert_no_locked_month_records(
            [{"timestamp": f"{LOCKED_YEAR}-{LOCKED_MONTH:02d}-01T00:00:00Z"}]
        )
    assert "BLK-07" in str(excinfo.value)
    # Clean records pass.
    assert_no_locked_month_records([{"timestamp": f"{LOCKED_YEAR}-11-01T00:00:00Z"}])


def test_an_undatable_record_fails_closed_rather_than_being_kept() -> None:
    with pytest.raises(AcquisitionError) as excinfo:
        partition_by_locked_month([{"timestamp": "not-a-date"}])
    assert "fail closed" in str(excinfo.value)
    with pytest.raises(AcquisitionError):
        partition_by_locked_month([{"no_timestamp_at_all": True}])


# =======================================================================================
# Step 4 — write_restricted (R-33, SD-A-03, Q1=A, Q2=C), tmp_path roots ONLY
# =======================================================================================


def _write_record(purpose: str = "acquisition_write") -> AccessRecord:
    return AccessRecord(
        run_id="test-write-run",
        retrieved_at_utc="2026-09-05T00:00:00Z",
        scope="synthetic tmp_path boundary; no December content",
        purpose=purpose,
        performance_inspected=False,
        locked_test_accessed=True,
        authorization="D-31-authorised mechanism test; BLK-07 authorization limb open",
    )


@pytest.fixture
def synthetic_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The module's SUPPORTED TEST SEAM: `_repo_root` is monkeypatched to `tmp_path`,
    so the boundary is `tmp_path / RESTRICTED_ROOT` — composed from the imported
    constant, never spelled in this file (R-28), and holding no real December bytes."""
    monkeypatch.setattr(locked_test, "_repo_root", lambda: tmp_path)
    monkeypatch.setenv("TEC_PLATFORM", "local")
    return tmp_path / RESTRICTED_ROOT


def test_purposes_gained_the_two_acquisition_values_compatibly() -> None:
    """Q2=C's enum extension: the three Vision 8.3 values remain, two are added."""
    assert {"coverage_audit", "regime_audit", "locked_evaluation"} <= PURPOSES
    assert {"acquisition_read", "acquisition_write"} <= PURPOSES
    assert len(PURPOSES) == 5
    # AccessRecord accepts the new purposes (the extension is compatible).
    assert _write_record().purpose == "acquisition_write"


def test_write_restricted_logs_durably_first_then_writes(
    synthetic_boundary: Path,
) -> None:
    registry = synthetic_boundary.parent.parent / "access.jsonl"
    target = synthetic_boundary / "reacquired" / "sample.hdf5"
    returned = write_restricted(
        target, b"provider bytes", record=_write_record(), registry=registry
    )
    assert returned.read_bytes() == b"provider bytes"
    import json

    rows = [
        json.loads(line)
        for line in registry.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert len(rows) == 1
    assert rows[0]["purpose"] == "acquisition_write"
    assert "logged_at_utc" in rows[0], "the guard must stamp its own ordering evidence"


def test_failed_log_append_aborts_the_write_with_no_byte_written(
    synthetic_boundary: Path, tmp_path: Path
) -> None:
    """R-33's central negative control: no mutation without a record."""
    blocker = tmp_path / "blocker"
    blocker.write_text("a file, not a directory", encoding="utf-8")
    unwritable_registry = blocker / "nested" / "access.jsonl"
    target = synthetic_boundary / "sample.hdf5"
    with pytest.raises(locked_test.LockedTestError) as excinfo:
        write_restricted(target, b"bytes", record=_write_record(), registry=unwritable_registry)
    assert "BEFORE any byte" in str(excinfo.value)
    assert not target.exists(), "a byte was written with no durable access row"
    assert not target.parent.exists() or not any(target.parent.iterdir())


def test_ordinary_path_is_refused_for_writes(synthetic_boundary: Path, tmp_path: Path) -> None:
    registry = tmp_path / "access.jsonl"
    ordinary = tmp_path / "ordinary" / "file.bin"
    with pytest.raises(locked_test.LockedTestError) as excinfo:
        write_restricted(ordinary, b"x", record=_write_record(), registry=registry)
    assert RESTRICTED_ROOT in str(excinfo.value)
    assert not registry.exists(), "a refused write consumed an access row"
    assert not ordinary.exists()


def test_uncharacterised_platform_refuses_the_write_before_any_row(
    synthetic_boundary: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Q1=A applied to the write side: fail closed, no row, no byte."""
    monkeypatch.setenv("TEC_PLATFORM", "kaggle")
    registry = tmp_path / "access.jsonl"
    target = synthetic_boundary / "sample.hdf5"
    with pytest.raises(locked_test.LockedTestError) as excinfo:
        write_restricted(target, b"x", record=_write_record(), registry=registry)
    assert "uncharacterised" in str(excinfo.value)
    assert not registry.exists() and not target.exists()


def test_a_read_purpose_is_refused_on_the_write_path(
    synthetic_boundary: Path, tmp_path: Path
) -> None:
    """A write recorded under a read purpose describes an event that did not happen."""
    registry = tmp_path / "access.jsonl"
    target = synthetic_boundary / "sample.hdf5"
    with pytest.raises(locked_test.LockedTestError) as excinfo:
        write_restricted(
            target, b"x", record=_write_record(purpose="coverage_audit"), registry=registry
        )
    assert "acquisition_write" in str(excinfo.value)
    assert not registry.exists() and not target.exists()


def test_an_existing_restricted_target_is_never_overwritten(
    synthetic_boundary: Path, tmp_path: Path
) -> None:
    registry = tmp_path / "access.jsonl"
    target = synthetic_boundary / "sample.hdf5"
    write_restricted(target, b"first", record=_write_record(), registry=registry)
    with pytest.raises(locked_test.LockedTestError) as excinfo:
        write_restricted(target, b"second", record=_write_record(), registry=registry)
    assert "never" in str(excinfo.value) and "overwritten" in str(excinfo.value)
    assert target.read_bytes() == b"first"


# =======================================================================================
# Step 6 — the notebook saved-output check (Q3=A, SD-A-02 limb 2)
# =======================================================================================


def _notebook(cells: list[dict]) -> dict:
    return {"cells": cells, "nbformat": 4, "nbformat_minor": 5}


def test_clean_notebook_passes() -> None:
    clean = _notebook(
        [
            {"cell_type": "markdown", "source": ["# prose\n"]},
            {"cell_type": "code", "source": ["x = 1\n"], "outputs": [], "execution_count": None},
        ]
    )
    assert notebook_output_violations(clean) == []


def test_saved_outputs_and_execution_counts_are_violations() -> None:
    dirty = _notebook(
        [
            {
                "cell_type": "code",
                "source": ["print(1)\n"],
                "outputs": [{"output_type": "stream", "text": ["1\n"]}],
                "execution_count": 3,
            }
        ]
    )
    violations = notebook_output_violations(dirty)
    assert any("saved output" in v for v in violations)
    assert any("execution_count=3" in v for v in violations)


def test_unparseable_notebook_fails_closed() -> None:
    with pytest.raises(AcquisitionError) as excinfo:
        notebook_output_violations_from_text("{not json", name="broken.ipynb")
    assert "fail" in str(excinfo.value).lower()
    with pytest.raises(AcquisitionError):
        notebook_output_violations_from_text('["not-an-object"]', name="broken.ipynb")
    with pytest.raises(AcquisitionError):
        notebook_output_violations({"no_cells": True})


def test_the_workspace_notebook_is_clean_today() -> None:
    """The hook is PREVENTIVE (nfr-design review Minor 2): the existing notebook holds
    no saved outputs as of this pass, and this test keeps that true."""
    notebook_path = REPO_ROOT / "notebooks" / "madrigal_phase1_coverage_audit.ipynb"
    if not notebook_path.is_file():
        pytest.skip("workspace notebook absent")
    violations = notebook_output_violations_from_text(
        notebook_path.read_text(encoding="utf-8"), name=notebook_path.name
    )
    assert violations == []


# =======================================================================================
# Step 5 — the stage script's conventions, pinned statically (no execution: main()
# re-execs the interpreter, so these are AST assertions, the project's own pattern)
# =======================================================================================

SCRIPT = REPO_ROOT / "scripts" / "00_acquire_prepared_vtec.py"


def test_stage_script_opens_main_with_ensure_process_determinism() -> None:
    """R-05 / the six-step entry contract: the FIRST statement of main()."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))
    main_def = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    )
    first = main_def.body[0]
    assert isinstance(first, ast.Expr) and isinstance(first.value, ast.Call)
    func = first.value.func
    name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
    assert name == "ensure_process_determinism", (
        "main()'s first statement must be ensure_process_determinism(sys.argv) — "
        "before any framework import can matter (R-05)"
    )


def test_stage_script_takes_config_and_never_imports_the_restricted_guard() -> None:
    """§13.2's `--config configs/` convention, and the no-restricted-path claim in
    checkable form: the script imports nothing from the guard module, so it cannot
    construct a restricted path (R-28, R-32)."""
    source = SCRIPT.read_text(encoding="utf-8")
    assert '"--config"' in source
    tree = ast.parse(source, filename=str(SCRIPT))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
    assert not any("locked_test" in module for module in imported), (
        "the acquisition stage script must not import the restricted-root guard: it "
        "names no restricted artifact and constructs no restricted path (R-32; no "
        "December access of any kind in this Bolt)"
    )


def test_acquisition_preflight_entry_names_the_d144_identity_fields() -> None:
    """The REQUIRED_FIELDS_MAP entry exists and names field IDENTITIES the owner must
    freeze — the script refuses at preflight until data.yaml carries them (TE 18.3)."""
    from src.data.config import required_fields_for

    fields = required_fields_for("acquisition", 1)
    assert "data.acquisition.experiment" in fields
    assert "data.acquisition.kindat" in fields
    assert "data.acquisition.parameters" in fields
    assert "seeds.development" in fields
