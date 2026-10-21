"""Proof-dispatched exact constants with unchanged archived fallback leaves.

Constructor API:
    ConstantIntegrationLibrary(path, target, source,
        log_strategy="signed-digit-carry-save", general_replacements=None)

Set log_strategy=None for an isolated full-width general-constant experiment.
The ln(2) coefficient is reserved: exponential/unproved ln(2) calls always keep
their original leaf. General replacements have no narrowed-input promise.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
from collections import Counter
from collections.abc import Mapping
from pathlib import Path

import numpy as np

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.constant_multiplier import (
    LOWERING as CONSTANT_LOWERING,
    STRATEGIES,
    build_constant_multiplier,
)
from research.controlled_source_completion.exact_lookup import LOOKUP_LOWERING
from research.controlled_source_completion.log_constant_multiplier import (
    COEFFICIENT,
    build_log_constant_multiplier,
    leaf_spec,
)
from research.controlled_source_completion.primitives import (
    Library,
    array_gates,
    gate_resources,
    resources,
)
from research.limitation_program_20261001.prove_log_exponent import (
    SSAContext,
    prove_log_site,
)

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION_LOWERING = "proof-dispatched-constant-library-v1"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def filename(name):
    if not isinstance(name, str) or not name or name in (".", ".."):
        raise ValueError("invalid leaf filename")
    if Path(name).name != name or "/" in name or "\\" in name:
        raise ValueError("leaf filename must not contain a path")
    return name


def actual_resources(gates, qubits):
    counts, tdepth, depth = gate_resources(gates, qubits)
    x, cx, ccx = map(int, counts)
    return {
        "qubits": qubits,
        "source_gates": len(gates),
        "x": x,
        "cx": cx,
        "ccx": ccx,
        "t_count": 7 * ccx,
        "t_depth": int(tdepth),
        "clifford_t_depth": int(depth),
        "clifford_cx": cx + 6 * ccx,
        "clifford_h": 2 * ccx,
    }


class ConstantIntegrationLibrary(Library):
    """Snapshot and bind the exact target; retain original keys/bytes on fallback."""

    def __init__(
        self, path, target, source, *,
        log_strategy="signed-digit-carry-save", general_replacements=None,
    ):
        if log_strategy is not None and log_strategy not in STRATEGIES:
            raise ValueError("known logarithm strategy or None required")
        replacements = {} if general_replacements is None else general_replacements
        if not isinstance(replacements, Mapping):
            raise ValueError("general replacements must map integer coefficients to strategies")
        for coefficient, strategy in replacements.items():
            if type(coefficient) is not int or strategy not in STRATEGIES:
                raise ValueError(
                    "general replacement needs an integer coefficient and known strategy"
                )
            if coefficient == COEFFICIENT:
                raise ValueError("ln2 coefficient is reserved for guarded logarithm dispatch")
        self.context = SSAContext(target)
        frozen = self.context.target
        self.source = copy.deepcopy(source)
        self.log_strategy = log_strategy
        self.general_replacements = dict(replacements)
        self.archive = resolve_library(self.source, workspace_root=ROOT)
        self.decisions, self.proofs, self.general_sites = [], [], []
        self._decided = set()
        self._nodes, self._old_keys, self._call_indices = {}, {}, {}
        self._original_metadata_hashes = {}
        self._validated_entry_signatures = {}
        self._tables_signature = canonical(frozen["tables"])
        self._validate_source_interface(frozen)
        self.original_entries = entries(self.source)
        for key, entry in self.original_entries.items():
            filename(key)
            self._validate_entry_shape(key, entry)
            metadata_path = self.archive / (key + ".json")
            self._original_metadata_hashes[key] = digest(metadata_path)
            self._validate_original_files(key)
        noninputs = [(index, node) for index, node in enumerate(frozen["nodes"])
                     if node["op"] != "input"]
        if len(noninputs) != len(self.source["forward_calls"]):
            raise ValueError("target/source forward-call count mismatch")
        for call_index, ((index, node), call) in enumerate(
            zip(noninputs, self.source["forward_calls"])
        ):
            if canonical([node["args"], node["out"]]) != canonical([call["args"], call["out"]]):
                raise ValueError("target/source argument or output binding mismatch")
            key = call["leaf"]
            entry = self.original_entries[key]
            if entry["op"] != node["op"] or canonical(entry["params"]) != canonical(node["params"]):
                raise ValueError("source leaf operation/params differ from target")
            if len(entry["args"]) != len(node["args"]) or len(entry["outs"]) != len(node["out"]):
                raise ValueError("source leaf arity differs from target")
            self._validate_original_contract(index, node, entry)
            if node["op"] == "lookup":
                self._validate_lookup_binding(frozen, node, key, entry)
            outputs = tuple(node["out"])
            self._nodes[outputs] = (index, canonical(node))
            self._old_keys[index], self._call_indices[index] = key, call_index
        # No archived file is copied until all source/binding/table/hash checks
        # above have passed. The superclass only creates the new destination.
        super().__init__(
            path, frozen["width"], frozen["fraction_bits"], copy.deepcopy(frozen["tables"])
        )

    def _validate_source_interface(self, frozen):
        if (self.source["word_width"], self.source["fraction_bits"]) != (
            frozen["width"], frozen["fraction_bits"]
        ):
            raise ValueError("source width/fraction differ from target")
        inputs = [node for node in frozen["nodes"] if node["op"] == "input"]
        if canonical(self.source["inputs"]) != canonical(inputs):
            raise ValueError("source input declarations differ from target")
        if canonical(self.source["outputs"]) != canonical(frozen["outputs"]):
            raise ValueError("source named outputs differ from target")
        if self.source["values"] != len(self.context.producers):
            raise ValueError("source SSA value count differs from target")
        keys = self.source["library_keys"]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate source library key")
        for key in keys:
            filename(key)
        if set(keys) != {call["leaf"] for call in self.source["forward_calls"]}:
            raise ValueError("source library keys do not match invocation keys")

    def _validate_entry_shape(self, key, entry):
        width = self.context.target["width"]
        if entry.get("key") != key or not isinstance(entry.get("params"), dict):
            raise ValueError("source leaf key/params metadata invalid")
        if entry.get("gate_file") != key + ".npy":
            raise ValueError("source gate file does not match its key")
        filename(entry["gate_file"])
        qubits = entry["resources"].get("qubits")
        if type(qubits) is not int or qubits < 1:
            raise ValueError("invalid leaf qubit count")
        arguments, outputs = entry["args"], entry["outs"]
        expected = 0
        for register in arguments + outputs:
            if register != list(range(expected, expected + width)):
                raise ValueError("unsupported source leaf register layout/width")
            expected += width
        if expected > qubits:
            raise ValueError("source leaf registers exceed its qubits")

    def _validate_original_files(self, key):
        entry = self.original_entries[key]
        if digest(self.archive / (key + ".json")) != self._original_metadata_hashes[key]:
            raise ValueError("archived leaf metadata changed after snapshot")
        if digest(self.archive / entry["gate_file"]) != entry["sha256"]:
            raise ValueError("archived source gate SHA mismatch")

    def _validate_original_contract(self, index, node, entry):
        contract = entry.get("input_contract")
        if contract is None:
            return
        if not isinstance(contract, dict) or set(contract) not in (
            {"zero_low_bits"}, {"zero_low_bits", "signed_upper_bits"}
        ):
            raise ValueError("unsupported archived input contract")
        zero = contract["zero_low_bits"]
        width = self.context.target["width"]
        if type(zero) is not int or not 0 <= zero < width:
            raise ValueError("invalid archived zero-low input contract")
        if zero:
            if node["op"] != "cmul" or len(node["args"]) != 1:
                raise ValueError("unsupported zero-low input contract operation")
            producer = self.context.producers[node["args"][0]]
            shift = producer["params"].get("shift")
            if producer["op"] != "bits" or type(shift) is not int or shift > -zero:
                raise ValueError("archived zero-low input promise is not proved by target")
        if "signed_upper_bits" in contract:
            if contract != {"zero_low_bits": 40, "signed_upper_bits": 7}:
                raise ValueError("unsupported archived signed-upper input contract")
            if prove_log_site(self.context, index) is None:
                raise ValueError("archived signed7 contract is not proved by target")

    def _validate_lookup_binding(self, frozen, node, key, entry):
        name = node["params"].get("table")
        if name not in frozen["tables"]:
            raise ValueError("target lookup table is missing")
        table = frozen["tables"][name]
        if not table or not table[0] or any(len(row) != len(table[0]) for row in table):
            raise ValueError("target lookup table has invalid dimensions")
        if len(entry["outs"]) != len(table[0]):
            raise ValueError("source lookup table output width differs from target")
        if entry.get("table_bits") != len(table) * len(table[0]) * frozen["width"]:
            raise ValueError("source lookup table size differs from target")
        spec = {
            "op": "lookup", "width": frozen["width"],
            "fraction_bits": frozen["fraction_bits"], "params": node["params"], "table": table,
        }
        expected = {hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]}
        if node["params"].get("lookup_strategy", "shared_prefix") == "shared_prefix":
            for lowering in {LOOKUP_LOWERING, "shared-prefix-xor-v1"}:
                lowered = dict(spec, lowering=lowering)
                expected.add(hashlib.sha256(canonical(lowered).encode()).hexdigest()[:20])
        if key not in expected:
            raise ValueError("source lookup key is not bound to the target table values")

    def _requested_node(self, node):
        if canonical(self.tables) != self._tables_signature:
            raise ValueError("compiler lookup tables changed from the frozen target")
        outputs = node.get("out")
        if not isinstance(outputs, list) or any(type(value) is not int for value in outputs):
            raise ValueError("requested node lacks valid target outputs")
        match = self._nodes.get(tuple(outputs))
        if match is None or canonical(node) != match[1]:
            raise ValueError("requested node semantics differ from the immutable target")
        return match[0]

    def _copy_original(self, key):
        cached = self._cached_entry(key)
        if cached is not None:
            if canonical(cached) != canonical(self.original_entries[key]):
                raise ValueError("fallback cache metadata differs from the archived leaf")
            return key, cached
        self._validate_original_files(key)
        entry = self.original_entries[key]
        for name in (key + ".json", entry["gate_file"]):
            destination = self.path / name
            if destination.exists():
                if digest(destination) != digest(self.archive / name):
                    raise ValueError("fallback cache bytes differ from the archived leaf")
            else:
                shutil.copy2(self.archive / name, destination)
        self._remember_entry(key, copy.deepcopy(entry))
        return key, self.entries[key]

    def _cached_entry(self, key):
        """Use a validated per-compilation entry; a fresh library rechecks disk.

        Source files are checked upfront, and each copied/generated cache key is
        checked before its first use. Root receipts additionally check unique
        gate files after compilation. Avoid rehashing large fallback binaries or
        rescheduling the same constant gates for every financial invocation.
        """
        if key not in self.entries:
            return None
        entry = self.entries[key]
        if canonical(entry) != self._validated_entry_signatures.get(key):
            raise ValueError("in-memory leaf cache metadata changed after validation")
        return entry

    def _remember_entry(self, key, entry):
        self.entries[key] = entry
        self._validated_entry_signatures[key] = canonical(entry)

    def _new_leaf(self, node, spec, builder):
        key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        cached = self._cached_entry(key)
        if cached is not None:
            if (
                canonical(cached.get("spec")) != canonical(spec)
                or canonical(cached.get("input_contract")) != canonical(spec["input_contract"])
                or cached.get("op") != node["op"]
                or canonical(cached.get("params")) != canonical(node["params"])
            ):
                raise ValueError("specialized constant cache spec/contract mismatch")
            return key, cached
        metadata_path, binary = self.path / (key + ".json"), self.path / (key + ".npy")
        if metadata_path.exists() != binary.exists():
            raise ValueError("incomplete specialized constant cache")
        if metadata_path.exists():
            entry = json.loads(metadata_path.read_text())
            if (
                entry.get("key") != key or canonical(entry.get("spec")) != canonical(spec)
                or canonical(entry.get("input_contract")) != canonical(spec["input_contract"])
                or entry.get("op") != node["op"]
                or canonical(entry.get("params")) != canonical(node["params"])
                or entry.get("gate_file") != binary.name
                or digest(binary) != entry.get("sha256")
            ):
                raise ValueError("specialized constant cache metadata/spec/SHA mismatch")
            self._validate_entry_shape(key, entry)
            gates = np.load(binary, allow_pickle=False)
            observed = actual_resources(gates, entry["resources"]["qubits"])
            if any(entry["resources"].get(field) != value for field, value in observed.items()):
                raise ValueError("specialized constant cache resource mismatch")
        else:
            program, arguments, outputs = builder()
            np.save(binary, array_gates(program))
            entry = {
                "key": key, "op": node["op"], "params": copy.deepcopy(node["params"]),
                "spec": copy.deepcopy(spec),
                "input_contract": copy.deepcopy(spec["input_contract"]),
                "args": list(map(list, arguments)), "outs": list(map(list, outputs)),
                "resources": resources(program), "gate_file": binary.name,
                "sha256": digest(binary), "table_bits": 0,
            }
            metadata_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
        self._remember_entry(key, entry)
        return key, entry

    def _record(self, index, node, key, kind, proof):
        if index in self._decided:
            return
        self._decided.add(index)
        decision = {
            "node_index": index, "forward_call_index": self._call_indices[index],
            "outputs": list(node["out"]), "op": node["op"],
            "coefficient": node["params"].get("c"),
            "old_key": self._old_keys[index], "new_key": key,
            "type": kind, "proof": proof,
        }
        self.decisions.append(decision)
        if kind == "log-signed7":
            self.proofs.append(decision)
        elif kind == "general-constant":
            self.general_sites.append(decision)

    def get(self, node):
        index = self._requested_node(node)
        proof = None
        if self.log_strategy is not None:
            proof = prove_log_site(self.context, index)
        if proof is not None:
            spec = leaf_spec(self.log_strategy, "fused-child-copy")
            spec = dict(spec, integration_lowering=INTEGRATION_LOWERING)
            key, entry = self._new_leaf(
                node, spec, lambda: build_log_constant_multiplier(
                    self.log_strategy, "fused-child-copy"
                )
            )
            kind = "log-signed7"
        elif node["op"] == "cmul" and node["params"].get("c") in self.general_replacements:
            coefficient = node["params"]["c"]
            strategy = self.general_replacements[coefficient]
            spec = {
                "op": "cmul", "width": self.w, "fraction_bits": self.f,
                "coefficient": coefficient, "zero_bits": 0,
                "strategy": strategy, "lowering": CONSTANT_LOWERING,
                "integration_lowering": INTEGRATION_LOWERING,
                "input_contract": {"zero_low_bits": 0},
            }
            key, entry = self._new_leaf(
                node, spec,
                lambda: build_constant_multiplier(self.w, self.f, coefficient, 0, strategy),
            )
            proof = {
                "theorem": "Full signed-width constant multiplication with original "
                "floor/shift semantics",
                "input_contract": {"zero_low_bits": 0},
                "coefficient": coefficient, "no_narrowed_input_promise": True,
            }
            kind = "general-constant"
        else:
            key, entry = self._copy_original(self._old_keys[index])
            kind = "fallback"
        self._record(index, node, key, kind, proof)
        return key, entry

    @property
    def counts(self):
        return dict(Counter(decision["type"] for decision in self.decisions))
