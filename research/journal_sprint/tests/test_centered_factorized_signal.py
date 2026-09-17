"""Small operator checks and bounded resource planning; no hardware calls."""

import math

import numpy as np
import pytest

from research.journal_sprint import centered_factorized_signal as centered
from research.journal_sprint.combined_qsp import response
from research.journal_sprint.factorized_signal import FactorizedSignal


def operator(circuit):
    quantum_info = pytest.importorskip("qiskit.quantum_info")
    return quantum_info.Operator(circuit).data


def direct_signal(plan):
    # Joint enumeration is restricted to these tiny tests.
    return np.array([
        (np.mean(np.exp(plan.means + plan.factor @ np.array([
            plan.nodes[j, (word >> (j*plan.q)) & ((1 << plan.q)-1)]
            for j in range(plan.d)]))) - plan.strike)/plan.B
        for word in range(1 << plan.path_qubits)])


@pytest.fixture(scope="module", params=[(1, .8), (1, 2.), (2, .8), (2, 2.)])
def small(request):
    d, strike = request.param
    plan = centered.CenteredFactorizedSignal(
        [.1, -.2][:d], np.array([[.3, -.15], [-.2, .25]])[:d, :d],
        strike, 1, 1.5, nodes=np.array([[-1.5, .7], [-.4, 1.5]])[:d])
    circuit = centered.signal_circuit(plan)
    return plan, circuit, operator(circuit)


def test_actual_hermiticity_involution_and_original_block(small):
    plan, _, unitary = small
    n = 1 << plan.path_qubits
    np.testing.assert_allclose(unitary, unitary.conj().T, atol=3e-12)
    np.testing.assert_allclose(unitary @ unitary, np.eye(len(unitary)), atol=4e-12)
    expected = direct_signal(plan)
    np.testing.assert_allclose(unitary[:n, :n], np.diag(expected), atol=3e-12)
    np.testing.assert_allclose(np.sum(abs(unitary[n:, :n])**2, axis=0),
                               1-expected**2, atol=4e-12)


def test_unused_indices_and_absent_coordinates_select_identity(small):
    plan, circuit, unitary = small
    from qiskit import QuantumCircuit

    prep_circuit = QuantumCircuit(plan.num_qubits)
    prep_circuit.append(circuit.data[0].operation,
                        list(range(plan.path_qubits+plan.d, plan.num_qubits)))
    prep = operator(prep_circuit)
    select = prep @ unitary @ prep.conj().T
    block_size = 1 << (plan.path_qubits+plan.d)
    for k in range(1 << plan.index_bits):
        expected = np.eye(block_size)
        if k == 0:
            expected *= -1 if plan.constant_coefficient < 0 else 1
        elif k <= len(plan.terms):
            row, subset = plan.terms[k-1]
            expected = np.zeros((block_size, block_size))
            for word in range(1 << plan.path_qubits):
                local = np.ones((1, 1))
                for j in reversed(range(plan.d)):
                    r = plan.marginal_values(row, j)[(word >> j) & 1]
                    s = np.sqrt(max(0., 1-r*r))
                    reflection = np.array([[r, s], [s, -r]])
                    local = np.kron(local, reflection if subset & (1 << j) else np.eye(2))
                ids = word + (np.arange(1 << plan.d) << plan.path_qubits)
                expected[np.ix_(ids, ids)] = local
        sl = slice(k*block_size, (k+1)*block_size)
        np.testing.assert_allclose(select[sl, sl], expected, atol=5e-12)


def test_actual_walk_and_complex_qsp_response(small):
    plan, _, unitary = small
    n = 1 << plan.path_qubits
    expected_walk = unitary.copy()
    expected_walk[n:] *= -1
    np.testing.assert_allclose(operator(centered.walk_circuit(plan)), expected_walk, atol=5e-12)
    x = direct_signal(plan)
    assert np.max(abs(x)) <= 1+5e-15
    # Independent floating evaluation can overshoot an exact endpoint by an ulp.
    x = np.clip(x, -1, 1)
    for phases in ([.31], [.2, -.4], [.4, -.7, .2]):
        actual = operator(centered.phased_walk_circuit(plan, phases))[:n, :n]
        np.testing.assert_allclose(actual, np.diag(response(x, phases)),
                                   atol=8e-12)


@pytest.mark.parametrize("q", [2, 10])
def test_dense_d4_resources_marginal_angles_and_old_comparison(q, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("resource planning must not build circuits")

    monkeypatch.setattr(centered, "signal_circuit", forbidden)
    factor = np.full((4, 4), .05)
    factor[::2] *= -1
    plan = centered.CenteredFactorizedSignal(np.zeros(4), factor, 1., q, 4.)
    old = FactorizedSignal(np.zeros(4), factor, 1., q, 4.)
    meta = plan.resource_metadata()
    assert meta["lcu_terms"] == meta["max_lcu_terms"] == 61
    assert meta["lcu_ancillas"] == 6
    assert meta["prep_amplitudes"] == 64
    assert meta["total_qubits"] == 4*q+10
    assert meta["local_reflections"] == 128
    assert meta["marginal_entries"] == 16*(1 << q)
    assert meta["select_angle_entries"] == 128*(1 << q)
    assert meta["compiled_gate_counts"] is None
    for key in ("normalization_certificate", "uniform_phase_certificate",
                "joint_table_enumerated", "clean_ancillas"):
        assert meta[key] is False
    assert plan.B == pytest.approx(old.B-2*min(plan.basket_constant, plan.strike))
    assert plan.B == pytest.approx(math.exp(.8)-1)
    assert plan.B < old.B
    assert plan.nodes.shape == (4, 1 << q)
    assert np.all(plan.coefficients[1:] > 0)
    for i in range(4):
        for j in range(4):
            r = plan.marginal_values(i, j)
            angles = plan.marginal_angles(i, j)
            assert angles.shape == (1 << q,)
            assert np.all((r >= -1) & (r <= 1))
            np.testing.assert_allclose(np.cos(angles/2), r, atol=5e-16)
            np.testing.assert_allclose(math.cosh(.2)+math.sinh(.2)*r,
                                       np.exp(factor[i, j]*plan.nodes[j]), atol=5e-16)
    for k, (i, subset) in enumerate(plan.terms, 1):
        expected = .25*math.prod(math.sinh(.2) if subset & (1 << j)
                                else math.cosh(.2) for j in range(4))
        assert plan.coefficients[k] == pytest.approx(expected)


@pytest.mark.parametrize("b", [.3, -.3, 1e-14, -1e-14, 0.])
def test_marginal_endpoints_tiny_and_zero_factors(b):
    plan = centered.CenteredFactorizedSignal([0.], [[b]], .7, 1, 2., nodes=[-2., 2.])
    expected = [-np.sign(b), np.sign(b)]
    np.testing.assert_allclose(plan.marginal_values(0, 0), expected, atol=5e-16)
    if b == 0:
        assert not plan.terms
        unitary = operator(centered.signal_circuit(plan))
        np.testing.assert_allclose(unitary, np.eye(len(unitary)), atol=1e-14)


def test_zero_constant_and_sparse_zero_coefficients():
    base = centered.CenteredFactorizedSignal([0.], [[.2]], 0., 1, 2.)
    plan = centered.CenteredFactorizedSignal([0.], [[.2]], base.basket_constant, 1, 2.)
    assert plan.constant_coefficient == 0
    np.testing.assert_allclose(operator(centered.signal_circuit(plan))[:2, :2],
                               np.diag(direct_signal(plan)), atol=1e-12)
    sparse = centered.CenteredFactorizedSignal(np.zeros(4), np.eye(4)*.2, 1., 10, 4.)
    assert sparse.resource_metadata()["lcu_terms"] == 5
    assert sparse.resource_metadata()["local_reflections"] == 4


@pytest.mark.parametrize("strike", [0., 2.])
def test_constant_only_signed_block(strike):
    plan = centered.CenteredFactorizedSignal([0.], [[0.]], strike, 1, 2.)
    unitary = operator(centered.signal_circuit(plan))
    np.testing.assert_allclose(unitary[:2, :2], np.diag(direct_signal(plan)), atol=1e-14)
    np.testing.assert_allclose(unitary @ unitary, np.eye(len(unitary)), atol=1e-14)


def test_input_arrays_are_copied_and_readonly():
    means, factor, nodes = np.array([0.]), np.array([[.2]]), np.array([-1., 1.])
    plan = centered.CenteredFactorizedSignal(means, factor, 1., 1, 2., nodes)
    means[:] = 4
    factor[:] = 4
    nodes[:] = 0
    np.testing.assert_array_equal(plan.means, [0.])
    np.testing.assert_array_equal(plan.factor, [[.2]])
    np.testing.assert_array_equal(plan.nodes, [[-1., 1.]])
    for array in (plan.means, plan.factor, plan.nodes, plan.coefficients):
        assert not array.flags.writeable


@pytest.mark.parametrize("change", [
    {"q": 0}, {"q": 11}, {"q": True}, {"q": 1.5}, {"means": []},
    {"means": [0.]*5}, {"means": [[0.]]}, {"means": [np.nan]},
    {"factor": [[np.inf]]}, {"factor": [[.1, .2]]}, {"strike": -1.},
    {"strike": np.inf}, {"L": 0.}, {"L": np.nan}, {"nodes": [0.]},
    {"nodes": [0., 3.]}, {"nodes": [np.nan, 0.]}, {"means": [1000.]},
    {"means": [-1000.]}, {"factor": [[0.]], "strike": 1.},
])
def test_invalid_plan(change):
    args = dict(means=[0.], factor=[[.2]], strike=1., q=1, L=2.)
    args.update(change)
    with pytest.raises(ValueError):
        centered.CenteredFactorizedSignal(**args)


def test_invalid_indices_phases_and_plan_type():
    plan = centered.CenteredFactorizedSignal([0.], [[.2]], 1., 1, 2.)
    for row, coordinate in [(-1, 0), (0, 1), (True, 0)]:
        with pytest.raises(ValueError):
            plan.marginal_values(row, coordinate)
    for phases in ([], [[0.]], [np.nan], [np.inf]):
        with pytest.raises(ValueError):
            centered.phased_walk_circuit(plan, phases)
    with pytest.raises(TypeError):
        centered.signal_circuit(object())
