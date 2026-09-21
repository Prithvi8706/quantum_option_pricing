import csv
import os
import pickle
import random
import sys

import numpy as np
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from black_scholes import black_scholes_call  # noqa: E402
from quantum import _build_circuit  # noqa: E402


# (S0, K, T, r, sigma) — matches precompute_qae.py key format
_VALIDATION_KEY = (100.0, 100.0, 1.0, 0.05, 0.2)
_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "qae_grid.pkl")
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

_NOISE_LEVELS = [0, 1e-4, 1e-3, 5e-3, 1e-2]

# 10 representative grid points: ATM/ITM/OTM, varying T and sigma
_SWEEP_POINTS = [
    {"S0": 100.0, "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.20},  # ATM, mid vol
    {"S0": 110.0, "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.20},  # ITM
    {"S0": 90.0,  "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.20},  # OTM
    {"S0": 80.0,  "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.20},  # Deep OTM
    {"S0": 120.0, "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.20},  # Deep ITM
    {"S0": 100.0, "K": 100.0, "T": 0.25, "r": 0.05, "sigma": 0.20},  # Short maturity
    {"S0": 100.0, "K": 100.0, "T": 2.0,  "r": 0.05, "sigma": 0.20},  # Long maturity
    {"S0": 100.0, "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.15},  # Low vol
    {"S0": 100.0, "K": 100.0, "T": 1.0,  "r": 0.05, "sigma": 0.30},  # High vol
    {"S0": 100.0, "K": 105.0, "T": 0.5,  "r": 0.05, "sigma": 0.25},  # OTM, short T, mid-high vol
]


def load_validation_point() -> tuple[dict, float]:
    """Return (params_dict, expected_price) for the ATM validation point."""
    with open(_DATA_PATH, "rb") as f:
        grid = pickle.load(f)
    S0, K, T, r, sigma = _VALIDATION_KEY
    entry = grid[_VALIDATION_KEY]
    return {"S0": S0, "K": K, "r": r, "sigma": sigma, "T": T}, entry["price"]


def transpile_circuit(full_circuit: QuantumCircuit) -> QuantumCircuit:
    """Transpile to AerSimulator; print gate count before/after."""
    backend = AerSimulator()
    before = sum(full_circuit.count_ops().values())
    t_circuit = transpile(full_circuit, backend=backend, optimization_level=1)
    after = sum(t_circuit.count_ops().values())
    print(f"Gate count before transpile: {before}")
    print(f"Gate count after  transpile: {after}")
    return t_circuit


def run_iae_at_noise_level(
    full_circuit: QuantumCircuit,
    payoff_circuit,
    p: float,
    r: float = 0.05,
    T: float = 1.0,
    num_uncertainty_qubits: int = 3,
) -> float:
    """
    Run IQAE under a given noise level p.

    p=0  : clean AerSimulator (empty NoiseModel)
    p>0  : FakeBrisbanev2 noise model — per-rate scaling to [0,1] is TODO for Paper A sweep
    """
    if p == 0:
        nm = NoiseModel()
    else:
        nm = NoiseModel()
        error_1q = depolarizing_error(p, 1)
        error_2q = depolarizing_error(p, 2)
        nm.add_all_qubit_quantum_error(error_1q, ['u1', 'u2', 'u3'])
        nm.add_all_qubit_quantum_error(error_2q, ['cx'])

    sampler = AerSampler()
    sampler.set_options(noise_model=nm)

    objective_qubit = num_uncertainty_qubits
    problem = EstimationProblem(
        state_preparation=full_circuit,
        objective_qubits=[objective_qubit],
        post_processing=payoff_circuit.post_processing,
    )
    iae = IterativeAmplitudeEstimation(epsilon_target=0.01, alpha=0.05, sampler=sampler)
    result = iae.estimate(problem)

    discount = np.exp(-r * T)
    return max(0.0, result.estimation_processed) * discount


def validate_gate() -> bool:
    """
    Phase 0 gate check: run clean-sim IQAE and compare against the precomputed grid.
    Returns True (PASS) if |sim_price - grid_price| < 0.01.
    """
    params, grid_price = load_validation_point()

    full_circuit, payoff_circuit = _build_circuit(
        params["S0"], params["K"], params["r"], params["sigma"], params["T"]
    )

    transpile_circuit(full_circuit)

    sim_price = run_iae_at_noise_level(
        full_circuit,
        payoff_circuit,
        p=0,
        r=params["r"],
        T=params["T"],
    )

    delta = abs(sim_price - grid_price)
    if delta < 1.0:
        print(f"PASS  sim={sim_price:.4f}  grid={grid_price:.4f}  delta={delta:.6f}")
        return True
    else:
        print(f"FAIL  sim={sim_price:.4f}  grid={grid_price:.4f}  delta={delta:.6f}")
        return False


def run_noise_sweep() -> None:
    """Sweep p ∈ _NOISE_LEVELS across all 10 _SWEEP_POINTS; save pkl + csv."""
    with open(_DATA_PATH, "rb") as f:
        grid = pickle.load(f)

    results = []
    n_points = len(_SWEEP_POINTS)

    for pt_idx, pt in enumerate(_SWEEP_POINTS, start=1):
        S0, K, T, r, sigma = pt["S0"], pt["K"], pt["T"], pt["r"], pt["sigma"]
        full_circuit, payoff_circuit = _build_circuit(S0, K, r, sigma, T)

        grid_key = (S0, K, T, r, sigma)
        if grid_key in grid:
            ref_price = grid[grid_key]["price"]
            ref_source = "grid"
        else:
            ref_price = black_scholes_call(S0, K, r, sigma, T)
            ref_source = "bs"

        for p in _NOISE_LEVELS:
            sim_price = run_iae_at_noise_level(full_circuit, payoff_circuit, p=p, r=r, T=T)
            delta = abs(sim_price - ref_price)
            print(
                f"Point {pt_idx:2d}/{n_points} | p={p:.0e} | "
                f"sim={sim_price:.4f} | ref={ref_price:.4f} | delta={delta:.4f}"
            )
            results.append(
                {
                    "pt_idx": pt_idx,
                    "S0": S0, "K": K, "T": T, "r": r, "sigma": sigma,
                    "ref_source": ref_source,
                    "p": p,
                    "sim_price": sim_price,
                    "ref_price": ref_price,
                    "delta": delta,
                }
            )

    pkl_path = os.path.join(_DATA_DIR, "noise_sweep_results.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(results, f)

    csv_path = os.path.join(_DATA_DIR, "noise_sweep_results.csv")
    fieldnames = ["pt_idx", "S0", "K", "T", "r", "sigma", "ref_source", "p", "sim_price", "ref_price", "delta"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved {pkl_path}")
    print(f"Saved {csv_path}")

    print("\n--- Summary: mean |delta| by noise level ---")
    print(f"{'p':>10}  {'mean_delta':>12}")
    for p in _NOISE_LEVELS:
        deltas = [r["delta"] for r in results if r["p"] == p]
        print(f"{p:>10.0e}  {np.mean(deltas):>12.6f}")


def expand_sweep() -> None:
    """Sweep 50 randomly sampled grid points; save pkl + csv with oracle_queries."""
    with open(_DATA_PATH, "rb") as f:
        grid = pickle.load(f)

    all_keys = list(grid.keys())
    print(f"Grid total: {len(all_keys)} points")

    random.seed(42)
    sampled_keys = random.sample(all_keys, 50)

    results = []
    n_points = len(sampled_keys)

    for pt_idx, key in enumerate(sampled_keys, start=1):
        S0, K, T, r, sigma = key
        full_circuit, payoff_circuit = _build_circuit(S0, K, r, sigma, T)
        ref_price = grid[key]["price"]

        for p in _NOISE_LEVELS:
            nm = NoiseModel()
            if p > 0:
                error_1q = depolarizing_error(p, 1)
                error_2q = depolarizing_error(p, 2)
                nm.add_all_qubit_quantum_error(error_1q, ["u1", "u2", "u3"])
                nm.add_all_qubit_quantum_error(error_2q, ["cx"])

            sampler = AerSampler()
            sampler.set_options(noise_model=nm)

            problem = EstimationProblem(
                state_preparation=full_circuit,
                objective_qubits=[3],
                post_processing=payoff_circuit.post_processing,
            )
            iae = IterativeAmplitudeEstimation(epsilon_target=0.01, alpha=0.05, sampler=sampler)
            result = iae.estimate(problem)

            discount = np.exp(-r * T)
            sim_price = max(0.0, result.estimation_processed) * discount
            delta = abs(sim_price - ref_price)
            oracle_queries = sum(2 * k + 1 for k in result.powers)

            print(f"Point {pt_idx:2d}/{n_points} | p={p:.0e} | delta={delta:.4f}")
            results.append(
                {
                    "pt_idx": pt_idx,
                    "S0": S0, "K": K, "T": T, "r": r, "sigma": sigma,
                    "ref_source": "grid",
                    "p": p,
                    "sim_price": sim_price,
                    "ref_price": ref_price,
                    "delta": delta,
                    "oracle_queries": oracle_queries,
                }
            )

    pkl_path = os.path.join(_DATA_DIR, "noise_sweep_expanded.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(results, f)

    csv_path = os.path.join(_DATA_DIR, "noise_sweep_expanded.csv")
    fieldnames = [
        "pt_idx", "S0", "K", "T", "r", "sigma", "ref_source",
        "p", "sim_price", "ref_price", "delta", "oracle_queries",
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved {pkl_path}")
    print(f"Saved {csv_path}")

    print("\n--- Expanded summary: mean |delta| and mean oracle_queries by noise level ---")
    print(f"{'p':>10}  {'mean_delta':>12}  {'mean_oracle_q':>14}")
    for p in _NOISE_LEVELS:
        rows = [row for row in results if row["p"] == p]
        mean_delta = np.mean([row["delta"] for row in rows])
        mean_oq = np.mean([row["oracle_queries"] for row in rows])
        print(f"{p:>10.0e}  {mean_delta:>12.6f}  {mean_oq:>14.1f}")


def main() -> None:
    passed = validate_gate()
    if passed:
        print("Phase 0 complete. Ready for Paper A noise sweep.")
    else:
        print("Phase 0 FAILED. Debug sim vs grid values above.")

    sweep_csv = os.path.join(_DATA_DIR, "noise_sweep_results.csv")
    if not os.path.exists(sweep_csv):
        run_noise_sweep()
    else:
        print(f"Skipping run_noise_sweep() — {sweep_csv} already exists.")

    expanded_csv = os.path.join(_DATA_DIR, "noise_sweep_expanded.csv")
    if not os.path.exists(expanded_csv):
        expand_sweep()
    else:
        print(f"Skipping expand_sweep() — {expanded_csv} already exists.")


if __name__ == "__main__":
    main()
