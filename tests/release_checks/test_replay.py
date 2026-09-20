import json
import pytest
from research.release_checks.replay import compare_replay


def test_replay_rejects_boolean_integer_alias(tmp_path):
    paths = [tmp_path / "a", tmp_path / "b"]
    for path in paths:
        path.mkdir()
        for name in ("results.json", "inputs.json"):
            (path / name).write_text('{"value":false}', encoding="utf-8")
        (path / "complete.json").write_text(
            json.dumps({"sha256": {"results.json": "unused", "inputs.json": "unused"}}),
            encoding="utf-8",
        )
    assert compare_replay(*paths)["exact_bytes"]
    (paths[1] / "results.json").write_text('{"value":0}', encoding="utf-8")
    with pytest.raises(ValueError, match="differs"):
        compare_replay(*paths)
