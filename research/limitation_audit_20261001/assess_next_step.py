"""Read-only scientific screen of the improved source's remaining bottlenecks.

Writes a new receipt; does not change or execute the source circuits. Zero-cost
screens are counterfactual arithmetic diagnostics, not proposed implementations.
"""

import json
from collections import Counter
from pathlib import Path

from research.controlled_source_completion.compiler import resolve_library


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results/limitation_audit_20261001"


def assess(case):
    directory = RESULTS / "multiplier_v2" / case
    source = json.loads((directory / "source.json").read_text())
    schedule = json.loads((directory / "schedule_capped.json").read_text())
    library = resolve_library(source)
    entries = {key: json.loads((library / (key + ".json")).read_text())
               for key in source["library_keys"]}
    dominant = Counter()
    for group in schedule["groups"]:
        rs = [entries[source["forward_calls"][index]["leaf"]]
              for index in group["call_indices"]]
        assert max(r["resources"]["t_depth"] for r in rs) == group["t_depth"]
        names = sorted({r["op"] for r in rs
                        if r["resources"]["t_depth"] == group["t_depth"]})
        dominant["/".join(names)] += 2 * group["t_depth"]
    depth = schedule["resources"]["t_depth"]
    assert sum(dominant.values()) == depth
    operations = source["forward_operation_costs"]
    zero_cost = {}
    for removed in operations:
        counterfactual = 0
        for group in schedule["groups"]:
            counterfactual += 2 * max((
                entry["resources"]["t_depth"] if entry["op"] != removed else 0
                for index in group["call_indices"]
                for entry in [entries[source["forward_calls"][index]["leaf"]]]
            ), default=0)
        zero_cost[removed] = dict(counterfactual_t_depth=counterfactual,
                                 depth_reduction_fraction=1 - counterfactual / depth)
    historical = json.loads((ROOT / "results/frontier_completion_20260927/stage_a/"
                             "historical_frontier.json").read_text())
    comparisons = []
    for row in historical["grid"]:
        if (row["case"] == case and row["schedule"] == "all"
                and row["eps"] in (.01, .001) and row["k"] == 3
                and row["t_layer_seconds"] == 1e-7):
            calls = row["hypothetical_calls"]
            classical = row["historical_classical_model_seconds"]
            modeled = calls * depth * row["t_layer_seconds"]
            comparisons.append(dict(
                epsilon=row["eps"], hypothetical_source_calls=calls,
                historical_classical_model_seconds=classical,
                improved_source_only_model_seconds=modeled,
                historical_depth_budget_for_10x=row["historical_d_max"],
                ratio_to_10x_depth_budget=depth / row["historical_d_max"],
                source_only_model_quantum_over_classical=modeled / classical,
            ))
    return dict(case=case, depth=depth, qubits=schedule["resources"]["logical_qubits"],
                batch_max_depth_attribution=dict(dominant.most_common()),
                fixed_schedule_zero_cost_diagnostics=zero_cost,
                t_count_shares={op: costs["t_count"] / sum(
                    r["t_count"] for r in operations.values())
                    for op, costs in operations.items()}, historical_sensitivity=comparisons)


def main():
    result = dict(cases=[assess(case) for case in ("B4x12", "B8x52")],
        attribution_scope="Assign each batch's max T-depth to the operation family "
        "setting that maximum. This is schedule attribution, not a causal global "
        "critical-path decomposition; reordering may change it.",
        zero_cost_scope="Set one operation family's depth to zero in the same schedule. "
        "No gates removed, new circuit emitted, or performance gain verified. Does not "
        "predict changing the Gaussian law or changing dependencies.",
        historical_scope="Unchanged archived fitted classical times, hypothetical "
        "variance estimator k=3, 100ns per T layer, and source only. Not fresh pricing "
        "timings, a proven estimator schedule, or a physical hardware forecast.")
    with (RESULTS / "next_step_screen_v1.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    for case in result["cases"]:
        print(case["case"], "batch depth", case["batch_max_depth_attribution"])
        print("zero-cost depth reduction fractions", {
            op: round(r["depth_reduction_fraction"], 4)
            for op, r in case["fixed_schedule_zero_cost_diagnostics"].items()
            if r["depth_reduction_fraction"] > .01})
        print("historical sensitivity", case["historical_sensitivity"])


if __name__ == "__main__":
    main()
