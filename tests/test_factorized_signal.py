"""Small actual-circuit checks; joint enumeration exists only in these tests."""

import numpy as np
import pytest

pytest.importorskip("qiskit")
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator

from research.journal_sprint.combined_qsp import response
from research.journal_sprint.factorized_signal import (
    FactorizedSignal,
    phased_walk_circuit,
    projected_phase,
    signal_circuit,
    walk_circuit,
)


def direct_signal(plan):
    values = []
    for word in range(1 << plan.path_qubits):
        z = np.array([plan.nodes[j, (word >> (j*plan.q)) & ((1 << plan.q)-1)]
                      for j in range(plan.d)])
        values.append((np.mean(np.exp(plan.means + plan.factor @ z))-plan.strike)/plan.B)
    return np.array(values)


@pytest.fixture(scope="module", params=[(1, 1), (1, 2), (2, 1), (2, 2)])
def small_signal(request):
    d, q = request.param
    plan = FactorizedSignal([.1, -.2][:d], np.array([[.3, -.15], [-.2, .25]])[:d, :d],
                            strike=.8, q=q, L=1.5)
    circuit = signal_circuit(plan)
    return plan, circuit, Operator(circuit).data


def test_actual_signal_hermitian_involution_block_and_garbage(small_signal):
    plan, _, unitary = small_signal
    n = 1 << plan.path_qubits
    np.testing.assert_allclose(unitary, unitary.conj().T, atol=2e-12)
    np.testing.assert_allclose(unitary @ unitary, np.eye(len(unitary)), atol=3e-12)
    expected = direct_signal(plan)
    np.testing.assert_allclose(unitary[:n, :n], np.diag(expected), atol=2e-12)
    # Garbage has the complementary norm; no uncomputation/clean-output claim.
    np.testing.assert_allclose(np.sum(abs(unitary[n:, :n])**2, axis=0),
                               1-expected**2, atol=3e-12)
    assert np.linalg.norm(unitary[n:, :n]) > .1


def test_actual_phased_walk_matches_complex_response(small_signal):
    plan, _, unitary = small_signal
    n = 1 << plan.path_qubits
    walk = Operator(walk_circuit(plan)).data
    reflected = unitary.copy()
    reflected[n:, :] *= -1
    np.testing.assert_allclose(walk, reflected, atol=3e-12)
    for phases in ([.31], [.21, -.37], [.4, -.7, .2], [.17, .8, -.31, .52]):
        actual = Operator(phased_walk_circuit(plan, phases)).data[:n, :n]
        expected = np.diag(response(direct_signal(plan), phases))
        np.testing.assert_allclose(actual, expected, atol=8e-12)
        np.testing.assert_allclose(actual.real, expected.real, atol=8e-12)


@pytest.mark.parametrize("good", [(0,), (2, 0), (0, 1, 2)])
def test_projected_phase_including_controlled_global_phase(good):
    phi = .371
    circuit = projected_phase(3, good, phi)
    diagonal = [np.exp(1j*phi*(1 if all((k >> j) & 1 == 0 for j in good) else -1))
                for k in range(8)]
    np.testing.assert_allclose(Operator(circuit).data, np.diag(diagonal), atol=1e-14)
    controlled = QuantumCircuit(4)
    controlled.append(circuit.to_gate().control(), [3, 0, 1, 2])
    np.testing.assert_allclose(Operator(controlled).data,
                               np.diag([1]*8 + diagonal), atol=1e-14)


def test_endpoint_nodes_zero_factor_and_zero_strike():
    for factor, strike in (([[0.]], 0.), ([[-.3]], .7)):
        plan = FactorizedSignal([.2], factor, strike, 1, 2., nodes=[-2., 2.])
        unitary = Operator(signal_circuit(plan)).data
        np.testing.assert_allclose(unitary[:2, :2], np.diag(direct_signal(plan)), atol=1e-12)
        np.testing.assert_allclose(unitary @ unitary, np.eye(8), atol=1e-12)


def test_coordinate_specific_nodes():
    plan = FactorizedSignal([0., .2], [[.1, -.2], [.3, .1]], .9, 1, 2.,
                            nodes=[[-2., .5], [-.3, 2.]])
    actual = Operator(signal_circuit(plan)).data[:4, :4]
    np.testing.assert_allclose(actual, np.diag(direct_signal(plan)), atol=1e-12)


def test_large_plan_never_compiles_or_enumerates_joint_table(monkeypatch):
    import research.journal_sprint.factorized_signal as module

    def forbidden(*args, **kwargs):
        raise AssertionError("resource planning must not construct a circuit")

    monkeypatch.setattr(module, "signal_circuit", forbidden)
    plan = FactorizedSignal(np.zeros(4), np.eye(4)*.2, 1., 10, 4.)
    metadata = plan.resource_metadata()
    assert metadata["marginal_entries"] == 4*4*1024
    assert metadata["total_qubits"] == 47
    assert metadata["lcu_ancillas"] == 3
    assert metadata["compiled_gate_counts"] is None
    assert not metadata["joint_table_enumerated"]
    assert not metadata["clean_ancillas"]
    assert not metadata["uniform_phase_certificate"]
    assert plan.nodes.shape == (4, 1024)
    assert metadata["normalization"] == pytest.approx(np.exp(.8)+1)
    for i in range(4):
        for j in range(4):
            a = plan.marginal_values(i, j)
            assert a.shape == (1024,)
            assert np.all((a >= 0) & (a <= 1))


def test_compile_only_small_circuit():
    plan = FactorizedSignal([.1], [[-.2]], .9, 1, 2.)
    original = phased_walk_circuit(plan, [.2, -.4, .1])
    compiled = transpile(original, basis_gates=["u", "cx"], optimization_level=1)
    np.testing.assert_allclose(Operator(compiled).data, Operator(original).data, atol=2e-12)


@pytest.mark.parametrize("change", [
    {"q": 0}, {"q": True}, {"q": 1.5}, {"means": []}, {"means": [[0.]]},
    {"means": [np.nan]}, {"factor": [[np.inf]]}, {"factor": [[1., 2.]]},
    {"strike": -1.}, {"strike": np.nan}, {"L": 0.}, {"L": np.inf},
    {"nodes": [0.]}, {"nodes": [0., 3.]}, {"nodes": [0., np.nan]},
    {"means": [1000.]}, {"means": [-1000.]},
])
def test_invalid_plan(change):
    args = dict(means=[0.], factor=[[.2]], strike=1., q=1, L=2.)
    args.update(change)
    with pytest.raises(ValueError):
        FactorizedSignal(**args)


@pytest.mark.parametrize("phases", [[], [[0.]], [np.nan], [np.inf]])
def test_invalid_phases(phases):
    with pytest.raises(ValueError):
        phased_walk_circuit(FactorizedSignal([0.], [[.2]], 1., 1, 2.), phases)


@pytest.mark.parametrize("n,good,phi", [
    (0, [0], 0.), (2, [], 0.), (2, [0, 0], 0.), (2, [2], 0.),
    (2, [-1], 0.), (2, [True], 0.), (2, [0], np.nan),
])
def test_invalid_projector(n, good, phi):
    with pytest.raises(ValueError):
        projected_phase(n, good, phi)


def test_invalid_marginal_indices():
    plan = FactorizedSignal([0.], [[.2]], 1., 1, 2.)
    for row, coordinate in [(-1, 0), (0, 1), (True, 0)]:
        with pytest.raises(ValueError):
            plan.marginal_values(row, coordinate)
