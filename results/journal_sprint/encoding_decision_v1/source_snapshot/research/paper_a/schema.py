"""Versioned result records and the append-only JSONL store.

Retries never overwrite a first planned attempt, and reconstructed circuit
fields never populate actual_* fields (Annex I).
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "paper-a-record-v1"

REQUIRED_FIELDS = (
    "schema_version",
    "experiment_uuid",
    "phase",
    "config_id",
    "n",
    "replicate",
    "condition",
    "attempt_kind",
    "raw_estimation",
    "raw_confidence_interval",
    "raw_price",
    "presentation_clipped_price",
    "completion_state",
    "environment",
)

_ACTUAL_PREFIXES = ("actual_circuit_", "actual_isa_", "actual_gate_")
_RECONSTRUCTED_PREFIXES = (
    "reconstructed_logical_",
    "reconstructed_isa_",
    "reconstructed_resource_",
    "reconstructed_circuit_",
)


def _populated(record: dict, prefixes: tuple[str, ...]) -> bool:
    return any(record.get(k) is not None for k in record if k.startswith(prefixes))


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return a list of violations; empty means the record is valid."""
    violations: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            violations.append(f"missing required field {field}")
    if violations:
        return violations

    if record["schema_version"] != SCHEMA_VERSION:
        violations.append(f"schema_version {record['schema_version']} != {SCHEMA_VERSION}")

    est = record["raw_estimation"]
    if est is not None and (not _finite_number(est) or not 0.0 <= est <= 1.0):
        violations.append(f"raw_estimation {est} outside [0,1]")

    ci = record["raw_confidence_interval"]
    if ci is not None:
        if (
            not isinstance(ci, (list, tuple))
            or len(ci) != 2
            or not all(_finite_number(value) for value in ci)
            or not 0.0 <= ci[0] <= ci[1] <= 1.0
        ):
            violations.append(f"invalid interval {ci}")

    price, clipped = record["raw_price"], record["presentation_clipped_price"]
    if price is not None and (
        not _finite_number(price) or not _finite_number(clipped) or clipped != max(0.0, price)
    ):
        violations.append(f"presentation_clipped_price {clipped} != max(0, {price})")

    if _populated(record, _ACTUAL_PREFIXES) and _populated(record, _RECONSTRUCTED_PREFIXES):
        violations.append("mixed provenance: actual_* and reconstructed_* both populated")

    return violations


def _finite_number(value):
    try:
        return (
            isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        )
    except OverflowError:
        return False


def append_record(path: Path, record: dict[str, Any]) -> None:
    """Durably append one record. Never rewrites earlier lines."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def read_records(path: Path) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8").strip()
    return [json.loads(line) for line in text.splitlines()] if text else []


def idempotency_key(
    experiment_uuid: str,
    phase: str,
    config_id: str,
    n: int,
    replicate: int,
    condition: str,
    purpose: str,
) -> str:
    return "/".join([experiment_uuid, phase, config_id, str(n), str(replicate), condition, purpose])
