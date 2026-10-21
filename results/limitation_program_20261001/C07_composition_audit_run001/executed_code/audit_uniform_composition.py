"""Independent audit of two fixed optimistic formula-budget screens, not bias."""

from fractions import Fraction
from math import factorial
from pathlib import Path

import mpmath as mp

from research.limitation_program_20261001 import audit_barrier_band as receipt


ROOT = receipt.ROOT
RESULTS = receipt.RESULTS
METHODS = ("density", "centered_interval_maximum")
ALLOWANCE = Fraction(11, 2000)


def independent_formula(error, variance):
    """Enclose two Gaussian interval supremum FORMULAS, not actual probabilities."""
    error, variance = receipt.exact(error), receipt.exact(variance)
    receipt.require(error >= 0 and variance > 0, "Formula domain changed")
    old = mp.iv.dps
    mp.iv.dps = 110
    try:
        z = receipt.iv(error) / mp.iv.sqrt(receipt.iv(variance))
        receipt.require(
            receipt.endpoints(z)[1] < Fraction(1, 10), "Fixed screen small-argument domain"
        )
        density = 2 * receipt.iv(error) / mp.iv.sqrt(2 * mp.iv.pi * receipt.iv(variance))
        series = mp.iv.mpf(0)
        for k in range(65):
            series += (-1) ** k * z ** (2 * k + 1) / (2**k * factorial(k) * (2 * k + 1))
        hi_z = receipt.endpoints(z)[1]
        remainder = hi_z**131 / (2**65 * factorial(65) * 131)
        lo, hi = receipt.endpoints(series)
        widened = mp.iv.mpf([receipt.iv(lo - remainder).a, receipt.iv(hi + remainder).b])
        centered = mp.iv.sqrt(2 / mp.iv.pi) * widened
        return {
            "density": receipt.endpoints(density),
            "centered_interval_maximum": receipt.endpoints(centered),
        }
    finally:
        mp.iv.dps = old


def actual_coefficients(target, candidate):
    """Read only the actual first-date typed graph's two native multipliers."""
    date = candidate["B4_date1"]
    nodes = {value: node for node in target["nodes"] for value in node["out"]}
    scope = date["all_four_asset_date1_scopes"][0]
    clip = nodes[scope["clipped_log"]]
    receipt.require(clip["op"] == "select", "Original high clipping selector changed")
    middle = nodes[clip["args"][1]]
    receipt.require(middle["op"] == "select", "Original low clipping selector changed")
    stack, products = [middle["args"][2]], []
    while stack:
        node = nodes[stack.pop()]
        if node["op"] == "add":
            stack.extend(node["args"])
        elif node["op"] == "cmul":
            products.append(node)
        else:
            receipt.require(node["op"] == "const", "Unexpected date1 increment leaf")
    receipt.require(len(products) == 2, "Original two date1 noise coefficients required")
    by_normal = {node["args"][0]: node["params"]["c"] for node in products}
    common, idio = [
        Fraction(by_normal[normal], 1 << target["fraction_bits"])
        for normal in scope["normal_values"]
    ]
    receipt.require(common > 0 and idio > 0, "Actual B4 native coefficients must be positive")
    receipt.require(
        common == receipt.exact(date["common_coefficient_literal_exact"])
        and idio == receipt.exact(date["idiosyncratic_coefficient_literal_exact"]),
        "Screen coefficient source is not actual target",
    )
    return common, idio


def check_scope_flags(screen):
    receipt.require(
        len(screen["dates"]) == 12 and [x["date"] for x in screen["dates"]] == list(range(1, 13)),
        "Exactly original12 dates required",
    )
    for name in (
        "omitted_terms_credited_as_certified_zero",
        "full_path_stock_or_basket_discrepancy_certified",
        "complete_continuous_price_certificate",
    ):
        receipt.require(screen[name] is False, "Unsupported native/full-price assertion: " + name)
    for value in screen["methods"].values():
        receipt.require(
            value["actual_probability_lower_bound_claimed"] is False
            and value["actual_price_bias_lower_bound_claimed"] is False,
            "Formula lower endpoint mislabelled as actual bias/probability",
        )


def audit(root=ROOT):
    root = Path(root).resolve()
    base = root / "results/limitation_program_20261001"
    directory = base / "C07_composition_screen_run001"
    manifests = {}
    for name in (
        "C06_pair_run001",
        "C06_pair_audit_run001",
        "C07_bound_date1_run001",
        "C07_composition_screen_run001",
    ):
        source_dir = base / name
        manifests[name] = receipt.verify_manifest(root, source_dir)
        receipt.require(
            receipt.read(source_dir / "summary.json")["passed"] is True,
            "Source or screen receipt failed",
        )
    counts = receipt.xml_counts(directory / "tests.xml")
    receipt.require(
        counts == dict(tests=10, failures=0, errors=0, skipped=0),
        "Producer fixture count/status changed",
    )
    protocol = receipt.read(directory / "protocol.json")
    receipt.require(
        protocol["candidates"] == [20, 24]
        and protocol["dates"] == list(range(1, 13))
        and protocol["methods"] == list(METHODS)
        and protocol["allowance_dollars_exact"] == [11, 2000]
        and protocol["before_tests_and_two_fixed_cutoff_screens"] is True,
        "Prospective screen scope changed",
    )
    certificate = receipt.read(base / "C06_pair_run001/certificate.json")
    target_info = certificate["source_bindings"]["B4x12"]
    target_path = receipt.local(root, target_info["target"])
    receipt.require(
        receipt.sha(target_path) == target_info["target_sha256"]
        and target_info["pair_count"] == 30
        and target_info["scalar_count"] == 60,
        "Original B4 source/pair contract changed",
    )
    target = receipt.read(target_path)
    audited = []
    for bits in (20, 24):
        candidate = next(x for x in certificate["candidates"] if x["cutoff_bits"] == bits)
        screen = receipt.read(directory / f"cutoff{bits}_screen.json")
        check_scope_flags(screen)
        beta = receipt.exact(candidate["coordinate_discrepancy_upper_exact"])
        delta = Fraction(1, 1 << bits)
        common, idio = actual_coefficients(target, candidate)
        receipt.require(
            receipt.exact(candidate["delta_exact"]) == delta
            and candidate["coupling_id"] == f"C06_q32_f40_shared_uniform_delta2minus{bits}",
            "Selected cutoff coupling changed",
        )
        totals = {method: [Fraction(0), Fraction(0)] for method in METHODS}
        dates = []
        for row in screen["dates"]:
            date = row["date"]
            error, variance = date * (common + idio) * beta, Fraction(3 * date, 1000)
            receipt.require(
                receipt.exact(row["optimistic_log_discrepancy_exact"]) == error
                and receipt.exact(row["common_log_variance_exact"]) == variance,
                "Datewise optimistic formula/source coefficients changed",
            )
            formulas = row["formula_enclosures"]
            receipt.require(
                formulas["log_length_interval_exact"] == [receipt.pair(2 * error)] * 2,
                "Formula log interval length changed",
            )
            independent = independent_formula(error, variance)
            for method in METHODS:
                receipt.enclose_claim(
                    formulas[method]["interval_exact"],
                    independent[method],
                    f"cutoff{bits}/date{date}/{method}",
                )
                for side in (0, 1):
                    totals[method][side] += receipt.exact(formulas[method]["interval_exact"][side])
            dates.append(
                dict(
                    date=date,
                    independent_formula_intervals_exact={
                        name: list(map(receipt.pair, values))
                        for name, values in independent.items()
                    },
                )
            )
        tail = 40 * 30 * delta
        receipt.require(
            receipt.exact(screen["tail_formula_dollars_exact"]) == tail,
            "Whole30-pair tail not charged once in dollars",
        )
        methods = {}
        for method, total in totals.items():
            union = [min(Fraction(1), value) for value in total]
            dollars = [40 * value + tail for value in union]
            saved = screen["methods"][method]
            receipt.require(
                saved["union_formula_interval_exact"] == list(map(receipt.pair, union))
                and saved["barrier_and_tail_formula_dollars_interval_exact"]
                == list(map(receipt.pair, dollars))
                and saved["formula_floor_exceeds_remaining_headroom"] == (dollars[0] > ALLOWANCE),
                "Exact union/cap/tail formula budget classification changed",
            )
            methods[method] = dict(
                formula_dollars_interval_exact=list(map(receipt.pair, dollars)),
                lower_formula_value_exceeds_headroom=dollars[0] > ALLOWANCE,
                actual_probability_or_price_lower_bound=False,
            )
        audited.append(dict(cutoff_bits=bits, independently_audited_dates=dates, methods=methods))
    summary = receipt.read(directory / "summary.json")
    receipt.require(
        summary["actual_price_bias_lower_bound_claimed"] is False
        and summary["full_native_path_error_proved"] is False
        and summary["full_G2_closed"] is False
        and summary["financial_samples_or_gate_replays"] == 0,
        "Screen summary claimed full financial proof",
    )
    return dict(
        passed=True,
        local_only=True,
        manifests=manifests,
        producer_tests=counts,
        target_binding={"path": target_info["target"], "sha256": receipt.sha(target_path)},
        rows=audited,
        independently_enclosed_formula_rows=48,
        new_cutoff_candidates=0,
        financial_samples_or_replays=0,
        interpretation=(
            "Lower endpoints enclose chosen upper-bound formula values only; "
            "not actual bias/probability lower bounds"
        ),
        complete_price_error_dollars=None,
        full_G2_closed=False,
    )
