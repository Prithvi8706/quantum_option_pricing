"""Bounded separable-signal / symmetric-phase development, not confirmation."""

import argparse
from datetime import datetime, timezone
import math
from pathlib import Path
import platform
import numpy as np
import scipy
import mpmath

from .asian_basket import Basket, setup
from .asian_encoding import grid
from .combined_qsp import abs_polynomial, response
from .decimal_enclosure import Interval as I
from .encoding_enclosure import base_enclosure, at_precision, upward_float
from .factorized_signal import FactorizedSignal, signal_circuit, phased_walk_circuit
from .normal_loader_budget import loader_plan, circuit as loader_circuit
from .polynomial_residual import basket_moments, polynomial_control
from .qsp_error_budget import residual_coefficients, polynomial_error, dollar_budget
from .run_combined_development import circuit_cost
from .symmetric_phase import synthesize_even, uniform_phase_bound
from .storage import ROOT, sha256, write_json


CONFIG = dict(degrees=[8, 16, 32, 64, 128], low=4, cutoff=4, normal_bits=2,
              precision_plans=[2, 6, 10], max_nfev_per_stage=150,
              uniform_acceptance=1e-8, adaptive_development=True, confirmation=False)
SOURCES = tuple("research/journal_sprint/"+name for name in (
    "run_barrier_development.py", "symmetric_phase.py", "qsp_error_budget.py",
    "factorized_signal.py", "combined_qsp.py", "polynomial_residual.py",
    "asian_basket.py", "asian_encoding.py", "encoding_enclosure.py",
    "decimal_enclosure.py", "normal_loader_budget.py", "price_contract.py",
    "encoding_decision.py", "run_combined_development.py", "combined_representation.py",
    "storage.py")) + ("docs/journal_sprint/BARRIER_DEVELOPMENT_PROTOCOL.md",)


def tiny_integrated_check(phases):
    """Actual QSP Hadamard circuit with product loading; no joint prep table."""
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    contract = Basket(1, 2, 100)
    model = setup(contract)
    plan = FactorizedSignal(model["means"], model["factor"], 100, 1, 4)
    unitary = phased_walk_circuit(plan, phases)
    circuit = QuantumCircuit(plan.num_qubits+1)
    loader = loader_plan(1, 4)
    for j in range(plan.d):
        circuit.compose(loader_circuit(loader), [j], inplace=True)
    test = plan.num_qubits
    circuit.h(test)
    circuit.append(unitary.to_gate().control(), [test]+list(range(test)))
    circuit.h(test)
    state = Statevector.from_instruction(circuit)
    measured = 1-2*float(np.sum(abs(state.data[1 << test:])**2))
    data = grid(contract, 1, 4)  # independent tiny diagnostic, never an oracle input
    values = np.exp(model["means"]+data["normals"] @ model["factor"].T).mean(axis=1)
    expected = float(data["weights"] @ response((values-100)/plan.B, phases).real)
    discrepancy = abs(measured-expected)
    if discrepancy > 1e-8:
        raise ArithmeticError("separable product-loader Hadamard mismatch")
    return dict(contract="tiny one-asset/two-date finite smoke test, not original contract",
                measured=measured, expected=expected, discrepancy=discrepancy,
                cost=circuit_cost(circuit), product_loader=True, joint_preparation_table=False,
                clean_ancillas=False, quantum_hardware_used=False)


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES}
    import qiskit
    write_json(output/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               mpmath=mpmath.__version__, qiskit=qiskit.__version__,
               started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        contract = Basket(2, 2, 100)
        model = setup(contract)
        discount = math.exp(-contract.rate*contract.maturity)
        discount_upper = upward_float((-I(str(contract.rate))*I(str(contract.maturity))).exp().hi)
        upper = sum(((I(float(mu))+4*sum((I(float(b)).absolute() for b in row), I(0))).exp()
                     for mu, row in zip(model["means"], model["factor"])), I(0))/4+100
        safe_B = upward_float(upper.hi)
        base = base_enclosure(contract, model, 4, "raw")
        encoding = {q: at_precision(base, q) for q in CONFIG["precision_plans"]}
        plans = []
        for q in CONFIG["precision_plans"]:
            plan = FactorizedSignal(model["means"], model["factor"], 100, q, 4)
            record = plan.resource_metadata()
            record["product_normal_loader_controlled_rotations"] = 4*((1 << q)-1)
            record["avoided_joint_table_entries"] = str(1 << (4*q))
            record["directed_ideal_radius_upper"] = safe_B
            if q == 2:
                record["actual_signal_cost"] = circuit_cost(signal_circuit(plan))
            plans.append(record)
        write_json(output/"signal_plans.json", dict(plans=plans, original_contract=True,
                   implementation_error_enclosed=False, encoding=encoding))
        print("Separable signal emitted/compiled at q2; q6/q10 plans recorded", flush=True)

        data = grid(contract, 2, 4)
        weights = data["weights"]
        values = np.exp(model["means"]+data["normals"] @ model["factor"].T).mean(axis=1)
        moments, terms = basket_moments(model["means"], model["factor"],
                                      np.array([-3., -1., 1., 3.]), data["marginal"], 4)
        truth = discount*np.maximum(values-100, 0)
        true_price = float(weights @ truth)
        rows, budgets = [], []
        for degree in CONFIG["degrees"]:
            coefficients, rho = residual_coefficients(degree)
            synthesis = synthesize_even(coefficients, CONFIG["max_nfev_per_stage"])
            certificate = uniform_phase_bound(synthesis["phases"], coefficients)
            accepted = certificate["uniform_error_upper"] < CONFIG["uniform_acceptance"]
            polynomial = polynomial_error(degree, 4, coefficients, rho)
            write_json(output/f"phase_{degree}.json", dict(synthesis=synthesis, certificate=certificate,
                       rho=rho, polynomial=polynomial, uniform_accepted=accepted))
            if not accepted:
                print(f"Degree {degree}: rejected, attempts retained", flush=True)
                continue
            for name, radius in (("old_observed_radius", float(np.max(abs(values-100)))),
                                 ("separable_safe_radius", safe_B)):
                signal = (values-100)/radius
                factor = discount*radius/2
                control, offset = polynomial_control(values, 100, radius, discount, moments, 4)
                observable = response(signal, synthesis["phases"]).real
                expectation = float(weights @ observable)
                estimated = offset+factor*rho*expectation
                c, tail = abs_polynomial(degree)
                p = np.polynomial.chebyshev.chebval(signal, c)
                comparator_price = discount*(moments[1]-100)/2+factor*(1+tail)*float(weights @ p)
                if abs(estimated-comparator_price) > 1e-7:
                    raise ArithmeticError("equal-polynomial comparison mismatch")
                raw_variance = (factor*(1+tail))**2*(1-float(weights @ p)**2)
                residual_variance = (factor*rho)**2*(1-expectation**2)
                controlled = truth-control
                rows.append(dict(degree=degree, radius_kind=name, radius=radius,
                    true_finite_price=true_price, approximate_price=estimated,
                    observed_price_bias=estimated-true_price,
                    equal_polynomial_discrepancy=abs(estimated-comparator_price),
                    raw_ideal_hadamard_variance=raw_variance,
                    residual_ideal_hadamard_variance=residual_variance,
                    quantum_to_quantum_variance_reduction=raw_variance/residual_variance,
                    classical_controlled_variance=float(weights @ (controlled-weights @ controlled)**2),
                    beta=factor*rho, actual_hardware_speedup=False))
            for q in CONFIG["precision_plans"]:
                representation = upward_float(I(encoding[q]["partial_sum"]["upper"]).hi)
                budget = dollar_budget(degree=degree, discount=discount_upper, radius=safe_B, rho=rho,
                    polynomial=polynomial, phase_error=certificate["uniform_error_upper"],
                    representation_upper=representation)
                budgets.append(dict(normal_bits=q, degree=degree, **budget))
            if degree == 8:
                write_json(output/"tiny_integrated.json", tiny_integrated_check(synthesis["phases"]))
            print(f"Degree {degree}: uniform phase bound {certificate['uniform_error_upper']:.3g}", flush=True)
        write_json(output/"results.json", dict(rows=rows, budgets=budgets,
                   moment_terms=terms, original_contract_finite_diagnostic=True,
                   application_admitted=False, quantum_advantage=False,
                   qualification="adaptive development; no production statevector or continuous confirmation"))
        if hashes != {name: sha256(ROOT/name) for name in SOURCES}:
            raise RuntimeError("source changed during acquisition")
        write_json(output/"complete.json", dict(sha256={p.name: sha256(p) for p in sorted(output.iterdir()) if p.is_file()}))
        print("Bounded development complete; full error budget still unresolved", flush=True)
    except BaseException as error:
        write_json(output/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
