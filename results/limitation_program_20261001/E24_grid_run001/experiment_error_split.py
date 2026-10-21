"""One represented source width and three exact statistical shares, locally."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.financial_bounded_schedule import certified_schedule
from research.limitation_program_20261001.financial_estimator_ledger import assemble_estimator_row
from research.limitation_program_20261001.financial_iqft import synthesized_row


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    receipts = ("E07_complete_run001", "E02_IQFT_run001", "E02_IQFT_audit_run001")
    assert all(read(PROGRAM / name / "summary.json")["passed"] for name in receipts)
    output.mkdir()
    frozen = {}
    for name in receipts:
        directory = PROGRAM / name
        receipt = read(directory / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    code = Path(__file__).resolve()
    frozen[relative(code)] = digest(code)
    shutil.copy2(code, output / code.name)
    protocol = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        local_only=True,
        before_finite_grid_reconciliation=True,
        represented_source_widths=[dict(native=72, fraction=40, midpoint_uniform=32)],
        statistical_shares_exact=[[1, 4], [9, 20], [13, 20]],
        epsilon_dollars_exact=[1, 100],
        estimator_failure_exact=[3, 1000],
        cases=["B4x12", "B8x52"],
        source_variants=1,
        continuous_bound_interpolation_or_different_law_transfer_allowed=False,
        acceptance=(
            "Full-price feasibility requires the existing exact-source bias and "
            "physical certificates; unproved rows remain conditional regardless "
            "of lower digital logical cost"
        ),
        stop_rule=(
            "Exactly the one represented width times three shares; no new "
            "precision, law, rotations or financial runs. Retain the current split "
            "unless a complete compatible certificate proves feasibility."
        ),
        frozen_inputs=frozen,
        new_pytest_cases=0,
        financial_prices_or_gate_replays=0,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    rotations = read(PROGRAM / "E02_IQFT_run001/rotations.json")
    rows = []
    for case in protocol["cases"]:
        wrapper = read(PROGRAM / "E02_financial_run002" / case / "iterate.json")
        complete = read(PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"))
        assert not complete["assessment"]["complete_price_certified"]
        base_T = read(PROGRAM / "E02_IQFT_run001" / case / "synthesized_estimator_ledger.json")[
            "full_T_count"
        ]
        for numerator, denominator in protocol["statistical_shares_exact"]:
            fraction = Fraction(numerator, denominator)
            allowance = Fraction(1, 100) * fraction
            schedule = certified_schedule(allowance, Fraction(3, 1000), 64)
            row = assemble_estimator_row(wrapper, schedule)
            required = ["pi_1_%d" % (1 << (gap + 1)) for gap in range(2, schedule["qpe_bits"])]
            missing = [key for key in required if key not in rotations]
            candidate = output / case / (str(numerator) + "_of_" + str(denominator))
            candidate.mkdir(parents=True)
            save(candidate / "schedule.json", schedule)
            if not missing:
                operations, row = synthesized_row(
                    row, rotations, relative(candidate / "iqft_operations.json")
                )
                save(candidate / "iqft_operations.json", operations)
            save(candidate / "digital_estimator_row.json", row)
            rows.append(
                dict(
                    case=case,
                    statistical_share_exact=[numerator, denominator],
                    statistical_allowance_dollars_exact=[
                        allowance.numerator,
                        allowance.denominator,
                    ],
                    remaining_deterministic_headroom_dollars_exact=[
                        (Fraction(1, 100) - allowance).numerator,
                        (Fraction(1, 100) - allowance).denominator,
                    ],
                    controlled_G_calls=schedule["controlled_grover_calls"],
                    qpe_bits=schedule["qpe_bits"],
                    missing_rotation_certificates=missing,
                    full_logical_T_count=row["full_T_count"],
                    conditional_logical_work_smaller=(
                        row["full_T_count"] is not None and row["full_T_count"] < base_T
                    ),
                    source_compatible_digital_estimator_certified=not missing,
                    complete_price_feasible=False,
                    open_obligations=complete["assessment"]["open_obligations"],
                    other_sampler_law_bounds_transferred=False,
                )
            )
    assert len(rows) == 6
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            candidates=rows,
            full_price_feasible_rows=0,
            adopted_statistical_share_exact=[9, 20],
            accepted_source_or_allocation_changed=False,
            unsupported_bias_interpolation_or_quantile_law_transfer=False,
            financial_prices_or_gate_replays=0,
            new_pytest_cases=0,
            next_required_certificate=(
                "Complete exact-source continuous-price bias, especially "
                "all-date barrier/native-path error"
            ),
            full_G2_closed=False,
            physical_execution_certificate=False,
        ),
    )
    manifest(output, protocol)
    print(
        "Six error-split rows retained; zero full-price feasible rows; original split unchanged",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
