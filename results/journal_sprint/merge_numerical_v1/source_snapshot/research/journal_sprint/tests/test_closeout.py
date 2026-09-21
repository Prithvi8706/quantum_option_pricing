import pytest

from research.journal_sprint.closeout import rate_interval, summarize_cell


def test_rate_interval_boundaries():
    assert rate_interval(0, 0) is None
    assert rate_interval(0, 200)[0] == 0
    assert rate_interval(200, 200)[1] == 1
    assert rate_interval(0, 200)[1] == pytest.approx(1 - 0.025 ** (1 / 200))


def test_refusals_are_not_coverage_failures_among_executed():
    common = {"false_declaration": False, "a_queries": 0, "total_shots": 0}
    refusal = {**common, "state": "pre_refusal", "declared": False, "price_contains": False}
    success = {
        **common,
        "state": "precision_met",
        "declared": True,
        "price_contains": True,
        "price_interval": [0, 1],
    }
    result = summarize_cell([refusal, success])
    assert result["delivery_rate"] == 0.5
    assert result["price_containment_among_executed"] == 1
    assert result["attempts"] == 2 and result["executed"] == 1


def test_no_output_has_no_conditional_rate():
    result = summarize_cell(
        [
            {
                "state": "pre_refusal",
                "declared": False,
                "false_declaration": False,
                "price_contains": False,
                "a_queries": 0,
                "total_shots": 0,
            }
        ]
    )
    assert result["false_among_declarations"] is None
    assert result["price_containment_among_executed"] is None
