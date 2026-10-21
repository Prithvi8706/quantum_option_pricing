"""Independent Gaussian integrals and every saved quantile-floor comparison."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from math import factorial
from pathlib import Path
import shutil

import mpmath as mp
from mpmath.libmp import to_rational

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_checkpoint import (
    PROGRAM,
    manifest,
    read,
    relative,
    save,
    verify,
)


def interval(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    return tuple(Fraction(*to_rational(x)) for x in value._mpi_)


@lru_cache(None)
def independent_pi_interval():
    lower, upper = Fraction(0), Fraction(0)
    for inverse in (2, 3):
        partial = sum(
            (Fraction((-1) ** k, (2 * k + 1) * inverse ** (2 * k + 1)) for k in range(200)),
            Fraction(0),
        )
        lower += 4 * partial
        upper += 4 * (partial + Fraction(1, 401 * inverse**401))
    assert lower > Fraction(25, 8)
    return lower, upper


@lru_cache(None)
def independent_cdf(argument):
    """Taylor180, interval110digits, independently enclosed atan(1/2)+atan(1/3)."""
    argument = Fraction(argument)
    assert -8 <= argument <= 8
    mp.iv.dps = 110
    if not argument:
        return Fraction(1, 2), Fraction(1, 2)
    x = abs(argument)
    y = interval(x**2 / 2)
    integral_polynomial = interval(Fraction((-1) ** 180, factorial(180) * 361))
    for k in range(179, -1, -1):
        integral_polynomial = integral_polynomial * y + interval(
            Fraction((-1) ** k, factorial(k) * (2 * k + 1))
        )
    remainder = x**363 / (2**181 * factorial(181) * 363)
    pi_lo, pi_hi = independent_pi_interval()
    pi = mp.iv.mpf([interval(pi_lo).a, interval(pi_hi).b])
    prefactor = 1 / mp.iv.sqrt(2 * pi)
    integral = interval(x) * integral_polynomial
    lo, hi = endpoints(integral)
    enclosure = mp.iv.mpf([interval(lo - remainder).a, interval(hi + remainder).b])
    positive = interval(Fraction(1, 2)) + prefactor * enclosure
    lo, hi = endpoints(positive)
    return (1 - hi, 1 - lo) if argument < 0 else (lo, hi)


def run(output):
    output.relative_to(PROGRAM.resolve())
    assert not output.exists()
    producer = PROGRAM / "C06_quantile_rounding_run001"
    assert read(producer / "summary.json")["passed"]
    output.mkdir()
    receipt = read(producer / "manifest.json")
    frozen = {**receipt["files"], **receipt["frozen_inputs"]}
    frozen[relative(producer / "manifest.json")] = digest(producer / "manifest.json")
    code = Path(__file__).resolve()
    frozen[relative(code)] = digest(code)
    shutil.copy2(code, output / code.name)
    protocol = dict(
        local_only=True,
        created_utc=datetime.now(timezone.utc).isoformat(),
        before_independent_Gaussian_comparisons=True,
        interval_decimal_precision=110,
        integrated_Gaussian_Taylor_degree=180,
        source_quantile_words=16,
        new_quantile_word_candidates=0,
        source_solver_or_CDF_implementation_imported=False,
        new_financial_prices_or_gates=0,
        new_pytest_cases=0,
        frozen_inputs=frozen,
    )
    save(output / "protocol.json", protocol)
    verify(protocol)
    word_records = read(producer / "quantile_words.json")["words"]
    raw_words = [row["raw_uniform_word"] for row in word_records]
    assert len(raw_words) == len(set(raw_words)) == 16
    count = 0
    reports = []
    for raw in raw_words:
        record = read(producer / "words" / (f"{raw:08x}.json"))
        probability = Fraction(2 * raw + 1, 2**33)
        assert record["raw_uniform_word"] == raw
        assert Fraction(*record["midpoint_probability_exact"]) == probability
        lo, hi = Fraction(-8), Fraction(8)
        assert independent_cdf(lo)[1] < probability < independent_cdf(hi)[0]
        for comparison in record["CDF_comparison_history"]:
            argument = (lo + hi) / 2
            assert Fraction(*comparison["argument_exact"]) == argument
            lower, upper = independent_cdf(argument)
            recorded_lower, recorded_upper = (
                Fraction(*v) for v in comparison["CDF_interval_exact"]
            )
            assert max(lower, recorded_lower) <= min(upper, recorded_upper)
            if upper < probability:
                assert recorded_upper < probability
                lo = argument
            else:
                assert lower > probability and recorded_lower > probability
                hi = argument
            count += 1
        assert list(map(lambda v: Fraction(*v), record["open_quantile_bracket_exact"])) == [lo, hi]
        assert record["certified"] and not record["censored"]
        assert record["bisection_steps"] == 44 == len(record["CDF_comparison_history"])
        assert record["CDF_enclosure_evaluations"] == 46
        native = record["native_signed72_f40_word"]
        assert Fraction(native, 2**40) <= lo < hi <= Fraction(native + 1, 2**40)
        assert -(1 << 71) <= native < 1 << 71
        assert record["native_two_complement_word"] == native % (1 << 72)
        assert not record["all_input_solver_completeness_inferred"]
        assert not record["quantum_gate_count_inferred"]
        reports.append(dict(raw=raw, native_signed_floor=native, all44_branches_verified=True))
    assert count == 704
    ks = Fraction(1, 2**33) + Fraction(2, 5 * 2**40)
    laws = []
    for case, dimension in (("B4x12", 60), ("B8x52", 468)):
        law = read(producer / (case + "_certificate.json"))
        assert Fraction(*law["defined_rounded_law_KS_upper_exact"]) == ks
        assert (
            Fraction(*law["all_date_defined_rounded_law_price_bias_upper_exact"])
            == dimension * 80 * ks
        )
        assert not any(
            law[f]
            for f in (
                "all_input_solver_completeness_certified",
                "accepted_Box_Muller_law_certified",
                "native_financial_path_arithmetic_certified",
                "coherent_loader_implemented",
                "complete_original_price_certified",
                "second_discount_applied",
                "quantum_resources_or_runtime_extrapolated_from_classical_solver",
            )
        )
        laws.append(
            dict(
                case=case, defined_law_KS_verified=True, continuous_payoff_BV_transfer_verified=True
            )
        )
    summary = read(producer / "summary.json")
    assert summary["actual_quantile_words_certified"] == 16
    assert summary["actual_quantile_words_censored"] == 0
    assert summary["total_actual_word_bisection_steps"] == count
    assert summary["fixtures_passed"] == 31
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            independently_certified_saved_words=reports,
            saved_Gaussian_bisection_branches_independently_verified=count,
            conditional_law_reports=laws,
            producer_tests_reconciled=31,
            new_pytest_cases=0,
            new_quantile_words=0,
            new_financial_prices_or_gates=0,
            all_input_solver_completeness_certified=False,
            coherent_loader_or_native_price_certified=False,
            full_G2_closed=False,
        ),
    )
    manifest(output, protocol)
    print("Independent16word/704branch Gaussian-floor audit PASS; loader remains open", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
