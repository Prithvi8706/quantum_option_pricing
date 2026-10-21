"""Preregistered three-law diagnostic and all-look finance admission; no finance draws."""
import argparse
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

PROCESS_STARTED = time.monotonic()
PROCESS_CPU_STARTED = time.process_time()

import numpy as np

from anytime_eb import (DyadicCS, Statistics, context, empirical_bernstein_radius,
                       exp_interval, fraction_interval, interval, look_failure)

ROOT = Path(__file__).resolve().parents[4]
SOURCE = Path(__file__).resolve().parent
DOCS = ROOT / "docs/limitation_program_20261001/continuation_20261004/E12"
PROTOCOL = DOCS / "PROTOCOL.json"


def digest(path):
    data = path.read_bytes()
    return dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


def relative(path):
    try:
        return str(path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path.resolve())


def fresh_out(name):
    out = Path(name).resolve()
    allowed = (ROOT / "results/limitation_program_20261001").resolve()
    if out.parent != allowed or not out.name.startswith("E12_continuation_20261004_"):
        raise ValueError("Fresh dedicated E12 result directory required")
    return out


def write(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def verify_inputs(out):
    inputs = json.loads((out / "frozen_inputs.json").read_text(encoding="utf-8"))
    mismatches = []
    for name, expected in inputs.items():
        path = Path(name) if Path(name).is_absolute() else ROOT / name
        if digest(path) != expected:
            mismatches.append(name)
    if mismatches:
        raise ValueError("Frozen input changed: " + repr(mismatches))
    return len(inputs)


def prepare(out):
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol["toy_corpus"]["laws"] != ["1/2", "1/256", "1/65536"] or protocol["finance_admission"]["finance_acquisitions_authorized"] != 0:
        raise ValueError("Frozen corpus/finance route guard")
    paths = [ROOT / name for name in protocol["input_paths"]]
    paths.extend([PROTOCOL, DOCS / "THEOREM_AND_SCOPE.md",
                  DOCS / "sources/PRIMARY_SOURCE.json", DOCS / "sources/maurer_pontil_colt2009.pdf"])
    paths.extend(sorted(SOURCE.glob("*.py")))
    paths.append(Path(sys.executable).resolve())
    paths.append(Path(np.__file__).resolve())
    paths.extend(sorted((Path(np.__file__).parent / "random").glob("*.pyd")))
    frozen = {relative(p):digest(p) for p in paths}
    out.mkdir(exist_ok=False)
    with (out / "protocol.json").open("xb") as stream:
        stream.write(PROTOCOL.read_bytes())
    write(out / "frozen_inputs.json", frozen)
    checks = verify_inputs(out)
    write(out / "PREPARED.json", dict(status="PREPARED", science_executed=False,
        source_protocol_sha256=digest(PROTOCOL)["sha256"], frozen_checks=checks,
        python_version=sys.version, numpy_version=np.__version__,
        stopping_rule_revisions=0, finance_acquisitions=0,
        runtime_pin_scope="Selected Python launcher, NumPy package init and NumPy random binaries; not complete runtime closure or financial evaluation provenance."))
    print(json.dumps(dict(status="PREPARED", output=relative(out), frozen_checks=checks)))


def finance_admission():
    alpha = Fraction(1, 2000)
    target = Decimal("0.19448064336973883")
    archive = json.loads((ROOT / "results/controlled_residual_feasibility/parity_iid_v1/summaries.json").read_text(), parse_float=Decimal)
    row = next(r for r in archive if r["case"] == "C4" and r["strike"] == 6)
    if row["second_moment_upper"] != target or row["samples"] != 1048576 or row["inner_samples"] != 16:
        raise ValueError("Unchanged C4 finance target/cap/inner guard")
    exp_lo, exp_hi = exp_interval(Fraction(-3, 100))
    floor_ctx, ceil_ctx = context(ROUND_FLOOR), context(ROUND_CEILING)
    width_lo = floor_ctx.multiply(Decimal(10000), exp_lo)
    width_hi = ceil_ctx.multiply(Decimal(10000), exp_hi)
    floors = []
    for exponent in range(1, 21):
        radius_lo, radius_hi = empirical_bernstein_radius(Fraction(0), 2**exponent,
                                                        Fraction(1), look_failure(alpha, exponent))
        # A nonnegative mean and nonnegative variance cannot improve this floor.
        # Clipping to known support must also be charged in the lower envelope.
        lo = min(width_lo, floor_ctx.multiply(width_lo, radius_lo))
        hi = min(width_hi, ceil_ctx.multiply(width_hi, radius_hi))
        floors.append(dict(exponent=exponent, samples=2**exponent,
                           per_look_failure=str(look_failure(alpha, exponent)),
                           zero_observation_floor_lower=str(lo),
                           zero_observation_floor_upper=str(hi)))
    best = min(floors, key=lambda r:Decimal(r["zero_observation_floor_lower"]))
    minimum_lower = Decimal(best["zero_observation_floor_lower"])
    rejected = minimum_lower > target
    if not rejected:
        raise AssertionError("Unexpected finance floor gate; this version cannot launch finance")
    return dict(schema="e12-finance-admission-v1", case="C4", compound_strike=6,
                status="FIXED_STOPPING_RULE_REJECTED_BEFORE_ACQUISITION",
                target_dollars_squared=str(target), support_squared_lower=str(width_lo),
                support_squared_upper=str(width_hi), all_20_look_floors=floors,
                minimum_all_look_lower_floor=str(minimum_lower), best_look=best["samples"],
                rejection_certified_by_outward_lower=True, finance_draws=0,
                reserve_for_other_moment_stream="1/2000",
                complete_acquisition_plus_estimation_latency=None, matched_complete_latency=None,
                scope="Rejects this unchanged-target rule only. Sharper sequences and larger-moment versus complete-latency tradeoffs remain unresolved.")


def diagnostic_trial(law_index, probability, replicate, protocol):
    alpha = Fraction(protocol["allocation"]["per_stream_failure"])
    target = Fraction(protocol["toy_corpus"]["target_upper"])
    cap = protocol["toy_corpus"]["sample_cap"]
    cap_exponent = cap.bit_length()-1
    seed = np.random.SeedSequence([protocol["toy_corpus"]["root_seed"], law_index, replicate])
    rng = np.random.Generator(np.random.PCG64(seed))
    blocks, previous_n, cumulative = [], 0, 0
    # Complete paired diagnostic trajectory; actual sequential sampler latency is
    # deliberately not inferred from this compressed binomial simulation.
    for exponent in range(1, cap_exponent+1):
        n = 2**exponent
        increment = int(rng.binomial(n-previous_n, float(probability)))
        cumulative += increment
        blocks.append(dict(n=n, block_size=n-previous_n, successes=increment,
                           cumulative_successes=cumulative))
        previous_n = n
    cs = DyadicCS(alpha, cap_exponent)
    for block in blocks:
        cs.update(Statistics.bernoulli(block["n"], block["cumulative_successes"]))
        if cs.reaches(target) or cs.empty:
            break
    decision = cs.result(target)
    terminal = Statistics.bernoulli(cap, cumulative)
    low, high, radius = interval(terminal, alpha)
    fixed_ready = high <= fraction_interval(target)[0]
    fixed = dict(status="TARGET_CERTIFIED" if fixed_ready else "SUPPORT_FALLBACK",
                 observations=cap, certificate_upper=str(high) if fixed_ready else "1",
                 lower=str(low), upper=str(high), radius_upper=str(radius[1]),
                 allocated_failure=str(alpha))
    # True p enters only diagnostics after both controllers made their decisions.
    before_stop_coverage = all(Fraction(Decimal(look["retained_lower"])) <= probability <=
                               Fraction(Decimal(look["retained_upper"])) for look in cs.looks)
    stopped_coverage = (probability <= Fraction(Decimal(decision["certificate_upper"])))
    fixed_coverage = Fraction(low) <= probability <= Fraction(high)
    return dict(law=str(probability), replicate=replicate,
                seed_entropy=[protocol["toy_corpus"]["root_seed"], law_index, replicate],
                paired_full_trajectory=blocks, cs_looks_before_stop=cs.looks,
                cs=decision, fixed_n=fixed,
                diagnostic_simultaneous_coverage_before_stop=before_stop_coverage,
                diagnostic_delivered_upper_coverage=stopped_coverage,
                diagnostic_fixed_interval_coverage=fixed_coverage,
                cost_unit="Logical Bernoulli observations; synthetic compressed simulation, no measured acquisition latency")


def run(out):
    if not (out / "PREPARED.json").exists() or (out / "STARTED.json").exists():
        raise ValueError("Exactly one run of a fresh prepared directory is required")
    input_checks = verify_inputs(out)
    protocol = json.loads((out / "protocol.json").read_text(encoding="utf-8"))
    if digest(out / "protocol.json") != digest(PROTOCOL):
        raise ValueError("Prepared protocol copy differs")
    started, cpu_start = PROCESS_STARTED, PROCESS_CPU_STARTED
    write(out / "STARTED.json", dict(status="STARTED", frozen_checks=input_checks,
                                     protocol_sha256=digest(PROTOCOL)["sha256"]))
    def guard():
        if time.process_time()-cpu_start > protocol["budgets"]["cpu_seconds"] or time.monotonic()-started > protocol["budgets"]["wall_seconds"]:
            raise TimeoutError("Preregistered scientific/admin execution budget exhausted")
    try:
        admission = finance_admission()
        write(out / "finance_admission.json", admission)
        guard()
        summaries, total_attempts = [], 0
        with (out / "toy_attempts.jsonl").open("x", encoding="utf-8") as stream:
            for law_index, literal in enumerate(protocol["toy_corpus"]["laws"]):
                probability = Fraction(literal)
                rows = []
                for replicate in range(protocol["toy_corpus"]["replicates_per_law"]):
                    guard()
                    row = diagnostic_trial(law_index, probability, replicate, protocol)
                    rows.append(row)
                    stream.write(json.dumps(row)+"\n")
                    stream.flush()
                    total_attempts += 1
                n = len(rows)
                samples = [r["cs"]["observations"] for r in rows]
                summaries.append(dict(law=literal, attempts=n,
                    cs_target_certified=sum(r["cs"]["status"] == "TARGET_CERTIFIED" for r in rows),
                    cs_target_failures_retained=sum(r["cs"]["status"] != "TARGET_CERTIFIED" for r in rows),
                    cs_empty_intersections=sum(r["cs"]["empty"] for r in rows),
                    cs_observation_total=sum(samples), cs_observation_mean=sum(samples)/n,
                    cs_observation_median=float(np.median(samples)),
                    cs_observation_min=min(samples), cs_observation_max=max(samples),
                    cs_confidence_evaluations=sum(len(r["cs_looks_before_stop"]) for r in rows),
                    fixed_n_target_certified=sum(r["fixed_n"]["status"] == "TARGET_CERTIFIED" for r in rows),
                    fixed_n_observation_total=protocol["toy_corpus"]["sample_cap"]*n,
                    fixed_n_observations_each=protocol["toy_corpus"]["sample_cap"],
                    fixed_n_confidence_evaluations=n,
                    diagnostic_before_stop_coverage_failures=sum(not r["diagnostic_simultaneous_coverage_before_stop"] for r in rows),
                    diagnostic_delivered_upper_failures=sum(not r["diagnostic_delivered_upper_coverage"] for r in rows),
                    diagnostic_fixed_interval_failures=sum(not r["diagnostic_fixed_interval_coverage"] for r in rows)))
        if total_attempts != 384 or len(summaries) != 3:
            raise AssertionError("Declared corpus incomplete")
        guard()
        certificate = dict(schema="e12-dyadic-eb-component-certificate-v1", component_completed=True,
            result="THEOREM_BACKED_IID_CS_IMPLEMENTED; FINANCE_FIXED_RULE_REJECTED",
            exact_failure_telescope_finite_20=str(Fraction(1, 2000)*Fraction(20, 21)),
            infinite_look_stream_failure="1/2000", per_price_two_stream_failure="1/1000",
            proof_location=relative(DOCS / "THEOREM_AND_SCOPE.md"),
            statistical_scope="Conditional on ideal iid outer groups, independently frozen training, disjoint fixed inner groups, deterministic support and exact observations. No empirical coverage claim substitutes for the theorem.",
            all_zero_first_toy_target_look=8192, finance_admission=admission["status"],
            finance_draws=0, quantum_gate_emissions=0, finance_fixture_credit=0,
            new_financial_replays=0, full_E12_completed=False, quantum_advantage=False,
            broad_item_status="PARTIAL: fixed bounded iid alternative finished with a negative finance-admission result",
            remaining_obligations=["A sharper sequence or explicit larger-moment tradeoff requires new preregistration.",
                "Finite finance sampling law and group evaluation error remain separate.",
                "Complete acquisition-plus-estimation comparator latency remains unresolved; no promotion.",
                "General conditional-mean Howard sequence is not implemented here."])
        write(out / "certificate.json", certificate)
        write(out / "comparison.json", dict(schema="e12-three-law-comparison-v1", toy_laws=summaries,
            finance_admission=admission,
            complete_acquisition_plus_estimation_latency=None, matched_complete_latency=None,
            financial_promotion=False,
            scope="Observation counts are diagnostics for exact laws. Confidence arithmetic, policy training, source/inverse, confidence/readout and physical latency cannot be inferred from them."))
        final_checks = verify_inputs(out)
        artifact_bytes = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
        if artifact_bytes > protocol["budgets"]["artifact_bytes"]:
            raise MemoryError("Preregistered artifact cap exhausted")
        guard()
        receipt = dict(status="COMPONENT_COMPLETED_FINANCE_RULE_REJECTED", passed=True,
                       protocol_sha256=digest(PROTOCOL)["sha256"], attempts=total_attempts,
                       scientific_inputs_final_checks=final_checks,
                       finance_acquisitions=0, fixture_credit=0, financial_promotion=False,
                       artifact_bytes_before_receipt=artifact_bytes,
                       administrative_cpu_seconds=time.process_time()-cpu_start,
                       administrative_wall_seconds=time.monotonic()-started,
                       timer_scope="Starts before NumPy import, includes initial input verification; receipt subtotal ends before terminal manifest sealing. Final body guard also checks after sealing. Python startup/stdlib imports preceding this timer are unmeasured.",
                       runtime_pin_scope="Selected launcher/NumPy RNG inputs only; no complete runtime or financial-source closure claim.",
                       timings_not_matched_performance=True)
        write(out / "receipt.json", receipt)
        owned = {relative(p):digest(p) for p in sorted(out.rglob("*")) if p.is_file()}
        write(out / "manifest.json", dict(schema="e12-continuation-owned-and-input-manifest-v1",
              owned_files=owned, frozen_inputs=json.loads((out / "frozen_inputs.json").read_text()),
              manifest_self_excluded=True, component_passed=True, finance_rule_rejected=True))
        guard()
        if sum(p.stat().st_size for p in out.rglob("*") if p.is_file()) > protocol["budgets"]["artifact_bytes"]:
            raise MemoryError("Preregistered final artifact cap exhausted")
        print(json.dumps(receipt))
        print(json.dumps(summaries))
    except BaseException as error:
        write(out / "FAILED.json", dict(status="FAILED", component_completed=False,
              error=repr(error), traceback=traceback.format_exc(),
              partial_results_unapproved=True, finance_draws=0,
              administrative_cpu_seconds=time.process_time()-cpu_start,
              administrative_wall_seconds=time.monotonic()-started))
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["prepare", "run", "inspect"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = fresh_out(args.out)
    if args.mode == "prepare":
        prepare(out)
    elif args.mode == "run":
        run(out)
    else:
        count = verify_inputs(out)
        manifest = json.loads((out / "manifest.json").read_text())
        mismatches = []
        for name, expected in manifest["owned_files"].items():
            if digest(ROOT / name) != expected:
                mismatches.append(name)
        if mismatches or (out / "FAILED.json").exists():
            raise ValueError("Failed/changed run: " + repr(mismatches))
        print(json.dumps(dict(status="INSPECT_PASS", frozen_checks=count,
                              owned_checks=len(manifest["owned_files"]), mismatches=0)))


if __name__ == "__main__":
    main()
