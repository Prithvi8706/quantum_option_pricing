"""Small deterministic audit fixtures; no confirmation observations."""

import json

import pytest

from research.journal_sprint import run_encoding_enclosure as runner
from research.journal_sprint.storage import sha256


@pytest.fixture(autouse=True)
def fixture_config(monkeypatch):
    monkeypatch.setattr(
        runner, "CONFIG", dict(runner.CONFIG, cases=[3], cutoffs=[3], precisions=[1, 2])
    )
    monkeypatch.setattr(runner, "SOURCES", ["research/journal_sprint/run_encoding_enclosure.py"])


def test_fixture_replay_and_ownership(tmp_path):
    output = tmp_path / "output"
    assert runner.run(output)["rows"] == 4
    assert runner.verify(output)["rows"] == 4
    with pytest.raises(FileExistsError):
        runner.run(output)
    assert not (output / "failure.json").exists()


@pytest.mark.parametrize("mutation", ["nested_complete", "changed_row", "git", "time", "extra"])
def test_tampering_rejected(tmp_path, mutation):
    runner.run(tmp_path / "out")
    output = tmp_path / "out"
    manifest = json.loads((output / "complete.json").read_text())
    if mutation == "nested_complete":
        (output / "unexpected").mkdir()
        (output / "unexpected/complete.json").write_text("{}")
    else:
        filename = "case_3_cutoff_3.json" if mutation == "changed_row" else "planned.json"
        value = json.loads((output / filename).read_text())
        if mutation == "changed_row":
            value["rows"][0]["partial_sum"]["upper"] = "0"
        elif mutation == "git":
            value["git_head"] = "invalid"
        elif mutation == "time":
            value["started_utc"] = "2999-01-01T00:00:00+00:00"
        else:
            value["unconsumed"] = True
        (output / filename).write_text(json.dumps(value))
        manifest["sha256"][filename] = sha256(output / filename)
        (output / "complete.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        runner.verify(output)


def test_failure_persisted(tmp_path, monkeypatch):
    def fail(*args):
        raise ArithmeticError("fixture calculation failure")

    monkeypatch.setattr(runner, "calculate", fail)
    with pytest.raises(ArithmeticError):
        runner.run(tmp_path / "out")
    assert (tmp_path / "out/failure.json").exists()
    assert not (tmp_path / "out/complete.json").exists()


def test_source_change_fails_before_completion(tmp_path, monkeypatch):
    original = runner.source_identity()
    calls = iter([original, {k: "changed" for k in original}])
    monkeypatch.setattr(runner, "source_identity", lambda: next(calls))
    with pytest.raises(ValueError, match="changed"):
        runner.run(tmp_path / "out")
    assert (tmp_path / "out/failure.json").exists()
    assert not (tmp_path / "out/complete.json").exists()
