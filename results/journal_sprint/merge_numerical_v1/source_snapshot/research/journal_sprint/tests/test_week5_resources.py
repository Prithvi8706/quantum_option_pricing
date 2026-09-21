import pytest

from research.journal_sprint.larger_resources import resource_matrix


def test_old_matrix_unchanged():
    matrix = resource_matrix("week3")
    assert len(matrix) == len(set(matrix)) == 20
    assert {r[3] for r in matrix} == {0, 1}


def test_missing_profiles_only():
    matrix = resource_matrix("week5-k2")
    assert len(matrix) == len(set(matrix)) == 10
    assert {r[3] for r in matrix} == {2}
    assert not set(matrix).intersection(resource_matrix("week3"))


def test_unknown_profile_rejected():
    with pytest.raises(ValueError):
        resource_matrix("bad")
