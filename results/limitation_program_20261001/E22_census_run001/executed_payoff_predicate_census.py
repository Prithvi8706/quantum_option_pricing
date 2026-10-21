"""Frozen actual-source census for exact log-domain payoff eligibility.

Rebuild the original B4/B8 builder only to label its unchanged optimized SSA.
Enumerate every predicate and guard separately. No source compilation, circuit,
path price, financial observation, or signal approximation is performed.
"""

from __future__ import annotations

# Receipt explanations are readable prose.
# ruff: noqa: E501

import argparse
import ast
from collections import Counter, defaultdict
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
ACCEPTED = PROGRAM / "A10_coefficient_run001"
CASES = (("B4x12", 4, 12), ("B8x52", 8, 52))


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen dependency changed", name)


def local_import_inventory(seeds):
    """Read-only static inventory of possible local imports, before analysis."""
    pending, result = list(seeds), set()
    while pending:
        path = Path(pending.pop()).resolve()
        if path in result:
            continue
        assert path.is_file() and path.is_relative_to(ROOT)
        result.add(path)
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
                modules.append(node.module)
                modules.extend(node.module + "." + alias.name for alias in node.names)
        for module in modules:
            if module.startswith("research."):
                candidate = ROOT.joinpath(*module.split(".")).with_suffix(".py")
                if candidate.is_file() and candidate not in result:
                    pending.append(candidate)
    return sorted(result)


def capture_builder(assets, dates, target):
    from research.advantage_frontier_20260923 import barrier_oracle_depth as builder
    from research.controlled_source_completion.ir import Graph
    from research.controlled_source_completion.optimize import optimize
    from research.limitation_program_20261001.baseline import fingerprints

    normal_values, exponentials, clips, contexts = [], [], [], []
    saved = builder.normals_graph, builder.exp_estrin, Graph.clip, Graph.interpolate

    def normals(graph, count, q):
        result = saved[0](graph, count, q)
        normal_values.extend(result)
        return result

    def exponential(graph, value):
        out = saved[1](graph, value)
        exponentials.append((value, out))
        return out

    def clip(graph, value, low, high):
        first = len(graph.nodes)
        out = saved[2](graph, value, low, high)
        clips.append(
            dict(
                value=value,
                low=low,
                high=high,
                out=out,
                table=contexts[-1] if contexts else None,
                lt_values=[node["out"][0] for node in graph.nodes[first:] if node["op"] == "lt"],
            )
        )
        return out

    def interpolate(graph, name, value):
        contexts.append(name)
        try:
            return saved[3](graph, name, value)
        finally:
            contexts.pop()

    builder.normals_graph, builder.exp_estrin, Graph.clip, Graph.interpolate = (
        normals,
        exponential,
        clip,
        interpolate,
    )
    try:
        original = json.loads(json.dumps(builder.build(assets, dates, q=32).as_dict()))
    finally:
        builder.normals_graph, builder.exp_estrin, Graph.clip, Graph.interpolate = saved
    assert optimize(copy.deepcopy(original)) == target, (
        "Full original builder/optimizer differs from accepted target"
    )
    before, after = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in after.items()}
    assert len(reverse) == len(after), "Ambiguous accepted structural SSA labels"

    def mapped(value):
        return reverse[before[value]]

    assert len(normal_values) == dates * (assets + 1) and len(exponentials) == assets * dates
    return dict(
        original_fingerprint=fingerprint(original),
        target_fingerprint=fingerprint(target),
        normal_values=list(map(mapped, normal_values)),
        exponentials=[
            dict(
                asset=index // dates,
                date=index % dates,
                clipped_log=mapped(log),
                stock=mapped(stock),
                stock_structural_fingerprint=after[mapped(stock)],
            )
            for index, (log, stock) in enumerate(exponentials)
        ],
        clips=[
            dict(
                value=mapped(item["value"]),
                low=mapped(item["low"]),
                high=mapped(item["high"]),
                out=mapped(item["out"]),
                table=item["table"],
                lt_values=list(map(mapped, item["lt_values"])),
            )
            for item in clips
        ],
        complete_optimized_graph_equality=True,
    )


def census_case(case, assets, dates):
    from research.controlled_priority_completion.parallel_source import entries
    from research.controlled_source_completion.compact_parallel_v7 import _storage
    from research.controlled_source_completion.compiler import resolve_library

    directory = ACCEPTED / case / "min-depth"
    target, source = read(directory / "target.json"), read(directory / "source.json")
    task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
    support = read(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"))
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    labels = capture_builder(assets, dates, target)
    assert target["width"] == source["word_width"] == 72
    assert target["fraction_bits"] == source["fraction_bits"] == 40
    Q = 1 << 40
    nodes = target["nodes"]
    producers = {value: index for index, node in enumerate(nodes) for value in node["out"]}
    assert len(producers) == source["values"] and set(producers) == set(range(source["values"]))
    noninput = [index for index, node in enumerate(nodes) if node["op"] != "input"]
    call_for_node = dict(zip(noninput, range(len(source["forward_calls"])), strict=True))

    def node(value):
        return nodes[producers[value]]

    def constant(value):
        item = node(value)
        assert item["op"] == "const"
        raw = item["params"]["value"]
        return raw - (1 << 72) if raw & (1 << 71) else raw

    def ancestors(roots, stop=()):
        boundaries, seen, stack = set(stop), set(), list(roots)
        while stack:
            value = stack.pop()
            if value in boundaries:
                continue
            index = producers[value]
            if index not in seen:
                seen.add(index)
                stack.extend(nodes[index]["args"])
        return seen

    full_ancestry = ancestors(target["outputs"].values())
    assert set(noninput) <= full_ancestry
    gaussian_ancestry = ancestors(labels["normal_values"])
    stock_values = [item["stock"] for item in labels["exponentials"]]
    assert len(set(stock_values)) == assets * dates
    stocks_set = set(stock_values)

    def flatten_sum(value):
        if value in stocks_set:
            return [value]
        item = node(value)
        assert item["op"] == "add", ("Expected original stock sum", value)
        return flatten_sum(item["args"][0]) + flatten_sum(item["args"][1])

    output_value = target["outputs"]["Y"]
    output = node(output_value)
    assert (
        target["outputs"] == source["outputs"] == dict(Y=output_value) and output["op"] == "select"
    )
    alive, discounted, zero = output["args"]
    alive_node, discount_node = node(alive), node(discounted)
    assert alive_node["op"] == "lt" and discount_node["op"] == "cmul" and constant(zero) == 0
    maximum, H_value = alive_node["args"]
    assert constant(H_value) == 140 * Q
    positive = discount_node["args"][0]
    assert node(positive)["op"] == "positive"
    difference = node(positive)["args"][0]
    assert node(difference)["op"] == "sub"
    average, K_value = node(difference)["args"]
    assert constant(K_value) == 100 * Q and node(average)["op"] == "cmul"
    asian_sum = node(average)["args"][0]
    assert sorted(flatten_sum(asian_sum)) == sorted(stock_values)
    average_coefficient = node(average)["params"]["c"]
    assert average_coefficient == round(float(Fraction(1, assets * dates)) * Q)
    assert discount_node["params"]["c"] == round(math.exp(-0.03) * Q)
    assert task["assets"] == assets and task["dates"] == dates
    assert task["strike_dollars"] == 100 and task["barrier_dollars"] == 140
    assert task["spot_each_asset_dollars"] == 100 and task["annual_rate"] == 0.03
    assert task["annual_volatility_each_asset"] == 0.3 and task["equicorrelation"] == 0.4
    assert (
        task["maturity_years"] == 1
        and task["barrier_equality"] == "basket >= H is knocked out; alive uses strict < H"
    )
    assert task["digital_source"]["output"] == target["outputs"]
    assert (
        support["all_stock_native_intermediates_no_overflow"]
        and support["all_actual_sum_max_average_subtract_discount_nodes_safe"]
    )

    baskets, max_flags = {}, []
    for date in range(dates):
        expected = sorted(item["stock"] for item in labels["exponentials"] if item["date"] == date)
        matches = [
            item
            for item in nodes
            if item["op"] == "cmul"
            and item["params"]["c"] == Q // assets
            and sorted(flatten_sum(item["args"][0])) == expected
        ]
        # Only invoke stock-sum flattening on possible basket coefficients;
        # those power-of-two coefficient sites in this builder are baskets.
        assert len(matches) == 1
        item = matches[0]
        value = item["out"][0]
        baskets[value] = dict(
            date=date,
            basket_value=value,
            basket_sum_value=item["args"][0],
            stock_values=expected,
            coefficient=item["params"]["c"],
            native_comparison="floor(sum(stock_raw)*coefficient/2^40) < 140*2^40",
            strict_alive=True,
            knockout_at_equality=True,
            implemented_via_maximum_tree_and_global_alive_value=alive,
            independent_per_date_comparison_gate_emitted=False,
        )

    def flatten_max(value):
        if value in baskets:
            return [value]
        item = node(value)
        assert item["op"] == "select"
        flag, selected_large, selected_small = item["args"]
        compare = node(flag)
        assert compare["op"] == "lt" and compare["args"] == [selected_small, selected_large]
        max_flags.append(flag)
        return flatten_max(selected_small) + flatten_max(selected_large)

    assert sorted(flatten_max(maximum)) == sorted(baskets)
    assert len(set(max_flags)) == dates - 1

    classes = {}

    def classify(values, category):
        for value in values:
            assert value not in classes, ("Predicate classified twice", value)
            classes[value] = category

    classify([alive], "strict_survival_of_monitored_arithmetic_baskets")
    classify(max_flags, "maximum_tree_between_arithmetic_baskets")
    classify([positive], "positive_part_of_arithmetic_Asian_strike_difference")
    path_clips, gaussian_clips = [], []
    clipped_values = {item["clipped_log"] for item in labels["exponentials"]}
    for clip in labels["clips"]:
        assert len(clip["lt_values"]) == 2
        if clip["out"] in clipped_values:
            assert clip["table"] is None
            assert constant(clip["low"]) == round(math.log(2**-16) * Q)
            assert constant(clip["high"]) == round(math.log(4096) * Q)
            path_clips.append(clip)
            classify(clip["lt_values"], "path_log_clipping_guard")
        else:
            assert clip["table"] in ("log", "cos")
            gaussian_clips.append(clip)
            classify(clip["lt_values"], "Gaussian_" + clip["table"] + "_table_argument_guard")
    assert len(path_clips) == assets * dates
    gaussian_pairs = dates * (assets + 1) // 2
    assert len(gaussian_clips) == 3 * gaussian_pairs
    for item in nodes:
        value = item["out"][0]
        if item["op"] in ("lt", "positive") and value not in classes:
            assert producers[value] in gaussian_ancestry
            if item["op"] == "positive":
                classify([value], "Gaussian_square_root_nonnegative_argument_guard")
            else:
                assert constant(item["args"][1]) == 1
                classify([value], "Gaussian_log_positive_input_guard")
    all_predicates = [item for item in nodes if item["op"] in ("lt", "positive")]
    assert len(classes) == len(all_predicates)
    predicate_rows = []
    for item in all_predicates:
        value, index = item["out"][0], producers[item["out"][0]]
        assert index in full_ancestry
        predicate_rows.append(
            dict(
                node_index=index,
                call_index=call_for_node[index],
                op=item["op"],
                args=item["args"],
                out=item["out"],
                params=item["params"],
                classification=classes[value],
                financial_output_ancestor=True,
                Gaussian_ancestor=index in gaussian_ancestry,
                native_integer_semantics="signed less-than"
                if item["op"] == "lt"
                else "max(signed argument,0)",
                eligible_one_asset_financial_log_threshold=False,
            )
        )
    for item in nodes:
        if item["op"] == "select":
            assert item["args"][0] in classes and node(item["args"][0])["op"] == "lt"
    selection_rows = [
        dict(
            node_index=index,
            call_index=call_for_node[index],
            args=item["args"],
            out=item["out"],
            flag_value=item["args"][0],
            flag_classification=classes[item["args"][0]],
            classification="financial_output_alive_payoff_selection"
            if item["out"] == [output_value]
            else "branch_of_classified_original_comparison",
        )
        for index, item in enumerate(nodes)
        if item["op"] == "select"
    ]
    sites = defaultdict(list)
    for index in noninput:
        call_index = call_for_node[index]
        call = source["forward_calls"][call_index]
        sites[call["leaf"]].append(
            dict(
                call_index=call_index,
                node_index=index,
                args=call["args"],
                out=call["out"],
                region="Gaussian" if index in gaussian_ancestry else "financial_path_or_payoff",
            )
        )
    library = resolve_library(source)
    native_interfaces = [
        dict(
            key=key,
            op=metadata[key]["op"],
            params=metadata[key]["params"],
            input_contract=metadata[key].get("input_contract", {}),
            spec=metadata[key].get("spec"),
            gate_sha256=metadata[key]["sha256"],
            metadata_sha256=sha(library / (key + ".json")),
            sites=sites[key],
            domain_contract_is_not_a_financial_payoff_predicate=True,
        )
        for key in sorted(metadata)
    ]
    assert sum(len(item["sites"]) for item in native_interfaces) == len(source["forward_calls"])
    lookup_rows = [
        dict(
            node_index=index,
            call_index=call_for_node[index],
            table=item["params"]["table"],
            args=item["args"],
            out=item["out"],
            index_bits=item["params"]["bits"],
            table_fingerprint=fingerprint(target["tables"][item["params"]["table"]]),
        )
        for index, item in enumerate(nodes)
        if item["op"] == "lookup"
    ]
    assert len(lookup_rows) == 3 * gaussian_pairs
    assert all(item["table"] in ("log", "cos") for item in lookup_rows)
    category_counts = dict(Counter(classes.values()))
    assert category_counts["path_log_clipping_guard"] == 2 * assets * dates
    assert category_counts["Gaussian_log_positive_input_guard"] == gaussian_pairs
    assert category_counts["Gaussian_square_root_nonnegative_argument_guard"] == gaussian_pairs
    return dict(
        passed=True,
        case=case,
        assets=assets,
        dates=dates,
        accepted_target_sha256=sha(directory / "target.json"),
        accepted_source_sha256=sha(directory / "source.json"),
        frozen_original_task_sha256=sha(PROGRAM / "G0_run003" / (case + "_task.json")),
        builder_label_proof=labels,
        whole_original_native_site_validation=True,
        every_output_ancestor_predicate_classified_once=True,
        predicate_count=len(predicate_rows),
        predicate_category_counts=category_counts,
        actual_predicate_rows=predicate_rows,
        actual_selection_rows=selection_rows,
        original_operation_counts=dict(Counter(item["op"] for item in nodes)),
        stock_native_raw_support_bounds=support["stock_raw_bounds"],
        monitored_date_basket_conditions=sorted(baskets.values(), key=lambda row: row["date"]),
        original_maximum_tree_flags=max_flags,
        original_strict_alive_value=alive,
        original_Asian_strike=dict(
            average_value=average,
            sum_value=asian_sum,
            stock_values=stock_values,
            average_coefficient=average_coefficient,
            strike_value=K_value,
            strike_raw=100 * Q,
            difference_value=difference,
            positive_value=positive,
            strictly_positive_payoff_before_discount="native average > K; equality has zero payoff",
            discount_coefficient=discount_node["params"]["c"],
            output_value=output_value,
        ),
        path_clipping_guards=path_clips,
        Gaussian_table_clipping_guards=gaussian_clips,
        Gaussian_lookup_producers=lookup_rows,
        native_leaf_interfaces=native_interfaces,
        storage_proof_fingerprint=fingerprint(storage),
        required_signal_interface=(
            "The strict monitored payoff needs each date's exact sum of guarded native stock exponentials, their floor average, a strict H comparison and maximum/AND composition; the Asian strike needs the exact all-stock/date sum, rounded averaging coefficient, strict positive part and already-discounted magnitude. A coherent log-sum-exp or alternative signal must implement these dependencies with normalization, finite native/tie errors, preparation, inverse, comparison and all oracle invocations paid."
        ),
        eligible_whole_supported_domain_one_asset_financial_predicates=0,
        new_source_or_gates=0,
        new_path_prices=0,
        quantum_observations=0,
    )


def algebraic_eligibility_checks(censuses):
    """Two interface-level diagnostics, without new financial paths or prices."""
    records = []
    Q = 1 << 40
    for case in censuses:
        assets, dates = case["assets"], case["dates"]
        basket_c = case["monitored_date_basket_conditions"][0]["coefficient"]

        def basket(values):
            return (sum(value * Q for value in values) * basket_c) >> 40

        fixed_asset_a, fixed_asset_b = [100] * assets, [100] + [200] * (assets - 1)
        isolated_log_test_counterexample = [200] + [100] * (assets - 1)
        assert all(
            case["stock_native_raw_support_bounds"][0]
            <= value * Q
            <= case["stock_native_raw_support_bounds"][1]
            for value in (
                *fixed_asset_a,
                *fixed_asset_b,
                *isolated_log_test_counterexample,
                50,
                90,
                162,
            )
        )
        assert basket(fixed_asset_a) < 140 * Q <= basket(fixed_asset_b)
        assert fixed_asset_a[0] == fixed_asset_b[0]
        assert (
            basket(isolated_log_test_counterexample) < 140 * Q
            and max(isolated_log_test_counterexample) >= 140
        )
        n, coefficient = assets * dates, case["original_Asian_strike"]["average_coefficient"]
        uniform_words, dispersed_words = [90] * n, [50, 162] * (n // 2)
        average_a, average_b = (
            (sum(uniform_words) * coefficient),
            (sum(dispersed_words) * coefficient),
        )
        assert n % 2 == 0 and 50 * 162 == 90**2
        assert average_a < 100 * Q < average_b
        # Each date may pair 50 with 162 across the even asset count, making
        # the algebraic date baskets 106 < 140; this is not a finite-law path.
        assert basket([50, 162] * (assets // 2)) < 140 * Q
        records.append(
            dict(
                case=case["case"],
                diagnostic_domain="Algebraic/native stock-sum interface tuples within clipping support; these are not claimed to be realised finite Box-Muller paths",
                one_stock_threshold_diagnostic=dict(
                    same_first_asset_dollars=100,
                    surviving_stock_tuple=fixed_asset_a,
                    knocked_out_stock_tuple=fixed_asset_b,
                    exact_native_basket_raw_values=[basket(fixed_asset_a), basket(fixed_asset_b)],
                    all_individual_stocks_below_H_is_not_necessary=dict(
                        stock_tuple=isolated_log_test_counterexample,
                        basket_raw=basket(isolated_log_test_counterexample),
                    ),
                    conclusion="A predicate on one fixed stock/log cannot determine an unrestricted sum-of-stocks basket; conjunction of stock<H conditions is only sufficient. No whole finite-law replacement theorem is supplied.",
                ),
                arithmetic_Asian_log_average_diagnostic=dict(
                    equal_product_identity="50*162 = 90^2, so paired geometric means and ideal average logs agree",
                    uniform_stock_dollars=90,
                    alternate_pair_dollars=[50, 162],
                    total_stock_dates=n,
                    exact_native_average_raw_values=[average_a, average_b],
                    native_strike_raw=100 * Q,
                    conclusion="Equal products/average logs do not fix the arithmetic Asian mean or its strictly positive strike predicate. Native floor and the actual rounded coefficient were retained.",
                ),
            )
        )
    return dict(
        passed=True,
        diagnostic_families=2,
        cases=records,
        algebraically_eligible_whole_domain_predicate_proofs=0,
        conditional_single_asset_submodel_only=(
            "For a separately defined ideal single-asset positive spot, exp(log S)<H iff log S<log H; min/max of such component comparisons may be composed. This does not certify a threshold for the current quantized polynomial, ties or native clipped endpoints, and does not replace current arithmetic baskets or Asian means."
        ),
        direct_exact_log_domain_transfer_for_current_payoff_closed=True,
        universal_QSP_impossibility_claim=False,
        approximate_structured_signal_remaining_conditional=True,
        new_financial_paths_or_prices=0,
        new_circuits=0,
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    own = Path(__file__).resolve()
    seed_names = (
        "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "research/controlled_source_completion/compact_parallel_v7.py",
        "research/controlled_priority_completion/parallel_source.py",
        "research/limitation_program_20261001/baseline.py",
    )
    code = local_import_inventory([own, *(ROOT / name for name in seed_names)])
    frozen = {relative(path): sha(path) for path in code}
    inventory = []
    legacy = {
        name.replace("\\", "/"): digest for name, digest in read(ACCEPTED / "manifest.json").items()
    }
    frozen[relative(ACCEPTED / "manifest.json")] = sha(ACCEPTED / "manifest.json")
    for case, assets, dates in CASES:
        directory = ACCEPTED / case / "min-depth"
        source = read(directory / "source.json")
        paths = [
            directory / name for name in ("target.json", "source.json", "schedule_capped.json")
        ]
        paths.extend(directory / "leaves" / (key + ".json") for key in source["library_keys"])
        for path in paths:
            accepted_relative = path.relative_to(ACCEPTED).as_posix()
            assert sha(path) == legacy[accepted_relative]
            frozen[relative(path)] = sha(path)
        for path in (
            PROGRAM / "G0_run003" / (case + "_task.json"),
            PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"),
        ):
            frozen[relative(path)] = sha(path)
        inventory.append(
            dict(
                case=case,
                assets=assets,
                dates=dates,
                target=relative(directory / "target.json"),
                source=relative(directory / "source.json"),
                library_keys=source["library_keys"],
                original_contract=relative(PROGRAM / "G0_run003" / (case + "_task.json")),
            )
        )
    for directory in (PROGRAM / "G0_run003", PROGRAM / "E03_support_audit_run002"):
        assert read(directory / "summary.json")["passed"]
        for name in ("summary.json", "manifest.json", "protocol.json"):
            path = directory / name
            frozen[relative(path)] = sha(path)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_payoff_predicate_census.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_predicate_analysis=True,
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            immutable_case_inventory=inventory,
            code_dependency_inventory_count=len(code),
            complete_census_passes=1,
            at_most_algebraic_diagnostic_families=2,
            at_most_eligible_predicate_proofs=2,
            required_proof="Every exact replacement must preserve the actual entire supported domain, strict ties, guarded endpoints and native coefficients/flooring before any circuit can be emitted",
            stop_rule="If no exact one-asset financial predicate is certified, close direct exact log-domain transfer for this payoff and name the paid sum-of-exponentials/signal interface; no arithmetic-free source attempt",
            no_source_compilation=True,
            new_prices=0,
            new_gates=0,
            quantum_observations=0,
        ),
    )
    print("E22 actual payoff census source/contract inventory frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    assert protocol["before_predicate_analysis"] and protocol["complete_census_passes"] == 1
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    cases = []
    for case, assets, dates in CASES:
        census = census_case(case, assets, dates)
        save(output / (case + "_predicate_census.json"), census)
        cases.append(census)
        print(
            case,
            census["predicate_count"],
            "actual predicates classified once; no financial one-asset threshold",
            flush=True,
        )
    eligibility = algebraic_eligibility_checks(cases)
    save(output / "certificate.json", eligibility)
    save(
        output / "comparison.json",
        dict(
            cases=[
                dict(
                    case=item["case"],
                    monitored_date_basket_conditions=item["dates"],
                    stock_exponentials=item["assets"] * item["dates"],
                    predicate_category_counts=item["predicate_category_counts"],
                    eligible_one_asset_financial_predicates=0,
                    required_signal_interface=item["required_signal_interface"],
                )
                for item in cases
            ],
            accepted_target_source_unchanged=True,
            mathematical_single_asset_submodel_conditional_only=True,
            omitted_log_sum_exp_normalization_comparison_cost_allowed=False,
            complete_QSP_source_or_cost_emitted=False,
            quantum_advantage_claim=False,
        ),
    )
    verify(protocol["frozen_inputs"])
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            complete_actual_censuses=2,
            bounded_census_passes=1,
            actual_predicates_classified=sum(item["predicate_count"] for item in cases),
            monitored_sum_of_stock_barriers=64,
            actual_financial_survival_comparators=2,
            arithmetic_Asian_strike_predicates=2,
            current_stock_exponentials=464,
            eligibility_diagnostic_families=2,
            exact_eligible_whole_supported_domain_predicate_proofs=0,
            financial_predicate_circuits_emitted=0,
            accepted_source_or_contract_changed=False,
            direct_exact_log_domain_QSP_transfer_closed_for_current_payoff=True,
            sum_of_exponentials_signal_interface_required=True,
            universal_QSP_impossibility_proved=False,
            new_source_compilations=0,
            new_gates=0,
            new_prices=0,
            quantum_observations=0,
            continuous_price_or_physical_certificate=False,
            quantum_advantage_claim=False,
        ),
    )
    finish_manifest(output)
    print(
        "E22 actual payoff-predicate census PASS; direct transfer closed, arithmetic retained",
        flush=True,
    )


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


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
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    new_prices=0,
                    new_gates=0,
                    quantum_observations=0,
                ),
            )
            finish_manifest(output)
            raise
