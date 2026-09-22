"""Independent arithmetic checks for the QqMC literature investigation.

This does not reproduce a quantum simulation or measure quantum hardware.
The linear-family and accounting checks use the settings and conventions in
Recchia et al., arXiv:2609.03625v1, sections 5.2-5.3. The latency table is a
conditional break-even calculation, not a resource estimate.
"""
from pathlib import Path
import json
import platform

import numpy as np
import scipy
from scipy.stats import qmc


def main():
    rows = []
    for weights in ([1.0], [0.9, 0.1]):
        w = np.array(weights)
        exact = float(w.sum() / 2)
        for q in range(1, 7):
            points = qmc.Sobol(d=len(weights), scramble=False).random_base2(q)
            estimate = float((points @ w).mean())
            midpoint = float(np.full(len(weights), 0.5) @ w)
            antithetic = float(((points @ w) + ((1 - points) @ w)).mean() / 2)
            predicted_bias = -float(w.sum()) / (2 * 2**q)
            assert abs(estimate - exact - predicted_bias) < 1e-14
            assert abs(midpoint - exact) < 1e-14
            assert abs(antithetic - exact) < 1e-14
            rows.append(dict(weights=weights, q=q, classical_points=2**q,
                             exact=exact, sobol=estimate, midpoint=midpoint,
                             antithetic=antithetic, sobol_bias=predicted_bias))
    accounting = []
    for r in range(6):
        schedule = [2**s for s in range(r + 1)]
        effective = sum(schedule)
        calls = 2048 * sum(2*k + 1 for k in schedule)
        accounting.append(dict(schedule=schedule, effective_amplification_budget=effective,
                               full_A_or_Adagger_calls=calls,
                               ratio=calls/effective))
    thresholds = [dict(classical_seconds=tc, full_oracle_calls=nq,
                       speedup_required=10,
                       max_seconds_per_full_oracle=tc/(10*nq))
                  for tc in (0.001, 0.1, 10.0) for nq in (1000, 100000, 10000000)]
    result = dict(
        purpose="Independent toy-family falsification and honest query-accounting checks",
        paper="https://arxiv.org/html/2609.03625v1",
        scope="No option-pricing quantum advantage or hardware timing measured",
        python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
        linear_family=rows, query_accounting=accounting,
        hypothetical_10x_latency_thresholds=thresholds,
        sensitivity=[dict(rqmc_rmse_exponent=a,
                          quantum_relative_speedup_multiplier_when_error_divided_by_10=10**(1/a-1))
                     for a in (0.5, 0.75, 1.0, 1.25, 1.5)],
    )
    output = Path(__file__).with_name("qqmc_sanity.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(output=str(output), toy_checks=len(rows),
                          minimum_full_calls=accounting[0]["full_A_or_Adagger_calls"],
                          minimum_linear_midpoint_error=0.0)))


if __name__ == "__main__":
    main()
