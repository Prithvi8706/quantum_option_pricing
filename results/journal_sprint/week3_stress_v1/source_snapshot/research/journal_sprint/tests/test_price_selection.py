import pytest

from research.journal_sprint.run_price_intervals import select_representation, summarize


def test_bound_only_selection_and_refusal():
    bad = {"n": 3, "scale": 0.25, "bias_bound": 2.0, "sensitivity": 100.0}
    good = {"n": 6, "scale": 0.125, "bias_bound": 0.2, "sensitivity": 100.0}
    assert select_representation([bad]) is None
    assert select_representation([bad, good]) == good
    with pytest.raises(ValueError):
        select_representation([dict(good, exact_price=10)])


def test_refusals_stay_in_denominator():
    row = {
        "declared": False,
        "state": "pre_refusal",
        "price_contains": False,
        "probability_contains": False,
        "false_declaration": False,
        "a_queries": 0,
        "radius": None,
    }
    result = summarize([row] * 3)
    assert result["trials"] == 3 and result["refused_rate"] == 1
    assert result["false_given_declaration"] is None
