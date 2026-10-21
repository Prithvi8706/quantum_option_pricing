"""Freeze exactly two elementary RMSE confidence conversions at the current budget."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil

import pytest

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT
from research.limitation_program_20261001.rmse_confidence import conversions


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    output.mkdir()
    directory = PROGRAM / "E07_schedule_run001"
    receipt = read(directory / "manifest.json")
    frozen = {**receipt["files"], **receipt["frozen_inputs"]}
    frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in ("rmse_confidence.py", "test_rmse_confidence.py", "experiment_rmse_confidence.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
        shutil.copy2(path, output / name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_tests_and_two_conversions=True,
        statistical_error_dollars_exact=[9, 2000],
        failure_exact=[3, 1000],
        families=["one-run squared-error Markov", "independent odd median"],
        finite_odd_repetition_cap=101,
        new_financial_prices_or_gates=0,
        RMSE_construction_or_query_cost_provided=False,
        stop_rule=(
            "Two elementary conversions only; absent E20 schedules/costs "
            "remain named prerequisites"
        ),
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_rmse_confidence.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen confidence-conversion fixtures failed")
    certificate = conversions(max_repetitions=protocol["finite_odd_repetition_cap"])
    save(output / "certificate.json", certificate)
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            conversion_families=2,
            median_repetitions=certificate["independent_median"]["repetitions"],
            median_failure_upper_exact=certificate["independent_median"][
                "certified_failure_upper_exact"
            ],
            actual_E20_finite_RMSE_constructions_supplied=0,
            complete_cost_winner_selected=False,
            new_financial_prices_or_gates=0,
            full_price_confidence_certified=False,
        ),
    )
    manifest(output, protocol)
    print(
        "Two exact RMSE confidence conversions retained; no unsupported cost promotion", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
