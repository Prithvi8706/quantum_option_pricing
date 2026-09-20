import pytest
from research.release_checks.inputs import input_entries, verify_inputs


def test_role_bridge_and_missing_roles():
    assert input_entries({"paths": {"p": "x"}, "sha256": {"p": "a"}}) == {"x": "a"}
    with pytest.raises(ValueError, match="role inventory"):
        input_entries({"paths": {"p": "x"}, "sha256": {}})


def test_input_scope_cannot_be_empty(tmp_path):
    with pytest.raises(ValueError, match="inventory"):
        verify_inputs(tmp_path, {}, [])
    with pytest.raises(ValueError, match="inventory"):
        verify_inputs(tmp_path, {"x": "0" * 64}, ["y"])
