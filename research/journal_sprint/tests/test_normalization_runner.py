import json
import pytest
from research.journal_sprint import run_normalization_approximation as runner


def test_exclusive_output_and_failure_marker(tmp_path, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("injected model failure")
    monkeypatch.setattr(runner, "setup", fail)
    output = tmp_path/"study"
    with pytest.raises(RuntimeError, match="injected"):
        runner.run(output)
    assert json.loads((output/"failed.json").read_text())["type"] == "RuntimeError"
    assert not (output/"complete.json").exists()
    with pytest.raises(FileExistsError):
        runner.run(output)


def test_unsupported_control_config_rejected_before_creation(tmp_path, monkeypatch):
    monkeypatch.setitem(runner.CONFIG, "low", 6)
    with pytest.raises(ValueError):
        runner.run(tmp_path/"bad")
    assert not (tmp_path/"bad").exists()
