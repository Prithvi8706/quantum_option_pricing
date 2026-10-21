"""Structural full-source binding fixtures; no path/price/gate evaluation."""

from copy import deepcopy
from unittest.mock import patch

import pytest

import research.controlled_source_completion.ir as ir
from research.limitation_program_20261001.as241_financial_target import (
    CASES,
    LAW,
    SCALAR,
    S,
    W,
    F,
    archived_semantics,
    build_financial_target,
    financial_closure,
    fingerprint,
    load_archive,
    load_scalar,
    normalized_financial,
    read,
    source_matched_ledger,
    validate_financial_binding,
)


@pytest.fixture(scope="module")
def shapes():
    def forbidden(*args, **kwargs):
        raise AssertionError("Financial splice reached a float/coefficient frontend")

    with (
        patch.multiple(ir.Graph, c=forbidden, cmul=forbidden, interpolate=forbidden, log=forbidden),
        patch.object(ir, "coefficients", forbidden),
    ):
        return {case: build_financial_target(case) for case in CASES}


def producers(target):
    return {value: node for node in target["nodes"] for value in node["out"]}


def refresh_fingerprint(target, bundle):
    """A new checksum alone cannot authorize a changed financial function."""
    bundle["target_sha256"] = fingerprint(target)
    bundle["new_source_matched_ledger"] = source_matched_ledger(bundle["case"], fingerprint(target))


@pytest.mark.parametrize("case", tuple(CASES))
def test_fixed_two_shapes_precision_and_full_source_binding(case, shapes):
    target, bundle = shapes[case]
    assets, dates = CASES[case]
    checked = validate_financial_binding(target, bundle)
    assert checked["passed"]
    assert (target["width"], target["fraction_bits"]) == (W, F)
    assert len(target["inputs"]) == len(bundle["normal_values"]) == (assets + 1) * dates
    assert len(set(target["inputs"])) == len(set(bundle["normal_values"]))
    assert checked["source_old_costs_or_Box_Muller_law_transferred"] is False


@pytest.mark.parametrize("case", tuple(CASES))
def test_actual_strict_barrier_asian_discount_and_all_stock_inventory(case, shapes):
    target, bundle = shapes[case]
    labels, nodes = bundle["semantics"], producers(target)
    assets, dates = CASES[case]
    assert all(len(row) == dates for row in labels["stock_values"])
    assert len(labels["stock_values"]) == assets
    assert nodes[labels["alive_value"]]["op"] == "lt"
    assert nodes[labels["alive_value"]]["args"] == [
        labels["maximum_basket_value"],
        labels["barrier_value"],
    ]
    assert nodes[labels["barrier_value"]]["params"]["value"] == 140 * S
    assert nodes[labels["strike_value"]]["params"]["value"] == 100 * S
    assert nodes[labels["average_value"]]["params"]["c"] == labels["average_coefficient_raw"]
    assert (
        nodes[labels["discounted_payoff_value"]]["params"]["c"]
        == labels["discount_coefficient_raw"]
    )
    assert labels["strict_barrier_equality_knockout"] is True
    assert labels["raw_prefix_multisets_checked_without_clipped_feedback"] is True


@pytest.mark.parametrize("case", tuple(CASES))
def test_uniform_inputs_have_date_major_common_and_asset_roles(case, shapes):
    target, bundle = shapes[case]
    assets, _ = CASES[case]
    rows = bundle["normal_source"]["invocations"]
    nodes = producers(target)
    for coordinate, row in enumerate(rows):
        date, role = divmod(coordinate, assets + 1)
        assert row["date_index"] == date
        assert row["role"] == ("common" if role == 0 else "idiosyncratic")
        assert row["asset_index"] == (None if role == 0 else role - 1)
        assert row["input_value"] == target["inputs"][coordinate]
        assert nodes[row["input_value"]]["params"] == {
            "name": "as241_uniform_" + str(coordinate),
            "bits": 32,
            "preparation": "uniform",
        }
        assert nodes[row["output_value"]]["op"] != "input"


@pytest.mark.parametrize("case", tuple(CASES))
def test_every_archived_financial_raw_literal_is_copied_exactly(case, shapes):
    target, bundle = shapes[case]
    old, archive = load_archive(case)
    mapping = {
        int(key): value
        for key, value in bundle["financial_normalization"]["original_to_new"].items()
    }
    actual = producers(target)
    for index in financial_closure(old, archive["normal_values"]):
        node = old["nodes"][index]
        copied = actual[mapping[node["out"][0]]]
        assert copied["op"] == node["op"] and copied["params"] == node["params"]
        assert copied["args"] == [mapping[value] for value in node["args"]]
    assert (
        archived_semantics(old, archive)["average_coefficient_raw"]
        == bundle["semantics"]["average_coefficient_raw"]
    )


@pytest.mark.parametrize("case", tuple(CASES))
def test_full_sampler_closure_contains_actual_paid_scalar_recipes(case, shapes):
    target, bundle = shapes[case]
    scalar, _ = load_scalar()
    finance = financial_closure(target, bundle["normal_values"])
    assert len(target["nodes"]) == len(bundle["normal_values"]) * len(scalar["nodes"]) + len(
        finance
    )
    assert all(
        node["params"].get("preparation") == "uniform"
        for node in target["nodes"]
        if node["op"] == "input"
    )
    assert bundle["normal_source"]["law"] == LAW
    assert bundle["full_quantum_source_compilation_or_adoption"] is False
    assert bundle["actual_source_or_estimator_gate_resources"] is None


@pytest.mark.parametrize("kind", ("date", "role", "asset", "input"))
def test_invocation_role_or_input_forgery_rejected(kind, shapes):
    target, bundle = shapes["B4x12"]
    forged = deepcopy(bundle)
    row = forged["normal_source"]["invocations"][1]
    if kind == "date":
        row["date_index"] += 1
    elif kind == "role":
        row["role"] = "common"
    elif kind == "asset":
        row["asset_index"] = 2
    else:
        row["input_value"] = target["inputs"][0]
    with pytest.raises(ValueError):
        validate_financial_binding(target, forged)


@pytest.mark.parametrize(
    "kind", ("clamp", "coefficient", "discount", "strike", "barrier", "average", "prefix")
)
def test_changed_financial_function_rejected_even_after_rehash(kind, shapes):
    target, bundle = deepcopy(shapes["B4x12"])
    labels, nodes = bundle["semantics"], producers(target)
    if kind == "clamp":
        upper = nodes[labels["clipped_log_values"][0][0]]
        nodes[upper["args"][2]]["params"]["value"] += 1
    elif kind == "coefficient":
        common = next(
            node
            for node in target["nodes"]
            if node["op"] == "cmul" and node["args"] == [bundle["normal_values"][0]]
        )
        common["params"]["c"] += 1
    elif kind == "discount":
        nodes[labels["discounted_payoff_value"]]["params"]["c"] += 1
    elif kind in ("strike", "barrier"):
        nodes[labels[kind + "_value"]]["params"]["value"] += 1
    elif kind == "average":
        nodes[labels["average_value"]]["params"]["c"] += 1
    else:
        nodes[labels["raw_log_values"][1][-1]]["args"][0] = labels["clipped_log_values"][0][0]
    refresh_fingerprint(target, bundle)
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


@pytest.mark.parametrize("kind", ("map", "semantics", "literals", "ledger"))
def test_bundle_root_map_literal_and_price_ledger_forgery_rejected(kind, shapes):
    target, bundle = shapes["B4x12"]
    bundle = deepcopy(bundle)
    if kind == "map":
        old_key = next(
            key
            for key, value in bundle["financial_normalization"]["original_to_new"].items()
            if value == bundle["semantics"]["strike_value"]
        )
        bundle["financial_normalization"]["original_to_new"][old_key] = bundle["semantics"][
            "barrier_value"
        ]
        bundle["semantics"]["strike_value"] = bundle["semantics"]["barrier_value"]
    elif kind == "semantics":
        bundle["semantics"]["stock_values"][0][0] = bundle["semantics"]["raw_log_values"][0][0]
    elif kind == "literals":
        bundle["literal_inventory"][0]["params"] = {"value": 123}
    else:
        bundle["new_source_matched_ledger"]["residual_financial_allowance_dollars_exact"] = [1, 100]
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


@pytest.mark.parametrize("kind", ("scalar_hash", "old_cost", "law"))
def test_unaccepted_source_cost_or_law_transfer_rejected(kind, shapes):
    target, bundle = shapes["B4x12"]
    bundle = deepcopy(bundle)
    if kind == "scalar_hash":
        bundle["normal_source"]["scalar_actual_source_file_sha256"] = "0" * 64
    elif kind == "old_cost":
        bundle["new_source_matched_ledger"]["source_resources"] = {"t_count": 123}
    else:
        bundle["normal_source"]["law"] = "original paired Box-Muller"
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


@pytest.mark.parametrize("kind", ("free_normal", "shared_input"))
def test_unpaid_free_normal_or_shared_uniform_source_rejected(kind, shapes):
    target, bundle = deepcopy(shapes["B4x12"])
    nodes = producers(target)
    if kind == "free_normal":
        node = nodes[bundle["normal_values"][0]]
        node.update(
            op="input", args=[], params={"name": "free_normal", "bits": 40, "preparation": "free"}
        )
        target["inputs"] = [row["out"][0] for row in target["nodes"] if row["op"] == "input"]
    else:
        second = bundle["normal_source"]["invocations"][1]
        node = next(row for row in target["nodes"] if second["input_value"] in row["args"])
        node["args"] = [
            target["inputs"][0] if value == second["input_value"] else value
            for value in node["args"]
        ]
    refresh_fingerprint(target, bundle)
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


def test_unused_or_used_native_log_table_mutation_rejected(shapes):
    target, bundle = deepcopy(shapes["B4x12"])
    name = next(iter(target["tables"]))
    target["tables"][name][0][0] += 1
    refresh_fingerprint(target, bundle)
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


def test_unaccepted_scalar_recipe_cannot_become_a_new_input_premise(shapes):
    target, bundle = shapes["B4x12"]
    scalar = read(SCALAR / "scalar_target.json")
    node = next(node for node in scalar["nodes"] if node["op"] == "const")
    node["params"]["value"] += 1
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle, scalar)


def test_extraneous_unbound_ssa_node_rejected(shapes):
    target, bundle = deepcopy(shapes["B4x12"])
    next_value = sum(len(node["out"]) for node in target["nodes"])
    target["nodes"].append(
        {"op": "const", "args": [], "out": [next_value], "params": {"value": 123}}
    )
    refresh_fingerprint(target, bundle)
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


def test_scalar_constant_cannot_replace_financial_constant_leaving_a_ghost(shapes):
    target, bundle = deepcopy(shapes["B4x12"])
    source = producers(target)
    scalar, _ = load_scalar()
    scalar_region_end = len(bundle["normal_values"]) * len(scalar["nodes"])
    scalar_zero = next(
        node["out"][0]
        for node in target["nodes"][:scalar_region_end]
        if node["op"] == "const" and node["params"]["value"] == 0
    )
    copied_zero = source[target["outputs"]["Y"]]["args"][2]
    assert scalar_zero != copied_zero
    assert source[copied_zero]["params"] == source[scalar_zero]["params"]
    for node in target["nodes"][scalar_region_end:]:
        node["args"] = [scalar_zero if value == copied_zero else value for value in node["args"]]
    mapping = bundle["financial_normalization"]["original_to_new"]
    old_zero = next(key for key, value in mapping.items() if value == copied_zero)
    mapping[old_zero] = scalar_zero
    for item in bundle["literal_inventory"]:
        item["new_outputs"] = [
            scalar_zero if value == copied_zero else value for value in item["new_outputs"]
        ]
    refresh_fingerprint(target, bundle)
    with pytest.raises(ValueError):
        validate_financial_binding(target, bundle)


@pytest.mark.parametrize("case", tuple(CASES))
def test_boundary_normalized_hash_and_exact_new_source_ledger(case, shapes):
    target, bundle = shapes[case]
    old, archive = load_archive(case)
    old_body, old_hash = normalized_financial(old, archive["normal_values"])
    new_body, new_hash = normalized_financial(target, bundle["normal_values"])
    assert old_body == new_body and old_hash == new_hash
    ledger = bundle["new_source_matched_ledger"]
    assert ledger == source_matched_ledger(case, fingerprint(target))
    assert ledger["epsilon_dollars_exact"] == [1, 100]
    assert ledger["statistical_allowance_dollars_exact"] == [9, 2000]
    assert ledger["residual_financial_allowance_dollars_exact"] == [11, 2000]
    assert ledger["source_resources"] is None and ledger["wrapper_resources"] is None
    assert ledger["accepted_joint_Box_Muller_obligation_filled"] is False
