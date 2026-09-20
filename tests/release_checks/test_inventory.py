import json
import pytest
from research.release_checks.hashes import digest
from research.release_checks.inventory import verify_archive


def test_closed_archive(tmp_path):
    names = ["planned.json", "inputs.json", "results.json"]
    for name in names:
        (tmp_path / name).write_text("{}", encoding="utf-8")
    (tmp_path / "complete.json").write_text(
        json.dumps({"sha256": {n: digest(tmp_path / n) for n in names}}), encoding="utf-8"
    )
    assert verify_archive(tmp_path) == 3
    (tmp_path / "extra").write_text("unrecorded", encoding="utf-8")
    with pytest.raises(ValueError, match="unrecorded"):
        verify_archive(tmp_path)
