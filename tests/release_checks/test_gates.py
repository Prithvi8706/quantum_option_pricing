import pytest
from research.release_checks.gates import GATES, scientific_status


def test_no_automatic_admission():
    gates = dict.fromkeys(GATES, False)
    assert not scientific_status(gates)["submission_ready"]
    gates["fresh_confirmation"] = True
    with pytest.raises(ValueError, match="promotion"):
        scientific_status(gates)


def test_missing_and_nonboolean_gates():
    with pytest.raises(ValueError):
        scientific_status({})
    with pytest.raises(ValueError):
        scientific_status(dict.fromkeys(GATES, 0))
