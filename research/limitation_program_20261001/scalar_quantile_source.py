"""Guarded scalar-source compilation with one paid generic-divider control.

No native arrays are constructed or copied on import. Typed reuse is admitted
only after the complete new scalar recipe and proof inputs reconcile.
"""

from copy import deepcopy
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil

from research.limitation_program_20261001.scalar_quantile_ir import (
    ROOT,
    PROGRAM,
    S,
    W,
    F,
    canonical,
    fingerprint,
    read,
    validate_site_binding,
)


DIVIDER = PROGRAM / "A17_quantile_divider_run001"
SQRT = PROGRAM / "A10_coefficient_run001/B4x12/min-depth/leaves/160a18dba2e09b8e1ad2.json"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _registers(arguments, outputs):
    registers = arguments + outputs
    if any(
        register != list(range(index * W, (index + 1) * W))
        for index, register in enumerate(registers)
    ):
        raise ValueError("Full native72 contiguous input/output registers required")


def _native_records():
    if read(DIVIDER / "summary.json").get("passed") is not True:
        raise ValueError("Successful actual candidate64/original72 divider receipt required")
    rows = read(DIVIDER / "leaf_ledgers.json")
    records = {row["name"]: row for row in rows}
    if set(records) != {"candidate64", "original72"} or len(rows) != 2:
        raise ValueError("One bounded divider and one exact generic control required")
    sqrt = read(SQRT)
    spec = sqrt["spec"]
    if (
        spec.get("op"),
        spec.get("width"),
        spec.get("fraction_bits"),
        spec.get("active_input_bits"),
        spec.get("input_contract"),
        spec.get("lowering"),
    ) != (
        "sqrt",
        W,
        F,
        46,
        {"unsigned_input_bits": 46},
        "unsigned-nonrestoring-sqrt-signed-remainder-v1",
    ):
        raise ValueError("Frozen native unsigned46 sqrt interface changed")
    return records, sqrt


def compile_scalar_source(
    target,
    bindings,
    literals,
    proofs,
    proof_inputs,
    directory,
    divider_mode="bounded64",
    reuse_directory=None,
):
    """Compile one frozen graph; full copied native input slots stay charged."""
    if divider_mode not in ("bounded64", "original72"):
        raise ValueError("Exactly one denominator64 candidate and generic72 control allowed")
    validate_site_binding(target, bindings, literals, proofs, proof_inputs)
    records, sqrt_entry = _native_records()
    directory = Path(directory)
    if directory.exists():
        raise FileExistsError("Fresh scalar source directory required")
    from research.controlled_source_completion.compiler import compile_graph
    from research.controlled_source_completion.primitives import Library
    from research.limitation_program_20261001.bounded_quantile_divider import leaf_spec

    class ScalarLibrary(Library):
        def __init__(self):
            super().__init__(directory / "leaves", W, F, deepcopy(target["tables"]))
            self.admissions = []
            if reuse_directory is not None:
                for metadata in sorted((Path(reuse_directory) / "leaves").glob("*.json")):
                    entry = read(metadata)
                    if entry["op"] != "divide":
                        binary = metadata.parent / entry["gate_file"]
                        if digest(binary) != entry["sha256"]:
                            raise ValueError("Generated matched-control reuse array hash differs")
                        shutil.copy2(metadata, self.path / metadata.name)
                        shutil.copy2(binary, self.path / binary.name)

        def copy_native(self, node, entry, binary, origin):
            entry = deepcopy(entry)
            _registers(entry["args"], entry["outs"])
            if entry["params"] != node["params"] or entry["op"] != node["op"]:
                raise ValueError("Archived native operation/parameters differ from new site")
            if digest(binary) != entry["sha256"]:
                raise ValueError("Archived actual native gate bytes changed")
            key = entry["key"]
            if key not in self.entries:
                entry["proof_target_sha256"] = proofs["target_sha256"]
                entry["origin_receipt_or_metadata"] = str(origin.relative_to(ROOT))
                entry["origin_gate_sha256"] = digest(binary)
                shutil.copy2(binary, self.path / entry["gate_file"])
                (self.path / (key + ".json")).write_text(canonical(entry) + "\n", encoding="utf-8")
                self.entries[key] = entry
            self.admissions.append(
                {
                    "op": node["op"],
                    "out": node["out"],
                    "args": node["args"],
                    "leaf": key,
                    "whole_target_sha256": proofs["target_sha256"],
                    "all_input_new_site_proof": True,
                    "native_gate_sha256": entry["sha256"],
                }
            )
            return key, self.entries[key]

        def get(self, node):
            if node["op"] == "sqrt":
                if node["out"] != [bindings["square_root"]] or node["args"] != [
                    bindings["sqrt_argument"]
                ]:
                    raise ValueError("Unsigned46 sqrt requested at an unproved new site")
                return self.copy_native(
                    node, sqrt_entry, SQRT.parent / sqrt_entry["gate_file"], SQRT
                )
            if node["op"] == "divide":
                if (
                    node["out"] != [bindings["quotient"]]
                    or node["args"] != proofs["sites"]["divide"]["args"]
                ):
                    raise ValueError("Shared divider requested at an unproved new site")
                row = records["candidate64" if divider_mode == "bounded64" else "original72"]
                expected = (
                    leaf_spec(W, F, 64)
                    if divider_mode == "bounded64"
                    else {
                        "op": "divide",
                        "width": W,
                        "fraction_bits": F,
                    }
                )
                if row["spec"] != expected:
                    raise ValueError(
                        "Actual archived divider candidate/control specification changed"
                    )
                _registers(row["input_registers"], row["output_registers"])
                key = fingerprint({"spec": expected, "params": {}})[:20]
                binary = ROOT / row["actual_gate_file"].replace("\\", "/")
                entry = {
                    "key": key,
                    "op": "divide",
                    "params": {},
                    "spec": expected,
                    "args": row["input_registers"],
                    "outs": row["output_registers"],
                    "resources": row["resources"],
                    "gate_file": key + ".npy",
                    "sha256": row["actual_gate_sha256"],
                    "table_bits": 0,
                    "input_contract": {"unsigned_denominator_bits": 64}
                    if divider_mode == "bounded64"
                    else {},
                }
                return self.copy_native(node, entry, binary, DIVIDER / "leaf_ledgers.json")
            return super().get(node)

    library = ScalarLibrary()
    source, _ = compile_graph(target, directory, library=library)
    source["new_site_proofs"] = deepcopy(proofs)
    source["typed_native_admissions"] = library.admissions
    source["fixed_optimizer"] = "none: exact guarded SSA recipe and floor order retained"
    source["scalar_law"] = "independent q32 mathematical-native signed-restored AS241"
    source["accepted_Box_Muller_source_changed"] = False
    ledger = reconcile_actual_cost(source, directory)
    source["compiler_resource_reference"] = source["resources"]
    source["resources"] = ledger["clean_resources"]
    (directory / "source.json").write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    return source, ledger


def reconcile_actual_cost(source, directory):
    """Scan real native arrays and their literal reverse; never flatten full F."""
    import numpy as np
    from research.controlled_source_completion.primitives import gate_resources

    path = Path(directory) / "leaves"
    native, forward, inverse = {}, Counter(), Counter()
    fields = ("x", "cx", "ccx", "source_gates", "t_count", "t_depth", "clifford_t_depth")
    copies, copy_rounds, private = 0, 0, 0
    for call in source["forward_calls"]:
        key = call["leaf"]
        if key not in native:
            entry = read(path / (key + ".json"))
            _registers(entry["args"], entry["outs"])
            binary = path / entry["gate_file"]
            if digest(binary) != entry["sha256"]:
                raise ValueError("Actual scalar gate-array hash differs")
            gates = np.load(binary, mmap_mode="r", allow_pickle=False)
            if gates.dtype != np.dtype("int32") or gates.ndim != 2 or gates.shape[1] != 4:
                raise ValueError("Native scalar int32 X/CX/CCX array ABI required")
            qubits = entry["resources"]["qubits"]
            if np.any((gates[:, 0] < 1) | (gates[:, 0] > 3)):
                raise ValueError("Unsupported native phase/arbitrary gate placeholder")
            for column in (1, 2, 3):
                active = gates[:, 0] >= column
                if np.any((gates[active, column] < 0) | (gates[active, column] >= qubits)):
                    raise ValueError("Native gate references unallocated wire")
            directions = []
            for array in (gates, gates[::-1]):
                counts, td, ct = gate_resources(array, qubits)
                x, cx, ccx = map(int, counts)
                directions.append(
                    {
                        "x": x,
                        "cx": cx,
                        "ccx": ccx,
                        "source_gates": len(gates),
                        "t_count": 7 * ccx,
                        "t_depth": int(td),
                        "clifford_t_depth": int(ct),
                    }
                )
            if any(entry["resources"][name] != directions[0][name] for name in fields):
                raise ValueError("Native resource metadata differs from actual saved arrays")
            native[key] = {
                "qubits": qubits,
                "gate_sha256": digest(binary),
                "native_args": entry["args"],
                "native_outputs": entry["outs"],
                "forward": directions[0],
                "literal_inverse": directions[1],
            }
        row = native[key]
        for name in fields:
            forward[name] += row["forward"][name]
            inverse[name] += row["literal_inverse"][name]
        copies += 2 * len(call["args"]) * W
        copy_rounds += max(Counter(call["args"]).values(), default=0)
        private = max(private, row["qubits"] - len(call["out"]) * W)
    clean = {name: forward[name] + inverse[name] for name in fields}
    output_copy = len(source["outputs"]) * W
    clean["source_gates"] += 2 * copies + output_copy
    clean["cx"] += 2 * copies + output_copy
    clean["clifford_t_depth"] += 4 * copy_rounds + 1
    clean.update(
        clifford_cx=clean["cx"] + 6 * clean["ccx"],
        clifford_h=2 * clean["ccx"],
        logical_qubits=(source["values"] + len(source["outputs"])) * W + private,
        max_reused_scratch_qubits=private,
        random_hadamards=32,
        ssa_words=source["values"],
        output_words=1,
        t_depth_schedule="serial complete native leaves, ASAP7T per direction; all copies paid",
        ccx_expansion="exact7T CCX; X/CX/CCX arrays, no relative phase substitutions",
    )
    if clean["logical_qubits"] != source["resources"]["logical_qubits"]:
        raise ValueError("Actual scalar source allocation differs from compiler bank layout")
    return {
        "native_leaves": native,
        "forward_native_resources": dict(forward),
        "literal_inverse_native_resources": dict(inverse),
        "clean_resources": clean,
        "argument_copy_CX_forward": copies,
        "argument_copy_CX_inverse": copies,
        "named_full72_output_copy_CX": output_copy,
        "all_native_high_input_output_and_private_wires_charged": True,
        "flat_full_gate_array_materialized": False,
        "actual_scalar_component_cost_only": True,
        "financial_loader_path_or_runtime_cost_extrapolated": False,
        "initial_Hadamards_counted_separately": 32,
        "fraction_scale": S,
    }
