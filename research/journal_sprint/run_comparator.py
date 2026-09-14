"""Reproduce pinned source golden tests and reduced independent benchmarks."""

from .checks import require

import argparse
import time

import numpy as np
from scipy.stats import binom

from .storage import finish_run, start_run, write_json
from .vendor.mlqae_core import evaluate_schedule, flagship_schedule


def quantile_interval(errors, scale, p=0.95, alpha=0.05):
    """Distribution-free order-statistic CI for a continuous population quantile.

    If B counts observations below the quantile, B ~ Binomial(n,p).
    Lower rank L and upper rank U cover when L <= B < U (one-based ranks).
    """
    values = np.sort(errors)
    n = len(values)
    lower_rank = int(binom.ppf(alpha / 2, n, p))
    upper_rank = int(binom.ppf(1 - alpha / 2, n, p)) + 1
    lower = 0.0 if lower_rank == 0 else float(values[lower_rank - 1] * scale)
    upper = None if upper_rank > n else float(values[upper_rank - 1] * scale)
    return [lower, upper]


def validate_golden(rows):
    golden = {row["name"]: row for row in rows if row["name"].startswith("golden_")}
    if set(golden) != {"golden_plain", "golden_flagship"} or not all(
        row.get("golden_pass") is True for row in golden.values()
    ):
        raise ValueError("Source golden regression failed or missing")


def finish_accepted_run(path, rows):
    try:
        validate_golden(rows)
    except ValueError as error:
        write_json(path / "failure.json", {"scientific_acceptance": False, "error": str(error)})
        raise
    write_json(path / "acceptance.json", {"golden_regressions_passed": True})
    finish_run(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/comparator_v1")
    args = parser.parse_args()
    experiments = [
        ("golden_plain", 125, None, 30000, 880125, 0.0, None),
        ("golden_flagship", 125, 1.3, 30000, 880125, 0.0, None),
        ("table_i_cap60", 60, 1.3, 30000, 2026090960, 0.0, None),
        ("table_i_cap125", 125, 1.3, 30000, 20260909125, 0.0, None),
        ("noise_matched", 182, 1.3, 20000, 20260909182, 0.001, 0.001),
        ("noise_ignored", 182, 1.3, 20000, 20260909182, 0.001, 0.0),
    ]
    path = start_run(
        args.output, {"experiments": experiments, "protocol": "PROTOCOL_V1", "chunk": 4000}
    )
    rows = []
    matched_counts = None
    for name, cap, divisor, trials, seed, eta, model_eta in experiments:
        started = time.perf_counter()
        depths, shots = flagship_schedule(cap, cap_divisor=divisor)
        out = evaluate_schedule(
            depths, shots, trials, seed, eta=eta, model_eta=model_eta, return_extra=True
        )
        raw = {key: out.pop(key) for key in ("errors", "a_true", "theta_hat", "counts")}
        np.savez_compressed(path / f"{name}.npz", **raw)
        if name == "noise_matched":
            matched_counts = raw["counts"].copy()
        if name == "noise_ignored":
            require(np.array_equal(matched_counts, raw["counts"]))
        out.update(
            name=name,
            depths=depths,
            shots=shots,
            trials=trials,
            seed=seed,
            eta=eta,
            model_eta=model_eta,
            total_shots=int(sum(shots)),
            grover_queries=int(np.dot(shots, depths)),
            a_equivalent_queries=int(np.dot(shots, 2 * np.array(depths) + 1)),
            C95_interval=quantile_interval(raw["errors"], out["nq"]),
            wall_seconds=time.perf_counter() - started,
        )
        if name == "golden_plain":
            out["golden_pass"] = abs(out["C95"] - 2.82) <= 0.04
        if name == "golden_flagship":
            out["golden_pass"] = (
                abs(out["C95"] - 2.85) <= 0.05
                and abs(out["C99"] - 5.23) <= 0.30
                and abs(out["C95par"] - 0.209) <= 0.008
            )
        if name.startswith("table_i"):
            out["paper_C95"] = 2.776 if cap == 60 else 2.886
            out["difference_from_paper"] = out["C95"] - out["paper_C95"]
        write_json(path / f"{name}.json", out)
        rows.append(out)
        print(f"{name}: C95={out['C95']:.6f}; CI={out['C95_interval']}", flush=True)
    write_json(path / "summary.json", rows)
    finish_accepted_run(path, rows)


if __name__ == "__main__":
    main()
