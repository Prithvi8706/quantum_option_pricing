"""Predeclared encoding/anytime discovery. Synthetic readout, not hardware."""

import argparse
from dataclasses import asdict
from importlib.metadata import version
import json
import math
import os
import shutil
import time

from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_algorithms import EstimationProblem

from .anytime_readout import calibrated_cs
from .calibrated_readout import invert_calibrated
from .exact_payoff import exact_components
from .intervals import price_decision
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities, p_grid


def profiles(contract):
    out = {}
    for encoding in ("linearized", "exact_table"):
        tick = time.monotonic()
        if encoding == "exact_table":
            circuit, bounds, amplitude, _ = exact_components(contract, 6)
            objective = 6
        else:
            bounds, _ = tighter_bounds_for(contract, 6, 0.125)
            ec = build_european(contract, bounds.lower, bounds.upper, 6, 0.125)
            circuit, objective = ec.circuit, ec.objective_qubit
            x = grid_points(bounds.lower, bounds.upper, 6)
            pi = grid_probabilities(contract, bounds.lower, bounds.upper, 6)
            amplitude = a_calc(pi, x, contract.K, bounds.upper, 0.125)
        problem = EstimationProblem(circuit, objective_qubits=[objective])
        depths = {}
        for k in (0, 1, 2):
            qc = circuit.copy()
            if k:
                qc.compose(problem.grover_operator.power(k), inplace=True)
            actual = float(Statevector(qc).probabilities([objective])[1])
            predicted = math.sin((2 * k + 1) * math.asin(math.sqrt(amplitude))) ** 2
            if abs(actual - predicted) > 1e-9:
                raise ValueError("amplified circuit mismatch")
            compiled = transpile(
                qc, basis_gates=["u", "cx"], optimization_level=1, seed_transpiler=1729
            )
            depths[str(k)] = dict(
                gates=dict(compiled.count_ops()),
                depth=compiled.depth(),
                qubits=compiled.num_qubits,
                amplitude_error=abs(actual - predicted),
            )
        out[encoding] = dict(
            bounds=asdict(bounds),
            amplitude=amplitude,
            profiles=depths,
            construction_and_validation_seconds=time.monotonic() - tick,
        )
    return out


def acquisition(contract, encoding, profile, guard, axis, rep, old_cx):
    b = profile["bounds"]
    bias = b["support"] + b["grid"] + b["encoding"]
    cx = profile["profiles"]["0"]["gates"]["cx"]
    cap = 32768 if axis == "shots" else (32768 * old_cx) // cx
    identity = dict(contract=contract.id, encoding=encoding, guard=guard, axis=axis, rep=rep)
    truth = black_scholes_call(contract.S0, contract.K, contract.r, contract.sigma, contract.T)
    if bias >= 1:
        return [
            dict(
                **identity,
                inference=inference,
                status="refused",
                shots=0,
                calibration_shots=0,
                pricing_cx=0,
                contains=None,
                erroneous=False,
            )
            for inference in ("fixed_cp", "anytime_cs")
        ]
    key = ("rescue_v1", contract.id, encoding, str(guard), axis, rep)
    cal = rng_for(*key, "calibration").binomial(16384, [0.02, 0.07]).tolist()
    q = 0.02 + 0.91 * profile["amplitude"]
    rng = rng_for(*key, "validation")
    looks = []
    n = 1024
    while n < cap:
        looks.append(n)
        n *= 2
    looks.append(cap)
    count = previous = 0
    stopped = None
    trace = []

    def record(decision, used, inference):
        interval = decision["interval"]
        midpoint = sum(interval) / 2 if interval is not None else None
        return dict(
            **identity,
            inference=inference,
            **decision,
            shots=used,
            calibration_shots=32768,
            pricing_cx=used * cx,
            pricing_A_equivalents=used,
            total_shots=used + 32768,
            contains=bool(interval is not None and interval[0] <= truth <= interval[1]),
            erroneous=bool(decision["status"] == "precision_met" and abs(midpoint - truth) > 1),
            midpoint_error=None if midpoint is None else abs(midpoint - truth),
            cap=cap,
            bias=bias,
            calibration_errors=cal,
        )

    for used in looks:
        count += int(rng.binomial(used - previous, q))
        previous = used
        trace.append([used, count])
        if stopped is None:
            cs = calibrated_cs([count], [used], [0], cal, [16384, 16384], guard=guard)
            decision = price_decision(cs, b["sensitivity"], b["offset"], bias)
            if decision["status"] == "precision_met" or used == cap:
                stopped = record(decision, used, "anytime_cs")
    confidence, _ = invert_calibrated(
        [count], [cap], [0], cal, [16384, 16384], transfer_bounds=(guard, guard)
    )
    fixed = record(price_decision(confidence, b["sensitivity"], b["offset"], bias), cap, "fixed_cp")
    # Shared path retained once: not two independent acquisitions.
    fixed["synthetic_path"] = trace
    return [fixed, stopped]


def summarize(rows):
    cells = []
    for contract in C6:
        for guard in (0.0, 0.003, 0.03):
            for axis in ("shots", "cx"):
                for inference in ("fixed_cp", "anytime_cs"):
                    group = [
                        r
                        for r in rows
                        if r["contract"] == contract
                        and r["guard"] == guard
                        and r["axis"] == axis
                        and r["inference"] == inference
                    ]
                    rates = {
                        e: sum(r["status"] == "precision_met" for r in group if r["encoding"] == e)
                        / 30
                        for e in ("linearized", "exact_table")
                    }
                    cells.append(
                        dict(
                            contract=contract,
                            guard=guard,
                            axis=axis,
                            inference=inference,
                            delivery=rates,
                            gain=rates["exact_table"] - rates["linearized"],
                        )
                    )
    promoted = {}
    for inference in ("fixed_cp", "anytime_cs"):
        improved = [
            c
            for c in C6
            if c != "E001"
            and all(
                next(
                    r["gain"]
                    for r in cells
                    if r["contract"] == c
                    and r["guard"] == 0
                    and r["axis"] == axis
                    and r["inference"] == inference
                )
                > 0
                for axis in ("shots", "cx")
            )
        ]
        promoted[inference] = improved
    return dict(
        inference_rows=len(rows),
        refused=sum(r["status"] == "refused" for r in rows),
        declared=sum(r["status"] == "precision_met" for r in rows),
        interval_misses=sum(r["contains"] is False for r in rows),
        erroneous_declarations=sum(r["erroneous"] for r in rows),
        improved_non_e001_both_axes=promoted,
        cells=cells,
        caveat="shared-data inference arms, unpaired encoding contrasts, discovery only",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 1_000_000_000:
        raise RuntimeError("need 1 GB free")
    sources = sorted((ROOT / "research/journal_sprint").glob("*.py"))
    sources += sorted((ROOT / "research/paper_a").rglob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_RESCUE_V1.md"]
    sources = [p for p in sources if "tests" not in p.parts]
    output = start_run(
        args.output,
        dict(
            protocol="PROTOCOL_RESCUE_V1",
            replicates=30,
            packages={
                p: version(p)
                for p in ("qiskit-terra", "qiskit-algorithms", "qiskit-finance", "mpmath")
            },
            sources={str(p.relative_to(ROOT)): sha256(p) for p in sources},
        ),
    )
    rows = []
    tick = time.monotonic()
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(p) != sha256(target):
                raise ValueError("source drift")
        all_profiles = {}
        for name in C6:
            if time.monotonic() - tick > 1800:
                raise RuntimeError("elapsed limit")
            all_profiles[name] = profiles(by_id(name))
            write_json(output / f"profile_{name}.json", all_profiles[name])
            print(f"profiled {name}", flush=True)
        classical = []
        for name in C6:
            c = by_id(name)
            b = all_profiles[name]["exact_table"]["bounds"]
            before = time.perf_counter()
            value = p_grid(c, b["lower"], b["upper"], 6)
            classical.append(
                dict(
                    contract=name,
                    terms=64,
                    value=value,
                    elapsed_seconds=time.perf_counter() - before,
                    continuous_error=abs(value - black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)),
                    bound=b["support"] + b["grid"],
                )
            )
        write_json(output / "classical.json", classical)
        with (output / "records.jsonl").open("x", encoding="utf-8") as stream:
            for name in C6:
                c = by_id(name)
                p = all_profiles[name]
                for guard in (0.0, 0.003, 0.03):
                    for axis in ("shots", "cx"):
                        for encoding in ("linearized", "exact_table"):
                            for rep in range(30):
                                if time.monotonic() - tick > 1800:
                                    raise RuntimeError("elapsed limit")
                                batch = acquisition(
                                    c,
                                    encoding,
                                    p[encoding],
                                    guard,
                                    axis,
                                    rep,
                                    p["linearized"]["profiles"]["0"]["gates"]["cx"],
                                )
                                rows.extend(batch)
                                for row in batch:
                                    stream.write(json.dumps(row, allow_nan=False) + "\n")
                                stream.flush()
                                os.fsync(stream.fileno())
                print(f"sampled {name}", flush=True)
        summary = summarize(rows)
        write_json(output / "summary.json", summary)
        finish_run(output)
        print(json.dumps({k: v for k, v in summary.items() if k != "cells"}))
    except Exception as error:
        write_json(output / "failure.json", dict(completed_rows=len(rows), error=str(error)))
        raise


if __name__ == "__main__":
    main()
