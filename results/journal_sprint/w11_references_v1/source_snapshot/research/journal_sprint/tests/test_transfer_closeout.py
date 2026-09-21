import json

import pytest

from research.journal_sprint.closeout_transfer_grid import contrasts, validate_config
from research.journal_sprint.run_transfer_grid import cells
from research.journal_sprint.storage import ROOT


@pytest.mark.parametrize(
    "field,value",
    [
        ("repetitions", 99),
        ("calibration_sizes", [4096]),
        ("alpha_validation", 0.05),
        ("transfer_bounds", [0.04, 0.03]),
        ("tolerance", 2.0),
        ("budget", 73728),
    ],
)
def test_config_mutation_rejected(field, value):
    config = json.loads(
        (ROOT / "results/journal_sprint/week6_transfer_grid_v1/planned.json").read_text()
    )["config"]
    validate_config(config, config["input_manifests"])
    config[field] = value
    with pytest.raises(ValueError, match="configuration"):
        validate_config(config, config["input_manifests"])


def fake_cells():
    return [
        dict(
            contract=cid,
            calibration_n=n,
            position=p,
            design=d,
            attempts=100,
            executed=0 if cid == "E030" else 100,
            declared=0 if cid == "E030" else (20 if n == 4096 else 30),
            acquisition_totals=dict(calibration_shots=0 if cid == "E030" else 200 * n),
        )
        for cid, n, p, d in cells()
    ]


def test_contrast_denominators_and_costs():
    result = contrasts(fake_cells())
    assert len(result["calibration_contrasts"]) == 162
    assert len(result["design_contrasts"]) == 216
    assert len(result["rate_ranges"]) == 36
    for row in result["calibration_contrasts"]:
        if row["contract"] == "E030":
            assert row["delivery_difference"] is None
            assert row["added_acquired_shots"] == 0
        else:
            assert row["delivery_difference"] == pytest.approx(0.1)
            assert row["added_acquired_shots"] == 2457600


@pytest.mark.parametrize("mutation", ["duplicate", "missing"])
def test_bad_matrix_rejected(mutation):
    rows = fake_cells()
    rows = rows + [rows[0]] if mutation == "duplicate" else rows[:-1]
    with pytest.raises(ValueError, match="matrix"):
        contrasts(rows)
