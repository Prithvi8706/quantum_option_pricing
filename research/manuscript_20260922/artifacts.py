"""Generate paper tables and exportable figures without new pricing observations."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = ROOT / "results/journal_sprint/stronger_arithmetic_analysis_v1"
RESOURCE = (ROOT / "docs/novelty_assessment/2026-09-21/reviews/resources"
            / "archived_resource_check.json")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def table(output, name, rows):
    if not rows:
        raise ValueError("Empty paper table")
    columns = list(rows[0])
    with (output / (name + ".csv")).open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    lines.extend("| " + " | ".join(str(row[c]) for c in columns) + " |" for row in rows)
    (output / (name + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_figure(fig, output, name):
    fig.savefig(output / (name + ".png"), dpi=220, bbox_inches="tight")
    fig.savefig(output / (name + ".svg"), bbox_inches="tight", metadata={"Date": None})
    fig.savefig(output / (name + ".pdf"), bbox_inches="tight",
                metadata={"CreationDate": None, "ModDate": None})


def historical_artifacts(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams.update({"svg.hashsalt": "pricing-20260922", "font.size": 10,
                                "axes.spines.top": False, "axes.spines.right": False})
    completion = json.loads((HISTORICAL / "complete.json").read_text())
    for name, expected in completion["sha256"].items():
        if digest(HISTORICAL / name) != expected:
            raise ValueError("Historical evidence mismatch: " + name)
    historical = json.loads((HISTORICAL / "summary.json").read_text())
    resource = json.loads(RESOURCE.read_text())
    if len(historical["rows"]) != 166 or not resource["passed"]:
        raise ValueError("Complete verified historical menu required")
    selected = resource["selected"]
    selected_rows = []
    for case in ("D1", "D2"):
        for route in ("reflection", "raw_matched_parent", "residual", "raw_best"):
            row = selected[case][route]
            selected_rows.append({"case": case, "route": route,
                                  "CX_control_cancelled": row["control_cancelled_cx"],
                                  "CX_conservative": row["conservative_cx"],
                                  "allocated_qubits": row["total_qubits"], "M": row["M"],
                                  "A_CX": row["a_cx"], "price_sensitivity": row["slope_upper"],
                                  "deterministic_allowance": row["deterministic_upper"]})
    table(output, "historical_selected", selected_rows)
    table(output, "historical_all_166", historical["rows"])

    colors = {"primary": "#39768A", "residual": "#BB6337", "reflection": "#382C63"}
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    for i, case in enumerate(("D1", "D2")):
        for j, (key, label) in enumerate((("control_cancelled_cx", "Control-cancelled ledger"),
                                           ("conservative_cx", "Conservative ledger"))):
            ax = axes[i, j]
            for source, marker in (("primary", "o"), ("residual", "s")):
                rows = [r for r in historical["rows"] if r["case"] == case and r["source"] == source
                        and r["status"] == "ideal_plan"]
                ax.scatter([r["total_qubits"] for r in rows], [r[key] for r in rows],
                           c=colors[source], marker=marker, alpha=.45, s=24, label=source)
            ref = selected[case]["reflection"]
            ax.scatter([ref["total_qubits"]], [ref[key]], marker="*", s=140,
                       c=colors["reflection"], label="reflection")
            ax.set(xscale="log", yscale="log", xlabel="Total allocated logical qubits",
                   ylabel="Projected CX per price estimate", title=f"{case}: {label}")
            ax.grid(alpha=.18)
    axes[0, 0].legend(frameon=False)
    save_figure(fig, output, "historical_width_cost")
    plt.close(fig)

    ratios = []
    metrics = [("a_cx", "CX per A"), ("slope_upper", "Price sensitivity"),
               ("M", "AE size M"), ("control_cancelled_cx", "Total CX")]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), constrained_layout=True)
    for ax, case in zip(axes, ("D1", "D2")):
        parent, residual = selected[case]["raw_matched_parent"], selected[case]["residual"]
        values = [residual[key] / parent[key] for key, _ in metrics]
        ax.bar(range(len(metrics)), values, color=[colors["primary"], colors["residual"],
                                                  colors["residual"], colors["reflection"]])
        ax.axhline(1, color="black", linewidth=.7, linestyle="--")
        ax.set(yscale="log", title=case, ylabel="Residual / exact raw-parent ratio",
               xticks=list(range(len(metrics))), xticklabels=[label for _, label in metrics])
        ax.tick_params(axis="x", labelrotation=20)
        for index, value in enumerate(values):
            ax.text(index, value * 1.09, f"{value:.3f}", ha="center", fontsize=9)
        ratios.append({"case": case, **{key: value for (key, _), value in zip(metrics, values)}})
    table(output, "matched_parent_ratios", ratios)
    save_figure(fig, output, "matched_parent_mechanism")
    plt.close(fig)
    paths = [HISTORICAL / name for name in ("complete.json", "summary.json", "all_rows.csv")]
    return paths + [RESOURCE]


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    sources = historical_artifacts(output)
    import matplotlib
    write_json(output / "manifest.json", {
        "scope": "Historical paper artifacts only; new common-policy results are separate.",
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                             text=True).strip(),
        "python": platform.python_version(), "matplotlib": matplotlib.__version__,
        "source_sha256": {str(Path(__file__).relative_to(ROOT)): digest(Path(__file__))},
        "input_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
        "output_sha256": {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
        "historical_rows": 166, "new_pricing_observations": 0,
        "note": "All nominal rows retained; coincident points represent quantized duplicates.",
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
