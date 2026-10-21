"""Three fixed estimator families under the current span64 financial contract.

IQAE/MIQAE rows are rigorous enclosures of general query upper-bound formulas.
They do not prove lower bounds on actual controller costs, delivery or advantage.
"""

from fractions import Fraction
from math import ceil
from pathlib import Path

import mpmath as mp

from research.limitation_program_20261001 import audit_barrier_band as audit


ROOT = audit.ROOT
RESULTS = audit.RESULTS
SPAN = 64
ERROR = Fraction(9, 2000)
FAILURE = Fraction(3, 1000)
AMPLITUDE_ERROR = ERROR / SPAN
FAMILIES = ("canonical-bounded-QAE", "original-IQAE", "modified-IQAE")
PRIMARY_SOURCES = {
    "original-IQAE": {
        "url": "https://arxiv.org/html/1912.05559v3",
        "location": "Theorem1 equation9 and its Q-query convention in SectionII",
        "formula": "50/epsilon * ln((2/alpha)*log2(pi/(4*epsilon)))",
        "query_unit": "Grover Q applications; preparation/measurement/reset separately required",
        "native_controller_transfer_status": (
            "Repeated-look/native confidence interface requires audit"
        ),
    },
    "modified-IQAE": {
        "url": "https://arxiv.org/html/2208.14612v4",
        "location": "Lemma3.7 equations3.19-3.31, retaining exact coefficient",
        "formula": "3*pi/(8*epsilon*sin(pi/21)^2*sin(8*pi/21)^2) * ln(sqrt(27)/alpha)",
        "query_unit": "Proof sums k_i*N_i, i.e. Grover Q applications",
        "printed_query_wording_ambiguous": True,
        "native_controller_transfer_status": (
            "Per-round/per-look confidence spending and preparation counts required"
        ),
    },
}


def formula_intervals(error=ERROR, failure=FAILURE, span=SPAN):
    if isinstance(error, (float, bool)) or isinstance(failure, (float, bool)):
        raise ValueError("Exact financial error/failure required")
    error, failure = Fraction(error), Fraction(failure)
    if error != ERROR or failure != FAILURE or type(span) is not int or span != SPAN:
        raise ValueError("Fixed current span64/.0045/.003 contract required")
    old = mp.iv.dps
    mp.iv.dps = 110
    try:
        epsilon, alpha = audit.iv(error / span), audit.iv(failure)
        original = (
            50
            / epsilon
            * mp.iv.log((2 / alpha) * mp.iv.log(mp.iv.pi / (4 * epsilon)) / mp.iv.log(2))
        )
        constant = 1 / (mp.iv.sin(mp.iv.pi / 21) ** 2 * mp.iv.sin(8 * mp.iv.pi / 21) ** 2)
        modified = 3 * mp.iv.pi * constant / (8 * epsilon) * mp.iv.log(mp.iv.sqrt(27) / alpha)
        return {
            "original-IQAE": audit.endpoints(original),
            "modified-IQAE": audit.endpoints(modified),
        }
    finally:
        mp.iv.dps = old


def screen(root=ROOT):
    root = Path(root).resolve()
    base = root / "results/limitation_program_20261001"
    for name in (
        "E07_schedule_run001",
        "E02_financial_run002",
        "E02_IQFT_run001",
        "E02_IQFT_audit_run001",
    ):
        directory = base / name
        audit.verify_manifest(root, directory)
        audit.require(
            audit.read(directory / "summary.json")["passed"] is True,
            "Passed financial prerequisite required",
        )
    schedule = audit.read(base / "E07_schedule_run001/schedule.json")
    audit.require(
        schedule["normalization_span_dollars"] == SPAN
        and audit.exact(schedule["statistical_error_dollars_exact"]) == ERROR
        and schedule["requested_failure_exact"] == [3, 1000]
        and schedule["controlled_grover_calls"] == 983025,
        "Current canonical financial schedule changed",
    )
    canonical_path = base / "E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json"
    canonical = audit.read(canonical_path)
    wrapper_path = base / "E02_financial_run002/B4x12/iterate.json"
    wrapper = audit.read(wrapper_path)
    audit.require(
        canonical["normalization_span_dollars"] == SPAN
        and canonical["fresh_preparations"] == 15
        and canonical["wrapper_sha256"] == audit.sha(wrapper_path),
        "Canonical source recipe mismatch",
    )
    rows = [
        {
            "family": FAMILIES[0],
            "status": "retained_same-output_ideal_digital_baseline",
            "grover_calls": 983025,
            "fresh_uniform_preparations": 15,
            "longest_single_shot_Q_chain": 65535,
            "logical_T_count": canonical["full_T_count"],
            "logical_serial_T_depth": canonical["full_T_depth"],
            "source_matched_synthesized_recipe": str(canonical_path),
            "recipe_sha256": audit.sha(canonical_path),
            "physical_readout_reset_feedback_seconds": None,
            "full_continuous_price_certificate": False,
        }
    ]
    for family, interval in formula_intervals().items():
        rows.append(
            {
                "family": family,
                "status": "general_query_upper_bound_screen_only",
                "primary_source": PRIMARY_SOURCES[family],
                "general_Q_bound_formula_interval_exact": list(map(audit.pair, interval)),
                "rigorous_Q_bound_formula_ceiling": ceil(interval[1]),
                "general_Q_bound_formula_lower_endpoint_above_canonical_Q_count": interval[0]
                > 983025,
                "actual_Q_count_lower_bound_claimed": False,
                "actual_financial_cost_lower_bound_claimed": False,
                "fresh_preparation_count": None,
                "terminal_predicate_observations": None,
                "adaptive_rounds": None,
                "longest_single_shot_Q_chain": None,
                "financial_forward_calls": None,
                "financial_literal_inverse_calls": None,
                "selector_forward_calls": None,
                "selector_literal_inverse_calls": None,
                "logical_T_count": None,
                "logical_serial_T_depth": None,
                "physical_readout_reset_feedback_seconds": None,
                "controller_coverage_and_delivery_audited": False,
                "eligible_for_financial_promotion": False,
            "missing_proof": (
                "Explicit executable finite controller, all adaptive looks and delivery, "
                "shot preparation/readout/reset ledger"
            ),
            }
        )
    return {
        "passed": True,
        "families": rows,
        "family_count": 3,
        "normalization": "p=E[original already-discounted native Y]/64",
        "span_dollars": SPAN,
        "statistical_error_dollars_exact": audit.pair(ERROR),
        "amplitude_error_exact": audit.pair(AMPLITUDE_ERROR),
        "ideal_failure_exact": audit.pair(FAILURE),
        "prior_residual_span256_counts_transferred": False,
        "wrapper_binding": {
            "path": str(wrapper_path),
            "sha256": audit.sha(wrapper_path),
            "sequence": wrapper["sequence"],
            "resource_qubits": wrapper["resources"]["logical_qubits"],
        },
        "IQAE_terminal_predicate_requirement": (
            "For each shot, unchanged uniform H preparation, pinned-active original Grover"
            " hierarchy Q^k, then original F+selector to measure its good flag, then literal"
            " inverse selector+F cleanup. Preparations and terminal marking add one financial/"
            "selector forward and inverse per shot. Readout, reset and controller feedback"
            " are counted separately, without invented durations."
        ),
        "same_output_conditional_operation_pricing_allowed": True,
        "physical_execution_or_full_G2_certified": False,
        "general_bound_screen_is_not_controller_impossibility": True,
        "new_financial_samples_or_gate_replays": 0,
        "next_finite_controller_scope": {
            "maximum_settings": 8,
            "maximum_exact_toy_laws": 2,
            "families": ["original-IQAE-adapter", "modified-IQAE-adapter"],
            "settings": [
                {"family": name, "first_batch_shots": shots}
                for name in ("original-IQAE-adapter", "modified-IQAE-adapter")
                for shots in (16, 32, 64, 128)
            ],
            "stop_rule": (
                "Eight fixed settings/two exact toy laws only; incomplete/censored rows "
                "are not certified financial improvements"
            ),
        },
    }
