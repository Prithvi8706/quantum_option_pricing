"""Render the completed common-policy study without recalibrating any method."""

import argparse
from fractions import Fraction
import json
from pathlib import Path
import platform
import subprocess

from .artifacts import ROOT, digest, save_figure, table, write_json


def run(archive, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    archive, output = Path(archive), Path(output)
    completion = json.loads((archive / "complete.json").read_text(encoding="utf-8"))
    if completion["status"] != "complete":
        raise ValueError("Complete source-bound acquisition required")
    for name, expected in completion["sha256"].items():
        if digest(archive / name) != expected:
            raise ValueError("Common-study output hash mismatch: " + name)
    for name, expected in completion["input_sha256"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("Common-study input hash mismatch: " + name)
    result = json.loads((archive / "results.json").read_text(encoding="utf-8"))
    rows = result["rows"]
    expected = {(case, route) for case in ("D1", "D2")
                for route in ("reflection", "raw_parent", "residual")}
    if len(rows) != 6 or {(r["case"], r["route"]) for r in rows} != expected:
        raise ValueError("Exactly six fixed oracle rows required")
    output.mkdir(parents=True, exist_ok=False)
    selected, budgets, comparisons, claims = [], [], [], []
    for row in rows:
        selected.append({"case": row["case"], "route": row["route"],
                         "M": row["schedule"]["M"],
                         "allocated_qubits": row["total_allocated_qubits"],
                         "A_U": row["a"]["u"], "A_CX": row["a"]["cx"],
                         "controlled_CX": row["totals"]["controlled"]["cx"],
                         "control_cancelled_CX": row["totals"]["control_cancelled"]["cx"],
                         "controlled_serial_depth_upper":
                             row["totals"]["controlled"]["serial_depth_upper"],
                         "cancelled_serial_depth_upper":
                             row["totals"]["control_cancelled"]["serial_depth_upper"]})
        bridge = row["label_bridge"]
        budgets.append({"case": row["case"], "route": row["route"],
                        "deterministic_bound": row["budget"]["deterministic_upper"],
                        "added_label_allowance_exact": bridge["extra_price_bound_rational"],
                        "added_label_allowance_display":
                            float(Fraction(bridge["extra_price_bound_rational"])),
                        "remaining_margin_exact": bridge["remaining_price_margin_rational"],
                        "remaining_margin_display":
                            float(Fraction(bridge["remaining_price_margin_rational"])),
                        "repetitions": row["schedule"]["repetitions"]})
        claims.append({"claim_id": row["case"] + "_" + row["route"] + "_cost_width",
                       "evidence": str(archive / (row["case"] + "_" + row["route"] + ".json")),
                       "fields": "totals;total_allocated_qubits;schedule;label_bridge",
                       "scope": "Ideal logical fixed-menu projection; serial depth upper bound"})
    for comparison in result["comparisons"]:
        for ledger, values in comparison["ledgers"].items():
            ratio = values["reflection_over_residual"]
            comparisons.append({"case": comparison["case"], "ledger": ledger,
                                "winner": values["winner"], "reflection_over_residual_exact": ratio,
                                "reflection_over_residual_display": float(Fraction(ratio))})
    table(output, "common_selected", selected)
    table(output, "common_error_budget", budgets)
    table(output, "common_comparisons", comparisons)
    table(output, "claim_evidence", claims)

    matplotlib.rcParams.update({"svg.hashsalt": "pricing-common-20260922", "font.size": 10,
                                "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.8), constrained_layout=True)
    routes = ("reflection", "raw_parent", "residual")
    colors = ("#382C63", "#39768A", "#BB6337")
    for i, case in enumerate(("D1", "D2")):
        chosen = {r["route"]: r for r in rows if r["case"] == case}
        for j, ledger in enumerate(("controlled", "control_cancelled")):
            ax = axes[i, j]
            values = [chosen[route]["totals"][ledger]["cx"] for route in routes]
            ax.bar(range(3), values, color=colors)
            ax.set(yscale="log", title=f"{case}: {ledger.replace('_', ' ')}",
                   ylabel="Projected CX per price estimate", xticks=[0, 1, 2],
                   xticklabels=["Reflection", "Raw parent", "Residual"])
            ax.set_ylim(min(values) / 3, max(values) * 3)
            for k, value in enumerate(values):
                ax.text(k, value * 1.15, f"{value:.3g}", ha="center", fontsize=9)
    save_figure(fig, output, "common_policy_cost")
    plt.close(fig)
    inputs = [archive / name for name in ("planned.json", "results.json", "complete.json")]
    sources = [Path(__file__), Path(__file__).with_name("artifacts.py")]
    write_json(output / "manifest.json", {
        "scope": "New common-policy acquisition rendered without new pricing observations.",
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                             text=True).strip(),
        "python": platform.python_version(), "matplotlib": matplotlib.__version__,
        "source_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
        "input_sha256": {p.resolve().relative_to(ROOT).as_posix(): digest(p) for p in inputs},
        "output_sha256": {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
        "new_pricing_observations": 0, "oracle_rows": 6,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.archive, args.output)
