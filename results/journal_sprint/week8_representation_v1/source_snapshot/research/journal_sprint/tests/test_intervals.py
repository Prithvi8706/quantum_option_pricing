import itertools

import numpy as np
import pytest
from scipy.stats import binom

from research.journal_sprint.intervals import (
    ConfidenceSet,
    clopper_pearson,
    invert,
    price_decision,
    response,
    sine_preimage,
)
from research.journal_sprint.storage import rng_for, start_run


def test_preimage_keeps_all_aliases():
    intervals = sine_preimage(0.3, 0.4, 8)
    assert len(intervals) > 8
    theta = np.linspace(0, np.pi / 2, 10001)
    truth = (np.sin(17 * theta) ** 2 >= 0.3) & (np.sin(17 * theta) ** 2 <= 0.4)
    included = np.array([any(lo <= t <= hi for lo, hi in intervals) for t in theta])
    assert np.array_equal(included, truth)


def test_endpoint_counts():
    lo, hi = clopper_pearson([0, 10], [10, 10], 0.05)
    assert lo[0] == 0 and hi[1] == 1
    assert invert([0], [10], [0]).contains(0)
    assert invert([10], [10], [0]).contains(1)


@pytest.mark.parametrize("a", [0.0, 0.01, 0.1, 0.3, 0.5, 0.9, 1.0])
def test_noise_envelope_encloses_matched_set(a):
    depths = [0, 1, 2, 4, 8]
    counts = np.round(response(a, depths, 0.01) * 1000).astype(int)
    matched = invert(counts, [1000] * 5, depths, (0.01, 0.01))
    envelope = invert(counts, [1000] * 5, depths, (0.005, 0.015))
    assert matched.contains(a) and envelope.contains(a)
    for lo, hi in matched.components:
        assert any(e_lo <= lo and hi <= e_hi for e_lo, e_hi in envelope.components)


@pytest.mark.parametrize("a", [0.0, 0.01, 0.1, 0.3, 0.5, 0.8, 0.99, 1.0])
def test_exact_small_sample_joint_coverage(a):
    depths, shots = [0, 2], [4, 4]
    probabilities = response(a, depths, 0.02)
    coverage = 0.0
    for counts in itertools.product(range(5), repeat=2):
        probability = np.prod(binom.pmf(counts, shots, probabilities))
        if invert(counts, shots, depths, (0.01, 0.03)).contains(a):
            coverage += probability
    assert coverage >= 0.95 - 1e-12


def test_incompatible_and_no_signal():
    assert not invert([0, 10000], [10000, 10000], [0, 1]).components
    assert invert([50], [100], [2], (1.0, 1.0)).hull == (0.0, 1.0)
    assert not invert([0], [100], [2], (1.0, 1.0)).components


def test_price_units_and_bias():
    c = ConfidenceSet(((0.4, 0.42),), 0.05)
    assert price_decision(c, 1, bias_bound=0.1)["status"] == "precision_met"
    assert price_decision(c, 100, bias_bound=0.1)["status"] == "unresolved"
    assert price_decision(ConfidenceSet((), 0.05), 100)["status"] == "incompatible"


@pytest.mark.parametrize(
    "args",
    [
        ([2], [1], [0]),
        ([0], [0], [0]),
        ([0.5], [1], [0]),
        ([0], [1], [-1]),
        ([0], [1], [0, 1]),
    ],
)
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        invert(*args)


def test_bad_envelope_and_alpha():
    with pytest.raises(ValueError):
        invert([1], [2], [0], (0.1, 0.01))
    with pytest.raises(ValueError):
        invert([1], [2], [0], alpha=2)
    with pytest.raises(ValueError):
        invert([1, 1], [2, 2], [0, 1], alpha=1.5)


def test_ideal_circuit_response():
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator, Statevector

    z = np.diag([1.0, -1.0])
    for a in (0.01, 0.1, 0.3, 0.5, 0.9, 0.99):
        circuit = QuantumCircuit(1)
        circuit.ry(2 * np.arcsin(np.sqrt(a)), 0)
        unitary = Operator(circuit).data
        grover = -unitary @ z @ unitary.conj().T @ z
        state = Statevector.from_instruction(circuit).data
        for k in (0, 1, 2, 4, 8):
            actual = abs((np.linalg.matrix_power(grover, k) @ state)[1]) ** 2
            assert actual == pytest.approx(response(a, [k])[0], abs=1e-12)


def test_streams_and_exclusive_storage(tmp_path):
    assert rng_for("pilot", 1).random() == rng_for("pilot", 1).random()
    assert rng_for("pilot", 1).random() != rng_for("validation", 1).random()
    start_run(tmp_path / "run", {"test": True})
    with pytest.raises(FileExistsError):
        start_run(tmp_path / "run", {"test": True})
