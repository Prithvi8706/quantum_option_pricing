"""Small exact-digital timing screen and explicit remaining sampling costs.

This is not a confidence certificate: 32 development draws cannot close the
baseline-mean or regret obligations. No large run is launched by this script.
"""

import json
import math
from pathlib import Path
import time

import numpy as np

from research.compound_feasibility.model import MODELS
from research.controlled_priority_completion.range_audit import Audit, build
from research.controlled_source_completion.finance import prune
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.optimize import optimize


def main():
    count, seed = 32, 2026092805
    tic = time.perf_counter()
    graph = build(MODELS[0])
    construction = time.perf_counter() - tic
    data = graph.as_dict()
    audit = Audit(data, graph.witnesses).run()
    baseline = optimize(prune(data, ["base_6"]))
    rng = np.random.default_rng(seed)
    samples = []
    tic = time.perf_counter()
    for _ in range(count):
        inputs = {
            "uniform_%d" % i: int(x)
            for i, x in enumerate(rng.integers(0, 1 << 32, size=len(graph.inputs), dtype=np.int64))
        }
        samples.append(evaluate(baseline, inputs)["base_6"])
    elapsed = time.perf_counter() - tic
    upper_raw = audit.bounds[data["outputs"]["base_6"]][1]
    support = upper_raw / (1 << 40)
    epsilon, failure = 0.003, 0.002
    hoeffding = math.ceil(support * support * math.log(2 / failure) / (2 * epsilon * epsilon))
    # Necessary for this empirical-Bernstein radius even if sample variance=0.
    eb_floor = math.floor(7 * support * math.log(4 / failure) / (3 * epsilon)) + 2
    variance = float(np.var(samples, ddof=1))

    def radius(n):
        return math.sqrt(2 * variance * math.log(4 / failure) / n) + 7 * support * math.log(
            4 / failure
        ) / (3 * (n - 1))

    lo, hi = 2, hoeffding * 2
    while lo < hi:
        mid = (lo + hi) // 2
        if radius(mid) <= epsilon:
            hi = mid
        else:
            lo = mid + 1
    row = dict(
        model="C4",
        strike=6,
        seed=seed,
        development_samples=count,
        exact_digital_baseline_values=samples,
        construction_seconds=construction,
        sample_seconds=elapsed,
        seconds_per_sample=elapsed / count,
        guaranteed_baseline_range_dollars=[0, support],
        baseline_error_allocation=epsilon,
        baseline_failure_allocation=failure,
        unconditional_hoeffding_sample_count=hoeffding,
        zero_variance_empirical_bernstein_necessary_samples=eb_floor,
        diagnostic_sample_variance=variance,
        empirical_bernstein_count_if_variance_stayed_at_diagnostic_value=lo,
        projected_serial_seconds={
            "hoeffding": hoeffding * elapsed / count,
            "zero_variance_eb_floor": eb_floor * elapsed / count,
            "diagnostic_variance_eb": lo * elapsed / count,
        },
        classification=(
            "Development timing and sample-size screen, not a baseline "
            "certificate or a lower bound for all classical methods."
        ),
        reason_large_run_not_started=(
            "Even the selected empirical-Bernstein certificate at "
            "zero variance requires millions of exact-policy samples; "
            "the cost gate already fails and no certificate-accelerating "
            "implementation was validated."
        ),
    )
    p = Path("results/controlled_priority_completion/range_sampling_screen.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(row, indent=2) + "\n")
    print(
        json.dumps({k: v for k, v in row.items() if k != "exact_digital_baseline_values"}),
        flush=True,
    )


if __name__ == "__main__":
    main()
