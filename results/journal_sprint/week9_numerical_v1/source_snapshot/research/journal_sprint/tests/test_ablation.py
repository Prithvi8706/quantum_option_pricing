from collections import Counter

import pytest

from research.journal_sprint.closeout_ablation import analyze, enclosed, validate_config
from research.journal_sprint.run_ablation import (
    cells,
    configuration,
    summarize,
    trial,
    valid_guards,
)


def test_matrix_and_valid_guards():
    keys = list(cells())
    assert len(keys) == len(set(keys)) == 216
    assert sum(len(valid_guards(k[3])) for k in keys) == 432
    assert valid_guards("stationary") == (0.0, 0.01, 0.03)
    assert valid_guards("small_transfer") == (0.01, 0.03)
    assert valid_guards("boundary_transfer") == (0.03,)


def test_refusal_without_target_or_cost():
    key = ("E030", 294912, 4096, "stationary", "direct")
    row = trial(key, 0, {"refused": True}, None)
    assert set(row["cost"].values()) == {0}
    assert "counts" not in row and len(row["arms"]) == 3
    result = summarize([row])
    assert result["acquired"] == 0 and result["refused"] == 1
    assert all(a["false_given_declaration"] is None for a in result["arms"].values())


def test_single_charge_shared_arms_and_nesting():
    p = dict(
        refused=False,
        bound_total=0.01,
        bounds=dict(sensitivity=1.0, offset=0.0),
        designs={"294912": {"direct": dict(depths=[0], shots=[100], cost={})}},
    )
    key = ("E001", 294912, 4096, "stationary", "direct")
    row = trial(key, 0, p, dict(amplitude=0.2, price=0.2))
    assert row == trial(key, 0, p, dict(amplitude=0.2, price=0.2))
    assert row["cost"]["total_shots"] == 8292
    assert all("cost" not in a and "counts" not in a for a in row["arms"].values())
    assert enclosed(row["arms"]["0.0"]["components"], row["arms"]["0.03"]["components"])


def test_enclosure_detects_missing_branch():
    assert enclosed([], [])
    assert not enclosed([(0, 0.1), (0.8, 0.9)], [(0, 0.2)])


@pytest.mark.parametrize(
    "field,value",
    [("budgets", [1]), ("guards", [0.04]), ("alpha_validation", 0.05), ("readiness_delivery", 0.5)],
)
def test_config_mutation(field, value):
    c = configuration({}, {})
    validate_config(c, {})
    c[field] = value
    with pytest.raises(ValueError, match="config"):
        validate_config(c, {})


def fake_summaries():
    rows = []
    for cid, b, n, c, d in cells():
        refused = cid in ("E030", "E038")
        rows.append(
            dict(
                contract=cid,
                budget=b,
                calibration_n=n,
                condition=c,
                design=d,
                acquired=0 if refused else 100,
                acquisition_totals=dict(total_shots=0 if refused else b + 2 * n),
                arms={
                    str(g): dict(
                        executed=0 if refused else 100,
                        declared=0 if refused or d == "direct" else 90,
                    )
                    for g in valid_guards(c)
                },
            )
        )
    return rows


def test_contrasts_and_readiness():
    result = analyze(fake_summaries())
    assert Counter(r["axis"] for r in result["contrasts"]) == dict(
        pricing=216, calibration=216, design=288, guard=288
    )
    assert all(s["passes"] and len(s["checks"]) == 12 for s in result["readiness"])
    refused = [r for r in result["contrasts"] if r["key"][0] == "E030"]
    assert all(r["delivery_difference"] is None for r in refused)
    rows = fake_summaries()
    rows[0]["arms"]["0.03"]["declared"] = 90
    assert not analyze(rows)["readiness"][0]["passes"]


def test_missing_analysis_cell_rejected():
    with pytest.raises(ValueError, match="matrix"):
        analyze(fake_summaries()[:-1])
