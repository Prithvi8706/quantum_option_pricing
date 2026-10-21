"""Attach independently audited synthesis to separate B4 and B8 price ledgers."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
import shutil

from research.limitation_program_20261001.complete_price_ledger import assess
from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    BASELINE,
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)
from research.limitation_program_20261001.progress import ROOT


IQFT = PROGRAM / "E02_IQFT_run001"
IQFT_AUDIT = PROGRAM / "E02_IQFT_audit_run001"
SCHEDULE = PROGRAM / "E07_schedule_run001"
SUPPORT = PROGRAM / "E03_support_run001"


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    assert read(IQFT_AUDIT / "summary.json")["passed"]
    output.mkdir()
    frozen = {}
    for directory in (IQFT, IQFT_AUDIT, SCHEDULE):
        receipt = read(directory / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = digest(directory / "manifest.json")
    for name in ("experiment_complete_price_ledger.py", "complete_price_ledger.py"):
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = digest(path)
        shutil.copy2(path, output / name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        item="E07 complete-price reconciliation after audited logical IQFT synthesis",
        before_ledger_reconciliation=True,
        cases=["B4x12", "B8x52"],
        epsilon_dollars_exact=[1, 100],
        statistical_allowance_exact=[9, 2000],
        same_complete_failure_allocation=True,
        financial_or_quantum_gate_replays=0,
        new_pytest_cases=0,
        closure_rule=(
            "Only attach the certified synthesis term; every continuous "
            "law/tail/arithmetic/physical bound stays null until its own full-price proof"
        ),
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    original = read(SCHEDULE / "complete_price_ledger.json")
    summaries = []
    for case in protocol["cases"]:
        ledger = deepcopy(original)
        ledger["task"] = case + " original monitored arithmetic-basket knock-out call"
        current = BASELINE / case / "min-depth"
        for field, file in (
            ("target", "target.json"),
            ("source", "source.json"),
            ("capped_schedule", "schedule_capped.json"),
        ):
            ledger["source"][field] = relative(current / file)
            ledger["source"][field + "_sha256"] = digest(current / file)
        proof = read(SUPPORT / (case + "_certificate.json"))
        ledger["support"].update(
            certificate=relative(SUPPORT / (case + "_certificate.json")),
            native_payoff_lower=proof["payoff_raw_bounds"][0],
            native_payoff_upper=proof["payoff_raw_bounds"][1],
        )
        row_path = IQFT / case / "synthesized_estimator_ledger.json"
        row = read(row_path)
        assert row["case"] == case
        assert row["binding"]["hashes"]["target.json"] == ledger["source"]["target_sha256"]
        assert row["binding"]["hashes"]["source.json"] == ledger["source"]["source_sha256"]
        assert row["binding"]["payoff_raw_bounds"] == proof["payoff_raw_bounds"]
        assert row["statistical_error_dollars_exact"] == ledger["dollar_terms"][-1]["bound"]
        synthesis = next(
            term for term in ledger["failure_terms"] if term["name"] == "QPE_rotation_synthesis"
        )
        synthesis.update(
            bound=row["synthesis_total_observation_perturbation_upper_exact"],
            certificate=relative(IQFT_AUDIT / "summary.json"),
            source=relative(row_path),
            reason=(
                "Independent exact-target gate-string audit and telescoped "
                "whole-IQFT observation perturbation bound"
            ),
        )
        estimator = next(
            term for term in ledger["failure_terms"] if term["name"] == "ideal_estimator"
        )
        assert estimator["bound"] == row["ideal_failure_upper_exact"]
        combined = Fraction(*estimator["bound"]) + Fraction(*synthesis["bound"])
        confidence = 1 - combined
        ledger.update(
            source_compatible_logical_estimator=relative(row_path),
            source_compatible_logical_estimator_sha256=digest(row_path),
            independent_IQFT_audit=relative(IQFT_AUDIT / "summary.json"),
            noiseless_digital_mean_confidence_lower_exact=[
                confidence.numerator,
                confidence.denominator,
            ],
            physical_execution_assumed_ideal_for_digital_certificate=True,
            all_input_error_to_original_continuous_price_certified=False,
        )
        ledger["assessment"] = assess(ledger)
        assert not ledger["assessment"]["complete_price_certified"]
        assert ledger["assessment"]["open_obligations"] == [
            "finite_input_law_and_joint_Box_Muller",
            "clipped_log_tail",
            "native_arithmetic_and_polynomial",
            "physical_execution",
        ]
        save(output / (case + "_complete_price_ledger.json"), ledger)
        summaries.append(
            dict(
                case=case,
                known_failure_upper=float(combined),
                noiseless_digital_mean_confidence_lower=float(confidence),
                remaining_dollar_headroom_exact=[11, 2000],
                open_obligations=ledger["assessment"]["open_obligations"],
                complete_price_certified=False,
            )
        )
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            cases=summaries,
            synthesis_obligation_resolved_at_logical_level=True,
            financial_or_quantum_gate_replays=0,
            new_pytest_cases=0,
            physical_runtime_certified=False,
            continuous_financial_price_certified=False,
        ),
    )
    manifest(output, protocol)
    print("Two rational complete-price ledgers reconciled; four obligations remain", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
