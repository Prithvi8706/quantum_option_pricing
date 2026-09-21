import pytest

from research.journal_sprint.classical_baselines import estimate
from research.journal_sprint.run_comparator import validate_golden


def test_typo_rejected_before_sampling():
    with pytest.raises(ValueError, match="unknown classical method"):
        estimate({}, "rqcm", 64, ("test",))


@pytest.mark.parametrize(
    "rows",
    [
        [],
        [{"name": "golden_plain", "golden_pass": True}],
        [
            {"name": "golden_plain", "golden_pass": False},
            {"name": "golden_flagship", "golden_pass": True},
        ],
    ],
)
def test_failed_or_missing_golden_rejected(rows):
    with pytest.raises(ValueError, match="golden regression"):
        validate_golden(rows)


def test_passed_golden_accepted():
    validate_golden(
        [
            {"name": "golden_plain", "golden_pass": True},
            {"name": "golden_flagship", "golden_pass": True},
        ]
    )


@pytest.mark.parametrize("module", ["classical_baselines", "larger_resources"])
def test_runner_output_override_and_exclusive_creation(tmp_path, monkeypatch, module):
    from importlib import import_module

    runner = import_module(f"research.journal_sprint.{module}")
    destination = tmp_path / "existing"
    destination.mkdir()
    with pytest.raises(FileExistsError):
        runner.main(["--output", str(destination)])
    assert list(destination.iterdir()) == []


def test_failed_golden_never_completes(tmp_path):
    from research.journal_sprint.run_comparator import finish_accepted_run

    with pytest.raises(ValueError):
        finish_accepted_run(tmp_path, [])
    assert (tmp_path / "failure.json").is_file()
    assert not (tmp_path / "complete.json").exists()
    assert not (tmp_path / "acceptance.json").exists()


def test_readout_output_override_is_exclusive(tmp_path, monkeypatch):
    import json
    from research.journal_sprint import readout_stress

    baseline = tmp_path / "baseline"
    baseline.mkdir()
    (baseline / "complete.json").write_text(json.dumps({"sha256": {}}))
    (baseline / "summary.json").write_text(json.dumps({"rows": []}))
    output = tmp_path / "existing"
    output.mkdir()
    with pytest.raises(FileExistsError):
        readout_stress.main(["--baseline", str(baseline), "--output", str(output)])
    assert list(output.iterdir()) == []
