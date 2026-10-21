"""Bounded read-only q32/f40 scalar-loader interface and method census.

Freeze the methods and error target before inspecting cost outcomes. Read
existing gate metadata only; generate no tables, leaves, circuits or price paths.
"""

import argparse
import ast
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil
import sys
import time

from research.controlled_priority_completion.parallel_source import entries
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    BASELINE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT


ROUNDING = PROGRAM / "C06_quantile_rounding_run001"
PREFIX = ROOT / "results/limitation_audit_20261001/gaussian_v3"
METHODS = (
    "rigorous_fixed_precision_CDF_bisection",
    "AS241_piecewise_rational_inverse_normal",
    "archived_prefix_rotation_Gaussian_preparation",
)
TARGET = Fraction(1, 100000000)
LOCAL_CODE = (
    "research/limitation_program_20261001/quantile_loader_census.py",
    "research/limitation_program_20261001/quantile_rounding_certificate.py",
    "research/limitation_program_20261001/barrier_band_certificate.py",
    "research/controlled_source_completion/ir.py",
    "research/controlled_source_completion/primitives.py",
    "research/controlled_source_completion/compiler.py",
    "research/controlled_priority_completion/parallel_source.py",
    "research/limitation_audit_20261001/experiment_gaussian.py",
    "docs/limitation_audit_20261001/implementation_plan/ARITHMETIC.md",
)
PRIMARY_URLS = (
    "https://svn.r-project.org/R/trunk/src/nmath/qnorm.c",
    "https://doi.org/10.2307/2347330",
)


def pair(value):
    return [value.numerator, value.denominator]


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("New prospective bounded census receipt required")
    if not read(ROUNDING / "summary.json")["passed"]:
        raise ValueError("Accepted local rounded-quantile prerequisite required")
    receipt = read(ROUNDING / "manifest.json")
    frozen = {
        name.replace("\\", "/"): sha
        for field in ("files", "frozen_inputs")
        for name, sha in receipt[field].items()
    }
    frozen[relative(ROUNDING / "manifest.json")] = digest(ROUNDING / "manifest.json")
    # The A10 legacy manifest binds every original source and native leaf.
    legacy = read(BASELINE / "manifest.json")
    for name, sha in legacy.items():
        path = BASELINE / name.replace("\\", "/")
        frozen[relative(path)] = sha
    frozen[relative(BASELINE / "manifest.json")] = digest(BASELINE / "manifest.json")
    for name in LOCAL_CODE:
        frozen[name] = digest(ROOT / name)
    for path in PREFIX.rglob("*"):
        if path.is_file():
            frozen[relative(path)] = digest(path)
    verify({"frozen_inputs": frozen})
    output.mkdir()
    shutil.copy2(Path(__file__), output / Path(__file__).name)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_outcome_sensitive_native_or_loader_cost_inspection": True,
        "methods": list(METHODS),
        "maximum_methods": 3,
        "uniform_bits": 32,
        "fraction_bits": 40,
        "native_word_width": 72,
        "required_uniform_absolute_quantile_error_exact": pair(TARGET),
        "error_reference": "exact Phi_inverse((raw+1/2)/2^32) on every unsigned q32 raw word",
        "conditional_additional_price_bias_exact": {
            case: pair(dimension * 80 * Fraction(2, 5) * TARGET)
            for case, dimension in (("B4x12", 60), ("B8x52", 468))
        },
        "additional_native_path_error_included": False,
        "primary_sources_allowed": list(PRIMARY_URLS),
        "source_retrieval_and_method_notes": (
            "After this freeze, record primary source bytes/hash and bounded "
            "method/interface observations in primary_sources.json and method_notes.json. "
            "No coefficients fitted, algorithm evaluated, or candidate circuit emitted."
        ),
        "cost_basis": "Existing archived primitive metadata and prototype solver work only",
        "stop_rule": (
            "Exactly three fixed methods, one1e-8 target; no tuning, table fitting, "
            "new gate generation, quantumcost extrapolation, or financial sample. "
            "A candidate requires a global target-error certificate and exact "
            "primitive/domain/cleanup interfaces before a reversible implementation."
        ),
        "QSVT_new_candidate_added": False,
        "original_Box_Muller_baseline_edited": False,
        "preexisting_Stage_C_jobs_edited": False,
        "new_quantum_gates_generated_or_replayed": 0,
        "new_B4_B8_price_observations": 0,
        "process_CPU_limit_seconds": 120,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    print("Three-method q32/f40 loader census prospectively frozen", flush=True)


def primitive_inventory():
    paths = (
        ROOT / "research/controlled_source_completion/ir.py",
        ROOT / "research/controlled_source_completion/primitives.py",
    )
    result = []
    wanted = {"add", "sub", "mul", "cmul", "divide", "sqrt", "lookup", "lt", "select", "log", "cdf"}
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = [
            {"name": node.name, "line": node.lineno}
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
        operation_literals = defaultdict(list)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value in wanted
            ):
                operation_literals[node.value].append(node.lineno)
        result.append(
            {
                "path": relative(path),
                "sha256": digest(path),
                "functions": functions,
                "operation_literal_evidence_lines": dict(operation_literals),
                "numeric_quantum_cost_newly_inferred": False,
            }
        )
    return result


def archived_native_cost_census():
    result = {}
    for case in ("B4x12", "B8x52"):
        source_path = BASELINE / case / "min-depth/source.json"
        source = read(source_path)
        metadata = entries(source)
        by_op = defaultdict(list)
        for leaf, entry in metadata.items():
            by_op[entry["op"]].append(
                {
                    "leaf": leaf,
                    "native_arg_widths": [len(register) for register in entry["args"]],
                    "native_out_widths": [len(register) for register in entry["outs"]],
                    "native_qubits": entry["resources"]["qubits"],
                    "actual_forward_T_count": entry["resources"]["t_count"],
                    "actual_forward_T_depth": entry["resources"]["t_depth"],
                    "actual_forward_source_gates": entry["resources"]["source_gates"],
                    "input_law_or_range_contract": entry.get("contract"),
                }
            )
        result[case] = {
            "original_source_path": relative(source_path),
            "original_source_sha256": digest(source_path),
            "original_word_width": source["word_width"],
            "original_fraction_bits": source["fraction_bits"],
            "existing_leaf_count": len(metadata),
            "existing_leaves_by_op": dict(by_op),
            "specialized_site_cost_is_a_generic_quantile_cost": False,
            "copies_native_high_outputs_scratch_and_inverse_not_free": True,
            "candidate_quantile_T_count": None,
            "candidate_quantile_T_depth": None,
        }
    return result


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Census already completed")
    protocol = read(output / "protocol.json")
    verify(protocol)
    if protocol["methods"] != list(METHODS):
        raise ValueError("Fixed method list changed")
    started = time.process_time()
    notes = read(output / "method_notes.json")
    primary = read(output / "primary_sources.json")
    if [row["method"] for row in notes["methods"]] != list(METHODS):
        raise ValueError("Exactly the preregistered methods required")
    for row in primary["sources"]:
        if row["url"] not in PRIMARY_URLS:
            raise ValueError("Unregistered primary algorithm source")
        if row.get("local_path"):
            if digest(ROOT / row["local_path"]) != row["sha256"]:
                raise ValueError("Retrieved primary source bytes changed")
    for row in notes["methods"]:
        if (
            row["globally_certified_q32_f40_error_at_target"] is not False
            or row["coherent_loader_implemented"] is not False
            or row["quantile_quantum_T_count"] is not None
            or row["quantile_quantum_T_depth"] is not None
        ):
            raise ValueError("Unproved candidate admitted or quantum cost inferred")
    save(output / "primitive_interface_inventory.json", primitive_inventory())
    save(output / "archived_native_cost_inventory.json", archived_native_cost_census())
    save(output / "archived_prefix_summary.json", read(PREFIX / "summary.json"))
    solver = read(ROUNDING / "summary.json")
    measured_solver = {
        name: solver[name]
        for name in (
            "actual_quantile_words_attempted",
            "actual_quantile_words_certified",
            "total_actual_word_bisection_steps",
            "total_actual_word_CDF_enclosure_evaluations",
            "maximum_actual_word_bisection_steps",
            "classical_actual_word_solver_CPU_seconds",
            "all_input_solver_completeness_certified",
            "quantum_gate_costs_extrapolated",
        )
    }
    save(output / "actual_prototype_classical_work.json", measured_solver)
    elapsed = time.process_time() - started
    if elapsed > protocol["process_CPU_limit_seconds"]:
        raise TimeoutError("Bounded read-only census CPU limit")
    summary = {
        "passed": True,
        "local_only": True,
        "fixed_methods": list(METHODS),
        "required_uniform_absolute_quantile_error_exact": pair(TARGET),
        "conditional_additional_price_bias_exact": protocol[
            "conditional_additional_price_bias_exact"
        ],
        "native_path_error_included": False,
        "globally_certified_loader_candidates_at_target": 0,
        "new_tables_or_leaves_or_circuits_generated": 0,
        "new_financial_price_observations_or_gate_replays": 0,
        "original_Box_Muller_baseline_edited": False,
        "preexisting_Stage_C_jobs_edited": False,
        "candidate_quantum_costs": None,
        "smallest_missing_prerequisite": notes["smallest_missing_prerequisite"],
        "next_fixed_bounded_work": notes["next_fixed_bounded_work"],
        "primary_source_notes_path": relative(output / "primary_sources.json"),
        "method_notes_path": relative(output / "method_notes.json"),
        "complete_G2_closed": False,
        "quantum_advantage_established": False,
        "elapsed_read_only_census_CPU_seconds": elapsed,
    }
    save(output / "summary.json", summary)
    manifest(output, protocol)
    print("Bounded loader census complete; no candidate adopted", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
