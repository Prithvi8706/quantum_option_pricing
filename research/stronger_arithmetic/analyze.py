"""Export every bounded-study row and an honest combined logical decision."""

import argparse
import csv
from fractions import Fraction
from pathlib import Path

from research.journal_sprint.storage import ROOT, finish_run, sha256, write_json

PRIMARY = "results/journal_sprint/stronger_arithmetic_v1"
RESIDUAL = "results/journal_sprint/signed_residual_arithmetic_v1"


def analyze(primary, residual):
    rows = []
    for source, records in (("primary", primary["rows"]), ("residual", residual["rows"])):
        for row in records:
            spec = row["spec"] or dict(width=40, fraction_bits=20, degree=24, reductions=0)
            r = row["resources"] or {}
            rows.append(
                dict(
                    source=source,
                    case=row["case"],
                    arm=row.get("arm", "signed_residual"),
                    layout=row.get("layout", "reused"),
                    **spec,
                    status=row["status"],
                    deterministic_upper=row["budget"]["deterministic_upper"],
                    ae_size=row["budget"]["schedule"].get("M"),
                    a_calls=row["budget"]["schedule"].get("a_calls"),
                    conservative_cx=r.get("total_cx_projection"),
                    control_cancelled_cx=r.get("control_cancelled_total_cx_projection"),
                    a_qubits=r.get("a_qubits"),
                    total_qubits=r.get("total_qubits"),
                )
            )
    decisions = []
    for case in ("D1", "D2"):
        eligible = [r for r in rows if r["case"] == case and r["status"] == "ideal_plan"]
        reflection = next(r for r in primary["summary"] if r["case"] == case)[
            "reflection_reference"
        ]
        ref = reflection["resources"]["control_cancelled_total_cx_projection"]
        best = min(eligible, key=lambda r: r["control_cancelled_cx"]) if eligible else None
        minimum = min(ref, best["control_cancelled_cx"]) if best else ref
        winners = [r for r in eligible if r["control_cancelled_cx"] == minimum]
        decisions.append(
            dict(
                case=case,
                best_arithmetic=best,
                selected_reflection_degree=reflection["degree"],
                reflection_resources=reflection["resources"],
                minimum_logical_cx=minimum,
                arithmetic_ties=winners,
                reflection_tied_for_minimum=ref == minimum,
                reflection_over_best_arithmetic_rational=str(
                    Fraction(ref, best["control_cancelled_cx"])
                )
                if best
                else None,
                production_choice=None,
                physical_execution_error=None,
            )
        )
    return dict(
        rows=rows,
        decisions=decisions,
        candidate_status="standby",
        confirmation_admitted=False,
        quantum_over_classical_advantage=False,
        scope="matched quantum-route logical projections; not measured runtime",
    )


def run(path):
    from .verify import archive

    primary = archive(ROOT / PRIMARY)["results.json"]
    residual = archive(ROOT / RESIDUAL)["results.json"]
    for result in (primary, residual):
        if (
            result["candidate_status"] != "standby"
            or result["confirmation_admitted"] is not False
            or result["quantum_over_classical_advantage"] is not False
        ):
            raise ValueError("unexpected scientific promotion")
    if len(primary["rows"]) != 148 or len(residual["rows"]) != 18:
        raise ValueError("complete study row menus required")
    result = analyze(primary, residual)
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    write_json(
        path / "inputs.json",
        {
            name + "/" + file: sha256(ROOT / name / file)
            for name in (PRIMARY, RESIDUAL)
            for file in ("complete.json", "results.json")
        },
    )
    write_json(path / "summary.json", result)
    with (path / "all_rows.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result["rows"][0]))
        writer.writeheader()
        writer.writerows(result["rows"])
    finish_run(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
