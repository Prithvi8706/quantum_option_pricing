"""Pinned BIQAE source smoke using a local StatevectorSampler, never hardware."""

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import shutil
from pathlib import Path
import subprocess

import numpy as np

from .storage import finish_run


def local_backend(seed=317):
    from qiskit.primitives import StatevectorSampler

    return StatevectorSampler(seed=np.random.default_rng(seed))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, output / "wrapper.py")
    source = checkout / "src/biae.py"
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=checkout, text=True
    ).strip()
    if status:
        raise RuntimeError("BIQAE checkout is not clean")
    if head != "bbd28a3efa659e1c0feec6b86ba13389cb127dbd":
        raise RuntimeError("unexpected BIQAE revision")
    plan = {
        "commit": head,
        "wrapper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "a": 0.17,
        "epsilon": 0.05,
        "alpha": 0.05,
        "shots_per_iteration": 10,
        "seed": 317,
        "scope": "ideal local source smoke, not coverage validation",
        "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
    }
    (output / "planned.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    try:
        from qiskit import QuantumCircuit
        from qiskit_algorithms import EstimationProblem

        spec = importlib.util.spec_from_file_location("pinned_biae", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        np.random.seed(317)
        # A persistent Generator advances across jobs. An integer seed restarts
        # the stream for each pub in this Qiskit version, duplicating batches.
        backend = local_backend()
        ledger = []

        class LocalSampler:
            def run(self, circuits, shots):
                if len(ledger) >= 1000:
                    raise RuntimeError("smoke iteration safety cap")
                job = backend.run(circuits, shots=shots)
                result = job.result()
                counts = result[0].data.c0.get_counts()
                ledger.append({"shots": shots, "counts": counts})

                class Completed:
                    def result(self):
                        return result

                return Completed()

        circuit = QuantumCircuit(1)
        circuit.ry(2 * np.arcsin(np.sqrt(0.17)), 0)
        problem = EstimationProblem(circuit, objective_qubits=[0])
        estimator = module.BayesianIQAE(0.05, 0.05, sampler=LocalSampler())
        result = estimator.estimate(problem, n_shots=10)
        powers = list(map(int, result.powers))
        if len(powers) != len(ledger):
            raise RuntimeError("ledger length mismatch")
        q = sum(k * r["shots"] for k, r in zip(powers, ledger))
        a_cost = sum((2 * k + 1) * r["shots"] for k, r in zip(powers, ledger))
        if q != result.num_oracle_queries:
            raise RuntimeError("Grover cost mismatch")
        record = {
            "estimate": result.estimation,
            "interval": list(map(float, result.confidence_interval)),
            "epsilon_estimated": float(result.epsilon_estimated),
            "powers": powers,
            "ledger": ledger,
            "Grover_queries": q,
            "A_equivalent_queries": a_cost,
            "posterior_params": [list(map(float, p)) for p in result.posterior_params],
            "interval_semantics": (
                "upstream fitted-Beta credible intervals; no new frequentist guarantee"
            ),
        }
        (output / "result.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        finish_run(output)
        print(json.dumps(record), flush=True)
    except Exception as error:
        (output / "failure.json").write_text(
            json.dumps({"type": type(error).__name__, "message": str(error)}, indent=2),
            encoding="utf-8",
        )
        raise


if __name__ == "__main__":
    main()
