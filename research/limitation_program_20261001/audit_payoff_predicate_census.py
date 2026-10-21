"""Independent actual-IR predicate, sum/max and native-interface reconciliation."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import shutil

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


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    receipt_dir = PROGRAM / "E22_census_run002"
    receipt = read(receipt_dir / "manifest.json")
    assert read(receipt_dir / "summary.json")["passed"]
    consumed = [receipt_dir / "manifest.json", BASELINE / "manifest.json"]
    for key, expected in receipt["files"].items():
        assert digest(ROOT / key) == expected
        consumed.append(ROOT / key)
    legacy = {
        name.replace("\\", "/"): value for name, value in read(BASELINE / "manifest.json").items()
    }
    for case in ("B4x12", "B8x52"):
        directory = BASELINE / case / "min-depth"
        source = read(directory / "source.json")
        paths = [directory / name for name in ("target.json", "source.json")]
        paths.extend(directory / "leaves" / (key + ".json") for key in source["library_keys"])
        for path in paths:
            assert digest(path) == legacy[path.relative_to(BASELINE).as_posix()]
        consumed.extend(paths)
    own = Path(__file__).resolve()
    consumed.extend(
        ROOT / "research/limitation_program_20261001" / name
        for name in (own.name, "constant_library.py", "experiment_checkpoint.py", "progress.py")
    )
    frozen = {relative(path): digest(path) for path in consumed}
    output.mkdir()
    shutil.copy2(own, output / own.name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_independent_IR_audit=True,
        frozen_inputs=frozen,
        producer_math_imported=False,
        builder_rerun=False,
        cases=["B4x12", "B8x52"],
        new_financial_prices_gates_tests=0,
        scope="Actual stored IR, complete predicate coverage, financial sums/max and native sites",
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    audits = []
    Q = 1 << 40
    for case, assets, dates in (("B4x12", 4, 12), ("B8x52", 8, 52)):
        census = read(receipt_dir / (case + "_predicate_census.json"))
        directory = BASELINE / case / "min-depth"
        target, source = read(directory / "target.json"), read(directory / "source.json")
        nodes = target["nodes"]
        owner = {value: index for index, node in enumerate(nodes) for value in node["out"]}
        assert len(owner) == source["values"]

        def node(value):
            return nodes[owner[value]]

        def const(value):
            record = node(value)
            assert record["op"] == "const"
            raw = record["params"]["value"]
            return raw - (1 << 72) if raw >= 1 << 71 else raw

        indexed = {
            index: value for index, value in enumerate(nodes) if value["op"] in ("lt", "positive")
        }
        rows = census["actual_predicate_rows"]
        assert len(rows) == len(indexed) == census["predicate_count"]
        assert len({row["node_index"] for row in rows}) == len(rows)
        by_value = {}
        noninput = [index for index, item in enumerate(nodes) if item["op"] != "input"]
        call_index = {index: call for call, index in enumerate(noninput)}
        for row in rows:
            actual = indexed[row["node_index"]]
            assert all(row[key] == actual[key] for key in ("op", "args", "out", "params"))
            assert row["call_index"] == call_index[row["node_index"]]
            assert not row["eligible_one_asset_financial_log_threshold"]
            by_value[row["out"][0]] = row["classification"]
        assert Counter(by_value.values()) == census["predicate_category_counts"]
        pairs = dates * (assets + 1) // 2
        expected = dict(
            strict_survival_of_monitored_arithmetic_baskets=1,
            maximum_tree_between_arithmetic_baskets=dates - 1,
            positive_part_of_arithmetic_Asian_strike_difference=1,
            Gaussian_log_table_argument_guard=2 * pairs,
            Gaussian_cos_table_argument_guard=4 * pairs,
            path_log_clipping_guard=2 * assets * dates,
            Gaussian_log_positive_input_guard=pairs,
            Gaussian_square_root_nonnegative_argument_guard=pairs,
        )
        assert census["predicate_category_counts"] == expected
        selections = census["actual_selection_rows"]
        actual_selects = {i: n for i, n in enumerate(nodes) if n["op"] == "select"}
        assert len(selections) == len(actual_selects)
        for row in selections:
            actual = actual_selects[row["node_index"]]
            assert row["args"] == actual["args"] and row["out"] == actual["out"]
            assert row["flag_value"] == actual["args"][0]
            assert row["flag_classification"] == by_value[row["flag_value"]]

        baskets = census["monitored_date_basket_conditions"]
        assert sorted(row["date"] for row in baskets) == list(range(dates))
        stocks = {value for row in baskets for value in row["stock_values"]}
        assert len(stocks) == assets * dates

        def terms(value):
            if value in stocks:
                return [value]
            actual = node(value)
            assert actual["op"] == "add"
            return terms(actual["args"][0]) + terms(actual["args"][1])

        for row in baskets:
            basket = node(row["basket_value"])
            assert basket["op"] == "cmul" and basket["params"]["c"] == Q // assets
            assert basket["args"] == [row["basket_sum_value"]]
            assert sorted(terms(row["basket_sum_value"])) == sorted(row["stock_values"])
            assert len(row["stock_values"]) == assets
            assert row["strict_alive"] and row["knockout_at_equality"]
            assert not row["independent_per_date_comparison_gate_emitted"]
        Y = node(target["outputs"]["Y"])
        assert Y["op"] == "select" and const(Y["args"][2]) == 0
        alive, discounted, _ = Y["args"]
        survival = node(alive)
        assert survival["op"] == "lt" and const(survival["args"][1]) == 140 * Q
        maximum_flags = []
        basket_values = {row["basket_value"] for row in baskets}

        def maxima(value):
            if value in basket_values:
                return [value]
            selected = node(value)
            assert selected["op"] == "select"
            flag, high, low = selected["args"]
            test = node(flag)
            assert test["op"] == "lt" and test["args"] == [low, high]
            maximum_flags.append(flag)
            return maxima(high) + maxima(low)

        assert sorted(maxima(survival["args"][0])) == sorted(basket_values)
        assert sorted(maximum_flags) == sorted(census["original_maximum_tree_flags"])
        discount = node(discounted)
        assert discount["op"] == "cmul"
        positive = node(discount["args"][0])
        assert positive["op"] == "positive"
        difference = node(positive["args"][0])
        assert difference["op"] == "sub" and const(difference["args"][1]) == 100 * Q
        average = node(difference["args"][0])
        assert average["op"] == "cmul"
        assert average["params"]["c"] == (Q + assets * dates // 2) // (assets * dates)
        assert sorted(terms(average["args"][0])) == sorted(stocks)
        calls = source["forward_calls"]
        covered = set()
        for interface in census["native_leaf_interfaces"]:
            metadata = read(directory / "leaves" / (interface["key"] + ".json"))
            assert metadata["sha256"] == interface["gate_sha256"]
            assert metadata["op"] == interface["op"]
            assert metadata["params"] == interface["params"]
            for site in interface["sites"]:
                index = site["call_index"]
                assert index not in covered
                covered.add(index)
                call = calls[index]
                assert call["leaf"] == interface["key"]
                assert call["args"] == site["args"] and call["out"] == site["out"]
                assert noninput[index] == site["node_index"]
        assert covered == set(range(len(calls)))
        audits.append(
            dict(
                case=case,
                predicates=len(rows),
                native_sites=len(calls),
                monitored_basket_conditions=dates,
                maximum_tree_comparisons=len(maximum_flags),
                emitted_final_survival_comparators=1,
                arithmetic_Asian_strike_positive_parts=1,
                independent_IR_and_native_site_audit_passed=True,
            )
        )
    eligibility = read(receipt_dir / "certificate.json")
    assert eligibility["algebraically_eligible_whole_domain_predicate_proofs"] == 0
    assert not eligibility["universal_QSP_impossibility_claim"]
    for record, (_, assets, dates) in zip(
        eligibility["cases"], (("B4x12", 4, 12), ("B8x52", 8, 52)), strict=True
    ):
        diagnostic = record["one_stock_threshold_diagnostic"]
        native_baskets = [
            sum(values) * Q // assets
            for values in (
                diagnostic["surviving_stock_tuple"],
                diagnostic["knocked_out_stock_tuple"],
            )
        ]
        assert native_baskets == diagnostic["exact_native_basket_raw_values"]
        assert native_baskets[0] < 140 * Q <= native_baskets[1]
        n = assets * dates
        coefficient = (Q + n // 2) // n
        asian = record["arithmetic_Asian_log_average_diagnostic"]
        averages = [90 * n * coefficient, 106 * n * coefficient]
        assert averages == asian["exact_native_average_raw_values"]
        assert averages[0] < 100 * Q < averages[1]
        assert 50 * 162 == 90**2
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=audits,
            all_3106_predicates_reconciled=True,
            interface_diagnostics_are_not_reachable_path_impossibility_proofs=True,
            exact_financial_log_domain_replacement_theorems=0,
            new_financial_prices_gates_tests=0,
        ),
    )
    manifest(output, protocol)
    print("Independent E22 IR/native-site audit passed; no exact predicate transfer", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
