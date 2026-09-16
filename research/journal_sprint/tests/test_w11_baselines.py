"""Pre-acquisition equivalence, stream separation, accounting and recovery tests."""

import json

import numpy as np
import pytest

from research.journal_sprint.asian_basket import Basket, estimate, setup
from research.journal_sprint import run_w11_baselines as runner
from research.journal_sprint.storage import write_json
from research.journal_sprint.w11_baselines import (
    METHODS, deployment, method_setup, pilot_schedule, seed_for,
)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("dims", [(1, 1), (2, 12), (4, 52)])
def test_method_specific_setup_equivalence(method, dims):
    c = Basket(*dims, 100.)
    old, new = setup(c), method_setup(c, method)
    for key in new:
        np.testing.assert_allclose(new[key], old[key], atol=1e-12, rtol=1e-12)
    assert ("factor" in new) != ("residual" in new)
    actual = estimate(c, new, 5, 987, method, 1.)
    expected = estimate(c, old, 5, 987, method, 1.)
    np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=1e-12)


def test_frozen_schedule_and_stream_separation():
    schedule = pilot_schedule()
    assert schedule == pilot_schedule()
    assert len(schedule) == 132
    assert [s["phase"] for s in schedule[:4]] == ["warmup"] * 4
    for start in range(4, 132, 4):
        block = schedule[start:start+4]
        assert {s["method"] for s in block} == set(METHODS)
        assert len({(s["assets"], s["dates"], s["power"], s["rep"]) for s in block}) == 1
    assert len({tuple(s["method"] for s in schedule[i:i+4])
                for i in range(4, 132, 4)}) > 1
    seeds = [seed_for(purpose, phase, i) for purpose in ("training", "evaluation", "order")
             for phase in ("pilot", "warmup") for i in range(132)]
    assert len(seeds) == len(set(seeds))


@pytest.mark.parametrize("method", METHODS)
def test_deployment_costs_and_repeatability(method):
    spec = dict(phase="test", assets=1, dates=1, strike=100., power=5, rep=0, method=method)
    a, b = deployment(Basket(1, 1, 100.), spec), deployment(Basket(1, 1, 100.), spec)
    assert a["value"] == b["value"]
    assert a["beta"] == b["beta"]
    assert a["training_count"] == (0 if method == "rqmc_raw" else 1024)
    assert a["evaluation_count"] == 32
    assert a["standalone_seconds"] == pytest.approx(
        a["setup_seconds"] + a["training_seconds"] + a["evaluation_seconds"]
    )
    assert a["amortized_100_seconds"] <= a["amortized_10_seconds"] <= a["standalone_seconds"]


def test_unknown_method_rejected():
    with pytest.raises(ValueError):
        method_setup(Basket(1, 1, 100.), "typo")


def test_thread_configuration_required(tmp_path, monkeypatch):
    monkeypatch.delenv("OMP_NUM_THREADS", raising=False)
    with pytest.raises(ValueError, match="thread"):
        runner.run(tmp_path / "bad")
    assert not (tmp_path / "bad").exists()


def configure(monkeypatch):
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        monkeypatch.setenv(name, "1")
    monkeypatch.setattr(runner, "inventory_environment", lambda: {"test_fixture": True})


def test_acquisition_failure_is_preserved(tmp_path, monkeypatch):
    configure(monkeypatch)

    def failure(contract, spec):
        raise ArithmeticError("injected failure")

    out = tmp_path / "failed"
    with pytest.raises(ArithmeticError):
        runner.run(out, acquire=failure)
    assert json.loads((out / "failure.json").read_text())["attempt"] == 0
    assert not (out / "complete.json").exists()
    states = runner.audit_events(out)["states"]
    assert states["0"] == "failed"
    assert states["1"] == "not_started"
    with pytest.raises(FileExistsError):
        runner.run(out, acquire=failure)


def test_soft_cap_records_partial_without_acquisition(tmp_path, monkeypatch):
    configure(monkeypatch)
    ticks = iter([0., 2., 3.])
    monkeypatch.setattr(runner.time, "perf_counter", lambda: next(ticks))
    out = tmp_path / "capped"
    result = runner.run(out, cap_seconds=1, acquire=lambda *args: pytest.fail("unexpected call"))
    assert result["status"] == "time_cap_partial"
    assert result["completed"] == 0
    assert result["planned"] == 132


def test_raw_written_before_terminal_event_is_reconcilable(tmp_path):
    write_json(tmp_path / "schedule.json", pilot_schedule())
    runner.append_event(tmp_path, dict(attempt=0, status="started"))
    write_json(tmp_path / "row_000.json", {"fixture": True})
    assert runner.audit_events(tmp_path)["states"]["0"] == "raw_present_needs_reconciliation"


def test_complete_event_missing_raw_is_detected(tmp_path):
    write_json(tmp_path / "schedule.json", pilot_schedule())
    runner.append_event(tmp_path, dict(attempt=0, status="completed"))
    assert runner.audit_events(tmp_path)["states"]["0"] == "completed_event_missing_raw"


def test_numeric_replay_and_tamper_detection(tmp_path, monkeypatch):
    configure(monkeypatch)
    tiny = [dict(attempt=0, phase="warmup", assets=1, dates=1,
                 strike=100., power=5, rep=0, method="rqmc_cv")]
    monkeypatch.setattr(runner, "pilot_schedule", lambda: tiny)
    out = tmp_path / "replay"
    runner.run(out)
    assert runner.verify(out)["replayed_rows"] == 1
    # Simulate tampering using exclusive replacement in this isolated test fixture.
    row = out / "row_000.json"
    row.unlink()
    write_json(row, {"tampered": True})
    with pytest.raises(ValueError):
        runner.verify(out)
