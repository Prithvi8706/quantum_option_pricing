"""Adaptive development follow-up; compare equal-bias quantum representations."""

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import time
import numpy as np

from .asian_basket import Basket
from .asian_encoding import grid
from .combined_qsp import synthesize, response, qsp_circuit, hadamard_mean
from .polynomial_residual import basket_moments, polynomial_control, residual_synthesis
from .run_combined_development import circuit_cost
from .storage import ROOT, sha256, write_json


CONFIG = dict(low=4, high=[8, 16, 32], strikes=[90, 95, 100, 105, 110],
              normal_bits=2, cutoff=4, adaptive_development=True, confirmation=False)
SOURCES = tuple("research/journal_sprint/"+name for name in (
    "polynomial_residual.py", "run_polynomial_residual.py", "combined_qsp.py",
    "run_combined_development.py", "combined_representation.py", "asian_basket.py",
    "asian_encoding.py", "price_contract.py", "encoding_decision.py", "storage.py")) + (
    "docs/journal_sprint/COMBINED_FOLLOWUP_PROTOCOL.md",)


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES}
    write_json(output/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               python=platform.python_version(), started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        basket = Basket(2, 2, 100)
        data = grid(basket, CONFIG["normal_bits"], CONFIG["cutoff"])
        weights = data["weights"]
        logs = data["model"]["means"]+data["normals"] @ data["model"]["factor"].T
        values = np.exp(logs).mean(axis=1)
        nodes = np.array([-3., -1., 1., 3.])
        start = time.perf_counter()
        moments, terms = basket_moments(data["model"]["means"], data["model"]["factor"], nodes, data["marginal"], CONFIG["low"])
        setup_seconds = time.perf_counter()-start
        direct = np.array([weights @ values**k for k in range(CONFIG["low"]+1)])
        relative_error = float(np.max(abs(moments-direct)/np.maximum(1, abs(direct))))
        if relative_error > 1e-12:
            raise ArithmeticError("factorized moment expansion mismatch")
        write_json(output/"moments.json", dict(values=moments.tolist(), multinomial_terms=terms,
                   marginal_exponential_entries=terms*4*len(nodes), setup_seconds=setup_seconds,
                   finite_enumeration_relative_check=relative_error,
                   reuse=[dict(valuations=n, terms_per_valuation=terms/n,
                               classical_same_moments_available=True,
                               new_strike_signal_table_entries=256,
                               signal_rebuild_not_amortized=True) for n in (1, 5, 25, 100)],
                   target="finite product-normal grid, not continuous Gaussian moments"))
        rows = []
        for degree in CONFIG["high"]:
            raw, residual = synthesize(degree), residual_synthesis(degree, CONFIG["low"])
            write_json(output/f"synthesis_{degree}.json", dict(raw=raw, residual=residual))
            if not raw["fit_accepted"] or not residual["fit_accepted"]:
                print(f"Degree {degree}: phase fit rejected, attempts retained", flush=True)
                continue
            for strike in CONFIG["strikes"]:
                radius = float(np.max(abs(values-strike)))
                signal = (values-strike)/radius
                discount = math.exp(-basket.rate*basket.maturity)
                factor = discount*radius/2
                control, expectation = polynomial_control(values, strike, radius, discount, moments, CONFIG["low"])
                if abs(expectation-weights @ control) > 1e-9:
                    raise ArithmeticError("polynomial control moment mismatch")
                raw_beta, residual_beta = factor*raw["abs_rescale"], factor*residual["rho"]
                raw_observable = response(signal, raw["phases"]).real
                residual_observable = response(signal, residual["phases"]).real
                raw_offset = discount*(moments[1]-strike)/2
                raw_price = raw_offset+raw_beta*float(weights @ raw_observable)
                residual_price = expectation+residual_beta*float(weights @ residual_observable)
                if abs(raw_price-residual_price) > 1e-6:
                    raise ArithmeticError("equal-polynomial-bias identity mismatch")
                truth = discount*np.maximum(values-strike, 0)
                true_residual = truth-control
                raw_variance = raw_beta**2*(1-float(weights @ raw_observable)**2)
                residual_variance = residual_beta**2*(1-float(weights @ residual_observable)**2)
                classical_raw_variance = float(weights @ (truth-weights @ truth)**2)
                classical_residual_variance = float(weights @ (true_residual-weights @ true_residual)**2)
                row = dict(degree=degree, strike=strike, raw_beta=raw_beta, residual_beta=residual_beta,
                           normalization_reduction=raw_beta/residual_beta,
                           raw_hadamard_variance=raw_variance, residual_hadamard_variance=residual_variance,
                           hadamard_variance_reduction=raw_variance/residual_variance,
                           true_finite_price=float(weights @ truth), raw_qsp_price=raw_price, residual_qsp_price=residual_price,
                           observed_equal_bias_error=abs(raw_price-residual_price),
                           observed_price_bias=raw_price-float(weights @ truth),
                           analytic_truncation_price_expression=factor*raw["analytic_truncation_expression"],
                           classical_raw_variance=classical_raw_variance, classical_controlled_variance=classical_residual_variance,
                           quantum_hardware_advantage=False, uniform_phase_certificate=False)
                if strike == 100:
                    for name, plan, expected in (("raw", raw, weights @ raw_observable),
                                                ("residual", residual, weights @ residual_observable)):
                        actual, circuit = hadamard_mean(qsp_circuit(signal, plan["phases"]), weights)
                        if abs(actual-expected) > 1e-8:
                            raise ArithmeticError("actual follow-up circuit mismatch")
                        row[name+"_cost"] = circuit_cost(circuit)
                        row[name+"_circuit_error"] = abs(actual-float(expected))
                    row["cx_weighted_variance_reduction"] = raw_variance*row["raw_cost"]["cx"]/(residual_variance*row["residual_cost"]["cx"])
                rows.append(row)
            print(f"Degree {degree}: equal-bias identities and actual circuits checked", flush=True)
        write_json(output/"results.json", dict(rows=rows, application_admitted=False,
                   quantum_discovery_used=False,
                   qualification="analytical control inside QSP, observed finite-circuit resource improvement only; same controls offered classically"))
        if hashes != {name: sha256(ROOT/name) for name in hashes}:
            raise RuntimeError("source changed during follow-up")
        write_json(output/"complete.json", dict(finished_utc=datetime.now(timezone.utc).isoformat(),
                   sha256={p.name: sha256(p) for p in sorted(output.iterdir()) if p.is_file()}))
        print(json.dumps([r for r in rows if r["strike"] == 100]), flush=True)
    except BaseException as error:
        write_json(output/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
