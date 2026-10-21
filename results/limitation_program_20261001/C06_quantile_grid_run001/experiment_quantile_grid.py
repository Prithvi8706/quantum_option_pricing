"""Freeze a different-law ideal scalar Gaussian quantile-grid certificate."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil

import pytest

from research.limitation_program_20261001.barrier_band_certificate import original_model
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
from research.limitation_program_20261001.quantile_grid_certificate import law_bound


CODE = (
    "experiment_quantile_grid.py",
    "quantile_grid_certificate.py",
    "test_quantile_grid_certificate.py",
)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    screen = PROGRAM / "C07_composition_screen_run001"
    assert read(screen / "summary.json")["passed"]
    assert not read(screen / "summary.json")["optimistic_uniform_composition_can_fit"]
    output.mkdir()
    receipt = read(screen / "manifest.json")
    frozen = {**receipt["files"], **receipt["frozen_inputs"]}
    frozen[relative(screen / "manifest.json")] = digest(screen / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
        shutil.copy2(path, output / name)
    builder = Path(original_model()["builder_path"])
    frozen[relative(builder)] = digest(builder)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_tests_and_ideal_law_certificate_evaluation=True,
        cases=["B4x12", "B8x52"],
        uniform_bits=32,
        ideal_loader="independent exact scalar normal inverse-CDF midpoints",
        original_source_law_changed_if_implemented=True,
        source_graph_modified=False,
        candidate_precisions=1,
        alternative_ideal_laws=1,
        toy_fixture=(
            "Approximate90-digit one-asset one-date Gaussian knockout closed "
            "expectation, q4/q8; fixture only, analytic BV proof is the certificate"
        ),
        original_B4_B8_price_observations_or_gate_replays=0,
        acceptance=(
            "Prove uniform coordinate variation and product midpoint quadrature "
            "error at exact original financial parameters; keep the actual "
            "Box-Muller/native/coherent-implementation obligations explicit"
        ),
        stop_rule=(
            "One q32 ideal law, both contract dimensions. No loader adoption or "
            "precision sweep without independent proof and charged arithmetic/circuit costs"
        ),
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_quantile_grid_certificate.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", dict(passed=False, return_code=int(rc)))
        manifest(output, protocol)
        raise AssertionError("Frozen ideal quantile-grid theorem fixtures failed")
    rows = []
    for case in protocol["cases"]:
        model = original_model(case)
        assert digest(Path(model["builder_path"])) == model["builder_sha256"]
        row = law_bound(model, protocol["uniform_bits"])
        row["original_model_binding"] = model
        save(output / (case + "_certificate.json"), row)
        rows.append({key: value for key, value in row.items() if key != "proof"})
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=rows,
            alternative_ideal_law_grid_bias_certificate=True,
            accepted_Box_Muller_full_price_certificate=False,
            coherent_inverse_CDF_loader_implemented=False,
            native_financial_arithmetic_price_bound=None,
            full_G2_closed=False,
            source_graph_changed=False,
            original_B4_B8_price_observations_or_gate_replays=0,
            quantum_advantage_established=False,
            next_required=(
                "Bind a rigorously rounded normal quantile implementation to this "
                "different law, propagate native arithmetic through the barrier, "
                "then price its reversible implementation before adoption"
            ),
        ),
    )
    manifest(output, protocol)
    print(
        "Conditional ideal quantile-grid law certificate retained; loader not adopted", flush=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
