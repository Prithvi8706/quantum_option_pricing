import json
import pytest
from research.journal_sprint import run_barrier_development as runner


def test_failure_is_archived_and_output_cannot_be_overwritten(tmp_path, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("injected bounded failure")
    monkeypatch.setattr(runner, "setup", fail)
    output = tmp_path/"acquisition"
    with pytest.raises(RuntimeError, match="injected"):
        runner.run(output)
    planned = json.loads((output/"planned.json").read_text())
    assert planned["config"]["confirmation"] is False
    assert planned["source_sha256"]
    assert json.loads((output/"failed.json").read_text())["type"] == "RuntimeError"
    assert not (output/"complete.json").exists()
    with pytest.raises(FileExistsError):
        runner.run(output)
