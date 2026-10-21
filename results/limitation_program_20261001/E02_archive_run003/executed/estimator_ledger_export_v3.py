"""Expand immutable archived estimator recipes without transferring their contract.

This is a count and binding audit. It never executes, changes, or resynthesizes
the archived financial circuits. Saved leaf resource certificates supply the
native costs; their gate arrays are identified, not replayed or rescanned here.
"""

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ARCHIVE = "results/controlled_priority_completion/combined_estimators.json"
SELECTOR = "results/controlled_priority_completion/estimator_bounded_selector.json"
SELECTED_ROWS = (
    ("C4", "hadamard", "continuous_moment_conditional"),
    ("H8", "hadamard", "continuous_moment_conditional"),
    ("C4", "bounded_QAE", "unconditional_digital_support"),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, name, minimum=0):
    require(type(value) is int and value >= minimum, f"Invalid integer {name}")
    return value


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_json_sha256(path):
    """Historical range_audit hashes sorted JSON, not the serialized file bytes."""
    return hashlib.sha256(json.dumps(read(path), sort_keys=True).encode()).hexdigest()


def local_path(root, relative):
    root = Path(root).resolve()
    path = (root / str(relative).replace("\\", "/")).resolve()
    require(path.is_relative_to(root), f"Nonlocal dependency: {relative}")
    require(path.is_file(), f"Missing dependency: {relative}")
    return path


def selected_rows(archive):
    rows = []
    for identity in SELECTED_ROWS:
        matches = [
            row for row in archive["rows"] if (row["model"], row["method"], row["mode"]) == identity
        ]
        require(len(matches) == 1, f"Ambiguous archive row: {identity}")
        rows.append(matches[0])
    return rows


def discover_archive_inputs(root, archive_path=ARCHIVE):
    """Structural dependency inventory, suitable for a prospective freeze."""
    root = Path(root).resolve()
    archive_file = local_path(root, archive_path)
    archive = read(archive_file)
    paths = {archive_file, local_path(root, SELECTOR)}
    paths.update(local_path(root, archive[key]) for key in ("cost_artifact", "synthesis_library"))
    for row in selected_rows(archive):
        wrapper_file = local_path(root, row["wrapper"])
        paths.update((wrapper_file, local_path(root, row["allocation_source"])))
        for operation in read(wrapper_file)["operations"]:
            if operation["gate"] != "call_wave_half":
                continue
            source_file = local_path(root, operation["manifest"])
            schedule_file = local_path(root, operation["wave_schedule"])
            source, schedule = read(source_file), read(schedule_file)
            paths.update((source_file, schedule_file))
            library = source.get("library_workspace_relative", source["library"])
            for key in source["library_keys"]:
                paths.add(local_path(root, f"{library}/{key}.json"))
            if "range_certificate" in schedule:
                paths.add(local_path(root, schedule["range_certificate"]))
                paths.add(local_path(root, source_file.parent / "target.json"))
    return sorted(paths)


def expand_hadamard(allocation):
    stages = allocation["stages"]
    require(bool(stages), "Empty Hadamard schedule")
    expanded = []
    for position, stage in enumerate(stages):
        require(stage["stage"] == position, "Hadamard stage order")
        power = integer(stage["T"], "Hadamard power", 1)
        repetitions = integer(stage["repetitions"], "Hadamard repetitions", 1)
        count = power * repetitions
        require(stage["controlled_U_calls"] == count, "Hadamard stage multiplicity")
        expanded.append(dict(stage=position, power=power, repetitions=repetitions, calls=count))
    calls = sum(stage["calls"] for stage in expanded)
    preparations = sum(stage["repetitions"] for stage in expanded)
    longest = max(stage["power"] for stage in expanded)
    require(calls == allocation["controlled_U_calls"], "Hadamard total multiplicity")
    require(preparations == allocation["hadamard_test_executions"], "Hadamard preparation total")
    require(longest == allocation["longest_single_chain"], "Hadamard longest chain")
    return dict(
        controlled_wrapper_calls=calls,
        fresh_preparations=preparations,
        longest_wrapper_chain=longest,
        repetitions_by_stage=expanded,
        adaptive_stages=len(stages),
        between_stage_feedback_dependencies=len(stages) - 1,
        measured_bits=preparations,
        qpe_bits=0,
        qpe_executions=0,
        iqft_gate_counts={},
        iqft_exact_T_count=0,
        iqft_exact_T_depth_serial=0,
        iqft_synthesis_usage={},
    )


def expected_iqft(controls):
    operations = [
        dict(gate="swap", wires=[controls[j], controls[-j - 1]]) for j in range(len(controls) // 2)
    ]
    for j, target in enumerate(controls):
        for k in range(j):
            operations.append(
                dict(gate="cp", wires=[controls[k], target], angle_pi=[-1, 1 << (j - k)])
            )
        operations.append(dict(gate="h", wires=[target]))
    return operations


def phase_synthesis_key(operation, angle_kind):
    angle = Fraction(*operation[f"angle_{angle_kind}"])
    require(angle != 0, "Zero controlled phase is outside archived recipe")
    half = angle / 2
    key = (
        f"{'radian' if angle_kind == 'radians' else 'pi'}_{abs(half).numerator}_{half.denominator}"
    )
    require(operation.get("synthesis_key") == key, "Controlled phase synthesis key")
    require(operation.get("half_angle_sign") == (1 if half > 0 else -1), "Phase sign")
    return key


def expand_qpe(allocation, controller, controls):
    bits = integer(allocation["qpe_bits"], "QPE bits", 1)
    repetitions = integer(allocation["repetitions"], "QPE repetitions", 1)
    require(repetitions % 2 == 1, "Median repetition count must be odd")
    require(len(controls) == bits and len(set(controls)) == bits, "QPE control register")
    require(allocation["M"] == 1 << bits, "QPE M/register mismatch")
    powers = controller["powers"]
    expected = [
        dict(control=wire, repetitions_of_wrapper=1 << j) for j, wire in enumerate(controls)
    ]
    require(powers == expected, "QPE powers do not match actual control convention")
    require(controller["repetitions"] == repetitions, "QPE controller repetitions")
    calls_per_preparation = sum(
        integer(p["repetitions_of_wrapper"], "QPE power", 1) for p in powers
    )
    calls = repetitions * calls_per_preparation
    require(calls == allocation["controlled_grover_calls"], "QPE controlled-call total")
    operations = controller["IQFT_operations"]
    require(len(operations) == len(expected_iqft(controls)), "IQFT operation count")
    synthesis = Counter()
    exact_cp = 0
    for operation, expected_op in zip(operations, expected_iqft(controls)):
        require(all(operation.get(k) == v for k, v in expected_op.items()), "IQFT gate order/angle")
        require(
            set(operation)
            <= set(expected_op) | {"synthesis_key", "half_angle_sign", "exact_T_count"},
            "Uncharged IQFT metadata",
        )
        if operation["gate"] != "cp":
            require(set(operation) == set(expected_op), "Unexpected IQFT phase metadata")
            continue
        if abs(Fraction(*operation["angle_pi"]) / 2) == Fraction(1, 4):
            require(operation.get("exact_T_count") == 3, "IQFT exact pi/2 controlled phase")
            require("synthesis_key" not in operation, "Exact phase charged twice")
            exact_cp += 1
        else:
            require("exact_T_count" not in operation, "Synthesized phase charged twice")
            synthesis[phase_synthesis_key(operation, "pi")] += 3 * repetitions
    counts = Counter(operation["gate"] for operation in operations)
    return dict(
        controlled_wrapper_calls=calls,
        fresh_preparations=repetitions,
        longest_wrapper_chain=calls_per_preparation,
        largest_controlled_power=max(p["repetitions_of_wrapper"] for p in powers),
        repetitions=repetitions,
        powers_per_preparation=powers,
        adaptive_stages=0,
        between_stage_feedback_dependencies=0,
        measured_bits=bits * repetitions,
        qpe_bits=bits,
        qpe_executions=repetitions,
        iqft_gate_counts={key: value * repetitions for key, value in counts.items()},
        iqft_exact_controlled_phases=exact_cp * repetitions,
        iqft_exact_T_count=3 * exact_cp * repetitions,
        iqft_exact_T_depth_serial=2 * exact_cp * repetitions,
        iqft_synthesis_usage=dict(synthesis),
    )


def audit_reflection(operations, random_wires):
    require(
        len(random_wires) >= 2 and len(set(random_wires)) == len(random_wires),
        "Reflection random register",
    )
    n = len(random_wires)
    prefix = [dict(gate="h", wires=[wire]) for wire in random_wires]
    prefix += [dict(gate="x", wires=[wire]) for wire in random_wires]
    require(len(operations) >= 2 * n + 1, "Truncated reflection")
    require(operations[: 2 * n] == prefix, "Reflection preparation order")
    first = operations[2 * n]
    require(
        first["gate"] == "ccx" and first["wires"][:2] == random_wires[:2], "Reflection ladder start"
    )
    scratch = integer(first["wires"][2], "Reflection scratch")
    require(
        set(range(scratch, scratch + n - 1)).isdisjoint(random_wires), "Reflection scratch alias"
    )
    ladder = [first]
    ladder += [
        dict(gate="ccx", wires=[scratch + j - 2, random_wires[j], scratch + j - 1])
        for j in range(2, n)
    ]
    expected = prefix + ladder + [dict(gate="cz", wires=[scratch + n - 2, "control"])]
    expected += list(reversed(ladder))
    expected += [dict(gate="x", wires=[wire]) for wire in random_wires]
    expected += [dict(gate="h", wires=[wire]) for wire in random_wires]
    expected += [dict(gate="z", wires=["control"])]
    require(operations == expected, "Reflection inverse or controlled relative sign")
    return dict(
        ccx=2 * (n - 1),
        h=2 * n,
        x=2 * n,
        cz=1,
        control_z=1,
        scratch=scratch,
        scratch_qubits=n - 1,
        T_count=14 * (n - 1),
        T_depth_serial_upper=12 * (n - 1),
        depth_semantics=(
            "Archived conservative six T layers per serial CCX; not an optimized depth or duration."
        ),
    )


def random_input_wires(source):
    """Only uniform inputs are H-prepared; provided/classical inputs are charged elsewhere."""
    result = []
    width = integer(source["word_width"], "Preparation native width", 1)
    for node in source["inputs"]:
        preparation = node["params"].get("preparation", "uniform")
        require(preparation in ("uniform", "provided", "classical"), "Unknown input preparation")
        if preparation == "uniform":
            result.extend(node["out"][0] * width + j for j in range(node["params"]["bits"]))
    return result


def audit_wave(root, operation):
    source_path = local_path(root, operation["manifest"])
    schedule_path = local_path(root, operation["wave_schedule"])
    source, schedule = read(source_path), read(schedule_path)
    source_hash, schedule_hash = sha256(source_path), sha256(schedule_path)
    require(schedule["source_sha256"] == source_hash, "Wave source binding")
    if "source_manifest_sha256" in operation:
        require(operation["source_manifest_sha256"] == source_hash, "Wrapper source binding")
        require(operation["wave_schedule_sha256"] == schedule_hash, "Wrapper schedule binding")
    width = integer(source["word_width"], "Native width", 1)
    library = source.get("library_workspace_relative", source["library"])
    metadata = {
        key: read(local_path(root, f"{library}/{key}.json")) for key in source["library_keys"]
    }
    calls = source["forward_calls"]
    known = {value for node in source["inputs"] for value in node["out"]}
    visited = set()
    half = Counter()
    bindings = []
    for key, entry in metadata.items():
        resources = entry["resources"]
        require(resources["t_count"] == 7 * resources["ccx"], "Native seven-T certificate")
        require(
            resources["source_gates"] == resources["x"] + resources["cx"] + resources["ccx"],
            "Native source gate inventory",
        )
        bindings.append(
            dict(
                leaf=key,
                metadata=f"{library}/{key}.json".replace("\\", "/"),
                gate_sha256=entry["sha256"],
            )
        )
    max_private = 0
    for group in schedule["groups"]:
        indices = group["call_indices"]
        require(bool(indices), "Empty native wave batch")
        batch_outputs = set()
        arguments = Counter()
        private, td, ct = 0, 0, 0
        for index in indices:
            integer(index, "Native call index")
            require(index < len(calls) and index not in visited, "Duplicate/invalid native call")
            visited.add(index)
            call = calls[index]
            require(all(arg in known for arg in call["args"]), "Native wave dependency")
            require(not (set(call["out"]) & (known | batch_outputs)), "Native SSA output alias")
            require(len(set(call["out"])) == len(call["out"]), "Native atomic output duplicate")
            batch_outputs.update(call["out"])
            arguments.update(call["args"])
            entry = metadata[call["leaf"]]
            require(
                len(entry["args"]) == len(call["args"]) and len(entry["outs"]) == len(call["out"]),
                "Native arity",
            )
            resources = entry["resources"]
            input_copies = 2 * len(call["args"]) * width
            require(call["argument_copy_cx"] == input_copies, "Native argument copy charge")
            private += resources["qubits"] - len(call["out"]) * width
            td, ct = max(td, resources["t_depth"]), max(ct, resources["clifford_t_depth"])
            for key in ("t_count", "ccx", "x", "cx", "source_gates", "clifford_cx", "clifford_h"):
                half[key] += resources[key]
            for key in ("cx", "source_gates", "clifford_cx"):
                half[key] += input_copies
        copy_rounds = max(arguments.values(), default=0)
        require(group["private_scratch_qubits"] == private, "Native private allocation")
        require(group["copy_rounds"] == copy_rounds, "Native shared input copy rounds")
        require(
            group["t_depth"] == td and group["clifford_t_depth"] == ct + 2 * copy_rounds,
            "Native wave depth certificate",
        )
        half["t_depth"] += td
        half["clifford_t_depth"] += ct + 2 * copy_rounds
        max_private = max(max_private, private)
        known.update(batch_outputs)
    require(visited == set(range(len(calls))), "Incomplete native wave schedule")
    outputs = source["outputs"]
    require(all(value in known for value in outputs.values()), "Undefined native output")
    resources = schedule["resources"]
    output_bits = len(outputs) * width
    for key in ("t_count", "ccx", "x", "cx", "source_gates", "clifford_cx", "clifford_h"):
        extra_copy = output_bits if key in ("cx", "source_gates", "clifford_cx") else 0
        require(resources[key] == 2 * half[key] + extra_copy, f"Full clean schedule {key}")
    require(resources["t_depth"] == 2 * half["t_depth"], "Full clean schedule T depth")
    output_rounds = max(Counter(outputs.values()).values(), default=0)
    require(
        resources["clifford_t_depth"] == 2 * half["clifford_t_depth"] + output_rounds,
        "Full clean schedule Clifford depth",
    )
    require(
        resources["logical_qubits"] == (source["values"] + len(outputs)) * width + max_private,
        "Full clean allocation",
    )
    random = random_input_wires(source)
    require(resources["random_hadamards"] == len(random), "Random preparation width")
    support, range_binding = None, None
    if "range_certificate" in schedule:
        certificate_path = local_path(root, schedule["range_certificate"])
        certificate = read(certificate_path)
        require(
            sha256(certificate_path) == schedule["range_certificate_sha256"],
            "Archived range binding",
        )
        target_path = local_path(root, source_path.parent / "target.json")
        require(
            canonical_json_sha256(target_path) == certificate["target_sha256"],
            "Archived range target binding",
        )
        range_binding = dict(
            certificate=schedule["range_certificate"],
            certificate_sha256=schedule["range_certificate_sha256"],
            target=target_path.relative_to(Path(root).resolve()).as_posix(),
            target_file_sha256=sha256(target_path),
            target_semantic_sha256=certificate["target_sha256"],
            target_semantic_serialization="json.dumps(parsed_target, sort_keys=True).encode()",
        )
        require(read(target_path)["outputs"] == outputs, "Archived range output identity")
        require(
            certificate["guaranteed"] is True and certificate["signed_overflow_sites"] == [],
            "Archived no-overflow support",
        )
        require(
            certificate["fraction_bits"] == source["fraction_bits"]
            and certificate["width"] == width,
            "Archived range precision",
        )
        support = {name: certificate["bounds"][str(value)] for name, value in outputs.items()}
    return dict(
        manifest=operation["manifest"],
        source_sha256=source_hash,
        wave_schedule=operation["wave_schedule"],
        schedule_sha256=schedule_hash,
        source=source,
        half_resources=dict(half),
        logical_qubits=resources["logical_qubits"],
        random_wires=random,
        raw_output_support=support,
        range_binding=range_binding,
        native_gate_bindings=bindings,
        native_gate_bytes_replayed=False,
    )


def audit_wrapper(root, wrapper, method):
    operations = wrapper["operations"]
    limit = integer(wrapper["qpe_register_base"], "Wrapper internal wire limit", 1)
    for operation in operations:
        wires = operation.get("wires", [])
        require(len(wires) == len(set(wires)), "Wrapper gate wire alias")
        require(
            all(w == "control" or (type(w) is int and 0 <= w < limit) for w in wires),
            "Wrapper gate wire bound",
        )
    indices = [j for j, op in enumerate(operations) if op["gate"] == "call_wave_half"]
    require(len(indices) == (4 if method == "hadamard" else 2), "Wrapper graph invocation count")
    require(indices[0] == 0, "Wrapper starts before financial compute")
    calls = [operations[j] for j in indices]
    for forward, inverse in zip(calls[: len(calls) // 2], reversed(calls[len(calls) // 2 :])):
        require(
            forward["inverse"] is False and inverse["inverse"] is True,
            "Wrapper compute/erase directions",
        )
        require(
            {k: v for k, v in forward.items() if k != "inverse"}
            == {k: v for k, v in inverse.items() if k != "inverse"},
            "Wrapper compute/erase bindings",
        )
    financial = audit_wave(root, calls[0])
    require(
        calls[0]["base"] == 0 and financial["source"]["outputs"].keys() == {"Y_6"},
        "Archived residual source identity",
    )
    source = financial["source"]
    require(
        source["word_width"] == 72 and source["fraction_bits"] == 40,
        "Archived financial native contract",
    )
    phase, selector, phase_usage = None, None, Counter()
    if method == "hadamard":
        require(wrapper["fused_compute_phase_uncompute"] is True, "Archived fused phase contract")
        phase = audit_wave(root, calls[1])
        require(calls[1]["base"] == financial["logical_qubits"], "Phase private address binding")
        psource = phase["source"]
        base, pw = calls[1]["base"], psource["word_width"]
        require(pw == 96 and psource["fraction_bits"] == 64, "Archived phase precision")
        pinputs = {node["params"]["name"]: base + node["out"][0] * pw for node in psource["inputs"]}
        require(wrapper["phase_classical_input_width"] == pw, "Phase constant width")
        require(
            wrapper["phase_classical_input_offsets"]
            == {key: pinputs[key] for key in ("left", "scale_exponent")},
            "Phase constant addresses",
        )
        shift = psource["fraction_bits"] - source["fraction_bits"]
        y_offset = source["outputs"]["Y_6"] * source["word_width"]
        copies = [
            dict(gate="cx", wires=[y_offset + j, pinputs["Y"] + shift + j])
            for j in range(source["word_width"])
        ]
        require(
            operations[1 : indices[1]] == copies
            and operations[indices[2] + 1 : indices[3]] == list(reversed(copies)),
            "Financial phase copies/uncopies",
        )
        phase_output = base + next(iter(psource["outputs"].values())) * pw
        phases = operations[indices[1] + 1 : indices[2]]
        require(len(phases) == psource["fraction_bits"] + 3, "Phase bit enumeration")
        for j, operation in enumerate(phases):
            angle = Fraction(-1 if j == psource["fraction_bits"] + 2 else 1) * Fraction(2) ** (
                j - psource["fraction_bits"]
            )
            require(
                operation["gate"] == "cp" and operation["wires"] == ["control", phase_output + j],
                "Phase control/output binding",
            )
            require(Fraction(*operation["angle_radians"]) == angle, "Signed phase bit angle")
            phase_usage[phase_synthesis_key(operation, "radians")] += 3
        random_wires = financial["random_wires"]
        scratch = base + phase["logical_qubits"]
    else:
        require(
            wrapper["source_manifest_sha256"] == financial["source_sha256"],
            "Bounded wrapper source binding",
        )
        selector_record = read(local_path(root, SELECTOR))
        require(
            selector_record["word_width"] == 72 and selector_record["fraction_bits"] == 40,
            "Archived selector precision",
        )
        mapping = wrapper["selector_wire_mapping"]
        sq = selector_record["resources"]["qubits"]
        y_offset = source["outputs"]["Y_6"] * source["word_width"]
        expected_mapping = [
            y_offset + j if j < 72 else financial["logical_qubits"] + j - 72 for j in range(sq)
        ]
        require(mapping == expected_mapping, "Selector source/private binding")
        emitted = [
            dict(gate=("x", "cx", "ccx")[len(gate) - 1], wires=[mapping[wire] for wire in gate])
            for gate in selector_record["emitted_gate_records"]
        ]
        marker = dict(gate="cz", wires=["control", mapping[selector_record["outputs"][0]]])
        require(
            operations[1 : indices[1]] == emitted + [marker] + list(reversed(emitted)),
            "Selector literal inverse/phase binding",
        )
        counts = Counter(op["gate"] for op in emitted)
        sr = selector_record["resources"]
        require(
            sr["source_gates"] == len(emitted)
            and sr["ccx_source"] == counts["ccx"]
            and sr["x"] == counts["x"],
            "Selector gate inventory",
        )
        require(
            sr["cx"] == counts["cx"] + 6 * counts["ccx"] and sr["h"] == 2 * counts["ccx"],
            "Selector exact CCX Clifford charge",
        )
        require(
            sr["t_count"] == 7 * counts["ccx"] and sr["t_depth"] <= 4 * counts["ccx"],
            "Selector exact seven-T charge",
        )
        selector = dict(
            emitted_gate_counts=dict(counts),
            source_contract=selector_record["source_contract"],
            description=selector_record["description"],
            resources=sr,
            forward_T_depth_serial_upper=4 * counts["ccx"],
            inverse_T_depth_serial_upper=4 * counts["ccx"],
            inverse_semantics="Literal reverse of the self-inverse X/CX/CCX selector records",
        )
        bound = financial["raw_output_support"]["Y_6"]
        require(
            -100 * (1 << 40) < bound[0] <= bound[1] < 100 * (1 << 40),
            "Archived selector support proof",
        )
        random_wires = financial["random_wires"] + [
            mapping[j] for j in selector_record["inputs"][1]
        ]
        scratch = financial["logical_qubits"] + sq - 72
    require(wrapper["random_wires"] == random_wires, "Uniform random source/selector register")
    reflection = audit_reflection(operations[indices[-1] + 1 :], random_wires)
    require(
        reflection["scratch"] == scratch and limit == scratch + len(random_wires) - 1,
        "Reflection physical addresses",
    )
    for call, body in zip(calls[: len(calls) // 2], (financial, phase)):
        require(
            integer(call["base"], "Call base") + body["logical_qubits"] <= limit,
            "Wave call address bound",
        )
    return dict(
        financial=financial,
        phase=phase,
        selector=selector,
        reflection=reflection,
        phase_synthesis_per_wrapper=dict(phase_usage),
    )


def export_archive(root, archive_path=ARCHIVE):
    """Return three independently expanded archive rows and explicit omissions."""
    root = Path(root).resolve()
    archive_file = local_path(root, archive_path)
    archive = read(archive_file)
    require(archive["format"] == "bound-controlled-compound-estimators-v1", "Archive recipe format")
    cost_file, synthesis_file = (
        local_path(root, archive[key]) for key in ("cost_artifact", "synthesis_library")
    )
    require(sha256(cost_file) == archive["cost_artifact_sha256"], "Archived cost binding")
    require(
        sha256(synthesis_file) == archive["synthesis_library_sha256"], "Archived synthesis binding"
    )
    costs, synthesis = read(cost_file), read(synthesis_file)
    rows = []
    for row in selected_rows(archive):
        identity = tuple(row[key] for key in ("model", "method", "mode"))
        wrapper_file, allocation_file = (
            local_path(root, row[key]) for key in ("wrapper", "allocation_source")
        )
        require(sha256(wrapper_file) == row["wrapper_sha256"], "Archived wrapper binding")
        require(
            sha256(allocation_file) == row["allocation_source_sha256"],
            "Archived allocation binding",
        )
        record_matches = [
            r
            for r in read(allocation_file)
            if r["model"] == row["model"]
            and r.get("mode", "unconditional_digital_support") == row["mode"]
        ]
        require(
            len(record_matches) == 1 and record_matches[0]["allocation"] == row["allocation"],
            "Archived allocation identity",
        )
        cost_matches = [
            r
            for r in costs["rows"]
            if tuple(r[key] for key in ("model", "method", "mode")) == identity
        ]
        require(len(cost_matches) == 1, "Archived cost identity")
        cost = cost_matches[0]
        wrapper = read(wrapper_file)
        require(row["random_wires"] == wrapper["random_wires"], "Estimator random wire binding")
        controls = row["control_wires"]
        require(
            controls
            == list(
                range(wrapper["qpe_register_base"], wrapper["qpe_register_base"] + len(controls))
            ),
            "Estimator control wire addresses",
        )
        require(max(controls) < row["allocated_logical_qubits_upper"], "Allocated control bound")
        controller = row["classical_controller"]
        allocation = row["allocation"]
        require(allocation["ideal_test_failure"] == 0.003, "Original failure contract")
        if row["method"] == "hadamard":
            require(
                len(controls) == 1 and controller["IQFT_operations"] == [],
                "Hadamard controller has unexpected QPE",
            )
            expanded = expand_hadamard(allocation)
        else:
            expanded = expand_qpe(allocation, controller, controls)
        audited = audit_wrapper(root, wrapper, row["method"])
        calls, preparations = expanded["controlled_wrapper_calls"], expanded["fresh_preparations"]
        financial, phase, selector, reflection = (
            audited[key] for key in ("financial", "phase", "selector", "reflection")
        )
        unit_t = 2 * financial["half_resources"]["t_count"] + reflection["T_count"]
        unit_td = 2 * financial["half_resources"]["t_depth"] + reflection["T_depth_serial_upper"]
        usage = Counter(expanded["iqft_synthesis_usage"])
        if phase:
            unit_t += 2 * phase["half_resources"]["t_count"]
            unit_td += 2 * phase["half_resources"]["t_depth"]
            usage.update(
                {
                    key: value * calls
                    for key, value in audited["phase_synthesis_per_wrapper"].items()
                }
            )
        if selector:
            unit_t += 2 * selector["resources"]["t_count"]
            unit_td += (
                selector["forward_T_depth_serial_upper"] + selector["inverse_T_depth_serial_upper"]
            )
        require(
            dict(usage) == row["synthesis_usage"] == cost["synthesis_usage"],
            "Archived exact synthesis usage",
        )
        for key in usage:
            rotation = synthesis["rotations"][key]
            gates = rotation["matrix_product_gates"]
            require(set(gates) <= set("THSXW"), "Uncharged synthesized gate")
            require(rotation["t_count"] == gates.count("T"), "Synthesized gate-string T count")
            require(
                rotation["clifford_count"] == sum(gates.count(gate) for gate in "HSX"),
                "Synthesized gate-string Clifford count",
            )
            require(
                rotation["global_w_count"] == gates.count("W"),
                "Synthesized gate-string global phase inventory",
            )
        synthesis_t = sum(
            count * synthesis["rotations"][key]["t_count"] for key, count in usage.items()
        )
        synthesis_clifford = sum(
            count * synthesis["rotations"][key]["clifford_count"] for key, count in usage.items()
        )
        arithmetic_t = calls * unit_t + expanded["iqft_exact_T_count"]
        arithmetic_td = calls * unit_td + expanded["iqft_exact_T_depth_serial"]
        total_t = arithmetic_t + synthesis_t
        reconciliations = dict(
            controlled_iterations=calls,
            fresh_preparations=preparations,
            measured_bits=expanded["measured_bits"],
            single_iterate_arithmetic_T_depth=unit_td,
            arithmetic_T_count=arithmetic_t,
            synthesized_rotation_T_count=synthesis_t,
            synthesized_rotation_Clifford_count=synthesis_clifford,
            complete_logical_T_count=total_t,
            arithmetic_wave_T_depth=arithmetic_td,
            wave_plus_serial_rotations_T_depth=arithmetic_td + synthesis_t,
            source_wave_T_depth=2 * financial["half_resources"]["t_depth"],
            longest_coherent_chain_arithmetic_T_depth=expanded["longest_wrapper_chain"] * unit_td,
        )
        for key, value in reconciliations.items():
            require(cost[key] == value, f"Archived resource reconciliation: {key}")
        require(
            row["complete_logical_T_count"] == total_t
            and row["allocated_logical_qubits_upper"] == cost["logical_qubits_upper"],
            "Bound estimator total resource identity",
        )
        nrandom = len(wrapper["random_wires"])
        synthesis_error = (
            2 * sum(usage.values()) * Fraction(*synthesis["common_operator_epsilon_exact"])
        )
        counts = dict(
            fresh_uniform_preparations=preparations,
            uniform_preparation_H=nrandom * preparations,
            control_preparation_H=len(controls) * preparations,
            financial_graph_forward_calls=calls,
            financial_graph_inverse_calls=calls,
            financial_graph_output_copy_calls=0,
            phase_graph_forward_calls=calls if phase else 0,
            phase_graph_inverse_calls=calls if phase else 0,
            phase_bit_controlled_phases=sum(audited["phase_synthesis_per_wrapper"].values())
            // 3
            * calls,
            selector_forward_calls=calls if selector else 0,
            selector_inverse_calls=calls if selector else 0,
            selector_controlled_CZ=calls if selector else 0,
            signed_controlled_reflections=calls,
            reflection_control_Z=calls,
            reflection_gate_counts={
                key: reflection[key] * calls for key in ("ccx", "h", "x", "cz")
            },
            iqft_gate_counts=expanded["iqft_gate_counts"],
            iqft_swap_decomposition_CX=3 * expanded["iqft_gate_counts"].get("swap", 0),
            controlled_phase_decomposition_CX=2
            * (
                expanded["iqft_gate_counts"].get("cp", 0)
                + sum(audited["phase_synthesis_per_wrapper"].values()) // 3 * calls
            ),
            synthesized_single_qubit_rotations=sum(usage.values()),
            readout_bits=expanded["measured_bits"],
            readout_batches=preparations,
            required_clean_reset_bits_before_preparation=(nrandom + len(controls)) * preparations,
            physical_reset_commands=None,
            final_H_before_Hadamard_readout=preparations if phase else 0,
            adaptive_quantum_stages=expanded["adaptive_stages"],
            between_stage_feedback_dependencies=expanded["between_stage_feedback_dependencies"],
            classical_median_decodings=1 if selector else 0,
            classical_individual_QPE_decodings=preparations if selector else 0,
            classical_stage_threshold_evaluations=expanded["adaptive_stages"],
            classical_constant_load_unload_X_exact=None if phase else 0,
            classical_constant_load_unload_X_upper=4
            * wrapper.get("phase_classical_input_width", 0)
            * preparations,
        )
        body_records = []
        for role, body in (("financial", financial), ("phase", phase)):
            if body:
                body_records.append(
                    {
                        key: body[key]
                        for key in (
                            "manifest",
                            "source_sha256",
                            "wave_schedule",
                            "schedule_sha256",
                            "half_resources",
                            "logical_qubits",
                            "raw_output_support",
                            "range_binding",
                            "native_gate_bindings",
                            "native_gate_bytes_replayed",
                        )
                    }
                    | dict(role=role, forward_calls=calls, inverse_calls=calls)
                )
        rows.append(
            dict(
                model=row["model"],
                method=row["method"],
                mode=row["mode"],
                wrapper=row["wrapper"],
                wrapper_sha256=row["wrapper_sha256"],
                source_contract=dict(
                    archived_family="C4/H8 controlled compound residual",
                    output="Y_6",
                    Kc=6,
                    strikes_charged=1,
                    native_width=72,
                    financial_fraction_bits=40,
                    requested_residual_mean_error=allocation["error"],
                    ideal_estimator_failure=allocation["ideal_test_failure"],
                    continuous_moment=allocation.get("moment"),
                    moment_digital_transfer_certified=False if phase else None,
                    normalized_probability=selector["description"] if selector else None,
                    support_raw=financial["raw_output_support"],
                    full_price_contract=False,
                    compatible_with_current_B4_source=False,
                ),
                schedule_expansion=expanded,
                archived_classical_controller=controller,
                invocation_counts=counts,
                bound_graph_bodies=body_records,
                selector=selector,
                reflection=reflection,
                synthesis_usage=dict(usage),
                resource_reconciliation=reconciliations,
                allocated_logical_qubits_upper=row["allocated_logical_qubits_upper"],
                archived_sequential_adaptive_stage_label=cost["sequential_adaptive_stages"],
                synthesized_rotation_total_variation_upper_exact=[
                    synthesis_error.numerator,
                    synthesis_error.denominator,
                ],
                required_phase_function_error=cost["required_phase_function_error"],
                unknowns=dict(
                    physical_layout_and_routing=None,
                    Clifford_duration_seconds=None,
                    rotation_duration_seconds=None,
                    readout_duration_seconds=None,
                    reset_duration_seconds=None,
                    classical_feedback_duration_seconds=None,
                    classical_input_output_seconds=None,
                    decoder_and_factory_supply=None,
                    whole_computation_failure_budget=None,
                    full_price_error_certificate=None,
                    full_price_latency_seconds=None,
                    reset_note=(
                        "The recipe requires clean random/control registers before each execution; "
                        "physical reset commands and post-test merging are unspecified."
                    ),
                    constant_load_note=(
                        "Hadamard target loads depend on observations; exact X count is unknown "
                        "and the archived deterministic upper bound is charged separately."
                    ),
                ),
                scope=(
                    "Logical count and saved schedule reconciliation only; "
                    "no new financial replay, statevector, physical runtime, or advantage claim."
                ),
            )
        )
    return dict(
        format="archived-estimator-invocation-ledger-v1",
        archive=archive_path,
        archive_sha256=sha256(archive_file),
        original_resource_contract=costs["resource_contract"],
        omitted_full_price_terms=costs["omitted_full_price_terms"],
        preserved_synthesis_semantics=synthesis["semantics"],
        rows=rows,
        financial_pair=dict(
            status="pending",
            target="Current native-dollar B4 source/selector/estimator",
            reason=(
                "Requires its own all-input support proof, exact dollar selector, "
                "freshly bound wrapper and error contract."
            ),
            archived_counts_times_B4_depth_allowed=False,
        ),
        new_financial_replays=0,
        new_quantum_unitary_tests=0,
        historical_sources_unchanged=True,
        advantage_demonstrated=False,
    )
