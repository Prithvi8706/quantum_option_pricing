"""Tiny end-to-end experiment: 2 configs, n=3, 2 seeds, ideal only.

Exercises config -> references -> circuit -> recorded IQAE -> raw records ->
resources -> validation -> COMPLETE, so the pipeline is proven before any
full experiment runs.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from pathlib import Path

from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation

from research.paper_a.benchmark import BENCHMARK, by_id
from research.paper_a.environment import capture_environment
from research.paper_a.errors import deterministic_ladder
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import C_RESCALING, presentation_clipped, to_price
from research.paper_a.recording import RecordingSampler
from research.paper_a.references import select_support_rule, support_bounds
from research.paper_a.resources import (
    executed_powers,
    m_a_executed,
    m_a_logical,
    m_q_executed,
    max_executed_depth,
    shot_weighted_gates,
)
from research.paper_a.schema import (
    SCHEMA_VERSION,
    append_record,
    idempotency_key,
    read_records,
    validate_record,
)
from research.paper_a.streams import generator, stream_key

CONFIGS = ("E001", "E025")
REPLICATES = (0, 1)
CONFIG = json.loads((Path(__file__).parent.parent / "configs/e0.json").read_text())
N = 3
EXPERIMENT_UUID = "smoke-0001"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_state(path, payload):
    """Flush a replacement before publishing it; never publish a partial marker."""
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, allow_nan=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def _indexed_records(path):
    rows = read_records(path) if path.exists() else []
    indexed = {r["idempotency_key"]: r for r in rows}
    if len(indexed) != len(rows):
        raise ValueError(f"duplicate attempt keys in {path.name}")
    return indexed


def _recover_pairs(out, raw_path, res_path):
    """Recover only original recorded payloads, never reconstructed resources."""
    raw, resources = _indexed_records(raw_path), _indexed_records(res_path)
    for journal in sorted((out / "attempt_journal").glob("*.json")):
        pair = json.loads(journal.read_text(encoding="utf-8"))
        key = pair["raw"]["idempotency_key"]
        if pair["resources"]["idempotency_key"] != key:
            raise ValueError("journal attempt keys differ")
        for field, saved, path in (("raw", raw, raw_path), ("resources", resources, res_path)):
            if key in saved and saved[key] != pair[field]:
                raise ValueError(f"journal conflicts with {field} record")
            if key not in saved:
                append_record(path, pair[field])
                saved[key] = pair[field]
    if raw.keys() != resources.keys():
        raise ValueError("unpaired legacy attempt has no recovery journal; retain and audit")
    return set(raw)


def _persist_pair(out, raw_path, res_path, record, resource):
    journals = out / "attempt_journal"
    journals.mkdir(exist_ok=True)
    key = record["idempotency_key"]
    path = journals / (hashlib.sha256(key.encode()).hexdigest() + ".json")
    if path.exists():
        raise ValueError("attempt journal already exists; recovery must run first")
    _write_state(path, {"raw": record, "resources": resource})
    append_record(raw_path, record)
    append_record(res_path, resource)


def run_smoke(output_dir, shots: int = 512) -> dict:
    if isinstance(shots, bool) or not isinstance(shots, int) or shots <= 0:
        raise ValueError("shots must be a positive integer")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_path, res_path = out / "raw.jsonl", out / "resources.jsonl"

    # Invalidate a stale success marker before any recovery or validation can fail.
    (out / "COMPLETE").unlink(missing_ok=True)
    done = _recover_pairs(out, raw_path, res_path)
    q_total = select_support_rule(BENCHMARK, CONFIG["q_total_candidates"])
    plan = {
        "version": "smoke-v2",
        "shots": shots,
        "q_total": q_total,
        "n": N,
        "rescaling": C_RESCALING,
        "contracts": list(CONFIGS),
        "replicates": list(REPLICATES),
        "experiment_uuid": EXPERIMENT_UUID,
    }
    plan_path = out / "acquisition.json"
    if plan_path.exists():
        if json.loads(plan_path.read_text()) != plan:
            raise ValueError("acquisition configuration changed; use a new output directory")
    elif done:
        # Legacy data cannot establish the requested acquisition configuration.
        if any(validate_record(r) for r in read_records(raw_path)):
            _write_state(out / "validation.json", {"violations": "legacy record validation failed"})
            raise ValueError("raw record validation failed")
        raise ValueError("legacy acquisition configuration unknown; use a new output directory")
    else:
        _write_state(plan_path, plan)
    if done and any(r["completion_state"] != "complete" for r in read_records(raw_path)):
        raise ValueError("failed attempt retained; use a new output directory for a retry")
    environment = capture_environment()
    planned_attempts = 0

    for cid in CONFIGS:
        contract = by_id(cid)
        L, U = support_bounds(contract, q_total)
        ladder = deterministic_ladder(contract, q_total, N, C_RESCALING)
        ec = build_european(contract, L, U, N, C_RESCALING)

        for replicate in REPLICATES:
            # Counts planned config x replicate combinations, including ones
            # skipped below because they were already done.
            planned_attempts += 1
            key = idempotency_key(
                EXPERIMENT_UUID, "SMOKE", cid, N, replicate, "ideal", f"shots-{shots}"
            )
            if key in done:
                continue

            skey = stream_key(
                "paper-a/pilot/v1", EXPERIMENT_UUID, "SMOKE", cid, N, replicate, "ideal", "shots"
            )
            sampler = RecordingSampler(Sampler(options={"seed": generator(skey)}), shots=shots)
            iqae = IterativeAmplitudeEstimation(
                epsilon_target=0.05, alpha=0.05, confint_method="beta", sampler=sampler
            )
            try:
                result = iqae.estimate(
                    EstimationProblem(
                        state_preparation=ec.circuit, objective_qubits=[ec.objective_qubit]
                    )
                )
            except Exception as error:
                failed = {
                    "schema_version": SCHEMA_VERSION,
                    "experiment_uuid": EXPERIMENT_UUID,
                    "phase": "SMOKE",
                    "config_id": cid,
                    "n": N,
                    "replicate": replicate,
                    "condition": "ideal",
                    "attempt_kind": "first_planned",
                    "idempotency_key": key,
                    "stream_key": skey,
                    "raw_estimation": None,
                    "raw_confidence_interval": None,
                    "raw_price": None,
                    "presentation_clipped_price": None,
                    "completion_state": "failed",
                    "environment": environment,
                    "error": f"{type(error).__name__}: {error}",
                    "shots": shots,
                    "q_total": q_total,
                    "L": L,
                    "U": U,
                    "rescaling": C_RESCALING,
                }
                resource = {
                    "idempotency_key": key,
                    "provenance": "actual",
                    "invocation_ledger": [asdict(item) for item in sampler.invocations],
                    "known_effective_shots": sum(
                        i.effective_shots or 0 for i in sampler.invocations
                    ),
                    "unknown_shot_invocations": sum(
                        i.effective_shots is None for i in sampler.invocations
                    ),
                    "powers": None,
                    "query_costs": None,
                    "scope": "partial actual ledger; unknown powers/costs are not reconstructed",
                }
                _persist_pair(out, raw_path, res_path, failed, resource)
                raise

            price = to_price(result.estimation, contract.K, U, C_RESCALING, contract.r, contract.T)
            record = {
                "schema_version": SCHEMA_VERSION,
                "experiment_uuid": EXPERIMENT_UUID,
                "phase": "SMOKE",
                "config_id": cid,
                "n": N,
                "replicate": replicate,
                "condition": "ideal",
                "attempt_kind": "first_planned",
                "idempotency_key": key,
                "stream_key": skey,
                "raw_estimation": float(result.estimation),
                "raw_confidence_interval": [float(x) for x in result.confidence_interval],
                "raw_price": price,
                "presentation_clipped_price": presentation_clipped(price),
                "completion_state": "complete",
                "environment": environment,
                "P_BS": ladder.P_BS,
                "P_support": ladder.P_support,
                "P_grid": ladder.P_grid,
                "P_circuit": ladder.P_circuit,
                "e_support": ladder.e_support,
                "e_grid": ladder.e_grid,
                "e_encode": ladder.e_encode,
                "q_total": q_total,
                "L": L,
                "U": U,
                "shots": shots,
                "rescaling": C_RESCALING,
            }
            powers = executed_powers(result.powers, sampler.invocations)
            shot_list = [i.effective_shots for i in sampler.invocations]
            resource = {
                "idempotency_key": key,
                "config_id": cid,
                "n": N,
                "replicate": replicate,
                "invocations": len(sampler.invocations),
                "powers": powers,
                "m_a_logical": m_a_logical(powers),
                "m_a_executed": m_a_executed(powers, shot_list),
                "m_q_executed": m_q_executed(powers, shot_list),
                "max_executed_depth": max_executed_depth(sampler.invocations),
                "shot_weighted_gates": shot_weighted_gates(sampler.invocations),
                "provenance": "actual",
                "invocation_ledger": [asdict(item) for item in sampler.invocations],
            }
            _persist_pair(out, raw_path, res_path, record, resource)

    violations = {r["idempotency_key"]: validate_record(r) for r in read_records(raw_path)}
    _write_state(
        out / "validation.json",
        {"violations": {k: v for k, v in violations.items() if v}, "records": len(violations)},
    )
    if any(violations.values()):
        raise ValueError("raw record validation failed; no COMPLETE marker")
    expected_keys = {
        idempotency_key(EXPERIMENT_UUID, "SMOKE", cid, N, rep, "ideal", f"shots-{shots}")
        for cid in CONFIGS
        for rep in REPLICATES
    }
    if _recover_pairs(out, raw_path, res_path) != expected_keys:
        raise ValueError("unexpected or missing attempt keys; no COMPLETE marker")

    _write_state(
        out / "COMPLETE",
        {
            "raw_sha256": _sha256(raw_path),
            "resources_sha256": _sha256(res_path),
            "validation_sha256": _sha256(out / "validation.json"),
            "environment": environment,
        },
    )
    return {"planned_attempts": planned_attempts, "records": len(violations)}


if __name__ == "__main__":
    print(run_smoke(Path("data/paper_a/smoke")))
