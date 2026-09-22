"""Independent high-precision recomputation of the FT allocation formulas."""

import json
from decimal import Decimal, localcontext
from pathlib import Path


def run():
    data = json.loads(Path("results/controlled_completion_followup/ft_scenarios.json").read_text())
    checks = []
    with localcontext() as ctx:
        ctx.prec = 100
        for row in data["rows"]:
            n_t = row["counts"]["t_count"]
            for scenario in row["scenarios"]:
                p = Decimal(str(scenario["physical_error_probability_assumption"]))
                error = p
                factory = scenario["factory"]
                for _ in range(factory["levels"]):
                    error = 455 * error**3 / (1 - error) ** 15
                reject = 1 - (1 - p) ** 15
                attempts = factory["retries_per_distillation"]
                groups = n_t * sum((15 * attempts) ** j for j in range(factory["levels"]))
                raw = n_t * (15 * attempts) ** factory["levels"]
                retry = groups * reject**attempts + raw * Decimal(2) ** (
                    -factory["raw_injection_retries"]
                )
                p_logical = Decimal(".1") * (100 * p) ** ((scenario["distance"] + 1) // 2)
                faults = scenario["logical_patch_round_exposure_upper"] * p_logical
                magic = n_t * error
                assert groups == factory["distillation_invocations_upper"]
                assert raw == factory["raw_injection_invocations_upper"]
                assert faults < Decimal(".001")
                assert retry < Decimal(".0001")
                assert magic < Decimal(".0005")
                assert faults + retry + magic + Decimal(".0004") < Decimal(".002")
                checks.append(
                    {
                        "tag": row["tag"],
                        "distance": scenario["distance"],
                        "p": str(p),
                        "logical_bound_decimal": str(faults),
                        "retry_bound_decimal": str(retry),
                        "magic_bound_decimal": str(magic),
                    }
                )
    report = {
        "status": (
            "Independent 100-digit Decimal reevaluation; numerical check, "
            "not directed interval proof"
        ),
        "scenario_count": len(checks),
        "all_component_and_total_allocations_pass": True,
        "checks": checks,
    }
    output = Path("results/controlled_completion_followup/financial_ft_cross_review.json")
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("All %d independent scenario allocation checks passed" % len(checks))


if __name__ == "__main__":
    run()
