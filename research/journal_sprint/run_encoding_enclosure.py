"""Deterministic gate-development audit; no acquisitions or confirmation seeds."""

import argparse
from datetime import datetime, timezone
import decimal
from decimal import Decimal
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess

from .asian_basket import Basket
from .encoding_enclosure import base_enclosure, at_precision
from .storage import ROOT, sha256, write_json


PROTOCOL = "docs/journal_sprint/CONFIRMATION_GATE_BOUNDS.md"
CONFIG = dict(
    cases=list(range(6)),
    cutoffs=[3, 4, 5],
    representations=["raw", "residual"],
    precisions=list(range(1, 17)),
    partial_budget="0.25",
    confirmation=False,
)
SOURCES = [
    "research/journal_sprint/" + name
    for name in (
        "decimal_enclosure.py",
        "encoding_enclosure.py",
        "run_encoding_enclosure.py",
        "asian_basket.py",
        "price_contract.py",
        "encoding_decision.py",
        "storage.py",
        "intervals.py",
        "__init__.py",
    )
] + ["research/__init__.py", PROTOCOL]


def source_identity():
    return {name: sha256(ROOT / name) for name in SOURCES}


def input_identity():
    path = ROOT / "results/journal_sprint/w13_encoding_v1"
    recorded = json.loads((path / "complete.json").read_text())
    actual = {
        p.relative_to(path).as_posix(): sha256(p)
        for p in path.rglob("*")
        if p.is_file() and p != path / "complete.json"
    }
    if actual != {Path(k).as_posix(): v for k, v in recorded["sha256"].items()}:
        raise ValueError("input inventory or digest mismatch")
    return {"manifest": sha256(path / "complete.json")}


def calculate(case, cutoff):
    original = json.loads(
        (ROOT / f"results/journal_sprint/w13_encoding_v1/case_{case}.json").read_text()
    )
    contract = Basket(**original["basket"])
    model = dict(
        means=original["means"],
        factor=original["factor"],
        expected_control=original["rows"][1]["contract"]["offset"],
    )
    rows, first = [], {}
    for rep in CONFIG["representations"]:
        base = base_enclosure(contract, model, cutoff, rep)
        records = [at_precision(base, q) for q in CONFIG["precisions"]]
        for record in records:
            record["partial_budget_met"] = Decimal(record["partial_sum"]["upper"]) <= Decimal(
                CONFIG["partial_budget"]
            )
        rows.extend(records)
        first[rep] = next((r for r in records if r["partial_budget_met"]), None)
    return dict(
        case=case,
        cutoff=cutoff,
        basket=original["basket"],
        rows=rows,
        first_partial_budget=first,
        old_at_original_cutoff_and_precision={
            row["representation"]: row["analytic_bounds"] for row in original["rows"]
        },
        original_precision=original["case"][2],
        application_admitted=False,
    )


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    active = "provenance"
    try:
        sources, inputs = source_identity(), input_identity()
        write_json(
            output / "planned.json",
            dict(
                config=CONFIG,
                sources=sources,
                inputs=inputs,
                python=platform.python_version(),
                git_head=subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
                libmpdec=decimal.__libmpdec_version__,
                started_utc=datetime.now(timezone.utc).isoformat(),
            ),
        )
        for name in sources:
            destination = output / "sources" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        for case in CONFIG["cases"]:
            for cutoff in CONFIG["cutoffs"]:
                active = f"case_{case}_cutoff_{cutoff}"
                write_json(output / f"{active}_started.json", dict(case=case, cutoff=cutoff))
                write_json(output / f"{active}.json", calculate(case, cutoff))
        if source_identity() != sources or input_identity() != inputs:
            raise ValueError("sources/input changed during deterministic audit")
        if any(sha256(output / "sources" / n) != h for n, h in sources.items()):
            raise ValueError("source snapshot mismatch")
        write_json(
            output / "complete.pending.json",
            dict(
                finished_utc=datetime.now(timezone.utc).isoformat(),
                sha256={
                    p.relative_to(output).as_posix(): sha256(p)
                    for p in sorted(output.rglob("*"))
                    if p.is_file()
                },
                confirmation=False,
                application_admitted=False,
            ),
        )
        os.rename(output / "complete.pending.json", output / "complete.json")
    except BaseException as error:
        try:
            write_json(
                output / "failure.json",
                dict(
                    stage=active, type=type(error).__name__, message=str(error), confirmation=False
                ),
            )
        except BaseException:
            pass
        raise
    cells = len(CONFIG["cases"]) * len(CONFIG["cutoffs"])
    return dict(
        cases=len(CONFIG["cases"]),
        cutoff_cells=cells,
        rows=cells * len(CONFIG["representations"]) * len(CONFIG["precisions"]),
        confirmation=False,
    )


def verify(output):
    output = Path(output)
    read = lambda name: json.loads((output / name).read_text())  # noqa: E731
    manifest = read("complete.json")
    if set(manifest) != {"finished_utc", "sha256", "confirmation", "application_admitted"}:
        raise ValueError("manifest schema mismatch")
    actual = {
        p.relative_to(output).as_posix(): sha256(p)
        for p in output.rglob("*")
        if p.is_file() and p != output / "complete.json"
    }
    if actual != manifest["sha256"] or manifest["confirmation"] or manifest["application_admitted"]:
        raise ValueError("inventory/digest or scope mismatch")
    plan = read("planned.json")
    if set(plan) != {
        "config",
        "sources",
        "inputs",
        "python",
        "git_head",
        "libmpdec",
        "started_utc",
    } or not re.fullmatch(r"[0-9a-f]{40}", plan["git_head"]):
        raise ValueError("plan schema or Git identity mismatch")
    start, end = (
        datetime.fromisoformat(t) for t in (plan["started_utc"], manifest["finished_utc"])
    )
    if (
        start.utcoffset() != timezone.utc.utcoffset(None)
        or end.utcoffset() != start.utcoffset()
        or end < start
    ):
        raise ValueError("invalid UTC chronology")
    if (
        plan["config"] != CONFIG
        or plan["sources"] != source_identity()
        or plan["inputs"] != input_identity()
        or plan["python"] != platform.python_version()
        or plan["libmpdec"] != decimal.__libmpdec_version__
    ):
        raise ValueError("provenance mismatch")
    expected = {"planned.json"}
    for name, digest in plan["sources"].items():
        filename = "sources/" + name
        if actual[filename] != digest:
            raise ValueError("source copy mismatch")
        expected.add(filename)
    for case in CONFIG["cases"]:
        for cutoff in CONFIG["cutoffs"]:
            stem = f"case_{case}_cutoff_{cutoff}"
            if read(f"{stem}_started.json") != dict(case=case, cutoff=cutoff):
                raise ValueError("started marker mismatch")
            if read(f"{stem}.json") != calculate(case, cutoff):
                raise ValueError("deterministic replay mismatch")
            expected.update((f"{stem}.json", f"{stem}_started.json"))
    if expected != set(actual):
        raise ValueError("unconsumed records")
    rows = (
        len(CONFIG["cases"])
        * len(CONFIG["cutoffs"])
        * len(CONFIG["representations"])
        * len(CONFIG["precisions"])
    )
    return dict(files=len(actual) + 1, rows=rows, exact_decimal_replay=True, confirmation=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("run", "verify"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps((run if args.action == "run" else verify)(args.output), indent=2))
