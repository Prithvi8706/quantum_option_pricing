"""Read-only replay of the separate signed-residual archive.

Certificates and finite diagnostics always replay. Gate re-emission is optional;
even full residual replay inherits the frozen primary conversion gate evidence.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import re

from . import verify as primary_verify
from .verify import archive, equal, integer, ledger, read, safe_file, schedule
from research.journal_sprint.storage import ROOT, sha256, write_json

PROTOCOL = "docs/release/SIGNED_RESIDUAL_PROTOCOL_20260921.md"
PRIMARY = "results/journal_sprint/stronger_arithmetic_v1"
LOW_MODEL = "results/journal_sprint/normalization_approximation_v1/model.json"
LOW_COMPLETE = "results/journal_sprint/normalization_approximation_v1/complete.json"
SPECS = [
    dict(fraction_bits=24, width=48, degree=d, reductions=s)
    for d, s in product((8, 12, 16), (1, 2, 3))
]
CONFIG = dict(
    cases=["D1", "D2"],
    specs=SPECS,
    q=10,
    cutoff=4,
    tolerance="1",
    confidence="0.95",
    repetitions=17,
    call_cap=10_000_000,
    candidate_status="standby",
    confirmation=False,
)
FILES = {"planned.json", "finite.json", "results.json", "D1_offset.json", "D2_offset.json"} | {
    f"{case}_{i:02}.json" for case in CONFIG["cases"] for i in range(9)
}
CAP_REASONS = {
    "conversion exceeds 8,000,000 gates",
    "conversion exceeds 4096 wires",
    "residual oracle exceeds 8M gates or 4096 wires",
    "residual component exceeds 100M gate applications",
}
GATES = ("x", "cx", "ccx")


def normalized(value):
    return json.loads(json.dumps(value, allow_nan=False))


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def provenance(planned, root=ROOT):
    """Bind both acquisition generations, exact live bytes, and committed inputs."""
    root = Path(root)
    head = planned["git_head"]
    if not isinstance(head, str) or not re.fullmatch("[0-9a-f]{40}", head):
        raise ValueError("invalid residual acquisition commit")
    equal(planned["tracked_tree_dirty"], False, "tracked tree declaration")
    names = (
        primary_verify.git(
            root,
            "ls-tree",
            "-r",
            "--name-only",
            head,
            "--",
            "research/journal_sprint",
            "research/stronger_arithmetic",
            "research/release_checks",
        )
        .decode()
        .splitlines()
    )
    expected = {n for n in names if n.endswith(".py")} | {PROTOCOL}
    required = {
        "research/stronger_arithmetic/" + n + ".py"
        for n in (
            "run_residual",
            "residual",
            "residual_circuits",
            "residual_components",
            "verify_residual",
            "verify",
            "run_study",
        )
    }
    if not required <= expected or set(planned["source_sha256"]) != expected:
        raise ValueError("residual source inventory differs")
    for directory in ("research/journal_sprint", "research/release_checks"):
        live = {p.relative_to(root).as_posix() for p in (root / directory).rglob("*.py")}
        if live - expected:
            raise ValueError("untracked executable dependencies")
    primary = archive(root / PRIMARY, primary_verify.FILES)
    references = primary_verify.provenance(primary["planned.json"], root)
    equal(primary["planned.json"]["config"], primary_verify.CONFIG, "primary config")
    for key, value in dict(
        candidate_status="standby",
        production_choice=None,
        confirmation_admitted=False,
        quantum_over_classical_advantage=False,
    ).items():
        equal(primary["results.json"][key], value, "primary promotion")
    equal(
        primary["results.json"]["summary"],
        primary_verify.summary(primary["results.json"]["rows"], references),
        "primary summary",
    )
    inputs = {
        PRIMARY + "/" + n: sha256(safe_file(root / PRIMARY, n))
        for n in set(primary) | {"complete.json"}
    }
    inputs.update(primary["planned.json"]["input_sha256"])
    inputs.update({n: sha256(safe_file(root, n)) for n in (LOW_MODEL, LOW_COMPLETE)})
    equal(planned["input_sha256"], inputs, "residual input inventory/hashes")
    low_complete = read(root / LOW_COMPLETE)
    equal(low_complete["sha256"]["model.json"], inputs[LOW_MODEL], "control model hash")
    for mapping in (planned["source_sha256"], inputs):
        for name, expected_hash in mapping.items():
            disk = safe_file(root, name).read_bytes()
            if hashlib.sha256(disk).hexdigest() != expected_hash:
                raise ValueError("source/input hash mismatch: " + name)
            blob = primary_verify.git(root, "show", head + ":" + name)
            exact = name.startswith("research/stronger_arithmetic/") or name == PROTOCOL
            if (
                blob != disk
                if exact
                else blob.replace(b"\r\n", b"\n") != disk.replace(b"\r\n", b"\n")
            ):
                raise ValueError("source/input differs from residual commit: " + name)
    return primary, read(root / LOW_MODEL)["low_coefficients"]


def prepare_case(case_id, low):
    from . import run_residual as study

    case = next(c for c in study.CASES[:2] if c["id"] == case_id)
    return case, {q: study.case_constants(case, low, q) for q in (1, 2, 10)}


def replay_certificate(context, spec, low, parent_record, loading):
    from . import run_residual as study
    from . import run_study
    from research.journal_sprint.decimal_enclosure import Interval

    case, constants = context
    model, radius, offset = constants[10]
    parent = study.make_plan(case, spec)
    equal(parent_record["plan"], parent, "primary matching plan")
    contract = study.contract_of(case)
    parent_budget = run_study.arithmetic_budget(
        contract, model, parent, Interval(loading["error_upper"]), "0"
    )
    equal(parent_record["budget"], parent_budget, "primary matching budget")
    certificate = study.residual_plan(
        parent,
        model["means"],
        model["factor"],
        radius=radius,
        low_coefficients=low,
        offset_certificate=offset,
    )
    budget = study.complete_budget(certificate, parent_budget, loading["error_upper"])
    finite = study.finite_diagnostics(case, spec, low, constants)
    return normalized((certificate, budget, finite))


def counts(record):
    return {k: integer(record[k]) for k in GATES}


def compiler(total):
    x, cx, ccx = (integer(total[k]) for k in GATES)
    u, cx = x + 9 * ccx, cx + 6 * ccx
    return dict(u=u, cx=cx, controlled_u=6 * u + 9 * cx + 1, controlled_cx=2 * u + 6 * cx)


def semantic_checks(parent, certificate, base):
    """Recompute endpoint integers; these are diagnostics, not gate simulation."""
    from .budget import evaluate_reduced_integer

    checks = []
    row_checks = []
    unit = 1 << certificate["fraction_bits"]
    for packed in (0, (1 << parent["normal_qubits"]) - 1):
        total = 0
        for i, (a, cs) in enumerate(parent["affine_rows"]):
            log = a + sum(((packed >> k) & 1) * c for k, c in enumerate(cs))
            price = evaluate_reduced_integer(
                log,
                parent["exp_budget"]["coefficients"],
                parent["fraction_bits"],
                parent["reductions"],
                parent["spot"],
            )
            total += price
            row_checks.append(
                dict(
                    row=i,
                    packed_input=packed,
                    log_integer=log,
                    price_integer=price,
                    clean_workspace=True,
                    inverse_checked=True,
                )
            )
        delta = total - certificate["strike_sum"]
        x = delta * certificate["reciprocal_integer"] // unit
        y = certificate["control_coefficients"][-1]
        for c in reversed(certificate["control_coefficients"][:-1]):
            y = x * y // unit + c
        control = y * certificate["control_scale_integer"] // unit
        residual = max(delta, 0) - control
        numerator = residual + certificate["shift_integer"]
        lo, hi = certificate["threshold_integer_bounds"]
        if not 0 <= lo <= numerator <= hi < 1 << certificate["selector_bits"]:
            raise ValueError("endpoint outside certified threshold")
        checks.append(
            dict(
                sum_integer=total,
                poststrike_integer=delta,
                normalized_integer=x,
                polynomial_integer=y,
                control_integer=control,
                residual_integer=residual,
                threshold_integer=numerator,
                packed_input=packed,
                selectors=sorted(
                    {0, (1 << certificate["selector_bits"]) - 1, max(0, numerator - 1), numerator}
                ),
                both_initial_flags_checked=True,
                clean_workspace=True,
                inverse_checked=True,
            )
        )
    equal(
        sorted(base["row_checks"], key=lambda r: (r["packed_input"], r["row"])),
        row_checks,
        "primary conversion endpoint evidence",
    )
    return checks


def component_metadata(component, parent, certificate, base):
    """Independent composition from pinned primary counts and recorded new oracle."""
    equal(base["parent_plan"], parent, "bound primary plan")
    for key, expected in dict(
        schema="stronger_arithmetic_components_v1",
        reuse=True,
        reduced=True,
        aggregation_included=True,
        aggregation_zero_initialized=True,
    ).items():
        equal(base[key], expected, "primary component " + key)
    conv, agg, post, cmp = (
        counts(base[k])
        for k in ("conversion_forward", "aggregation", "postaggregation_payoff", "comparator")
    )
    primary_total = {k: 2 * conv[k] + 2 * agg[k] + 2 * post[k] + cmp[k] for k in GATES}
    equal(base["total"], primary_total, "primary gate composition")
    native = compiler(primary_total)
    equal(base["native"], {k: native[k] for k in ("u", "cx")}, "primary native counts")
    equal(base["emitted_gate_applications"], sum(primary_total.values()), "primary applications")
    n, w, d = parent["normal_qubits"], parent["width"], len(parent["affine_rows"])
    s, sold = certificate["selector_bits"], parent["selector_bits"]
    scratch = integer(base["conversion_scratch_per_row"])
    if scratch < 1:
        raise ValueError("positive conversion scratch required")
    equal(
        base["qubits"],
        n + sold + 1 + 2 * w * d + scratch + 3 * w + 1 + 2 * (sold + 1),
        "primary allocation",
    )
    oracle = component["complete_postoracle"]
    oc = counts(oracle)
    if sum(oc.values()) > 8_000_000 or not s + 1 < integer(oracle["qubits"]) <= 4096:
        raise ValueError("oracle cap exceeded")
    total = {k: 2 * conv[k] + 2 * agg[k] + oc[k] for k in GATES}
    if sum(total.values()) > 100_000_000:
        raise ValueError("component cap exceeded")
    native = compiler(total)
    private = oracle["qubits"] - s - 1
    depth = min(
        2 * integer(base["logical_depth"]),
        2 * sum(conv.values()) + 2 * integer(base["aggregation"]["logical_depth"]),
    )
    expected = dict(
        schema="signed_residual_components_v1",
        native={k: native[k] for k in ("u", "cx")},
        qubits=n + s + 1 + 2 * w * d + scratch + private,
        depth_upper=depth + integer(oracle["logical_depth"]),
        depth_kind="conservative_composition_upper_bound",
        actual_remapped_depth=False,
        depth_bound_derivation="min(2*primary_full_depth, 2*conversion_forward_gate_count "
        "+ 2*aggregation_depth) + complete_oracle_depth",
        total=total,
        compiler_counts=native,
        emitted_gate_applications=sum(total.values()),
        inherited_conversion_forward=conv,
        inherited_aggregation_forward=agg,
        complete_postoracle=oracle,
        oracle_private_qubits=private,
        wire_layout=dict(
            inputs=n,
            selector=s,
            flag=1,
            retained_logs_spots=2 * w * d,
            shared_conversion_scratch=scratch,
            total_and_oracle_private=private,
        ),
        aggregation_helper="oracle strike-subtraction helper; zero before and after oracle",
        parent_plan_sha256=digest(parent),
        base_component_sha256=digest(base),
        residual_certificate_sha256=digest(certificate),
        semantic_checks=semantic_checks(parent, certificate, base),
        aggregation_included=True,
        all_inverses_included=True,
        loading_included=False,
        selector_preparation_included=False,
        ae_included=False,
        qualification="Inherited emitted conversion/aggregation counts plus new emitted "
        "sum-to-delta, signed control, shift, comparator and all inverses. "
        "Qubits use shared clean conversion scratch and separate oracle scratch. "
        "Depth is a conservative projection, not an actually remapped full-circuit depth.",
    )
    equal(component, expected, "residual component mapping")


def reemit_component(parent, certificate, base):
    from .residual_components import residual_components

    return residual_components(parent, certificate, base)


def summary(rows, primary):
    result = []
    for case in CONFIG["cases"]:
        eligible = [r for r in rows if r["case"] == case and r["status"] == "ideal_plan"]

        def value(row):
            return integer(row["resources"]["control_cancelled_total_cx_projection"])

        best = min(eligible, key=value) if eligible else None
        prior = next(r for r in primary["summary"] if r["case"] == case)
        reflection, old = prior["reflection_reference"], prior["best_arithmetic"]
        item = dict(
            case=case,
            feasible_configurations=len(eligible),
            best_residual=best,
            best_primary_arithmetic=old,
            reflection_reference=reflection,
        )
        if best:
            a, b = value(best), value(reflection)
            item.update(
                primary_over_residual_rational=str(Fraction(value(old), a)),
                reflection_over_residual_rational=str(Fraction(b, a)),
                winner_vs_reflection="residual_arithmetic"
                if a < b
                else "tie"
                if a == b
                else "reflection",
            )
        choices = dict(reflection=value(reflection), primary_arithmetic=value(old))
        if best:
            choices["residual_arithmetic"] = value(best)
        minimum = min(choices.values())
        item.update(
            minimum_logical_projection=minimum,
            lowest_cost_routes=[name for name, cost in choices.items() if cost == minimum],
        )
        result.append(item)
    return result


def verify(path, *, reemit=False, reemit_selected=False):
    if reemit and reemit_selected:
        raise ValueError("choose full or selected re-emission")
    data = archive(path, FILES)
    equal(data["planned.json"]["config"], CONFIG, "fixed residual config")
    primary, low = provenance(data["planned.json"])
    recorded_rows = data["results.json"]["rows"]
    if len(recorded_rows) != 18:
        raise ValueError("complete 18-row residual menu required")
    loading = primary["loader.json"]
    if Fraction(loading["error_upper"]) < 0:
        raise ValueError("negative recorded loader error")
    for key in ("cx", "u", "qubits", "depth"):
        integer(loading["resources"][key])
    if reemit or reemit_selected:
        equal(loading, primary_verify.reemit_loader(), "re-emitted loader")
    selected = set()
    if reemit_selected:
        for item in summary(recorded_rows, primary["results.json"]):
            if item["best_residual"] is not None:
                selected.add((item["case"], SPECS.index(item["best_residual"]["spec"])))
    rows, finite, emitted, caps, zero_cache = [], [], [], [], {}
    for case in CONFIG["cases"]:
        context = prepare_case(case, low)
        equal(data[case + "_offset.json"], context[1][10][2], "offset certificate")
        for index, spec in enumerate(SPECS):
            label = f"{case}_{index:02}"
            record = data[label + ".json"]
            candidates = [
                v
                for name, v in primary.items()
                if name.startswith(case + "_") and v.get("spec") == spec
            ]
            if len(candidates) != 1:
                raise ValueError("primary exact spec missing/duplicated")
            parent_record = candidates[0]
            cert, budget, diagnostic = replay_certificate(
                context, spec, low, parent_record, loading
            )
            equal(
                budget["schedule"],
                schedule(budget["beta_upper_rational"], budget["deterministic_upper"]),
                "independent schedule",
            )
            parts = [Fraction(v) for v in budget["components"].values()]
            if any(v < 0 for v in parts) or sum(parts) > Fraction(budget["deterministic_upper"]):
                raise ValueError("deterministic budget sum invalid")
            status = budget["schedule"]["status"] if cert["overflow_safe"] else "certificate_failed"
            if status == "ideal_plan" and parent_record["status"] != "ideal_plan":
                status = "parent_components_unavailable"
            expected = dict(
                case=case, spec=spec, certificate=cert, budget=budget, status=status, resources=None
            )
            emit_this = reemit or (case, index) in selected
            if status == "ideal_plan":
                parent = parent_record["plan"]
                base = {**parent_record["components"]["reused"], "parent_plan": parent}
                if record["status"] == "resource_cap":
                    if record.get("reason") not in CAP_REASONS:
                        raise ValueError("invalid resource cap reason")
                    if emit_this:
                        from .components import ResourceLimitError

                        try:
                            reemit_component(parent, cert, base)
                        except ResourceLimitError as error:
                            equal(str(error), record["reason"], "replayed cap reason")
                            caps.append(label)
                        else:
                            raise ValueError("resource cap not reproduced")
                    expected.update(status="resource_cap", reason=record["reason"])
                else:
                    component = record["components"]
                    component_metadata(component, parent, cert, base)
                    if emit_this:
                        equal(component, reemit_component(parent, cert, base), "re-emitted oracle")
                        emitted.append(label)
                    native = {
                        k: component["native"][k]
                        + len(parent["affine_rows"]) * loading["resources"][k]
                        for k in ("u", "cx")
                    }
                    native["u"] += cert["selector_bits"] + 1
                    zero = record["resources"]["zero_reflection_cx_projection"]
                    if emit_this:
                        qubits = component["qubits"]
                        if qubits not in zero_cache:
                            zero_cache[qubits] = primary_verify.reemit_zero(qubits)
                        equal(zero, zero_cache[qubits], "re-emitted zero reflection")
                    expected.update(
                        components=component,
                        resources=ledger(native, component["qubits"], zero, budget["schedule"]),
                    )
            equal(record, expected, "residual record " + label)
            rows.append({k: expected[k] for k in ("case", "spec", "budget", "status", "resources")})
            finite.append(dict(case=case, spec=spec, diagnostics=diagnostic))
    equal(data["finite.json"], finite, "finite residual diagnostics")
    equal(
        data["results.json"],
        dict(
            rows=rows,
            summary=summary(rows, primary["results.json"]),
            candidate_status="standby",
            production_choice=None,
            quantum_over_classical_advantage=False,
            confirmation_admitted=False,
        ),
        "results/menu/promotion",
    )
    feasible = sum(r["status"] == "ideal_plan" for r in rows)
    return dict(
        passed=True,
        rows_checked=18,
        certificates_replayed=18,
        finite_configurations_replayed=18,
        offset_certificates_replayed=2,
        independent_schedules_checked=18,
        logical_cx_ledgers_checked=2 * feasible,
        files_checked=len(FILES) + 1,
        inputs_source_head_checked=True,
        gate_reconstruction_mode="all_residual_oracles"
        if reemit
        else "selected_residual_oracles"
        if reemit_selected
        else "metadata",
        all_gates_reconstructed=False,
        inherited_primary_gates_reemitted=False,
        oracle_acquisitions_total=feasible,
        oracle_acquisitions_reemitted=len(emitted),
        reemitted_configurations=emitted,
        resource_cap_configurations_replayed=caps,
        loader_reemitted=bool(reemit or reemit_selected),
        zero_reflection_acquisitions_reemitted=len(zero_cache),
        scope="All residual certificates, finite diagnostics and logical compositions checked. "
        "Only listed oracles were re-emitted; other oracle counts and inherited primary "
        "conversion/aggregation gates are recorded metadata. Depth is a composition upper bound.",
        candidate_status="standby",
        confirmation_admitted=False,
    )


def verify_replay(first, replay, *, reemit=False, reemit_selected=False):
    checks = [verify(p, reemit=reemit, reemit_selected=reemit_selected) for p in (first, replay)]
    for name in FILES - {"planned.json"}:
        equal(
            read(Path(first) / name),
            read(Path(replay) / name),
            "residual acquisition replay " + name,
        )
    a, b = (read(Path(p) / "planned.json") for p in (first, replay))
    for key in ("config", "git_head", "source_sha256", "input_sha256"):
        equal(a[key], b[key], "residual replay provenance " + key)
    return dict(passed=True, exact_replay=True, checks=checks)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    options = parser.add_mutually_exclusive_group()
    options.add_argument("--reemit", action="store_true")
    options.add_argument("--reemit-selected", action="store_true")
    args = parser.parse_args(argv)
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.output.resolve().is_relative_to(args.archive.resolve()):
        raise ValueError("output must be outside the exclusive archive")
    report = verify(args.archive, reemit=args.reemit, reemit_selected=args.reemit_selected)
    write_json(args.output, {**report, "verifier_sha256": sha256(Path(__file__))})


if __name__ == "__main__":
    main()
