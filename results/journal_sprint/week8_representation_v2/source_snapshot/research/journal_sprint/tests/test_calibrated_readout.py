import pytest

from research.journal_sprint.calibrated_readout import invert_calibrated
from research.journal_sprint.readout_stress import invert_readout


def test_calibration_enclosure_contains_known_solution():
    known = invert_readout([3840], [10000], [0], 0.02, 0.07, alpha=0.025)
    result, calibration = invert_calibrated([3840], [10000], [0], [20, 70], [1000] * 2)
    assert result.contains(0.4)
    assert result.hull[0] <= known.hull[0]
    assert result.hull[1] >= known.hull[1]
    assert calibration["positive_contrast_certified"]
    assert result.alpha == pytest.approx(0.05)


def test_uncertified_contrast_returns_full_set():
    result, calibration = invert_calibrated([10], [100], [0], [5, 5], [10, 10])
    assert not calibration["positive_contrast_certified"]
    assert result.hull == (0, 1)


@pytest.mark.parametrize("errors,n", [([0], [100]), ([0, 0, 0], [100] * 3)])
def test_requires_two_calibration_states(errors, n):
    with pytest.raises(ValueError, match="two calibration"):
        invert_calibrated([40], [100], [0], errors, n)


def test_rejects_depth_mismatch():
    with pytest.raises(ValueError):
        invert_calibrated([40], [100], [0, 1], [2, 7], [100, 100])


def test_rejects_invalid_allocation():
    with pytest.raises(ValueError):
        invert_calibrated([40], [100], [0], [2, 7], [100, 100], 0.6, 0.6)
