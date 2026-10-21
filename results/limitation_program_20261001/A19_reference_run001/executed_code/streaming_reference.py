"""Capture the unchanged B2x4 financial template and reuse proved native leaves.

No streaming schedule is executed here. The optional compiler creates a new
matched control source; every reused range contract is proved at its actual B2
site against the complete original graph before archived bytes are copied.
"""

from __future__ import annotations

from collections import Counter
import copy
import json
import math
from pathlib import Path
import shutil

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v7 import _storage, fingerprint
from research.controlled_source_completion.compiler import compile_graph, resolve_library
from research.controlled_source_completion.ir import Graph
from research.controlled_source_completion.optimize import optimize
from research.limitation_program_20261001.baseline import fingerprints
from research.limitation_program_20261001.coefficient_library import CoefficientIntegrationLibrary
from research.limitation_program_20261001.constant_library import canonical, digest


ROOT = Path(__file__).resolve().parents[2]
ACCEPTED = ROOT / "results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth"


def build_reference():
    """Label actual Gaussian, raw-log, stock, basket and payoff template roots."""
    from research.advantage_frontier_20260923 import barrier_oracle_depth as builder

    normal_roots, exponential_roots, clip_arguments = [], [], {}
    saved_normals, saved_exp, saved_clip = builder.normals_graph, builder.exp_estrin, Graph.clip

    def capture_normals(graph, count, q):
        result = saved_normals(graph, count, q)
        normal_roots.extend(result)
        return result

    def capture_exp(graph, value):
        out = saved_exp(graph, value)
        exponential_roots.append((value, out))
        return out

    def capture_clip(graph, value, low, high):
        out = saved_clip(graph, value, low, high)
        clip_arguments[out] = (value, low, high)
        return out

    builder.normals_graph, builder.exp_estrin, Graph.clip = (
        capture_normals,
        capture_exp,
        capture_clip,
    )
    try:
        original = json.loads(json.dumps(builder.build(2, 4, q=32).as_dict()))
    finally:
        builder.normals_graph, builder.exp_estrin, Graph.clip = (
            saved_normals,
            saved_exp,
            saved_clip,
        )
    target = optimize(copy.deepcopy(original))
    before, after = fingerprints(original), fingerprints(target)
    reverse = {token: value for value, token in after.items()}
    if len(reverse) != len(after):
        raise ValueError("Ambiguous optimized structural fingerprints")
    if len(normal_roots) != 12 or len(exponential_roots) != 8:
        raise ValueError("Unexpected B2x4 builder template order")

    def mapped(value):
        return reverse[before[value]]

    normals = [mapped(value) for value in normal_roots]
    raw_logs, clips, stocks = [], [], []
    for asset in range(2):
        raw_row, clip_row, stock_row = [], [], []
        for date in range(4):
            clipped, stock = exponential_roots[asset * 4 + date]
            if clipped not in clip_arguments:
                raise ValueError("Stock exponent is not bound to captured log clipping")
            raw, low, high = clip_arguments[clipped]
            raw_row.append(mapped(raw))
            clip_row.append(mapped(clipped))
            stock_row.append(mapped(stock))
        raw_logs.append(raw_row)
        clips.append(clip_row)
        stocks.append(stock_row)
    nodes = target["nodes"]
    producers = {value: node for node in nodes for value in node["out"]}
    modulus, quantum = 1 << target["width"], 1 << target["fraction_bits"]
    dt = builder.T / 4
    common_coefficient = round(builder.SIGMA * math.sqrt(dt * builder.CORR) * quantum)
    idio_coefficient = round(builder.SIGMA * math.sqrt(dt * (1 - builder.CORR)) * quantum)
    drift = round((builder.RATE - 0.5 * builder.SIGMA**2) * dt * quantum)
    increments = {}
    for node in nodes:
        if node["op"] != "add":
            continue
        operands = [producers[value] for value in node["args"]]
        fixed = [n for n in operands if n["op"] == "const"]
        noise = [n for n in operands if n["op"] == "add"]
        if len(fixed) != 1 or len(noise) != 1:
            continue
        if fixed[0]["params"]["value"] != drift % modulus:
            continue
        terms = [producers[value] for value in noise[0]["args"]]
        if any(term["op"] != "cmul" for term in terms):
            continue
        common = [term for term in terms if term["params"]["c"] == common_coefficient]
        idio = [term for term in terms if term["params"]["c"] == idio_coefficient]
        if len(common) == len(idio) == 1:
            key = (common[0]["args"][0], idio[0]["args"][0])
            if key in increments:
                raise ValueError("Ambiguous financial increment template")
            increments[key] = node["out"][0]
    if len(increments) != 8:
        raise ValueError("Complete correlation/drift increment template not found")
    dates = []
    for date in range(4):
        stock_values = [stocks[asset][date] for asset in range(2)]
        basket_nodes = []
        for node in nodes:
            if node["op"] != "cmul" or node["params"]["c"] != quantum // 2:
                continue
            total = producers[node["args"][0]]
            if total["op"] == "add" and sorted(total["args"]) == sorted(stock_values):
                basket_nodes.append(node)
        if len(basket_nodes) != 1:
            raise ValueError("Unique monitored arithmetic basket template not found")
        common_normal = normals[date * 3]
        idio_normals = [normals[date * 3 + 1 + asset] for asset in range(2)]
        dates.append(
            {
                "date": date,
                "raw_log_values": [raw_logs[asset][date] for asset in range(2)],
                "clipped_log_values": [clips[asset][date] for asset in range(2)],
                "stock_values": stock_values,
                "common_normal_value": common_normal,
                "idiosyncratic_normal_values": idio_normals,
                "increment_values": [increments[(common_normal, n)] for n in idio_normals],
                "basket_value": basket_nodes[0]["out"][0],
                "basket_sum_value": basket_nodes[0]["args"][0],
            }
        )
    output = producers[target["outputs"]["Y"]]
    if output["op"] != "select":
        raise ValueError("Financial output is not the original alive/payoff selection")
    alive, payoff, zero = output["args"]
    alive_node, payoff_node = producers[alive], producers[payoff]
    if alive_node["op"] != "lt" or payoff_node["op"] != "cmul":
        raise ValueError("Financial barrier or discount boundary changed")
    maximum, barrier = alive_node["args"]
    positive = payoff_node["args"][0]
    positive_node = producers[positive]
    if positive_node["op"] != "positive":
        raise ValueError("Original positive payoff boundary changed")
    strike_difference = positive_node["args"][0]
    strike_node = producers[strike_difference]
    if strike_node["op"] != "sub":
        raise ValueError("Original strike subtraction boundary changed")
    average, strike = strike_node["args"]
    average_node = producers[average]
    if average_node["op"] != "cmul" or average_node["params"]["c"] != quantum // 8:
        raise ValueError("Original Asian averaging boundary changed")
    constants = {node["params"]["value"]: node["out"][0] for node in nodes if node["op"] == "const"}
    semantics = {
        "format": "exact-monitored-B2x4-reference-v1",
        "assets": 2,
        "dates": 4,
        "word_width": target["width"],
        "fraction_bits": target["fraction_bits"],
        "uniform_bits_each": 32,
        "normal_values": normals,
        "date_bindings": dates,
        "initial_log_value": constants[round(math.log(builder.S0) * quantum)],
        "global_constant_values": sorted(constants.values()),
        "barrier_value": barrier,
        "strike_value": strike,
        "zero_value": zero,
        "maximum_basket_value": maximum,
        "alive_value": alive,
        "asian_sum_value": average_node["args"][0],
        "average_value": average,
        "strike_difference_value": strike_difference,
        "positive_payoff_value": positive,
        "discounted_payoff_value": payoff,
        "output_value": target["outputs"]["Y"],
        "discount_coefficient": payoff_node["params"]["c"],
        "average_coefficient": average_node["params"]["c"],
        "common_coefficient": common_coefficient,
        "idiosyncratic_coefficient": idio_coefficient,
        "drift_word": drift % modulus,
        "count_width": (4 + 1).bit_length(),
        "barrier_tie": "basket >= H knocks out; all baskets < H survives",
        "integer_update_identity": (
            "Raw log and Asian-sum addition is modulo 2^72; "
            "associativity preserves the exact prefix/tree result. "
            "Clipped logs never feed later dates."
        ),
        "original_fingerprint": fingerprint(original),
        "target_fingerprint": fingerprint(target),
        "stock_structural_fingerprints": [[after[value] for value in row] for row in stocks],
        "builder_files": {
            path: digest(ROOT / path)
            for path in (
                "research/advantage_frontier_20260923/barrier_oracle_depth.py",
                "research/controlled_source_completion/finance.py",
                "research/controlled_source_completion/ir.py",
                "research/controlled_source_completion/optimize.py",
                "research/limitation_program_20261001/baseline.py",
            )
        },
    }
    return original, target, semantics


class StreamingPortfolioLibrary(CoefficientIntegrationLibrary):
    """Reuse immutable accepted kernels only after guards pass at new sites."""

    def __init__(self, path, target, generic_source, accepted_directory=ACCEPTED):
        directory = Path(accepted_directory)
        accepted_target = json.loads((directory / "target.json").read_text(encoding="utf-8"))
        accepted_source = json.loads((directory / "source.json").read_text(encoding="utf-8"))
        self.accepted_metadata = entries(accepted_source)
        self.accepted_archive = resolve_library(accepted_source)
        _storage(accepted_target, accepted_source, self.accepted_metadata)
        if (accepted_target["width"], accepted_target["fraction_bits"]) != (
            target["width"],
            target["fraction_bits"],
        ):
            raise ValueError("Accepted leaf native precision differs from new exact target")
        self.accepted_file_hashes = {}
        for key, entry in self.accepted_metadata.items():
            for file in (
                self.accepted_archive / (key + ".json"),
                self.accepted_archive / entry["gate_file"],
            ):
                self.accepted_file_hashes[str(file.relative_to(ROOT)).replace("\\", "/")] = digest(
                    file
                )
            if digest(self.accepted_archive / entry["gate_file"]) != entry["sha256"]:
                raise ValueError("Accepted portfolio native leaf hash differs")
        self.reuse_decisions = []
        super().__init__(path, target, generic_source, replacements={})

    def get(self, node):
        index = self._requested_node(node)
        eligible, rejected = [], []
        for key, entry in self.accepted_metadata.items():
            if entry["op"] != node["op"] or canonical(entry["params"]) != canonical(node["params"]):
                continue
            if len(entry["args"]) != len(node["args"]) or len(entry["outs"]) != len(node["out"]):
                continue
            try:
                self._validate_entry_shape(key, entry)
                self._validate_original_contract(index, node, entry)
                if node["op"] == "lookup":
                    self._validate_lookup_binding(self.context.target, node, key, entry)
            except ValueError as error:
                rejected.append({"key": key, "reason": str(error)})
                continue
            eligible.append((key, entry))
        if not eligible:
            key, entry = self._copy_original(self._old_keys[index])
            kind = "new-site-full-native-generic-fallback"
        else:
            key, entry = min(
                eligible,
                key=lambda pair: (
                    pair[1]["resources"]["t_depth"],
                    pair[1]["resources"]["t_count"],
                    pair[1]["resources"]["qubits"],
                    pair[0],
                ),
            )
            for filename in (key + ".json", entry["gate_file"]):
                source_file, destination = self.accepted_archive / filename, self.path / filename
                if destination.exists():
                    if digest(destination) != digest(source_file):
                        raise ValueError("Accepted native leaf copy collided with different bytes")
                else:
                    shutil.copy2(source_file, destination)
            self._remember_entry(key, copy.deepcopy(entry))
            kind = "accepted-native-function-actual-site-guard-proved"
        self.reuse_decisions.append(
            {
                "node_index": index,
                "outputs": list(node["out"]),
                "op": node["op"],
                "leaf": key,
                "kind": kind,
                "rejected_typed_candidates": rejected,
            }
        )
        return key, entry


def compile_reference(target, directory, accepted_directory=ACCEPTED):
    """Inventory-only new matched SSA source, with no candidate schedule/replay."""
    directory = Path(directory)
    if directory.exists():
        raise FileExistsError("B2 reference compilation directory must be fresh")
    generic, _ = compile_graph(target, directory / "generic")
    library = StreamingPortfolioLibrary(
        directory / "matched/leaves", target, generic, accepted_directory
    )
    source, _ = compile_graph(target, directory / "matched", library)
    _storage(target, source, entries(source))
    report = {
        "new_reference_source_only": True,
        "candidate_schedule_generated": False,
        "gate_replay_executed": False,
        "generic_source_fingerprint": fingerprint(generic),
        "matched_source_fingerprint": fingerprint(source),
        "target_fingerprint": fingerprint(target),
        "selection_rule": (
            "Actual native function and complete new-site typed guards; minimum frozen "
            "accepted T-depth, T-count, native qubits, key; otherwise generic native fallback"
        ),
        "reuse_counts": dict(Counter(row["kind"] for row in library.reuse_decisions)),
        "reuse_decisions": library.reuse_decisions,
        "accepted_file_hashes": library.accepted_file_hashes,
        "whole_original_typed_storage_validated": True,
    }
    (directory / "reference_compilation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return source, report
