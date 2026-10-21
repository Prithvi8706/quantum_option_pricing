"""Prospective guarded divider leaf/control experiment, held for Stage C timing.

One64-bit-denominator candidate with unchanged72-bit input/output words, versus
the actual original72-bit divider. No source, price or reciprocal-method sweep.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402
import numba  # noqa: E402
import pytest  # noqa: E402

from research.limitation_program_20261001.bounded_quantile_divider import (  # noqa: E402
    leaf_spec,
)
from research.limitation_program_20261001.test_bounded_quantile_divider import (  # noqa: E402
    exact_ccx_phase_columns,
    production_fixtures,
    production_pair,
)
from research.controlled_source_completion.primitives import (  # noqa: E402
    array_gates,
    resources,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
FIXTURES = 17
CPU_LIMIT = 180
MAX_TOOL_FILES = 12288
CODE = (
    "bounded_quantile_divider.py",
    "test_bounded_quantile_divider.py",
    "experiment_quantile_divider.py",
    "quantile_divider_preflight.json",
)
INPUT_RECEIPTS = (
    "A02_quantile_central_run002",
    "A02_quantile_central_audit_run001",
    "A02_quantile_tail_run001",
    "A02_quantile_tail_audit_run001",
    "A02_quantile_transform_run002",
    "A16_dynamic_run001",
)
DEPENDENCIES = (
    "research/journal_sprint/reversible_fixed_point.py",
    "research/controlled_source_completion/primitives.py",
    "research/controlled_source_completion/exact_lookup.py",
    "research/antithetic_feasibility/reversible.py",
    "research/limitation_program_20261001/temporary_and_fulladder.py",
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def verify(frozen):
    for name, expected in frozen.items():
        assert sha(ROOT / name) == expected, ("Changed frozen dependency", name)


def bind(frozen, name, digest):
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT)
    normalized = relative(path)
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(char not in "0123456789abcdef" for char in digest)
    ):
        raise ValueError("Explicit canonical SHA256 dependency expected")
    if normalized in frozen and frozen[normalized] != digest:
        raise ValueError("Existing frozen SHA expectation conflicts: " + normalized)
    frozen[normalized] = digest


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def tool_paths():
    import _pytest
    import llvmlite

    modules = (np, numba, pytest, _pytest, llvmlite)
    directories = [Path(module.__file__).resolve().parent for module in modules]
    directories.extend(
        Path(module.__file__).resolve().parent.parent / (module.__name__ + ".libs")
        for module in (np, llvmlite)
    )
    files = set()
    for directory in directories:
        if not directory.exists():
            continue
        directory.relative_to(ROOT)
        for path in directory.rglob("*"):
            if (
                path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix.lower()
                in (
                    ".py",
                    ".pyd",
                    ".dll",
                    ".so",
                )
            ):
                files.add(path)
                if len(files) > MAX_TOOL_FILES:
                    raise ValueError("Fixed divider installed-tool inventory exceeded")
    return sorted(files)


def finish_manifest(output, checked_files=None):
    files = receipt_files(output) if checked_files is None else dict(checked_files)
    if checked_files is not None:
        files[relative(output / "summary.json")] = sha(output / "summary.json")
    create(
        output / "manifest.json",
        dict(
            files=files,
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    if output.exists():
        raise FileExistsError("Fresh divider receipt required; no same-receipt retry")
    frozen = {}
    try:
        prepare_body(output, frozen)
    except BaseException as failure:
        if output.exists():
            if not (output / "protocol.json").exists():
                create(
                    output / "protocol.json",
                    dict(
                        local_only=True,
                        frozen_inputs=frozen,
                        terminal_partial_preparation=True,
                        declared_unique_tests=FIXTURES,
                    ),
                )
            create(
                output / "preparation_failure.json",
                dict(
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    traceback=traceback.format_exc(),
                    frozen_bytes_expected_at_failure=frozen,
                    partial_files_preserved=True,
                    same_receipt_retry_allowed=False,
                ),
            )
            create(
                output / "summary.json",
                dict(
                    passed=False,
                    new_test_credit=0,
                    local_only=True,
                    preparation_failed=True,
                    budget_censored=isinstance(failure, TimeoutError),
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    fixed_receipt_terminal_no_retry=True,
                    new_financial_price_observations=0,
                    new_financial_source_replays=0,
                ),
            )
            finish_manifest(output)
        raise


def prepare_body(output, frozen):
    for name in INPUT_RECEIPTS:
        receipt = PROGRAM / name
        summary = read(receipt / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful uncensored prerequisite required: " + name)
        if name == "A02_quantile_transform_run002":
            assert summary["native_transform_certificate_succeeded"] is True
            assert summary["budget_censored"] is False
        prior = read(receipt / "manifest.json")
        for group in ("files", "frozen_inputs"):
            for path, expected in prior[group].items():
                bind(frozen, path, expected)
        bind(frozen, receipt / "manifest.json", sha(receipt / "manifest.json"))
    paths = [RESEARCH / name for name in CODE] + [ROOT / name for name in DEPENDENCIES]
    paths.append(Path(sys.executable))
    paths.extend(tool_paths())
    for path in paths:
        bind(frozen, path, sha(path))
    verify(frozen)
    transform = read(PROGRAM / "A02_quantile_transform_run002/native_transform_certificate.json")
    assert transform["certified"] is True and transform["budget_censored"] is False
    assert transform["central_denominator64"]["unsigned64_denominator_no_truncation"] is True
    tail = read(PROGRAM / "A02_quantile_tail_run001/tail_certificate.json")
    native = tail["native_interface"]
    assert native["unsigned64_denominator_no_truncation"] is True
    assert native["native_denominator_floor_at_one_guard_inactive"] is True
    output.mkdir()
    for name in CODE:
        shutil.copy2(RESEARCH / name, output / name)
        if sha(output / name) != frozen[relative(RESEARCH / name)]:
            raise ValueError("Frozen divider code snapshot differs: " + name)
    create(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_tests_gate_construction_or_costs=True,
            frozen_inputs=frozen,
            fixed_candidate=leaf_spec(72, 40, 64),
            paid_control="Original build(divide,72,40)",
            tiny_interfaces=[[3, 1, 2], [4, 2, 3]],
            declared_unique_tests=FIXTURES,
            exhaustive_tiny_clean_XOR_gate_replays=4608,
            fixed_native_fixture_pairs=8,
            dirty_output_patterns=4,
            directions=["forward", "literal inverse"],
            actual_native_leaf_replays=128,
            fixture_endpoints_are_conservative_domains_not_claimed_actual_q32_samples=True,
            CCX_phase_proof="Exact Q(omega),omega^4=-1, every8column phase1",
            process_CPU_limit_seconds=CPU_LIMIT,
            elapsed_wall_limit_seconds=600,
            new_work_admission_CPU_seconds=150,
            cleanup_CPU_reserve_seconds=30,
            numerical_threads_per_process=1,
            tool_package_inventory=["numpy", "pytest", "_pytest", "numba", "llvmlite"],
            adjacent_NumPy_LLVM_DLL_libraries_frozen=True,
            maximum_tool_files=MAX_TOOL_FILES,
            new_source_graphs_or_financial_replays=0,
            matched_compact_gate_array_ABI=True,
            repeated_declared_fixture_tests=False,
            actual_full_quantile_loader_cost=None,
            original_Box_Muller_division_sites=0,
            full_G2_or_quantum_advantage_established=False,
        ),
    )
    verify(frozen)
    print("Guarded quantile divider prospectively frozen", flush=True)


def run(output):
    started_cpu, started_wall = time.process_time(), time.monotonic()
    if (output / "summary.json").exists():
        raise FileExistsError("Divider receipt already terminal; no retry")
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    rc = pytest.main(
        [
            str(RESEARCH / "test_bounded_quantile_divider.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    xml = ET.parse(output / "tests.xml").getroot()
    cases = list(xml.iter("testcase"))
    assert rc == 0 and len(cases) == FIXTURES
    assert len({(c.attrib.get("classname"), c.attrib["name"]) for c in cases}) == FIXTURES
    assert not any(list(xml.iter(k)) for k in ("failure", "error", "skipped"))
    if time.process_time() - started_cpu >= 150 or time.monotonic() - started_wall >= 600:
        raise TimeoutError("Fixed divider150CPU work-admission or600wall budget exceeded")
    candidate, registers, control, args, outs = production_pair()
    saved = []
    for name, program, inputs, outputs, spec in (
        (
            "candidate64",
            candidate,
            [registers["numerator"], registers["denominator"]],
            [registers["output"]],
            leaf_spec(72, 40, 64),
        ),
        ("original72", control, args, outs, dict(op="divide", width=72, fraction_bits=40)),
    ):
        gates = array_gates(program)
        assert gates.dtype == np.dtype("int32") and gates.shape[1] == 4
        path = output / (name + ".npy")
        np.save(path, gates, allow_pickle=False)
        actual = np.load(path, allow_pickle=False)
        assert np.array_equal(actual, gates)
        counts = {kind: int(np.count_nonzero(actual[:, 0] == kind)) for kind in (1, 2, 3)}
        assert sum(counts.values()) == len(gates)
        ledger = resources(program)
        assert (ledger["x"], ledger["cx"], ledger["ccx"]) == tuple(counts[k] for k in (1, 2, 3))
        assert ledger["t_count"] == 7 * counts[3]
        saved.append(
            dict(
                name=name,
                input_registers=[list(r) for r in inputs],
                output_registers=[list(r) for r in outputs],
                spec=spec,
                qubits=program.qubits,
                actual_gate_file=relative(path),
                actual_gate_sha256=sha(path),
                resources=ledger,
                all_native_replays_already_checked_once_in_fixed_pytest_case=True,
            )
        )
    create(output / "leaf_ledgers.json", saved)
    create(output / "fixed_native_fixture_pairs.json", production_fixtures())
    create(output / "exact_CCX_phase_proof.json", exact_ccx_phase_columns())
    verify(protocol["frozen_inputs"])
    checked_files = receipt_files(output)
    cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
    if cpu >= CPU_LIMIT or wall >= 600:
        raise TimeoutError("Fixed divider180CPU or600wall terminal budget exceeded")
    create(
        output / "summary.json",
        dict(
            passed=True,
            budget_censored=False,
            local_only=True,
            distinct_pytest_cases=FIXTURES,
            exhaustive_tiny_gate_replays=4608,
            actual_native_leaf_gate_replays=128,
            exact_seven_T_primitive_phase_proved=True,
            candidate=saved[0]["resources"],
            paid_control=saved[1]["resources"],
            actual_saved_gate_arrays=2,
            native_argument_guard_from_both_AS241_branches_bound=True,
            current_Box_Muller_source_changed=False,
            actual_quantile_graph_or_loader_adopted=False,
            new_financial_price_observations=0,
            new_financial_source_replays=0,
            full_G2_or_quantum_advantage_established=False,
            CPU_seconds=cpu,
            wall_seconds=wall,
        ),
    )
    return checked_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.mode == "prepare":
        prepare(output)
        return
    output.relative_to(PROGRAM)
    if (output / "summary.json").exists():
        raise FileExistsError("Divider receipt is terminal; retry may not mutate it")
    checked_files = None
    try:
        checked_files = run(output)
    except BaseException as failure:
        create(
            output / "failure.json",
            dict(
                passed=False,
                traceback=traceback.format_exc(),
                failure_type=type(failure).__name__,
                message=str(failure),
                budget_censored=isinstance(failure, TimeoutError),
                partial_files_preserved=True,
                same_receipt_retry_allowed=False,
            ),
        )
        if not (output / "summary.json").exists():
            create(
                output / "summary.json",
                dict(
                    passed=False,
                    new_test_credit=0,
                    local_only=True,
                    budget_censored=isinstance(failure, TimeoutError),
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    fixed_receipt_terminal_no_retry=True,
                    new_financial_price_observations=0,
                    new_financial_source_replays=0,
                ),
            )
        raise
    finally:
        finish_manifest(output, checked_files)
    print("Guarded quantile divider and actual control passed", flush=True)


if __name__ == "__main__":
    main()
