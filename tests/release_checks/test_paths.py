import pytest
from research.release_checks.paths import normalized, within


@pytest.mark.parametrize(
    "name",
    [
        "../x",
        "/x",
        "C:/x",
        "a//b",
        "./a",
        "a/../b",
        "",
        "CON",
        "aux.txt",
        "a/NUL",
        "COM1",
        "a.",
        "a ",
    ],
)
def test_reject_unsafe_names(tmp_path, name):
    with pytest.raises(ValueError):
        within(tmp_path, name)


def test_windows_paths_and_aliases(tmp_path):
    assert within(tmp_path, "a\\b") == tmp_path / "a" / "b"
    with pytest.raises(ValueError, match="duplicate"):
        normalized({"a/b": 1, "a\\b": 2})
    with pytest.raises(ValueError, match="duplicate"):
        normalized({"a/b": 1, "A/B": 2})
