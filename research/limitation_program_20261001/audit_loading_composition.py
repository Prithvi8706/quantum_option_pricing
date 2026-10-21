"""Independent bounded audit of A05 preparation-state error composition.

Do not import or execute producer functions or repeat its twelve fixtures.
Check saved exact allowances, archive comparisons, factorization guards and
their limited claims against an independent fidelity/telescoping derivation.
"""

from __future__ import annotations

# Receipt prose records the exact scope of the mathematical checks.
# ruff: noqa: E501

import argparse
import ast
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A05_loading_run001"
CASES = (("B4x12", 60), ("B8x52", 468))
BITS = 128
BUDGET = Fraction(1, 1000)
SPAN = Fraction(40)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_float=Decimal)


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    assert isinstance(value, list) and len(value) == 2
    assert all(type(number) is int for number in value)
    result = Fraction(*value)
    assert pair(result) == value
    return result


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("Frozen dependency changed", name)


def independent_dyadic_lower(square):
    """Binary-search the dyadic integer; do not reuse producer's integer sqrt."""
    scale = 1 << BITS
    left, right = 0, scale + 1
    while right - left > 1:
        center = (left + right) // 2
        if center * center * square.denominator <= square.numerator * scale * scale:
            left = center
        else:
            right = center
    answer = Fraction(left, scale)
    assert answer**2 <= square < (answer + Fraction(1, scale)) ** 2
    return answer


def independent_structure_checks():
    """Exact rank-two density check and a correlated-marginal counterexample."""
    # Rational unit vectors avoid floating point eigensolver assertions.
    a, b = Fraction(3, 5), Fraction(5, 13)
    vectors = ((Fraction(4, 5), a), (Fraction(12, 13), b))
    state = [x * y for x in vectors[0] for y in vectors[1]]
    assert sum(x * x for x in state) == 1
    delta = [[state[i] * state[j] - int(i == j == 0) for j in range(4)] for i in range(4)]
    trace = sum(delta[i][i] for i in range(4))
    trace_squared = sum(delta[i][j] * delta[j][i] for i in range(4) for j in range(4))
    assert trace == 0
    product_squared = 1 - (1 - a * a) * (1 - b * b)
    assert trace_squared == 2 * product_squared == 2 * (a * a + b * b - a * a * b * b)
    # Delta is a difference of two rank-one matrices. Thus its at most two
    # nonzero eigenvalues are +/-sqrt(trace(Delta^2)/2), proving D^2.
    rho = (Fraction(1, 2), Fraction(0), Fraction(0), Fraction(1, 2))
    sigma = (Fraction(0), Fraction(1, 2), Fraction(1, 2), Fraction(0))
    assert sum(abs(x - y) for x, y in zip(rho, sigma)) / 2 == 1
    for state_diag in (rho, sigma):
        assert [state_diag[0] + state_diag[1], state_diag[2] + state_diag[3]] == [Fraction(1, 2)] * 2
        assert [state_diag[0] + state_diag[2], state_diag[1] + state_diag[3]] == [Fraction(1, 2)] * 2
    return dict(
        two_factor_product_distance_squared=pair(product_squared),
        density_matrix_exact_arithmetic=True,
        correlated_joint_trace_distance_exact=[1, 1],
        correlated_marginal_distances_exact=[[0, 1], [0, 1]],
        pure_product_derivation="For pure factors Fi=|<psi_i|phi_i>|^2=1-di^2. Independent tensor overlaps multiply, so D^2=1-product(Fi). Two factors expand to d1^2+d2^2-d1^2*d2^2.",
        product_upper_derivation="For 0<=xi<=1, 1-product(1-xi)<=sum(xi), by induction from x+y-xy<=x+y. With xi=di^2 this yields D<=sqrt(sum(di^2)).",
        general_tensor_derivation="Expand tensor(rho_i)-tensor(sigma_i) as the sum of one changed factor with preceding rho and succeeding sigma factors. The trace norm of a tensor product multiplies, and every density operator has trace norm one. Triangle inequality therefore gives D<=sum(di); D<=1 supplies the cap.",
        bounded_observable_derivation="For Delta=rho-sigma with trace zero, Jordan parts have Tr(Delta+)=Tr(Delta-)=D. If 0<=Y<=40*I, both Tr(Y*Delta+) and Tr(Y*Delta-) lie in [0,40D], hence |Tr(Y*Delta)|<=40D.",
        arbitrary_correlated_state_bound_from_marginals_valid=False,
        full_unitary_operator_bound_from_prepared_state_bound_valid=False,
    )


def static_guards():
    text = (SOURCE / "loading_error_composition.py").read_text(encoding="utf-8")
    tree = ast.parse(text)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    product = functions["product_trace_squared"]
    assert len(product.args.kwonlyargs) == 1
    assert product.args.kwonlyargs[0].arg == "independent_pure_product"
    guard = product.body[0]
    assert isinstance(guard, ast.If) and isinstance(guard.body[0], ast.Raise)
    assert ast.unparse(guard.test) == "independent_pure_product is not True"
    assert "type(value) is int or isinstance(value, Fraction)" in ast.unparse(functions["probability"])
    assert "0 <= value <= 1" in ast.unparse(functions["probability"])
    assert "min(Fraction(1), sum(errors, Fraction(0)))" in ast.unparse(functions["general_trace_upper"])
    assert "type(draws) is not int or draws < 1" in ast.unparse(functions["allowances"])
    assert "result ** 2 <= value < (result + Fraction(1, scale)) ** 2" in ast.unparse(functions["sqrt_lower"])
    return dict(pure_product_keyword_requires_literal_True=True, exact_rational_and_nonempty_error_inputs_checked=True, general_product_bound_has_unit_cap=True, producer_functions_executed_by_auditor=0)


def audit_row(row, case, draws, archived):
    assert row["case"] == case and row["draws"] == draws
    task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
    assert task["digital_source"]["normal_count"] == draws == (task["assets"] + 1) * task["dates"]
    assert Fraction(task["barrier_dollars"]) - Fraction(task["strike_dollars"]) == SPAN
    assert task["annual_rate"] >= 0 and task["maturity_years"] > 0
    assert task["digital_source"]["uniform_bits_each"] == 32
    assert "Box-Muller" in task["digital_source"]["law"]
    assert "discount is already applied" in task["digital_source"]["output_dollar_conversion"]
    support = read(PROGRAM / "E03_support_run001" / (case + "_certificate.json"))
    support_audit = read(PROGRAM / "E03_support_audit_run002/summary.json")
    accepted_support = next(item for item in support_audit["cases"] if item["case"] == case)
    assert support_audit["passed"] is True and support_audit["all_input_native_output_support_certified"] is True
    assert support["all_original_uniform_word_patterns"] is True
    assert support["payoff_raw_bounds"] == accepted_support["payoff_raw_bounds"]
    assert support["payoff_raw_bounds"][0] == 0
    assert Fraction(support["payoff_raw_bounds"][1], 1 << 40) < SPAN
    ledger = read(PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"))
    headroom = exact(ledger["assessment"]["remaining_dollar_headroom"])
    assert headroom > BUDGET
    assert ledger["full_price_confidence_claim"] is False and ledger["assessment"]["complete_price_certified"] is False
    total = BUDGET / SPAN
    conservative = total / draws
    square = total**2 / draws
    pure = independent_dyadic_lower(square)
    assert exact(row["loading_bias_dollars_exact"]) == BUDGET
    assert exact(row["payoff_span_dollars_exact"]) == SPAN
    assert exact(row["total_preparation_trace_allowance_exact"]) == total
    assert exact(row["conservative_scalar_trace_allowance_exact"]) == conservative == Fraction(1, 40000 * draws)
    assert exact(row["pure_product_scalar_trace_allowance_lower_exact"]) == pure
    assert exact(row["pure_product_scalar_trace_allowance_square_upper_exact"]) == square
    assert exact(row["product_distance_squared_proved_upper_exact"]) == draws * pure * pure <= total * total
    assert draws * conservative * SPAN == BUDGET
    # Exact product is checked internally; its large fraction is not serialized.
    product_squared = 1 - (1 - pure * pure) ** draws
    assert product_squared <= draws * pure * pure <= total * total
    assert row["exact_product_distance_squared_formula"] == "1-(1-tau^2)^draws"
    assert row["pure_product_independence_and_purity_required"] is True
    for key in ("scalar_operator_norm_guarantee_supplied", "coherent_rotation_errors_or_correlated_noise_included", "current_price_ledger_changed"):
        assert row[key] is False
    diagnostics = []
    assert len(row["archived_q10_diagnostics"]) == len(archived) == 3
    for record, old in zip(row["archived_q10_diagnostics"], archived):
        assert record["bond_cap"] == old["bond_cap"]
        assert "Numerical compression only" in old["scope"]
        error = Fraction(old["trace_distance"])
        assert exact(record["recorded_numerical_scalar_trace_error_exact"]) == error
        assert record["below_conservative_scalar_allowance_numerically"] is (error <= conservative)
        assert record["below_pure_product_scalar_allowance_numerically"] is (error <= pure)
        for key in ("error_is_a_rigorous_preparation_certificate", "emitted_and_synthesized_MPS_circuit", "q10_binned_truncated_law_matches_current_q32_BM", "full_continuous_price_bridge_certified"):
            assert record[key] is False
        diagnostics.append(dict(bond_cap=old["bond_cap"], saved_numeric_error_exact=pair(error), conservative_threshold_pass=error <= conservative, pure_product_threshold_pass=error <= pure, numerical_only=True))
    assert [item["bond_cap"] for item in diagnostics] == [2, 4, 8]
    return dict(case=case, factors=draws, conservative_scalar_allowance_exact=pair(conservative), independent_128_bit_pure_scalar_lower_exact=pair(pure), exact_product_inequality_checked=True, reserved_loading_dollars_exact=pair(BUDGET), current_unallocated_headroom_exact=pair(headroom), previously_audited_native_payoff_upper_dollars_exact=pair(Fraction(support["payoff_raw_bounds"][1], 1 << 40)), native_selector_normalization_is_separate_from_40_dollar_observable_bound=True, loading_budget_adopted_in_complete_price_ledger=False, diagnostics=diagnostics)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    manifest = read(SOURCE / "manifest.json")
    frozen = dict(manifest["files"])
    frozen.update(manifest["frozen_inputs"])
    frozen[relative(SOURCE / "manifest.json")] = sha(SOURCE / "manifest.json")
    for path in (PROGRAM / "E03_support_audit_run002/summary.json", *(PROGRAM / "E03_support_run001" / (case + "_certificate.json") for case, _ in CASES)):
        frozen[relative(path)] = sha(path)
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_loading_composition.py")
    save(output / "protocol.json", dict(created_utc=datetime.now(timezone.utc).isoformat(), local_only=True, before_independent_reconciliation=True, frozen_inputs=frozen, interpreter_sha256=sha(sys.executable), source_receipt=relative(SOURCE), fixed_cases=[dict(case=case, draws=draws) for case, draws in CASES], scalar_dyadic_precision_bits=BITS, numerical_archive_bits=10, numerical_archive_bond_caps=[2, 4, 8], independent_allowance_method="Exact rational binary search for the largest 128-bit dyadic with square <= total_trace_allowance^2/draws", composition_derivation="Independent pure overlap multiplicativity, general tensor trace-norm telescoping, and Jordan-decomposition effect duality", process_CPU_limit_seconds=60, producer_test_reexecutions=0, new_compression_experiments=0, new_preparation_or_financial_circuits=0, loading_law_adoption=False, repeated_coherent_or_operator_error_adoption=False))
    print("A05 loading audit prospectively frozen", flush=True)


def run(output):
    started = time.process_time()
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    source_protocol = read(SOURCE / "protocol.json")
    assert source_protocol["before_tests_and_loading_allowance_screen"] is True
    assert source_protocol["fixed_dyadic_scalar_allowance_bits"] == BITS
    assert source_protocol["loading_budget_is_exploratory_not_adopted_in_current_BM_ledger"] is True
    assert source_protocol["coherent_gate_operator_errors_are_separate_from_state_preparation_law_bias"] is True
    assert source_protocol["actual_driver_counts"] == [60, 468]
    assert source_protocol["archive_diagnostic_grid_bits"] == 10 and source_protocol["archive_bond_caps"] == [2, 4, 8]
    xml = ET.parse(SOURCE / "tests.xml").getroot()
    cases = list(xml.iter("testcase"))
    assert len(cases) == 12
    assert len({(item.attrib.get("classname"), item.attrib["name"]) for item in cases}) == 12
    assert not list(xml.iter("failure")) and not list(xml.iter("error")) and not list(xml.iter("skipped"))
    certificate = read(SOURCE / "certificate.json")
    assert certificate["trace_distance_convention"] == "one half of trace norm"
    expected_formulae = dict(two_factor_identity="D_product^2 = D1^2+D2^2-D1^2*D2^2 for independent pure products", general_bound="D(tensor rho_i,tensor sigma_i) <= min(1,sum_i D(rho_i,sigma_i))", pure_bound="D_product^2 = 1-product_i(1-D_i^2) <= sum_i D_i^2", bounded_observable_bound="0<=Y<=40 implies |Tr[Y(rho-sigma)]|<=40*D(rho,sigma)")
    assert all(certificate[key] == value for key, value in expected_formulae.items())
    for key in ("purity_failure_or_factor_correlation_requires_general_valid_joint_bound", "basis_state_preparation_error_is_not_full_unitary_operator_error", "approximate_law_bias_and_repeated_gate_execution_error_are_distinct"):
        assert certificate[key] is True
    assert len(certificate["rows"]) == 2
    archived = read(PROGRAM / "A02_quantile_census_run001/archived_prefix_summary.json")
    q10 = [row for row in archived["cases"] if row["bits"] == 10]
    assert len(q10) == 1 and q10[0]["cutoff"] == 6 and q10[0]["rotation_synthesis_t_count"] is None
    rows = [audit_row(row, case, draws, q10[0]["mps"]) for row, (case, draws) in zip(certificate["rows"], CASES)]
    proofs = independent_structure_checks()
    proofs["producer_guard_review"] = static_guards()
    save(output / "independent_composition_proof.json", proofs)
    save(output / "case_allowances_and_numeric_comparisons.json", rows)
    summary = read(SOURCE / "summary.json")
    assert summary["passed"] is True and summary["composition_families"] == 2 and summary["actual_driver_profiles"] == 2
    assert summary["archived_numerical_diagnostics"] == 6 and summary["actual_certified_and_synthesized_MPS_candidates"] == 0
    for key in ("law_replacement_adopted", "current_complete_price_ledger_changed", "full_continuous_price_or_physical_certificate"):
        assert summary[key] is False
    assert summary["new_financial_prices_or_gates"] == 0
    verify(protocol["frozen_inputs"])
    assert time.process_time() - started < 60
    save(output / "summary.json", dict(passed=True, local_only=True, producer_distinct_fixture_results_reconciled=12, producer_fixture_reexecutions=0, additional_fixture_test_credit=0, exact_driver_profiles_reconciled=2, existing_unique_q10_MPS_numeric_records=3, case_threshold_comparisons=6, new_MPS_compression_experiments=0, numerical_threshold_passing_bond_caps=[8], rigorous_preparation_certificate_candidates=0, general_mixed_tensor_product_bound_valid=True, general_correlated_joint_bound_from_marginals_valid=False, pure_product_structure_required=True, bounded_0_to_40_observable_factor_exact=[40, 1], exploratory_loading_dollars_exact=[1, 1000], loading_allocation_adopted=False, full_unitary_or_repeated_coherent_error_guarantee_adopted=False, accepted_finite_Box_Muller_source_changed=False, new_preparation_or_financial_circuits=0, full_continuous_price_certificate=False, quantum_advantage_claim=False, elapsed_process_CPU_seconds=time.process_time() - started))
    finish_manifest(output)
    print("A05 loading composition independent audit PASS", flush=True)


def finish_manifest(output):
    save(output / "manifest.json", dict(files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()}, frozen_inputs=read(output / "protocol.json")["frozen_inputs"], manifest_self_hash_excluded=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(output / "summary.json", dict(passed=False, local_only=True, failure_type=type(failure).__name__, message=str(failure), producer_fixture_reexecutions=0, additional_fixture_test_credit=0, new_preparation_or_financial_circuits=0, accepted_finite_Box_Muller_source_changed=False))
            finish_manifest(output)
            raise
