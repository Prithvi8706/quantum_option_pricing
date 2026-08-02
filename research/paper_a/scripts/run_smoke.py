"""Tiny end-to-end experiment: 2 configs, n=3, 2 seeds, ideal only.

Exercises config -> references -> circuit -> recorded IQAE -> raw records ->
resources -> validation -> COMPLETE, so the pipeline is proven before any
full experiment runs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation

from research.paper_a.benchmark import by_id
from research.paper_a.environment import capture_environment
from research.paper_a.errors import deterministic_ladder
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import C_RESCALING, presentation_clipped, to_price
from research.paper_a.recording import RecordingSampler
from research.paper_a.references import support_bounds
from research.paper_a.resources import (
    executed_powers, m_a_executed, m_a_logical, m_q_executed,
    max_executed_depth, shot_weighted_gates,
)
from research.paper_a.schema import (
    SCHEMA_VERSION, append_record, idempotency_key, read_records,
    validate_record,
)
from research.paper_a.streams import stream_key

CONFIGS = ("E001", "E025")
REPLICATES = (0, 1)
Q_TOTAL = 1e-4
N = 3
EXPERIMENT_UUID = "smoke-0001"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_smoke(output_dir, shots: int = 512) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_path, res_path = out / "raw.jsonl", out / "resources.jsonl"

    done = {r["idempotency_key"] for r in read_records(raw_path)} \
        if raw_path.exists() else set()
    environment = capture_environment()
    planned_attempts = 0

    for cid in CONFIGS:
        contract = by_id(cid)
        L, U = support_bounds(contract, Q_TOTAL)
        ladder = deterministic_ladder(contract, Q_TOTAL, N, C_RESCALING)
        ec = build_european(contract, L, U, N, C_RESCALING)

        for replicate in REPLICATES:
            # Counts planned config x replicate combinations, including ones
            # skipped below because they were already done.
            planned_attempts += 1
            key = idempotency_key(EXPERIMENT_UUID, "SMOKE", cid, N, replicate,
                                  "ideal", "shots")
            if key in done:
                continue

            skey = stream_key("paper-a/pilot/v1", EXPERIMENT_UUID, "SMOKE",
                              cid, N, replicate, "ideal", "shots")
            sampler = RecordingSampler(Sampler(options={"seed": replicate}),
                                       shots=shots)
            iqae = IterativeAmplitudeEstimation(
                epsilon_target=0.05, alpha=0.05, confint_method="beta",
                sampler=sampler)
            result = iqae.estimate(EstimationProblem(
                state_preparation=ec.circuit,
                objective_qubits=[ec.objective_qubit]))

            price = to_price(result.estimation, contract.K, U, C_RESCALING,
                             contract.r, contract.T)
            record = {
                "schema_version": SCHEMA_VERSION,
                "experiment_uuid": EXPERIMENT_UUID, "phase": "SMOKE",
                "config_id": cid, "n": N, "replicate": replicate,
                "condition": "ideal", "attempt_kind": "first_planned",
                "idempotency_key": key, "stream_key": skey,
                "raw_estimation": float(result.estimation),
                "raw_confidence_interval": [float(x) for x in
                                            result.confidence_interval],
                "raw_price": price,
                "presentation_clipped_price": presentation_clipped(price),
                "completion_state": "complete", "environment": environment,
                "P_BS": ladder.P_BS, "P_support": ladder.P_support,
                "P_grid": ladder.P_grid, "P_circuit": ladder.P_circuit,
                "e_support": ladder.e_support, "e_grid": ladder.e_grid,
                "e_encode": ladder.e_encode,
            }
            append_record(raw_path, record)

            powers = executed_powers(result.powers, sampler.invocations)
            shot_list = [i.effective_shots for i in sampler.invocations]
            append_record(res_path, {
                "idempotency_key": key, "config_id": cid, "n": N,
                "replicate": replicate,
                "invocations": len(sampler.invocations),
                "powers": powers,
                "m_a_logical": m_a_logical(powers),
                "m_a_executed": m_a_executed(powers, shot_list),
                "m_q_executed": m_q_executed(powers, shot_list),
                "max_executed_depth": max_executed_depth(sampler.invocations),
                "shot_weighted_gates": shot_weighted_gates(
                    sampler.invocations),
                "provenance": "actual",
            })

    violations = {r["idempotency_key"]: validate_record(r)
                  for r in read_records(raw_path)}
    (out / "validation.json").write_text(json.dumps(
        {"violations": {k: v for k, v in violations.items() if v},
         "records": len(violations)}, indent=2))

    (out / "COMPLETE").write_text(json.dumps({
        "raw_sha256": _sha256(raw_path),
        "resources_sha256": _sha256(res_path),
        "validation_sha256": _sha256(out / "validation.json"),
        "environment": environment,
    }, indent=2))
    return {"planned_attempts": planned_attempts, "records": len(violations)}


if __name__ == "__main__":
    print(run_smoke(Path("data/paper_a/smoke")))
