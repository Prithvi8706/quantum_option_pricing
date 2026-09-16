"""Isolated tiny archive fixtures; never acquire the week13 study in tests."""

import json

import pytest

from research.journal_sprint import run_w13 as runner
from research.journal_sprint.storage import sha256
from scripts.verify_week13_independent import audit


@pytest.fixture(autouse=True)
def isolated(monkeypatch):
    monkeypatch.setattr(runner, "CASES", ((1, 2, 1),))
    monkeypatch.setattr(runner, "NAMESPACE", "TEST_ONLY_week13_archive_fixture")
    monkeypatch.setattr(runner, "STRIKE", 71.0)
    monkeypatch.setattr(runner, "POWER", 3)
    monkeypatch.setattr(runner, "SCRAMBLES", 2)


def test_archive_replay_and_exclusive_output(tmp_path):
    path = tmp_path / "fixture"
    assert runner.run(path)["circuits"] == 4
    assert runner.verify(path)["numerical_replay"] is True
    assert audit(path)["audited_cases"] == 1
    with pytest.raises(FileExistsError):
        runner.run(path)


@pytest.mark.parametrize("mutation", ["missing", "extra", "checksum", "identity", "result"])
def test_tamper_rejected_even_with_rehashed_manifest(tmp_path, mutation):
    path = tmp_path / "fixture"
    runner.run(path)
    manifest_path = path / "complete.json"
    manifest = json.loads(manifest_path.read_text())
    if mutation == "missing":
        (path / "finished_0.json").unlink()
    elif mutation == "extra":
        (path / "extra.json").write_text("{}")
    else:
        target = path / ("source_identity.json" if mutation == "identity" else "case_0.json")
        row = json.loads(target.read_text())
        if mutation == "identity":
            row = {}
        else:
            row["rows"][0]["expectation"] += .3
        target.write_text(json.dumps(row))
        if mutation != "checksum":
            manifest["sha256"][target.name] = sha256(target)
            manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        runner.verify(path)


def test_failure_retained_not_completed(tmp_path, monkeypatch):
    def fail(*args):
        raise ArithmeticError("fixture injected failure")
    monkeypatch.setattr(runner, "execute_case", fail)
    path = tmp_path / "fixture"
    with pytest.raises(ArithmeticError, match="injected"):
        runner.run(path)
    assert (path / "started_0.json").exists()
    assert (path / "failure.json").exists()
    assert not (path / "complete.json").exists()
    with pytest.raises(ValueError):
        runner.verify(path)


@pytest.mark.parametrize("value", [-1, float("nan"), True, "1"])
def test_bad_timing_rejected(value):
    with pytest.raises(ValueError):
        runner.equivalent({"seconds": value}, {"seconds": 1.0})


@pytest.mark.parametrize("mutation", ["environment_null", "version", "sources",
                                      "timestamp", "git", "threads"])
def test_provenance_tamper_rejected(tmp_path, mutation):
    path = tmp_path / "fixture"
    runner.run(path)
    target = path / ("environment.json" if mutation == "environment_null" else "planned.json")
    value = json.loads(target.read_text())
    if mutation == "environment_null":
        value = None
    elif mutation == "version":
        value["environment"]["python"] = "invented"
    elif mutation == "sources":
        value["source_sha256"] = {}
    elif mutation == "timestamp":
        value["started_utc"] = "not a timestamp"
    elif mutation == "git":
        value["git_head"] = "oops"
    else:
        value["environment"]["threads"] = {}
    target.write_text(json.dumps(value))
    manifest = json.loads((path / "complete.json").read_text())
    manifest["sha256"][target.name] = sha256(target)
    (path / "complete.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        runner.verify(path)


def test_initialization_failure_is_recorded(tmp_path, monkeypatch):
    def fail(*args):
        raise OSError("fixture initialization")
    monkeypatch.setattr(runner, "sha256", fail)
    path = tmp_path / "fixture"
    with pytest.raises(OSError):
        runner.run(path)
    failure = json.loads((path / "failure.json").read_text())
    assert failure["active_stage"] == "initialization"
    assert failure["accounting_complete"] is False


@pytest.mark.parametrize("exception", [RuntimeError, KeyboardInterrupt])
def test_completed_stage_survives_later_failure(tmp_path, monkeypatch, exception):
    original = runner.measure
    calls = []
    def fail_second(*args):
        calls.append(1)
        if len(calls) == 2:
            raise exception("fixture second loader")
        return original(*args)
    monkeypatch.setattr(runner, "measure", fail_second)
    path = tmp_path / "fixture"
    with pytest.raises(exception):
        runner.run(path)
    assert (path / "stage_0_reference_finished.json").exists()
    first = json.loads((path / "stage_0_raw_product_finished.json").read_text())["value"]
    assert first["acquisition"]["cx"] >= 0
    assert first["compile_and_statevector_seconds"] > 0
    failure = json.loads((path / "failure.json").read_text())
    assert failure["active_stage"] == "case_0:raw_dense"
    assert failure["failed_stage_seconds"] >= 0
    assert failure["unavailable_counts"] is None
    assert not (path / "complete.json").exists()


def test_atomic_completion_failure(tmp_path, monkeypatch):
    def fail(*args):
        raise OSError("fixture atomic rename")
    monkeypatch.setattr(runner.os, "rename", fail)
    path = tmp_path / "fixture"
    with pytest.raises(OSError):
        runner.run(path)
    assert (path / "complete.pending.json").exists()
    assert (path / "failure.json").exists()
    assert not (path / "complete.json").exists()


@pytest.mark.parametrize("stage", ["result", "reconstruction", "checkpoint"])
def test_failure_stage_is_not_completed_acquisition(tmp_path, monkeypatch, stage):
    original_write = runner.write_json
    def fail_write(path, value):
        names = {"result": "case_0.json", "checkpoint": "stage_0_raw_product_finished.json"}
        if path.name == names.get(stage):
            raise OSError("fixture persistence")
        return original_write(path, value)
    monkeypatch.setattr(runner, "write_json", fail_write)
    if stage == "reconstruction":
        def fail_contract(*args):
            raise OSError("fixture reconstruction")
        monkeypatch.setattr(runner, "price_contract", fail_contract)
    path = tmp_path / "fixture"
    with pytest.raises(OSError):
        runner.run(path)
    failure = json.loads((path / "failure.json").read_text())
    expected = {"result": "case_0:result_persistence", "reconstruction": "case_0:reconstruction",
                "checkpoint": "case_0:raw_product:checkpoint_finished"}
    assert failure["active_stage"] == expected[stage]
    if stage == "checkpoint":
        assert failure["pending_completed_result"]["loader"] == "product"
    else:
        assert failure["pending_completed_result"] is None


@pytest.mark.parametrize("mutation", ["rows", "circuits", "normals", "factor", "nan",
                                      "fidelity", "inverse", "extra_row"])
def test_independent_audit_rejects_vacuous_or_invalid_checks(tmp_path, mutation):
    path = tmp_path / "fixture"
    runner.run(path)
    target = path / "case_0.json"
    row = json.loads(target.read_text())
    if mutation == "rows":
        row["rows"] = []
    elif mutation == "circuits":
        row["rows"][0]["circuits"] = []
    elif mutation == "normals":
        row["normals"] = [[] for _ in row["normals"]]
    elif mutation == "factor":
        row["factor"] = [[] for _ in row["factor"]]
    elif mutation == "extra_row":
        row["rows"].append(row["rows"][0])
    else:
        key = {"nan": "max_joint_probability_error", "fidelity": "state_fidelity_error",
               "inverse": "inverse_return_error"}[mutation]
        row["rows"][0]["circuits"][0][key] = float("nan") if mutation == "nan" else .1
    target.write_text(json.dumps(row))
    with pytest.raises(ValueError):
        audit(path)
