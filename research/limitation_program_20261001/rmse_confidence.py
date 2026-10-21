"""Finite confidence conversion of a proved RMSE, without invented query costs."""

from fractions import Fraction

from research.limitation_program_20261001.barrier_band_certificate import exact, pair, sqrt_interval
from research.limitation_program_20261001.financial_bounded_schedule import binomial_majority_tail


def conversions(error=Fraction(9, 2000), failure=Fraction(3, 1000), max_repetitions=101):
    error, failure = exact(error), exact(failure)
    if error <= 0 or not 0 < failure < Fraction(1, 2):
        raise ValueError("Positive dollar allowance and failure below one half required")
    if type(max_repetitions) is not int or max_repetitions < 1:
        raise ValueError("Positive finite repetition cap required")
    safe_single, enclosure_hi = sqrt_interval(error**2 * failure)
    assert safe_single**2 <= error**2 * failure
    chosen = next(
        (
            r
            for r in range(1, max_repetitions + 1, 2)
            if binomial_majority_tail(r, Fraction(1, 4)) <= failure
        ),
        None,
    )
    return dict(
        statistical_error_dollars_exact=pair(error),
        failure_allowance_exact=pair(failure),
        one_run=dict(
            RMSE_target_squared_dollars_exact=pair(error**2 * failure),
            RMSE_target_dollars_interval_exact=[pair(safe_single), pair(enclosure_hi)],
            safe_rational_RMSE_target_dollars_exact=pair(safe_single),
            repetitions=1,
            proof="Markov applied to squared error: P(abs(Z-mu)>e)<=RMSE^2/e^2",
            requires_unbiasedness=False,
            quantum_query_or_runtime_cost=None,
        ),
        independent_median=dict(
            per_run_RMSE_target_dollars_exact=pair(error / 2),
            per_run_bad_probability_upper_exact=[1, 4],
            repetitions=chosen,
            certified_failure_upper_exact=(
                pair(binomial_majority_tail(chosen, Fraction(1, 4))) if chosen else None
            ),
            proof=(
                "Each bad-run probability is at most1/4 by squared-error Markov. "
                "Independent bad indicators are stochastically dominated by "
                "independent Bernoulli(1/4); an incorrect median requires a majority."
            ),
            independent_fresh_runs_required=True,
            source_inverse_preparation_readout_reset_multiplicity=chosen,
            complete_quantum_cost=None,
        ),
        construction_with_proved_RMSE_cost_supplied=False,
        cheaper_complete_conversion_selected=False,
        RMSE_equals_dollar_allowance_is_not_a_failure_certificate=True,
        original_continuous_price_bias_covered=False,
    )
