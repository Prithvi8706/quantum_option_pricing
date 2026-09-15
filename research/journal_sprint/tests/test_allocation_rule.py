"""Allocation, sample separation, reference inversion and budget regressions."""

import inspect
import math

import pytest
from scipy.stats import beta

from research.journal_sprint.allocation_rule import allocate, cp_decision, preselect
from research.journal_sprint.encoding_decision import Encoding
from research.journal_sprint.run_allocation import trial


def test_preselect_has_no_truth_and_no_noise_dominance_claim():
    menu = [Encoding("old", 10, 0, .5, 1), Encoding("exact", 2, 0, .1, 1)]
    assert preselect(menu)["selected"] == "exact"
    assert set(inspect.signature(preselect).parameters) == {"encodings", "tolerance"}
    assert preselect([Encoding("bad", 2, 0, 1, 1)])["selected"] is None


@pytest.mark.parametrize("s", [0, 1, 512, 1023, 1024])
def test_allocation_budget_and_forecast_identity(s):
    e = Encoding("e", 20, 0, .1, 1)
    result = allocate(e, s)
    assert result["forecast_only"] is True
    assert result["pricing_shots"] + 2 * result["calibration_per_state"] + 1024 == 65536
    assert len(result["forecasts"]) == 5
    finite = [f for f in result["forecasts"] if f["projected_radius"] is not None]
    if finite:
        best = min(finite, key=lambda f: (f["projected_radius"], f["calibration_per_state"]))
        assert best["calibration_per_state"] == result["calibration_per_state"]


@pytest.mark.parametrize("kwargs", [
    {"pilot_successes": True}, {"pilot_successes": 1025}, {"pilot_successes": -1},
    {"pilot_successes": 1, "menu": (40000,)},
    {"pilot_successes": 1, "menu": (1024, 1024)},
    {"pilot_successes": 1, "design_readout": (.6, .6)},
    {"pilot_successes": 1, "design_readout": (float("nan"), 0)},
])
def test_invalid_allocation(kwargs):
    with pytest.raises(ValueError):
        allocate(Encoding("e", 2, 0, .1, 1), **kwargs)


def test_cp_matches_independent_corner_formula():
    e = Encoding("e", 30, -4, .2, 1)
    m, n, s, cal = 10000, 20000, 1000, [200, 700]
    result = cp_decision(e, s, n, cal, m)
    fl, gl = [beta.ppf(.025 / 4, x, m - x + 1) for x in cal]
    fu, gu = [beta.ppf(1 - .025 / 4, x + 1, m - x) for x in cal]
    ql = beta.ppf(.025 / 2, s, n - s + 1)
    qu = beta.ppf(1 - .025 / 2, s + 1, n - s)
    lo = max(0, (ql - fu) / (1 - fu - gl))
    hi = min(1, (qu - fl) / (1 - fl - gu))
    assert result["interval"] == pytest.approx([-4 + 30 * lo - .2, -4 + 30 * hi + .2],
                                                abs=1e-9)


def test_pilot_cannot_be_included_in_terminal_interface():
    assert "pilot_successes" not in inspect.signature(cp_decision).parameters
    with pytest.raises(ValueError):
        cp_decision(Encoding("e", 2, 0, .1, 1), 12, 10, [1, 2], 100)
    with pytest.raises(ValueError):
        cp_decision(Encoding("e", 2, 0, .1, 1), 1, 10, [True, 2], 100)


@pytest.mark.parametrize("arm", ["fixed_cp", "pilot_cp", "single_hoeffding"])
def test_runner_separate_counts_cost_and_replay(arm):
    # Synthetic fixture, not measured circuit data or a physical error model.
    profiles = {}
    for label, scale in [("linearized", 10), ("exact_table", 2)]:
        profiles[label] = dict(bounds=dict(sensitivity=scale, offset=0, support=.01,
                                          grid=.01, encoding=0), amplitude=.2,
                               profiles={"0": {"gates": {"cx": 126}}})
    row = trial("E001", profiles, 0, "swapped", arm, 0)
    assert row == trial("E001", profiles, 0, "swapped", arm, 0)
    assert row["total_shots"] == sum(row[k] for k in
                                      ("pilot_shots", "calibration_shots", "pricing_shots"))
    assert row["total_shots"] <= 65536
    assert row["total_cx"] == (row["pilot_shots"] + row["pricing_shots"]) * 126
    if arm in ("fixed_cp", "pilot_cp"):
        assert row["total_shots"] == 65536
    if row["successes"] is not None:
        assert 0 <= row["successes"] <= row["pricing_shots"]
    if row["radius"] is not None:
        assert math.isfinite(row["radius"])
