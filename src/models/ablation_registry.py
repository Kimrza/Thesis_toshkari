"""TE 7.2 ablation run-ID registration: the convention and the registration checks.

Purpose
-------
TE 7.2 says: "Ablations are named, predeclared runs ... Each is registered in
experiment.yaml with its own run ID." `src.models.train.read_ablations` already refuses
when an entry is missing or unexpected, and `assert_ablation_runnable` refuses an entry with
no `run_id` / `registered_at`. This module adds the checks a registration act needs before
it can be adopted:

* every run ID follows the one convention `ablation-<ablation id, lower case>`. The ID is
  derived from the ablation's identity alone, never from a result, a timestamp or a score
  (TE 7.2: never invented after results are seen);
* run IDs are unique across the five entries;
* each run ID matches its own entry (no swapped or mismatched IDs);
* no run ID collides with any run ID already in the experiment registry, whether historical,
  archived, superseded, aborted or undesignated;
* `registered_at` is an ISO-8601 UTC timestamp.

Fold and seed are NOT part of the registered ID. An ablation executes on the frozen F1-F4
folds with the confirmatory seeds (TE 7.2; seeds.yaml), each as a child run
`<run_id>/<fold_id>/seed-<seed>` (`child_run_id`). The registered ID names the ablation,
and the children name its executions.

Inputs
------
`AblationEntry` tuples from `src.models.train.read_ablations`; the registry's run IDs.

Re-run behaviour
----------------
Pure functions. Every refusal raises `IntegrityError` naming the resource.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Iterable, Sequence
from typing import Final

from src.data.config import IntegrityError
from src.models.train import ABLATION_IDS, AblationEntry

__all__ = [
    "RUN_ID_PREFIX",
    "canonical_run_id",
    "child_run_id",
    "assert_registration",
]

RUN_ID_PREFIX: Final[str] = "ablation-"


def canonical_run_id(ablation_id: str) -> str:
    """The one registered run ID for an ablation: a function of its identity only."""
    if ablation_id not in ABLATION_IDS:
        raise IntegrityError(
            f"ablation {ablation_id!r}", f"is not one of TE 7.2's five {list(ABLATION_IDS)}"
        )
    return RUN_ID_PREFIX + ablation_id.lower()


def child_run_id(run_id: str, *, fold_id: str, seed: int) -> str:
    """One execution of a registered ablation on one fold and one confirmatory seed."""
    return f"{run_id}/{fold_id}/seed-{int(seed)}"


def _utc(value: str, *, resource: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntegrityError(resource, f"registered_at {value!r} is not ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != dt.timedelta(0):
        raise IntegrityError(resource, f"registered_at {value!r} must be UTC")
    return parsed


def assert_registration(
    entries: Sequence[AblationEntry], *, registry_run_ids: Iterable[str]
) -> dict[str, str]:
    """Every entry registered, by convention, uniquely, without registry collision.

    Returns `{ablation_id: run_id}`. Refuses on the first violation.
    """
    ids = [e.ablation_id for e in entries]
    if sorted(ids) != sorted(ABLATION_IDS) or len(set(ids)) != len(ids):
        raise IntegrityError(
            "ablations.entries",
            f"must be exactly TE 7.2's five {list(ABLATION_IDS)}, each once; got {ids}",
        )
    existing = {str(r) for r in registry_run_ids}
    seen: dict[str, str] = {}
    for entry in entries:
        resource = f"ablations.entries.{entry.ablation_id}"
        if entry.run_id is None or entry.registered_at is None:
            raise IntegrityError(
                resource,
                "run_id / registered_at is still TBD; no ablation runs while its ID is TBD "
                "(TE 7.2; R-97)",
            )
        expected = canonical_run_id(entry.ablation_id)
        if entry.run_id != expected:
            raise IntegrityError(
                resource,
                f"run_id {entry.run_id!r} does not match its ablation; the registered ID is "
                f"{expected!r} (convention `{RUN_ID_PREFIX}<ablation id, lower case>`)",
            )
        if entry.run_id in seen:
            raise IntegrityError(
                resource, f"run_id {entry.run_id!r} duplicates {seen[entry.run_id]}'s"
            )
        collisions = sorted(
            r for r in existing if r == entry.run_id or r.startswith(entry.run_id + "/")
        )
        if collisions:
            raise IntegrityError(
                resource,
                f"run_id {entry.run_id!r} collides with existing registry run(s) "
                f"{collisions[:3]}; a registered ID must be unused",
            )
        _utc(entry.registered_at, resource=resource)
        seen[entry.run_id] = entry.ablation_id
    return {seen[r]: r for r in seen}
