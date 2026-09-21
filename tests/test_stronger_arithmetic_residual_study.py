"""Full signed-residual error ledger and bounded comparison decisions."""

from fractions import Fraction

import pytest

from research.stronger_arithmetic.run_residual import complete_budget, summarize
from research.stronger_arithmetic.residual import menu


def test_residual_fixed_menu_is_independent_of_primary_winners():
    specs = menu()
    assert len(specs) == len({tuple(sorted(s.items())) for s in specs}) == 9
    assert {s["width"] for s in specs} == {48}
    assert {s["fraction_bits"] for s in specs} == {24}
    assert {s["degree"] for s in specs} == {8, 12, 16}
    assert {s["reductions"] for s in specs} == {1, 2, 3}


def certificate():
    return dict(
        dimension=2,
        sensitivity_upper="32",
        arithmetic_price_error_upper="0.1",
        offset_certificate={"error_upper": "0.02"},
        offset_bridge_upper="0.03",
        decoding_error_upper="0.04",
        decoder_scale=32.0,
        decoder_intercept=-10.0,
    )


def test_every_error_source_and_probability_scale_are_charged():
    result = complete_budget(certificate(), {"components": {"representation": "0.2"}}, "0.001")
    assert Fraction(result["deterministic_upper"]) >= Fraction("0.518")
    assert Fraction(result["components"]["preparation"]) == Fraction("0.128")
    assert Fraction(result["beta_upper_rational"]) == 16
    assert result["schedule"]["status"] == "ideal_plan"
    assert result["physical_execution_error"] is None
    assert not result["confirmation_admitted"]
    assert result["decoder_intercept"] == -10


def test_residual_fails_closed_when_loading_uses_budget():
    result = complete_budget(certificate(), {"components": {"representation": "0.2"}}, "1")
    assert result["schedule"]["status"] == "deterministic_budget_exhausted"


@pytest.mark.parametrize(
    "value,winner", [(50, "residual_arithmetic"), (100, "tie"), (200, "reflection")]
)
def test_residual_decision_keeps_ties_and_unfavorable_results(value, winner):
    prior = {
        "summary": [
            dict(
                case=case,
                reflection_reference={"resources": {"control_cancelled_total_cx_projection": 100}},
                best_arithmetic={"resources": {"control_cancelled_total_cx_projection": 300}},
            )
            for case in ("D1", "D2")
        ]
    }
    rows = [
        dict(
            case=case,
            status="ideal_plan",
            resources={"control_cancelled_total_cx_projection": value},
        )
        for case in ("D1", "D2")
    ]
    rows.append(dict(case="D1", status="certificate_failed", resources=None))
    result = summarize(rows, prior)
    assert all(r["winner_vs_reflection"] == winner for r in result)
    assert all(r["feasible_configurations"] == 1 for r in result)
