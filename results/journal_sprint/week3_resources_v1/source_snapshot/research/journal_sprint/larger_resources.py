"""Larger-register logical compilation with an explicit initial smoke gate."""

import shutil
import time

import numpy as np
from qiskit import qpy, transpile
from qiskit.quantum_info import Statevector

from .circuit_gate import amplified_circuit
from .storage import ROOT, finish_run, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import by_id
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import a_calc
from research.paper_a.references import grid_points, grid_probabilities


def main():
    matrix = [
        (cid, n, scale, k)
        for cid in ("E001", "E014", "E025", "E049")
        for scale in ((0.125, 0.25) if cid == "E001" else (0.125,))
        for n in (5, 6)
        for k in (0, 1)
    ]
    path = start_run(
        "results/journal_sprint/week3_resources_v1",
        {
            "protocol": "PROTOCOL_W3_RESOURCES",
            "matrix": matrix,
            "basis": ["u", "cx"],
            "optimization_level": 0,
            "seed": 317,
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += list((ROOT / "research/paper_a").rglob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_W3_RESOURCES.md"]
    for source in sources:
        target = path / "source_snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    started = time.perf_counter()
    rows = []
    try:
        for cid, n, scale, k in matrix:
            if time.perf_counter() - started > 900:
                raise TimeoutError("between-case 15-minute limit")
            key = f"{cid}_n{n}_c{scale}_k{k}"
            write_json(path / f"{key}_planned.json", {"id": key})
            tick = time.perf_counter()
            contract = by_id(cid)
            bound, _ = tighter_bounds_for(contract, n, scale)
            ec = build_european(contract, bound.lower, bound.upper, n, scale)
            compiled = transpile(
                amplified_circuit(ec.circuit, ec.objective_qubit, k),
                basis_gates=["u", "cx"],
                optimization_level=0,
                seed_transpiler=317,
            )
            compile_seconds = time.perf_counter() - tick
            storage = 16 * 2**compiled.num_qubits
            if storage > 16 * 1024**2:
                raise MemoryError("state array exceeds 16 MiB smoke budget")
            a = a_calc(
                grid_probabilities(contract, bound.lower, bound.upper, n),
                grid_points(bound.lower, bound.upper, n),
                contract.K,
                bound.upper,
                scale,
            )
            predicted = float(np.sin((2 * k + 1) * np.arcsin(np.sqrt(a))) ** 2)
            actual = float(Statevector(compiled).probabilities([ec.objective_qubit])[1])
            if abs(actual - predicted) > 1e-9:
                raise RuntimeError(f"ideal amplification mismatch: {key}")
            elapsed = time.perf_counter() - tick
            if not rows and elapsed > 120:
                raise TimeoutError("initial smoke exceeds 120 seconds")
            with (path / f"{key}.qpy").open("xb") as stream:
                qpy.dump(compiled, stream)
            row = {
                "id": key,
                "contract": cid,
                "n": n,
                "scale": scale,
                "k": k,
                "total_qubits": compiled.num_qubits,
                "gates": dict(compiled.count_ops()),
                "depth": compiled.depth(),
                "compile_seconds": compile_seconds,
                "case_seconds": elapsed,
                "dense_statevector_bytes": storage,
                "ideal": actual,
                "predicted": predicted,
                "absolute_difference": abs(actual - predicted),
                "bound": vars(bound),
            }
            write_json(path / f"{key}.json", row)
            rows.append(row)
            print(key, row["gates"], flush=True)
        write_json(
            path / "summary.json",
            {
                "rows": rows,
                "seconds": time.perf_counter() - started,
                "scope": "logical, ideal only",
            },
        )
        finish_run(path)
    except Exception as error:
        write_json(path / "failure.json", {"error": str(error), "completed": len(rows)})
        raise


if __name__ == "__main__":
    main()
