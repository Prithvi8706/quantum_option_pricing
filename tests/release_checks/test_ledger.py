import pytest
from research.release_checks.ledger import total, verify_ledger
from .test_targets import evidence


def test_all_archived_ledgers_and_mutation():
    rows = [r for c in evidence()["comparisons"] for r in c["alternatives"]]
    assert all(verify_ledger(r) for r in rows)
    row = rows[2]
    row["resources"]["total_cx_projection"] -= 1
    with pytest.raises(ValueError, match="mismatch"):
        verify_ledger(row)


def test_swaps_and_boolean_counts():
    r = dict(a_cx_projection=2, controlled_a_cx_projection=3, zero_reflection_cx_projection=4)
    s = dict(M=4, repetitions=1, phase_qubits=2)
    assert total(r, s) == 40
    s["M"] = True
    with pytest.raises(ValueError):
        total(r, s)
