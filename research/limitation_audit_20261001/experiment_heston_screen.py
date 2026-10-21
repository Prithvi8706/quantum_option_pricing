"""Test necessary Heston fast-forwarding assumptions against actual local factors."""

import argparse
import math
from dataclasses import asdict
from pathlib import Path

import numpy as np

from research.antithetic_feasibility.classical import MODELS, factors
from research.limitation_audit_20261001.experiment_lookup import dump


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for model in MODELS:
        u, av, ash, asi = factors(model)
        variance = (u * av ** 2) @ u.T
        equity = (u * (ash ** 2 + asi ** 2)) @ u.T
        cross = (u * (ash * av)) @ u.T
        eye = np.eye(model.assets)
        c = (1 - model.correlation) * eye + model.correlation * np.ones_like(eye)
        assert np.max(np.abs(variance - (model.leverage ** 2 * c
                              + (1 - model.leverage ** 2) * eye))) < 1e-12
        assert np.max(np.abs(equity - c)) < 1e-12
        assert np.max(np.abs(cross - model.leverage * c)) < 1e-12
        offdiag_v = float(np.max(np.abs(variance - np.diag(np.diag(variance)))))
        offdiag_x = float(np.max(np.abs(cross - np.diag(np.diag(cross)))))
        eta = 4 * model.kappa * model.theta / model.xi ** 2
        # This necessary sign condition is independent of Delta or time units.
        tail_middle = (2 * model.kappa * model.xi * model.leverage
                       - model.leverage ** 2 * model.xi ** 2)
        # Paper's standardized transition uses physical duration 2*Delta.
        delta = model.maturity / model.dates / 2
        truncation = dict(
            delta_at_least_one=delta >= 1,
            sum_exponentials_less_than_one=(math.exp(-model.kappa * delta / 2)
                                           + math.exp(-model.kappa * delta)) < 1,
            kappa_squared_gt_middle_ge_zero=model.kappa ** 2 > tail_middle >= 0,
            final_inequality=((1 + math.exp(-2 * model.kappa * delta)) / 4
                 + model.leverage * model.xi / model.kappa
                 * (1 - math.exp(-2 * model.kappa * delta)) / 4)
                 < 1 / (2 * (1 + math.exp(-model.kappa * delta / 2))),
        )
        rows.append(dict(model=asdict(model), eta=eta, eta_at_least_five=eta >= 5,
                         variance_covariance=variance.tolist(),
                         equity_variance_cross_covariance=cross.tolist(),
                         largest_offdiagonal_variance_covariance=offdiag_v,
                         largest_cross_asset_equity_variance_covariance=offdiag_x,
                         correlation_form_matches=(offdiag_v < 1e-12 and offdiag_x < 1e-12),
                         tail_middle=tail_middle, native_time_delta=delta,
                         literal_truncation_conditions=truncation,
                         direct_transfer_of_full_stated_bound=False))
    assert all(row["tail_middle"] < 0 for row in rows)
    assert rows[0]["correlation_form_matches"] and not rows[1]["correlation_form_matches"]
    result = dict(cases=rows, passed=True,
        paper="https://arxiv.org/html/2602.03725v1#S6.SS2.SSS2",
        disposition="Reject a direct use of this paper's stated full bound for the "
        "current cases. A1 passes eta and covariance, but not the literal sufficient "
        "truncation hypotheses. A4 additionally has incompatible variance correlations.",
        scope="Failure of sufficient hypotheses is not an impossibility result. "
        "A new negative-leverage tail proof may apply. Time rescaling must transform "
        "all SDE parameters; it cannot change the negative sign of tail_middle.",
        payoff="Vanilla arithmetic basket/Asian calls are piecewise linear in spots; "
        "the knock-out contracts additionally fail the cited Lipschitz payoff premise.")
    dump(output / "summary.json", result)
    print([(row["model"]["name"], row["eta"],
            row["largest_offdiagonal_variance_covariance"], row["tail_middle"])
           for row in rows])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
