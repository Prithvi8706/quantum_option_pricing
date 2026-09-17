import json
import pytest
from research.journal_sprint import run_arithmetic_development as runner


def test_failure_is_preserved_and_output_is_exclusive(tmp_path, monkeypatch):
    def fail(*args):
        raise ArithmeticError("injected loader failure")
    monkeypatch.setattr(runner, "loader_plan", fail)
    output = tmp_path/"audit"
    with pytest.raises(ArithmeticError, match="injected"):
        runner.run(output)
    assert (output/"planned.json").exists()
    assert (output/"arithmetic_plan.json").exists()
    assert not (output/"complete.json").exists()
    assert json.loads((output/"failed.json").read_text())["type"] == "ArithmeticError"
    before = (output/"failed.json").read_bytes()
    with pytest.raises(FileExistsError):
        runner.run(output)
    assert (output/"failed.json").read_bytes() == before
