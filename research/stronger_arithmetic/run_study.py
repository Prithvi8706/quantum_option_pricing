"""Exclusive bounded arithmetic acquisition with frozen sources and all menu rows."""

import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from importlib.metadata import version
from itertools import product
from pathlib import Path
import platform
import subprocess

import numpy as np

from research.journal_sprint.asian_basket import setup
from research.journal_sprint.asian_encoding import grid
from research.journal_sprint.claim_assessment import projected_cost
from research.journal_sprint.decimal_enclosure import Interval
from research.journal_sprint.fixed_exp_budget import evaluate_integer
from research.journal_sprint.run_matched_arithmetic import arithmetic_budget, plan_for
from research.journal_sprint.run_minimal_pivot_week1 import cost
from research.journal_sprint.run_minimal_pivot_week2 import CASES, contract_of
from research.journal_sprint.storage import ROOT, finish_run, sha256, write_json
from research.journal_sprint.week2_pipeline import controlled_zero, loader

from .budget import evaluate_reduced_integer, reduced_plan

PROTOCOL = "docs/release/STRONGER_ARITHMETIC_PROTOCOL_20260921.md"
REFERENCE = "results/journal_sprint/matched_arithmetic_v1"
CONFIG = {
    "cases": ["D1", "D2"],
    "fraction_bits": [20, 24],
    "widths": [40, 48],
    "degrees": [8, 12, 16],
    "reductions": [1, 2, 3],
    "q": 10,
    "cutoff": 4,
    "tolerance": "1",
    "confidence": "0.95",
    "repetitions": 17,
    "call_cap": 10_000_000,
    "conversion_gate_cap": 8_000_000,
    "conversion_wire_cap": 4096,
    "component_gate_cap": 100_000_000,
    "candidate_status": "standby",
    "confirmation": False,
}


def read(path):
    from research.release_checks.json_io import read as strict_read

    return strict_read(path)


def menu():
    return [
        dict(fraction_bits=f, width=w, degree=d, reductions=s)
        for f, w, d, s in product(
            CONFIG["fraction_bits"], CONFIG["widths"], CONFIG["degrees"], CONFIG["reductions"]
        )
    ]


def source_manifest():
    names = subprocess.check_output(
        [
            "git",
            "ls-files",
            "research/journal_sprint",
            "research/stronger_arithmetic",
            "research/release_checks",
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    names = [n for n in names if n.endswith(".py")] + [PROTOCOL]
    if "research/stronger_arithmetic/run_study.py" not in names:
        raise ValueError("study sources must be tracked before acquisition")
    tracked = set(names)
    for directory in ("research/journal_sprint", "research/release_checks"):
        unexpected = {
            p.relative_to(ROOT).as_posix() for p in (ROOT / directory).rglob("*.py")
        } - tracked
        if unexpected:
            raise ValueError("untracked executable dependencies: " + ", ".join(sorted(unexpected)))
    return {n: sha256(ROOT / n) for n in sorted(names)}


def reference_manifest():
    complete = read(ROOT / REFERENCE / "complete.json")
    expected = set(complete["sha256"]) | {"complete.json"}
    actual = {p.name for p in (ROOT / REFERENCE).iterdir() if p.is_file()}
    if actual != expected:
        raise ValueError("reference archive inventory differs")
    result = {}
    for name in sorted(expected):
        if Path(name).name != name:
            raise ValueError("reference path must be a basename")
        relative = REFERENCE + "/" + name
        digest = sha256(ROOT / relative)
        if name != "complete.json" and digest != complete["sha256"][name]:
            raise ValueError("reference artifact hash mismatch")
        result[relative] = digest
    return result


def make_plan(case, spec, q=10):
    contract = contract_of(case)
    model = setup(contract)
    if spec is None:
        return plan_for(contract, model, q)
    return reduced_plan(
        model["means"],
        model["factor"],
        normal_bits=q,
        cutoff=4,
        spot=100,
        strike=int(contract.strike),
        discount=(-Interval(str(contract.rate)) * Interval(str(contract.maturity))).exp(),
        **spec,
    )


def finite_diagnostics(case, spec):
    records = []
    for q in (1, 2):
        finite = grid(contract_of(case), q, 4)
        plan = make_plan(case, spec, q)
        if not plan["overflow_safe"]:
            records.append({"q": q, "status": "overflow_certificate_failed"})
            continue
        scale = 1 << plan["fraction_bits"]
        errors = []
        coefficients = plan["exp_budget"]["coefficients"]
        discount = np.exp(-contract_of(case).rate * contract_of(case).maturity)
        truth = discount * np.maximum(
            np.exp(finite["model"]["means"] + finite["normals"] @ finite["model"]["factor"].T).mean(
                axis=1
            )
            - contract_of(case).strike,
            0,
        )
        for packed in range(len(truth)):
            logs = [
                a + sum(((packed >> i) & 1) * c for i, c in enumerate(cs))
                for a, cs in plan["affine_rows"]
            ]
            if spec is None:
                prices = [evaluate_integer(x, coefficients, plan["fraction_bits"]) for x in logs]
            else:
                prices = [
                    evaluate_reduced_integer(
                        x, coefficients, plan["fraction_bits"], spec["reductions"], 100
                    )
                    for x in logs
                ]
            payoff = max(sum(prices) - plan["strike_sum"], 0)
            if payoff >= 1 << plan["selector_bits"]:
                raise ArithmeticError("finite diagnostic selector truncation")
            actual = discount * payoff / scale / len(prices)
            errors.append(abs(actual - truth[packed]))
        observed = float(max(errors))
        if observed > float(plan["arithmetic_price_error_upper"]) + 1e-10:
            raise ArithmeticError("finite diagnostic exceeds arithmetic certificate")
        records.append(
            dict(
                q=q,
                inputs=len(truth),
                max_pointwise_error=observed,
                arithmetic_bound=plan["arithmetic_price_error_upper"],
                scope="binary64 finite-grid diagnostic, not confirmation",
            )
        )
    return records


@lru_cache(maxsize=256)
def zero_cost(qubits):
    return cost(controlled_zero(qubits))["cx"]


def resources(native, qubits, ae):
    cx, u = native["cx"], native["u"]
    result = dict(
        a_cx_projection=cx,
        a_u_projection=u,
        controlled_a_cx_projection=6 * cx + 2 * u,
        zero_reflection_cx_projection=zero_cost(qubits),
        a_qubits=qubits,
        total_qubits=None,
        total_cx_projection=None,
        control_cancelled_total_cx_projection=None,
        physical_execution_error=None,
    )
    if ae["status"] == "ideal_plan":
        result["total_qubits"] = 2 * qubits - 2 + ae["phase_qubits"]
        result["total_cx_projection"] = projected_cost(result, ae["M"], ae["repetitions"])
        result["control_cancelled_total_cx_projection"] = projected_cost(
            {**result, "controlled_a_cx_projection": cx}, ae["M"], ae["repetitions"]
        )
    return result


def summarize(rows, references):
    summaries = []
    for case in CONFIG["cases"]:
        eligible = [r for r in rows if r["case"] == case and r["status"] == "ideal_plan"]
        candidates = [r for r in eligible if r["arm"] == "range_reduced"]
        best = (
            min(candidates, key=lambda r: r["resources"]["control_cancelled_total_cx_projection"])
            if candidates
            else None
        )
        reflection = min(
            [
                r
                for r in references[case]["alternatives"]
                if r["mode"] == "reflection"
                and r["resources"]["control_cancelled_total_cx_projection"] is not None
            ],
            key=lambda r: r["resources"]["control_cancelled_total_cx_projection"],
        )
        base = next(r for r in references[case]["alternatives"] if r["mode"] == "ripple")
        summary = dict(
            case=case,
            feasible_rows=len(eligible),
            best_reduced=best,
            reflection_reference=reflection,
            original_arithmetic_reference=base,
            best_arithmetic=min(
                eligible, key=lambda r: r["resources"]["control_cancelled_total_cx_projection"]
            )
            if eligible
            else None,
        )
        if best:
            value = best["resources"]["control_cancelled_total_cx_projection"]
            reflection_value = reflection["resources"]["control_cancelled_total_cx_projection"]
            summary.update(
                original_over_reduced_rational=str(
                    Fraction(base["resources"]["control_cancelled_total_cx_projection"], value)
                ),
                reduced_over_reflection_rational=str(Fraction(value, reflection_value)),
                winner="arithmetic"
                if value < reflection_value
                else "tie"
                if value == reflection_value
                else "reflection",
            )
        summaries.append(summary)
    return summaries


def acquire_case(case, path, marginal_cost, marginal_error):
    from .components import ResourceLimitError, components

    rows, finite = [], []
    reference = read(ROOT / REFERENCE / ("case_" + case["id"] + ".json"))
    # Catch environment/model drift before comparing any new route with old evidence.
    import json

    if (
        json.dumps(make_plan(case, None), sort_keys=True)
        != json.dumps(reference["arithmetic_plan"], sort_keys=True)
        or case != reference["case"]
    ):
        raise ValueError("archived baseline/model drift: " + case["id"])
    for index, spec in enumerate([None] + menu()):
        label = case["id"] + "_" + str(index).zfill(2)
        print("acquire", label, spec, flush=True)
        plan = make_plan(case, spec)
        budget = arithmetic_budget(
            contract_of(case), setup(contract_of(case)), plan, Interval(marginal_error), "0"
        )
        arm = "workspace_only" if spec is None else "range_reduced"
        record = dict(case=case["id"], arm=arm, spec=spec, plan=plan, budget=budget)
        finite.append(dict(case=case["id"], spec=spec, diagnostics=finite_diagnostics(case, spec)))
        status = (
            budget["schedule"]["status"] if plan["overflow_safe"] else "overflow_certificate_failed"
        )
        component = None
        if status == "ideal_plan":
            try:
                component = components(plan, reduced=spec is not None)
            except ResourceLimitError as error:
                status = "resource_cap"
                record["reason"] = str(error)
        if component is not None:
            record["components"] = component
        for layout in ("retained", "reused"):
            row = dict(
                case=case["id"],
                arm=arm,
                spec=spec,
                layout=layout,
                status=status,
                budget=budget,
                resources=None,
            )
            if component is not None:
                detail = component[layout]
                native = {
                    k: detail["native"][k] + len(plan["affine_rows"]) * marginal_cost[k]
                    for k in ("cx", "u")
                }
                native["u"] += plan["selector_bits"] + 1
                row.update(
                    arithmetic_depth=detail["logical_depth"],
                    resources=resources(native, detail["qubits"], budget["schedule"]),
                )
            if "reason" in record:
                row["reason"] = record["reason"]
            rows.append(row)
        record["status"] = status
        write_json(path / (label + ".json"), record)
    return rows, finite


def run(path):

    path = Path(path)
    sources, inputs = source_manifest(), reference_manifest()
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True
    )
    if dirty.strip():
        raise ValueError("commit tracked changes before acquisition")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    for name in sources:
        committed = subprocess.check_output(["git", "show", head + ":" + name], cwd=ROOT)
        disk = (ROOT / name).read_bytes()
        # Older tracked dependencies may use checkout CRLF conversion. Bind their
        # text to Git and their exact execution bytes to the manifest separately.
        same = (
            committed == disk
            if name.startswith("research/stronger_arithmetic/") or name == PROTOCOL
            else committed.replace(b"\r\n", b"\n") == disk.replace(b"\r\n", b"\n")
        )
        if not same:
            raise ValueError("source bytes differ from committed tree: " + name)
    path.mkdir(parents=True, exist_ok=False)
    write_json(
        path / "planned.json",
        dict(
            started_utc=datetime.now(timezone.utc).isoformat(),
            config=CONFIG,
            source_sha256=sources,
            input_sha256=inputs,
            git_head=head,
            python=platform.python_version(),
            numpy=np.__version__,
            dependencies={name: version(name) for name in ("numpy", "scipy", "qiskit-terra")},
            tracked_tree_dirty=False,
        ),
    )
    try:
        marginal, marginal_error = loader(10)
        marginal_cost = cost(marginal)
        write_json(
            path / "loader.json", dict(resources=marginal_cost, error_upper=str(marginal_error.hi))
        )
        rows, finite = [], []
        references = {
            case: read(ROOT / REFERENCE / ("case_" + case + ".json")) for case in CONFIG["cases"]
        }
        # Case workers have independent, bounded caches and disjoint output files.
        # Collect in declared case order so completion timing cannot reorder rows.
        with ProcessPoolExecutor(max_workers=2) as pool:
            futures = [
                pool.submit(acquire_case, case, path, marginal_cost, str(marginal_error.hi))
                for case in CASES[:2]
            ]
            for future in futures:
                case_rows, case_finite = future.result()
                rows.extend(case_rows)
                finite.extend(case_finite)
        write_json(path / "finite.json", finite)
        result = dict(
            rows=rows,
            summary=summarize(rows, references),
            residual_arm={
                "status": "not_admitted",
                "reason": "signed residual certificate and emitted oracle required",
            },
            candidate_status="standby",
            quantum_over_classical_advantage=False,
            confirmation_admitted=False,
            production_choice=None,
        )
        write_json(path / "results.json", result)
        for name, digest in {**sources, **inputs}.items():
            if sha256(ROOT / name) != digest:
                raise ValueError("source/input changed during acquisition: " + name)
        finish_run(path)
    except BaseException as error:
        write_json(path / "failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
