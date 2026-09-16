import numpy as np
import pytest
from numpy.polynomial.chebyshev import chebval

from research.journal_sprint.combined_representation import (
    fwht, parity_matrix, discovery_vector, quantum_discovery, rank_words,
    fit_control, greedy_words, mps_diagnostic,
)
from research.journal_sprint.combined_qsp import (
    abs_polynomial, response, synthesize, qsp_circuit, lcu_circuit,
    hadamard_mean, weighted_depth,
)


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_fourier_circuit_against_complete_classical_transform(bits):
    rng = np.random.default_rng(bits)
    vector = rng.normal(size=1 << bits)
    vector /= np.linalg.norm(vector)
    _, probabilities, error = quantum_discovery(vector)
    transform = parity_matrix(bits).T @ vector
    assert np.allclose(fwht(vector), transform)
    assert np.allclose(probabilities, transform**2/len(vector))
    assert error < 1e-10


def test_discovery_cannot_read_holdout_labels():
    payoff = np.arange(16, dtype=float)
    training = np.arange(16) < 8
    weights = np.ones(16)/16
    before = discovery_vector(payoff, weights, training)
    payoff[~training] = 1e10
    assert np.array_equal(before, discovery_vector(payoff, weights, training))


def test_full_pool_classical_recovers_planted_high_order_word():
    features = parity_matrix(4)
    payoff = 3+2*features[:, 15]
    weights, training = np.ones(16)/16, np.arange(16) != 3
    assert greedy_words(payoff, weights, training, features, 1) == [15]
    fit = fit_control(payoff, weights, training, features[:, [15]])
    assert fit["residual_sd"] < 1e-12
    assert fit["control_expectation"] == pytest.approx(3)


@pytest.mark.parametrize("degree", [4, 8])
def test_abs_polynomial_and_synthesized_qsp(degree):
    coefficients, tail = abs_polynomial(degree)
    mesh = np.linspace(-1, 1, 4097)
    approximation = chebval(mesh, coefficients)
    assert np.max(abs(approximation)) <= 1
    assert np.max(abs((1+tail)*approximation-abs(mesh))) <= tail+1e-14
    plan = synthesize(degree)
    assert plan["fit_accepted"]
    assert not plan["uniform_phase_certificate"]
    signal = np.array([-.9, -.2, .4, 1.])
    weights = np.array([.1, .2, .3, .4])
    actual, _ = hadamard_mean(qsp_circuit(signal, plan["phases"]), weights)
    assert actual == pytest.approx(weights @ response(signal, plan["phases"]).real, abs=1e-10)


def test_coherent_lcu_recovers_signed_controlled_payoff():
    plan = synthesize(4)
    signal = np.array([-.8, -.1, .3, .9])
    weights = np.array([.1, .2, .3, .4])
    coefficients, words, factor = [1.2, -.7], [3], 2.
    circuit, beta = lcu_circuit(signal, plan["phases"], factor, plan["abs_rescale"], coefficients, words)
    control = coefficients[0]+coefficients[1]*parity_matrix(2)[:, 3]
    call = factor*(signal+plan["abs_rescale"]*response(signal, plan["phases"]).real)
    actual, _ = hadamard_mean(circuit, weights)
    assert actual*beta == pytest.approx(weights @ (call-control), abs=1e-9)
    assert beta == pytest.approx(factor*(1+plan["abs_rescale"])+sum(abs(c) for c in coefficients))


@pytest.mark.parametrize("bond", [1, 2, 4])
def test_mps_exact_product(bond):
    amplitudes = np.ones(16)/4
    diagnostic = mps_diagnostic(amplitudes, bond)
    assert diagnostic["observed_vector_error"] < 1e-12
    assert not diagnostic["circuit_synthesized"]


def test_weighted_critical_path_not_gate_sum():
    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.h(1)
    circuit.cx(0, 1)
    assert weighted_depth(circuit, {"h": 1, "cx": 10}) == 11
    with pytest.raises(ValueError):
        weighted_depth(circuit, {"h": 1})


@pytest.mark.parametrize("values", [[1, 2, 3], [np.nan, 1], []])
def test_bad_fourier_inputs(values):
    with pytest.raises(ValueError):
        fwht(values)


def test_ranking_ties_are_deterministic():
    assert rank_words(np.ones(16), 4) == [1, 2, 3, 4]


def test_factorized_moments_and_control_against_joint_enumeration():
    from research.journal_sprint.polynomial_residual import basket_moments, polynomial_control
    means = np.array([1., 1.1])
    factor = np.array([[.2, -.1], [.1, .3]])
    nodes, marginal = np.array([-1., 1.]), np.array([.4, .6])
    normals = np.array([[-1., -1.], [-1., 1.], [1., -1.], [1., 1.]])
    weights = np.array([.16, .24, .24, .36])
    values = np.exp(means+normals @ factor.T).mean(axis=1)
    moments, terms = basket_moments(means, factor, nodes, marginal, 4)
    assert terms == 15
    assert moments == pytest.approx([weights @ values**k for k in range(5)])
    control, expectation = polynomial_control(values, 3, 4, .97, moments)
    assert expectation == pytest.approx(weights @ control, abs=1e-12)


def test_pre_normalized_residual_qsp_reduces_scale_at_identical_polynomial():
    from research.journal_sprint.polynomial_residual import residual_synthesis
    residual = residual_synthesis(8)
    assert residual["fit_accepted"]
    high, high_tail = abs_polynomial(8)
    low, low_tail = abs_polynomial(4)
    x = np.linspace(-1, 1, 257)
    target = (1+high_tail)*chebval(x, high)-(1+low_tail)*chebval(x, low)
    assert np.max(abs(target-residual["rho"]*response(x, residual["phases"]).real)) < 1e-8
    assert residual["rho"] < .1


def test_runner_failure_keeps_artifacts_and_refuses_reuse(tmp_path, monkeypatch):
    from research.journal_sprint import run_combined_development as runner
    def fail(*args):
        raise ArithmeticError("injected grid error")
    monkeypatch.setattr(runner, "grid", fail)
    target = tmp_path/"run"
    with pytest.raises(ArithmeticError, match="injected"):
        runner.run(target)
    assert (target/"planned.json").exists()
    assert (target/"failed.json").exists()
    assert not (target/"complete.json").exists()
    with pytest.raises(FileExistsError):
        runner.run(target)
