"""Frozen finite-target week14 campaign, durable checkpoints and strict replay."""

import argparse
from datetime import datetime, timezone
import inspect
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

import numpy as np
from qiskit.algorithms import IterativeAmplitudeEstimation
from qiskit.primitives import Sampler
import qiskit

from .asian_basket import Basket
from .asian_encoding import grid, price_contract
from .run_w13 import environment, equivalent
from .storage import ROOT, sha256, write_json, rng_for
from .unequal_allocation import ARMS
from .w14_circuits import response, DEPTHS
from .w14_comparators import native_iqae, native_csae
from .w14_inference import fixed_comparison, policy_comparison, classical_comparison


PROTOCOL = "docs/journal_sprint/PROTOCOL_W14_FINITE_V1.md"
INPUT = "results/journal_sprint/w13_encoding_v1"
NAMESPACE = "week14_development_v1"
TRIALS = 16
NATIVE_TRIALS = 8
CONTRACT = Basket(2, 2, 100.0)
PRECISION = 1
APPROVED_NATIVE = {
    "Terra_IQAE": "3f5e35af63e251450322c89f064de2730fa57ae045252d04e819fa9b1c059807",
    "Terra_Sampler": "7379135461d034a98acfdc22e550572309e52f8e178586975254caa6ddbd6608",
}


def configuration():
    return dict(
        namespace=NAMESPACE,
        trials=TRIALS,
        native_trials=NATIVE_TRIALS,
        basket=vars(CONTRACT),
        precision=PRECISION,
        cutoff=3.0,
        representations=["raw", "residual"],
        depths=list(DEPTHS),
        noise_pairs=[[0.0, 0.0], [0.02, 0.02], [0.02, 0.0]],
        transfer_pairs=[[0.0, 0.0], [0.03, 0.0], [0.03, 0.03]],
        arms=list(ARMS),
        tolerance=1.0,
        confirmation=False,
    )


def jsonable(value):
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [jsonable(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def dependencies():
    # Explicit runtime import closure; unrelated historical tests are not producers.
    modules = (
        "run_w14.py",
        "w14_circuits.py",
        "w14_comparators.py",
        "w14_inference.py",
        "w14_analysis.py",
        "asian_basket.py",
        "asian_encoding.py",
        "price_contract.py",
        "encoding_decision.py",
        "intervals.py",
        "storage.py",
        "run_w13.py",
        "unequal_allocation.py",
        "allocation_rule.py",
        "calibrated_readout.py",
        "vendor/mlqae_core.py",
        "vendor/__init__.py",
        "__init__.py",
    )
    files = [ROOT / "research/journal_sprint" / name for name in modules]
    files += [ROOT / "research/__init__.py", ROOT / PROTOCOL]
    return {p.relative_to(ROOT).as_posix(): sha256(p) for p in files}


def native_identity():
    result = {
        name: sha256(inspect.getfile(obj))
        for name, obj in (("Terra_IQAE", IterativeAmplitudeEstimation), ("Terra_Sampler", Sampler))
    }
    if qiskit.__version__ != "0.46.3" or result != APPROVED_NATIVE:
        raise ValueError("requires approved Terra 0.46.3 IQAE/Sampler source")
    return result


def input_identity():
    root = ROOT / INPUT
    manifest = json.loads((root / "complete.json").read_text(encoding="utf-8"))
    actual = {
        p.relative_to(root).as_posix(): sha256(p)
        for p in root.rglob("*")
        if p.is_file() and p != root / "complete.json"
    }
    if actual != {Path(n).as_posix(): h for n, h in manifest["sha256"].items()}:
        raise ValueError("week13 input archive not intact")
    return dict(manifest=sha256(root / "complete.json"), case=sha256(root / "case_3.json"))


def input_record():
    return json.loads((ROOT / INPUT / "case_3.json").read_text(encoding="utf-8"))


def campaign(perform):
    holder = {}

    def setup_task(emit):
        started = time.perf_counter()
        data = grid(CONTRACT, PRECISION, 3.0)
        source = input_record()
        equivalent(source["case"], [CONTRACT.assets, CONTRACT.dates, PRECISION])
        equivalent(source["basket"], vars(CONTRACT))
        for field in ("normals", "weights", "raw", "control"):
            equivalent(source[field], data[field].tolist())
        holder["data"] = data
        return dict(
            setup_seconds=time.perf_counter() - started,
            truth=float(data["weights"] @ data["raw"]),
            finite_control=float(data["weights"] @ data["control"]),
            normals=data["normals"],
            weights=data["weights"],
            raw=data["raw"],
            control=data["control"],
            residual=data["residual"],
            model=data["model"],
            admission={
                rep: price_contract(CONTRACT, PRECISION, 3.0, data, rep).readiness(1.0)
                for rep in ("raw", "residual")
            },
        )

    perform("setup", setup_task)
    data = holder["data"]
    # Exact numerical finite-table target, not the continuous-model price.
    truth = float(data["weights"] @ data["raw"])
    finite_control = float(data["weights"] @ data["control"])
    for representation in ("raw", "residual"):
        scale = float(data[representation].max())
        offset = finite_control if representation == "residual" else 0.0
        amplitude = float(data["weights"] @ data[representation]) / scale
        key = f"{NAMESPACE}:{representation}"
        responses = {}
        for eta in (0.0, 0.02):
            for depth in DEPTHS:
                responses[(depth, eta)] = perform(
                    f"{representation}_response_{int(eta * 100)}_{depth}",
                    lambda emit, k=depth, e=eta: response(data, PRECISION, representation, k, e),
                )
        for pair, (eta, assumed) in enumerate(((0.0, 0.0), (0.02, 0.02), (0.02, 0.0))):
            for method in ("direct_shots", "direct_queries", "depth_limited"):
                perform(
                    f"{representation}_fixed_{pair}_{method}",
                    lambda emit, m=method, e=eta, assumed=assumed: fixed_comparison(
                        responses, scale, offset, truth, m, e, assumed, key, TRIALS, emit
                    ),
                )
            seed = int(rng_for(key, "native_csae", eta).integers(0, 2**32))

            def csae_task(emit, e=eta, assumed=assumed, s=seed):
                result = native_csae(amplitude, s, e, assumed, trials=TRIALS)
                emit("native_output", result)
                result["per_trial_cost"].update(
                    logical_cx=sum(
                        n * responses[(k, e)]["circuit"]["cx"]
                        for k, n in zip(result["depths"], result["shots"])
                    ),
                    maximum_depth=max(
                        responses[(k, e)]["circuit"]["depth"] for k in result["depths"]
                    ),
                    qubits=responses[(0, e)]["circuit"]["qubits"],
                    maximum_measurement_depth=max(
                        responses[(k, e)]["measurement_circuit"]["depth"] for k in result["depths"]
                    ),
                    depth_convention="maximum_depth is unitary-only",
                    evidence_kind="projected_from_measured_circuit_counts",
                )
                result["price_estimates"] = [
                    offset + scale * a for a in result["amplitude_estimates"]
                ]
                result["absolute_errors"] = [abs(p - truth) for p in result["price_estimates"]]
                return result

            perform(f"{representation}_csae_{pair}", csae_task)
        for pair, (drift, guard) in enumerate(((0.0, 0.0), (0.03, 0.0), (0.03, 0.03))):
            for arm in ARMS:
                perform(
                    f"{representation}_policy_{pair}_{arm}",
                    lambda emit, arm=arm, d=drift, g=guard: policy_comparison(
                        amplitude,
                        scale,
                        offset,
                        truth,
                        arm,
                        d,
                        g,
                        key,
                        TRIALS,
                        responses[(0, 0.0)]["circuit"]["cx"],
                        emit,
                    ),
                )
        for trial in range(NATIVE_TRIALS):
            seed = int(rng_for(key, "native_iqae", trial).integers(0, 2**32))

            def native_task(emit, seed=seed):
                from .asian_encoding import circuits

                started = time.perf_counter()
                _, _, preparation = circuits(data, PRECISION, representation, "product")
                preparation_seconds = time.perf_counter() - started

                def checkpoint(stage, event, value):
                    batch = value["batch"]
                    index = batch["batch"] if isinstance(batch, dict) else batch
                    emit(f"{stage}_{event}_{index}", value)

                result = native_iqae(preparation, scale, offset, seed, checkpoint=checkpoint)
                result["preparation_seconds"] = preparation_seconds
                if result["status"] == "error":
                    emit("failed_native_result", result)
                    raise RuntimeError("native IQAE failed; see durable result checkpoint")
                return result

            perform(f"{representation}_iqae_{trial}", native_task)
        perform(
            f"{representation}_classical",
            lambda emit: classical_comparison(
                data, representation, offset, truth, NAMESPACE, TRIALS, emit
            ),
        )


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    active, active_started, pending = "initialization", time.perf_counter(), None
    try:
        sources = dependencies()
        write_json(
            output / "planned.json",
            dict(
                started_utc=datetime.now(timezone.utc).isoformat(),
                config=configuration(),
                git_head=subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
                environment=environment(),
                native_identity=native_identity(),
                sources=sources,
                input_identity=input_identity(),
            ),
        )
        for name in sources:
            destination = output / "sources" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)

        def perform(name, operation):
            nonlocal active, active_started, pending
            active, active_started = f"{name}:start_persistence", time.perf_counter()
            write_json(output / f"{name}__started.json", dict(task=name))
            active, active_started = name, time.perf_counter()

            def emit(child, value):
                nonlocal active, active_started, pending
                if not re.fullmatch(r"[A-Za-z0-9_]+", child):
                    raise ValueError("unsafe checkpoint label")
                pending = jsonable(value)
                active, active_started = f"{name}:{child}:persistence", time.perf_counter()
                write_json(output / f"{name}__{child}.json", pending)
                pending = None
                active, active_started = f"{name}:computation_after_{child}", time.perf_counter()

            started = time.perf_counter()
            result = jsonable(operation(emit))
            pending = result
            active, active_started = f"{name}:result_persistence", time.perf_counter()
            write_json(
                output / f"{name}__result.json",
                dict(value=result, task_seconds=time.perf_counter() - started),
            )
            pending = None
            return result

        campaign(perform)
        active, active_started = "completion", time.perf_counter()
        if dependencies() != sources:
            raise ValueError("producing sources changed during acquisition")
        if any(sha256(output / "sources" / name) != digest for name, digest in sources.items()):
            raise ValueError("copied producing source mismatch")
        native_identity()
        if input_identity() != json.loads((output / "planned.json").read_text())["input_identity"]:
            raise ValueError("input changed during acquisition")
        manifest = dict(
            finished_utc=datetime.now(timezone.utc).isoformat(),
            sha256={
                p.relative_to(output).as_posix(): sha256(p)
                for p in sorted(output.rglob("*"))
                if p.is_file()
            },
        )
        write_json(output / "complete.pending.json", manifest)
        os.rename(output / "complete.pending.json", output / "complete.json")
    except BaseException as error:
        try:
            write_json(
                output / "failure.json",
                dict(
                    type=type(error).__name__,
                    message=str(error),
                    active_stage=active,
                    failed_stage_seconds=time.perf_counter() - active_started,
                    pending_completed_result=pending,
                    unavailable_costs=None,
                    accounting_complete=False,
                ),
            )
        except BaseException:
            pass
        raise
    return dict(output=str(output), development_complete=True, application_admitted=False)


def verify(output):
    output = Path(output)

    def read(name):
        return json.loads((output / name).read_text(encoding="utf-8"))

    complete = read("complete.json")
    if set(complete) != {"finished_utc", "sha256"}:
        raise ValueError("completion schema")
    actual = {
        p.relative_to(output).as_posix(): sha256(p)
        for p in output.rglob("*")
        if p.is_file() and p != output / "complete.json"
    }
    if actual != complete["sha256"]:
        raise ValueError("manifest/inventory mismatch")
    plan = read("planned.json")
    if set(plan) != {
        "started_utc",
        "config",
        "git_head",
        "environment",
        "native_identity",
        "sources",
        "input_identity",
    }:
        raise ValueError("plan schema")
    for key, expected in (
        ("config", configuration()),
        ("environment", environment()),
        ("native_identity", native_identity()),
        ("sources", dependencies()),
        ("input_identity", input_identity()),
    ):
        equivalent(plan[key], expected)
    if not re.fullmatch(r"[0-9a-f]{40}", plan["git_head"]):
        raise ValueError("invalid Git identity")
    start, finish = (
        datetime.fromisoformat(x) for x in (plan["started_utc"], complete["finished_utc"])
    )
    if (
        start.utcoffset() != timezone.utc.utcoffset(None)
        or finish.utcoffset() != start.utcoffset()
        or finish < start
    ):
        raise ValueError("invalid UTC chronology")
    checked = {"planned.json"}
    for name, digest in plan["sources"].items():
        copied = "sources/" + name
        if actual.get(copied) != digest:
            raise ValueError("copied source mismatch")
        checked.add(copied)
    tasks = []

    def perform(name, operation):
        equivalent(read(f"{name}__started.json"), dict(task=name))
        checked.add(f"{name}__started.json")

        def emit(child, value):
            filename = f"{name}__{child}.json"
            equivalent(read(filename), jsonable(value))
            checked.add(filename)

        result = jsonable(operation(emit))
        filename = f"{name}__result.json"
        equivalent(read(filename), dict(value=result, task_seconds=0.0))
        checked.add(filename)
        tasks.append(name)
        return result

    campaign(perform)
    if checked != set(actual):
        raise ValueError("unconsumed or unexpected archive records")
    return dict(
        tasks=len(tasks),
        files=len(actual) + 1,
        full_numerical_replay=True,
        application_admitted=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("run", "verify"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps((run if args.action == "run" else verify)(args.output), indent=2))
