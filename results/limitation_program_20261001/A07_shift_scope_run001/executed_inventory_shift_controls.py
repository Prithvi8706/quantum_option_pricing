"""Prospective same-SSA shift-count range inventory; no circuit changes."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.progress import ROOT


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def signed_bits(low, high, width):
    return next(n for n in range(1, width + 1) if -(1 << (n - 1)) <= low <= high < 1 << (n - 1))


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(exist_ok=False)
    baseline = ROOT / "results/limitation_program_20261001/A11_run001"
    assert read(baseline / "summary.json")["accepted"]
    frozen = {}
    for name in ("inventory_shift_controls.py", "interval_bounds.py", "prove_log_exponent.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[str(path.relative_to(ROOT))] = digest(path)
    frozen[str((baseline / "manifest.json").relative_to(ROOT))] = digest(baseline / "manifest.json")
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = baseline / case / name
            frozen[str(path.relative_to(ROOT))] = digest(path)
    shutil.copy2(Path(__file__), output / "executed_inventory_shift_controls.py")
    save(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "before_analysis": True,
            "local_only": True,
            "baseline": str(baseline.relative_to(ROOT)),
            "candidate_guard": "Actual shift-count SSA interval in [-64,63], native72 inputs/output",
            "purpose": "Check signed7 control feasibility without altering data width or input law",
            "acceptance": "Only same-SSA intervals derived from declared domain establish the guard",
            "excluded": "No emitted leaf, gate replay, realized resource saving or G2-G5 closure",
            "frozen_inputs": frozen,
            "python": sys.version,
        },
    )
    checked = 0
    for width in range(1, 6):
        sign = 1 << (width - 1)
        for low in range(-sign, sign):
            for high in range(low, sign):
                n = signed_bits(low, high, width)
                assert all(-(1 << (n - 1)) <= k < 1 << (n - 1) for k in range(low, high + 1))
                assert n == 1 or low < -(1 << (n - 2)) or high >= 1 << (n - 2)
                checked += 1
    cases = []
    for case in ("B4x12", "B8x52"):
        target, source = (read(baseline / case / name) for name in ("target.json", "source.json"))
        assert (target["width"], target["fraction_bits"]) == (72, 40)
        bounds, rules = bound_graph(target)
        calls = iter(source["forward_calls"])
        sites = []
        for index, node in enumerate(target["nodes"]):
            if node["op"] == "input":
                continue
            call = next(calls)
            assert (call["args"], call["out"]) == (node["args"], node["out"])
            if node["op"] != "shift":
                continue
            low, high = bounds[node["args"][1]]
            bits = signed_bits(low, high, 72)
            sites.append(
                {
                    "node_index": index,
                    "data_value": node["args"][0],
                    "shift_value": node["args"][1],
                    "output_value": node["out"][0],
                    "shift_bounds": [low, high],
                    "signed_control_bits": bits,
                    "signed7_guard_proved": -64 <= low <= high <= 63,
                    "rule": rules[node["args"][1]],
                    "leaf": call["leaf"],
                }
            )
        save(output / (case + "_shift_sites.json"), sites)
        cases.append(
            {
                "case": case,
                "shift_calls": len(sites),
                "signed7_guard_proved_calls": sum(s["signed7_guard_proved"] for s in sites),
                "control_width_inventory": dict(Counter(s["signed_control_bits"] for s in sites)),
            }
        )
    assert all(digest(ROOT / name) == value for name, value in frozen.items())
    save(
        output / "summary.json",
        {
            "passed": True,
            "cases": cases,
            "small_interval_checks": checked,
            "signed7_maximum_magnitude": 64,
            "all_signed7_shifts_are_smaller_than_data_width72": 64 < 72,
            "realized_savings": False,
            "financial_function_changed": False,
            "next": "One exact signed7-control barrel shift with full72 data/interface and static fallback",
        },
    )
    files = {
        str(path.relative_to(ROOT)): digest(path) for path in output.rglob("*") if path.is_file()
    }
    save(output / "manifest.json", {"files": files, "frozen_inputs": frozen})
    print(json.dumps({"passed": True, "cases": cases}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    run(parser.parse_args().output)
