from pathlib import Path
import pytest
from research.release_checks.claims import pointer, verify_claims
from research.release_checks.json_io import read


def test_live_claim_register():
    root = Path(__file__).resolve().parents[2]
    assert verify_claims(root, read(root / "docs/release/claims.json"))["claims_checked"] == 4


def test_pointer_escaping_and_bad_indices():
    assert pointer({"a/b": {"~": [7]}}, "/a~1b/~0/0") == 7
    for value in ["/01", "/-1", "/~2"]:
        with pytest.raises(ValueError):
            pointer([1, 2], value)
