"""Exclusive, bounded approximation/centering development. No confirmation."""

import argparse
from datetime import datetime, timezone
import math
from pathlib import Path
import platform
import time
import numpy as np
import scipy
import mpmath
from numpy.polynomial.chebyshev import chebval

from .asian_basket import Basket, setup
from .asian_encoding import grid
from .certified_payoff import discrete_minimax, uniform_abs_bound, comparison_allowance
from .combined_qsp import response
from .centered_factorized_signal import CenteredFactorizedSignal, signal_circuit as centered_circuit
from .control_offset_enclosure import moment_enclosure, control_enclosure
from .decimal_enclosure import Interval as I
from .encoding_enclosure import base_enclosure, at_precision, upward_float
from .factorized_signal import FactorizedSignal, signal_circuit as original_circuit
from .normalization_study import radius_enclosures, truncated_candidate, normalized_residual
from .normal_loader_budget import loader_plan
from .qsp_error_budget import dollar_budget
from .run_combined_development import circuit_cost
from .symmetric_phase import synthesize_even, uniform_phase_bound
from .storage import ROOT, sha256, write_json


CONFIG = dict(degrees=[16, 32, 64, 128], low=4, cutoff=4, finite_q=2, budget_q=10,
              assets=2, dates=2, strike=100, fit_points=8193,
              synthesis_cap=150, phase_tolerance=1e-8, numerical_comparison_allowance=1e-8,
              adaptive_development=True, confirmation=False)
SOURCES = tuple("research/journal_sprint/"+name for name in (
    "run_normalization_approximation.py", "normalization_study.py", "certified_payoff.py",
    "centered_factorized_signal.py", "control_offset_enclosure.py", "factorized_signal.py",
    "symmetric_phase.py", "qsp_error_budget.py", "combined_qsp.py", "polynomial_residual.py",
    "decimal_enclosure.py", "encoding_enclosure.py", "normal_loader_budget.py", "asian_basket.py",
    "asian_encoding.py", "price_contract.py", "encoding_decision.py", "combined_representation.py",
    "run_combined_development.py", "storage.py")) + (
    "docs/journal_sprint/NORMALIZATION_APPROXIMATION_PROTOCOL.md",)


def serialize_control(record):
    return dict(value=record["value"].record(), moments=[v.record() for v in record["moments"]],
                terms=record["terms"], work=record["work"], scope=record["scope"])


def run(output):
    if CONFIG["low"] != 4 or CONFIG["cutoff"] != 4:
        raise ValueError("control certificate currently supports low4/cutoff4 only")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES}
    import qiskit
    write_json(output/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               mpmath=mpmath.__version__, qiskit=qiskit.__version__,
               numerical_backend=np.__config__.show(mode="dicts"),
               started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        contract = Basket(CONFIG["assets"], CONFIG["dates"], CONFIG["strike"])
        model = setup(contract)
        low = truncated_candidate(CONFIG["low"])["coefficients"]
        discount = math.exp(-contract.rate*contract.maturity)
        real_discount = (-I(str(contract.rate))*I(str(contract.maturity))).exp()
        radii = radius_enclosures(model["means"], model["factor"], contract.strike, CONFIG["cutoff"])
        write_json(output/"model.json", dict(means=model["means"].tolist(), factor=model["factor"].tolist(),
                   means_hex=[float(v).hex() for v in model["means"]],
                   factor_hex=[[float(v).hex() for v in row] for row in model["factor"]],
                   discount_hex=discount.hex(), low_coefficients=low,
                   low_coefficients_hex=[float(v).hex() for v in low],
                   radius_enclosures={k: v.record() for k, v in radii.items()},
                   qualification="exact binary inputs archived before fits and numerical acquisition"))
        plans = []
        for family, cls in (("original", FactorizedSignal), ("centered", CenteredFactorizedSignal)):
            for q in (CONFIG["finite_q"], CONFIG["budget_q"]):
                p = cls(model["means"], model["factor"], contract.strike, q, CONFIG["cutoff"])
                plans.append(dict(family=family, **p.resource_metadata()))
        tiny_model = setup(Basket(1, 2, CONFIG["strike"]))
        costs = {}
        for family, cls, circuit in (("original", FactorizedSignal, original_circuit),
                                     ("centered", CenteredFactorizedSignal, centered_circuit)):
            p = cls(tiny_model["means"], tiny_model["factor"], contract.strike, 1, CONFIG["cutoff"])
            costs[family] = dict(radius=p.B, cost=circuit_cost(circuit(p)), metadata=p.resource_metadata())
        write_json(output/"signal_plans.json", dict(plans=plans, tiny_costs=costs,
                   scope="d2/q1 signal-only compiled comparison; no production circuit runtime"))
        print("Signal plans and matched tiny signal compilation complete", flush=True)

        data = grid(contract, CONFIG["finite_q"], CONFIG["cutoff"])
        if (not np.array_equal(data["model"]["factor"], model["factor"])
                or not np.array_equal(data["model"]["means"], model["means"])):
            raise ArithmeticError("diagnostic model differs from archived model")
        values = np.exp(model["means"]+data["normals"] @ model["factor"].T).mean(axis=1)
        weights = data["weights"]
        truth = discount*np.maximum(values-contract.strike, 0)
        base = base_enclosure(contract, model, CONFIG["cutoff"], "raw")
        encoding = at_precision(base, CONFIG["budget_q"])
        loader = loader_plan(CONFIG["budget_q"], CONFIG["cutoff"])
        write_json(output/"loader.json", loader)
        state_error = upward_float((I(loader["operator_error_upper"])*len(model["means"])).hi)
        representation = I(encoding["partial_sum"]["upper"])
        representation += (real_discount-I(discount)).absolute()*radii["cube_basket_upper"]
        write_json(output/"encoding.json", dict(base=encoding,
                   discount_bridge_upper=str(((real_discount-I(discount)).absolute()*radii["cube_basket_upper"]).hi),
                   representation_upper=str(representation.hi),
                   product_loader_state_error_upper=state_error,
                   loader_scope="tensor product stored-angle ideal controlled-RY; no hardware noise"))
        moments_by_q, moment_records = {}, {}
        for q in (CONFIG["finite_q"], CONFIG["budget_q"]):
            start = time.perf_counter()
            record = moment_enclosure(model["means"], model["factor"], q,
                                      CONFIG["cutoff"], CONFIG["low"])
            moments_by_q[q] = record
            moment_records[str(q)] = dict(moments=[v.record() for v in record["moments"]],
                work=record["work"], terms=record["terms"], scope=record["scope"],
                elapsed_seconds=time.perf_counter()-start)
        write_json(output/"moments.json", moment_records)
        controls = {}
        for family in ("original", "centered"):
            radius = upward_float(radii[family].hi)
            records = {}
            for q in (CONFIG["finite_q"], CONFIG["budget_q"]):
                start = time.perf_counter()
                record = dict(moments_by_q[q])
                record.update(control_enclosure(record["moments"], contract.strike, radius, discount, low))
                # Decimal midpoint rounding does not need to be trusted: the
                # actual chosen binary offset is compared with the full enclosure.
                offset = float((record["value"].lo+record["value"].hi)/2)
                error = upward_float((I(offset)-record["value"]).absolute().hi)
                records[str(q)] = dict(**serialize_control(record), offset=offset,
                                      offset_hex=offset.hex(), offset_error_upper=error,
                                      elapsed_seconds=time.perf_counter()-start)
            controls[family] = dict(radius=radius, by_precision=records)
            print(f"{family}: control offset enclosed at both precisions", flush=True)
        write_json(output/"controls.json", controls)

        rows, budgets = [], []
        for degree in CONFIG["degrees"]:
            candidates = {"truncated": truncated_candidate(degree),
                          "minimax": discrete_minimax(degree, CONFIG["fit_points"])}
            for approximation, candidate in candidates.items():
                if not candidate["solver_success"]:
                    write_json(output/f"{approximation}_{degree}.json", dict(candidate=candidate, accepted=False))
                    continue
                high = candidate["coefficients"]
                if approximation == "minimax":
                    candidate["uniform_certificate"] = uniform_abs_bound(high)
                    candidate["uniform_error_upper"] = candidate["uniform_certificate"]["uniform_error_upper"]
                residual = normalized_residual(high, low)
                synthesis = synthesize_even(residual["coefficients"], CONFIG["synthesis_cap"])
                phase = uniform_phase_bound(synthesis["phases"], residual["coefficients"])
                accepted = phase["uniform_error_upper"] < CONFIG["phase_tolerance"]
                write_json(output/f"{approximation}_{degree}.json", dict(candidate=candidate,
                    residual=residual, synthesis=synthesis, phase_certificate=phase, accepted=accepted))
                if not accepted:
                    print(f"{approximation}/{degree}: phase rejected, retained", flush=True)
                    continue
                for family in ("original", "centered"):
                    radius = controls[family]["radius"]
                    factor = discount*radius/2
                    beta = factor*residual["rho"]
                    x = (values-contract.strike)/radius
                    low_values = chebval(x, low)
                    control = factor*(x+low_values)
                    finite_control = controls[family]["by_precision"][str(CONFIG["finite_q"])]
                    offset = finite_control["offset"]
                    high_values = chebval(x, high)
                    ideal_price = float(weights @ (factor*(x+high_values)))
                    polynomial_price = offset+factor*float(weights @ (high_values-low_values))
                    identity_error = abs(polynomial_price-ideal_price)
                    if identity_error > CONFIG["numerical_comparison_allowance"]:
                        raise ArithmeticError("polynomial identity or finite control mismatch")
                    mean = float(weights @ response(x, synthesis["phases"]).real)
                    phase_price = offset+beta*mean
                    allowance = comparison_allowance(beta, phase["uniform_error_upper"],
                        factor*residual["coefficient_bridge_upper"], CONFIG["numerical_comparison_allowance"])
                    if abs(phase_price-polynomial_price) > allowance:
                        raise ArithmeticError("dollar-scaled phase comparison failed")
                    raw_scale = factor*(1+candidate["uniform_error_upper"])
                    raw_mean = float(weights @ high_values)/(1+candidate["uniform_error_upper"])
                    classical_residual = truth-control
                    variance = beta*beta*(1-mean*mean)
                    rows.append(dict(family=family, approximation=approximation, degree=degree,
                        radius=radius, beta=beta, true_finite_price=float(weights @ truth),
                        approximate_price=phase_price, observed_bias=phase_price-float(weights @ truth),
                        polynomial_identity_error=identity_error, phase_price_error=abs(phase_price-polynomial_price),
                        phase_comparison_allowance=allowance,
                        uniform_payoff_error_upper=upward_float((I(discount)*I(radius)/2*I(candidate["uniform_error_upper"])).hi),
                        quantum_ideal_variance=variance, raw_ideal_variance=raw_scale**2*(1-raw_mean**2),
                        classical_controlled_variance=float(weights @ (classical_residual-weights @ classical_residual)**2),
                        equal_total_error_runtime_comparison=False))
                    numerical_control = controls[family]["by_precision"][str(CONFIG["budget_q"])]
                    budget = dollar_budget(degree=degree, discount=discount, radius=radius,
                        rho=residual["rho"],
                        polynomial=dict(truncation_upper=candidate["uniform_error_upper"],
                                        stored_coefficient_error_upper=residual["coefficient_bridge_upper"]),
                        phase_error=phase["uniform_error_upper"],
                        representation_upper=upward_float(representation.hi),
                        preparation_state_error=state_error,
                        control_offset_error=numerical_control["offset_error_upper"])
                    budgets.append(dict(family=family, approximation=approximation, degree=degree,
                        normal_bits=CONFIG["budget_q"], **budget))
                print(f"{approximation}/{degree}: uniform approx {candidate['uniform_error_upper']:.6g}, phase {phase['uniform_error_upper']:.3g}", flush=True)
        write_json(output/"results.json", dict(rows=rows, budgets=budgets, application_admitted=False,
                   quantum_advantage=False, confirmation=False,
                   qualification="bounded adaptive development; partial ideal-model budget, no hardware results"))
        if hashes != {name: sha256(ROOT/name) for name in SOURCES}:
            raise RuntimeError("source changed during acquisition")
        write_json(output/"complete.json", dict(sha256={p.name: sha256(p) for p in sorted(output.iterdir()) if p.is_file()}))
        print("Normalization/approximation study complete", flush=True)
    except BaseException as error:
        write_json(output/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
