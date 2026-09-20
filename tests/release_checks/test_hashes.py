import pytest
from research.release_checks.hashes import digest, verify_hashes


def test_byte_exact_and_tamper(tmp_path):
    path = tmp_path / "a"
    path.write_bytes(b"a\r\n")
    expected = digest(path)
    assert verify_hashes(tmp_path, {"a": expected}) == 1
    path.write_bytes(b"a\n")
    with pytest.raises(ValueError, match="mismatch"):
        verify_hashes(tmp_path, {"a": expected})


@pytest.mark.parametrize("entries", [{}, {"a": "bad"}, {"a": None}])
def test_invalid_inventory(tmp_path, entries):
    with pytest.raises(ValueError):
        verify_hashes(tmp_path, entries)
