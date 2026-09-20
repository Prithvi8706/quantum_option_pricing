import pytest
from research.release_checks.pins import pins


def test_exact_pins():
    assert pins("# replay\nNumPy==2.0.2\ntyping_extensions==4.15.0") == {
        "numpy": "2.0.2",
        "typing-extensions": "4.15.0",
    }


@pytest.mark.parametrize(
    "text", ["", "numpy", "numpy>=2", "numpy==2.*", "a_b==1\na-b==1", "-r other.txt"]
)
def test_unpinned_or_ambiguous_requirements(text):
    with pytest.raises(ValueError):
        pins(text)
