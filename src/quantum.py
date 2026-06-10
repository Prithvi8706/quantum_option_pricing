import time

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit_finance.circuit.library import EuropeanCallPricingObjective, LogNormalDistribution


def _build_circuit(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 3,
) -> tuple[QuantumCircuit, EuropeanCallPricingObjective]:
    # Very low sigma (< ~0.15) causes two Qiskit errors:
    #   "Breakpoints must be included in domain"  — K falls outside the tight ±3σ bounds
    #   "Breakpoints must be unique and sorted"   — 2^n grid points collapse at the mean
    # Clamp to 0.15 before all circuit construction; prices for sigma < 0.15 are
    # returned as the sigma=0.15 approximation (acceptable for dashboard display).
    sigma = max(sigma, 0.15)

    mu_ln = (r - 0.5 * sigma**2) * T + np.log(S0)
    sigma_ln = sigma * np.sqrt(T)
    sigma_var = sigma_ln**2

    # Support bounds: mean ± 3σ in stock-price space.
    # Also ensure K is within the domain — for deep OTM/ITM + short T + low vol
    # the ±3σ window can be too narrow to include the strike, causing Qiskit to
    # raise "Breakpoints must be included in domain" / "must be unique and sorted".
    mean_stock = np.exp(mu_ln + 0.5 * sigma_var)
    var_stock = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
    std_stock = np.sqrt(var_stock)
    low = max(0.0, min(mean_stock - 3 * std_stock, K * 0.98))
    high = max(mean_stock + 3 * std_stock, K * 1.02)
    bounds = (low, high)

    uncertainty_model = LogNormalDistribution(
        num_uncertainty_qubits,
        mu=mu_ln,
        sigma=sigma_var,
        bounds=bounds,
    )

    # c_approx = 0.25 keeps the rotation angle well inside [0, π/2] for typical params.
    # EuropeanCallPricingObjective does not accept uncertainty_model directly;
    # we compose the two circuits manually below.
    c_approx = 0.25
    payoff_circuit = EuropeanCallPricingObjective(
        num_state_qubits=num_uncertainty_qubits,
        strike_price=K,
        rescaling_factor=c_approx,
        bounds=bounds,
    )

    full_circuit = QuantumCircuit(payoff_circuit.num_qubits)
    full_circuit.append(uncertainty_model, range(num_uncertainty_qubits))
    full_circuit.append(payoff_circuit, range(payoff_circuit.num_qubits))

    return full_circuit, payoff_circuit


def quantum_call(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 3,
    epsilon: float = 0.01,
    alpha: float = 0.05,
) -> tuple[float, tuple[float, float], float, int]:
    """
    Price a European call option using Iterative Quantum Amplitude Estimation.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)
    num_uncertainty_qubits : Qubits to discretise the log-normal distribution.
                             3 = fast (demo), 5 = more accurate.
    epsilon : Target half-width precision for IAE on the normalised amplitude.
    alpha   : Significance level for the returned confidence interval.

    Returns
    -------
    price          : float — discounted expected payoff (option price)
    conf_int       : (float, float) — (1-alpha) confidence interval on the price
    elapsed        : float — wall-clock seconds for the QAE run
    oracle_queries : int — number of oracle calls used by IAE (for speedup chart)
    """
    t0 = time.perf_counter()

    full_circuit, payoff_circuit = _build_circuit(S0, K, r, sigma, T, num_uncertainty_qubits)

    # The objective qubit is the single qubit in the second register (q1), at index n
    objective_qubit = num_uncertainty_qubits

    # Amplitude estimation
    problem = EstimationProblem(
        state_preparation=full_circuit,
        objective_qubits=[objective_qubit],
        post_processing=payoff_circuit.post_processing,
    )

    iae = IterativeAmplitudeEstimation(
        epsilon_target=epsilon,
        alpha=alpha,
        sampler=Sampler(),
    )
    result = iae.estimate(problem)

    # Discount back to present value
    discount = np.exp(-r * T)
    price = max(0.0, result.estimation_processed) * discount
    ci_raw = result.confidence_interval_processed
    conf_int = (max(0.0, ci_raw[0]) * discount, ci_raw[1] * discount)

    elapsed = time.perf_counter() - t0
    # num_oracle_queries is always 0 with the statevector Sampler (shots=None).
    # Derive from result.powers: each IAE round with power k uses 2k+1 oracle calls.
    oracle_queries = sum(2 * k + 1 for k in result.powers)
    return price, conf_int, elapsed, oracle_queries


def _build_digital_circuit(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 5,
) -> tuple[QuantumCircuit, int]:
    # Same sigma clamp as _build_circuit: very low sigma causes Qiskit domain errors.
    sigma = max(sigma, 0.15)

    mu_ln = (r - 0.5 * sigma**2) * T + np.log(S0)
    sigma_ln = sigma * np.sqrt(T)
    sigma_var = sigma_ln**2

    mean_stock = np.exp(mu_ln + 0.5 * sigma_var)
    var_stock = (np.exp(sigma_var) - 1) * np.exp(2 * mu_ln + sigma_var)
    std_stock = np.sqrt(var_stock)
    low = max(0.0, min(mean_stock - 3 * std_stock, K * 0.98))
    high = max(mean_stock + 3 * std_stock, K * 1.02)

    uncertainty_model = LogNormalDistribution(
        num_uncertainty_qubits,
        mu=mu_ln,
        sigma=sigma_var,
        bounds=(low, high),
    )

    # Step function: f(x) = 0 for x < K, f(x) = 1 for x >= K.
    # rescaling_factor=1.0 is exact for binary payoff (no Woerner approximation).
    # breakpoints=[low, K] puts K on the >= side (pays 1 at S_T = K).
    digital_obj = LinearAmplitudeFunction(
        num_state_qubits=num_uncertainty_qubits,
        slope=[0, 0],
        offset=[0, 1],
        domain=(low, high),
        image=(0, 1),
        breakpoints=[low, K],
        rescaling_factor=1.0,
    )

    full_circuit = QuantumCircuit(digital_obj.num_qubits)
    full_circuit.append(uncertainty_model, range(num_uncertainty_qubits))
    full_circuit.append(digital_obj, range(digital_obj.num_qubits))

    return full_circuit, num_uncertainty_qubits


def quantum_digital_call(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    num_uncertainty_qubits: int = 5,
    epsilon: float = 0.01,
    alpha: float = 0.05,
) -> tuple[float, tuple[float, float], float, int]:
    """
    Price a European digital (cash-or-nothing) call via IQAE.

    Parameters
    ----------
    S0    : Initial stock price
    K     : Strike price
    r     : Risk-free interest rate (annualised)
    sigma : Volatility (annualised)
    T     : Time to expiry (years)
    num_uncertainty_qubits : Qubits to discretise the log-normal distribution.
    epsilon : IQAE target half-width precision.
    alpha   : Significance level for the confidence interval.

    Returns
    -------
    price          : float — discounted P(S_T > K on n-qubit grid) = grid_true_price
    conf_int       : (float, float) — (1-alpha) CI on the price
    elapsed        : float — wall-clock seconds
    oracle_queries : int — sum(2k+1 for k in result.powers)

    Note: price converges to grid_true_price (exact probability on the n-qubit
    grid), NOT to the continuous digital_bs_price. Grid bias at n=5 ≈ 2.16e-02
    at standard params (S0=K=100, r=0.05, sigma=0.2, T=1.0) — a fixed
    systematic offset independent of epsilon.

    Implementation note: post_processing=lambda a: a (identity). In Qiskit
    0.3.1, IQAE reports result.estimation = P(obj=|1>) directly (the probability,
    not the amplitude sqrt(P)). Confirmed empirically: result.estimation=grid_p.
    LinearAmplitudeFunction.post_processing is NOT used here.
    """
    t0 = time.perf_counter()

    full_circuit, objective_qubit = _build_digital_circuit(
        S0, K, r, sigma, T, num_uncertainty_qubits
    )

    problem = EstimationProblem(
        state_preparation=full_circuit,
        objective_qubits=[objective_qubit],
        post_processing=lambda a: a,  # identity: IQAE returns P(obj=1) = grid_p
    )

    iae = IterativeAmplitudeEstimation(
        epsilon_target=epsilon,
        alpha=alpha,
        sampler=Sampler(),
    )
    result = iae.estimate(problem)

    discount = np.exp(-r * T)
    price = result.estimation_processed * discount
    ci_raw = result.confidence_interval_processed
    conf_int = (max(0.0, ci_raw[0]) * discount, min(1.0, ci_raw[1]) * discount)

    elapsed = time.perf_counter() - t0
    oracle_queries = sum(2 * k + 1 for k in result.powers)
    return price, conf_int, elapsed, oracle_queries
