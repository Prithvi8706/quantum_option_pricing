"""Source-compatible logical hardware demand and whole-price fault targets.

Counts reuse independently audited native leaf scans and terminal IQFT tokens.
No code cycles, physical clocks, memory exposure or executable latency are
inferred from logical T depth. A finite protected implementation remains open.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from research.limitation_program_20261001.checkpoint_circuit import fingerprint


FORMAT = "source-compatible-complete-price-hardware-demand-v1"
ELEMENTARY_GATES = ("x", "cx", "h", "t", "s", "z", "cz")
PHYSICAL_ALLOWANCE = Fraction(3, 1000)
ALLOCATIONS = {
    "data": Fraction(1, 1000),
    "magic_states": Fraction(1, 1000),
    "control": Fraction(1, 1000),
}
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    if isinstance(value, (float, bool)):
        raise ValueError("Exact rational hardware parameter required")
    if isinstance(value, (list, tuple)):
        if len(value) != 2 or any(type(item) is not int for item in value) or value[1] <= 0:
            raise ValueError("Exact rational hardware parameter required")
        return Fraction(*value)
    if not isinstance(value, (int, Fraction, str)):
        raise ValueError("Exact rational hardware parameter required")
    return Fraction(value)


def _integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("Nonnegative exact integer demand required")
    return value


def expanded_native_counts(resources):
    """Exact seven-T/six-CX/two-H substitution, with no CCX double count."""
    x, cx, ccx = (_integer(resources[name]) for name in ("x", "cx", "ccx"))
    literal_h, cz, z = (_integer(resources.get(name, 0)) for name in ("h", "cz", "z"))
    expected = {
        "source_gates": x + cx + ccx + literal_h + cz + z,
        "t_count": 7 * ccx,
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": literal_h + 2 * ccx,
    }
    if any(resources[name] != count for name, count in expected.items()):
        raise ValueError("Audited native decomposition/count identity changed")
    if resources.get("clifford_cz", cz) != cz or resources.get("clifford_z", z) != z:
        raise ValueError("Audited phase gate count changed")
    return {
        "x": x,
        "cx": cx + 6 * ccx,
        "h": literal_h + 2 * ccx,
        "t": 7 * ccx,
        "s": 0,
        "z": z,
        "cz": cz,
    }


def iqft_token_counts(operations, control_wires):
    """Read actual terminal gate tokens; SWAP has exactly three logical CXs."""
    allowed = set(control_wires)
    if len(allowed) != len(control_wires) or any(
        type(wire) is not int or wire < 0 for wire in allowed
    ):
        raise ValueError("Distinct allocated IQFT controls required")
    raw, expanded = Counter(), Counter({name: 0 for name in ELEMENTARY_GATES})
    for operation in operations:
        gate, wires = operation["gate"], operation["wires"]
        arity = 2 if gate in ("cx", "cz", "swap") else 1
        if gate not in (*ELEMENTARY_GATES, "tdg", "sdg", "swap"):
            raise ValueError("Unsupported terminal IQFT primitive")
        if len(wires) != arity or len(set(wires)) != arity or not set(wires) <= allowed:
            raise ValueError("IQFT primitive aliases or leaves its QPE register")
        raw[gate] += 1
        if gate == "swap":
            expanded["cx"] += 3
        else:
            expanded[{"tdg": "t", "sdg": "s"}.get(gate, gate)] += 1
    return dict(raw), dict(expanded)


def source_batch_profile(wrapper, source, capped, metadata):
    """Native interfaces, compact copies and simultaneous private demand per batch."""
    if wrapper["source_fingerprint"] != fingerprint(source) or wrapper[
        "capped_fingerprint"
    ] != fingerprint(capped):
        raise ValueError("Demand binds a different financial source/schedule")
    widths, offsets = capped["widths"], capped["offsets"]
    if len(widths) != source["values"] or len(offsets) != len(widths):
        raise ValueError("Compact source allocation changed")
    cursor = 0
    for width, offset in zip(widths, offsets, strict=True):
        if _integer(width, 1) > source["word_width"] or offset != cursor:
            raise ValueError("Compact SSA native width/allocation changed")
        cursor += width
    if cursor != capped["retained_ssa_qubits"]:
        raise ValueError("Compact retained SSA width changed")
    private_base = cursor + len(source["outputs"]) * source["word_width"]
    q = wrapper["resources"]["logical_qubits"]
    if q != capped["resources"]["logical_qubits"] or wrapper["private_base"] != private_base:
        raise ValueError("Original source private bank/allocation changed")
    if len(wrapper["financial_batches"]) != len(capped["groups"]):
        raise ValueError("Financial batch coverage changed")
    available = {value for node in source["inputs"] for value in node["out"]}
    seen, batches, totals = set(), [], Counter()
    for batch_index, (batch, group) in enumerate(
        zip(wrapper["financial_batches"], capped["groups"], strict=True)
    ):
        if (
            batch["wave"] != group["wave"]
            or [record["call_index"] for record in batch["calls"]] != group["call_indices"]
        ):
            raise ValueError("Original financial batch order changed")
        copies, call_records, output_values = 0, [], set()
        components = Counter()
        resources = {"forward": Counter(), "inverse": Counter()}
        native_t_depths, native_ct_depths = (
            {"forward": [], "inverse": []},
            {"forward": [], "inverse": []},
        )
        cursor = private_base
        fanout = Counter()
        for record in batch["calls"]:
            index = record["call_index"]
            if index in seen or not 0 <= index < len(source["forward_calls"]):
                raise ValueError("Financial call duplicated or out of range")
            call = source["forward_calls"][index]
            entry = metadata[call["leaf"]]
            if record["leaf"] != call["leaf"] or any(
                value not in available for value in call["args"]
            ):
                raise ValueError("Financial predecessor/control binding changed")
            if len(call["args"]) != len(entry["args"]) or len(call["out"]) != len(entry["outs"]):
                raise ValueError("Native interface arity changed")
            interface = [wire for register in entry["args"] + entry["outs"] for wire in register]
            native_q = entry["resources"]["qubits"]
            if len(interface) != len(set(interface)) or any(
                not 0 <= wire < native_q for wire in interface
            ):
                raise ValueError("Native interface aliases or leaves allocated leaf")
            active_outputs = sum(widths[value] for value in call["out"])
            input_width = sum(len(register) for register in entry["args"])
            native_output_width = sum(len(register) for register in entry["outs"])
            native_internal = native_q - input_width - native_output_width
            if native_internal < 0 or any(
                widths[value] > len(register)
                for value, register in zip(
                    call["args"] + call["out"], entry["args"] + entry["outs"], strict=True
                )
            ):
                raise ValueError("Native full register footprint changed")
            private = native_q - active_outputs
            if record["private_base"] != cursor or record["private_width"] != private:
                raise ValueError("Paid native private/high-output scratch changed")
            cursor += private
            if (
                cursor > q
                or output_values.intersection(call["out"])
                or set(call["out"]).intersection(available)
            ):
                raise ValueError("Financial output/private allocation collision")
            active_args = sum(widths[value] for value in call["args"])
            copies += 2 * active_args
            fanout.update(call["args"])
            output_values.update(call["out"])
            components.update(
                {
                    "private_qubits": private,
                    "native_input_copy_register_qubits": input_width,
                    "native_internal_scratch_qubits": native_internal,
                    "unused_native_high_output_scratch_qubits": native_output_width
                    - active_outputs,
                    "active_output_qubits": active_outputs,
                    "active_argument_copy_bits": active_args,
                    "native_leaf_qubits": native_q,
                }
            )
            costs = wrapper["financial_native_costs"][call["leaf"]]
            for direction in ("forward", "inverse"):
                expanded_native_counts(costs[direction])
                for field in COUNT_FIELDS:
                    resources[direction][field] += costs[direction][field]
                native_t_depths[direction].append(costs[direction]["t_depth"])
                native_ct_depths[direction].append(costs[direction]["clifford_t_depth"])
            if any(costs["forward"][field] != entry["resources"][field] for field in COUNT_FIELDS):
                raise ValueError("Audited native metadata/count identity changed")
            call_records.append(
                {
                    "call_index": index,
                    "leaf": call["leaf"],
                    "private_qubits": private,
                    "native_full_input_qubits": input_width,
                    "active_argument_copy_bits": active_args,
                    "active_output_qubits": active_outputs,
                    "unused_native_high_output_scratch_qubits": native_output_width
                    - active_outputs,
                }
            )
            seen.add(index)
        if not call_records:
            raise ValueError("Empty financial demand batch")
        copy_rounds = max(fanout.values(), default=0)
        if copy_rounds != group["copy_rounds"] or copy_rounds != batch["copy_rounds"]:
            raise ValueError("Shared/repeated SSA argument fanout rounds changed")
        if components["private_qubits"] != group["private_scratch_qubits"]:
            raise ValueError("Joint native batch private footprint changed")
        for direction in ("forward", "inverse"):
            for field in ("source_gates", "cx", "clifford_cx"):
                resources[direction][field] += copies
            resources[direction]["t_depth"] = max(native_t_depths[direction])
            resources[direction]["clifford_t_depth"] = (
                max(native_ct_depths[direction]) + 2 * copy_rounds
            )
            totals.update(resources[direction])
        batches.append(
            {
                "batch": batch_index,
                "wave": batch["wave"],
                "call_count": len(call_records),
                "calls": call_records,
                "components": dict(components),
                "argument_copy_CX_per_direction": copies,
                "max_shared_SSA_argument_occurrences": copy_rounds,
                "max_shared_SSA_copy_target_bits": max(
                    (multiplicity * widths[value] for value, multiplicity in fanout.items()),
                    default=0,
                ),
                "shared_SSA_argument_occurrences": {
                    str(value): count for value, count in sorted(fanout.items())
                },
                "resources": {direction: dict(cost) for direction, cost in resources.items()},
            }
        )
        available.update(output_values)
    if (
        seen != set(range(len(source["forward_calls"])))
        or dict(totals) != wrapper["financial_resources"]
    ):
        raise ValueError("Financial batch counts do not reconcile to the audited iterate")
    max_private = max(batch["components"]["private_qubits"] for batch in batches)
    if private_base + max_private != q:
        raise ValueError("Financial source private peak does not reproduce allocation")
    maxima = {}
    for name, metric in (
        ("native_call_count", lambda batch: batch["call_count"]),
        ("joint_private_qubits", lambda batch: batch["components"]["private_qubits"]),
        ("forward_T_states", lambda batch: batch["resources"]["forward"]["t_count"]),
        ("copy_CX_per_direction", lambda batch: batch["argument_copy_CX_per_direction"]),
        ("SSA_fanout_occurrences", lambda batch: batch["max_shared_SSA_argument_occurrences"]),
        ("SSA_fanout_copy_target_bits", lambda batch: batch["max_shared_SSA_copy_target_bits"]),
    ):
        maximum = max(metric(batch) for batch in batches)
        maxima[name] = {
            "value": maximum,
            "batches": [batch["batch"] for batch in batches if metric(batch) == maximum],
        }
    return {
        "batches": batches,
        "batch_count_per_financial_direction": len(batches),
        "retained_SSA_qubits": capped["retained_ssa_qubits"],
        "named_output_buffer_qubits_reused_by_estimator": len(source["outputs"])
        * source["word_width"],
        "max_simultaneous_native_private_qubits": max_private,
        "compiled_logical_qubits": q,
        "compiler_qubit_cap": capped["qubit_cap"],
        "maxima": maxima,
        "financial_resources_per_iterate": dict(totals),
        "native_counts_basis": (
            "Immutable native arrays previously scanned and independently audited; "
            "no financial replay"
        ),
        "routing_gate_count": None,
        "physical_memory_exposure_code_cycles": None,
    }


def complete_price_demand(wrapper, synthesized_row, iqft_operations, batch_profile):
    Q, shots = (
        _integer(synthesized_row[name], 1) for name in ("financial_forwards", "serial_shots")
    )
    if (
        synthesized_row["binding"] != wrapper["binding"]
        or synthesized_row["source_iterate_resources"] != wrapper["resources"]
    ):
        raise ValueError("Synthesized estimator and financial iterate binding changed")
    if (
        synthesized_row["source_graph_directions"] != 2 * Q
        or synthesized_row["financial_literal_inverses"] != Q
        or any(
            synthesized_row[name] != Q
            for name in (
                "selector_forwards",
                "selector_literal_inverses",
                "controlled_predicate_CZ",
                "controlled_signed_reflections",
            )
        )
    ):
        raise ValueError("Full financial invocation multiplicities changed")
    unit = expanded_native_counts(wrapper["resources"])
    raw_iqft, iqft = iqft_token_counts(iqft_operations, synthesized_row["qpe_register_wires"])
    if raw_iqft != synthesized_row["iqft_per_shot_physical_gate_counts"]:
        raise ValueError("Actual terminal IQFT token counts changed")
    gates = Counter({name: Q * count for name, count in unit.items()})
    for name, count in iqft.items():
        gates[name] += shots * count
    fresh_h = shots * (len(wrapper["random_wires"]) + len(synthesized_row["qpe_register_wires"]))
    gates["h"] += fresh_h
    if gates["t"] != synthesized_row["full_T_count"]:
        raise ValueError("Complete price T-state demand disagrees with synthesized ledger")
    elementary = sum(gates.values())
    if (
        elementary == 0
        or batch_profile["compiled_logical_qubits"] != synthesized_row["logical_qubits"]
    ):
        raise ValueError("Complete estimator elementary work or memory footprint changed")
    native_ccx = Q * wrapper["resources"]["ccx"]
    remaining_single_t = gates["t"] - 7 * native_ccx
    if remaining_single_t < 0:
        raise ValueError("Arithmetic CCX and terminal rotation demand overlap")
    selector_resources = Counter()
    for direction in ("forward", "inverse"):
        selector_resources.update(wrapper["selector_costs"][direction])
    marker = {
        "source_gates": 1,
        "x": 0,
        "cx": 0,
        "ccx": 0,
        "t_count": 0,
        "clifford_cx": 0,
        "clifford_h": 0,
        "cz": 1,
    }
    unit_stages = {
        "financial_source_and_literal_inverse": expanded_native_counts(
            batch_profile["financial_resources_per_iterate"]
        ),
        "selector_and_literal_inverse": expanded_native_counts(selector_resources),
        "signed_uniform_reflection": expanded_native_counts(wrapper["reflection_resources"]),
        "controlled_predicate_marker": expanded_native_counts(marker),
    }
    stage_sum = Counter()
    for counts in unit_stages.values():
        stage_sum.update(counts)
    if dict(stage_sum) != unit:
        raise ValueError("Financial/selector/reflection/marker component counts do not reconcile")
    per_price_stages = {
        name: {gate: Q * count for gate, count in counts.items()}
        for name, counts in unit_stages.items()
    }
    per_price_stages["fresh_uniform_and_QPE_preparation"] = {
        name: fresh_h if name == "h" else 0 for name in ELEMENTARY_GATES
    }
    per_price_stages["complete_terminal_IQFT"] = {
        name: shots * count for name, count in iqft.items()
    }
    requirements = {
        "physical_failure_allowance_exact": pair(PHYSICAL_ALLOWANCE),
        "allocation_exact": {name: pair(value) for name, value in ALLOCATIONS.items()},
        "required_error_per_consumed_T_state_exact": pair(ALLOCATIONS["magic_states"] / gates["t"]),
        "required_data_error_per_elementary_logical_gate_exact": pair(
            ALLOCATIONS["data"] / elementary
        ),
        "required_control_error_per_elementary_logical_operation_exact": pair(
            ALLOCATIONS["control"] / elementary
        ),
        "known_elementary_gate_opportunity_count": elementary,
        "known_consumed_T_state_opportunity_count": gates["t"],
        "idle_or_code_cycle_opportunity_count": None,
        "physical_control_reset_feedback_opportunity_count": None,
        "known_gate_union_targets_cover_idle_and_feedback": False,
        "dependence_assumption": (
            "Union bound requires marginal bounds; independence is not assumed"
        ),
        "code_distance": None,
        "complete_execution_failure_upper": None,
        "published_factory_reliability_transferred": False,
    }
    return {
        "format": FORMAT,
        "case": wrapper["binding"]["case"],
        "binding": wrapper["binding"],
        "controlled_G_iterations": Q,
        "financial_graph_directions": 2 * Q,
        "financial_batches_executed": 2 * Q * batch_profile["batch_count_per_financial_direction"],
        "serial_fresh_shots": shots,
        "primitive_elementary_gate_counts": dict(gates),
        "primitive_elementary_gate_counts_by_stage": per_price_stages,
        "primitive_elementary_gate_count": elementary,
        "consumed_T_states": gates["t"],
        "native_CCX_positions_before_exact_seven_T_expansion": native_ccx,
        "remaining_single_qubit_T_positions_in_terminal_IQFT": remaining_single_t,
        "native_CCZ_factory_replacement_compiled": False,
        "fresh_uniform_and_QPE_preparation_H": fresh_h,
        "financial_argument_copy_CX_per_price": 2
        * Q
        * sum(batch["argument_copy_CX_per_direction"] for batch in batch_profile["batches"]),
        "full_terminal_IQFT_tokens_per_shot": raw_iqft,
        "expanded_terminal_IQFT_gates_per_shot": iqft,
        "full_logical_serial_T_depth": synthesized_row["full_T_depth"],
        "full_logical_Clifford_T_depth_upper": synthesized_row["full_known_clifford_t_depth_upper"],
        "measurement_reaction_depth": None,
        "logical_qubits": synthesized_row["logical_qubits"],
        "source_batch_profile": batch_profile,
        "failure_requirements": requirements,
        "physical_qubit_cap": None,
        "architecture_rows": [],
        "runtime_bottleneck_lower_bound_seconds": None,
        "complete_executable_latency_seconds": None,
        "full_physical_fidelity_certificate": False,
        "full_continuous_price_certificate": False,
        "no_archived_C4_H8_physical_cap_or_clock_transferred": True,
        "new_financial_gate_replays": 0,
        "new_financial_price_samples": 0,
        "missing_bounds_are_zero": False,
    }


def bottleneck_lower_bound(
    demand,
    reaction_depth=None,
    reaction_seconds=None,
    delivered_T_states_per_second=None,
    routing_seconds=None,
    other_dependency_seconds=None,
):
    """Conditional max bound; even every populated term gives no executable schedule."""
    if (reaction_depth is None) != (reaction_seconds is None):
        raise ValueError("Reaction depth and matching latency must be provided together")
    reaction = None
    if reaction_depth is not None:
        latency = exact(reaction_seconds)
        if latency <= 0:
            raise ValueError("Positive matched reaction latency required")
        reaction = _integer(reaction_depth) * latency
    supply = None
    if delivered_T_states_per_second is not None:
        rate = exact(delivered_T_states_per_second)
        if rate <= 0:
            raise ValueError("Positive delivered protected-state rate required")
        supply = Fraction(demand["consumed_T_states"], 1) / rate
    terms = {"reaction": reaction, "supply": supply}
    for name, parameter in (
        ("routing", routing_seconds),
        ("other_dependencies", other_dependency_seconds),
    ):
        value = exact(parameter) if parameter is not None else None
        if value is not None and value < 0:
            raise ValueError("Nonnegative dependency bound required")
        terms[name] = value
    known = [value for value in terms.values() if value is not None]
    return {
        "conditional_terms_seconds_exact": {
            name: pair(value) if value is not None else None for name, value in terms.items()
        },
        "lower_bound_seconds_exact": pair(max(known)) if known else None,
        "all_parameters_supplied": len(known) == len(terms),
        "bound_is_an_executable_latency": False,
        "executable_latency_seconds": None,
        "physical_footprint_routing_protection_certificate": None,
        "state_rate_scope": (
            "delivered accepted protected T states, including retries and routing; "
            "no free initial stock granted"
        ),
    }


def assess_error_proposal(demand, per_state_error, per_gate_data_error, per_gate_control_error):
    """Necessary certificate interface; unknown idle/control exposure prevents admission."""
    values = [
        exact(value) for value in (per_state_error, per_gate_data_error, per_gate_control_error)
    ]
    if any(not 0 <= value <= 1 for value in values):
        raise ValueError("Marginal probability bound outside [0,1]")
    opportunities = [
        demand["consumed_T_states"],
        demand["primitive_elementary_gate_count"],
        demand["primitive_elementary_gate_count"],
    ]
    names = ("magic_states", "data", "control")
    bounds = {
        name: value * count for name, value, count in zip(names, values, opportunities, strict=True)
    }
    passes = {name: bound <= ALLOCATIONS[name] for name, bound in bounds.items()}
    return {
        "known_operation_union_bounds_exact": {name: pair(bound) for name, bound in bounds.items()},
        "known_operation_certificate_condition_passes": passes,
        "hardware_admitted": False if not all(passes.values()) else None,
        "idle_code_cycles_and_control_feedback_remain_unproved": True,
        "failed_sufficient_union_condition_proves_actual_failure": False,
        "physical_runtime_certified": False,
    }
