"""Independent source/receipt and rigorous numeric audit of frozen C07 run002.

This module never imports the audited implementation and never samples a path.
The conditional Gaussian theorem is established analytically, independently of
the positive idiosyncratic factor and independently of the coupling good event.
"""

from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path
import xml.etree.ElementTree as ET

import mpmath as mp


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results/limitation_program_20261001"
IV_DIGITS = 110
PROOF = {
    "original_factorization": (
        "At t=1/12 the continuous original GBM is S_i=100 exp(-t*3/200"
        "+(3/10)sqrt((2/5)t)Z+(3/10)sqrt((3/5)t)Z_i). The continuous"
        " drivers are independent. Thus B=exp(s_c Z)W, W>0 finite almost"
        " surely and independent of Z, with s_c^2=3/1000. This assertion"
        " concerns the continuous model only, not the joint digital pair law."
    ),
    "density_bound": (
        "For 0<=eta<140, conditional on W, the log interval has length"
        " L=log((140+eta)/(140-eta)); the standard-normal interval length"
        " is L/s_c. Since phi(z)<=1/sqrt(2*pi), its probability is at most"
        " min(1,L/sqrt(2*pi*s_c^2)). Average this uniform bound over W."
    ),
    "centered_maximum": (
        "For half length d=L/(2*s_c), g(c)=Phi(c+d)-Phi(c-d) is even."
        " For c>=0, (c+d)^2-(c-d)^2=4cd>=0, hence g'(c)<=0; for c<=0"
        " the sign reverses. Its exact supremum over every positive W"
        " is g(0)=erf(L/sqrt(8*s_c^2)), also at most the density bound."
    ),
    "endpoint_and_good_event": (
        "The conditional lognormal law has no atom at either deterministic"
        " endpoint or H=140; averaging preserves zero endpoint probability."
        " The original strict basket<H test is preserved. Digital equality"
        " can have positive mass. Decision disagreement implies a bad event"
        " or the unconditional continuous band. No conditional-on-good-event"
        " independence or Gaussian law is used."
    ),
    "outward_arithmetic": (
        "For exact x=eta/H in [0,1), log((1+x)/(1-x))=2 sum x^(2k+1)/(2k+1)."
        " The remainder after N terms is at most 2*x^(2N+1)/((2N+1)*(1-x^2))."
        " Integer isqrt of floor(q*2^(2p)) brackets sqrt(q) on dyadics."
        " Every dyadic lower endpoint uses floor and upper uses ceiling;"
        " multiplication takes the minimum and maximum of four products."
        " For exp(-z^2/2), the integrated degree-N Taylor remainder on [0,8]"
        " is at most 8^(2N+3)/(2^(N+1)*(N+1)!*(2N+3)), since every exp(-t)"
        " derivative has magnitude at most one for t>=0. Above8, monotonicity"
        " supplies the lower bound at min(z_lower,8), and one supplies the upper."
        " Positive denominator lower endpoints and upper numerators give"
        " outward quotient uppers. Clipping by a second proved upper is valid."
    ),
    "relative_log_radius": (
        "If exp(-delta)<=S_d/S_c<=exp(delta) holds for every stock INCLUDING"
        " native exp/clipping, positive sums preserve these inequalities."
        " The decision band has log length 2*delta. A symmetric dollar radius"
        " H*(exp(delta)-1) covers both sides because exp(delta)+exp(-delta)>=2."
        " On 0<=delta<=1/2, sum_{k=1}^{80}delta^k/k! is a lower endpoint."
        " The remaining positive terms are bounded by delta^81/81! divided"
        " by 1-delta/82: all following ratios are at most delta/82. The upper"
        " endpoint is exact rational (no float or rounded-down radius)."
        " A discrepancy of raw pre-exp logs alone is not this stock ratio claim."
    ),
    "scope": (
        "One-date bands do not provide full smooth Asian payoff zeta, an"
        " any-date band union, a native discrepancy radius, or tail dollars."
        " These remain null in the audited production artifact. The fixed"
        " eta=1/10000 dollar is exploratory only, not a financial certificate."
    ),
}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exact(value):
    return Fraction(*value) if isinstance(value, (list, tuple)) else Fraction(value)


def pair(value):
    value = exact(value)
    return [value.numerator, value.denominator]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "Manifest path escaped workspace")
    return path


def verify_manifest(root, directory, verify_current_inputs=True):
    data = read(directory / "manifest.json")
    require(data.get("manifest_self_hash_excluded") is True, "Manifest rule changed")
    checked = []
    for name, digest in data["files"].items():
        path = local(root, name)
        require(path.is_relative_to(directory.resolve()), "Receipt file outside receipt")
        require(sha(path) == digest, "Receipt file hash changed: " + name)
        checked.append(name)
    if verify_current_inputs:
        for name, digest in data["frozen_inputs"].items():
            require(sha(local(root, name)) == digest, "Frozen input changed: " + name)
    actual = {
        path.relative_to(root).as_posix()
        for path in directory.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    require(set(checked) == actual, "Manifest file inventory incomplete")
    for snapshot in directory.joinpath("executed_code").glob("*.py"):
        original = "research/limitation_program_20261001/" + snapshot.name
        require(
            sha(snapshot) == data["frozen_inputs"].get(original),
            "Executed snapshot does not match frozen original: " + original,
        )
    return {"receipt_files": len(checked), "frozen_inputs": len(data["frozen_inputs"])}


def xml_counts(path):
    return {
        name: sum(
            int(node.attrib.get(name, 0)) for node in ET.parse(path).getroot().iter("testsuite")
        )
        for name in ("tests", "failures", "errors", "skipped")
    }


def iv(value):
    value = exact(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    # libmp converts finite binary endpoints exactly; no decimal float enters.
    return tuple(Fraction(*mp.libmp.to_rational(point)) for point in value._mpi_)


def independent_band_enclosure(eta, barrier, variance):
    """mp.iv plus a separate 64-term integrated series, for the fixed small band."""
    eta, barrier, variance = map(exact, (eta, barrier, variance))
    require(0 <= eta < barrier and variance > 0, "Independent band domain")
    old = mp.iv.dps
    mp.iv.dps = IV_DIGITS
    try:
        length = mp.iv.log((iv(barrier) + iv(eta)) / (iv(barrier) - iv(eta)))
        scale = mp.iv.sqrt(iv(variance))
        density = length / mp.iv.sqrt(2 * mp.iv.pi * iv(variance))
        argument = length / (2 * scale)
        require(endpoints(argument)[1] < Fraction(1, 10), "Fixed small-band audit domain")
        terms = 64
        polynomial = mp.iv.mpf(0)
        for k in range(terms + 1):
            polynomial += (-1) ** k * argument ** (2 * k + 1) / (2**k * factorial(k) * (2 * k + 1))
        upper_argument = endpoints(argument)[1]
        remainder = upper_argument ** (2 * terms + 3) / (
            2 ** (terms + 1) * factorial(terms + 1) * (2 * terms + 3)
        )
        integral_lo, integral_hi = endpoints(polynomial)
        integral = mp.iv.mpf([iv(integral_lo - remainder).a, iv(integral_hi + remainder).b])
        maximum = mp.iv.sqrt(2 / mp.iv.pi) * integral
        return {
            "log_length": [pair(x) for x in endpoints(length)],
            "density": [pair(x) for x in endpoints(density)],
            "centered_interval_maximum": [pair(x) for x in endpoints(maximum)],
            "independent_integrated_taylor_terms": terms,
            "mp_iv_digits": IV_DIGITS,
            "all_interval_endpoints_exact_binary_rationals": True,
        }
    finally:
        mp.iv.dps = old


def independent_radius_enclosure(delta, barrier):
    delta, barrier = exact(delta), exact(barrier)
    old = mp.iv.dps
    # The smallest fixture's saved rational width is ~1e-767.
    mp.iv.dps = 1000
    try:
        return [pair(x) for x in endpoints(iv(barrier) * (mp.iv.exp(iv(delta)) - 1))]
    finally:
        mp.iv.dps = old


def enclose_claim(claim, reference, label):
    lo, hi = map(exact, claim)
    ref_lo, ref_hi = map(exact, reference)
    require(lo <= ref_lo <= ref_hi <= hi, label + " does not enclose independent interval")


def source_contract(builder):
    tree = ast.parse(builder.read_text(encoding="utf-8"))
    constants = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Tuple) and all(isinstance(x, ast.Name) for x in target.elts):
                if [x.id for x in target.elts] == ["SIGMA", "CORR", "S0", "RATE", "T", "K", "H"]:
                    constants.append([Fraction(str(x)) for x in ast.literal_eval(node.value)])
    require(
        constants
        == [
            [
                Fraction(3, 10),
                Fraction(2, 5),
                Fraction(100),
                Fraction(3, 100),
                Fraction(1),
                Fraction(100),
                Fraction(140),
            ]
        ],
        "Original GBM changed",
    )
    build = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build"
    )
    normalized = ast.unparse(build)
    checks = (
        "dt = T / nt",
        "count = nt * (na + 1)",
        "zs = normals_graph(g, count, q)",
        "zs[j * (na + 1)]",
        "zs[j * (na + 1) + 1 + i]",
        "SIGMA * math.sqrt(dt * CORR)",
        "SIGMA * math.sqrt(dt * (1 - CORR))",
        "(RATE - 0.5 * SIGMA ** 2) * dt",
        "1 / na",
        "g.lt(tree(g, baskets, g.maximum), g.c(H))",
        "math.exp(-RATE * T)",
    )
    for check in checks:
        require(check in normalized, "Original builder structure changed: " + check)
    return {
        "builder_sha256": sha(builder),
        "assets": 4,
        "dates": 12,
        "date": 1,
        "common_log_variance_exact": [3, 1000],
        "barrier_dollars_exact": [140, 1],
        "strict_alive_less_than_barrier": True,
        "continuous_endpoint_mass_exact": [0, 1],
        "digital_endpoint_mass_claimed_zero": False,
        "original_source_ast_checks": len(checks),
    }


def audit(root=ROOT):
    root = Path(root).resolve()
    base = root / "results/limitation_program_20261001"
    old, current = base / "C07_barrier_run001", base / "C07_barrier_run002"
    manifests = {
        name: verify_manifest(root, directory)
        for name, directory in (("run001", old), ("run002", current))
    }
    prior_counts, counts = xml_counts(old / "tests.xml"), xml_counts(current / "tests.xml")
    require(
        prior_counts == {"tests": 51, "failures": 1, "errors": 0, "skipped": 0},
        "Preserved first-run fixture history changed",
    )
    require(
        counts == {"tests": 51, "failures": 0, "errors": 0, "skipped": 0},
        "Run002 fixture history changed",
    )
    failures = [
        node
        for node in ET.parse(old / "tests.xml").getroot().iter("testcase")
        if node.find("failure") is not None
    ]
    require(
        len(failures) == 1 and failures[0].attrib["name"].endswith("[delta1]"),
        "First-run failure identity changed",
    )
    old_test = (old / "executed_code/test_barrier_band_certificate.py").read_text(encoding="utf-8")
    new_test = (current / "executed_code/test_barrier_band_certificate_v2.py").read_text(
        encoding="utf-8"
    )
    require(
        old_test.replace(
            "with mp.workdps(120):\n        exact_radius",
            "with mp.workdps(1000):\n        exact_radius",
        )
        == new_test,
        "Run002 changed more than independent radius reference precision",
    )
    require(
        sha(old / "executed_code/barrier_band_certificate.py")
        == sha(current / "executed_code/barrier_band_certificate.py"),
        "Analytic implementation changed",
    )
    require(
        not (old / "B4_date1_certificate.json").exists() and not (old / "summary.json").exists(),
        "Failed run001 gained candidate outputs",
    )
    protocol, summary = read(current / "protocol.json"), read(current / "summary.json")
    certificate = read(current / "B4_date1_certificate.json")
    require(
        summary["passed"] is True
        and protocol["before_tests_and_probability_bound_evaluation"] is True,
        "Prospective or success status changed",
    )
    require(
        protocol["analytical_bound_forms"] == ["density", "centered_interval_maximum"]
        and protocol["diagnostic_eta_dollars_exact"] == [1, 10000]
        and protocol["diagnostic_eta_is_a_proved_native_discrepancy"] is False
        and protocol["eta_grid_or_adaptive_radius_search"] is False,
        "Fixed exploratory scope changed",
    )
    source = source_contract(root / "research/advantage_frontier_20260923/barrier_oracle_depth.py")
    require(
        certificate["model"]["builder_sha256"] == source["builder_sha256"]
        and certificate["model"]["assets"] == 4
        and certificate["model"]["dates"] == 12
        and certificate["common_log_variance_exact"] == [3, 1000]
        and certificate["model"]["barrier_dollars_exact"] == [140, 1]
        and certificate["observation_time_exact"] == [1, 12]
        and certificate["date"] == 1,
        "Original one-date model binding changed",
    )
    null_fields = (
        "eta",
        "path_log_discrepancy",
        "bad_event_probability",
        "proved_discrepancy_band_bounds",
        "one_date_decision_disagreement_upper_exact",
        "discounted_smooth_payoff_zeta",
        "discounted_tail_dollars",
        "any_contractual_date_band_probability",
        "dollar_bias_upper_exact",
    )
    require(
        all(certificate[name] is None for name in null_fields),
        "Missing proof became a production value",
    )
    false_fields = (
        "full_G2_certificate",
        "digital_paired_outputs_claimed_independent_gaussian",
        "gaussian_law_conditioned_on_coupling_good_event",
        "all_contractual_dates_covered",
        "missing_bounds_are_zero",
        "second_discount_applied",
    )
    require(
        all(certificate[name] is False for name in false_fields), "Unsupported full-price assertion"
    )
    require(
        certificate["finite_financial_samples_used"] == 0
        and summary["new_financial_gate_replays"] == 0
        and summary["new_financial_price_samples"] == 0,
        "Unexpected financial samples",
    )
    assembly = certificate["dollar_bias_assembly"]
    require(
        assembly["dollar_bias_upper_exact"] is None
        and all(x is None for x in assembly["components"].values()),
        "Missing full-path component charged as known",
    )
    band = certificate["fixed_exploratory_band_diagnostic"]
    require(
        band["exploratory_only"] is True
        and band["proved_native_discrepancy"] is False
        and band["used_as_financial_error_certificate"] is False
        and band["eta_dollars_exact"] == [1, 10000],
        "Exploratory diagnostic promoted",
    )
    independent = independent_band_enclosure(Fraction(1, 10000), 140, Fraction(3, 1000))
    enclose_claim(band["log_length_interval_exact"], independent["log_length"], "Log length")
    for kind in ("density", "centered_interval_maximum"):
        enclose_claim(band[kind]["interval_exact"], independent[kind], kind)
        require(
            band[kind]["probability_upper_exact"] == band[kind]["interval_exact"][1],
            "Upper endpoint changed",
        )
    require(
        exact(band["centered_interval_maximum"]["probability_upper_exact"])
        < exact(band["density"]["interval_exact"][0]),
        "Centered bound no longer tighter",
    )
    return {
        "passed": True,
        "audit_independent_of_target_implementation": True,
        "source_contract": source,
        "historical_manifests": manifests,
        "run001_tests": prior_counts,
        "run001_passed_tests": 50,
        "run001_produced_candidates": 0,
        "run001_failure": failures[0].attrib["name"],
        "run002_tests": counts,
        "run002_only_reference_precision_changed": True,
        "independent_numeric_enclosure": independent,
        "proof": PROOF,
        "verified_null_production_fields": list(null_fields),
        "finite_financial_samples_used": 0,
        "new_financial_gate_replays": 0,
        "new_production_eta_values": 0,
        "full_G2_closed": False,
        "full_price_error_dollars": None,
    }
