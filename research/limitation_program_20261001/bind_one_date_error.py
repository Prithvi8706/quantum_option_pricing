"""Join exactly C06 delta20 and C07 B4/date1, retaining full-price unknowns.

The bounded object is the payoff difference restricted to a one-date decision
disagreement event. It is not a full-path price-error or Gaussian-law claim.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from research.limitation_program_20261001 import audit_barrier_band as audit
from research.limitation_program_20261001 import barrier_band_certificate as barrier


ROOT = audit.ROOT
RESULTS = audit.RESULTS
SELECTED_CUTOFF_BITS = 20
ETA_CLAIM = "delta2minus20_B4_date1_basket"
BAD_CLAIM = "delta2minus20_B4_date1_bad_event"
COUPLING_ID = "C06_q32_f40_shared_uniform_delta2minus20"
MEASURE = "continuous-underlying-uniform-coupling"
EVENT_PROOF = (
    "Let D1 be the event that the original continuous and digital strict"
    " date1 basket<H decisions differ. Let E1 be any of the first three radial"
    " uniforms below delta=2^-20. C06 proves |B_d-B_c|<=eta on E1 complement"
    " including native exp and clipping. Therefore D1 intersect E1 complement"
    " is contained in the unconditional continuous event |B_c-140|<=eta."
    " Both ORIGINAL fully monitored discounted payoffs Yc and Yd lie in [0,40];"
    " hence E[|Yc-Yd|1{D1 intersect E1 complement}]<=40*P(band), and"
    " E[|Yc-Yd|1{D1 intersect E1}]<=40*P(E1)<=40*3*delta. These give only"
    " the contribution on D1. The contribution on D1 complement remains"
    " unbounded here; in particular later-date switches and smooth Asian"
    " payoff discrepancy are unresolved. A whole-B4 radial bad-event tail"
    " bound40*30*delta is listed separately and is not added to the date1"
    " bad-event term. No good-event conditioned Gaussian law is asserted."
)


def validate_selected(certificate):
    audit.require(
        certificate["uniform_bits"] == 32
        and certificate["fraction_bits"] == 40
        and certificate["native_width"] == 72,
        "Actual q32/f40/72-bit coupling required",
    )
    rows = [x for x in certificate["candidates"] if x["cutoff_bits"] == SELECTED_CUTOFF_BITS]
    audit.require(len(rows) == 1, "Exactly one declared delta20 source row required")
    row = rows[0]
    delta = Fraction(1, 1 << SELECTED_CUTOFF_BITS)
    audit.require(
        audit.exact(row["delta_exact"]) == delta and row["coupling_id"] == COUPLING_ID,
        "Cutoff or coupling changed",
    )
    date = row["B4_date1"]
    audit.require(
        date["date"] == 1
        and date["observation_time_exact"] == [1, 12]
        and date["assets"] == 4
        and date["Gaussian_pairs_used"] == 3,
        "Date1 requires five shared-pair normals from three pairs",
    )
    audit.require(
        date["clipping_inactive_on_good_event"] is True
        and date["exp_final_shift_signed_overflow_excluded"] is True
        and date["unchanged_exp_templates_certified_by_independent_E03_audit"] is True
        and date["first_asset_template_bound_applies_to_all_four_assets"] is True,
        "Actual native exp/clipping inclusion required",
    )
    scopes = date["all_four_asset_date1_scopes"]
    audit.require([x["asset"] for x in scopes] == [0, 1, 2, 3], "All four date1 assets required")
    normals = certificate["source_bindings"]["B4x12"]["normal_values"]
    audit.require(
        [x["normal_values"] for x in scopes] == [[normals[0], normals[1 + i]] for i in range(4)],
        "Original common/idiosyncratic binding changed",
    )
    audit.require(
        certificate["source_bindings"]["B4x12"]["pair_count"] == 30
        and certificate["source_bindings"]["B4x12"]["scalar_count"] == 60,
        "Whole B4 must retain30 independent pairs, not60 independent finite normals",
    )
    eta, bad = certificate["claims"][ETA_CLAIM], certificate["claims"][BAD_CLAIM]
    for claim, kind in ((eta, "basket-absolute-error"), (bad, "bad-event-probability")):
        audit.require(
            claim["kind"] == kind
            and claim["scope"] == {"case": "B4x12", "date": 1}
            and claim["coupling_id"] == COUPLING_ID
            and claim["measure"] == MEASURE
            and claim["proved"] is True,
            "Claim kind/scope/coupling/measure changed",
        )
    audit.require(
        eta.get("native_exp_and_clipping_included") is True
        and eta.get("event") == "First three radial uniforms are at least delta",
        "Basket claim must cover the same native good domain",
    )
    audit.require(
        audit.exact(eta["upper_exact"]) == audit.exact(date["basket_discrepancy_dollars_exact"])
        and 0 <= audit.exact(eta["upper_exact"]) < 140,
        "Basket eta does not match the selected certified radius",
    )
    audit.require(
        audit.exact(bad["upper_exact"]) == 3 * delta,
        "Date1 bad event must be3*delta, not full30*delta",
    )
    audit.require(
        audit.exact(row["tail_probability_union_upper_exact"]["B4_all30_pairs"]) == 30 * delta,
        "Whole-B4 bad probability changed",
    )
    audit.require(
        audit.exact(
            row["tail_payoff_difference_dollars_upper_exact"]["B4_all30_pairs_bad_event_only"]
        )
        == 40 * 30 * delta,
        "Whole-B4 tail dollars changed",
    )
    return row, eta, bad


def pointer(path, claim=None):
    result = {"path": str(path.resolve()), "sha256": audit.sha(path)}
    if claim is not None:
        result["claim"] = claim
    return result


def bind(root=ROOT):
    root = Path(root).resolve()
    base = root / "results/limitation_program_20261001"
    pair_dir = base / "C06_pair_run001"
    barrier_dir = base / "C07_barrier_run002"
    audit_dir = base / "C07_barrier_audit_run001"
    for directory in (pair_dir, barrier_dir, audit_dir):
        audit.verify_manifest(root, directory)
        audit.require(
            audit.read(directory / "summary.json")["passed"] is True,
            "Passed source receipt required",
        )
    prior = audit.read(audit_dir / "audit.json")
    audit.require(
        prior["passed"] is True
        and prior["source_contract"]["common_log_variance_exact"] == [3, 1000],
        "Independent C07 audit required",
    )
    artifact_path = pair_dir / "certificate.json"
    source = audit.read(artifact_path)
    row, eta, bad = validate_selected(source)
    builder = root / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    builder_sha = audit.sha(builder)
    pair_manifest = audit.read(pair_dir / "manifest.json")
    audit.require(
        pair_manifest["frozen_inputs"][builder.relative_to(root).as_posix()] == builder_sha
        and prior["source_contract"]["builder_sha256"] == builder_sha,
        "C06/C07 do not bind the identical original builder",
    )
    target = source["source_bindings"]["B4x12"]
    actual_target = audit.local(root, target["target"])
    audit.require(
        audit.sha(actual_target) == target["target_sha256"], "Actual accepted target changed"
    )
    audit.require(
        audit.read(barrier_dir / "protocol.json")["frozen_inputs"][target["target"]]
        == target["target_sha256"],
        "C07 model bound to another financial target",
    )
    support = source["payoff_support_bindings"]["B4x12"]
    support_path = audit.local(root, support["certificate"])
    support_audit_path = audit.local(root, support["independent_audit"])
    audit.require(
        audit.sha(support_path) == support["certificate_sha256"]
        and audit.sha(support_audit_path) == support["independent_audit_sha256"]
        and audit.read(support_audit_path)["passed"] is True,
        "Independently audited payoff support required",
    )
    audit.require(
        support["payoff_difference_on_bad_event_upper_dollars_exact"] == [40, 1],
        "Original discounted payoff difference cap changed",
    )
    native_support = audit.read(support_path)
    lo, hi = native_support["payoff_raw_bounds"]
    audit.require(
        0 <= lo <= hi < 40 * (1 << 40), "Native fully monitored payoff not below40 dollars"
    )
    result = barrier.certify_one_date(
        "B4x12",
        1,
        eta_proof=pointer(artifact_path, ETA_CLAIM),
        bad_probability_proof=pointer(artifact_path, BAD_CLAIM),
    )
    bounds = result["proved_discrepancy_band_bounds"]
    reference = audit.independent_band_enclosure(eta["upper_exact"], 140, Fraction(3, 1000))
    for kind in ("density", "centered_interval_maximum"):
        audit.enclose_claim(
            bounds[kind]["interval_exact"], reference[kind], "Bound actual eta: " + kind
        )
    cap, bad_prob = Fraction(40), audit.exact(bad["upper_exact"])
    contributions = {}
    for kind in ("density", "centered_interval_maximum"):
        probability = audit.exact(bounds[kind]["probability_upper_exact"])
        contributions[kind] = {
            "one_date_good_event_band_probability_upper_exact": audit.pair(probability),
            "one_date_good_event_payoff_difference_contribution_dollars_upper_exact": audit.pair(
                cap * probability
            ),
            "one_date_decision_disagreement_probability_upper_exact": audit.pair(
                min(Fraction(1), probability + bad_prob)
            ),
            "one_date_disagreement_event_only_payoff_difference_dollars_upper_exact": audit.pair(
                cap * min(Fraction(1), probability + bad_prob)
            ),
            "is_full_price_error_bound": False,
        }
    return {
        "format": "C06-delta20-C07-one-date-error-binding-v1",
        "passed": True,
        "scope": {"case": "B4x12", "date": 1, "observation_time_exact": [1, 12]},
        "selected_cutoff_bits": SELECTED_CUTOFF_BITS,
        "selected_eta_values": 1,
        "bound_forms": ["density", "centered_interval_maximum"],
        "coupling_id": COUPLING_ID,
        "measure": MEASURE,
        "domain": {
            "good_event": eta["event"],
            "delta_exact": row["delta_exact"],
            "q32_grid_aligned_cutoff": True,
            "midpoint_at_least_delta_on_good_event": True,
            "used_joint_pairs": 3,
            "used_normal_scalars": 5,
            "finite_normal_outputs_assumed_independent": False,
            "native_exp_and_clipping_included": True,
        },
        "eta_basket_dollars_exact": eta["upper_exact"],
        "date1_bad_event_probability_upper_exact": bad["upper_exact"],
        "whole_B4_all30_pairs_bad_event_probability_upper_exact": audit.pair(Fraction(30, 1 << 20)),
        "date1_bad_event_tail_dollars_upper_exact": audit.pair(cap * bad_prob),
        "whole_B4_all30_pairs_bad_event_tail_dollars_upper_exact": audit.pair(cap * 30 / (1 << 20)),
        "date1_and_whole_B4_tails_are_separate_alternatives_not_added": True,
        "payoff_difference_cap_dollars_exact": [40, 1],
        "cap_proof": (
            "Original continuous survival has everybasket<140, hence the Asian spot average<140,"
            " positive strike100 payoff<40 and discount<1. Independently audited actual digital"
            " fully monitored discounted payoff is nonnegative<40. Thus |Yc-Yd|<=40."
        ),
        "proof": EVENT_PROOF,
        "one_date_barrier_contributions": contributions,
        "barrier_api_certificate": result,
        "independent_numeric_validation": reference,
        "bindings": {
            "C06_certificate": pointer(artifact_path),
            "eta_claim": pointer(artifact_path, ETA_CLAIM),
            "bad_event_claim": pointer(artifact_path, BAD_CLAIM),
            "C07_certificate": pointer(barrier_dir / "B4_date1_certificate.json"),
            "C07_independent_audit": pointer(audit_dir / "audit.json"),
            "original_builder": pointer(builder),
            "accepted_target": pointer(actual_target),
            "digital_support_certificate": pointer(support_path),
            "digital_support_independent_audit": pointer(support_audit_path),
        },
        "C06_independent_audit_adoption": {"status": "required_before_adoption", "pointer": None},
        "adopted_as_complete_financial_error_certificate": False,
        "discounted_smooth_full_Asian_payoff_zeta": None,
        "any_contractual_date_band_probability": None,
        "full_path_native_exp_and_clipping_discrepancy": None,
        "complete_price_error_dollars_upper_exact": None,
        "full_G2_closed": False,
        "second_discount_applied": False,
        "new_financial_price_samples": 0,
        "new_financial_gate_replays": 0,
        "eta_grid_or_adaptive_radius_search": False,
    }
