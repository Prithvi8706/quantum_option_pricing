"""Fixed finite-oracle preflight, independent mpmath reference, no finance draw."""
import argparse
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time
import traceback

import mpmath as mp

from anytime_eb import (DyadicCS, Statistics, empirical_bernstein_radius,
                       exp_interval, fraction_interval, look_failure)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(function, exception):
    try:
        function()
    except exception:
        return
    raise AssertionError("Expected input refusal: " + repr(function))


def qmp(value):
    return mp.mpf(value.numerator) / value.denominator


def validation():
    checks = []
    # Pair-difference oracle from the paper, independent of producer sums/squares.
    corpus = ((Fraction(0), Fraction(1)),
              (Fraction(1, 7), Fraction(2, 7), Fraction(3, 7), Fraction(6, 7)),
              (Fraction(1, 3),) * 8,
              (Fraction(0),) * 16,
              (Fraction(1),) * 16)
    for values in corpus:
        stats = Statistics.observations(values)
        pairs = sum(((values[i]-values[j])**2 for i in range(len(values))
                     for j in range(i+1, len(values))), Fraction(0))
        oracle = pairs / (len(values)*(len(values)-1))
        require(stats.variance == oracle, "Pair-difference variance disagreement")
    checks.append(dict(name="five_exact_pair_difference_oracles", passed=True))

    for n in (2, 16, 1024, 65536):
        for k in (0, 1, n//2, n):
            stats = Statistics.bernoulli(n, k)
            require(stats.mean == Fraction(k, n), "Bernoulli mean")
            require(stats.variance == Fraction(k*(n-k), n*(n-1)), "Bernoulli variance")
    checks.append(dict(name="sixteen_bernoulli_count_oracles", passed=True))

    alpha = Fraction(1, 2000)
    spent = sum((look_failure(alpha, j) for j in range(1, 21)), Fraction(0))
    require(spent == alpha*Fraction(20, 21), "Failure allocation telescope")
    require(spent < alpha, "Finite looks overspend failure")
    checks.append(dict(name="exact_failure_telescope", allocated=str(alpha), spent=str(spent), passed=True))

    numerical = []
    with mp.workdps(140):
        for index, (n, v) in enumerate((n, v) for n in (2, 16, 65536, 1048576)
                                     for v in (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(2, 9))):
            width = Fraction(1) if index % 2 == 0 else Fraction(100, 3)
            delta = alpha if index % 3 == 0 else look_failure(alpha, n.bit_length()-1)
            lo, hi = empirical_bernstein_radius(v, n, width, delta)
            factor = mp.log(4/qmp(delta))
            reference = mp.sqrt(2*qmp(v)*factor/n) + 7*qmp(width)*factor/(3*(n-1))
            require(mp.mpf(str(lo)) <= reference <= mp.mpf(str(hi)), "Independent radius enclosure")
            numerical.append(dict(n=n, variance=str(v), width=str(width), failure=str(delta),
                                  lower=str(lo), upper=str(hi), independent_reference=mp.nstr(reference, 135)))
        exp_lo, exp_hi = exp_interval(Fraction(-3, 100))
        reference = mp.exp(-mp.mpf(3)/100)
        require(mp.mpf(str(exp_lo)) <= reference <= mp.mpf(str(exp_hi)), "Financial support exponential enclosure")
    checks.append(dict(name="sixteen_140_digit_mpmath_radius_and_one_exp_checks", passed=True))

    zero_lo, zero_hi = empirical_bernstein_radius(Fraction(0), 1048576, Fraction(1), look_failure(alpha, 20))
    require(0 < zero_lo <= zero_hi, "Zero events lost the range term")
    tighter = empirical_bernstein_radius(Fraction(0), 1048576, Fraction(1), alpha/2)
    ordinary = empirical_bernstein_radius(Fraction(0), 1048576, Fraction(1), alpha)
    require(tighter[0] > ordinary[1], "Smaller failure must enlarge bound")
    v, n, failure = Fraction(2, 9), 1024, alpha
    base = empirical_bernstein_radius(v, n, Fraction(1), failure)
    scaled = empirical_bernstein_radius(9*v, n, Fraction(3), failure)
    require(Fraction(scaled[0]) <= 3*Fraction(base[1]) and Fraction(scaled[1]) >= 3*Fraction(base[0]), "Range scaling")
    checks.append(dict(name="zero_range_failure_and_scale_checks", passed=True))

    refusals = (
        (lambda: Statistics.observations([Fraction(-1), Fraction(0)]), ValueError),
        (lambda: Statistics.observations([0.0, 1.0]), TypeError),
        (lambda: Statistics(2, Fraction(0), Fraction(-1)), ValueError),
        (lambda: Statistics(2, Fraction(1), Fraction(2)), ValueError),
        (lambda: Statistics.bernoulli(2, 3), ValueError),
        (lambda: Statistics.bernoulli(2, True), ValueError),
        (lambda: empirical_bernstein_radius(Fraction(-1), 2, Fraction(1), alpha), ValueError),
        (lambda: empirical_bernstein_radius(Fraction(0), 1, Fraction(1), alpha), ValueError),
        (lambda: empirical_bernstein_radius(Fraction(0), 2, Fraction(0), alpha), ValueError),
        (lambda: look_failure(alpha, 0), ValueError),
        (lambda: look_failure(Fraction(1), 2), ValueError),
    )
    for function, exception in refusals:
        rejects(function, exception)
    checks.append(dict(name="eleven_invalid_input_refusals", passed=True))

    controller = DyadicCS(alpha, 16)
    previous_upper = Decimal(1)
    first_ready = None
    for j in range(1, 17):
        controller.update(Statistics.bernoulli(2**j, 0))
        require(controller.upper <= previous_upper, "Intersection must retain best upper")
        previous_upper = controller.upper
        if controller.reaches(Fraction(1, 128)) and first_ready is None:
            first_ready = 2**j
    require(first_ready == 8192, "Frozen all-zero stopping path")
    require(controller.result(Fraction(1, 128))["status"] == "TARGET_CERTIFIED", "Ready certificate")
    rejects(lambda: controller.update(Statistics.bernoulli(2**17, 0)), ValueError)
    skip = DyadicCS()
    rejects(lambda: skip.update(Statistics.bernoulli(4, 0)), ValueError)
    bad = DyadicCS()
    bad.update(Statistics.bernoulli(2, 2))
    rejects(lambda: bad.update(Statistics.bernoulli(4, 0)), ValueError)
    failed = DyadicCS()
    for j in range(1, 17):
        failed.update(Statistics.bernoulli(2**j, 2**(j-1)))
    require(failed.result(Fraction(1, 128))["status"] == "SUPPORT_FALLBACK", "Cap fallback")
    require(failed.result(Fraction(1, 128))["certificate_upper"] == "1", "Failed target cannot keep a smaller delivered certificate")
    # Empty intersections are legitimate off the simultaneous event, not a target.
    empty = DyadicCS()
    for j in range(1, 15):
        empty.update(Statistics.bernoulli(2**j, 0))
    empty.update(Statistics.bernoulli(32768, 16384))
    require(empty.empty and not empty.reaches(Fraction(1, 128)), "Empty intersection incorrectly promoted")
    require(empty.result(Fraction(1, 128))["certificate_upper"] == "1", "Empty intersection fallback")
    checks.append(dict(name="ready_cap_empty_and_prefix_controller_checks", passed=True))
    return dict(schema="e12-fixed-finite-oracle-validation-v1", passed=True,
                checks=checks, numerical_oracles=numerical,
                first_all_zero_target_stop=first_ready,
                scope="Finite software/arithmetic preflight; theorem and optional-stopping proof are separate; zero finance fixtures or replays.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out).resolve()
    root = Path(__file__).resolve().parents[4]
    allowed = (root / "results/limitation_program_20261001").resolve()
    if out.parent != allowed or not out.name.startswith("E12_continuation_20261004_"):
        raise ValueError("Fresh dedicated E12 result directory required")
    out.mkdir(exist_ok=False)
    started, cpu = time.monotonic(), time.process_time()
    source_paths = [Path(__file__).resolve(), Path(__file__).with_name("anytime_eb.py").resolve()]
    source_map = {str(p.relative_to(root)).replace("\\", "/"): dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(), bytes=p.stat().st_size) for p in source_paths}
    (out / "prospective_source_map.json").write_text(json.dumps(source_map, indent=2)+"\n", encoding="utf-8")
    try:
        result = validation()
        result.update(administrative_cpu_seconds=time.process_time()-cpu,
                      administrative_wall_seconds=time.monotonic()-started)
        (out / "validation.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
        print(json.dumps({k:v for k,v in result.items() if k not in ("checks", "numerical_oracles")}))
    except BaseException as error:
        (out / "FAILED.json").write_text(json.dumps(dict(status="FAILED", passed=False, error=repr(error), trace=traceback.format_exc()), indent=2)+"\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
