from research.journal_sprint.run_transfer_grid import SHIFTS, cells, trial


def test_complete_matrix_and_valid_guard():
    matrix = list(cells())
    assert len(matrix) == len(set(matrix)) == 324
    assert all(
        0 <= 0.02 + df <= 1 and 0 <= 0.07 + dg <= 1 and abs(df) <= 0.03 and abs(dg) <= 0.03
        for df, dg in SHIFTS
    )


def test_refusal_never_needs_truth_or_acquires():
    row = trial("E030", 16384, 0, "direct", 0, {"refused": True}, None)
    assert row["status"] == "pre_refusal"
    assert set(row["cost"].values()) == {0}
    assert "counts" not in row


def test_calibration_cost_and_deterministic_streams():
    prepared = dict(
        refused=False,
        bound_total=0.01,
        bounds=dict(sensitivity=1.0, offset=0.0),
        designs={"direct": dict(depths=[0], shots=[100], cost=dict(pricing_shots=100))},
    )
    truth = dict(amplitude=0.2, price=0.2)
    low = trial("E001", 4096, 0, "direct", 0, prepared, truth)
    high = trial("E001", 16384, 0, "direct", 0, prepared, truth)
    assert low == trial("E001", 4096, 0, "direct", 0, prepared, truth)
    assert high["cost"]["total_shots"] - low["cost"]["total_shots"] == 24576
    assert high["shots"] == low["shots"]
    assert high["seed_key"] != low["seed_key"]
