import pytest
from research.release_checks.schedules import verify_schedule
from .test_targets import evidence


def test_all_fixed_schedules():
    rows = [r for c in evidence()["comparisons"] for r in c["alternatives"]]
    assert all(verify_schedule(r) for r in rows)
    rows[-1]["budget"]["schedule"]["a_calls"] -= 1
    with pytest.raises(ValueError, match="call count"):
        verify_schedule(rows[-1])


def test_repetitions_cannot_be_reduced():
    row = evidence()["comparisons"][0]["alternatives"][-1]
    row["budget"]["schedule"]["repetitions"] = 1
    with pytest.raises(ValueError, match="confidence"):
        verify_schedule(row)
