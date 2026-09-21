"""Prospective v1 finite-shot feasibility experiment; not a pricing benchmark."""

import argparse
import json
import os
import time

import numpy as np

from .intervals import invert, price_decision, response
from .storage import finish_run, rng_for, start_run, write_json

DEPTHS = np.array([0, 1, 2, 4, 8])
AMPLITUDES = [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
CONDITIONS = {
    "ideal": (0.0, (0.0, 0.0)),
    "matched": (0.01, (0.01, 0.01)),
    "envelope": (0.01, (0.005, 0.015)),
    "misspecified": (0.03, (0.0, 0.0)),
    "inconsistent": (None, (0.0, 0.0)),
}


def mle_batch(counts, shots, eta):
    # Numerical point baseline, with no confidence or global-optimality claim.
    theta = np.linspace(0.0, np.pi / 2, 16385)
    d = 2 * DEPTHS + 1
    q = 0.5 + (1 - eta) ** d * (np.sin(theta[:, None] * d) ** 2 - 0.5)
    q = np.clip(q, 1e-14, 1 - 1e-14)
    likelihood = counts @ np.log(q).T + (shots - counts) @ np.log1p(-q).T
    return np.sin(theta[np.argmax(likelihood, axis=1)]) ** 2


def describe(confidence, a):
    row = {
        "components": confidence.components,
        "radius": confidence.radius,
        "midpoint": confidence.midpoint,
        "incompatible": not bool(confidence.components),
        "contains": confidence.contains(a) if a is not None else None,
        "squared_error": (confidence.midpoint - a) ** 2
        if a is not None and confidence.midpoint is not None
        else None,
    }
    for tolerance in (0.01, 0.025):
        label = str(tolerance)
        declared = confidence.radius is not None and confidence.radius <= tolerance
        row["declared_" + label] = declared
        row["erroneous_" + label] = (
            declared and abs(confidence.midpoint - a) > tolerance if a is not None else None
        )
    for slope in (1, 100):
        decision = price_decision(confidence, slope, bias_bound=0.1, tolerance=1.0)
        row[f"price_{slope}"] = decision
    return row


def aggregate(rows):
    result = {"trials": len(rows)}
    for key in (
        "contains",
        "incompatible",
        "declared_0.01",
        "declared_0.025",
        "erroneous_0.01",
        "erroneous_0.025",
        "a_equivalent_queries",
    ):
        values = [r[key] for r in rows if r.get(key) is not None]
        result[key + "_mean"] = float(np.mean(values)) if values else None
    radii = [r["radius"] for r in rows if r["radius"] is not None]
    errors = [r["squared_error"] for r in rows if r["squared_error"] is not None]
    result["median_radius_nonempty"] = float(np.median(radii)) if radii else None
    result["rmse_nonempty"] = float(np.sqrt(np.mean(errors))) if errors else None
    result["multiple_components_rate"] = float(np.mean([len(r["components"]) > 1 for r in rows]))
    for tol in ("0.01", "0.025"):
        declared = [r for r in rows if r["declared_" + tol] and r["erroneous_" + tol] is not None]
        result["erroneous_conditional_" + tol] = (
            float(np.mean([r["erroneous_" + tol] for r in declared])) if declared else None
        )
    for slope in (1, 100):
        result[f"price_{slope}_declaration_rate"] = float(
            np.mean([r[f"price_{slope}"]["status"] == "precision_met" for r in rows])
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/prototype_v1")
    args = parser.parse_args()
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_V1",
            "amplitudes": AMPLITUDES,
            "conditions": CONDITIONS,
            "depths": DEPTHS.tolist(),
            "shots": [128, 512],
            "replicates": 200,
            "mle_theta_grid_points": 16385,
            "pilot_selection": "radius*sqrt(64/128)<=.01 ->128 else512",
        },
    )
    started = time.perf_counter()
    summary = []
    with (path / "records.jsonl").open("x", encoding="utf-8") as stream:

        def persist(row):
            stream.write(json.dumps(row, allow_nan=False) + "\n")

        for condition, (eta, bounds) in CONDITIONS.items():
            for shots in (128, 512):
                group_rows, direct_rows = [], []
                for a in AMPLITUDES:
                    truth = None if eta is None else a
                    q = (
                        np.array([0.05, 0.95, 0.05, 0.95, 0.05])
                        if eta is None
                        else response(a, DEPTHS, eta)
                    )
                    counts = np.array(
                        [
                            rng_for("fixed_v1", a, condition, shots, rep, "validation").binomial(
                                shots, q
                            )
                            for rep in range(200)
                        ]
                    )
                    mle = mle_batch(counts, shots, sum(bounds) / 2)
                    for rep in range(200):
                        confidence = invert(counts[rep], [shots] * 5, DEPTHS, bounds)
                        row = dict(
                            experiment="fixed",
                            condition=condition,
                            a=truth,
                            nominal_amplitude_key=a,
                            shots_per_depth=shots,
                            replicate=rep,
                            counts=counts[rep].tolist(),
                            **describe(confidence, truth),
                            mle_estimate=float(mle[rep]),
                            mle_squared_error=float((mle[rep] - a) ** 2)
                            if truth is not None
                            else None,
                            total_shots=5 * shots,
                            grover_queries=15 * shots,
                            a_equivalent_queries=35 * shots,
                            max_grover_depth=8,
                        )
                        persist(row)
                        group_rows.append(row)
                        if truth is not None:
                            direct_shots = 35 * shots
                            direct_count = int(
                                rng_for("fixed_v1", a, condition, shots, rep, "direct").binomial(
                                    direct_shots, response(a, [0], eta)[0]
                                )
                            )
                            direct = invert([direct_count], [direct_shots], [0], bounds)
                            direct_row = dict(
                                experiment="direct",
                                condition=condition,
                                a=a,
                                shots_per_depth=shots,
                                replicate=rep,
                                counts=[direct_count],
                                **describe(direct, a),
                                total_shots=direct_shots,
                                grover_queries=0,
                                a_equivalent_queries=direct_shots,
                                max_grover_depth=0,
                            )
                            persist(direct_row)
                            direct_rows.append(direct_row)
                    summary.append(
                        dict(
                            experiment="fixed",
                            condition=condition,
                            a=truth,
                            nominal_amplitude_key=a,
                            shots=shots,
                            **aggregate(group_rows[-200:]),
                        )
                    )
                pooled = dict(
                    experiment="fixed_pooled",
                    condition=condition,
                    shots=shots,
                    **aggregate(group_rows),
                )
                mle_errors = [
                    r["mle_squared_error"] for r in group_rows if r["mle_squared_error"] is not None
                ]
                pooled["mle_rmse"] = float(np.sqrt(np.mean(mle_errors))) if mle_errors else None
                summary.append(pooled)
                if direct_rows:
                    summary.append(
                        dict(
                            experiment="direct_pooled",
                            condition=condition,
                            shots=shots,
                            **aggregate(direct_rows),
                        )
                    )
                stream.flush()
                os.fsync(stream.fileno())
                print(
                    f"{condition} shots={shots}: containment={pooled['contains_mean']}, "
                    f"radius={pooled['median_radius_nonempty']}",
                    flush=True,
                )
                if time.perf_counter() - started > 3600:
                    raise TimeoutError(
                        "Prospective compute limit reached; partial records retained"
                    )

        pilot_rows = []
        for a in AMPLITUDES:
            for rep in range(200):
                q = response(a, DEPTHS, 0.01)
                pilot_counts = rng_for("pilot_v1", a, "matched", 64, rep, "pilot").binomial(64, q)
                pilot = invert(pilot_counts, [64] * 5, DEPTHS, (0.01, 0.01))
                shots = (
                    128
                    if pilot.radius is not None and pilot.radius * np.sqrt(64 / 128) <= 0.01
                    else 512
                )
                counts = rng_for("pilot_v1", a, "matched", shots, rep, "validation").binomial(
                    shots, q
                )
                confidence = invert(counts, [shots] * 5, DEPTHS, (0.01, 0.01))
                row = dict(
                    experiment="split_pilot",
                    condition="matched",
                    a=a,
                    replicate=rep,
                    shots_per_depth=shots,
                    pilot_counts=pilot_counts.tolist(),
                    counts=counts.tolist(),
                    **describe(confidence, a),
                    total_shots=5 * (64 + shots),
                    grover_queries=15 * (64 + shots),
                    a_equivalent_queries=35 * (64 + shots),
                    max_grover_depth=8,
                )
                persist(row)
                pilot_rows.append(row)
                if time.perf_counter() - started > 3600:
                    stream.flush()
                    os.fsync(stream.fileno())
                    raise TimeoutError("Compute limit reached; pilot records retained")
        pilot_summary = dict(
            experiment="split_pilot_pooled",
            condition="matched",
            selected_128_rate=float(np.mean([r["shots_per_depth"] == 128 for r in pilot_rows])),
            **aggregate(pilot_rows),
        )
        summary.append(pilot_summary)
        stream.flush()
        os.fsync(stream.fileno())
    write_json(path / "summary.json", summary)
    write_json(path / "timing.json", {"wall_seconds": time.perf_counter() - started})
    if time.perf_counter() - started > 3600:
        raise TimeoutError("Compute limit reached before completion; records retained")
    finish_run(path)
    print("Completed fixed, direct, and independent split-pilot experiments", flush=True)


if __name__ == "__main__":
    main()
