"""Splice independent scalar AS241 SSA invocations into archived B4/B8 finance.

No graph is constructed on import. Original financial operations and every raw
literal are copied verbatim; the old paired Box-Muller subgraph is not adopted.
"""

from collections import Counter
from copy import deepcopy
from research.limitation_program_20261001.scalar_quantile_ir import (
    ROOT,
    PROGRAM,
    S,
    W,
    F,
    fingerprint,
    read,
)
from research.limitation_program_20261001.scalar_quantile_source import digest


CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
PAIR = PROGRAM / "C06_pair_run001"
SUPPORT = PROGRAM / "E03_support_run001"
SCALAR = PROGRAM / "A02_quantile_scalar_run001"
LAW = "independent q32 midpoint inputs, mathematical-native signed-restored AS241"


def load_scalar(target=None, bindings=None):
    """Only the accepted actual scalar receipt may supply normal producers."""
    summary = read(SCALAR / "summary.json")
    if (
        summary.get("passed") is not True
        or summary.get("budget_censored") is not False
        or summary.get("actual_scalar_clean_XOR_source_emitted") is not True
    ):
        raise ValueError("Uncensored successful actual scalar source required")
    accepted = read(SCALAR / "scalar_target.json")
    accepted_bindings = read(SCALAR / "semantic_bindings.json")
    if target is not None and target != accepted:
        raise ValueError("Supplied scalar SSA differs from the accepted actual source")
    if bindings is not None and bindings != accepted_bindings:
        raise ValueError("Supplied scalar semantic binding differs from the accepted receipt")
    validate_ssa(accepted)
    if (
        (accepted["width"], accepted["fraction_bits"]) != (W, F)
        or accepted["outputs"] != {"Z": accepted_bindings["output"]}
        or len(accepted["inputs"]) != 1
    ):
        raise ValueError("Accepted actual one-input scalar SSA source required")
    input_node = next(node for node in accepted["nodes"] if node["op"] == "input")
    if input_node["params"] != {"name": "k", "bits": 32, "preparation": "uniform"}:
        raise ValueError("Actual independent uniform q32 scalar interface required")
    return deepcopy(accepted), deepcopy(accepted_bindings)


def load_archive(case):
    if case not in CASES:
        raise ValueError("Exactly original B4x12/B8x52 contracts required")
    binding = read(PAIR / "certificate.json")["source_bindings"][case]
    target_path = ROOT / binding["target"].replace("\\", "/")
    if digest(target_path) != binding["target_sha256"]:
        raise ValueError("Archived financial target differs from audited normal boundary binding")
    target = read(target_path)
    source_path = target_path.parent / "source.json"
    source = read(source_path)
    support_path = SUPPORT / (case + "_certificate.json")
    support = read(support_path)
    assets, dates = CASES[case]
    normals = binding["normal_values"]
    if (
        (target["width"], target["fraction_bits"]) != (W, F)
        or len(normals) != (assets + 1) * dates
        or len(set(normals)) != len(normals)
        or support["assets"] != assets
        or support["dates"] != dates
        or support["target_output"] != target["outputs"]
        or support.get("complete_builder_equality") is not True
    ):
        raise ValueError("Original financial precision/shape/support binding differs")
    noninputs = [node for node in target["nodes"] if node["op"] != "input"]
    if (
        len(noninputs) != len(source["forward_calls"])
        or any(
            (node["args"], node["out"]) != (call["args"], call["out"])
            for node, call in zip(noninputs, source["forward_calls"], strict=True)
        )
        or source["outputs"] != target["outputs"]
        or source["word_width"] != W
        or source["fraction_bits"] != F
    ):
        raise ValueError("Accepted A10 financial target/source invocation schema differs")
    return target, {
        "case": case,
        "assets": assets,
        "dates": dates,
        "normal_values": list(normals),
        "support": support,
        "accepted_target": str(target_path.relative_to(ROOT)).replace("\\", "/"),
        "accepted_target_sha256": digest(target_path),
        "accepted_source": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "accepted_source_sha256": digest(source_path),
        "normal_boundary_receipt": str(PAIR.relative_to(ROOT)).replace("\\", "/"),
        "support_receipt": str(SUPPORT.relative_to(ROOT)).replace("\\", "/"),
        "original_builder": "research/advantage_frontier_20260923/barrier_oracle_depth.py",
        "original_builder_sha256": digest(
            ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
        ),
    }


def validate_ssa(target):
    known = set()
    for node in target["nodes"]:
        if any(value not in known for value in node["args"]):
            raise ValueError("SSA forward reference or unknown operand")
        if node["out"] != list(range(len(known), len(known) + len(node["out"]))):
            raise ValueError("Contiguous fresh SSA outputs required")
        known.update(node["out"])
    if target["inputs"] != [node["out"][0] for node in target["nodes"] if node["op"] == "input"]:
        raise ValueError("Actual SSA input registry differs")
    if any(value not in known for value in target["outputs"].values()):
        raise ValueError("Unproduced named output")


def financial_closure(target, normals):
    producers = {
        value: index for index, node in enumerate(target["nodes"]) for value in node["out"]
    }
    stop, seen, used = set(normals), set(), set()
    stack = list(target["outputs"].values())
    while stack:
        value = stack.pop()
        if value in stop:
            used.add(value)
            continue
        index = producers[value]
        if index in seen:
            continue
        node = target["nodes"][index]
        if node["op"] == "input":
            raise ValueError("Financial closure reaches an uncut old uniform/free-normal input")
        seen.add(index)
        stack.extend(node["args"])
    if used != stop:
        raise ValueError("All original common/idiosyncratic normal boundaries must be used")
    return sorted(seen)


def normalized_financial(target, normals):
    """Boundary-aware full closure hash, retaining op order, arity and raw params."""
    tokens = {value: fingerprint(["normal_boundary", index]) for index, value in enumerate(normals)}
    records = []
    for index in financial_closure(target, normals):
        node = target["nodes"][index]
        record = {
            "op": node["op"],
            "args": [tokens[value] for value in node["args"]],
            "params": deepcopy(node["params"]),
            "outputs": len(node["out"]),
        }
        if node["op"] == "lookup":
            record["table_sha256"] = fingerprint(target["tables"][node["params"]["table"]])
        base = fingerprint(record)
        for slot, value in enumerate(node["out"]):
            tokens[value] = fingerprint([base, slot])
        records.append(record)
    body = {
        "width": target["width"],
        "fraction_bits": target["fraction_bits"],
        "normal_count": len(normals),
        "nodes": records,
        "outputs": {name: tokens[value] for name, value in target["outputs"].items()},
    }
    return body, fingerprint(body)


def _leaves(producers, value, stop, maximum=False):
    result, stack = [], [value]
    while stack:
        current = stack.pop()
        if current in stop:
            result.append(current)
            continue
        node = producers[current]
        if not maximum and node["op"] == "add":
            stack.extend(node["args"])
            continue
        if maximum and node["op"] == "select":
            flag, high, low = node["args"]
            comparison = producers[flag]
            if comparison["op"] == "lt" and comparison["args"] == [low, high]:
                stack.extend((low, high))
                continue
        raise ValueError("Actual financial addition/maximum tree differs from archived contract")
    return Counter(result)


def archived_semantics(target, archive):
    """Inventory raw roots and literals using audited labels; no numeric frontend."""
    assets, dates = archive["assets"], archive["dates"]
    support, normals = archive["support"], archive["normal_values"]
    producers = {value: node for node in target["nodes"] for value in node["out"]}
    closure = financial_closure(target, normals)
    nodes = [target["nodes"][index] for index in closure]
    if (
        len(support["stock_ids"]) != assets * dates
        or len(support["clipped_log_ids"]) != assets * dates
    ):
        raise ValueError("Every original stock/clip site must be inventoried")
    stocks = [support["stock_ids"][asset * dates : (asset + 1) * dates] for asset in range(assets)]
    clipped = [
        support["clipped_log_ids"][asset * dates : (asset + 1) * dates] for asset in range(assets)
    ]
    raw_logs, lower_words, upper_words = [], set(), set()
    for row in clipped:
        raw_row = []
        for value in row:
            upper = producers[value]
            if upper["op"] != "select":
                raise ValueError("Original upper stock clamp must be an actual selection")
            flag, inner, high = upper["args"]
            if producers[flag]["op"] != "lt" or producers[flag]["args"] != [inner, high]:
                raise ValueError("Original upper stock clamp predicate changed")
            lower = producers[inner]
            if lower["op"] != "select":
                raise ValueError("Original lower stock clamp must be an actual selection")
            flag, low, raw = lower["args"]
            if producers[flag]["op"] != "lt" or producers[flag]["args"] != [raw, low]:
                raise ValueError("Original lower stock clamp predicate changed")
            if producers[low]["op"] != "const" or producers[high]["op"] != "const":
                raise ValueError("Original raw clamp literals required")
            lower_words.add(producers[low]["params"]["value"])
            upper_words.add(producers[high]["params"]["value"])
            raw_row.append(raw)
        raw_logs.append(raw_row)
    if len(lower_words) != 1 or len(upper_words) != 1:
        raise ValueError("All original stock clamp literals must agree")

    def unique(predicate, label):
        matching = [node for node in nodes if predicate(node)]
        if len(matching) != 1:
            raise ValueError("Unique actual financial producer required: " + label)
        return matching[0]

    increments, common_coefficients, idio_coefficients, drift_words = [], [], [], []
    for date in range(dates):
        common = unique(
            lambda n: n["op"] == "cmul" and n["args"] == [normals[date * (assets + 1)]], "common"
        )
        row, idio_row = [], []
        for asset in range(assets):
            idio = unique(
                lambda n: (
                    n["op"] == "cmul" and n["args"] == [normals[date * (assets + 1) + asset + 1]]
                ),
                "idio",
            )
            noise = unique(
                lambda n: n["op"] == "add" and set(n["args"]) == {common["out"][0], idio["out"][0]},
                "noise",
            )
            increment = unique(
                lambda n: (
                    n["op"] == "add"
                    and noise["out"][0] in n["args"]
                    and any(producers[arg]["op"] == "const" for arg in n["args"])
                ),
                "drift increment",
            )
            fixed = next(arg for arg in increment["args"] if producers[arg]["op"] == "const")
            drift_words.append(producers[fixed]["params"]["value"])
            row.append(increment["out"][0])
            idio_row.append(idio["params"]["c"])
        increments.append(row)
        common_coefficients.append(common["params"]["c"])
        idio_coefficients.append(idio_row)
    initial_words, initial_values = set(), set()
    for asset in range(assets):
        first = producers[raw_logs[asset][0]]
        if first["op"] != "add" or increments[0][asset] not in first["args"]:
            raise ValueError("Initial spot must be added to first raw increment")
        fixed = next(arg for arg in first["args"] if arg != increments[0][asset])
        if producers[fixed]["op"] != "const":
            raise ValueError("Original initial log-spot literal required")
        initial_values.add(fixed)
        initial_words.add(producers[fixed]["params"]["value"])
        for date in range(dates):
            stop = {fixed, *(increments[j][asset] for j in range(date + 1))}
            if _leaves(producers, raw_logs[asset][date], stop) != Counter(
                {value: 1 for value in stop}
            ):
                raise ValueError(
                    "Raw-prefix dependency multiset changed or clipped state was reused"
                )
    if len(initial_words) != 1 or len(initial_values) != 1:
        raise ValueError("Original common initial log-spot literal required")
    baskets = []
    for date in range(dates):
        roots = {stocks[asset][date] for asset in range(assets)}
        matching = []
        for node in nodes:
            if node["op"] == "cmul" and node["params"]["c"] == S // assets:
                try:
                    if _leaves(producers, node["args"][0], roots) == Counter(
                        {value: 1 for value in roots}
                    ):
                        matching.append(node["out"][0])
                except ValueError:
                    pass
        if len(matching) != 1:
            raise ValueError("Exact original power-of-two basket producer required")
        baskets.append(matching[0])
    output = producers[target["outputs"]["Y"]]
    if output["op"] != "select":
        raise ValueError("Original financial output must retain alive/payoff/zero selection")
    alive, payoff, zero = output["args"]
    if producers[zero]["op"] != "const" or producers[zero]["params"]["value"] != 0:
        raise ValueError("Original financial dead output must be zero")
    alive_node, payoff_node = producers[alive], producers[payoff]
    if alive_node["op"] != "lt" or payoff_node["op"] != "cmul":
        raise ValueError("Original strict barrier/discount structure changed")
    maximum, barrier = alive_node["args"]
    if _leaves(producers, maximum, set(baskets), maximum=True) != Counter(
        {value: 1 for value in baskets}
    ):
        raise ValueError("Original all-date barrier maximum differs")
    if producers[barrier]["op"] != "const" or producers[barrier]["params"]["value"] != 140 * S:
        raise ValueError("Original exact barrier140 required")
    positive = producers[payoff_node["args"][0]]
    if positive["op"] != "positive":
        raise ValueError("Original Asian payoff must retain positive part")
    difference = producers[positive["args"][0]]
    if difference["op"] != "sub":
        raise ValueError("Original strike subtraction required")
    average, strike = difference["args"]
    if producers[strike]["op"] != "const" or producers[strike]["params"]["value"] != 100 * S:
        raise ValueError("Original exact strike100 required")
    avg_node = producers[average]
    if avg_node["op"] != "cmul":
        raise ValueError("Original rounded Asian mean coefficient required")
    all_stocks = {value for row in stocks for value in row}
    if _leaves(producers, avg_node["args"][0], all_stocks) != Counter(
        {value: 1 for value in all_stocks}
    ):
        raise ValueError("Original all-asset/date Asian stock sum changed")
    if (
        avg_node["params"]["c"] != support["average_coefficient"]
        or payoff_node["params"]["c"] != support["discount_coefficient"]
    ):
        raise ValueError("Archived actual Asian/discount coefficient differs from support binding")
    return {
        "raw_log_values": raw_logs,
        "clipped_log_values": clipped,
        "stock_values": stocks,
        "basket_values": baskets,
        "increment_values_by_date_asset": increments,
        "initial_log_value": next(iter(initial_values)),
        "initial_log_raw": next(iter(initial_words)),
        "lower_log_raw": next(iter(lower_words)),
        "upper_log_raw": next(iter(upper_words)),
        "common_coefficients_raw_by_date": common_coefficients,
        "idiosyncratic_coefficients_raw_by_date_asset": idio_coefficients,
        "drift_literals_raw_by_date_asset": [
            drift_words[j * assets : (j + 1) * assets] for j in range(dates)
        ],
        "basket_coefficient_raw": S // assets,
        "average_coefficient_raw": avg_node["params"]["c"],
        "discount_coefficient_raw": payoff_node["params"]["c"],
        "average_value": average,
        "asian_stock_sum_value": avg_node["args"][0],
        "alive_value": alive,
        "maximum_basket_value": maximum,
        "positive_payoff_value": positive["out"][0],
        "discounted_payoff_value": payoff,
        "output_value": target["outputs"]["Y"],
        "barrier_value": barrier,
        "strike_value": strike,
        "native_exp_inverse_ln2_raw": support["literal_inverse_ln2"],
        "native_exp_ln2_raw": support["literal_ln2"],
        "native_exp_coefficients_raw": support["literal_exp_coefficients"],
        "strict_barrier_equality_knockout": True,
        "raw_prefix_multisets_checked_without_clipped_feedback": True,
    }


VALUE_FIELDS = {
    "raw_log_values",
    "clipped_log_values",
    "stock_values",
    "basket_values",
    "increment_values_by_date_asset",
    "initial_log_value",
    "average_value",
    "asian_stock_sum_value",
    "alive_value",
    "maximum_basket_value",
    "positive_payoff_value",
    "discounted_payoff_value",
    "output_value",
    "barrier_value",
    "strike_value",
}


def _mapped(value, mapping):
    return [_mapped(item, mapping) for item in value] if isinstance(value, list) else mapping[value]


def source_matched_ledger(case, target_hash):
    return {
        "schema": "new-AS241-source-matched-price-prerequisites-v1",
        "case": case,
        "source_target_sha256": target_hash,
        "law": LAW,
        "epsilon_dollars_exact": [1, 100],
        "statistical_allowance_dollars_exact": [9, 2000],
        "residual_financial_allowance_dollars_exact": [11, 2000],
        "actual_statistical_error_bound": None,
        "actual_financial_bias_bound": None,
        "actual_source_gate_resources": None,
        "actual_wrapper_gate_resources": None,
        "source_resources": None,
        "wrapper_resources": None,
        "actual_full_estimator_gate_resources": None,
        "physical_runtime_or_failure_bound": None,
        "old_E02_source_costs_transferred": False,
        "old_E02_source_or_wrapper_costs_transferred": False,
        "old_joint_Box_Muller_ledger_obligation_filled": False,
        "accepted_joint_Box_Muller_obligation_filled": False,
        "new_financial_sampler_or_complete_price_adopted": False,
        "full_G2_or_quantum_advantage_established": False,
    }


def build_financial_target(case, scalar_target=None, scalar_bindings=None):
    """Deferred exact archive splice; no old builder/frontend regeneration."""
    old, archive = load_archive(case)
    scalar_target, scalar_bindings = load_scalar(scalar_target, scalar_bindings)
    old_semantics = archived_semantics(old, archive)
    nodes, inputs, normals, invocations, mapping = [], [], [], [], {}
    scalar_values = sum(len(node["out"]) for node in scalar_target["nodes"])
    for coordinate, old_normal in enumerate(archive["normal_values"]):
        offset = coordinate * scalar_values
        local = {value: offset + value for value in range(scalar_values)}
        name = "as241_uniform_" + str(coordinate)
        for node in scalar_target["nodes"]:
            new = deepcopy(node)
            new["args"] = [local[value] for value in node["args"]]
            new["out"] = [local[value] for value in node["out"]]
            if new["op"] == "input":
                new["params"]["name"] = name
                inputs.append(new["out"][0])
            nodes.append(new)
        normal = local[scalar_bindings["output"]]
        mapping[old_normal] = normal
        normals.append(normal)
        date, role = divmod(coordinate, archive["assets"] + 1)
        invocations.append(
            {
                "coordinate": coordinate,
                "date_index": date,
                "role": "common" if role == 0 else "idiosyncratic",
                "asset_index": None if role == 0 else role - 1,
                "input_name": name,
                "input_value": local[scalar_target["inputs"][0]],
                "output_value": normal,
                "value_offset": offset,
                "scalar_values": scalar_values,
            }
        )
    next_value = len(invocations) * scalar_values
    financial_indices = financial_closure(old, archive["normal_values"])
    for index in financial_indices:
        node = old["nodes"][index]
        new = deepcopy(node)
        new["args"] = [mapping[value] for value in node["args"]]
        new["out"] = []
        for value in node["out"]:
            mapping[value] = next_value
            new["out"].append(next_value)
            next_value += 1
        nodes.append(new)
    tables = deepcopy(scalar_target["tables"])
    for index in financial_indices:
        node = old["nodes"][index]
        if node["op"] == "lookup":
            name = node["params"]["table"]
            if name in tables and tables[name] != old["tables"][name]:
                raise ValueError("Archive/scalar table name collision changes native literals")
            tables[name] = deepcopy(old["tables"][name])
    target = {
        "format": old["format"],
        "width": W,
        "fraction_bits": F,
        "nodes": nodes,
        "inputs": inputs,
        "outputs": {name: mapping[value] for name, value in old["outputs"].items()},
        "tables": tables,
        "semantics": old["semantics"],
    }
    validate_ssa(target)
    old_normalized, old_hash = normalized_financial(old, archive["normal_values"])
    new_normalized, new_hash = normalized_financial(target, normals)
    if old_normalized != new_normalized or old_hash != new_hash:
        raise ValueError("New sampler changed the normalized original financial subgraph")
    semantics = {
        name: _mapped(value, mapping) if name in VALUE_FIELDS else value
        for name, value in old_semantics.items()
    }
    target_hash = fingerprint(target)
    bundle = {
        "schema": "as241-financial-target-bundle-v1",
        "case": case,
        "assets": archive["assets"],
        "dates": archive["dates"],
        "width": W,
        "fraction_bits": F,
        "uniform_bits_each": 32,
        "target_sha256": target_hash,
        "normal_values": normals,
        "normal_source": {
            "law": LAW,
            "scalar_receipt": str(SCALAR.relative_to(ROOT)).replace("\\", "/"),
            "scalar_target_sha256": fingerprint(scalar_target),
            "scalar_target_file_sha256": digest(SCALAR / "scalar_target.json"),
            "scalar_bindings_file_sha256": digest(SCALAR / "semantic_bindings.json"),
            "scalar_proofs_file_sha256": digest(SCALAR / "new_site_proofs.json"),
            "scalar_actual_source": str(
                (SCALAR / "candidate64/source.json").relative_to(ROOT)
            ).replace("\\", "/"),
            "scalar_actual_source_file_sha256": digest(SCALAR / "candidate64/source.json"),
            "input_names": [row["input_name"] for row in invocations],
            "invocations": invocations,
        },
        "financial_normalization": {
            **{
                name: value
                for name, value in archive.items()
                if name not in ("normal_values", "support")
            },
            "original_boundary_values": archive["normal_values"],
            "original_to_new": {str(key): value for key, value in mapping.items()},
            "normalized_equality": True,
            "normalized_closure_sha256": old_hash,
            "actual_scalar_producers_not_free_normals": True,
            "all_financial_ops_and_raw_params_preserved": True,
            "old_Box_Muller_law_or_source_hash_transferred": False,
        },
        "semantics": semantics,
        "literal_inventory": [
            {
                "original_node_index": index,
                "op": old["nodes"][index]["op"],
                "params": deepcopy(old["nodes"][index]["params"]),
                "new_outputs": [mapping[value] for value in old["nodes"][index]["out"]],
            }
            for index in financial_indices
            if old["nodes"][index]["params"]
        ],
        "new_source_matched_ledger": source_matched_ledger(case, target_hash),
        "full_quantum_source_compilation_or_adoption": False,
        "actual_source_or_estimator_gate_resources": None,
    }
    validate_financial_binding(target, bundle, scalar_target)
    return target, bundle


def validate_financial_binding(target, bundle, scalar_target=None):
    """Check actual independent scalar producers AND boundary-normalized finance."""
    scalar_target, scalar_bindings = load_scalar(scalar_target)
    validate_ssa(target)
    old, archive = load_archive(bundle["case"])
    assets, dates = CASES[bundle["case"]]
    if (
        bundle.get("schema") != "as241-financial-target-bundle-v1"
        or (
            bundle["assets"],
            bundle["dates"],
            bundle["width"],
            bundle["fraction_bits"],
            bundle["uniform_bits_each"],
        )
        != (assets, dates, W, F, 32)
        or target["format"] != old["format"]
        or target["semantics"] != old["semantics"]
        or (target["width"], target["fraction_bits"]) != (W, F)
    ):
        raise ValueError("Original financial format/precision and new bundle shape required")
    normal_source = bundle["normal_source"]
    scalar_identity = {
        "law": LAW,
        "scalar_receipt": str(SCALAR.relative_to(ROOT)).replace("\\", "/"),
        "scalar_target_sha256": fingerprint(scalar_target),
        "scalar_target_file_sha256": digest(SCALAR / "scalar_target.json"),
        "scalar_bindings_file_sha256": digest(SCALAR / "semantic_bindings.json"),
        "scalar_proofs_file_sha256": digest(SCALAR / "new_site_proofs.json"),
        "scalar_actual_source": str((SCALAR / "candidate64/source.json").relative_to(ROOT)).replace(
            "\\", "/"
        ),
        "scalar_actual_source_file_sha256": digest(SCALAR / "candidate64/source.json"),
    }
    if bundle["target_sha256"] != fingerprint(target) or any(
        normal_source.get(key) != value for key, value in scalar_identity.items()
    ):
        raise ValueError("New full source or scalar source fingerprint differs")
    scalar_values = sum(len(node["out"]) for node in scalar_target["nodes"])
    if len(bundle["normal_values"]) != len(archive["normal_values"]):
        raise ValueError("Actual original driver count must be preserved")
    nodes_by_output = {node["out"][0]: node for node in target["nodes"]}
    seen_inputs, outputs = [], []
    for coordinate, invocation in enumerate(bundle["normal_source"]["invocations"]):
        offset = coordinate * scalar_values
        if invocation["coordinate"] != coordinate or invocation["value_offset"] != offset:
            raise ValueError("Independent scalar invocation offsets differ")
        name = "as241_uniform_" + str(coordinate)
        date, role = divmod(coordinate, assets + 1)
        expected_invocation = {
            "coordinate": coordinate,
            "date_index": date,
            "role": "common" if role == 0 else "idiosyncratic",
            "asset_index": None if role == 0 else role - 1,
            "input_name": name,
            "input_value": offset + scalar_target["inputs"][0],
            "output_value": offset + scalar_bindings["output"],
            "value_offset": offset,
            "scalar_values": scalar_values,
        }
        if invocation != expected_invocation:
            raise ValueError("Date/common/asset scalar invocation binding differs")
        for local in scalar_target["nodes"]:
            expected = deepcopy(local)
            expected["args"] = [offset + value for value in local["args"]]
            expected["out"] = [offset + value for value in local["out"]]
            if expected["op"] == "input":
                expected["params"]["name"] = name
                seen_inputs.append(expected["out"][0])
            if nodes_by_output.get(expected["out"][0]) != expected:
                raise ValueError(
                    "Actual new scalar producer differs from accepted scalar SSA recipe"
                )
        output = offset + scalar_target["outputs"]["Z"]
        if invocation["output_value"] != output or invocation["input_name"] != name:
            raise ValueError("Scalar normal producer/name mapping differs")
        outputs.append(output)
    if (
        outputs != bundle["normal_values"]
        or seen_inputs != target["inputs"]
        or len(set(seen_inputs)) != len(seen_inputs)
        or normal_source["input_names"] != ["as241_uniform_" + str(j) for j in range(len(outputs))]
    ):
        raise ValueError("Every actual scalar normal requires its own uniform q32 input")
    old_normalized, old_hash = normalized_financial(old, archive["normal_values"])
    new_normalized, new_hash = normalized_financial(target, outputs)
    normalization = bundle["financial_normalization"]
    archive_identity = {
        key: value for key, value in archive.items() if key not in ("normal_values", "support")
    }
    if (
        old_normalized != new_normalized
        or old_hash != new_hash
        or normalization.get("normalized_equality") is not True
        or normalization["normalized_closure_sha256"] != old_hash
        or normalization["original_boundary_values"] != archive["normal_values"]
        or normalization["accepted_target_sha256"] != archive["accepted_target_sha256"]
        or normalization["accepted_source_sha256"] != archive["accepted_source_sha256"]
        or any(normalization.get(key) != value for key, value in archive_identity.items())
    ):
        raise ValueError("Full boundary-normalized financial source equality is unproved")
    # Reconstruct the actual correspondence; a forged label map cannot authorize
    # different semantic IDs even when an attacker changes the bundle with it.
    old_indices = financial_closure(old, archive["normal_values"])
    new_indices = financial_closure(target, outputs)
    scalar_region_nodes = len(outputs) * len(scalar_target["nodes"])
    if new_indices != list(range(scalar_region_nodes, len(target["nodes"]))):
        raise ValueError("Financial closure must be exactly the appended disjoint finance region")
    if len(target["nodes"]) != len(outputs) * len(scalar_target["nodes"]) + len(old_indices):
        raise ValueError("Uncharged or unbound additional full-target SSA nodes")
    expected_mapping = dict(zip(archive["normal_values"], outputs, strict=True))
    for old_index, new_index in zip(old_indices, new_indices, strict=True):
        old_node, new_node = old["nodes"][old_index], target["nodes"][new_index]
        if (
            new_node["op"] != old_node["op"]
            or new_node["params"] != old_node["params"]
            or new_node["args"] != [expected_mapping[value] for value in old_node["args"]]
            or len(new_node["out"]) != len(old_node["out"])
        ):
            raise ValueError("Actual financial node correspondence differs")
        expected_mapping.update(zip(old_node["out"], new_node["out"], strict=True))
    mapping = {int(key): value for key, value in normalization["original_to_new"].items()}
    if mapping != expected_mapping:
        raise ValueError("Provided financial label map differs from actual node correspondence")
    expected_literals = [
        {
            "original_node_index": index,
            "op": old["nodes"][index]["op"],
            "params": deepcopy(old["nodes"][index]["params"]),
            "new_outputs": [mapping[value] for value in old["nodes"][index]["out"]],
        }
        for index in old_indices
        if old["nodes"][index]["params"]
    ]
    if bundle["literal_inventory"] != expected_literals:
        raise ValueError("Complete archived financial literal inventory differs")
    expected_tables = deepcopy(scalar_target["tables"])
    for index in old_indices:
        node = old["nodes"][index]
        if node["op"] == "lookup":
            expected_tables[node["params"]["table"]] = old["tables"][node["params"]["table"]]
    if target["tables"] != expected_tables:
        raise ValueError("Actual frozen scalar/financial lookup tables differ")
    if (
        normalization.get("actual_scalar_producers_not_free_normals") is not True
        or normalization.get("all_financial_ops_and_raw_params_preserved") is not True
        or normalization.get("old_Box_Muller_law_or_source_hash_transferred") is not False
        or bundle.get("full_quantum_source_compilation_or_adoption") is not False
        or bundle.get("actual_source_or_estimator_gate_resources") is not None
    ):
        raise ValueError("New source prerequisite claims cannot adopt old cost/law resources")
    semantics = archived_semantics(old, archive)
    expected_semantics = {
        name: _mapped(value, mapping) if name in VALUE_FIELDS else value
        for name, value in semantics.items()
    }
    if bundle["semantics"] != expected_semantics:
        raise ValueError(
            "Actual new financial semantic roots/literals differ from original archive"
        )
    if bundle["new_source_matched_ledger"] != source_matched_ledger(
        bundle["case"], fingerprint(target)
    ):
        raise ValueError("Exact new-source1/100,9/2000,11/2000 ledger binding differs")
    return {
        "passed": True,
        "target_sha256": fingerprint(target),
        "normalized_financial_closure_sha256": new_hash,
        "independent_uniform_normal_producers": len(outputs),
        "source_old_costs_or_Box_Muller_law_transferred": False,
    }
