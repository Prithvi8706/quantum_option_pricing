"""
IBM Quantum Hardware Validation - Paper A
=========================================
Single-point validation: runs ONE minimal state-preparation circuit that
amplitude-encodes the benchmark probability p = 0.3 onto a single qubit, then
measures it. Comparing the hardware estimate of p against the ideal value
quantifies how much real-device noise perturbs the amplitude encoding that
Paper A's QAE pipeline depends on.

Why a single RY qubit (not the H + CX...CX circuit)?
    On a *perfect* simulator the entangling-gate version yields
    P(qubit1 = 1) = 0.50, not 0.30 - the CX gates wash out the encoded
    probability, so it can never validate against 0.30. RY(2*arcsin(sqrt(p)))
    on one isolated qubit gives P(1) = p exactly, so any deviation on hardware
    is a clean noise signal.

Usage:
    python ibm_validation.py             # dry run on local AerSimulator (default, safe)
    python ibm_validation.py --hardware  # submit ONE job to real IBM Quantum hardware

Auth (hardware mode): IBM Quantum Platform on IBM Cloud, channel="ibm_cloud".
Reads IBM_QUANTUM_TOKEN (API key) and IBM_QUANTUM_CRN (instance CRN) from .env.
"""
import os
import sys
import json

import numpy as np
from qiskit import QuantumCircuit, transpile

P_TARGET = 0.3
SHOTS = 1024
RESULTS_PATH = os.path.join("results", "ibm_hardware_validation.json")


def build_circuit() -> QuantumCircuit:
    """Minimal correct state-prep: RY encodes P(|1>) = P_TARGET on one qubit."""
    qc = QuantumCircuit(1)
    qc.ry(2 * np.arcsin(np.sqrt(P_TARGET)), 0)
    qc.measure_all()  # single classical register named 'meas', 1 bit
    return qc


def summarize(counts: dict, backend_name: str, job_id: str) -> dict:
    """Print and package the empirical estimate vs the theoretical value."""
    total = sum(counts.values())
    p_hat = counts.get("1", 0) / total
    abs_err = abs(p_hat - P_TARGET)
    print(f"Counts: {counts}")
    print(f"Empirical p estimate: {p_hat:.4f} (theoretical: {P_TARGET:.4f})")
    print(f"Absolute error: {abs_err:.4f}")
    return {
        "job_id": job_id,
        "backend": backend_name,
        "shots": SHOTS,
        "counts": counts,
        "p_hat": p_hat,
        "theoretical_p": P_TARGET,
        "absolute_error": abs_err,
        "notes": "Single-point hardware validation for Paper A",
    }


def run_dry() -> None:
    """Local noiseless check - no credentials, no hardware, nothing saved."""
    from qiskit_aer import AerSimulator

    sim = AerSimulator()
    qc = build_circuit()
    print(f"[DRY RUN] AerSimulator  depth={qc.depth()}  ops={dict(qc.count_ops())}")
    isa = transpile(qc, sim)
    counts = sim.run(isa, shots=SHOTS, seed_simulator=42).result().get_counts()
    summarize(counts, "AerSimulator", "dry-run")
    print("Dry run complete. Expect p_hat ~ 0.30. This result is NOT saved.")


def run_hardware() -> None:
    """Submit exactly one job to the least-busy real backend and save the result."""
    from dotenv import load_dotenv
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    load_dotenv()
    token = os.getenv("IBM_QUANTUM_TOKEN")
    crn = os.getenv("IBM_QUANTUM_CRN")
    if not token or token.startswith("replace_with"):
        raise ValueError("IBM_QUANTUM_TOKEN (IBM Cloud API key) not set in .env")
    if not crn or crn.startswith("replace_with"):
        raise ValueError("IBM_QUANTUM_CRN (instance CRN) not set in .env")

    service = QiskitRuntimeService(channel="ibm_cloud", token=token, instance=crn)
    backend = service.least_busy(operational=True, simulator=False, min_num_qubits=1)
    print(f"Running on: {backend.name}")

    qc = build_circuit()
    isa = transpile(qc, backend=backend, optimization_level=1)
    print(f"Circuit depth: {isa.depth()}, Gates: {dict(isa.count_ops())}")

    sampler = Sampler(mode=backend)
    job = sampler.run([isa], shots=SHOTS)
    print(f"Job ID: {job.job_id()}")
    print("Job submitted. Waiting for result...")

    result = job.result()
    counts = result[0].data.meas.get_counts()
    record = summarize(counts, backend.name, job.job_id())

    os.makedirs("results", exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(record, f, indent=2)
    print(f"Saved -> {RESULTS_PATH}")
    print("Validation complete. Save these numbers for Paper A Section IV.")


if __name__ == "__main__":
    if "--hardware" in sys.argv:
        run_hardware()
    else:
        run_dry()
