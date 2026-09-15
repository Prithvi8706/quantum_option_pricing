import mpmath as mp
import pytest
import json

from research.journal_sprint import numerical_reference as nr
from research.journal_sprint.week10_stress import cases, compare, interval
from research.journal_sprint.verify_week10 import verify


def test_matrix():
    assert len(cases()) == 80
    assert len(cases(True)) == 83
    assert len({r["case_id"] for r in cases(True)}) == 83


@pytest.mark.parametrize("n", [1, 64, 128])
def test_boundary_identity(n):
    with mp.workdps(80):
        for k in (0, n):
            assert max(
                abs(a - b)
                for a, b in zip(interval(k, n, mp.mpf(".025")), nr.cp(k, n, mp.mpf(".025")))
            ) < mp.mpf("1e-45")


def test_reject_large_interior():
    with pytest.raises(ValueError):
        interval(50000, 100000, mp.mpf(".025"))


@pytest.mark.parametrize("row", cases(True)[-3:])
def test_disconnected_intersection(row):
    result = compare(row)
    assert result["encloses"] and result["stable"]
    assert len(result["reference"]) > 1


def test_verifier_rejects_unlisted_file(tmp_path):
    (tmp_path / "complete.json").write_text(json.dumps({"sha256": {}}))
    (tmp_path / "unexpected.txt").write_text("unlisted")
    with pytest.raises(ValueError, match="inventory"):
        verify(tmp_path)


def test_verifier_rejects_hash_tampering(tmp_path):
    (tmp_path / "complete.json").write_text(json.dumps({"sha256": {"data.json": "bad"}}))
    (tmp_path / "data.json").write_text("{}")
    with pytest.raises(ValueError, match="hash"):
        verify(tmp_path)
