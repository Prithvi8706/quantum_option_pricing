"""Exclusive bounded integration/ablation; no automatic confirmation promotion."""

import argparse
from dataclasses import replace
from datetime import datetime, timezone
import json
import math
import platform
from pathlib import Path
import subprocess
import time

import numpy as np
import scipy
from scipy.special import ndtr
from qiskit import transpile

from .asian_basket import Basket
from .asian_encoding import grid
from .combined_representation import (
    fwht, parity_matrix, discovery_vector, quantum_discovery, rank_words,
    fit_control, greedy_words, mps_diagnostic,
)
from .combined_qsp import synthesize, response, qsp_circuit, lcu_circuit, hadamard_mean, weighted_depth
from .storage import ROOT, sha256, write_json, rng_for


CONFIG = dict(normal_bits=2, cutoff=4, training_paths=128, feature_count=4,
              strikes=[90, 95, 100, 105, 110], discovery_strike=100,
              shots=[256, 1024], repetitions=8, degrees=[4, 8],
              reuse=[1, 5, 25, 100], mps_bonds=[1, 2, 4, 8],
              scope="finite development with paid tables; no quantum advantage claim")
SOURCES = tuple("research/journal_sprint/"+name for name in (
    "combined_representation.py", "combined_qsp.py", "run_combined_development.py",
    "asian_encoding.py", "asian_basket.py", "price_contract.py", "encoding_decision.py",
    "storage.py")) + ("docs/journal_sprint/COMBINED_DEVELOPMENT_PROTOCOL.md",)


def circuit_cost(circuit):
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=1, seed_transpiler=717)
    return dict(qubits=compiled.num_qubits, u=int(compiled.count_ops().get("u", 0)),
                cx=int(compiled.count_ops().get("cx", 0)), depth=compiled.depth(),
                illustrative_gate_weighted_depth=weighted_depth(compiled, {"u": 1, "cx": 10}),
                duration_units="illustrative u=1,cx=10; not measured hardware time")


def serial_fit(fit):
    return {k: v.tolist() if isinstance(v, np.ndarray) else v
            for k, v in fit.items() if k != "residual"}


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES}
    import qiskit
    write_json(output/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               qiskit=qiskit.__version__, started_utc=datetime.now(timezone.utc).isoformat(),
               git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()))
    try:
        basket = Basket(2, 2, 100)
        data = grid(basket, CONFIG["normal_bits"], CONFIG["cutoff"])
        weights, n = data["weights"], len(data["weights"])
        parities = parity_matrix(8)
        training = np.zeros(n, dtype=bool)
        training[rng_for("combined-v1", "training").choice(n, CONFIG["training_paths"], replace=False)] = True
        vector = discovery_vector(data["raw"], weights, training)
        start = time.perf_counter()
        classical_scores = fwht(vector)**2/n
        exact_words = rank_words(classical_scores, CONFIG["feature_count"])
        fwht_seconds = time.perf_counter()-start
        start = time.perf_counter()
        greedy = greedy_words(data["raw"], weights, training, parities, CONFIG["feature_count"])
        greedy_seconds = time.perf_counter()-start
        discovery, probabilities, discrepancy = quantum_discovery(vector)
        discovery_cost = circuit_cost(discovery)
        selections = [dict(method="classical_fwht", words=exact_words),
                      dict(method="classical_full_pool_greedy", words=greedy)]
        for shots in CONFIG["shots"]:
            for replicate in range(CONFIG["repetitions"]):
                counts = rng_for("combined-v1", "fourier-shots", shots, replicate).multinomial(shots, probabilities/probabilities.sum())
                selections.append(dict(method="quantum_fourier_sampling", shots=shots, replicate=replicate,
                                       words=rank_words(counts, CONFIG["feature_count"]), counts=counts.tolist()))
        write_json(output/"discovery.json", dict(training_indices=np.flatnonzero(training).tolist(),
                   selections=selections, discovery_cost=discovery_cost, fwht_seconds=fwht_seconds,
                   greedy_seconds=greedy_seconds, statevector_error=discrepancy,
                   training_label_evaluations=CONFIG["training_paths"], state_preparation_table_entries=n,
                   full_pool_classical_available=True, quantum_hardware_used=False))
        records = []
        for strike in CONFIG["strikes"]:
            strike_data = grid(replace(basket, strike=strike), CONFIG["normal_bits"], CONFIG["cutoff"])
            payoff = strike_data["raw"]
            raw_sd = float(np.sqrt(weights @ (payoff-weights @ payoff)**2))
            geometric = fit_control(payoff, weights, training, strike_data["control"][:, None])
            records.append(dict(strike=strike, method="classical_geometric_control", raw_sd=raw_sd,
                                **serial_fit(geometric)))
            for selection in selections:
                fit = fit_control(payoff, weights, training, parities[:, selection["words"]])
                records.append(dict(strike=strike, **{k: v for k, v in selection.items() if k != "counts"},
                                    raw_sd=raw_sd, **serial_fit(fit)))
        write_json(output/"representations.json", dict(records=records,
                   scope="finite-model expectations; fit on training indices, holdout RMSE on other indices; no continuous certificate"))
        print("Representation ablations acquired; synthesizing QSP and checking circuits", flush=True)
        qsp_records, syntheses = [], []
        discount = math.exp(-basket.rate*basket.maturity)
        for degree in CONFIG["degrees"]:
            plan = synthesize(degree)
            syntheses.append(plan)
            if not plan["fit_accepted"]:
                continue
            for strike in CONFIG["strikes"]:
                logs = data["model"]["means"]+data["normals"] @ data["model"]["factor"].T
                amount = np.exp(logs).mean(axis=1)-strike
                radius = float(np.max(abs(amount)))
                signal, factor = amount/radius, discount*radius/2
                approximation = factor*(signal+plan["abs_rescale"]*response(signal, plan["phases"]).real)
                true_payoff = discount*np.maximum(amount, 0)
                raw_beta = factor*(1+plan["abs_rescale"])
                row = dict(strike=strike, degree=degree, signal_radius=radius, raw_lcu_beta=raw_beta,
                           actual_finite_price=float(weights @ true_payoff), qsp_finite_price=float(weights @ approximation),
                           observed_price_bias=float(weights @ (approximation-true_payoff)),
                           observed_uniform_payoff_error=float(np.max(abs(approximation-true_payoff))),
                           analytic_truncation_price_expression=factor*plan["analytic_truncation_expression"],
                           phase_error_certified=False, signal_table_entries=n)
                if strike == CONFIG["discovery_strike"]:
                    actual, hadamard = hadamard_mean(qsp_circuit(signal, plan["phases"]), weights)
                    expected = float(weights @ response(signal, plan["phases"]).real)
                    if abs(actual-expected) > 1e-8:
                        raise ArithmeticError("actual QSP Hadamard test mismatch")
                    row.update(hadamard_expectation=actual, hadamard_error=abs(actual-expected),
                               actual_qsp_hadamard_cost=circuit_cost(hadamard))
                qsp_records.append(row)
        write_json(output/"qsp.json", dict(syntheses=syntheses, records=qsp_records))
        if not any(plan["fit_accepted"] for plan in syntheses):
            raise ArithmeticError("all bounded QSP synthesis attempts failed")
        print("QSP checks passed; testing coherent combination on a 16-path circuit", flush=True)
        small = grid(basket, 1, CONFIG["cutoff"])
        small_features = parity_matrix(4)
        mask = np.arange(16) < 8
        small_vector = discovery_vector(small["raw"], small["weights"], mask)
        _, small_probabilities, _ = quantum_discovery(small_vector)
        small_counts = rng_for("combined-v1", "small-lcu").multinomial(1024, small_probabilities/small_probabilities.sum())
        small_words = rank_words(small_counts, 4)
        control = fit_control(small["raw"], small["weights"], mask, small_features[:, small_words])
        amount = np.exp(small["model"]["means"]+small["normals"] @ small["model"]["factor"].T).mean(axis=1)-100
        radius = float(np.max(abs(amount)))
        factor = discount*radius/2
        plan = next(p for p in syntheses if p["fit_accepted"])
        lcu, beta = lcu_circuit(amount/radius, plan["phases"], factor, plan["abs_rescale"], control["coefficients"], small_words)
        measured, combined_circuit = hadamard_mean(lcu, small["weights"])
        approximation = factor*(amount/radius+plan["abs_rescale"]*response(amount/radius, plan["phases"]).real)
        reconstructed = control["control_expectation"]+beta*measured
        expected = float(small["weights"] @ approximation)
        if abs(reconstructed-expected) > 1e-7:
            raise ArithmeticError("combined LCU/control expectation mismatch")
        write_json(output/"integrated_lcu.json", dict(normal_bits=1, paths=16, words=small_words,
                   beta=beta, raw_beta=factor*(1+plan["abs_rescale"]),
                   measured_hadamard_mean=measured, reconstructed_price=reconstructed, expected_qsp_price=expected,
                   true_finite_price=float(small["weights"] @ small["raw"]),
                   composition_error=abs(reconstructed-expected), cost=circuit_cost(combined_circuit),
                   quantum_hardware_used=False, full_statevector=True, scalable_signal=False))
        integrated_beta_ratio = beta/(factor*(1+plan["abs_rescale"]))
        edges = np.linspace(-4, 4, 1025)
        marginal = np.diff(ndtr(edges))
        marginal /= marginal.sum()
        write_json(output/"mps.json", dict(normal_bits=10, rows=[mps_diagnostic(np.sqrt(marginal), bond) for bond in CONFIG["mps_bonds"]],
                   scope="classical tensor compression diagnostic only; no loader circuit/certificate"))
        combined, reuse = [], []
        for qsp in qsp_records:
            for record in records:
                if record["strike"] != qsp["strike"] or record["method"] == "classical_geometric_control":
                    continue
                beta = qsp["raw_lcu_beta"]+record["control_l1"]
                residual_mean = qsp["qsp_finite_price"]-record["control_expectation"]
                # One controlled-LCU Hadamard outcome is +/-1. Its unbiased
                # residual-price variance is beta^2 - E[residual]^2.
                variance = max(0, beta*beta-residual_mean*residual_mean)
                raw_variance = max(0, qsp["raw_lcu_beta"]**2-qsp["qsp_finite_price"]**2)
                combined.append(dict(strike=record["strike"], degree=qsp["degree"], method=record["method"],
                                     shots=record.get("shots"), replicate=record.get("replicate"), beta=beta,
                                     raw_beta=qsp["raw_lcu_beta"], normalization_ratio=beta/qsp["raw_lcu_beta"],
                                     hadamard_price_variance=variance, raw_hadamard_price_variance=raw_variance,
                                     lower_hadamard_variance_than_raw=variance < raw_variance,
                                     quantum_advantage_established=False))
        for count in CONFIG["reuse"]:
            for shots in CONFIG["shots"]:
                reuse.append(dict(valuations=count, discovery_shots=shots,
                                  discovery_cx_per_valuation=shots*discovery_cost["cx"]/count,
                                  classical_fwht_add_subtract_per_valuation=n*8/count,
                                  quantum_training_labels_per_valuation=CONFIG["training_paths"]/count,
                                  classical_training_labels_per_valuation=CONFIG["training_paths"]/count,
                                  recurring_training_labels_per_new_strike=CONFIG["training_paths"],
                                  recurring_signal_table_entries=n,
                                  recurring_coefficient_refit=True,
                                  recurring_qae_or_shot_cost_included_in_total=False,
                                  hardware_time_break_even=None))
        write_json(output/"combined_screen.json", dict(rows=combined, reuse=reuse,
                   confirmation_unblocked=False, application_admitted=False,
                   missing=["scalable signal oracle", "uniform phase/loader certificate", "full continuous-target cost comparison", "human confirmation protocol review"]))
        if hashes != {name: sha256(ROOT/name) for name in hashes}:
            raise RuntimeError("producer changed during acquisition")
        write_json(output/"complete.json", dict(finished_utc=datetime.now(timezone.utc).isoformat(),
                   sha256={p.name: sha256(p) for p in sorted(output.iterdir()) if p.is_file()}))
        print(json.dumps(dict(representation_rows=len(records), combined_rows=len(combined),
                              lcu_error=abs(reconstructed-expected), lcu_beta_ratio=integrated_beta_ratio,
                              lower_variance_cells=sum(r["lower_hadamard_variance_than_raw"] for r in combined),
                              quantum_advantage=False)), flush=True)
    except BaseException as error:
        write_json(output/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
