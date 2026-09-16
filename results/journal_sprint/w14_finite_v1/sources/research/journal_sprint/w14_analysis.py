"""Prespecified descriptive week14 analysis; no selection or confirmation gate test."""

import argparse
import json
import math
from pathlib import Path

from scipy.stats import beta

from .storage import sha256, write_json


def rate(successes, count):
    if count == 0:
        return dict(successes=successes, denominator=count, estimate=None, pointwise_cp95=None)
    if not 0 <= successes <= count:
        raise ValueError("invalid rate counts")
    low = 0.0 if successes == 0 else float(beta.ppf(0.025, successes, count - successes + 1))
    high = 1.0 if successes == count else float(beta.ppf(0.975, successes + 1, count - successes))
    return dict(
        successes=successes,
        denominator=count,
        estimate=successes / count,
        pointwise_cp95=[low, high],
    )


def confidence_summary(rows, truth, native=False):
    declared = misses = erroneous = returned = capped = 0
    costs = {key: [] for key in ("shots", "A_equivalents", "logical_cx")}
    errors = []
    for row in rows:
        interval = row["price_interval"] if native else row["decision"]["interval"]
        if native:
            if row["status"] not in ("completed", "resource_capped"):
                raise ValueError("native error is not a completed diagnostic")
            capped += row["status"] == "resource_capped"
            metrics = row["totals"]
            cost = dict(
                shots=metrics["shots"],
                A_equivalents=metrics["a_equivalent_queries"],
                logical_cx=metrics["cx"],
            )
        else:
            cost = row.get("cost", {k: row.get(k) for k in costs})
        for key in costs:
            if cost[key] is not None:
                costs[key].append(cost[key])
        if interval is not None:
            if (
                len(interval) != 2
                or not all(math.isfinite(x) for x in interval)
                or interval[0] > interval[1]
            ):
                raise ValueError("invalid interval")
            returned += 1
            radius = (interval[1] - interval[0]) / 2
            estimate = sum(interval) / 2
            error = abs(estimate - truth)
            errors.append(error)
            delivered = radius <= 1.0
            declared += delivered
            misses += not interval[0] <= truth <= interval[1]
            erroneous += delivered and error > 1.0
            if not native:
                if row["decision"]["status"] == "precision_met" and not delivered:
                    raise ValueError("delivery/status inconsistency")
    n = len(rows)
    empty_misses = 0 if native else n - returned
    return dict(
        attempts=n,
        returned_intervals=returned,
        no_interval=n - returned,
        resource_capped=capped,
        declarations=declared,
        abstentions=n - declared,
        delivery=rate(declared, n),
        empty_confidence_sets=empty_misses,
        hull_containment_unconditional=rate(returned - misses, n),
        interval_miss_unconditional=rate(misses + empty_misses, n),
        interval_miss_given_return=rate(misses, returned),
        erroneous_declaration_unconditional=rate(erroneous, n),
        erroneous_given_declaration=rate(erroneous, declared),
        mean_interval_midpoint_error=None if not errors else sum(errors) / len(errors),
        containment_scope=(
            "hull intervals; caps give no containing output, not an invented interval"
            if native
            else "hull intervals; empty sets count as unconditional misses"
        ),
        costs={
            key: dict(
                total=sum(values),
                mean=None if not values else sum(values) / len(values),
                denominator=len(values),
            )
            for key, values in costs.items()
        },
    )


def analyze(output):
    output = Path(output)

    def read(name):
        return json.loads((output / name).read_text(encoding="utf-8"))

    manifest = read("complete.json")["sha256"]
    actual = {
        p.relative_to(output).as_posix(): sha256(p)
        for p in output.rglob("*")
        if p.is_file() and p != output / "complete.json"
    }
    if manifest != actual:
        raise ValueError("archive checksum/inventory mismatch")
    config = read("planned.json")["config"]
    setup = read("setup__result.json")["value"]
    truth = setup["truth"]
    cells = []
    native = {rep: [] for rep in config["representations"]}
    responses = []
    for file in sorted(output.glob("*__result.json")):
        name = file.name.removesuffix("__result.json")
        value = read(file.name)["value"]
        if name == "setup":
            continue
        if "_response_" in name:
            responses.append(value)
            continue
        if "_iqae_" in name:
            native[name.split("_")[0]].append(value)
            continue
        category = name.split("_")[1]
        if category in ("fixed", "policy"):
            rows = value["trials"]
            if len(rows) != config["trials"]:
                raise ValueError("missing trial")
            if category == "fixed":
                rows = [dict(row, cost=value["per_trial_cost"]) for row in rows]
            else:
                rows = [dict(row, shots=row["total_shots"]) for row in rows]
            model_valid = (
                value["model_valid"]
                if category == "policy"
                else value["eta"] == value["assumed_eta"]
            )
            cells.append(
                dict(
                    name=name,
                    kind="confidence",
                    model_valid=model_valid,
                    **confidence_summary(rows, truth),
                )
            )
        elif "_csae_" in name:
            if len(value["price_estimates"]) != config["trials"]:
                raise ValueError("missing source estimate")
            errors = [abs(x - truth) for x in value["price_estimates"]]
            cells.append(
                dict(
                    name=name,
                    kind="point_only",
                    attempts=len(errors),
                    mean_absolute_error=sum(errors) / len(errors),
                    rmse=math.sqrt(sum(x * x for x in errors) / len(errors)),
                    observed_within_dollar=sum(x <= 1 for x in errors),
                    delivered_confidence_intervals=0,
                    per_trial_cost=value["per_trial_cost"],
                )
            )
        elif name.endswith("_classical"):
            errors = [abs(row["estimate"] - truth) for row in value["trials"]]
            cells.append(
                dict(
                    name=name,
                    kind="point_only",
                    attempts=len(errors),
                    mean_absolute_error=sum(errors) / len(errors),
                    rmse=math.sqrt(sum(x * x for x in errors) / len(errors)),
                    observed_within_dollar=sum(x <= 1 for x in errors),
                    delivered_confidence_intervals=0,
                    path_evaluations=3200,
                    exact_finite_sum=value["exact_finite_sum"],
                )
            )
        else:
            raise ValueError("unexpected result task")
    for rep, rows in native.items():
        if len(rows) != config["native_trials"]:
            raise ValueError("missing native run")
        cells.append(
            dict(
                name=f"{rep}_iqae",
                kind="native_confidence",
                **confidence_summary(rows, truth, native=True),
            )
        )
        for suffix in ("csae", "fixed_direct_shots", "fixed_direct_queries", "fixed_depth_limited"):
            if suffix == "csae":
                first, second = (read(f"{rep}_csae_{p}__result.json")["value"] for p in (1, 2))
                if first["counts"] != second["counts"]:
                    raise ValueError("matched/ignored csAE observations not paired")
            else:
                method = suffix.removeprefix("fixed_")
                first, second = (
                    read(f"{rep}_fixed_{p}_{method}__result.json")["value"] for p in (1, 2)
                )
                if [r["counts"] for r in first["trials"]] != [
                    r["counts"] for r in second["trials"]
                ]:
                    raise ValueError("matched/ignored CP observations not paired")
    if len(cells) != 58 or len(responses) != 20:
        raise ValueError("incomplete analysis schedule")
    return dict(
        cells=cells,
        truth=truth,
        response_cases=len(responses),
        max_response_error=max(max(r["errors"].values()) for r in responses),
        application_admitted=False,
        confirmation_authorized=False,
        inference_scope="pointwise descriptive development; no significance test",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = analyze(args.archive)
    write_json(args.output, result)
    print(json.dumps(dict(cells=len(result["cells"]), response_cases=result["response_cases"])))
