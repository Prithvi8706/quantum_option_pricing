"""Combined decision must preserve ties, infeasibility and exact integer costs."""

from research.stronger_arithmetic.analyze import analyze


def record(case, cost, status="ideal_plan"):
    return dict(
        case=case,
        spec=None,
        status=status,
        budget={"deterministic_upper": "0.1", "schedule": {"M": 128}},
        resources={"control_cancelled_total_cx_projection": cost},
    )


def test_combined_menu_retains_all_rows_and_ties():
    primary = {
        "rows": [record("D1", 100), record("D2", 200)],
        "summary": [
            dict(
                case=c,
                reflection_reference={
                    "degree": 64,
                    "resources": {"control_cancelled_total_cx_projection": 100},
                },
            )
            for c in ("D1", "D2")
        ],
    }
    residual = {
        "rows": [record("D1", 100), record("D2", 50), record("D2", None, "certificate_failed")]
    }
    result = analyze(primary, residual)
    assert len(result["rows"]) == 5
    d1, d2 = result["decisions"]
    assert len(d1["arithmetic_ties"]) == 2
    assert d1["reflection_tied_for_minimum"]
    assert not d2["reflection_tied_for_minimum"]
    assert d2["reflection_over_best_arithmetic_rational"] == "2"
    assert not result["quantum_over_classical_advantage"]
    assert all(r["production_choice"] is None for r in result["decisions"])
