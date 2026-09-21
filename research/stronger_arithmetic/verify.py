"""Verify a frozen bounded study; optionally re-emit expensive gate acquisitions.

Run in the acquisition's pinned environment, with its source/input bytes checked
out. Default replay reconstructs certificates and finite diagnostics, but treats
emitted component, loader and zero-reflection counts as recorded metadata.
"""

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

from research.release_checks.json_io import read
from research.journal_sprint.storage import ROOT, sha256, write_json


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
SPECS = [None] + [
    dict(zip(("fraction_bits", "width", "degree", "reductions"), v))
    for v in product((20, 24), (40, 48), (8, 12, 16), (1, 2, 3))
]
FILES = {"planned.json", "loader.json", "finite.json", "results.json"} | {
    f"{case}_{i:02}.json" for case in ("D1", "D2") for i in range(37)
}


def equal(actual, expected, label):
    # JSON equality must distinguish booleans from integers, including in lists.
    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(
        expected, sort_keys=True, allow_nan=False
    ):
        raise ValueError(label + " differs")


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError("nonnegative integer required")
    return value


def safe_file(root, name):
    if not isinstance(name, str) or "\\" in name or ":" in name:
        raise ValueError("unsafe manifest path")
    parts = PurePosixPath(name)
    if (
        parts.is_absolute()
        or parts.as_posix() != name
        or any(p in (".", "..") for p in parts.parts)
        or not parts.parts
    ):
        raise ValueError("unsafe manifest path")
    path = root
    for part in parts.parts:
        path = path / part
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError("linked manifest path")
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("missing/outside manifest file: " + name)
    return path


def archive(path, expected=None):
    """Check an exact, flat, exclusive archive and parse every artifact strictly."""
    path = Path(path)
    complete = read(safe_file(path, "complete.json"))
    manifest = complete["sha256"]
    if not isinstance(manifest, dict) or "complete.json" in manifest:
        raise ValueError("invalid archive manifest")
    if expected is not None and set(manifest) != expected:
        raise ValueError("manifest inventory differs")
    if {p.name for p in path.iterdir()} != set(manifest) | {"complete.json"}:
        raise ValueError("archive inventory differs")
    records = {}
    for name, digest in manifest.items():
        if "/" in name:
            raise ValueError("archive manifest must be flat")
        item = safe_file(path, name)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("invalid digest")
        if sha256(item) != digest:
            raise ValueError("artifact hash mismatch: " + name)
        records[name] = read(item)
    return records


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def provenance(planned, root=ROOT):
    root = Path(root)
    head = planned["git_head"]
    if not isinstance(head, str) or not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("invalid acquisition commit")
    equal(planned["tracked_tree_dirty"], False, "tracked tree declaration")
    names = (
        git(
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
    mandatory = {
        "research/stronger_arithmetic/" + n + ".py"
        for n in ("run_study", "budget", "circuits", "components", "verify")
    }
    sources = planned["source_sha256"]
    if not mandatory <= expected or set(sources) != expected:
        raise ValueError("source inventory differs from committed tree")
    for directory in ("research/journal_sprint", "research/release_checks"):
        unexpected = {p.relative_to(root).as_posix() for p in (root / directory).rglob("*.py")}
        if unexpected - expected:
            raise ValueError("untracked executable dependencies")
    references = archive(root / REFERENCE)
    inputs = planned["input_sha256"]
    if set(inputs) != {REFERENCE + "/" + n for n in set(references) | {"complete.json"}}:
        raise ValueError("input inventory differs")
    for mapping in (sources, inputs):
        for name, digest in mapping.items():
            disk = safe_file(root, name).read_bytes()
            if hashlib.sha256(disk).hexdigest() != digest:
                raise ValueError("source/input hash mismatch: " + name)
            committed = git(root, "show", head + ":" + name)
            exact = name.startswith("research/stronger_arithmetic/") or name == PROTOCOL
            same = (
                committed == disk
                if exact
                else (committed.replace(b"\r\n", b"\n") == disk.replace(b"\r\n", b"\n"))
            )
            if not same:
                raise ValueError("source/input bytes differ from acquisition commit: " + name)
    return {c: references["case_" + c + ".json"] for c in CONFIG["cases"]}


def pi_upper():
    def bounds(inv, terms):
        value = sum(
            (Fraction((-1) ** k, (2 * k + 1) * inv ** (2 * k + 1)) for k in range(terms)),
            Fraction(0),
        )
        other = value + Fraction((-1) ** terms, (2 * terms + 1) * inv ** (2 * terms + 1))
        return min(value, other), max(value, other)

    return 16 * bounds(5, 48)[1] - 4 * bounds(239, 12)[0]


PI = pi_upper()


def schedule(beta, deterministic):
    """Independent exact-rational AE schedule, including minimal dyadic M."""
    beta, deterministic = Fraction(beta), Fraction(deterministic)
    if beta <= 0 or deterministic < 0:
        raise ValueError("invalid budget")
    remaining = 1 - deterministic
    if remaining <= 0:
        return dict(status="deterministic_budget_exhausted", M=None, a_calls=None)
    m = 2
    while 2 * beta * (PI / m + PI**2 / m**2) > remaining:
        m *= 2
        if m > 2**40:
            return dict(status="precision_cap", M=None, a_calls=None)
    bound = 2 * beta * (PI / m + PI**2 / m**2)
    calls = 17 * (2 * m - 1)
    return dict(
        status="ideal_plan" if calls <= 10_000_000 else "query_cap",
        M=m,
        a_calls=calls,
        phase_qubits=m.bit_length() - 1,
        repetitions=17,
        statistical_upper_rational=str(bound),
        fixed_schedule_margin_rational=str(remaining - bound),
    )


def ledger(native, qubits, zero, ae):
    cx, u, qubits, zero = map(integer, (native["cx"], native["u"], qubits, zero))
    if qubits < 2:
        raise ValueError("invalid A qubits")
    controlled = 6 * cx + 2 * u
    m, bits, reps = ae["M"], ae["phase_qubits"], ae["repetitions"]
    qft = bits * (bits - 1) + 3 * (bits // 2)
    return dict(
        a_cx_projection=cx,
        a_u_projection=u,
        controlled_a_cx_projection=controlled,
        zero_reflection_cx_projection=zero,
        a_qubits=qubits,
        total_qubits=2 * qubits - 2 + bits,
        total_cx_projection=reps * (cx + (m - 1) * (2 * controlled + zero + 1) + qft),
        control_cancelled_total_cx_projection=reps * (cx + (m - 1) * (2 * cx + zero + 1) + qft),
        physical_execution_error=None,
    )


def replay_certificate(case_id, spec, loader_error):
    from . import run_study as study
    from research.journal_sprint.decimal_enclosure import Interval

    case = next(c for c in study.CASES[:2] if c["id"] == case_id)
    plan = study.make_plan(case, spec)
    contract = study.contract_of(case)
    budget = study.arithmetic_budget(
        contract, study.setup(contract), plan, Interval(loader_error), "0"
    )
    finite = study.finite_diagnostics(case, spec)
    return json.loads(json.dumps((plan, budget, finite), allow_nan=False))


def reemit_components(plan, reduced):
    from .components import components_both

    return components_both(plan, reduced=reduced)


def reemit_loader():
    from . import run_study as study

    circuit, error = study.loader(10)
    return dict(resources=study.cost(circuit), error_upper=str(error.hi))


def reemit_zero(qubits):
    from . import run_study as study

    return study.zero_cost(qubits)


def summary(rows, references):
    result = []
    for case in CONFIG["cases"]:
        eligible = [r for r in rows if r["case"] == case and r["status"] == "ideal_plan"]
        candidates = [r for r in eligible if r["arm"] == "range_reduced"]

        def value(r):
            return integer(r["resources"]["control_cancelled_total_cx_projection"])

        best = min(candidates, key=value) if candidates else None
        alternatives = references[case]["alternatives"]
        reflection = min(
            (
                r
                for r in alternatives
                if r["mode"] == "reflection"
                and r["resources"]["control_cancelled_total_cx_projection"] is not None
            ),
            key=value,
        )
        base = next(r for r in alternatives if r["mode"] == "ripple")
        item = dict(
            case=case,
            feasible_rows=len(eligible),
            best_reduced=best,
            best_arithmetic=min(eligible, key=value) if eligible else None,
            reflection_reference=reflection,
            original_arithmetic_reference=base,
        )
        if best:
            a, b = value(best), value(reflection)
            item.update(
                original_over_reduced_rational=str(Fraction(value(base), a)),
                reduced_over_reflection_rational=str(Fraction(a, b)),
                winner="arithmetic" if a < b else "tie" if a == b else "reflection",
            )
        result.append(item)
    return result


def verify(path, *, reemit=False, reemit_selected=False):
    """Verify against local frozen sources/inputs; no acquisition is modified."""
    if reemit and reemit_selected:
        raise ValueError("choose either full or selected re-emission")
    data = archive(path, FILES)
    planned = data["planned.json"]
    equal(planned["config"], CONFIG, "fixed config")
    references = provenance(planned)
    loading = data["loader.json"]
    if Fraction(loading["error_upper"]) < 0:
        raise ValueError("negative loader error")
    for key in ("cx", "u", "qubits", "depth"):
        integer(loading["resources"][key])
    if reemit or reemit_selected:
        equal(loading, reemit_loader(), "re-emitted loader")
    if len(data["results.json"]["rows"]) != 148:
        raise ValueError("expected complete 148-row menu")
    rows, finite, emitted, zero_cache = [], [], 0, {}
    cap_rows = 0
    caps_replayed = 0
    selected = {(case, 0) for case in CONFIG["cases"]} if reemit_selected else set()
    if reemit_selected:
        # Recompute the choice from rows; the complete rows and summary are
        # independently checked below before any successful report is returned.
        for item in summary(data["results.json"]["rows"], references):
            if item["best_reduced"] is not None:
                selected.add((item["case"], SPECS.index(item["best_reduced"]["spec"])))
    reconstructed = []
    for case in CONFIG["cases"]:
        for index, spec in enumerate(SPECS):
            emit_this = reemit or (case, index) in selected
            record = data[f"{case}_{index:02}.json"]
            plan, budget, diagnostic = replay_certificate(case, spec, loading["error_upper"])
            if spec is None:
                equal(plan, references[case]["arithmetic_plan"], "archived baseline/model drift")
            ae = schedule(budget["beta_upper"], budget["deterministic_upper"])
            equal(budget["schedule"], ae, "independent schedule")
            parts = list(map(Fraction, budget["components"].values()))
            if any(p < 0 for p in parts) or sum(parts) > Fraction(budget["deterministic_upper"]):
                raise ValueError("invalid deterministic budget sum")
            status = ae["status"] if plan["overflow_safe"] else "overflow_certificate_failed"
            arm = "workspace_only" if spec is None else "range_reduced"
            expected = dict(case=case, spec=spec, arm=arm, plan=plan, budget=budget, status=status)
            if record["status"] == "resource_cap":
                if status != "ideal_plan" or record.get("reason") not in {
                    "conversion exceeds 8,000,000 gates",
                    "conversion exceeds 4096 wires",
                    "component exceeds 100,000,000 gate applications",
                }:
                    raise ValueError("invalid resource cap declaration")
                if emit_this:
                    from .components import ResourceLimitError

                    try:
                        reemit_components(plan, spec is not None)
                    except ResourceLimitError as error:
                        equal(str(error), record["reason"], "re-emitted resource cap")
                        caps_replayed += 1
                    else:
                        raise ValueError("resource cap not reproduced")
                status = "resource_cap"
                expected.update(status=status, reason=record["reason"])
                cap_rows += 2
            if status == "ideal_plan":
                component = record["components"]
                equal(sorted(component), ["retained", "reused"], "component layouts")
                if emit_this:
                    equal(
                        component,
                        reemit_components(plan, spec is not None),
                        "re-emitted components",
                    )
                    emitted += 1
                    reconstructed.append(f"{case}_{index:02}")
                expected["components"] = component
            equal(record, expected, "case record " + case + f"_{index:02}")
            finite.append(dict(case=case, spec=spec, diagnostics=diagnostic))
            for layout in ("retained", "reused"):
                row = dict(
                    case=case,
                    arm=arm,
                    spec=spec,
                    layout=layout,
                    status=status,
                    budget=budget,
                    resources=None,
                )
                if status == "resource_cap":
                    row["reason"] = record["reason"]
                if status == "ideal_plan":
                    detail = component[layout]
                    total = detail["total"]
                    x, cx, ccx = (integer(total[k]) for k in ("x", "cx", "ccx"))
                    native = dict(cx=cx + 6 * ccx, u=x + 9 * ccx)
                    equal(detail["native"], native, "component native decomposition")
                    equal(detail["reuse"], layout == "reused", "layout reuse")
                    equal(detail["reduced"], spec is not None, "component arm")
                    for k in native:
                        native[k] += len(plan["affine_rows"]) * loading["resources"][k]
                    native["u"] += plan["selector_bits"] + 1
                    # Counts below are metadata unless explicitly reconstructed.
                    recorded_row = data["results.json"]["rows"][len(rows)]
                    zero = recorded_row["resources"]["zero_reflection_cx_projection"]
                    if emit_this:
                        qubits = detail["qubits"]
                        if qubits not in zero_cache:
                            zero_cache[qubits] = reemit_zero(qubits)
                        equal(zero, zero_cache[qubits], "re-emitted reflection")
                    row.update(
                        arithmetic_depth=integer(detail["logical_depth"]),
                        resources=ledger(native, detail["qubits"], zero, ae),
                    )
                rows.append(row)
    equal(data["finite.json"], finite, "finite diagnostics")
    equal(
        data["results.json"],
        dict(
            rows=rows,
            summary=summary(rows, references),
            residual_arm=dict(
                status="not_admitted",
                reason="signed residual certificate and emitted oracle required",
            ),
            candidate_status="standby",
            quantum_over_classical_advantage=False,
            confirmation_admitted=False,
            production_choice=None,
        ),
        "results/menu/promotion",
    )
    return dict(
        passed=True,
        rows_checked=len(rows),
        files_checked=len(FILES) + 1,
        source_files_checked=len(planned["source_sha256"]),
        inputs_source_head_checked=True,
        certificates_replayed=74,
        finite_diagnostics_replayed=74,
        independent_schedules_checked=74,
        logical_cx_ledgers_checked=2 * sum(r["status"] == "ideal_plan" for r in rows),
        gate_reconstruction=bool(reemit),
        gate_reconstruction_mode="all" if reemit else "selected" if reemit_selected else "metadata",
        component_acquisitions_reemitted=emitted,
        component_acquisitions_total=sum(r["status"] == "ideal_plan" for r in rows) // 2,
        configurations_total=74,
        component_rows_reemitted=2 * emitted,
        reemitted_configurations=reconstructed,
        loader_reemitted=bool(reemit or reemit_selected),
        zero_reflection_acquisitions_reemitted=len(zero_cache),
        resource_cap_rows=cap_rows,
        resource_caps_reconstructed=bool(reemit),
        resource_cap_configurations_replayed=caps_replayed,
        scope=(
            "Re-emitted components, loader and reflections; independent logical CX ledgers."
            if reemit
            else "Selected baseline/best reduced components, loader and selected reflections "
            "re-emitted; remaining gate counts and cap outcomes are metadata. "
            "All certificates, finite diagnostics and logical CX ledgers checked."
            if reemit_selected
            else "Component, loader and reflection counts are recorded "
            "metadata; "
            "certificates/finite diagnostics replayed; independent logical CX ledgers."
        ),
        confirmation_admitted=False,
        candidate_status="standby",
    )


def verify_replay(first, replay, *, reemit=False, reemit_selected=False):
    """Compare full acquisitions made by the parent in separate environments."""
    checks = [verify(p, reemit=reemit, reemit_selected=reemit_selected) for p in (first, replay)]
    for name in FILES - {"planned.json"}:
        equal(read(Path(first) / name), read(Path(replay) / name), "acquisition replay " + name)
    a, b = (read(Path(p) / "planned.json") for p in (first, replay))
    for key in ("config", "git_head", "source_sha256", "input_sha256"):
        equal(a[key], b[key], "replay provenance " + key)
    return dict(passed=True, exact_replay=True, checks=checks)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    replay_options = parser.add_mutually_exclusive_group()
    replay_options.add_argument("--reemit", action="store_true")
    replay_options.add_argument("--reemit-selected", action="store_true")
    args = parser.parse_args(argv)
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.output.resolve().is_relative_to(args.archive.resolve()):
        raise ValueError("verification output must be outside the exclusive archive")
    report = verify(args.archive, reemit=args.reemit, reemit_selected=args.reemit_selected)
    write_json(args.output, {**report, "verifier_sha256": sha256(Path(__file__))})


if __name__ == "__main__":
    main()
