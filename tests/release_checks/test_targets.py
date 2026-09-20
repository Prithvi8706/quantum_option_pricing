from pathlib import Path
import pytest
from research.release_checks.json_io import read
from research.release_checks.targets import verify_targets


def evidence():
    return read(
        Path(__file__).resolve().parents[2]
        / "results/journal_sprint/matched_arithmetic_v1/results.json"
    )


def test_market_scope_and_duplicate_routes():
    data = evidence()
    assert verify_targets(data)["configurations"] == 12
    data["comparisons"][0]["alternatives"][1] = data["comparisons"][0]["alternatives"][0]
    with pytest.raises(ValueError, match="menu"):
        verify_targets(data)


def test_changed_contract_is_rejected():
    data = evidence()
    data["comparisons"][0]["case"]["strike"] = 100
    with pytest.raises(ValueError, match="financial"):
        verify_targets(data)
