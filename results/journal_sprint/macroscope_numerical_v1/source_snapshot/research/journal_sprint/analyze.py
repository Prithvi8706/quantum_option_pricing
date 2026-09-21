"""Rebuild descriptive tables and validation checks from preserved sprint outputs."""

from .checks import require

import csv
import json
from collections import defaultdict

import numpy as np

from .intervals import clopper_pearson
from .storage import ROOT, finish_run, sha256, start_run, write_json


def main():
    base = ROOT / "results/journal_sprint"
    inputs = [
        base / "prototype_v1/records.jsonl",
        base / "comparator_v1/summary.json",
        base / "historical_audit_v2/reference_rows.json",
    ]
    path = start_run(
        base / "analysis_v1",
        {
            "inputs": {str(p.relative_to(ROOT)): sha256(p) for p in inputs},
            "interpretation": "Exploratory fixed-grid summaries; no population generalization",
        },
    )
    groups = defaultdict(list)
    with inputs[0].open(encoding="utf-8") as stream:
        records = [json.loads(line) for line in stream]
    for row in records:
        key = (
            row["experiment"],
            row["condition"],
            row.get("shots_per_depth"),
            row.get("nominal_amplitude_key", row["a"]),
        )
        groups[key].append(row)
    expected = {"fixed": 14000, "direct": 11200, "split_pilot": 1400}
    actual = {name: sum(r["experiment"] == name for r in records) for name in expected}
    require(actual == expected, (actual, expected))
    cells = []
    for (experiment, condition, shots, amplitude), rows in groups.items():
        # Pilot-selected shot subgroups are selection-conditioned. Report only
        # descriptive counts here; do not attach binomial CI to those subgroups.
        n = len(rows)
        contained = sum(bool(r["contains"]) for r in rows) if rows[0]["a"] is not None else None
        ci = None
        if contained is not None and experiment != "split_pilot":
            lo, hi = clopper_pearson([contained], [n], 0.05)
            ci = [float(lo[0]), float(hi[0])]
        cells.append(
            dict(
                experiment=experiment,
                condition=condition,
                shots=shots,
                amplitude=amplitude,
                n=n,
                contained=contained,
                containment_ci95=ci,
                incompatible=sum(r["incompatible"] for r in rows),
                declarations=sum(r["declared_0.01"] for r in rows),
                false_declarations=sum(bool(r["erroneous_0.01"]) for r in rows)
                if contained is not None
                else None,
            )
        )
    write_json(path / "cell_uncertainty.json", cells)
    historical = json.loads(inputs[2].read_text(encoding="utf-8"))
    historic_summary = []
    for p in sorted({float(row["p"]) for row in historical}):
        rows = [row for row in historical if float(row["p"]) == p]
        stored = np.array([float(row["delta"]) for row in rows])
        observed = np.array([float(row["sim_price"]) for row in rows])
        reference = np.array([float(row["ref_price"]) for row in rows])
        bs = np.array([row["independent_black_scholes"] for row in rows])
        require(np.allclose(stored, abs(observed - reference), atol=1e-12))
        historic_summary.append(
            dict(
                p=p,
                n=len(rows),
                stored_mean_delta=float(stored.mean()),
                mean_absolute_bs_error=float(np.mean(abs(observed - bs))),
                mean_reference_bs_gap=float(np.mean(abs(reference - bs))),
            )
        )
    write_json(path / "historical_reference_summary.json", historic_summary)
    with (path / "historical_reference_summary.csv").open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(historic_summary[0]))
        writer.writeheader()
        writer.writerows(historic_summary)
    write_json(
        path / "integrity.json",
        {"expected_records": expected, "actual_records": actual, "historical_delta_identity": True},
    )
    # Pooled strata are independent but not identically distributed. A Hoeffding
    # band covers the equal-weight fixed-grid mean, not a contract population.
    write_json(
        path / "uncertainty_notes.json",
        {
            "pooled_n": 1400,
            "two_sided_95_hoeffding_half_width": float(np.sqrt(np.log(40) / (2 * 1400))),
            "zero_failures_1400_one_sided95_upper_average_failure": float(1 - 0.05 ** (1 / 1400)),
            "warning": "Per-cell CIs are marginal, not simultaneous. No population claim.",
        },
    )
    finish_run(path)
    print(json.dumps(historic_summary, indent=2))
    print("Record counts verified:", actual)


if __name__ == "__main__":
    main()
