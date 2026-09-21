"""Bounded signed residual acquisition from pinned arithmetic conversions."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from importlib.metadata import version
import math
from pathlib import Path
import platform
import subprocess

import numpy as np

from research.journal_sprint.asian_basket import setup
from research.journal_sprint.asian_encoding import grid
from research.journal_sprint.claim_assessment import schedule
from research.journal_sprint.decimal_enclosure import Interval
from research.journal_sprint.reviewed_reflection_signal import ReviewedReflectionSignal
from research.journal_sprint.run_minimal_pivot_week2 import CASES, contract_of
from research.journal_sprint.storage import ROOT, finish_run, sha256, write_json

from .budget import evaluate_reduced_integer
from .residual import (
    control_offset_certificate,
    evaluate_control_integer,
    menu,
    residual_plan,
)
from .run_study import REFERENCE, make_plan, read, resources
from .verify import archive, equal, provenance

PROTOCOL = "docs/release/SIGNED_RESIDUAL_PROTOCOL_20260921.md"
PRIMARY = "results/journal_sprint/stronger_arithmetic_v1"
LOW_MODEL = "results/journal_sprint/normalization_approximation_v1/model.json"
CONFIG = dict(
    cases=["D1", "D2"],
    specs=menu(),
    q=10,
    cutoff=4,
    tolerance="1",
    confidence="0.95",
    repetitions=17,
    call_cap=10_000_000,
    candidate_status="standby",
    confirmation=False,
)


def case_constants(case, low, q=10):
    contract = contract_of(case)
    model = setup(contract)
    signal = ReviewedReflectionSignal(
        model["means"], model["factor"], contract.strike, 10, 4, "reflection"
    )
    reference = read(ROOT / REFERENCE / ("case_" + case["id"] + ".json"))
    offsets = {
        r["budget"]["offset"] for r in reference["alternatives"] if r["mode"] == "reflection"
    }
    if len(offsets) != 1:
        raise ValueError("reflection offset is not constant across degree menu")
    chosen = offsets.pop()
    # q1/q2 diagnostics use their own certified finite-model expectation.
    if q != 10:
        from research.journal_sprint.control_offset_enclosure import (
            control_enclosure,
            moment_enclosure,
        )

        moments = moment_enclosure(model["means"], model["factor"], q, 4)
        interval = control_enclosure(
            moments["moments"],
            contract.strike,
            signal.B,
            math.exp(-contract.rate * contract.maturity),
            low,
        )["value"]
        chosen = float(interval.lo)
    offset = control_offset_certificate(
        model["means"],
        model["factor"],
        q=q,
        strike=contract.strike,
        radius=signal.B,
        low_coefficients=low,
        offset=chosen,
        discount=math.exp(-contract.rate * contract.maturity),
    )
    return model, signal.B, offset


def complete_budget(certificate, parent_budget, loader_error):
    d = certificate["dimension"]
    sensitivity = Interval(certificate["sensitivity_upper"])
    parts = dict(
        representation=Interval(parent_budget["components"]["representation"]),
        arithmetic=Interval(certificate["arithmetic_price_error_upper"]),
        preparation=2 * sensitivity * d * Interval(loader_error),
        offset=Interval(certificate["offset_certificate"]["error_upper"]),
        offset_discount_bridge=Interval(certificate["offset_bridge_upper"]),
        decoding=Interval(certificate["decoding_error_upper"]),
    )
    total = sum(parts.values(), Interval(0))
    beta = Fraction(sensitivity.hi) / 2
    return dict(
        components={k: str(v.hi) for k, v in parts.items()},
        deterministic_upper=str(total.hi),
        beta_upper_rational=str(beta),
        sensitivity_upper=str(sensitivity.hi),
        schedule=schedule(beta, Fraction(total.hi)),
        decoder_scale=certificate["decoder_scale"],
        decoder_intercept=certificate["decoder_intercept"],
        physical_execution_error=None,
        confirmation_admitted=False,
    )


def finite_diagnostics(case, spec, low, constants):
    result = []
    contract = contract_of(case)
    for q in (1, 2):
        model, radius, offset = constants[q]
        parent = make_plan(case, spec, q)
        cert = residual_plan(
            parent,
            model["means"],
            model["factor"],
            radius=radius,
            low_coefficients=low,
            offset_certificate=offset,
        )
        if not cert["overflow_safe"]:
            result.append(dict(q=q, status="certificate_failed", reasons=cert["overflow_failures"]))
            continue
        finite = grid(contract, q, 4)
        basket = np.exp(model["means"] + finite["normals"] @ model["factor"].T).mean(axis=1)
        x = (basket - contract.strike) / radius
        monomial = [float(Fraction(c)) for c in cert["polynomial"]["monomial_rationals"]]
        controls = radius * np.polynomial.polynomial.polyval(x, monomial)
        true_residual = np.maximum(basket - contract.strike, 0) - controls
        thresholds, discrepancies = [], []
        scale = 1 << parent["fraction_bits"]
        for packed in range(len(basket)):
            logs = [
                a + sum(((packed >> i) & 1) * c for i, c in enumerate(cs))
                for a, cs in parent["affine_rows"]
            ]
            prices = [
                evaluate_reduced_integer(
                    v, parent["exp_budget"]["coefficients"], 24, spec["reductions"], 100
                )
                for v in logs
            ]
            values = evaluate_control_integer(sum(prices), cert)
            numerator = values["threshold_integer"]
            if not 0 <= numerator < 1 << cert["selector_bits"]:
                raise ArithmeticError("finite residual selector overflow")
            thresholds.append(numerator / (1 << cert["selector_bits"]))
            discrepancies.append(
                abs(values["residual_integer"] / scale / len(prices) - true_residual[packed])
            )
        observed = float(max(discrepancies))
        allowance = float(cert["residual_sum_error_upper"]) / cert["dimension"]
        if observed > allowance + 1e-10:
            raise ArithmeticError("finite residual discrepancy exceeds certificate")
        probability = float(finite["weights"] @ np.asarray(thresholds))
        decoded = cert["decoder_intercept"] + cert["decoder_scale"] * probability
        target = float(
            finite["weights"]
            @ (
                math.exp(-contract.rate * contract.maturity)
                * np.maximum(basket - contract.strike, 0)
            )
        )
        if abs(decoded - target) > float(cert["deterministic_partial_upper"]) + 1e-10:
            raise ArithmeticError("finite restored expectation exceeds certificate")
        result.append(
            dict(
                q=q,
                inputs=len(basket),
                scalar_probability=probability,
                decoded_expectation=decoded,
                target_price=target,
                absolute_error=abs(decoded - target),
                max_residual_pointwise_error=observed,
                residual_error_bound=str(
                    (Interval(cert["residual_sum_error_upper"]) / cert["dimension"]).hi
                ),
                residual_error_units="undiscounted dollars per basket",
                deterministic_partial_upper=cert["deterministic_partial_upper"],
                scope="finite scalar expectation diagnostic; no AE simulation",
            )
        )
    return result


def summarize(rows, primary):
    summaries = []
    for case in CONFIG["cases"]:
        eligible = [r for r in rows if r["case"] == case and r["status"] == "ideal_plan"]
        best = (
            min(eligible, key=lambda r: r["resources"]["control_cancelled_total_cx_projection"])
            if eligible
            else None
        )
        prior = next(r for r in primary["summary"] if r["case"] == case)
        reflection = prior["reflection_reference"]
        entry = dict(
            case=case,
            feasible_configurations=len(eligible),
            best_residual=best,
            best_primary_arithmetic=prior["best_arithmetic"],
            reflection_reference=reflection,
        )
        if best:
            value = best["resources"]["control_cancelled_total_cx_projection"]
            ref = reflection["resources"]["control_cancelled_total_cx_projection"]
            old = prior["best_arithmetic"]["resources"]["control_cancelled_total_cx_projection"]
            entry.update(
                primary_over_residual_rational=str(Fraction(old, value)),
                reflection_over_residual_rational=str(Fraction(ref, value)),
                winner_vs_reflection="residual_arithmetic"
                if value < ref
                else "tie"
                if value == ref
                else "reflection",
            )
        choices = {
            "reflection": reflection["resources"]["control_cancelled_total_cx_projection"],
            "primary_arithmetic": prior["best_arithmetic"]["resources"][
                "control_cancelled_total_cx_projection"
            ],
        }
        if best:
            choices["residual_arithmetic"] = best["resources"][
                "control_cancelled_total_cx_projection"
            ]
        minimum = min(choices.values())
        entry["minimum_logical_projection"] = minimum
        entry["lowest_cost_routes"] = [name for name, value in choices.items() if value == minimum]
        summaries.append(entry)
    return summaries


def run(path):
    from .residual_components import residual_components
    from .components import ResourceLimitError

    primary = archive(ROOT / PRIMARY)
    provenance(primary["planned.json"])
    primary_names = set(primary) | {"complete.json"}
    inputs = {PRIMARY + "/" + n: sha256(ROOT / PRIMARY / n) for n in sorted(primary_names)}
    inputs.update(primary["planned.json"]["input_sha256"])
    inputs[LOW_MODEL] = sha256(ROOT / LOW_MODEL)
    low_manifest = read((ROOT / LOW_MODEL).with_name("complete.json"))
    if inputs[LOW_MODEL] != low_manifest["sha256"]["model.json"]:
        raise ValueError("archived control polynomial hash mismatch")
    inputs[str(Path(LOW_MODEL).with_name("complete.json")).replace("\\", "/")] = sha256(
        (ROOT / LOW_MODEL).with_name("complete.json")
    )
    low = read(ROOT / LOW_MODEL)["low_coefficients"]
    source_names = subprocess.check_output(
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
    source_names = [n for n in source_names if n.endswith(".py")] + [PROTOCOL]
    if "research/stronger_arithmetic/run_residual.py" not in source_names:
        raise ValueError("commit residual sources before acquisition")
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True
    )
    if dirty.strip():
        raise ValueError("commit tracked changes before acquisition")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    sources = {n: sha256(ROOT / n) for n in sorted(source_names)}
    for name in sources:
        blob = subprocess.check_output(["git", "show", head + ":" + name], cwd=ROOT)
        disk = (ROOT / name).read_bytes()
        same = (
            blob == disk
            if name.startswith("research/stronger_arithmetic/") or name == PROTOCOL
            else blob.replace(b"\r\n", b"\n") == disk.replace(b"\r\n", b"\n")
        )
        if not same:
            raise ValueError("uncommitted execution bytes: " + name)
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    write_json(
        path / "planned.json",
        dict(
            config=CONFIG,
            git_head=head,
            source_sha256=sources,
            input_sha256=inputs,
            python=platform.python_version(),
            dependencies={n: version(n) for n in ("numpy", "scipy", "qiskit-terra")},
            started_utc=datetime.now(timezone.utc).isoformat(),
            tracked_tree_dirty=False,
        ),
    )
    try:
        rows, finite = [], []
        loading = primary["loader.json"]
        for case in CASES[:2]:
            print("residual offset certificate", case["id"], flush=True)
            constants = {q: case_constants(case, low, q) for q in (1, 2, 10)}
            model, radius, offset = constants[10]
            write_json(path / (case["id"] + "_offset.json"), offset)
            for index, spec in enumerate(menu()):
                print("residual acquire", case["id"], spec, flush=True)
                candidates = [
                    v
                    for name, v in primary.items()
                    if name.startswith(case["id"] + "_") and v.get("spec") == spec
                ]
                if len(candidates) != 1:
                    raise ValueError("primary exact spec missing/duplicated")
                parent_record = candidates[0]
                parent = make_plan(case, spec)
                equal(parent_record["plan"], parent, "primary parent plan")
                certificate = residual_plan(
                    parent,
                    model["means"],
                    model["factor"],
                    radius=radius,
                    low_coefficients=low,
                    offset_certificate=offset,
                )
                budget = complete_budget(
                    certificate, parent_record["budget"], loading["error_upper"]
                )
                status = (
                    budget["schedule"]["status"]
                    if certificate["overflow_safe"]
                    else "certificate_failed"
                )
                record = dict(
                    case=case["id"],
                    spec=spec,
                    certificate=certificate,
                    budget=budget,
                    status=status,
                    resources=None,
                )
                if status == "ideal_plan" and parent_record["status"] != "ideal_plan":
                    record.update(status="parent_components_unavailable")
                elif status == "ideal_plan":
                    try:
                        component = residual_components(
                            parent,
                            certificate,
                            {**parent_record["components"]["reused"], "parent_plan": parent},
                        )
                        record["components"] = component
                        native = {
                            k: component["native"][k]
                            + len(parent["affine_rows"]) * loading["resources"][k]
                            for k in ("u", "cx")
                        }
                        native["u"] += certificate["selector_bits"] + 1
                        record["resources"] = resources(
                            native, component["qubits"], budget["schedule"]
                        )
                    except ResourceLimitError as error:
                        record.update(status="resource_cap", reason=str(error))
                diagnostics = finite_diagnostics(case, spec, low, constants)
                finite.append(dict(case=case["id"], spec=spec, diagnostics=diagnostics))
                write_json(path / (case["id"] + "_" + str(index).zfill(2) + ".json"), record)
                rows.append(
                    {k: record[k] for k in ("case", "spec", "budget", "status", "resources")}
                )
        write_json(path / "finite.json", finite)
        write_json(
            path / "results.json",
            dict(
                rows=rows,
                summary=summarize(rows, primary["results.json"]),
                candidate_status="standby",
                production_choice=None,
                quantum_over_classical_advantage=False,
                confirmation_admitted=False,
            ),
        )
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
