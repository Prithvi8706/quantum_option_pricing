"""Supplemental nonuniform-loader check and explicitly reconstructed model receipt."""

import argparse
import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .asian_basket import Basket, setup
from .asian_encoding import grid
from .combined_qsp import response
from .factorized_signal import FactorizedSignal, phased_walk_circuit
from .normal_loader_budget import loader_plan, circuit as loader_circuit
from .run_barrier_development import CONFIG, SOURCES
from .storage import ROOT, sha256, write_json


def nonuniform_check(phases):
    contract = Basket(1, 1, 100)
    model = setup(contract)
    plan = FactorizedSignal(model["means"], model["factor"], 100, 3, 4)
    loader = loader_circuit(loader_plan(3, 4))
    data = grid(contract, 3, 4)
    probabilities = Statevector.from_instruction(loader).probabilities()
    probability_error = float(np.max(abs(probabilities-data["marginal"])))
    reversed_bits = [int(f"{j:03b}"[::-1], 2) for j in range(8)]
    bit_reversal_l1 = float(np.sum(abs(probabilities-probabilities[reversed_bits])))
    if probability_error > 1e-12 or bit_reversal_l1 < .1:
        raise ArithmeticError("nonuniform-loader ordering check failed")
    unitary = phased_walk_circuit(plan, phases)
    circuit = QuantumCircuit(plan.num_qubits+1)
    circuit.compose(loader, list(range(3)), inplace=True)
    test = plan.num_qubits
    circuit.h(test)
    circuit.append(unitary.to_gate().control(), [test]+list(range(test)))
    circuit.h(test)
    state = Statevector.from_instruction(circuit)
    actual = 1-2*float(np.sum(abs(state.data[1 << test:])**2))
    values = np.exp(model["means"]+data["normals"] @ model["factor"].T).mean(axis=1)
    expected = float(data["weights"] @ response((values-100)/plan.B, phases).real)
    error = abs(actual-expected)
    if error > 1e-8:
        raise ArithmeticError("nonuniform integrated Hadamard check failed")
    return dict(contract="one-asset/one-date diagnostic, not original target", normal_bits=3,
                qubits=circuit.num_qubits, degree=len(phases)-1,
                preparation_probability_error=probability_error,
                bit_reversed_probability_l1=bit_reversal_l1,
                actual=actual, expected=expected, discrepancy=error,
                joint_signal_or_preparation_table=False, diagnostic_enumeration_only=True)


def verify(archive, receipt):
    archive = Path(archive)
    planned = json.loads((archive/"planned.json").read_text())
    if CONFIG["low"] != 4 or CONFIG["cutoff"] != 4 or CONFIG["normal_bits"] != 2:
        raise ValueError("v1 is a frozen fixed-configuration producer, not a general runner")
    if planned["config"] != CONFIG or set(planned["source_sha256"]) != set(SOURCES):
        raise ValueError("configuration/source inventory mismatch")
    for name, digest in planned["source_sha256"].items():
        if sha256(ROOT/name) != digest:
            raise ValueError("source hash mismatch")
    manifest = json.loads((archive/"complete.json").read_text())["sha256"]
    for name, digest in manifest.items():
        if sha256(archive/name) != digest:
            raise ValueError("artifact hash mismatch")
    phase = json.loads((archive/"phase_8.json").read_text())["synthesis"]["phases"]
    check = nonuniform_check(phase)
    model = setup(Basket(2, 2, 100))
    write_json(receipt, dict(nonuniform_integration=check,
               reconstructed_model=dict(means_hex=[float(v).hex() for v in model["means"]],
                   factor_hex=[[float(v).hex() for v in row] for row in model["factor"]],
                   qualification="reconstructed after acquisition in current environment; NOT a contemporaneous input snapshot"),
               configuration_guard="v1 fixed low4/cutoff4/q2 only; future acquisitions need fully operative config",
               archive_manifest_sha256=sha256(archive/"complete.json"),
               verifier_sha256=sha256(Path(__file__)), application_admitted=False))
    print(check, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("receipt")
    args = parser.parse_args()
    verify(args.archive, args.receipt)
