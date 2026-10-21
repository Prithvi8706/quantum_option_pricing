"""Execute an exact finite-law measure change and test a tempting wrong sampler."""

import argparse
import math
from pathlib import Path

import numpy as np
from scipy.special import ndtr

from research.limitation_audit_20261001.experiment_lookup import dump


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    size, cutoff = 128, 6
    edges = np.linspace(-cutoff, cutoff, size + 1)
    grid = (edges[:-1] + edges[1:]) / 2
    p = np.diff(ndtr(edges))
    p /= p.sum()
    points = np.stack(np.meshgrid(grid, grid, indexing="ij"), axis=-1)
    law = p[:, None] * p[None, :]
    loadings = np.array([[.3, 0], [.3 * .4, .3 * math.sqrt(1 - .4 ** 2)]])
    mu = np.log(100) + .03 - .5 * np.sum(loadings ** 2, axis=1)
    weights = np.array([.5, .5])
    stocks = np.exp(mu + points @ loadings.T)
    average = stocks @ weights
    strike, barrier, discount = 100., 140., math.exp(-.03)
    event = (average > strike) & (np.max(stocks, axis=-1) < barrier)
    m = float(np.sum(law * average))
    tilted_law = law * average / m
    direct = discount * float(np.sum(law * (average - strike) * event))
    original_probability = float(np.sum(law * event))
    tilted_probability = float(np.sum(tilted_law * event))
    decomposed = discount * (m * tilted_probability - strike * original_probability)
    assert abs(direct - decomposed) < 1e-12
    # Construct an exact finite mixture sampler. Each tilted coordinate remains
    # independent within a component, but it is not just a shifted CDF bin law.
    coordinate_laws, component_means = [], []
    for j in range(2):
        qs = [p * np.exp(loadings[j, k] * grid) for k in range(2)]
        means = [q.sum() for q in qs]
        coordinate_laws.append([q / q.sum() for q in qs])
        component_means.append(math.exp(mu[j]) * np.prod(means))
    mix = weights * component_means
    mix /= mix.sum()
    mixture_law = sum(mix[j] * coordinate_laws[j][0][:, None]
                      * coordinate_laws[j][1][None, :] for j in range(2))
    assert float(np.max(np.abs(mixture_law - tilted_law))) < 1e-15
    # Run the sampler too; compare its empirical probability to the known one.
    rng = np.random.default_rng(20261003)
    count = 131072
    labels = rng.choice(2, size=count, p=mix)
    sampled_event = np.zeros(count, bool)
    for j in range(2):
        selected = np.flatnonzero(labels == j)
        x = rng.choice(size, size=len(selected), p=coordinate_laws[j][0])
        y = rng.choice(size, size=len(selected), p=coordinate_laws[j][1])
        sampled_event[selected] = event[x, y]
    sample_probability = float(sampled_event.mean())
    se = math.sqrt(tilted_probability * (1 - tilted_probability) / count)
    assert abs(sample_probability - tilted_probability) < 6 * se
    # Negative control: Gaussian shifts are exact for the continuous identity,
    # but plugging them into this finite binned model silently changes its law.
    m_continuous_components = np.exp(mu + .5 * np.sum(loadings ** 2, axis=1))
    continuous_mix = weights * m_continuous_components
    continuous_mix /= continuous_mix.sum()
    wrong_law = np.zeros_like(law)
    for j in range(2):
        qs = [np.diff(ndtr(edges - loadings[j, k])) for k in range(2)]
        qs = [q / q.sum() for q in qs]
        wrong_law += continuous_mix[j] * qs[0][:, None] * qs[1][None, :]
    wrong_tv = float(.5 * np.abs(wrong_law - tilted_law).sum())
    wrong_price = discount * (m * float(np.sum(wrong_law * event))
                              - strike * original_probability)
    assert wrong_tv > 1e-7
    # Explicit joint error ledger; normalization must itself be certified before
    # these symbolic guarantees become a numerical price certificate.
    epsilon, alpha = .01, .01
    c1, c2 = discount * m, discount * strike
    dollar_errors = epsilon * np.sqrt([c1, c2]) / np.sqrt([c1, c2]).sum()
    probability_errors = dollar_errors / [c1, c2]
    bounded_payoff_range = discount * (barrier - strike)
    inverse_precision_sum = float(np.sum(1 / probability_errors))
    direct_inverse_precision = bounded_payoff_range / epsilon
    result = dict(passed=True, finite_grid=dict(points=size ** 2, cutoff=cutoff),
        direct_price=direct, decomposed_price=decomposed, identity_error=abs(direct - decomposed),
        finite_normalization=m, continuous_normalization=float(weights @ m_continuous_components),
        probabilities=dict(original=original_probability, tilted=tilted_probability),
        mixture_max_probability_error=float(np.max(np.abs(mixture_law - tilted_law))),
        sampled_paths=count, sampled_tilted_probability=sample_probability,
        sampler_standard_error=se,
        naive_shifted_grid_negative_control=dict(total_variation=wrong_tv,
                                                price_error=wrong_price - direct),
        joint_ledger=dict(dollar_target=epsilon, total_failure_probability=alpha,
            coefficient_values=[c1, c2], absolute_probability_errors=probability_errors.tolist(),
            per_estimate_failure_probabilities=[alpha / 2, alpha / 2],
            triangle_bound=float(np.dot([c1, c2], probability_errors)),
            required_extra_errors="If m is approximate, add discount*|m_hat-m|; "
            "also add preparation, grid, arithmetic and continuous-law errors."),
        simple_query_screen=dict(assumption="Equal source cost and equal constants for "
            "a 1/probability-error bounded estimator; not an executed quantum estimator",
            decomposition_inverse_precision_sum=inverse_precision_sum,
            direct_inverse_precision=direct_inverse_precision,
            decomposition_over_direct=inverse_precision_sum / direct_inverse_precision),
        disposition="Keep the exact identity and finite sampler. Do not replace the "
        "current pricing source: this bounded barrier example worsens the simple query "
        "precision budget, and both indicators still need the asset arithmetic.",
        certification="Algebraic finite-law identity and numerical checks completed. "
        "A certified rotation sampler, normalizer intervals and dollar-error bridge are not.")
    dump(output / "summary.json", result)
    print("Finite-law identity PASS", result["identity_error"],
          "naive shift TV", wrong_tv, "query screen ratio",
          result["simple_query_screen"]["decomposition_over_direct"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
