from pathlib import Path
import pytest
from research.release_checks.finite import verify_finite
from research.release_checks.json_io import read


def test_finite_coverage_is_not_trial_count():
    rows = read(
        Path(__file__).resolve().parents[2]
        / "results/journal_sprint/matched_arithmetic_v1/finite.json"
    )
    result = verify_finite(rows)
    assert result["grid_inputs"] == 292
    assert not result["independent_trials"]
    rows[0]["paths"] = 3
    with pytest.raises(ValueError, match="coverage"):
        verify_finite(rows)
