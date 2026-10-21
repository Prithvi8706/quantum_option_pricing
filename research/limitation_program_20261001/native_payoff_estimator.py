"""Source-bound positive-payoff selector and signed controlled Grover iterate.

The probability is E[already discounted native Y]/64. Every financial leaf,
selector comparison, copied control, literal inverse and reflection gate is
emitted. The uniform selector and phase controls use the old named-Y buffer;
temporary comparator/AND work reuses the financial private bank after F.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

import numpy as np
from numba import njit

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage
from research.controlled_source_completion.compiler import mapped_gates, resolve_library
from research.controlled_source_completion.primitives import array_gates
from research.journal_sprint.reversible_fixed_point import Program, less_than
from research.limitation_program_20261001.checkpoint_circuit import _native_cost, fingerprint


ROOT = Path(__file__).resolve().parents[2]
FORMAT = "native-positive-payoff-controlled-grover-v1"
GATE_NAMES = {1: "x", 2: "cx", 3: "ccx", 4: "h", 5: "cz", 6: "z"}
COUNT_FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_receipt(directory):
    directory = Path(directory)
    manifest = _read(directory / "manifest.json")
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError("Unknown native estimator receipt schema")
    if "files" in manifest or "frozen_inputs" in manifest:
        if set(manifest) != {"files", "frozen_inputs"}:
            raise ValueError("Unknown native estimator receipt schema")
        maps = [(ROOT, manifest[field]) for field in ("files", "frozen_inputs")]
    else:
        maps = [(directory, manifest)]
    protocol_path = directory / "protocol.json"
    if protocol_path.is_file():
        protocol = _read(protocol_path)
        if "frozen_inputs" in protocol:
            maps.append((ROOT, protocol["frozen_inputs"]))
    for base, records in maps:
        if not isinstance(records, dict):
            raise ValueError("Unknown native estimator receipt schema")
        for name, digest in records.items():
            if (
                not isinstance(name, str)
                or not isinstance(digest, str)
                or len(digest) != 64
                or any(character not in "0123456789abcdef" for character in digest)
            ):
                raise ValueError("Unknown native estimator receipt schema")
            path = (base / name.replace("\\", "/")).resolve()
            try:
                path.relative_to(base.resolve())
            except ValueError as exc:
                raise ValueError("Native estimator receipt path escapes its root") from exc
            if not path.is_file() or _sha(path) != digest:
                raise ValueError("Native estimator bound receipt changed: " + name)
    return manifest


def bind_source_estimator(case_directory, certificate_path, audit_directory):
    """Require accepted exact source and independently audited native support."""
    case_directory, certificate_path, audit_directory = (
        Path(p).resolve() for p in (case_directory, certificate_path, audit_directory)
    )
    case = case_directory.parent.name
    if case not in ("B4x12", "B8x52") or case_directory.name != "min-depth":
        raise ValueError("Estimator must bind accepted B4/B8 min-depth sources")
    if (
        case_directory.parent.parent
        != ROOT / "results/limitation_program_20261001/A10_coefficient_run001"
    ):
        raise ValueError("Estimator accepted arithmetic source identity changed")
    if (
        certificate_path
        != (
            ROOT
            / "results/limitation_program_20261001/E03_support_run001"
            / (case + "_certificate.json")
        )
        or audit_directory != ROOT / "results/limitation_program_20261001/E03_support_audit_run002"
    ):
        raise ValueError("Estimator requires the accepted support certificate and audit run002")
    for directory in (case_directory.parent.parent, certificate_path.parent, audit_directory):
        _verify_receipt(directory)
    certificate, audit_summary = _read(certificate_path), _read(audit_directory / "summary.json")
    audit = _read(audit_directory / (case + "_audit.json"))
    if (
        not audit_summary["passed"]
        or not audit["passed"]
        or not audit_summary["independent_actual_SSA_support_audit"]
    ):
        raise ValueError("Independent actual-SSA payoff support audit required")
    if (
        certificate["width"],
        certificate["fraction_bits"],
        certificate["selector_random_bits"],
        certificate["selector_span_raw"],
    ) != (72, 40, 46, 1 << 46):
        raise ValueError("Native positive selector precision/support changed")
    bounds = certificate["payoff_raw_bounds"]
    if bounds[0] != 0 or not 0 <= bounds[1] < 1 << 46 or bounds != audit["payoff_raw_bounds"]:
        raise ValueError("Native output does not have the audited nonnegative support")
    if (
        not certificate["all_original_uniform_word_patterns"]
        or certificate["sampled_price_maximum_used"]
        or not certificate["complete_builder_equality"]
    ):
        raise ValueError(
            "All original-word support proof required; finite samples cannot replace it"
        )
    if not audit["all_actual_sum_max_average_subtract_discount_nodes_safe"]:
        raise ValueError("Original arithmetic and discount support chain not independently proved")
    paths = {
        name: case_directory / name
        for name in ("target.json", "source.json", "schedule_capped.json")
    }
    source, target, capped = (
        _read(paths[name]) for name in ("source.json", "target.json", "schedule_capped.json")
    )
    if certificate["target_output"] != target["outputs"] or target["outputs"] != {
        "Y": source["outputs"]["Y"]
    }:
        raise ValueError("Support proof does not bind the native Y output")
    storage = _storage(target, source, entries(source))
    if any(capped[k] != v for k, v in storage.items()):
        raise ValueError("Accepted compact storage proof changed")
    if (capped["source_fingerprint"], capped["target_fingerprint"]) != (
        fingerprint(source),
        fingerprint(target),
    ):
        raise ValueError("Accepted capped source fingerprint changed")
    for directory in (certificate_path.parent, audit_directory):
        frozen = _read(directory / "protocol.json")["frozen_inputs"]
        for path in paths.values():
            if frozen.get(path.relative_to(ROOT).as_posix()) != _sha(path):
                raise ValueError("Support receipt binds different target/source/capped bytes")
    return {
        "case": case,
        "paths": {name: str(path) for name, path in paths.items()},
        "hashes": {name: _sha(path) for name, path in paths.items()},
        "certificate_path": str(certificate_path),
        "certificate_sha256": _sha(certificate_path),
        "audit_path": str(audit_directory / (case + "_audit.json")),
        "audit_sha256": _sha(audit_directory / (case + "_audit.json")),
        "audit_manifest_path": str(audit_directory / "manifest.json"),
        "audit_manifest_sha256": _sha(audit_directory / "manifest.json"),
        "word_width": 72,
        "fraction_bits": 40,
        "selector_bits": 46,
        "payoff_raw_bounds": bounds,
        "dollar_span": 64,
        "probability_law": "p=E[Yraw]/2**46=E[already discounted native dollar Y]/64",
        "second_discount_applied": False,
        "continuous_financial_error_certified": False,
    }


def make_selector(word_width=72, selector_bits=46):
    """Exact clean flag=[u<Y] under the proved 0<=Y<2**selector_bits law."""
    if (
        type(word_width) is not int
        or type(selector_bits) is not int
        or not 1 <= selector_bits <= word_width
    ):
        raise ValueError("selector must fit the full native payoff word")
    program = Program(compact=True)
    value, uniform = program.register(word_width), program.register(selector_bits)
    flag = program.register(1)[0]
    difference, extended, helper = (
        program.register(selector_bits + 1),
        program.register(selector_bits + 1),
        program.register(1)[0],
    )
    less_than(program, uniform, value[:selector_bits], flag, difference, extended, helper)
    return program, (value, uniform), (flag,)


def make_reflection(random_bits):
    """Actual H/X/CCX/CZ/Z primitive array for controlled (2|+><+|-I)."""
    if type(random_bits) is not int or random_bits < 2:
        raise ValueError("controlled reflection requires at least two random wires")
    random, control = list(range(random_bits)), random_bits
    scratch = list(range(random_bits + 1, 2 * random_bits))
    operations = [(4, wire, 0, 0) for wire in random]
    operations += [(1, wire, 0, 0) for wire in random]
    ladder = [(3, random[0], random[1], scratch[0])]
    ladder += [(3, scratch[j - 2], random[j], scratch[j - 1]) for j in range(2, random_bits)]
    operations += ladder + [(5, scratch[-1], control, 0)] + list(reversed(ladder))
    operations += [(1, wire, 0, 0) for wire in random]
    operations += [(4, wire, 0, 0) for wire in random]
    operations += [(6, control, 0, 0)]
    return np.asarray(operations, dtype=np.int32), {
        "qubits": 2 * random_bits,
        "random": random,
        "control": control,
        "scratch": scratch,
        "relative_sign": "Final Z(control) supplies the sign of 2|+><+|-I on the controlled branch",
    }


@njit(cache=True)
def _extended_depth(gates, qubits):
    levels, depth, counts = (
        np.zeros(qubits, np.int64),
        np.zeros(qubits, np.int64),
        np.zeros(6, np.int64),
    )
    for gate in gates:
        kind, a, b, c = gate
        counts[kind - 1] += 1
        if kind in (1, 4, 6):
            depth[a] += 1
        elif kind in (2, 5):
            t, d = max(levels[a], levels[b]), max(depth[a], depth[b]) + 1
            levels[a] = levels[b] = t
            depth[a] = depth[b] = d
        else:
            wires = (
                (c, c),
                (b, c),
                (c, c),
                (a, c),
                (c, c),
                (b, c),
                (c, c),
                (a, c),
                (b, b),
                (c, c),
                (c, c),
                (a, b),
                (a, a),
                (b, b),
                (a, b),
            )
            for j in range(15):
                aa, bb = wires[j]
                t = max(levels[aa], levels[bb]) + int(j in (2, 4, 6, 8, 9, 12, 13))
                d = max(depth[aa], depth[bb]) + 1
                levels[aa] = levels[bb] = t
                depth[aa] = depth[bb] = d
    return counts, levels.max(), depth.max()


def extended_resources(gates, qubits):
    if (
        not isinstance(gates, np.ndarray)
        or gates.ndim != 2
        or gates.shape[1] != 4
        or type(qubits) is not int
        or qubits <= 0
    ):
        raise ValueError("Invalid actual extended gate array")
    for kind, a, b, c in gates:
        if int(kind) not in GATE_NAMES:
            raise ValueError("Unknown logical primitive")
        arity = 1 if kind in (1, 4, 6) else 2 if kind in (2, 5) else 3
        wires = [int(wire) for wire in (a, b, c)[:arity]]
        if len(set(wires)) != arity or not all(0 <= wire < qubits for wire in wires):
            raise ValueError("Logical primitive has aliased or unallocated wires")
    counts, td, ctd = _extended_depth(gates, qubits)
    x, cx, ccx, h, cz, z = map(int, counts)
    return {
        "source_gates": len(gates),
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "h": h,
        "cz": cz,
        "z": z,
        "t_count": 7 * ccx,
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": h + 2 * ccx,
        "clifford_cz": cz,
        "clifford_z": z,
        "t_depth": int(td),
        "clifford_t_depth": int(ctd),
    }


def make_toy_iterate(kind):
    """Actual small full iterate arrays for independent controlled-unitary audits."""
    if kind not in ("positive-two-point", "positive-rare-event", "shifted-negative-two-point"):
        raise ValueError("Unknown frozen estimator toy")
    shifted = kind == "shifted-negative-two-point"
    source_bits = 2 if kind == "positive-rare-event" else 1
    word_width, selector_bits = (4, 2) if shifted else (2, 1)
    if shifted:
        from research.controlled_priority_completion.estimator_bounded import shifted_selector

        selector, (value, uniform), (flag,) = shifted_selector(word_width, 0, 2)
    else:
        selector, (value, uniform), (flag,) = make_selector(word_width, selector_bits)
    source = list(range(source_bits))
    y = list(range(source_bits, source_bits + word_width))
    u = list(range(source_bits + word_width, source_bits + word_width + selector_bits))
    flag_wire, control = u[-1] + 1, u[-1] + 2
    private_base = control + 1
    mapping = np.full(selector.qubits, -1, dtype=np.int64)
    mapping[list(value)], mapping[list(uniform)], mapping[flag] = y, u, flag_wire
    free = np.flatnonzero(mapping < 0)
    mapping[free] = np.arange(private_base, private_base + len(free))
    if shifted:
        financial = [(1, bit, 0, 0) for bit in y]
        financial += [(2, source[0], bit, 0) for bit in y[1:]]
    elif source_bits == 2:
        financial = [(3, source[0], source[1], y[0])]
    else:
        financial = [(2, source[0], y[0], 0)]
    native_selector = array_gates(selector)
    selected = []
    for row in native_selector:
        arity = int(row[0])
        wires = [int(mapping[wire]) for wire in row[1 : arity + 1]]
        selected.append((arity, *wires, *([0] * (3 - arity))))
    random_wires = source + u
    reflection, reflection_spec = make_reflection(len(random_wires))
    reflected_mapping = (
        random_wires
        + [control]
        + list(range(private_base, private_base + len(reflection_spec["scratch"])))
    )
    reflected = []
    for row in reflection:
        gate_kind = int(row[0])
        arity = 1 if gate_kind in (1, 4, 6) else 2 if gate_kind in (2, 5) else 3
        wires = [reflected_mapping[wire] for wire in row[1 : arity + 1]]
        reflected.append((gate_kind, *wires, *([0] * (3 - arity))))
    operations = (
        financial
        + selected
        + [(5, control, flag_wire, 0)]
        + list(reversed(selected))
        + list(reversed(financial))
        + reflected
    )
    qubits = private_base + max(len(free), len(reflection_spec["scratch"]))
    support, marking = [], []
    for raw in range(1 << len(random_wires)):
        source_word, uniform_word = raw & ((1 << source_bits) - 1), raw >> source_bits
        payoff = (
            (-1 if source_word == 0 else 1)
            if shifted
            else (int(source_word == 3) if source_bits == 2 else source_word)
        )
        support.append(payoff)
        marking.append(int(uniform_word < payoff + 2 if shifted else uniform_word < payoff))
    return np.asarray(operations, dtype=np.int32), {
        "kind": kind,
        "qubits": qubits,
        "random_wires": random_wires,
        "source_wires": source,
        "value_wires": y,
        "selector_wires": u,
        "control_wire": control,
        "flag_wire": flag_wire,
        "workspace_wires": sorted(set(range(qubits)) - set(random_wires + [control])),
        "payoff_for_each_random_word": support,
        "marking_for_each_random_word": marking,
        "probability_numerator": sum(marking),
        "probability_denominator": len(marking),
        "shift": 2 if shifted else 0,
        "selector_span": 1 << selector_bits,
        "expected_control_zero": "identity",
        "expected_control_one": "(2|+><+|-I)*marking",
        "source_inverse": "literal gate reversal",
        "selector_inverse": "literal gate reversal",
    }


def emit_toy_iterates(output_directory):
    """Persist prospective-frozen toy arrays for an independent unitary scanner."""
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=False)
    specs = []
    for kind in ("positive-two-point", "positive-rare-event", "shifted-negative-two-point"):
        gates, spec = make_toy_iterate(kind)
        file = output_directory / (kind + ".npy")
        np.save(file, gates)
        spec.update(gate_file=str(file.resolve()), sha256=_sha(file))
        specs.append(spec)
    (output_directory / "toys.json").write_text(
        json.dumps(specs, indent=2) + "\n", encoding="utf-8"
    )
    return specs


def _load_bound(binding):
    for name, path in binding["paths"].items():
        if _sha(path) != binding["hashes"][name]:
            raise ValueError("Bound estimator source changed")
    for path, expected in (
        (binding["certificate_path"], binding["certificate_sha256"]),
        (binding["audit_path"], binding["audit_sha256"]),
        (binding["audit_manifest_path"], binding["audit_manifest_sha256"]),
    ):
        if _sha(path) != expected:
            raise ValueError("Bound estimator support proof changed")
    source, target, capped = (
        _read(binding["paths"][name])
        for name in ("source.json", "target.json", "schedule_capped.json")
    )
    metadata = entries(source)
    storage = _storage(target, source, metadata)
    if any(capped[k] != v for k, v in storage.items()):
        raise ValueError("Bound estimator compact native storage changed")
    if (capped["source_fingerprint"], capped["target_fingerprint"]) != (
        fingerprint(source),
        fingerprint(target),
    ):
        raise ValueError("Bound estimator original graph fingerprints changed")
    certificate, audit = _read(binding["certificate_path"]), _read(binding["audit_path"])
    if (
        binding["word_width"],
        binding["fraction_bits"],
        binding["selector_bits"],
        binding["dollar_span"],
        binding["second_discount_applied"],
    ) != (72, 40, 46, 64, False) or (
        binding["payoff_raw_bounds"] != certificate["payoff_raw_bounds"]
        or binding["payoff_raw_bounds"] != audit["payoff_raw_bounds"]
        or certificate["target_output"] != target["outputs"]
    ):
        raise ValueError("Bound estimator normalization/support changed")
    return source, target, capped, metadata, storage


def emit_iterate(binding, output_directory):
    """Emit exact selector/reflection arrays and the original capped F hierarchy."""
    output_directory = Path(output_directory).resolve()
    output_directory.mkdir(parents=True, exist_ok=False)
    source, target, capped, metadata, storage = _load_bound(binding)
    w, selector_bits = source["word_width"], binding["selector_bits"]
    selector, (value, uniform), (flag,) = make_selector(w, selector_bits)
    selector_gates = array_gates(selector)
    selector_file = output_directory / "selector.npy"
    np.save(selector_file, selector_gates)
    output_base = storage["retained_ssa_qubits"]
    private_base = output_base + len(source["outputs"]) * w
    private_capacity = capped["resources"]["logical_qubits"] - private_base
    flag_wire, control_wire = output_base + selector_bits, output_base + selector_bits + 1
    selector_mapping = np.full(selector.qubits, -1, dtype=np.int64)
    y_value = source["outputs"]["Y"]
    y_base = storage["offsets"][y_value]
    if storage["widths"][y_value] != w:
        raise ValueError("Selector keeps the accepted full-native retained Y interface")
    selector_mapping[list(value)] = np.arange(y_base, y_base + w)
    selector_mapping[list(uniform)] = np.arange(output_base, output_base + selector_bits)
    selector_mapping[flag] = flag_wire
    free = np.flatnonzero(selector_mapping < 0)
    selector_mapping[free] = np.arange(private_base, private_base + len(free))
    random_wires = [
        storage["offsets"][node["out"][0]] + bit
        for node in source["inputs"]
        for bit in range(node["params"]["bits"])
    ]
    random_wires += [int(selector_mapping[wire]) for wire in uniform]
    reflection, reflection_spec = make_reflection(len(random_wires))
    reflection_file = output_directory / "reflection.npy"
    np.save(reflection_file, reflection)
    reflection_mapping = (
        random_wires
        + [control_wire]
        + list(range(private_base, private_base + len(reflection_spec["scratch"])))
    )
    if max(len(free), len(reflection_spec["scratch"])) > private_capacity:
        raise ValueError("Financial private bank cannot fit the paid selector/reflection workspace")
    if control_wire >= private_base or len(set(reflection_mapping)) != len(reflection_mapping):
        raise ValueError("Estimator control/random/reflection wires alias")
    library, native_costs, batches = resolve_library(source), {}, []
    financial_totals = Counter()
    for group in capped["groups"]:
        calls, cursor = [], private_base
        for index in group["call_indices"]:
            call, entry = (
                source["forward_calls"][index],
                metadata[source["forward_calls"][index]["leaf"]],
            )
            key = call["leaf"]
            if key not in native_costs:
                file = library / entry["gate_file"]
                if _sha(file) != entry["sha256"]:
                    raise ValueError("Estimator actual financial leaf changed")
                gates = np.load(file, mmap_mode="r")
                native_costs[key] = {
                    "forward": _native_cost(gates, entry["resources"]["qubits"], False),
                    "inverse": _native_cost(gates, entry["resources"]["qubits"], True),
                }
                if any(
                    native_costs[key]["forward"][field] != entry["resources"][field]
                    for field in COUNT_FIELDS + ("t_depth", "clifford_t_depth")
                ):
                    raise ValueError("Actual financial native leaf resources changed")
            private = entry["resources"]["qubits"] - sum(storage["widths"][v] for v in call["out"])
            calls.append(
                {"call_index": index, "leaf": key, "private_base": cursor, "private_width": private}
            )
            cursor += private
            for direction in ("forward", "inverse"):
                for field in COUNT_FIELDS:
                    financial_totals[field] += native_costs[key][direction][field]
            copies = 4 * sum(storage["widths"][v] for v in call["args"])
            for field in ("source_gates", "cx", "clifford_cx"):
                financial_totals[field] += copies
        if cursor - private_base != group["private_scratch_qubits"]:
            raise ValueError("Estimator original native batch private allocation changed")
        for direction in ("forward", "inverse"):
            financial_totals["t_depth"] += max(
                native_costs[c["leaf"]][direction]["t_depth"] for c in calls
            )
            financial_totals["clifford_t_depth"] += (
                max(native_costs[c["leaf"]][direction]["clifford_t_depth"] for c in calls)
                + 2 * group["copy_rounds"]
            )
        batches.append({"wave": group["wave"], "calls": calls, "copy_rounds": group["copy_rounds"]})
    selector_costs = {
        "forward": _native_cost(selector_gates, selector.qubits, False),
        "inverse": _native_cost(selector_gates, selector.qubits, True),
    }
    reflection_costs = extended_resources(reflection, reflection_spec["qubits"])
    totals = Counter(financial_totals)
    for costs in (*selector_costs.values(), reflection_costs):
        for field, count in costs.items():
            totals[field] += count
    totals["source_gates"] += 1
    totals["cz"] += 1
    totals["clifford_cz"] += 1
    totals["clifford_t_depth"] += 1
    resources = dict(totals)
    resources.update(
        logical_qubits=capped["resources"]["logical_qubits"],
        original_uniform_bits=source["resources"]["random_hadamards"],
        selector_uniform_bits=selector_bits,
        initial_uniform_preparation_h=len(random_wires),
        additional_logical_qubits=0,
        qpe_controls_available_in_old_output_buffer=w - selector_bits - 1,
    )
    wrapper = {
        "format": FORMAT,
        "binding": binding,
        "binding_fingerprint": fingerprint(binding),
        "source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "capped_fingerprint": fingerprint(capped),
        "financial_batches": batches,
        "financial_native_costs": native_costs,
        "financial_resources": dict(financial_totals),
        "selector_file": str(selector_file),
        "selector_sha256": _sha(selector_file),
        "selector_mapping": list(map(int, selector_mapping)),
        "selector_flag_wire": flag_wire,
        "selector_uniform_wires": [int(selector_mapping[v]) for v in uniform],
        "selector_native_value_register": list(value),
        "selector_native_uniform_register": list(uniform),
        "selector_native_flag_wire": flag,
        "selector_costs": selector_costs,
        "reflection_file": str(reflection_file),
        "reflection_sha256": _sha(reflection_file),
        "reflection_mapping": reflection_mapping,
        "reflection_spec": reflection_spec,
        "reflection_resources": reflection_costs,
        "random_wires": random_wires,
        "control_wire": control_wire,
        "allowed_qpe_control_wires": list(range(output_base + selector_bits + 1, private_base)),
        "private_base": private_base,
        "private_capacity": private_capacity,
        "resources": resources,
        "sequence": [
            "original compact F forward",
            "positive selector",
            "CZ(control,flag)",
            "literal inverse selector",
            "literal inverse original F",
            "signed controlled uniform reflection (includes final Z(control))",
        ],
        "native_named_Y_copy_omitted": True,
        "old_output_buffer_reused": True,
        "probability_law": binding["probability_law"],
        "second_discount_applied": False,
        "depth_convention": (
            "Original memory-capped source batches; exact separate forward/inverse leaf ASAP "
            "depths; serial selector/marker/reflection; shared-control copy rounds and H/CZ/Z "
            "layers charged"
        ),
        "G2_to_G5": "open",
    }
    wrapper["wrapper_fingerprint"] = fingerprint(wrapper)
    (output_directory / "iterate.json").write_text(
        json.dumps(wrapper, indent=2) + "\n", encoding="utf-8"
    )
    return wrapper


def _checked_wrapper(wrapper):
    if (
        wrapper.get("format") != FORMAT
        or wrapper.get("wrapper_fingerprint")
        != fingerprint(
            {name: value for name, value in wrapper.items() if name != "wrapper_fingerprint"}
        )
        or wrapper["binding_fingerprint"] != fingerprint(wrapper["binding"])
    ):
        raise ValueError("Emitted estimator wrapper changed")
    source, target, capped, metadata, storage = _load_bound(wrapper["binding"])
    if (
        wrapper["source_fingerprint"],
        wrapper["target_fingerprint"],
        wrapper["capped_fingerprint"],
    ) != (fingerprint(source), fingerprint(target), fingerprint(capped)):
        raise ValueError("Estimator original target/source/schedule changed")
    for file, digest in (
        (wrapper["selector_file"], wrapper["selector_sha256"]),
        (wrapper["reflection_file"], wrapper["reflection_sha256"]),
    ):
        if _sha(file) != digest:
            raise ValueError("Emitted estimator selector/reflection changed")
    expected = []
    for group in capped["groups"]:
        cursor, records = wrapper["private_base"], []
        for index in group["call_indices"]:
            call = source["forward_calls"][index]
            private = metadata[call["leaf"]]["resources"]["qubits"] - sum(
                storage["widths"][value] for value in call["out"]
            )
            records.append(
                {
                    "call_index": index,
                    "leaf": call["leaf"],
                    "private_base": cursor,
                    "private_width": private,
                }
            )
            cursor += private
        if cursor > wrapper["resources"]["logical_qubits"]:
            raise ValueError("Estimator financial native bank exceeds allocation")
        expected.append(
            {"wave": group["wave"], "calls": records, "copy_rounds": group["copy_rounds"]}
        )
    if wrapper["financial_batches"] != expected:
        raise ValueError("Estimator financial native schedule changed")
    return source, target, capped, metadata, storage


def _financial_bindings(source, storage, metadata, batch):
    bindings = []
    for record in batch["calls"]:
        call = source["forward_calls"][record["call_index"]]
        entry = metadata[record["leaf"]]
        if record["leaf"] != call["leaf"]:
            raise ValueError("Estimator financial invocation changed")
        mapping = np.full(entry["resources"]["qubits"], -1, dtype=np.int64)
        for value, register in zip(call["out"], entry["outs"], strict=True):
            width, offset = storage["widths"][value], storage["offsets"][value]
            mapping[register[:width]] = np.arange(offset, offset + width)
        free = np.flatnonzero(mapping < 0)
        if len(free) != record["private_width"]:
            raise ValueError("Estimator native unused output/input scratch changed")
        mapping[free] = np.arange(record["private_base"], record["private_base"] + len(free))
        bindings.append((call, entry, mapping))
    return bindings


def expand_invocations(wrapper, control_wire=None, include_financial=True):
    """Yield actual logical primitives lazily; never flatten billions of gates."""
    control = wrapper["control_wire"] if control_wire is None else control_wire
    if control not in wrapper["allowed_qpe_control_wires"]:
        raise ValueError("Estimator phase control aliases source/selector/scratch")
    source, _, _, metadata, storage = _checked_wrapper(wrapper)
    library = resolve_library(source)
    validated_leaves = set()

    def financial(inverse):
        for batch in (
            reversed(wrapper["financial_batches"]) if inverse else wrapper["financial_batches"]
        ):
            bindings = _financial_bindings(source, storage, metadata, batch)
            ordered = list(reversed(bindings)) if inverse else bindings
            for call, entry, mapping in ordered:
                arguments = list(zip(call["args"], entry["args"], strict=True))
                for value, register in reversed(arguments) if inverse else arguments:
                    bits = range(storage["widths"][value])
                    for bit in reversed(bits) if inverse else bits:
                        yield {
                            "gate": "cx",
                            "wires": [storage["offsets"][value] + bit, int(mapping[register[bit]])],
                        }
            for _, entry, mapping in ordered:
                file = library / entry["gate_file"]
                if entry["sha256"] not in validated_leaves:
                    if _sha(file) != entry["sha256"]:
                        raise ValueError("Actual financial estimator leaf changed before expansion")
                    validated_leaves.add(entry["sha256"])
                gates = np.load(file, mmap_mode="r")
                for row in gates[::-1] if inverse else gates:
                    kind = int(row[0])
                    yield {
                        "gate": GATE_NAMES[kind],
                        "wires": [int(mapping[q]) for q in row[1 : kind + 1]],
                    }
            for call, entry, mapping in ordered:
                arguments = list(zip(call["args"], entry["args"], strict=True))
                for value, register in reversed(arguments) if inverse else arguments:
                    bits = range(storage["widths"][value])
                    for bit in reversed(bits) if inverse else bits:
                        yield {
                            "gate": "cx",
                            "wires": [storage["offsets"][value] + bit, int(mapping[register[bit]])],
                        }

    if include_financial:
        yield from financial(False)
    selector = np.load(wrapper["selector_file"], mmap_mode="r")
    for row in selector:
        kind = int(row[0])
        yield {
            "gate": GATE_NAMES[kind],
            "wires": [wrapper["selector_mapping"][q] for q in row[1 : kind + 1]],
        }
    yield {"gate": "cz", "wires": [control, wrapper["selector_flag_wire"]]}
    for row in selector[::-1]:
        kind = int(row[0])
        yield {
            "gate": GATE_NAMES[kind],
            "wires": [wrapper["selector_mapping"][q] for q in row[1 : kind + 1]],
        }
    if include_financial:
        yield from financial(True)
    reflection = np.load(wrapper["reflection_file"], mmap_mode="r")
    mapping = list(wrapper["reflection_mapping"])
    mapping[wrapper["reflection_spec"]["control"]] = control
    for row in reflection:
        kind = int(row[0])
        arity = 1 if kind in (1, 4, 6) else 2 if kind in (2, 5) else 3
        yield {"gate": GATE_NAMES[kind], "wires": [mapping[q] for q in row[1 : arity + 1]]}


def replay_marking(wrapper, inputs, selector_value, control=1):
    """Basis replay of actual F/selector/inverses; CZ's diagonal phase is exact."""
    if type(selector_value) is not int or not 0 <= selector_value < 1 << len(
        wrapper["selector_uniform_wires"]
    ):
        raise ValueError("Selector value violates the uniform word law")
    if control not in (0, 1):
        raise ValueError("Basis marking replay takes one Boolean control")
    source, _, _, metadata, storage = _checked_wrapper(wrapper)
    state = np.zeros(wrapper["resources"]["logical_qubits"], dtype=np.uint8)
    for node in source["inputs"]:
        raw = int(inputs[node["params"]["name"]])
        if not 0 <= raw < 1 << node["params"]["bits"]:
            raise ValueError("Original financial uniform word law changed")
        value, width = node["out"][0], storage["widths"][node["out"][0]]
        offset = storage["offsets"][value]
        state[offset : offset + width] = [(raw >> bit) & 1 for bit in range(width)]
    state[wrapper["selector_uniform_wires"]] = [
        (selector_value >> bit) & 1 for bit in range(len(wrapper["selector_uniform_wires"]))
    ]
    state[wrapper["control_wire"]] = control
    before, library, cache = state.copy(), resolve_library(source), {}

    def half(inverse):
        for batch in (
            reversed(wrapper["financial_batches"]) if inverse else wrapper["financial_batches"]
        ):
            bindings = _financial_bindings(source, storage, metadata, batch)
            ordered = list(reversed(bindings)) if inverse else bindings
            for call, entry, mapping in ordered:
                for value, register in zip(call["args"], entry["args"], strict=True):
                    width, offset = storage["widths"][value], storage["offsets"][value]
                    state[mapping[register[:width]]] ^= state[offset : offset + width]
            for _, entry, mapping in ordered:
                key = entry["sha256"]
                if key not in cache:
                    file = library / entry["gate_file"]
                    if _sha(file) != key:
                        raise ValueError("Actual financial estimator leaf changed before replay")
                    cache[key] = np.load(file, mmap_mode="r")
                mapped_gates(cache[key], state, mapping, inverse)
            for call, entry, mapping in ordered:
                for value, register in zip(call["args"], entry["args"], strict=True):
                    width, offset = storage["widths"][value], storage["offsets"][value]
                    state[mapping[register[:width]]] ^= state[offset : offset + width]
            if np.any(state[wrapper["private_base"] :]):
                raise AssertionError("Financial estimator native batch scratch did not clean")

    half(False)
    y_value = source["outputs"]["Y"]
    y_offset = storage["offsets"][y_value]
    y_raw = sum(int(state[y_offset + bit]) << bit for bit in range(source["word_width"]))
    if (
        not wrapper["binding"]["payoff_raw_bounds"][0]
        <= y_raw
        <= wrapper["binding"]["payoff_raw_bounds"][1]
    ):
        raise AssertionError("Actual financial output violated its native support certificate")
    selector = np.load(wrapper["selector_file"], mmap_mode="r")
    mapping = np.asarray(wrapper["selector_mapping"], dtype=np.int64)
    mapped_gates(selector, state, mapping, False)
    marked = int(state[wrapper["selector_flag_wire"]])
    if marked != int(selector_value < y_raw):
        raise AssertionError("Actual native selector has the wrong strict comparison")
    phase = -1 if control and marked else 1
    mapped_gates(selector, state, mapping, True)
    half(True)
    return {
        "case": wrapper["binding"]["case"],
        "y_raw": y_raw,
        "selector_value": selector_value,
        "marked": bool(marked),
        "control": control,
        "controlled_phase": phase,
        "all_input_selector_control_and_workspace_restored": bool(np.array_equal(state, before)),
        "full_reflection_statevector_executed": False,
        "source_inverse_is_literal_gate_reverse": True,
    }
