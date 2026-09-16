"""Exclusive finite-circuit feasibility archive and environment-scoped replay."""

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json
import math
import os
import platform
from pathlib import Path
import re
import shutil
import subprocess
import time

import numpy as np
import qiskit
import scipy

from .asian_basket import Basket, evaluate, normal_points
from .asian_encoding import grid, price_contract, measure, analytic_bounds
from .storage import ROOT, write_json, sha256, rng_for


CASES = ((1, 2, 1), (1, 2, 2), (1, 2, 3), (2, 2, 1), (2, 2, 2), (2, 3, 1))
NAMESPACE = "week13_development_v1"
STRIKE = 100.0
POWER = 12
SCRAMBLES = 16
PROTOCOL = "docs/journal_sprint/PROTOCOL_W13_ENCODING_V1.md"
SOURCES = (
    "research/journal_sprint/asian_encoding.py", "research/journal_sprint/run_w13.py",
    "research/journal_sprint/asian_basket.py", "research/journal_sprint/price_contract.py",
    "research/journal_sprint/encoding_decision.py", "research/journal_sprint/storage.py",
    "research/journal_sprint/intervals.py", "research/journal_sprint/__init__.py",
    "research/__init__.py",
    PROTOCOL,
)


def configuration():
    return dict(cases=[list(c) for c in CASES], namespace=NAMESPACE, cutoff=3.0,
                tolerance=1.0, strike=STRIKE, rqmc_power=POWER, scrambles=SCRAMBLES,
                representation=["raw", "residual"], loaders=["product", "dense"])


def classical_reference(contract, data, case, namespace, power=12, scrambles=16):
    started = time.perf_counter()
    replicates = []
    for rep in range(scrambles):
        seed = int(rng_for(namespace, "rqmc_reference", case, rep).integers(0, 2**32))
        normals = normal_points(contract.assets * contract.dates, power, seed, "rqmc_raw")
        raw, control, _ = evaluate(contract, data["model"], normals)
        replicates.append(dict(seed=seed, raw=float(raw.mean()),
                               residual=float((raw - control).mean())
                               + data["model"]["expected_control"],
                               raw_path_sample_variance=float(np.var(raw, ddof=1)),
                               residual_path_sample_variance=float(np.var(raw-control, ddof=1))))
    summaries = {}
    for name in ("raw", "residual"):
        values = [r[name] for r in replicates]
        summaries[name] = dict(mean=float(np.mean(values)),
                               standard_error=float(np.std(values, ddof=1) / math.sqrt(scrambles)))
    return dict(replicates=replicates, summaries=summaries,
                shared_path_evaluations=scrambles * 2**power,
                seconds=time.perf_counter() - started, certified=False)


def execute_case(case, checkpoint=None):
    checkpoint = checkpoint or (lambda *args: None)
    assets, dates, precision = case
    contract = Basket(assets, dates, STRIKE)
    checkpoint("started", "setup", None)
    started = time.perf_counter()
    data = grid(contract, precision, 3.0)
    setup_seconds = time.perf_counter() - started
    checkpoint("finished", "setup", dict(seconds=setup_seconds))
    checkpoint("started", "reference", None)
    classical = classical_reference(contract, data, case, NAMESPACE, POWER, SCRAMBLES)
    checkpoint("finished", "reference", classical)
    rows = []
    for representation in ("raw", "residual"):
        started = time.perf_counter()
        expectation = float(data["weights"] @ data[representation])
        finite_control = float(data["weights"] @ data["control"])
        finite_price = expectation + (finite_control if representation == "residual" else 0)
        finite_sum_seconds = time.perf_counter() - started
        pc = price_contract(contract, precision, 3.0, data, representation)
        variance = float(data["weights"] @ (data[representation] - expectation)**2)
        measured = []
        for loader in ("product", "dense"):
            stage = f"{representation}_{loader}"
            checkpoint("started", stage, None)
            result = measure(data, precision, representation, loader)
            checkpoint("finished", stage, result)
            measured.append(result)
        rows.append(dict(representation=representation, expectation=expectation,
                         finite_control=finite_control, finite_price=finite_price,
                         application_approximation=pc.offset + expectation,
                         application_minus_finite=(pc.offset - finite_control
                                                   if representation == "residual" else 0.0),
                         variance=variance, contract=asdict(pc), readiness=pc.readiness(1.0),
                         analytic_bounds=analytic_bounds(contract, precision, 3.0,
                                                         data["model"], representation),
                         finite_sum_seconds=finite_sum_seconds,
                         circuits=measured))
    if abs(rows[0]["finite_price"] - rows[1]["finite_price"]) > 1e-10:
        raise ArithmeticError("raw/residual finite targets disagree")
    return dict(case=list(case), basket=asdict(contract), setup_seconds=setup_seconds,
                normals=data["normals"].tolist(), weights=data["weights"].tolist(),
                factor=data["model"]["factor"].tolist(), means=data["model"]["means"].tolist(),
                raw=data["raw"].tolist(), control=data["control"].tolist(),
                classical_reference=classical, rows=rows)


def environment():
    return dict(qiskit=qiskit.__version__, platform=platform.platform(),
                python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                threads={k: os.environ.get(k) for k in
                         ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")})


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)  # Ownership established; existing outputs untouched.
    active = "initialization"
    active_started = time.perf_counter()
    pending_completed_result = None
    try:
        identities = {n: sha256(ROOT / n) for n in SOURCES}
        write_json(output / "planned.json", dict(
            started_utc=datetime.now(timezone.utc).isoformat(), config=configuration(),
            git_head=subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                    capture_output=True, text=True, check=True).stdout.strip(),
            source_sha256=identities, environment=environment()))
        copied = output / "sources"
        for name in SOURCES:
            target = copied / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        write_json(output / "source_identity.json", identities)
        write_json(output / "environment.json", environment())
        for index, case in enumerate(CASES):
            active, active_started = f"case_{index}:start_persistence", time.perf_counter()
            write_json(output / f"started_{index}.json", dict(case=list(case), index=index))
            def checkpoint(event, stage, value):
                nonlocal active, active_started, pending_completed_result
                active = f"case_{index}:{stage}:checkpoint_{event}"
                active_started = time.perf_counter()
                pending_completed_result = value if event == "finished" else None
                write_json(output / f"stage_{index}_{stage}_{event}.json",
                           dict(stage=stage, event=event, value=value))
                pending_completed_result = None
                active = (f"case_{index}:{stage}" if event == "started"
                          else f"case_{index}:reconstruction")
                active_started = time.perf_counter()
            result = execute_case(case, checkpoint)
            active, active_started = f"case_{index}:result_persistence", time.perf_counter()
            write_json(output / f"case_{index}.json", result)
            active, active_started = f"case_{index}:finish_persistence", time.perf_counter()
            write_json(output / f"finished_{index}.json", dict(case=list(case), index=index))
        active, active_started = "completion", time.perf_counter()
        manifest = dict(finished_utc=datetime.now(timezone.utc).isoformat(), sha256={
            p.relative_to(output).as_posix(): sha256(p)
            for p in sorted(output.rglob("*")) if p.is_file()})
        write_json(output / "complete.pending.json", manifest)
        os.rename(output / "complete.pending.json", output / "complete.json")
    except BaseException as exc:
        try:
            write_json(output / "failure.json", dict(type=type(exc).__name__, message=str(exc),
                active_stage=active, failed_stage_seconds=time.perf_counter()-active_started,
                pending_completed_result=pending_completed_result,
                unavailable_counts=None, accounting_complete=False))
        except BaseException:
            pass  # Preserve original error and partial evidence even on disk failure.
        raise
    return dict(cases=len(CASES), circuits=len(CASES) * 4, archive=str(output))


def equivalent(actual, expected):
    """Compare full schema; timings validated but not equality-replayed."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise ValueError("replay schema mismatch")
        for key in expected:
            if key.endswith("seconds") and expected[key] is not None:
                if (isinstance(actual[key], bool) or not isinstance(actual[key], (float, int))
                        or not math.isfinite(actual[key]) or actual[key] < 0):
                    raise ValueError("invalid recorded timing")
            else:
                equivalent(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ValueError("replay length mismatch")
        for a, b in zip(actual, expected):
            equivalent(a, b)
    elif isinstance(expected, float):
        if (isinstance(actual, bool) or not isinstance(actual, (int, float))
                or not math.isfinite(actual)
                or not math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-10)):
            raise ValueError("numerical replay mismatch")
    elif type(actual) is not type(expected) or actual != expected:
        raise ValueError("replay value mismatch")


def verify(output):
    output = Path(output)
    def read(name):
        return json.loads((output / name).read_text(encoding="utf-8"))
    expected_files = {"planned.json", "source_identity.json", "environment.json"}
    expected_files |= {f"sources/{name}" for name in SOURCES}
    expected_files |= {f"{prefix}_{i}.json" for i in range(len(CASES))
                       for prefix in ("started", "case", "finished")}
    stages = ("setup", "reference", "raw_product", "raw_dense",
              "residual_product", "residual_dense")
    expected_files |= {f"stage_{i}_{stage}_{event}.json" for i in range(len(CASES))
                       for stage in stages for event in ("started", "finished")}
    actual_files = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual_files != expected_files | {"complete.json"}:
        raise ValueError("unexpected/missing archive files or incomplete run")
    completion = read("complete.json")
    if not isinstance(completion, dict) or set(completion) != {"finished_utc", "sha256"}:
        raise ValueError("completion schema mismatch")
    hashes = completion["sha256"]
    if {Path(name).as_posix() for name in hashes} != expected_files:
        raise ValueError("manifest inventory mismatch")
    for name, value in hashes.items():
        if sha256(output / name) != value:
            raise ValueError("manifest checksum mismatch")
    identities = read("source_identity.json")
    if set(identities) != set(SOURCES):
        raise ValueError("source inventory mismatch")
    for name, value in identities.items():
        if value != sha256(ROOT / name) or value != sha256(output / "sources" / name):
            raise ValueError("producing source mismatch; replay in producing checkout")
    plan = read("planned.json")
    if (not isinstance(plan, dict) or set(plan) !=
            {"started_utc", "config", "git_head", "source_sha256", "environment"}):
        raise ValueError("plan schema mismatch")
    equivalent(plan["config"], configuration())
    equivalent(plan["source_sha256"], identities)
    equivalent(read("environment.json"), environment())
    equivalent(plan["environment"], read("environment.json"))
    if not isinstance(plan["git_head"], str) or not re.fullmatch(r"[0-9a-f]{40}", plan["git_head"]):
        raise ValueError("invalid Git identity")
    try:
        start = datetime.fromisoformat(plan["started_utc"])
        end = datetime.fromisoformat(completion["finished_utc"])
        if (start.utcoffset() != timezone.utc.utcoffset(None)
                or end.utcoffset() != start.utcoffset() or end < start):
            raise ValueError("invalid timestamp chronology")
    except (TypeError, AttributeError) as exc:
        raise ValueError("invalid timestamp") from exc
    for i, case in enumerate(CASES):
        for prefix in ("started", "finished"):
            equivalent(read(f"{prefix}_{i}.json"), dict(case=list(case), index=i))
        def checkpoint(event, stage, value):
            equivalent(read(f"stage_{i}_{stage}_{event}.json"),
                       dict(stage=stage, event=event, value=value))
        equivalent(read(f"case_{i}.json"), execute_case(case, checkpoint))
    return dict(verified_cases=len(CASES), verified_circuits=len(CASES) * 4,
                files=len(actual_files), numerical_replay=True, certified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["run", "verify"])
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps((run if args.action == "run" else verify)(args.output), indent=2))


if __name__ == "__main__":
    main()
