"""Exclusive, source-bound acquisition of six fixed logical implementations."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from importlib.metadata import version
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import threading
import time

import psutil
from qiskit import QuantumCircuit

from research.assessment_20260921.label_bridge import label_amplitude
from research.assessment_20260921.verify_label_bridge import pi_bounds
from research.journal_sprint.asian_basket import setup
from research.journal_sprint.factorized_signal import projected_phase
from research.journal_sprint.reflection_centered_signal import phase_on_word, signal_circuit
from research.journal_sprint.reviewed_reflection_signal import ReviewedReflectionSignal
from research.journal_sprint.run_minimal_pivot_week2 import CASES, contract_of
from research.journal_sprint.week2_pipeline import controlled_zero, loader
from research.stronger_arithmetic.components import components
from research.stronger_arithmetic.residual_components import residual_components
from research.stronger_arithmetic.run_study import make_plan

from .compiler import Profile, ae_profile, arithmetic_profile, compile_block, controlled

ROOT = Path(__file__).resolve().parents[2]
BASE = "results/journal_sprint/"
PRIMARY = BASE + "stronger_arithmetic_v1/"
RESIDUAL = BASE + "signed_residual_arithmetic_v1/"
APPROX = BASE + "normalization_approximation_v1/"
PROTOCOL = "docs/release/COMMON_COMPILATION_PROTOCOL_20260922.md"
SOURCES = [
    "research/common_compilation_20260922",
    "research/stronger_arithmetic",
    "research/journal_sprint",
    "research/assessment_20260921",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


class Acquisition:
    def __init__(self, output):
        self.output = Path(output)
        self.started_cpu = time.process_time()
        self.started_wall = time.perf_counter()
        self.inputs = {}
        self.peak_rss = 0
        self.stop = threading.Event()
        self.sources = {}

    def read(self, name):
        self.inputs[name] = digest(ROOT / name)
        return json.loads((ROOT / name).read_text(encoding="utf-8"))

    def guard(self):
        process = psutil.Process()
        while not self.stop.wait(0.5):
            self.peak_rss = max(self.peak_rss, process.memory_info().rss)
            if time.process_time() - self.started_cpu > 7200 or self.peak_rss > 16 * 1024**3:
                write(
                    self.output / "resource_cap.json",
                    dict(
                        status="stopped_at_resource_cap",
                        cpu_seconds=time.process_time() - self.started_cpu,
                        peak_rss_bytes=self.peak_rss,
                        partial_results_retained=True,
                    ),
                )
                os._exit(3)

    def start(self):
        if version("qiskit-terra") != "0.46.3":
            raise ValueError("protocol requires Qiskit Terra 0.46.3")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        names = subprocess.check_output(
            ["git", "ls-files", "--", *SOURCES], cwd=ROOT, text=True
        ).splitlines()
        names = [name for name in names if name.endswith(".py")] + [PROTOCOL]
        if "research/common_compilation_20260922/run.py" not in names:
            raise ValueError("commit producer and protocol before acquisition")
        for name in names:
            blob = subprocess.check_output(["git", "show", head + ":" + name], cwd=ROOT)
            current = (ROOT / name).read_bytes()
            if blob.replace(b"\r\n", b"\n") != current.replace(b"\r\n", b"\n"):
                raise ValueError("source differs from frozen commit: " + name)
            self.sources[name] = digest(ROOT / name)
        self.output.mkdir(parents=True, exist_ok=False)
        write(
            self.output / "planned.json",
            dict(
                source_commit=head,
                source_sha256=self.sources,
                started_utc=datetime.now(timezone.utc).isoformat(),
                python=platform.python_version(),
                dependencies={n: version(n) for n in ("qiskit-terra", "numpy", "scipy", "psutil")},
                menu=[
                    case + "_" + route
                    for case in ("D1", "D2")
                    for route in ("reflection", "raw_parent", "residual")
                ],
                cpu_limit_seconds=7200,
                memory_limit_bytes=16 * 1024**3,
                policy="U/CX opt0 blocks, fixed 5U/2CX controlled-U, no local cancellation",
                depth_kind="serial_schedule_upper_bound_not_dependency_depth",
                clifford_t_available=False,
                hardware_admitted=False,
                confirmation_admitted=False,
            ),
        )
        threading.Thread(target=self.guard, daemon=True).start()


def bridge(budget, errors):
    size = budget["schedule"]["M"]
    if size not in errors:
        errors[size] = max(
            Fraction(label_amplitude(y, size)["conversion_error_upper"]) for y in range(size)
        )
    scale = (
        Fraction(budget["sensitivity_upper"])
        if "sensitivity_upper" in budget
        else 2 * Fraction(budget["beta"])
    )
    extra = scale * errors[size]
    _, upper = pi_bounds()
    margin = (
        1
        - Fraction(budget["deterministic_upper"])
        - extra
        - scale * (upper / size + upper * upper / (size * size))
    )
    if margin < 0:
        raise ArithmeticError("label bridge makes the fixed schedule infeasible")
    return dict(
        label_error_upper_rational=str(errors[size]),
        extra_price_bound_rational=str(extra),
        remaining_price_margin_rational=str(margin),
        original_schedule_feasible=True,
    )


def finish_row(acquisition, case, route, a, width, budget, parts, old, errors):
    begin = time.process_time()
    zero = compile_block(controlled_zero(width))
    schedule = budget["schedule"]
    schedules = {
        name: ae_profile(a, zero, schedule["M"], schedule["repetitions"], cancelled)
        for name, cancelled in (("controlled", False), ("control_cancelled", True))
    }
    row = dict(
        case=case,
        route=route,
        a=a.record(),
        a_inverse=a.record(),
        controlled_a=controlled(a).record(),
        controlled_a_inverse=controlled(a).record(),
        controlled_zero=zero.record(),
        a_qubits=width,
        total_allocated_qubits=2 * width - 2 + schedule["phase_qubits"],
        schedule=schedule,
        budget=budget,
        label_bridge=bridge(budget, errors),
        components=parts,
        totals={name: value.record() for name, value in schedules.items()},
        historical_resources=old,
        reconciliation={
            "a_cx_change": a.cx - old["a_cx_projection"],
            "controlled_total_cx_change": schedules["controlled"].cx - old["total_cx_projection"],
            "cancelled_total_cx_change": schedules["control_cancelled"].cx
            - old["control_cancelled_total_cx_projection"],
        },
        depth_kind="serial_schedule_upper_bound_not_dependency_depth",
        zero_and_label_cpu_seconds=time.process_time() - begin,
    )
    write(acquisition.output / (case + "_" + route + ".json"), row)
    print(case, route, "A CX", a.cx, "total CX", schedules["control_cancelled"].cx, flush=True)
    return row


def reflection(acq, case, reference, marginal, errors):
    begin = time.process_time()
    contract = contract_of(case)
    model = setup(contract)
    plan = ReviewedReflectionSignal(
        model["means"], model["factor"], contract.strike, 10, 4, "reflection"
    )
    signal, certificate = signal_circuit(plan)
    signal_cost = compile_block(signal)
    degree = reference["degree"]
    approximation = acq.read(APPROX + "minimax_" + str(degree) + ".json")
    phases = approximation["synthesis"]["phases"]
    if len(phases) != degree + 1:
        raise ValueError("phase degree mismatch")
    zero = QuantumCircuit(plan.num_qubits)
    phase_on_word(zero, list(plan.good_qubits), 0)
    zero.global_phase = math.pi
    reflection_cost = controlled(compile_block(zero))
    projectors = [
        controlled(compile_block(projected_phase(plan.num_qubits, plan.good_qubits, float(phi))))
        for phi in phases
    ]
    a = (
        marginal.times(plan.d)
        + controlled(signal_cost).times(degree)
        + reflection_cost.times(degree)
        + sum(projectors, Profile())
        + Profile(2, 0)
    )
    parts = dict(
        loader=marginal.record(),
        loader_copies=plan.d,
        signal=signal_cost.record(),
        controlled_signal=controlled(signal_cost).record(),
        signal_copies=degree,
        controlled_walk_reflection=reflection_cost.record(),
        controlled_projectors=[p.record() for p in projectors],
        readout_h=2,
        signal_certificate=certificate,
        plan=plan.metadata(),
        build_compile_cpu_seconds=time.process_time() - begin,
    )
    return finish_row(
        acq,
        case["id"],
        "reflection",
        a,
        plan.num_qubits + 1,
        reference["budget"],
        parts,
        reference["resources"],
        errors,
    )


def run(output):
    acq = Acquisition(output)
    acq.start()
    try:
        summary = acq.read(PRIMARY + "results.json")
        loading, loader_error = loader(10)
        marginal = compile_block(loading)
        write(
            acq.output / "loader.json",
            dict(
                profile=marginal.record(),
                error_upper=str(loader_error.hi),
                global_phase=float(loading.global_phase),
            ),
        )
        rows, errors, offset_work = [], {}, {}
        for case in CASES[:2]:
            primary = acq.read(PRIMARY + case["id"] + "_28.json")
            residual = acq.read(RESIDUAL + case["id"] + "_00.json")
            if make_plan(case, primary["spec"]) != primary["plan"]:
                raise ArithmeticError("model/environment drift from archived parent plan")
            ref = next(s for s in summary["summary"] if s["case"] == case["id"])
            rows.append(reflection(acq, case, ref["reflection_reference"], marginal, errors))
            begin = time.process_time()
            rebuilt = components(primary["plan"], reuse=True, reduced=True)
            if rebuilt != primary["components"]["reused"]:
                raise ArithmeticError("re-emitted primary component differs from archive")
            count = arithmetic_profile(rebuilt["total"])
            selector = primary["plan"]["selector_bits"]
            # Preserve the original one-U phase allowance as an explicit identity U.
            a = (
                count
                + marginal.times(len(primary["plan"]["affine_rows"]))
                + Profile(selector + 1, 0)
            )
            old = next(
                r["resources"]
                for r in summary["rows"]
                if r["case"] == case["id"]
                and r["spec"] == primary["spec"]
                and r["layout"] == "reused"
            )
            rows.append(
                finish_row(
                    acq,
                    case["id"],
                    "raw_parent",
                    a,
                    rebuilt["qubits"],
                    primary["budget"],
                    dict(
                        arithmetic=count.record(),
                        emitted=rebuilt["total"],
                        loader=marginal.record(),
                        loader_copies=len(primary["plan"]["affine_rows"]),
                        selector_h=selector,
                        explicit_identity_u=1,
                        reemission_cpu_seconds=time.process_time() - begin,
                    ),
                    old,
                    errors,
                )
            )
            begin = time.process_time()
            rebuilt_residual = residual_components(
                primary["plan"],
                residual["certificate"],
                {**rebuilt, "parent_plan": primary["plan"]},
            )
            if rebuilt_residual != residual["components"]:
                raise ArithmeticError("re-emitted residual differs from archive")
            count = arithmetic_profile(rebuilt_residual["total"])
            selector = residual["certificate"]["selector_bits"]
            a = (
                count
                + marginal.times(len(primary["plan"]["affine_rows"]))
                + Profile(selector + 1, 0)
            )
            rows.append(
                finish_row(
                    acq,
                    case["id"],
                    "residual",
                    a,
                    rebuilt_residual["qubits"],
                    residual["budget"],
                    dict(
                        arithmetic=count.record(),
                        emitted=rebuilt_residual["total"],
                        loader=marginal.record(),
                        loader_copies=len(primary["plan"]["affine_rows"]),
                        selector_h=selector,
                        explicit_identity_u=1,
                        reemission_cpu_seconds=time.process_time() - begin,
                    ),
                    residual["resources"],
                    errors,
                )
            )
            offset_work[case["id"]] = acq.read(RESIDUAL + case["id"] + "_offset.json")["work"]
        comparisons = []
        for case in ("D1", "D2"):
            chosen = {r["route"]: r for r in rows if r["case"] == case}
            comparisons.append(
                dict(
                    case=case,
                    ledgers={
                        ledger: dict(
                            winner=min(chosen, key=lambda k: chosen[k]["totals"][ledger]["cx"]),
                            reflection_over_residual=str(
                                Fraction(
                                    chosen["reflection"]["totals"][ledger]["cx"],
                                    chosen["residual"]["totals"][ledger]["cx"],
                                )
                            ),
                        )
                        for ledger in ("controlled", "control_cancelled")
                    },
                )
            )
        write(
            acq.output / "results.json",
            dict(
                rows=rows,
                comparisons=comparisons,
                physical_execution_error=None,
                quantum_advantage=False,
                confirmation_admitted=False,
                depth_comparison="serial upper bounds; no dependency-depth ordering asserted",
                clifford_t="unavailable: no certified common rotation synthesis allocation",
                classical_work=dict(
                    offset_inherited_operations=offset_work,
                    offset_scope="historical certified offline operation counts; not re-timed",
                    phase_preprocessing="archived degree64/128 phase synthesis reused; offline "
                    "synthesis cost excluded from gates, no new synthesis or amortization claim",
                    compiler_scope="CPU/wall/RSS measure this acquisition, not pricing runtime",
                ),
            ),
        )
        for name, value in acq.sources.items():
            if digest(ROOT / name) != value:
                raise ValueError("source changed during acquisition: " + name)
        for name, value in acq.inputs.items():
            if digest(ROOT / name) != value:
                raise ValueError("input changed during acquisition: " + name)
        write(
            acq.output / "complete.json",
            dict(
                status="complete",
                input_sha256=acq.inputs,
                cpu_seconds=time.process_time() - acq.started_cpu,
                wall_seconds=time.perf_counter() - acq.started_wall,
                peak_rss_bytes=acq.peak_rss,
                sha256={p.name: digest(p) for p in sorted(acq.output.glob("*.json"))},
            ),
        )
    except Exception as error:
        write(
            acq.output / "failed.json",
            dict(
                error=repr(error),
                inputs=acq.inputs,
                cpu_seconds=time.process_time() - acq.started_cpu,
            ),
        )
        raise
    finally:
        acq.stop.set()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
