"""Small finite Gaussian-grid Asian encodings, not scalable pricing or a certificate."""

import math
import time

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import StatePreparation, UCRYGate
from qiskit.quantum_info import Statevector
from scipy.special import ndtr

from .asian_basket import setup, evaluate
from .price_contract import BIAS_COMPONENTS, BiasComponent, PriceContract


def grid(contract, precision, cutoff):
    """Independent normal registers; coordinate zero occupies low-order bits.

    Cell probabilities are Gaussian CDF differences, NOT density samples.
    Midpoint quantization is conditional on all independent coordinates in cube.
    """
    dim = contract.assets * contract.dates
    if (isinstance(precision, bool) or not isinstance(precision, int)
            or precision < 1 or dim * precision > 8):
        raise ValueError("prototype requires 1..8 total normal-register qubits")
    if (isinstance(cutoff, bool) or not math.isfinite(cutoff)
            or not 0.5 <= cutoff <= 6):
        raise ValueError("cutoff must be finite in [0.5, 6]")
    count = 2**precision
    edges = np.linspace(-cutoff, cutoff, count + 1)
    nodes = (edges[:-1] + edges[1:]) / 2
    marginal = np.diff(ndtr(edges)) / (ndtr(cutoff) - ndtr(-cutoff))
    marginal /= marginal.sum()  # Floating normalization, not an enclosure.
    indices = np.arange(count**dim)
    digits = np.column_stack([(indices // count**j) % count for j in range(dim)])
    normals = nodes[digits]
    weights = marginal[digits].prod(axis=1)
    model = setup(contract)
    raw, control, _ = evaluate(contract, model, normals)
    residual = raw - control
    if residual.min() < -1e-10:
        raise ArithmeticError("AM-GM residual should be nonnegative")
    residual = np.maximum(residual, 0)
    return dict(normals=normals, weights=weights, marginal=marginal, raw=raw,
                control=control, residual=residual, model=model)


def analytic_bounds(contract, precision, cutoff, model, representation):
    """Real-arithmetic upper bounds, evaluated in floats (not outward rounded).

    Exponential tilting bounds omitted payoff mass using a union over independent
    Gaussian coordinates. Renormalization uses E[F]/P(cube). Midpoint error uses
    a cube-wide Lipschitz bound. Residual <= raw; Lipschitz constants add.
    """
    if representation not in ("raw", "residual"):
        raise ValueError("unknown representation")
    dim = len(model["means"])
    factor = model["factor"]
    discount = math.exp(-contract.rate * contract.maturity)
    expected_spots = np.exp(model["means"] + np.diag(model["covariance"]) / 2)
    cube_mass = float((ndtr(cutoff) - ndtr(-cutoff))**dim)
    omitted_spot = expected_spots * (
        ndtr(-cutoff - factor) + ndtr(-cutoff + factor)).sum(axis=1)
    tail = discount * float(omitted_spot.mean())
    tail += (1 - cube_mass) / cube_mass * discount * float(expected_spots.mean())
    row_l1 = np.abs(factor).sum(axis=1)
    upper_spots = np.exp(model["means"] + cutoff * row_l1)
    lipschitz = discount * float((upper_spots * row_l1).mean())
    discretization = lipschitz * cutoff / 2**precision
    if representation == "residual":
        geometric_l1 = float(np.abs(factor.mean(axis=0)).sum())
        geometric_lipschitz = discount * math.exp(
            float(model["means"].mean()) + cutoff * geometric_l1) * geometric_l1
        discretization += geometric_lipschitz * cutoff / 2**precision
    return dict(tail_and_renormalization=tail, discretization=discretization,
                cube_probability=cube_mass,
                continuous_cube_payoff_upper=discount * max(float(upper_spots.mean())
                                                           - contract.strike, 0))


def price_contract(contract, precision, cutoff, data, representation):
    values = data[representation]
    scale = float(values.max())
    if not scale > 0:
        raise ValueError("zero-payoff table requires no amplitude estimation")
    bounds = analytic_bounds(contract, precision, cutoff, data["model"], representation)
    parts = []
    for name in BIAS_COMPONENTS:
        bound = bounds.get(name)
        evidence = ("real-arithmetic derivation in PROTOCOL_W13_ENCODING_V1; "
                    "floating evaluation needs separate enclosure") if bound is not None else (
                    "unbounded floating synthesis/preparation/arithmetic/enclosure error; "
                    "statevector agreement is diagnostic only")
        parts.append(BiasComponent(name, bound, evidence))
    offset = 0.0 if representation == "raw" else data["model"]["expected_control"]
    return PriceContract(
        f"asian_{contract.assets}_{contract.dates}_{contract.strike}",
        "discounted equal-weight discrete arithmetic Asian basket under correlated GBM",
        "USD", representation, offset, scale, tuple(parts),
        "telescoping truncation, midpoint, implementation errors; analytic geometric "
        "control mean replaces finite-grid mean only for the continuous-model target",
        ("ideal simulator, no physical noise bound", "no directed numerical enclosure",
         "finite-table payoff, exponential dimension cost",))


def circuits(data, precision, representation, loader):
    if representation not in ("raw", "residual") or loader not in ("product", "dense"):
        raise ValueError("unknown representation or loader")
    dim = data["normals"].shape[1]
    bits = dim * precision
    prep = QuantumCircuit(bits + 1)
    if loader == "product":
        for j in range(dim):
            prep.append(StatePreparation(np.sqrt(data["marginal"])),
                        list(range(j * precision, (j + 1) * precision)))
    else:
        prep.append(StatePreparation(np.sqrt(data["weights"])), list(range(bits)))
    scale = float(data[representation].max())
    if not scale > 0:
        raise ValueError("zero-payoff table requires no circuit")
    angles = 2 * np.arcsin(np.sqrt(data[representation] / scale))
    payoff = QuantumCircuit(bits + 1)
    payoff.append(UCRYGate(angles.tolist()), [bits] + list(range(bits)))
    return prep, payoff, prep.compose(payoff)


def resources(circuit):
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0,
                         seed_transpiler=13001)
    return compiled, dict(qubits=compiled.num_qubits, depth=compiled.depth(),
                          cx=int(compiled.count_ops().get("cx", 0)),
                          u=int(compiled.count_ops().get("u", 0)))


def measure(data, precision, representation, loader):
    started = time.perf_counter()
    prep, payoff, circuit = circuits(data, precision, representation, loader)
    compiled, total = resources(circuit)
    _, loading = resources(prep)
    _, rotation = resources(payoff)
    _, inverse = resources(circuit.inverse())
    state = Statevector.from_instruction(compiled)
    bits = compiled.num_qubits - 1
    good = np.abs(state.data[2**bits:])**2
    expected_joint = data["weights"] * data[representation] / data[representation].max()
    expected_bad = data["weights"] - expected_joint
    intended = np.sqrt(np.concatenate([expected_bad, expected_joint])).astype(complex)
    fidelity_error = float(abs(1 - abs(np.vdot(intended, state.data))**2))
    error = float(max(np.max(np.abs(good - expected_joint)),
                      np.max(np.abs(np.abs(state.data[:2**bits])**2 - expected_bad))))
    amplitude = float(good.sum())
    expected = float(expected_joint.sum())
    if error > 1e-10 or abs(amplitude - expected) > 1e-10 or fidelity_error > 1e-10:
        raise ArithmeticError("compiled joint-state semantics failed")
    # Inverse is explicitly executed; this also checks clean ancilla reversibility.
    undone = state.evolve(compiled.inverse())
    inverse_error = float(abs(1 - abs(undone.data[0])**2))
    if inverse_error > 1e-10:
        raise ArithmeticError("uncompute validation failed")
    return dict(loader=loader, probability=amplitude, expected_probability=expected,
                max_joint_probability_error=error, inverse_return_error=inverse_error,
                state_fidelity_error=fidelity_error,
                loading=loading, payoff=rotation, acquisition=total, inverse=inverse,
                shots=0, quantum_device_seconds=None,
                compile_and_statevector_seconds=time.perf_counter() - started)
