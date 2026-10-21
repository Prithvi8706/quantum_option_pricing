"""Prospective single scalar AS241 graph and matched generic-divider control."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import pytest  # noqa: E402

from research.controlled_source_completion.compiler import execute  # noqa: E402
from research.controlled_source_completion.ir import evaluate  # noqa: E402
from research.limitation_program_20261001.experiment_checkpoint import (  # noqa: E402
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.scalar_quantile_ir import (  # noqa: E402
    ROOT,
    PROGRAM,
    FIXTURE_WORDS,
    MASK,
    K_CENTRAL,
    load_literals,
    build_scalar_graph,
    bind_site_proofs,
    read,
)
from research.limitation_program_20261001.scalar_quantile_source import (  # noqa: E402
    DIVIDER,
    SQRT,
    compile_scalar_source,
    digest,
)


CODE = (
    "scalar_quantile_ir.py",
    "scalar_quantile_source.py",
    "test_scalar_quantile_ir.py",
    "experiment_scalar_quantile_ir.py",
    "AS241_SCALAR_IR_PREFLIGHT.md",
)
RECEIPTS = (
    "A02_quantile_central_run002",
    "A02_quantile_central_audit_run001",
    "A02_quantile_tail_run001",
    "A02_quantile_tail_audit_run001",
    "A02_quantile_transform_run002",
    "A02_quantile_transform_audit_run001",
    "A02_quantile_law_run001",
    "A02_quantile_law_audit_run001",
    "A17_quantile_divider_run001",
)
DEPENDENCIES = (
    "research/controlled_source_completion/ir.py",
    "research/controlled_source_completion/compiler.py",
    "research/controlled_source_completion/primitives.py",
    "research/controlled_source_completion/exact_lookup.py",
    "research/journal_sprint/reversible_fixed_point.py",
    "research/antithetic_feasibility/reversible.py",
    "research/limitation_program_20261001/bounded_quantile_divider.py",
    "research/limitation_program_20261001/temporary_and_fulladder.py",
    "research/limitation_program_20261001/experiment_checkpoint.py",
    "research/limitation_program_20261001/scalar_quantile_ir.py",
)
DECLARED_TESTS = 27
CPU_LIMIT = 300
WALL_LIMIT = 600
ADMISSION_CPU = 240
DIRTY = (0, MASK)


def bind(frozen, name, expected):
    path = Path(str(name).replace("\\", "/"))
    path = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    normalized = relative(path)
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Explicit prerequisite SHA256 required")
    if normalized in frozen and frozen[normalized] != expected:
        raise ValueError("Historical prerequisite bytes conflict: " + normalized)
    frozen[normalized] = expected


def receipt_files(output):
    return {
        relative(path): digest(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def finish_manifest(output, protocol, files=None):
    if files is None:
        files = receipt_files(output)
    else:
        files = dict(files)
        files[relative(output / "summary.json")] = digest(output / "summary.json")
    save(
        output / "manifest.json",
        {
            "files": files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh scalar-IR prospective receipt required")
    frozen = {}
    for name in RECEIPTS:
        directory = PROGRAM / name
        summary = read(directory / "summary.json")
        if summary.get("passed") is not True or summary.get("budget_censored", False) is not False:
            raise ValueError("Successful prerequisite receipt required: " + name)
        if name == "A02_quantile_transform_run002" and (
            summary.get("native_transform_certificate_succeeded") is not True
            or summary.get("budget_censored") is not False
        ):
            raise ValueError("Uncensored successful native transform required")
        if (
            name == "A02_quantile_law_run001"
            and summary.get("different_AS241_scalar_law_ideal_GBM_bias_certificate") is not True
        ):
            raise ValueError("New law transfer prerequisite required")
        receipt = read(directory / "manifest.json")
        if (
            not {"files", "frozen_inputs"}.issubset(receipt)
            or not set(receipt).issubset({"files", "frozen_inputs", "manifest_self_hash_excluded"})
            or receipt.get("manifest_self_hash_excluded", True) is not True
        ):
            raise ValueError("Explicit prerequisite manifest schema required")
        for field in ("files", "frozen_inputs"):
            for path, expected in receipt[field].items():
                bind(frozen, path, expected)
        bind(frozen, directory / "manifest.json", digest(directory / "manifest.json"))
    for path in [ROOT / "research/limitation_program_20261001" / name for name in CODE] + [
        ROOT / name for name in DEPENDENCIES
    ]:
        bind(frozen, path, digest(path))
    bind(frozen, Path(sys.executable), digest(Path(sys.executable)))
    native_sqrt = read(SQRT)
    for path in (SQRT, SQRT.parent / native_sqrt["gate_file"]):
        bind(frozen, path, digest(path))
    verify({"frozen_inputs": frozen})
    output.mkdir()
    try:
        prepare_receipt(output, frozen)
    except BaseException as failure:
        save(
            output / "preparation_failure.json",
            {"failure": traceback.format_exc(), "partial_files_preserved": True},
        )
        save(
            output / "summary.json",
            {
                "passed": False,
                "preparation_failed": True,
                "budget_censored": isinstance(failure, TimeoutError),
                "new_financial_prices_or_replays": 0,
            },
        )
        finish_manifest(output, {"frozen_inputs": frozen})
        raise


def prepare_receipt(output, frozen):
    for name in CODE:
        source = ROOT / "research/limitation_program_20261001" / name
        destination = output / name
        shutil.copy2(source, destination)
        if digest(destination) != frozen[relative(source)]:
            raise ValueError("Scalar snapshot differs from frozen source bytes")
        bind(frozen, destination, frozen[relative(source)])
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_graph_construction_word_evaluation_leaf_generation_or_costs": True,
        "scalar_graphs": 1,
        "uniform_input_bits": 32,
        "native_width": 72,
        "fraction_bits": 40,
        "named_output": "Z72 dirty full-word XOR",
        "fixed_optimizer": "none",
        "compiler": "serial full-native SSA with distinct paid argument-copy slots",
        "central_floor_order": (
            "positive floor(qguard*Acentral/S), then unsigned division, exact sign restore"
        ),
        "shared_divide_count": 1,
        "eager_unused_branch_guards": (
            "min(qabs,Q_CENTRAL),min(p,P_TAIL), paid exact actualq32 boundary words"
        ),
        "coefficient_and_log_table_policy": (
            "Frozen raw literals and archived table only; no float APIs/regeneration"
        ),
        "candidate": (
            "one scalar source using actual denominator64 divider and archived unsigned46 sqrt"
        ),
        "paid_control": (
            "same exact graph/sqrt/all other gate bytes, actual original genericdivide72"
        ),
        "native_divider_receipt": relative(DIVIDER),
        "new_site_typed_admission": (
            "Full exact graph recipe + trusted complete proof inputs before any native copy"
        ),
        "guard_proof_q32_completeness": (
            "Structural/all-input arithmetic proofs; fixed vectors are diagnostics only"
        ),
        "declared_unique_tests": DECLARED_TESTS,
        "fixed_semantic_fixture_raw_words": list(FIXTURE_WORDS),
        "candidate_actual_gate_replay_raw_words": list(FIXTURE_WORDS),
        "dirty_output_patterns": list(DIRTY),
        "candidate_actual_clean_XOR_gate_replays": 16,
        "control_actual_gate_replay_raw_words": [K_CENTRAL],
        "control_actual_clean_XOR_gate_replays": 2,
        "full_wrapper_inverse": "F then outputCX then literal F^-1 is its own literal inverse",
        "resource_count": (
            "Scan saved native arrays/literal reverses; full copies/output72/native scratch paid"
        ),
        "initial_Hadamards": 32,
        "initial_Hadamards_separate_from_arithmetic_leaf_counts": True,
        "process_CPU_limit_seconds": CPU_LIMIT,
        "mandatory_successful_prerequisite_receipts": list(RECEIPTS),
        "interpreter_and_every_frozen_insertion_preserve_historical_expectations": True,
        "bulk_output_hashing_and_verification_before_terminal_CPU_wall_check": True,
        "elapsed_wall_limit_seconds": WALL_LIMIT,
        "new_work_admission_CPU_seconds": ADMISSION_CPU,
        "numerical_threads_per_process": 1,
        "new_financial_source_graphs_prices_or_replays": 0,
        "full_B4_B8_source_or_financial_sampler_adoption": False,
        "native_financial_path_error_certified": False,
        "quantum_advantage_established": False,
        "adaptive_method_cost_or_fixture_retry": False,
        "preexisting_Stage_C_jobs_edited": False,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    verify(protocol)
    print("One scalar graph and one generic-divider cost control prospectively frozen", flush=True)


def _credit(path):
    cases = list(ET.parse(path).getroot().iter("testcase"))
    identities = [(case.attrib.get("classname", ""), case.attrib["name"]) for case in cases]
    if len(cases) != DECLARED_TESTS or len(set(identities)) != DECLARED_TESTS:
        raise AssertionError("Declared distinct scalar fixture count differs")
    if any(case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")):
        raise AssertionError("Scalar fixture failure/error/skip cannot receive credit")
    return {
        "unique_new_fixtures_passed": len(set(identities)),
        "prior_fixture_counts_added_again": 0,
        "test_identities": [list(item) for item in identities],
    }


def _replay(source, target, raw, dirty):
    _, values = evaluate(target, {"k": raw}, trace=True)
    expected = dirty ^ values[target["outputs"]["Z"]]
    result = execute(source, {"k": raw}, initial_outputs={"Z": dirty})
    if (
        result["values"]["Z"] != expected
        or not result["workspace_clean"]
        or not result["inputs_preserved"]
    ):
        raise AssertionError("Actual full scalar native gates violate XOR/input/cleanup contract")
    return {
        "q32_raw": raw,
        "initial_output72": dirty,
        "expected_XOR_output72": expected,
        "observed_output72": result["values"]["Z"],
        "all_work_and_native_scratch_clean": True,
        "full_native_input72_preserved": True,
        "allocated_state_qubits": source["resources"]["logical_qubits"],
        "actual_gate_replay": True,
        "all_input_law_completeness_inferred_from_this_fixture": False,
    }


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Scalar source receipt is already terminal")
    protocol = read(output / "protocol.json")
    started_cpu, started_wall = time.process_time(), time.monotonic()
    files = None

    def admit():
        if (
            time.process_time() - started_cpu >= ADMISSION_CPU
            or time.monotonic() - started_wall >= WALL_LIMIT
        ):
            raise TimeoutError(
                "Fixed scalar work-admission budget reached; no added candidate/retry"
            )

    try:
        verify(protocol)
        rc = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_scalar_quantile_ir.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        if rc:
            raise AssertionError("Frozen scalar arithmetic/guard fixtures failed: " + str(int(rc)))
        save(output / "test_credit_reconciliation.json", _credit(output / "tests.xml"))
        admit()
        literals = load_literals()
        target, bindings = build_scalar_graph(literals)
        proof_inputs = {
            "central": read(PROGRAM / "A02_quantile_central_run002/central_certificate.json"),
            "tail": read(PROGRAM / "A02_quantile_tail_run001/tail_certificate.json"),
            "transform": read(
                PROGRAM / "A02_quantile_transform_run002/native_transform_certificate.json"
            ),
        }
        proofs = bind_site_proofs(target, bindings, literals, **proof_inputs)
        save(output / "literals.json", literals)
        save(output / "scalar_target.json", target)
        save(output / "semantic_bindings.json", bindings)
        save(output / "new_site_proofs.json", proofs)
        admit()
        candidate, candidate_ledger = compile_scalar_source(
            target,
            bindings,
            literals,
            proofs,
            proof_inputs,
            output / "candidate64",
        )
        save(output / "candidate64_actual_cost.json", candidate_ledger)
        admit()
        control, control_ledger = compile_scalar_source(
            target,
            bindings,
            literals,
            proofs,
            proof_inputs,
            output / "control72",
            divider_mode="original72",
            reuse_directory=output / "candidate64",
        )
        save(output / "control72_actual_cost.json", control_ledger)
        records = []
        for label, source, words in (
            ("candidate64", candidate, FIXTURE_WORDS),
            ("control72", control, (K_CENTRAL,)),
        ):
            for raw in words:
                for dirty in DIRTY:
                    admit()
                    row = {"source": label, **_replay(source, target, raw, dirty)}
                    records.append(row)
                    save(
                        output / "actual_gate_replays.json",
                        {"completed_replays": len(records), "rows": records},
                    )
        verify(protocol)
        files = receipt_files(output)
        cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
        censored = cpu > CPU_LIMIT or wall > WALL_LIMIT
        save(
            output / "summary.json",
            {
                "passed": not censored,
                "local_only": True,
                "budget_censored": censored,
                "new_unique_pytest_cases": DECLARED_TESTS,
                "previous_fixture_counts_added_again": 0,
                "mathematical_scalar_graph_emitted": True,
                "actual_scalar_clean_XOR_source_emitted": True,
                "candidate_actual_gate_replays": 16,
                "control_actual_gate_replays": 2,
                "candidate_clean_resources": candidate["resources"],
                "paid_control_clean_resources": control["resources"],
                "both_sources_same_exact_scalar_function": True,
                "complete_native_high_wires_copy_and_scratch_charged": True,
                "initial_Hadamards_separate_from_arithmetic": 32,
                "source_private_vs_full_source_memory_gain_measured_only": True,
                "all_Q32_uniform_law_proof_from_new_site_recipe_not_samples": True,
                "old_Box_Muller_financial_source_changed": False,
                "full_financial_sampler_or_price_certificate_adopted": False,
                "native_financial_path_error_bound": None,
                "financial_cost_or_physical_latency_extrapolated": False,
                "full_G2_or_quantum_advantage_established": False,
                "new_financial_prices_or_replays": 0,
                "CPU_seconds": cpu,
                "wall_seconds": wall,
            },
        )
    except BaseException as failure:
        save(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(failure, TimeoutError),
                "terminal_failure": traceback.format_exc(),
                "new_financial_prices_or_replays": 0,
            },
        )
        finish_manifest(output, protocol, files)
        raise
    finish_manifest(output, protocol, files)
    print("One actual scalar AS241 component and generic-divider control retained", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
