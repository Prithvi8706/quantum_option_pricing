"""Week-12 synthetic development acquisition, complete accounting and strict replay."""

import argparse
from dataclasses import asdict
import json
import math
import os
from pathlib import Path
import shutil
import time

import numpy as np
from scipy.stats import t

from .allocation_rule import allocate, preselect
from .encoding_decision import Encoding
from .intervals import clopper_pearson
from .run_encoding_decision import SOURCE, load_profiles, verify_inventory
from .run_w11_baselines import append_event, inventory_environment
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .unequal_allocation import ARMS, PILOT, choose_batch, terminal_decision
from .w12_recovery import reconcile
from research.paper_a.benchmark import C6, by_id
from research.paper_a.references import black_scholes_call


SCENARIOS = {"design_match": (0.02, 0.07), "swapped": (0.07, 0.02)}
NAMESPACES = {
    "pilot": "w12_asymmetric_pilot_v2",
    "primary": "w12_asymmetric_primary_v1",
    "secondary": "w12_asymmetric_secondary_v1",
}
PROTOCOLS = (
    "WEEK_12_DESIGN_MANIFEST.md",
    "PROTOCOL_W12_POLICY_V1.md",
    "PROTOCOL_W12_ACQUISITION_V1.md",
)


def schedule(stage):
    if stage not in ("pilot", "main"):
        raise ValueError("unknown stage")
    rows = []
    groups = (
        [("pilot", C6, ("design_match",), (0.0,), 3)]
        if stage == "pilot"
        else [
            ("primary", ("E001",), ("design_match",), (0.0,), 400),
            ("secondary", C6, tuple(SCENARIOS), (0.0, 0.003, 0.03), 30),
        ]
    )
    for phase, names, scenarios, guards, repeats in groups:
        for name in names:
            for scenario in scenarios:
                for guard in guards:
                    for rep in range(repeats):
                        order = rng_for(
                            "w12_order_v1", phase, name, scenario, guard, rep
                        ).permutation(5)
                        for i in order:
                            rows.append(
                                dict(
                                    phase=phase,
                                    contract=name,
                                    scenario=scenario,
                                    guard=guard,
                                    rep=rep,
                                    arm=ARMS[int(i)],
                                )
                            )
    return [dict(spec, attempt=i) for i, spec in enumerate(rows)]


def trial(spec, profiles, emit=lambda event: None):
    """Evaluator owns truths. emit durably records each synthetic draw boundary."""
    if (
        spec["arm"] not in ARMS
        or spec["scenario"] not in SCENARIOS
        or spec["phase"] not in ("pilot", "primary", "secondary")
    ):
        raise ValueError("unknown trial identity")
    encodings, excluded = [], {}
    for label in ("linearized", "exact_table"):
        b = profiles[label]["bounds"]
        if any(b.get(k) is None for k in ("sensitivity", "offset", "support", "grid", "encoding")):
            excluded[label] = "unknown_bias_or_mapping"
            continue
        encodings.append(
            Encoding(
                label, b["sensitivity"], b["offset"], b["support"] + b["grid"] + b["encoding"], 1.0
            )
        )
    choice = preselect(encodings) if encodings else dict(selected=None, scores=[])
    choice["excluded"] = excluded
    result = dict(
        spec=spec,
        choice=choice,
        plan=None,
        status="not_certified",
        interval=None,
        radius=None,
        pilot_successes=None,
        calibration_errors=None,
        successes=None,
        contains=None,
        erroneous=False,
        midpoint_error=None,
        pilot_shots=0,
        m0=0,
        m1=0,
        n=0,
        total_shots=0,
        total_cx=0,
        calibration_cx=0,
        penalized_cost=65536,
        selection_forecast_radius=None,
        diagnostic_forecast_kind="common_delta_proxy_not_historical_cp_selection",
    )
    if choice["selected"] is None:
        return result
    label = choice["selected"]
    encoding = next(e for e in encodings if e.name == label)
    profile = profiles[label]
    f, g = SCENARIOS[spec["scenario"]]
    amplitude = profile["amplitude"]  # evaluator-only, never passed to policy
    q = f + (1 - f - g) * amplitude
    cx = profile["profiles"]["0"]["gates"]["cx"]
    if not 0 <= q <= 1 or isinstance(cx, bool) or not isinstance(cx, int) or cx < 0:
        raise ValueError("invalid evaluator input")
    key = (
        NAMESPACES[spec["phase"]],
        spec["contract"],
        spec["scenario"],
        spec["guard"],
        spec["arm"],
        spec["rep"],
        label,
    )

    def draw(purpose, shots, probability, gates):
        emit(dict(event="draw_started", purpose=purpose, shots=shots, logical_cx=shots * gates))
        count = int(rng_for(*key, purpose).binomial(shots, probability))
        emit(
            dict(
                event="draw_completed",
                purpose=purpose,
                shots=shots,
                logical_cx=shots * gates,
                successes=count,
            )
        )
        return count

    paid = spec["arm"] in ("pilot_cp", "unequal_full", "unequal_target")
    pilot = draw("pilot", PILOT, q, cx) if paid else None
    plan = choose_batch(encoding, spec["arm"], pilot, guard=spec["guard"])
    selection_forecast = plan.forecast_radius
    if spec["arm"] == "pilot_cp":
        old = allocate(encoding, pilot, guard=spec["guard"])
        selection_forecast = next(
            f["projected_radius"] for f in old["forecasts"] if f["calibration_per_state"] == plan.m0
        )
    emit(dict(event="plan_frozen", plan=asdict(plan)))
    cal = [draw("calibration_0", plan.m0, f, 0), draw("calibration_1", plan.m1, g, 0)]
    count = draw("pricing", plan.n, q, cx)
    decision = terminal_decision(encoding, count, plan.n, cal, plan.m0, plan.m1, spec["guard"])
    c = by_id(spec["contract"])
    truth = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    interval = decision["interval"]
    error = None if interval is None else abs(sum(interval) / 2 - truth)
    delivered = decision["status"] == "precision_met"
    result.update(
        **decision,
        plan=asdict(plan),
        pilot_successes=pilot,
        calibration_errors=cal,
        successes=count,
        pilot_shots=plan.pilot_shots,
        m0=plan.m0,
        m1=plan.m1,
        n=plan.n,
        total_shots=plan.total_shots,
        total_cx=(plan.pilot_shots + plan.n) * cx,
        contains=None if interval is None else bool(interval[0] <= truth <= interval[1]),
        erroneous=bool(delivered and error > 1),
        midpoint_error=error,
        penalized_cost=plan.total_shots if delivered else 65536,
        selection_forecast_radius=selection_forecast,
    )
    return result


def proportion(k, n):
    if n == 0:
        return dict(count=k, denominator=n, fraction=None, cp95=None)
    lo, hi = clopper_pearson([k], [n], 0.05)
    return dict(count=k, denominator=n, fraction=k / n, cp95=[float(lo[0]), float(hi[0])])


def mean_interval(values):
    a = np.asarray(values, dtype=float)
    half = float(t.ppf(0.975, len(a) - 1) * a.std(ddof=1) / len(a) ** 0.5) if len(a) > 1 else None
    return dict(
        mean=float(a.mean()),
        approximate_t95=None if half is None else [float(a.mean() - half), float(a.mean() + half)],
    )


def analyze(rows):
    groups = {}
    for row in rows:
        s = row["spec"]
        key = (s["phase"], s["contract"], s["scenario"], s["guard"], s["arm"])
        groups.setdefault(key, []).append(row)
    cells = []
    for key, group in sorted(groups.items()):
        n = len(group)
        delivered = [r for r in group if r["status"] == "precision_met"]
        intervals = [r for r in group if r["interval"] is not None]
        forecasts = [r for r in group if r["plan"] and r["radius"] is not None]
        cells.append(
            dict(
                phase=key[0],
                contract=key[1],
                scenario=key[2],
                guard=key[3],
                arm=key[4],
                observations=n,
                delivery=proportion(len(delivered), n),
                misses=proportion(sum(r["contains"] is False for r in group), n),
                erroneous=proportion(sum(r["erroneous"] for r in group), n),
                erroneous_among_declarations=proportion(
                    sum(r["erroneous"] for r in delivered), len(delivered)
                ),
                misses_among_intervals=proportion(
                    sum(r["contains"] is False for r in intervals), len(intervals)
                ),
                actual_cost_among_deliveries=None
                if not delivered
                else mean_interval([r["total_shots"] for r in delivered]),
                actual_cost=mean_interval([r["total_shots"] for r in group]),
                penalized_cost=mean_interval([r["penalized_cost"] for r in group]),
                mean_logical_cx=sum(r["total_cx"] for r in group) / n,
                no_interval=sum(r["interval"] is None for r in group),
                forecast_comparable_rows=len(forecasts),
                mean_delta_forecast_radius=None
                if not forecasts
                else sum(r["plan"]["forecast_radius"] for r in forecasts) / len(forecasts),
                mean_observed_radius=None
                if not forecasts
                else sum(r["radius"] for r in forecasts) / len(forecasts),
                delta_forecast_optimistic=sum(
                    r["plan"]["forecast_radius"] < r["radius"] for r in forecasts
                ),
                forecast_margin_met=sum(
                    bool(r["plan"] and r["plan"]["forecast_target_met"]) for r in group
                ),
            )
        )
    primary = {c["arm"]: c for c in cells if c["phase"] == "primary"}
    gate = None
    if len(primary) == 5 and all(c["observations"] == 400 for c in primary.values()):
        target = primary["unequal_target"]
        comparisons = {}
        for arm in ("fixed_cp", "fixed_target"):
            base = primary[arm]
            reduction = 1 - target["penalized_cost"]["mean"] / base["penalized_cost"]["mean"]
            delta = target["delivery"]["fraction"] - base["delivery"]["fraction"]
            target_costs = [
                r["penalized_cost"]
                for r in rows
                if r["spec"]["phase"] == "primary" and r["spec"]["arm"] == "unequal_target"
            ]
            base_costs = [
                r["penalized_cost"]
                for r in rows
                if r["spec"]["phase"] == "primary" and r["spec"]["arm"] == arm
            ]
            mt, mb = float(np.mean(target_costs)), float(np.mean(base_costs))
            se_ratio = math.sqrt(
                float(np.var(target_costs, ddof=1)) / 400 / mb**2
                + mt**2 * float(np.var(base_costs, ddof=1)) / 400 / mb**4
            )
            lowers, uppers = clopper_pearson(
                [target["delivery"]["count"], base["delivery"]["count"]], [400, 400], 0.025
            )
            comparisons[arm] = dict(
                penalized_cost_reduction=reduction,
                delivery_difference=delta,
                delivery_difference_conservative95=[
                    float(lowers[0] - uppers[1]),
                    float(uppers[0] - lowers[1]),
                ],
                passed=(
                    20 * sum(target_costs) <= 17 * sum(base_costs)
                    and target["delivery"]["count"] - base["delivery"]["count"] >= -8
                ),
            )
            comparisons[arm]["cost_reduction_approximate_delta95"] = [
                reduction - 1.96 * se_ratio,
                reduction + 1.96 * se_ratio,
            ]
        gate = dict(
            comparisons=comparisons,
            passed=target["delivery"]["count"] >= 380
            and all(c["passed"] for c in comparisons.values()),
            scope="descriptive development threshold, not superiority/noninferiority proof",
        )
    return dict(rows=len(rows), cells=cells, primary_interest=gate)


def producing_sources():
    sources = sorted((ROOT / "research/journal_sprint").glob("*.py"))
    sources += sorted((ROOT / "research/paper_a").rglob("*.py"))
    return sources + [ROOT / "docs/journal_sprint" / name for name in PROTOCOLS]


def checked_time(value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError("invalid timing")
    return value


def check_deadline(deadline):
    if deadline is not None and time.perf_counter() >= deadline:
        raise TimeoutError("workflow verification deadline exceeded")


def same_inputs(left, right):
    for name in ["complete.json"] + [f"profile_{c}.json" for c in C6]:
        if sha256(Path(left) / name) != sha256(Path(right) / name):
            raise ValueError("pilot/main input identity mismatch")


def verify(output, deadline=None):
    output = Path(output)
    check_deadline(deadline)
    files = verify_inventory(output)
    planned = json.loads((output / "planned.json").read_text())
    config = planned["config"]
    if (
        set(config["replay_sources"]) != {str(p.relative_to(ROOT)) for p in producing_sources()}
        or config.get("synthetic") is not True
        or config.get("quantum_advantage") is not False
        or config["stage"] not in ("pilot", "main")
        or not 0
        < checked_time(config["cap_seconds"])
        <= (900 if config["stage"] == "pilot" else 3600)
        or any(
            planned["threads"].get(k) != "1"
            for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
        )
    ):
        raise ValueError("configuration/source inventory mismatch")
    for name, digest in config["replay_sources"].items():
        if sha256(ROOT / name) != digest or sha256(output / "source_snapshot" / name) != digest:
            raise ValueError("frozen source drift")
    specs = schedule(config["stage"])
    if specs != json.loads((output / "schedule.json").read_text()):
        raise ValueError("schedule mismatch")
    rows = [json.loads(p.read_text()) for p in sorted(output.glob("row_*.json"))]
    summary = json.loads((output / "summary.json").read_text())
    if (
        summary["status"] != "complete"
        or len(rows) != len(specs)
        or summary["completed"] != len(rows)
        or summary["planned"] != len(specs)
    ):
        raise ValueError("incomplete acquisition")
    if summary["stage"] != config["stage"]:
        raise ValueError("summary stage mismatch")
    elapsed = checked_time(summary["acquisition_seconds"])
    durations = [checked_time(r["elapsed_seconds"]) for r in rows]
    if elapsed + 1e-9 < sum(durations):
        raise ValueError("acquisition time inconsistent with row times")
    if config["stage"] == "pilot":
        projection = 4 * 7400 * max(max(durations), elapsed / len(rows))
        if config["gate"] is not None or checked_time(summary["projection_seconds"]) != projection:
            raise ValueError("projection mismatch")
    else:
        pilot_path = output / "pilot_evidence"
        same_inputs(output / "input", pilot_path / "input")
        verify(pilot_path, deadline)
        ps = json.loads((pilot_path / "summary.json").read_text())
        expected_gate = dict(
            pilot_manifest_sha256=sha256(pilot_path / "complete.json"),
            projection_seconds=ps["projection_seconds"],
        )
        if (
            ps["stage"] != "pilot"
            or ps["projection_seconds"] > 7200
            or config["gate"] != expected_gate
            or summary["projection_seconds"] is not None
        ):
            raise ValueError("main runtime gate mismatch")
    recovery = reconcile(output)
    if recovery["completed"] != len(specs) or recovery["truncated_event_tail"]:
        raise ValueError("unreconciled attempts")
    if recovery != json.loads((output / "recovery.json").read_text()):
        raise ValueError("recovery report mismatch")
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    event_groups = {}
    for e in events:
        event_groups.setdefault(e["attempt"], []).append(
            {k: v for k, v in e.items() if k != "attempt"}
        )
    if set(event_groups) != set(range(len(specs))):
        raise ValueError("extra/missing attempt events")
    profiles = load_profiles(output / "input")
    for spec, saved in zip(specs, rows):
        check_deadline(deadline)
        if saved["result"]["spec"] != spec:
            raise ValueError("row identity mismatch")
        expected_events = [dict(event="started")]
        expected = trial(spec, profiles[spec["contract"]], expected_events.append)
        expected_events.append(dict(event="completed"))
        if expected != saved["result"] or expected_events != event_groups[spec["attempt"]]:
            raise ValueError("result/event replay mismatch")
    if analyze([r["result"] for r in rows]) != json.loads((output / "analysis.json").read_text()):
        raise ValueError("analysis mismatch")
    check_deadline(deadline)
    return dict(
        verified=True, rows=len(rows), files=files, numerical_replay=True, timings_reproduced=False
    )


def run(output, stage, pilot=None, cap_seconds=None, acquire=trial):
    workflow_start = time.perf_counter()
    deadline = workflow_start + 7200 if stage == "main" else None
    if stage not in ("pilot", "main"):
        raise ValueError("unknown stage")
    limit = 900 if stage == "pilot" else 3600
    cap = limit if cap_seconds is None else cap_seconds
    if not 0 < checked_time(cap) <= limit:
        raise ValueError("invalid wall cap")
    if any(
        os.environ.get(k) != "1"
        for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
    ):
        raise ValueError("single thread environment required")
    gate = None
    if stage == "main":
        if pilot is None:
            raise ValueError("verified runtime pilot required")
        verify(pilot, deadline)
        pilot_summary = json.loads((Path(pilot) / "summary.json").read_text())
        if pilot_summary["stage"] != "pilot" or pilot_summary["projection_seconds"] > 7200:
            raise ValueError("runtime gate failed")
        gate = dict(
            pilot_manifest_sha256=sha256(Path(pilot) / "complete.json"),
            projection_seconds=pilot_summary["projection_seconds"],
        )
    profiles = load_profiles(SOURCE)
    if stage == "main":
        same_inputs(SOURCE, Path(pilot) / "input")
    sources = producing_sources()
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    output = start_run(
        output,
        dict(
            stage=stage,
            cap_seconds=cap,
            replay_sources=hashes,
            gate=gate,
            synthetic=True,
            quantum_advantage=False,
        ),
    )
    attempt = None
    try:
        if stage == "main":
            shutil.copytree(pilot, output / "pilot_evidence")
        for p in sources:
            dest = output / "source_snapshot" / p.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            if sha256(dest) != hashes[str(p.relative_to(ROOT))]:
                raise ValueError("source changed during snapshot")
        (output / "input").mkdir()
        for p in [SOURCE / "complete.json"] + [SOURCE / f"profile_{name}.json" for name in C6]:
            shutil.copy2(p, output / "input" / p.name)
        if load_profiles(output / "input") != profiles:
            raise ValueError("input drift")
        write_json(output / "environment.json", inventory_environment())
        specs = schedule(stage)
        write_json(output / "schedule.json", specs)
        with (output / "events.jsonl").open("x", encoding="utf-8"):
            pass
        rows, durations = [], []
        before = time.perf_counter()
        for spec in specs:
            check_deadline(deadline)
            if time.perf_counter() - before >= cap:
                break
            attempt = spec["attempt"]

            def emit(e):
                append_event(output, dict(e, attempt=attempt))

            start = time.perf_counter()
            emit(dict(event="started"))
            row = acquire(spec, profiles[spec["contract"]], emit)
            elapsed = time.perf_counter() - start
            write_json(
                output / f"row_{attempt:05d}.json", dict(result=row, elapsed_seconds=elapsed)
            )
            emit(dict(event="completed"))
            rows.append(row)
            durations.append(elapsed)
            attempt = None
            if len(rows) % 100 == 0:
                print(f"{stage}: {len(rows)}/{len(specs)}", flush=True)
        elapsed = time.perf_counter() - before
        summary = dict(
            stage=stage,
            completed=len(rows),
            planned=len(specs),
            status="complete" if len(rows) == len(specs) else "time_cap_partial",
            acquisition_seconds=elapsed,
            projection_seconds=None,
        )
        if stage == "pilot" and rows:
            summary["projection_seconds"] = 4 * 7400 * max(max(durations), elapsed / len(rows))
        write_json(output / "recovery.json", reconcile(output))
        write_json(output / "analysis.json", analyze(rows))
        write_json(output / "summary.json", summary)
        finish_run(output)
        if stage == "main" and summary["status"] == "complete":
            # Receipt is returned outside the immutable acquisition archive.
            checked = verify(output, deadline)
            check_deadline(deadline)
            return dict(
                summary, verification=checked, workflow_seconds=time.perf_counter() - workflow_start
            )
        return summary
    except BaseException as error:
        if (output / "complete.json").exists():
            raise  # Sealed acquisition remains immutable even if replay times out.
        # A failed append may have left a torn tail. Never append to it again.
        # Diagnostics are independent best-effort writes; retain original exception.
        try:
            write_json(output / "failure.json", dict(attempt=attempt, error=str(error)))
        except Exception:
            pass
        try:
            if (output / "schedule.json").exists() and not (output / "recovery.json").exists():
                write_json(output / "recovery.json", reconcile(output))
        except Exception as recovery_error:
            try:
                write_json(output / "recovery_error.json", dict(error=str(recovery_error)))
            except Exception:
                pass
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", choices=("pilot", "main"))
    parser.add_argument("--pilot", type=Path)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = verify(args.output) if args.verify else run(args.output, args.stage, args.pilot)
    if args.report:
        write_json(args.report, result)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
