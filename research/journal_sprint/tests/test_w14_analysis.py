"""Independent denominator and zero-declaration fixtures; no acquisitions."""

import pytest

from research.journal_sprint.w14_analysis import confidence_summary, rate


def test_empty_set_is_an_unconditional_miss():
    rows = [
        dict(decision=dict(interval=None, status="incompatible")),
        dict(decision=dict(interval=[0.1, 0.3], status="precision_met")),
    ]
    result = confidence_summary(rows, 0.2)
    assert result["hull_containment_unconditional"]["estimate"] == 0.5
    assert result["interval_miss_unconditional"]["successes"] == 1
    assert result["interval_miss_given_return"]["denominator"] == 1
    assert result["erroneous_declaration_unconditional"]["denominator"] == 2


def test_no_declarations_has_no_conditional_rate():
    result = confidence_summary([dict(decision=dict(interval=None, status="incompatible"))], 0.2)
    assert result["erroneous_given_declaration"]["estimate"] is None
    assert result["erroneous_given_declaration"]["denominator"] == 0


def test_native_cap_remains_in_non_delivery_denominator():
    result = confidence_summary(
        [
            dict(
                status="resource_capped",
                price_interval=None,
                totals=dict(shots=256, a_equivalent_queries=256, cx=512),
            )
        ],
        0.2,
        native=True,
    )
    assert result["attempts"] == result["resource_capped"] == 1
    assert result["delivery"]["estimate"] == 0
    assert result["empty_confidence_sets"] == 0
    assert result["interval_miss_given_return"]["estimate"] is None
    assert result["costs"]["shots"]["total"] == 256


def test_erroneous_declaration_requires_delivery_and_dollar_error():
    rows = [
        dict(decision=dict(interval=[3.0, 3.2], status="precision_met")),
        dict(decision=dict(interval=[3.0, 9.0], status="unresolved")),
    ]
    result = confidence_summary(rows, 0.2)
    assert result["erroneous_declaration_unconditional"]["estimate"] == 0.5
    assert result["erroneous_given_declaration"]["estimate"] == 1


def test_pointwise_zero_events_is_not_zero_risk():
    assert rate(0, 16)["pointwise_cp95"][1] == pytest.approx(0.205907, abs=1e-6)
    assert rate(0, 8)["pointwise_cp95"][1] == pytest.approx(0.369417, abs=1e-6)
