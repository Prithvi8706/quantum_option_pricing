"""Run the E0 gate battery over the full benchmark and print a report."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from research.paper_a.benchmark import BENCHMARK, VALIDATION_SET
from research.paper_a.environment import capture_environment
from research.paper_a.references import select_support_rule
from research.paper_a.validation import all_passed, run_e0_gates

CONFIG = json.loads(
    (Path(__file__).parent.parent / "configs" / "e0.json").read_text())


def main() -> int:
    contracts = list(BENCHMARK) + list(VALIDATION_SET)
    q_total = select_support_rule(BENCHMARK, CONFIG["q_total_candidates"])
    print(f"selected q_total = {q_total}")
    print(f"environment      = {capture_environment()['packages']}")

    results = run_e0_gates(contracts, q_total, CONFIG["qubit_counts"],
                           CONFIG["rescaling_factor"])
    width = max(len(r.name) for r in results)
    for r in sorted(results, key=lambda x: x.name):
        status = "PASS" if r.passed else "FAIL"
        print(f"  {status}  {r.name:<{width}}  worst={r.worst:.3e}  "
              f"tol={r.tolerance:.1e}  {r.detail}")

    if all_passed(results):
        print("\nE0 PASSED - stochastic experiments are unblocked.")
        return 0
    print("\nE0 FAILED - no stochastic experiment may start.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
