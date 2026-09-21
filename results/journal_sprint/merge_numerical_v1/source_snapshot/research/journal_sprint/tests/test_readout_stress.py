import pytest

from research.journal_sprint.intervals import invert
from research.journal_sprint.readout_stress import invert_readout, readout_probability


def test_readout_endpoints():
    assert readout_probability(0, 0.02, 0.07) == pytest.approx(0.02)
    assert readout_probability(1, 0.02, 0.07) == pytest.approx(0.93)


def test_identity_readout():
    corrected = invert_readout([400, 750, 90], [1024] * 3, [0, 1, 2], 0, 0)
    original = invert([400, 750, 90], [1024] * 3, [0, 1, 2])
    assert corrected.hull == pytest.approx(original.hull)


def test_corrected_known_readout():
    interval = invert_readout([int(10000 * 0.384)], [10000], [0], 0.02, 0.07)
    assert interval.contains(0.4)


def test_reject_nonpositive_contrast():
    with pytest.raises(ValueError):
        invert_readout([50], [100], [0], 0.6, 0.4)
