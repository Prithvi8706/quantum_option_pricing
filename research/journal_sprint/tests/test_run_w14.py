"""Fixture-isolated campaign, provenance, durable failures and replay."""

import json
from pathlib import Path

import pytest

from research.journal_sprint import run_w14 as runner
from research.journal_sprint.asian_basket import Basket
from research.journal_sprint.asian_encoding import grid
from research.journal_sprint.storage import sha256
from research.journal_sprint.w14_analysis import analyze


@pytest.fixture(autouse=True)
def isolated(monkeypatch):
    contract = Basket(1, 2, 71, spot=73, sigma=0.22)
    monkeypatch.setattr(runner, "CONTRACT", contract)
    monkeypatch.setattr(runner, "TRIALS", 2)
    monkeypatch.setattr(runner, "NATIVE_TRIALS", 1)
    monkeypatch.setattr(runner, "NAMESPACE", "TEST_ONLY_week14_fixture")
    monkeypatch.setattr(runner, "input_identity", lambda: {"fixture": "only"})

    def record():
        data = grid(contract, 1, 3.0)
        return dict(
            case=[1, 2, 1],
            basket=vars(contract),
            **{k: data[k].tolist() for k in ("normals", "weights", "raw", "control")},
        )

    monkeypatch.setattr(runner, "input_record", record)
    monkeypatch.setattr(
        runner,
        "dependencies",
        lambda: {"research/journal_sprint/run_w14.py": sha256(Path(runner.__file__))},
    )


def test_real_fixture_campaign_replays_and_no_overwrite(tmp_path):
    path = tmp_path / "fixture"
    runner.run(path)
    assert runner.verify(path)["tasks"] == 79
    assert len(analyze(path)["cells"]) == 58
    with pytest.raises(FileExistsError):
        runner.run(path)
    setup = json.loads((path / "setup__result.json").read_text())["value"]
    assert set(setup["admission"].values()) == {"unknown_bias"}
    matched = json.loads((path / "raw_csae_1__result.json").read_text())["value"]
    ignored = json.loads((path / "raw_csae_2__result.json").read_text())["value"]
    assert matched["counts"] == ignored["counts"]


def simple_campaign(perform):
    def task(emit):
        emit("draw", {"counts": [3], "shots": [9]})
        return {"answer": 0.173}

    perform("fixture", task)


@pytest.mark.parametrize(
    "mutation",
    [
        "source",
        "config",
        "environment",
        "native",
        "input",
        "extra",
        "nested_complete",
        "missing",
        "result",
        "timestamp",
    ],
)
def test_tampering_even_if_rehashed(tmp_path, monkeypatch, mutation):
    monkeypatch.setattr(runner, "campaign", simple_campaign)
    path = tmp_path / "fixture"
    runner.run(path)
    if mutation == "extra":
        (path / "extra.json").write_text("{}")
    elif mutation == "nested_complete":
        (path / "unexpected").mkdir()
        (path / "unexpected/complete.json").write_text("{}")
    elif mutation == "missing":
        (path / "fixture__draw.json").unlink()
    else:
        target = path / ("fixture__result.json" if mutation == "result" else "planned.json")
        value = json.loads(target.read_text())
        if mutation == "result":
            value["value"]["answer"] = 0.71
        elif mutation == "timestamp":
            value["started_utc"] = "not a timestamp"
        else:
            key = {
                "source": "sources",
                "config": "config",
                "environment": "environment",
                "native": "native_identity",
                "input": "input_identity",
            }[mutation]
            value[key] = {}
        target.write_text(json.dumps(value))
        manifest = json.loads((path / "complete.json").read_text())
        manifest["sha256"][target.name] = sha256(target)
        (path / "complete.json").write_text(json.dumps(manifest))
    with pytest.raises((ValueError, FileNotFoundError)):
        runner.verify(path)


@pytest.mark.parametrize("where", ["initialization", "after_draw", "result", "completion"])
def test_failure_durable_and_no_false_completion(tmp_path, monkeypatch, where):
    original_write = runner.write_json

    def failing_write(path, value):
        if where == "result" and path.name == "fixture__result.json":
            raise OSError("fixture write")
        return original_write(path, value)

    monkeypatch.setattr(runner, "write_json", failing_write)
    if where == "initialization":

        def fail():
            raise OSError("fixture init")

        monkeypatch.setattr(runner, "dependencies", fail)
    if where == "completion":

        def rename_fail(*args):
            raise OSError("fixture rename")

        monkeypatch.setattr(runner.os, "rename", rename_fail)

    def campaign(perform):
        def task(emit):
            emit("draw", {"counts": [3]})
            if where == "after_draw":
                raise KeyboardInterrupt("fixture interruption")
            return {"answer": 0.173}

        perform("fixture", task)

    monkeypatch.setattr(runner, "campaign", campaign)
    path = tmp_path / "fixture"
    with pytest.raises((OSError, KeyboardInterrupt)):
        runner.run(path)
    assert not (path / "complete.json").exists()
    failure = json.loads((path / "failure.json").read_text())
    assert failure["accounting_complete"] is False
    assert failure["unavailable_costs"] is None
    if where != "initialization":
        assert (path / "fixture__draw.json").exists()
    if where == "result":
        assert failure["active_stage"] == "fixture:result_persistence"
        assert failure["pending_completed_result"]["answer"] == 0.173


def test_native_version_is_enforced(monkeypatch):
    monkeypatch.setattr(runner.qiskit, "__version__", "0.45.3")
    with pytest.raises(ValueError, match="approved Terra"):
        runner.native_identity()


def test_native_source_pin_is_enforced(monkeypatch):
    monkeypatch.setattr(runner, "APPROVED_NATIVE", {})
    with pytest.raises(ValueError, match="approved Terra"):
        runner.native_identity()


def test_source_change_blocks_completion(tmp_path, monkeypatch):
    original = runner.dependencies
    calls = []

    def changing():
        calls.append(1)
        result = original()
        return result if len(calls) == 1 else {}

    monkeypatch.setattr(runner, "dependencies", changing)
    monkeypatch.setattr(runner, "campaign", simple_campaign)
    path = tmp_path / "fixture"
    with pytest.raises(ValueError, match="sources changed"):
        runner.run(path)
    assert not (path / "complete.json").exists()
