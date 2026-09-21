"""Exhaust the archived AE label menus and recheck dollar margins without acquisition."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import time

from .label_bridge import label_amplitude, price_allowance


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "results/journal_sprint/signed_residual_arithmetic_v1"


def pi_upper():
    """Independent rational Machin enclosure using alternating-series remainder."""
    def arctan_bounds(denominator):
        terms = 100
        total = sum(
            (Fraction((-1) ** k, (2 * k + 1) * denominator ** (2 * k + 1))
             for k in range(terms)),
            Fraction(0),
        )
        remainder = Fraction(1, (2 * terms + 1) * denominator ** (2 * terms + 1))
        return total - remainder, total + remainder

    lo239, _ = arctan_bounds(239)
    _, hi5 = arctan_bounds(5)
    return 16 * hi5 - 4 * lo239


def verify():
    start = time.process_time()
    paths = sorted(ARCHIVE.glob("D[12]_0[0-8].json"))
    if len(paths) != 18:
        raise ValueError("expected all 18 frozen residual configuration records")
    records = [(p, json.loads(p.read_text(encoding="utf-8"))) for p in paths]
    sizes = sorted({r["budget"]["schedule"]["M"] for _, r in records})
    if any(m > 4096 for m in sizes) or sum(sizes) > 20000:
        raise ValueError("label verification exceeds the declared menu cap")
    errors = {}
    for size in sizes:
        error = Fraction(0)
        for label in range(size):
            if time.process_time() - start > 300:
                raise TimeoutError("five-minute CPU verification cap reached")
            row = label_amplitude(label, size)
            error = max(error, Fraction(row["conversion_error_upper"]))
        errors[size] = error
    upper = pi_upper()
    rows = []
    for path, record in records:
        certificate, budget = record["certificate"], record["budget"]
        size = budget["schedule"]["M"]
        # Decimal outward multiplication is audited against its exact rational operands.
        err = errors[size]
        scale = Fraction(certificate["sensitivity_upper"])
        charge = scale * err
        deterministic = Fraction(budget["deterministic_upper"]) + charge

        def statistical(m):
            return scale * (upper / m + upper * upper / (m * m))

        margin = 1 - deterministic - statistical(size)
        previous_margin = 1 - deterministic - statistical(size // 2) if size > 2 else None
        if margin < 0:
            raise AssertionError(f"{path.name}: original schedule fails after label bridge")
        if previous_margin is not None and previous_margin >= 0:
            raise AssertionError(f"{path.name}: original schedule is not minimal")
        # Verify public allowance helper at a rationally enclosing decimal input.
        rounded_error = label_amplitude(size // 3, size)["conversion_error_upper"]
        assert Fraction(price_allowance(certificate["sensitivity_upper"], rounded_error)) >= (
            scale * Fraction(rounded_error)
        )
        rows.append({
            "configuration": path.stem,
            "M": size,
            "label_error_upper_rational": str(err),
            "additional_price_allowance_rational": str(charge),
            "additional_price_allowance_display": float(charge),
            "remaining_margin_rational": str(margin),
            "remaining_margin_display": float(margin),
            "previous_dyadic_margin_rational": str(previous_margin),
            "schedule_unchanged_and_minimal": True,
        })
    sources = list(Path(__file__).parent.glob("*.py")) + [
        ROOT / "research/journal_sprint/week2_decoding.py",
        ROOT / "research/journal_sprint/decimal_enclosure.py",
        ROOT / "research/journal_sprint/normal_loader_budget.py",
        ROOT / "docs/novelty_assessment/2026-09-21/LABEL_BRIDGE_PROTOCOL.md",
    ]
    return {
        "schema": "assessment_label_bridge_v1",
        "date": "2026-09-21",
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "source_hashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(sources)},
        "input_hashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p, _ in records},
        "labels_checked": sum(sizes),
        "distinct_M": sizes,
        "rows": rows,
        "all_schedules_unchanged": True,
        "scope": "Deterministic label conversion and price-budget overlay; no circuits or new pricing data.",
        "physical_errors_certified": False,
        "confirmation_admitted": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = verify()
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(f"Verified {report['labels_checked']} labels and {len(report['rows'])} schedules")


if __name__ == "__main__":
    main()
