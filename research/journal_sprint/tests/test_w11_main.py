"""Stage schedule, statistics and reference-gate checks before acquisition."""

import json

import numpy as np
import pytest

from research.journal_sprint import run_w11_main as runner
from research.journal_sprint.storage import write_json


def test_complete_schedules_are_disjoint_and_exclude_holdout():
    refs, main = runner.schedule_for("reference"), runner.schedule_for("main")
    assert len(refs) == 384
    assert len(main) == 2308
    assert main == runner.schedule_for("main")
    assert {s["phase"] for s in refs}.isdisjoint({s["phase"] for s in main})
    assert all(s["assets"] != 3 and s["dates"] != 24 for s in refs+main)
    for i in range(4, len(main), 4):
        assert len({s["method"] for s in main[i:i+4]}) == 4


def test_reference_mean_se_and_small_sample_handling():
    spec = runner.schedule_for("reference")[0]
    rows = [dict(spec=spec, result={"value": value}) for value in (1., 2., 3., 4.)]
    ref = runner.reference_summary(rows)["2/12/90"]
    assert ref["mean"] == 2.5
    assert ref["se"] == pytest.approx(np.std([1, 2, 3, 4], ddof=1)/2)
    assert runner.reference_summary(rows[:1])["2/12/90"]["se"] is None


def test_mean_interval_charges_all_repetitions_and_rmse_is_per_deployment():
    spec = runner.schedule_for("main")[4]
    fields = ("setup_seconds", "training_seconds", "evaluation_seconds",
              "amortized_10_seconds", "amortized_100_seconds")
    rows = [dict(spec=spec, result=dict(value=value, standalone_seconds=6.,
                                       evaluation_count=1024, training_count=1024,
                                       **{field: 1. for field in fields}))
            for value in (1., 2., 3., 4.)]
    result = runner.main_summary(rows, {"2/12/90": {"mean": 2.5, "se": .0001}})[0]
    assert result["rmse_to_reference"] == pytest.approx(np.sqrt(1.25))
    assert result["aggregate_mean_cost_seconds"] == 24
    assert result["mean_standalone_seconds"] == 6
    assert result["aggregate_evaluation_count"] == 4096
    assert result["aggregate_training_count"] == 4096
    assert result["reference_se"] == .0001


def test_partial_reference_rejected_before_main(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "verify_inventory", lambda path: 0)
    write_json(tmp_path / "planned.json", {"config": {"stage": "reference"}})
    write_json(tmp_path / "schedule.json", runner.schedule_for("reference"))
    with pytest.raises(ValueError, match="incomplete"):
        runner.reference_gate(tmp_path)


def test_reference_precision_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "verify_inventory", lambda path: 0)
    schedule = runner.schedule_for("reference")
    write_json(tmp_path / "planned.json", {"config": {"stage": "reference"}})
    write_json(tmp_path / "schedule.json", schedule)
    for spec in schedule:
        write_json(tmp_path / f"row_{spec['attempt']:04d}.json",
                   dict(spec=spec, result={"value": 1. + 1e-4*spec["rep"]}))
    assert len(runner.reference_gate(tmp_path)) == 12
    path = tmp_path / "row_0000.json"
    row = json.loads(path.read_text())
    path.unlink()
    row["result"]["value"] = 100.
    write_json(path, row)
    with pytest.raises(ValueError, match="precision"):
        runner.reference_gate(tmp_path)


def test_reference_stage_small_replay(tmp_path, monkeypatch):
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        monkeypatch.setenv(name, "1")
    tiny = [dict(attempt=i, assets=1, dates=1, strike=100., power=5,
                 rep=i, method="rqmc_cv", phase="reference") for i in range(2)]
    monkeypatch.setattr(runner, "schedule_for", lambda stage: tiny)
    monkeypatch.setattr(runner, "inventory_environment", lambda: {"test_fixture": True})
    out = tmp_path / "reference"
    assert runner.run(out, "reference")["completed"] == 2
    assert runner.verify(out)["replayed_rows"] == 2


def test_unknown_stage_rejected():
    with pytest.raises(ValueError):
        runner.schedule_for("typo")
