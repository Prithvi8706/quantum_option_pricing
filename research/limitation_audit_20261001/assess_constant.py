"""Identify the next exact constant leaf and screen its fixed-batch opportunity."""

import json
from pathlib import Path

from research.controlled_source_completion.compiler import resolve_library


def run():
    root = Path(__file__).resolve().parents[2] / "results/limitation_audit_20261001"
    coefficient, rows = 762123384786, []
    for name in ("B4x12", "B8x52"):
        directory = root / "multiplier_v2" / name
        source = json.loads((directory / "source.json").read_text())
        target = json.loads((directory / "target.json").read_text())
        schedule = json.loads((directory / "schedule_capped.json").read_text())
        library = resolve_library(source)
        entries = {k: json.loads((library / (k + ".json")).read_text())
                   for k in source["library_keys"]}
        chosen = {k for k, e in entries.items()
                  if e["op"] == "cmul" and e["params"].get("c") == coefficient}
        producers = {v: node for node in target["nodes"] for v in node["out"]}
        calls = [c for c in source["forward_calls"] if c["leaf"] in chosen]
        assert all(producers[c["args"][0]]["op"] == "bits"
                   and producers[c["args"][0]]["params"]["shift"] == -40 for c in calls)
        free = sum(2 * max((
            entries[source["forward_calls"][i]["leaf"]]["resources"]["t_depth"]
            if source["forward_calls"][i]["leaf"] not in chosen else 0
            for i in group["call_indices"]
        ), default=0) for group in schedule["groups"])
        rows.append(dict(case=name, coefficient=coefficient, occurrences=len(calls),
                         low_zero_bits_proved_by_producer=40,
                         fixed_schedule_zero_leaf_depth=free,
                         zero_cost_reduction_fraction=1 - free / schedule["resources"]["t_depth"],
                         scope="Counterfactual ceiling in unchanged batches; "
                         "no circuit improvement"))
    with (root / "next_constant_screen_v1.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(rows, indent=2) + "\n")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    run()
