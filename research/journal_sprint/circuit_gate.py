"""Actual amplified pricing circuits: logical resources and exact channel smoke tests."""

from .checks import require

import argparse
import json
import os
import shutil
import time

import numpy as np
from qiskit import QuantumCircuit, qpy, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, amplitude_damping_error, depolarizing_error

from .storage import ROOT, finish_run, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import by_id
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import a_calc
from research.paper_a.references import grid_points, grid_probabilities


def amplified_circuit(preparation, objective, depth):
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    result = preparation.copy()
    width = preparation.num_qubits
    for _ in range(depth):
        result.z(objective)
        result.compose(preparation.inverse(), inplace=True)
        result.x(range(width))
        result.h(width - 1)
        result.mcx(list(range(width - 1)), width - 1)
        result.h(width - 1)
        result.x(range(width))
        result.compose(preparation, inplace=True)
    return result


def noise_model(kind, strength):
    model = NoiseModel()
    if kind == "depolarizing":
        model.add_all_qubit_quantum_error(depolarizing_error(strength, 2), ["cx"])
    elif kind == "amplitude_damping":
        model.add_all_qubit_quantum_error(amplitude_damping_error(strength), ["u"])
    else:
        raise ValueError("unknown channel")
    return model


def density_probability(circuit, objective, model=None):
    simulation = circuit.copy()
    simulation.save_density_matrix()
    backend = AerSimulator(method="density_matrix", max_parallel_threads=1)
    result = backend.run(simulation, noise_model=model, shots=None).result()
    if not result.success:
        raise RuntimeError(str(result))
    matrix = np.asarray(result.data(0)["density_matrix"])
    diagonal = np.real(np.diag(matrix))
    if not np.isclose(diagonal.sum(), 1, atol=1e-9) or np.min(diagonal) < -1e-9:
        raise RuntimeError("Invalid density matrix normalization or diagonal")
    mask = (np.arange(len(diagonal)) & (1 << objective)) != 0
    return float(diagonal[mask].sum())


def positive_controls():
    excited = QuantumCircuit(1)
    excited.u(np.pi, 0, np.pi, 0)
    damped = density_probability(excited, 0, noise_model("amplitude_damping", 1))
    pair = QuantumCircuit(2)
    pair.u(np.pi, 0, np.pi, 0)
    pair.u(np.pi, 0, np.pi, 1)
    pair.cx(0, 1)
    depolarized = density_probability(pair, 1, noise_model("depolarizing", 1))
    require(abs(damped) < 1e-9)
    require(abs(depolarized - 0.5) < 1e-9)
    return {"full_damping_excited": damped, "full_cx_depolarization": depolarized}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week3_circuits_v1")
    args = parser.parse_args()
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_W3_CIRCUITS",
            "contracts": ["E001", "E030"],
            "n": [3, 4],
            "scale": [0.125, 0.25],
            "depth": [0, 1, 2],
            "basis": ["u", "cx"],
            "optimization_level": 0,
            "seed_transpiler": 317,
            "noise": {"depolarizing_cx": 0.001, "amplitude_damping_u": 0.005},
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += list((ROOT / "research/paper_a").glob("*.py"))
    sources += [
        ROOT / "research/paper_a/european/circuits.py",
        ROOT / "docs/journal_sprint/PROTOCOL_W3_CIRCUITS.md",
    ]
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    started = time.perf_counter()
    rows = []
    try:
        write_json(path / "controls.json", positive_controls())
        models = {
            kind: noise_model(kind, strength)
            for kind, strength in (("depolarizing", 0.001), ("amplitude_damping", 0.005))
        }
        for kind, model in models.items():
            write_json(path / f"noise_{kind}.json", model.to_dict(serializable=True))
        with (path / "events.jsonl").open("x", encoding="utf-8") as events:
            for cid in ("E001", "E030"):
                c = by_id(cid)
                for n in (3, 4):
                    for scale in (0.125, 0.25):
                        tick = time.perf_counter()
                        b, _ = tighter_bounds_for(c, n, scale)
                        ec = build_european(c, b.lower, b.upper, n, scale)
                        preparation_seconds = time.perf_counter() - tick
                        a = a_calc(
                            grid_probabilities(c, b.lower, b.upper, n),
                            grid_points(b.lower, b.upper, n),
                            c.K,
                            b.upper,
                            scale,
                        )
                        for depth in (0, 1, 2):
                            if time.perf_counter() - started > 900:
                                raise TimeoutError("between-circuit 15-minute limit")
                            key = f"{cid}_n{n}_c{scale}_k{depth}"
                            events.write(json.dumps({"event": "planned", "id": key}) + "\n")
                            events.flush()
                            os.fsync(events.fileno())
                            tick = time.perf_counter()
                            circuit = amplified_circuit(ec.circuit, ec.objective_qubit, depth)
                            construction_seconds = time.perf_counter() - tick
                            tick = time.perf_counter()
                            compiled = transpile(
                                circuit,
                                basis_gates=["u", "cx"],
                                optimization_level=0,
                                seed_transpiler=317,
                            )
                            compile_seconds = time.perf_counter() - tick
                            with (path / f"{key}.qpy").open("xb") as stream:
                                qpy.dump(compiled, stream)
                            tick = time.perf_counter()
                            actual = float(
                                Statevector(compiled).probabilities([ec.objective_qubit])[1]
                            )
                            statevector_seconds = time.perf_counter() - tick
                            predicted = float(np.sin((2 * depth + 1) * np.arcsin(np.sqrt(a))) ** 2)
                            require(abs(actual - predicted) < 1e-9, key)
                            ops = dict(compiled.count_ops())
                            require(set(ops) <= {"u", "cx"})
                            row = {
                                "id": key,
                                "contract": cid,
                                "n": n,
                                "scale": scale,
                                "k": depth,
                                "total_qubits": compiled.num_qubits,
                                "objective": ec.objective_qubit,
                                "depth": compiled.depth(),
                                "gates": ops,
                                "base_probability": a,
                                "predicted": predicted,
                                "ideal": actual,
                                "absolute_difference": abs(actual - predicted),
                                "preparation_seconds": preparation_seconds,
                                "construction_seconds": construction_seconds,
                                "compile_seconds": compile_seconds,
                                "statevector_seconds": statevector_seconds,
                                "dense_statevector_bytes": 16 * 2**compiled.num_qubits,
                                "dense_density_bytes": 16 * 4**compiled.num_qubits,
                                "noise": {},
                            }
                            if n == 3:
                                tick = time.perf_counter()
                                noiseless = density_probability(compiled, ec.objective_qubit)
                                require(abs(noiseless - actual) < 1e-9)
                                row["density_zero_noise"] = noiseless
                                for kind, model in models.items():
                                    probability = density_probability(
                                        compiled, ec.objective_qubit, model
                                    )
                                    row["noise"][kind] = {
                                        "probability": probability,
                                        "shift_from_ideal": probability - actual,
                                        "channel_locations": ops.get(
                                            "cx" if kind == "depolarizing" else "u", 0
                                        ),
                                    }
                                row["density_simulation_seconds"] = time.perf_counter() - tick
                            write_json(path / f"{key}.json", row)
                            rows.append(row)
                            events.write(json.dumps({"event": "completed", "id": key}) + "\n")
                            events.flush()
                            os.fsync(events.fileno())
                            print(key, ops, flush=True)
        write_json(
            path / "summary.json",
            {
                "circuits": len(rows),
                "noise_circuits": sum(bool(r["noise"]) for r in rows),
                "max_ideal_difference": max(r["absolute_difference"] for r in rows),
                "elapsed_seconds": time.perf_counter() - started,
                "rows": rows,
                "scope": "all-to-all logical resources; exact channel probabilities; no hardware",
            },
        )
        finish_run(path)
    except Exception as error:
        write_json(
            path / "failure.json",
            {"type": type(error).__name__, "message": str(error), "completed_circuits": len(rows)},
        )
        raise


if __name__ == "__main__":
    main()
