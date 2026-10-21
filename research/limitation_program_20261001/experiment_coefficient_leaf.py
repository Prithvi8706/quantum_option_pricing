"""Prospective exact full-domain coefficient multiplier leaf screen, entirely local."""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
from pathlib import Path
import shutil
import sys
import time

import numpy as np
import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES,
    build_constant_multiplier,
)
from research.controlled_source_completion.prefix_constant_multiplier import (
    build_prefix_constant_multiplier,
)
from research.limitation_program_20261001.prove_coefficient_input import frontier_leaf_spec
from research.controlled_source_completion.primitives import array_gates, resources
from research.limitation_program_20261001.constant_library import (
    actual_resources,
    canonical,
    digest,
)
from research.limitation_program_20261001.experiment_prefix_multiplier import ROOT, read, save

BASELINE = ROOT / "results/limitation_program_20261001/A09_range_run001"
COEFFICIENTS = (1067016148260, 60222732077, 22906492245)
ALL_STRATEGIES = (*STRATEGIES, "binary-prefix-carry-save", "signed-digit-prefix-carry-save")
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


def baseline_leaves():
    matched, inventory, combined_owners = {}, {}, {}
    for case in ("B4x12", "B8x52"):
        source = read(BASELINE / case / "source.json")
        target = read(BASELINE / case / "target.json")
        archive = resolve_library(source)
        metadata = entries(source)
        ledger = read(
            ROOT
            / "results/limitation_program_20261001/A01_run012"
            / (case + "_mixed24-40_trial_ledger.json")
        )
        assert ledger["resources"] == read(BASELINE / case / "schedule_capped.json")["resources"]
        owners = {}
        for batch in ledger["batches"]:
            if batch["dominant_op"] == "cmul":
                c = metadata[batch["dominant_leaf"]]["params"]["c"]
                owners[c] = owners.get(c, 0) + 2 * batch["t_depth"]
                combined_owners[c] = combined_owners.get(c, 0) + 2 * batch["t_depth"]
        nodes = [n for n in target["nodes"] if n["op"] != "input"]
        assert len(nodes) == len(source["forward_calls"])
        sites = []
        for index, (node, call) in enumerate(zip(nodes, source["forward_calls"], strict=True)):
            entry = metadata[call["leaf"]]
            assert (
                node["args"] == call["args"]
                and node["out"] == call["out"]
                and node["op"] == entry["op"]
                and node["params"] == entry["params"]
            )
            c = node["params"].get("c")
            if node["op"] != "cmul" or c not in COEFFICIENTS:
                continue
            assert not entry.get("input_contract")
            if c in matched:
                assert (
                    matched[c][0]["sha256"] == entry["sha256"]
                    and matched[c][0]["resources"] == entry["resources"]
                )
            matched[c] = (entry, archive / (entry["key"] + ".json"), archive / entry["gate_file"])
            sites.append(
                dict(
                    call_index=index,
                    coefficient=c,
                    args=call["args"],
                    out=call["out"],
                    leaf=call["leaf"],
                    gate_sha256=entry["sha256"],
                )
            )
        schedule = read(BASELINE / case / "schedule_capped.json")
        ceilings = {}
        for c in COEFFICIENTS:
            zero_depth = 2 * sum(
                max(
                    (
                        0
                        if metadata[source["forward_calls"][i]["leaf"]]["op"] == "cmul"
                        and metadata[source["forward_calls"][i]["leaf"]]["params"]["c"] == c
                        else metadata[source["forward_calls"][i]["leaf"]]["resources"]["t_depth"]
                        for i in batch["call_indices"]
                    ),
                    default=0,
                )
                for batch in schedule["groups"]
            )
            ceilings[str(c)] = schedule["resources"]["t_depth"] - zero_depth
        inventory[case] = dict(
            actual_declared_sites=sites,
            optimistic_fixed_batch_zero_cost_saving=ceilings,
            accepted_full_t_depth=schedule["resources"]["t_depth"],
            constant_depth_owners=[
                dict(coefficient=c, owned_t_depth=value)
                for c, value in sorted(owners.items(), key=lambda row: (-row[1], row[0]))
            ],
        )
    ranking = sorted(combined_owners, key=lambda c: (-combined_owners[c], c))
    assert tuple(ranking[:3]) == COEFFICIENTS and set(matched) == set(COEFFICIENTS)
    assert all(
        any(
            1000 * row["optimistic_fixed_batch_zero_cost_saving"][str(c)]
            >= row["accepted_full_t_depth"]
            for row in inventory.values()
        )
        for c in COEFFICIENTS
    )
    return matched, dict(
        cases=inventory,
        combined_ranking=[dict(coefficient=c, owned_t_depth=combined_owners[c]) for c in ranking],
        selected_coefficients=list(COEFFICIENTS),
    )


def run(output):
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    assert read(BASELINE / "summary.json")["accepted"]
    matched, inventory = baseline_leaves()
    output.mkdir(exist_ok=False)
    names = (
        "research/limitation_program_20261001/experiment_coefficient_leaf.py",
        "research/controlled_source_completion/prefix_constant_multiplier.py",
        "research/limitation_program_20261001/test_coefficient_frontier.py",
        "research/controlled_source_completion/prefix_multiplier.py",
        "research/controlled_source_completion/constant_multiplier.py",
        "research/limitation_program_20261001/prove_coefficient_input.py",
        "research/controlled_source_completion/carry_lookahead.py",
        "research/controlled_source_completion/primitives.py",
        "research/controlled_source_completion/exact_lookup.py",
        "research/journal_sprint/reversible_fixed_point.py",
        "research/antithetic_feasibility/reversible.py",
        "research/limitation_program_20261001/constant_library.py",
        "research/limitation_program_20261001/experiment_prefix_multiplier.py",
    )
    frozen, snapshots = {}, []
    for name in names:
        path = ROOT / name
        snapshot = output / "executed_code" / path.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen[name] = digest(path)
        snapshots.append(
            dict(source=name, snapshot=str(snapshot.relative_to(output)), sha256=digest(snapshot))
        )
    for _, metadata, binary in matched.values():
        for path in (metadata, binary):
            frozen[str(path.relative_to(ROOT))] = digest(path)
    for case in ("B4x12", "B8x52"):
        for name in ("target.json", "source.json", "schedule_capped.json"):
            path = BASELINE / case / name
            frozen[str(path.relative_to(ROOT))] = digest(path)
    for path in (
        BASELINE / "manifest.json",
        ROOT / "results/limitation_program_20261001/A01_run012/manifest.json",
    ):
        frozen[str(path.relative_to(ROOT))] = digest(path)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        item="A10 top-three exact full-domain coefficients",
        before_recorded_tests_and_cost=True,
        families=["existing-four-exact-constant-strategies", "CSA-with-clean-Brent-Kung-prefix"],
        coefficients=list(COEFFICIENTS),
        strategies=list(ALL_STRATEGIES),
        candidates=[
            dict(coefficient=c, strategy=strategy)
            for c in COEFFICIENTS
            for strategy in ALL_STRATEGIES
        ],
        width=72,
        fraction_bits=40,
        source_portfolios=["min-depth", "min-work"],
        baseline=str(BASELINE.relative_to(ROOT)),
        baseline_coefficients={str(c): matched[c][0] for c in COEFFICIENTS},
        zero_bits=0,
        inventory=inventory,
        semantics="Full native72 input and arbitrary72 output XOR floor(signed(x)*coefficient/2^40) mod2^72; unrestricted signed input, zero_bits=0; all input and scratch restored.",
        storage="Full112-bit correction and low carry columns, exact shift-add or retained CSA history, ripple/prefix final sum, native output copy and literal inverse all charged.",
        required_checks="Exhaust small signed x/coefficients/fractions with dirty output and inverse; native24/40/72, all three actual coefficients across all6 strategies, extrema/power boundaries/tiny negatives/randoms; invalid boolean parameters and structural cleanup.",
        resource_dimensions=list(DIMENSIONS),
        dominance="Dominance only within SAME coefficient including baseline and all six candidate strategies: all four dimensions<= and at least one<. Source may use only nondominated leaves with strict baseline improvement and Twork or qubits strictly improved.",
        stop_rule="Exactly three declared coefficients, four existing strategies and two prefix variants; at most two distinct source portfolios. Freeze min-depth and min-work per-coefficient selection; skip coefficients whose optimistic attribution is below0.1% of current source. No input narrowing/extra coefficients; semantic failure stops;30 process CPU minutes.",
        exclusions="No financial/source gain or advantage claim at leaf stage; G2-G5 remain open.",
        executed_dependencies=snapshots,
        dependencies=frozen,
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            executable_sha256=digest(Path(sys.executable)),
            packages={n: version(n) for n in ("numpy", "numba", "pytest")},
        ),
    )
    save(output / "protocol.json", protocol)
    save(output / "coefficient_inventory.json", inventory)
    print("Prospective coefficient frontier leaf protocol saved", flush=True)
    wall, cpu = time.perf_counter(), time.process_time()
    try:
        test_exit = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_coefficient_frontier.py"),
                "-q",
                "--junitxml=" + str(output / "regression.xml"),
            ]
        )
        if test_exit:
            raise AssertionError("Exact coefficient frontier tests failed")
        baselines, candidates = {}, []
        for c in COEFFICIENTS:
            old_entry, _, old_binary = matched[c]
            old = old_entry["resources"]
            actual_old = actual_resources(np.load(old_binary, allow_pickle=False), old["qubits"])
            assert all(old[n] == value for n, value in actual_old.items())
            baselines[str(c)] = old
            for strategy in ALL_STRATEGIES:
                if time.process_time() - cpu > 1800:
                    raise TimeoutError("Declared leaf CPU ceiling exceeded")
                builder = (
                    build_prefix_constant_multiplier
                    if "prefix" in strategy
                    else build_constant_multiplier
                )
                if "prefix" in strategy:
                    program, args, outs = builder(72, 40, c, strategy)
                else:
                    program, args, outs = builder(72, 40, c, zero_bits=0, strategy=strategy)
                spec = frontier_leaf_spec(72, 40, c, strategy)
                key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
                binary = output / (key + ".npy")
                np.save(binary, array_gates(program))
                metadata = dict(
                    coefficient_frontier="full-native-unrestricted-signed-v1",
                    key=key,
                    op="cmul",
                    params={"c": c},
                    spec=spec,
                    input_contract={"zero_low_bits": 0},
                    args=[list(a) for a in args],
                    outs=[list(o) for o in outs],
                    resources=resources(program),
                    gate_file=binary.name,
                    sha256=digest(binary),
                )
                save(output / (key + ".json"), metadata)
                candidates.append(dict(coefficient=c, strategy=strategy, metadata=metadata))
                print("exact coefficient", c, strategy, metadata["resources"], flush=True)
        for row in candidates:
            old = baselines[str(row["coefficient"])]
            new = row["metadata"]["resources"]
            peers = [old] + [
                other["metadata"]["resources"]
                for other in candidates
                if other["coefficient"] == row["coefficient"]
            ]
            dominated = any(
                all(peer[n] <= new[n] for n in DIMENSIONS)
                and any(peer[n] < new[n] for n in DIMENSIONS)
                for peer in peers
            )
            improves = any(new[n] < old[n] for n in DIMENSIONS)
            work_or_space = new["t_count"] < old["t_count"] or new["qubits"] < old["qubits"]
            row.update(
                leaf_nondominated=not dominated,
                any_resource_improvement=improves,
                clean_leaf_work_or_scratch_improved=work_or_space,
                source_screen_allowed=not dominated and improves and work_or_space,
            )
        result = dict(
            passed=True,
            candidates=candidates,
            baseline_coefficients=baselines,
            source_screen_allowed=any(c["source_screen_allowed"] for c in candidates),
            same_integer_function_unrestricted_signed_input=True,
            source_gain_claimed=False,
            financial_gate_replays_run=False,
            elapsed_seconds=time.perf_counter() - wall,
            cpu_seconds=time.process_time() - cpu,
        )
        save(output / "summary.json", result)
        assert all(digest(ROOT / name) == value for name, value in frozen.items())
        assert read(output / "protocol.json") == protocol
        save(
            output / "verification.json",
            dict(passed=True, pytest_exit_code=int(test_exit), dependencies_unchanged=True),
        )
    except Exception as error:
        save(
            output / "failure.json", dict(passed=False, type=type(error).__name__, error=str(error))
        )
        raise
    finally:
        files = {
            str(path.relative_to(ROOT)): digest(path)
            for path in output.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        }
        save(output / "manifest.json", dict(files=files, frozen_inputs=frozen))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)
