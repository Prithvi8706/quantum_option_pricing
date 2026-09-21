import numpy as np
import pytest

from research.journal_sprint.calibrated_readout import invert_calibrated
from research.journal_sprint.run_transfer_price import CONDITIONS, rates


@pytest.mark.parametrize("transfer", [(-0.1, 0), (np.nan, 0), (0,), (0, 2)])
def test_invalid_transfer_bound(transfer):
    with pytest.raises(ValueError, match="transfer bounds"):
        invert_calibrated([400], [1000], [0], [20, 70], [1000] * 2, transfer_bounds=transfer)


def test_guard_contains_unexpanded_hull():
    args = ([3840], [10000], [0], [20, 70], [1000] * 2)
    plain, _ = invert_calibrated(*args)
    guarded, _ = invert_calibrated(*args, transfer_bounds=(0.03, 0.03))
    assert guarded.hull[0] <= plain.hull[0]
    assert guarded.hull[1] >= plain.hull[1]


def test_large_guard_returns_full_set():
    result, _ = invert_calibrated([40], [100], [0], [0, 0], [100] * 2, transfer_bounds=(0.6, 0.6))
    assert result.hull == (0, 1)


@pytest.mark.parametrize("condition", CONDITIONS)
def test_declared_transfer_scope(condition):
    cal, f, g = rates(condition)
    maximum_change = max(np.max(abs(f - cal[0])), np.max(abs(g - cal[1])))
    assert (maximum_change <= 0.03 + 1e-14) == (condition != "outside_bound")


def test_guarded_shift_contains_target():
    # a=.4 with validation f=.05/g=.04 has q=.414; calibration f=.02/g=.07.
    guarded, _ = invert_calibrated(
        [41400], [100000], [0], [2000, 7000], [100000] * 2, transfer_bounds=(0.03, 0.03)
    )
    plain, _ = invert_calibrated([41400], [100000], [0], [2000, 7000], [100000] * 2)
    assert guarded.contains(0.4)
    assert not plain.contains(0.4)
