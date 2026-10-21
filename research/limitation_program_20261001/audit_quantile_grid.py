"""Independent audit of the different-law scalar midpoint-grid theorem.

This audit performs exact algebra and contract checks, without calling the
certificate producer or simulating a financial path or quantum circuit.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
import xml.etree.ElementTree as ET

import pytest

from research.limitation_program_20261001.progress import ROOT


PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "C06_quantile_grid_run001"
BUILDER = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
CODE = ("audit_quantile_grid.py", "test_audit_quantile_grid.py")
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
PARAMETERS = ("SIGMA", "CORR", "S0", "RATE", "T", "K", "H")
EXPECTED = tuple(map(Fraction, (".3", ".4", "100", ".03", "1", "100", "140")))
FALSE_GUARDS = (
    "accepted_Box_Muller_law_certified",
    "native_rounded_inverse_CDF_or_path_certified",
    "coherent_loader_implemented",
    "complete_original_price_certified",
    "second_discount_applied",
)
THEOREM = {
    "monotonicity": (
        "At date j the coefficient of an earlier common or idiosyncratic "
        "normal is respectively sigma*sqrt(dt*rho) or sigma*sqrt(dt*(1-rho)); "
        "both are positive. Fixing the other finite coordinates therefore "
        "makes every affected exact stock, date basket and Asian average "
        "nondecreasing. No digital exponent or clipped-path monotonicity is asserted."
    ),
    "cap_and_variation": (
        "A=(1/nt)*sum_j B_j. On survival every B_j<H, so A<H and "
        "0<=exp(-rT)*max(A-K,0)<(H-K)*exp(-rT)<40. Each coordinate's "
        "survival set is an intersection of lower half-lines. Before its "
        "endpoint the payoff is nonnegative and nondecreasing; at the "
        "strict-knockout endpoint it becomes zero. Its increase plus one "
        "downward jump has variation<=2*40=80. Empty/full half-lines obey "
        "the same bound. Increasing exact Phi inverse preserves this variation."
    ),
    "midpoint": (
        "On a width-w cell with midpoint m, each half contributes at most "
        "(w/2) times its pointwise variation from f(m). The left and right "
        "variation sum to the cell variation, including the specified "
        "midpoint value. Thus absolute cell quadrature error<=w*TVcell/2. "
        "Summing yields TV/(2*N). One-sided endpoint limits define f(0),f(1); "
        "endpoint choices have measure zero. Strict midpoint knockout is paid."
    ),
    "independent_product": (
        "Replace independent scalar uniform coordinates by their midpoint "
        "grid one at a time. For every fixed choice of all other coordinates, "
        "continuous or discrete, the same variation bound holds. Integrating "
        "each signed difference and applying triangle inequality gives "
        "d*80/(2*2^q). The bounded payoff makes all mixed integrations valid. "
        "The normal law here is the exact independent scalar quantile law."
    ),
    "nontransfer": (
        "This is a conditional price-law result for a different ideal loader. "
        "Finite paired Box-Muller, rounded quantiles, native clipping/exp, "
        "finite arithmetic and coherent implementation are not certified. "
        "No native source, loader, physical runtime or quantum advantage is adopted."
    ),
}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    if isinstance(value, (list, tuple)):
        if len(value) != 2 or any(type(item) is not int for item in value) or value[1] <= 0:
            raise ValueError("Exact rational pair required")
        return Fraction(*value)
    if type(value) is int or isinstance(value, Fraction):
        return Fraction(value)
    raise ValueError("Exact rational value required")


def _expression(source):
    return ast.dump(ast.parse(source, mode="eval").body, include_attributes=False)


def audit_builder_contract(builder_path=BUILDER):
    """Check the economic template, not the accuracy of its native approximation."""
    path = Path(builder_path)
    module = ast.parse(path.read_text(encoding="utf-8"))
    bindings = []
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Tuple) and all(isinstance(x, ast.Name) for x in target.elts):
            if tuple(x.id for x in target.elts) == PARAMETERS:
                bindings.append(tuple(Fraction(str(x)) for x in ast.literal_eval(node.value)))
    if bindings != [EXPECTED]:
        raise ValueError("Original continuous economic parameters changed")
    functions = [
        node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "build"
    ]
    if len(functions) != 1:
        raise ValueError("Unique original build template required")
    nodes = list(ast.walk(functions[0]))
    assignments = {
        "count": "nt * (na + 1)",
        "dt": "T / nt",
        "common": "g.cmul(zs[j * (na + 1)], SIGMA * math.sqrt(dt * CORR))",
        "idio": "g.cmul(zs[j * (na + 1) + 1 + i], SIGMA * math.sqrt(dt * (1 - CORR)))",
        "steps[0]": "g.add(steps[0], g.c(math.log(S0)))",
        "steps": "[steps[j] if j < d else g.add(steps[j], steps[j - d]) for j in range(nt)]",
        "baskets": (
            "[g.cmul(tree(g, [stocks[i][j] for i in range(na)], g.add), 1 / na) "
            "for j in range(nt)]"
        ),
        "alive": "g.lt(tree(g, baskets, g.maximum), g.c(H))",
        "average": "g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))",
        "payoff": "g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))",
        "g.outputs": "dict(Y=g.select(alive, payoff, g.c(0)))",
    }
    for target, expression in assignments.items():
        matching = [
            node
            for node in nodes
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and ast.unparse(node.targets[0]) == target
            and ast.dump(node.value, include_attributes=False) == _expression(expression)
        ]
        if len(matching) != 1:
            raise ValueError("Original positive-weight/strict-barrier template changed: " + target)
    step = _expression(
        "steps.append(g.add(g.add(common, idio), g.c((RATE - .5 * SIGMA ** 2) * dt)))"
    )
    if (
        sum(
            isinstance(node, ast.Call) and ast.dump(node, include_attributes=False) == step
            for node in nodes
        )
        != 1
    ):
        raise ValueError("Original common/idiosyncratic increment template changed")
    return {
        "parameter_bindings_exact": {
            name: pair(value) for name, value in zip(PARAMETERS, EXPECTED, strict=True)
        },
        "positive_increment_coefficients_and_average_template_checked": True,
        "strict_less_than_survival_template_checked": True,
        "native_clipping_exp_and_rounding_accuracy_audited": False,
        "builder_path": str(path.resolve()),
        "builder_sha256": sha(path),
    }


def independent_model(case, builder_path=BUILDER):
    if case not in CASES:
        raise ValueError("Original supported contract required")
    assets, dates = CASES[case]
    sigma, rho, spot, rate, maturity, strike, barrier = EXPECTED
    return {
        "case": case,
        "assets": assets,
        "dates": dates,
        "volatility_exact": pair(sigma),
        "correlation_exact": pair(rho),
        "spot_dollars_exact": pair(spot),
        "rate_exact": pair(rate),
        "maturity_years_exact": pair(maturity),
        "strike_dollars_exact": pair(strike),
        "barrier_dollars_exact": pair(barrier),
        "equal_asset_volatility": True,
        "basket": "positive equal-weight arithmetic spot basket",
        "builder_path": str(Path(builder_path).resolve()),
        "builder_sha256": sha(builder_path),
        "continuous_driver_law": "independent common and idiosyncratic Brownian drivers",
        "digital_paired_outputs_claimed_independent_gaussian": False,
    }


def audit_task(task, case):
    assets, dates = CASES[case]
    if task["assets"] != assets or task["dates"] != dates:
        raise ValueError("Original dimensions changed")
    names = (
        "annual_volatility_each_asset",
        "equicorrelation",
        "spot_each_asset_dollars",
        "annual_rate",
        "maturity_years",
        "strike_dollars",
        "barrier_dollars",
    )
    if tuple(Fraction(str(task[name])) for name in names) != EXPECTED:
        raise ValueError("Original task economic parameters changed")
    expected_payoff = (
        "exp(-r*T) * max(mean over all asset/date spots - K, 0) * "
        "indicator(max over monitored dates of equal-weight spot basket < H)"
    )
    if (
        task["payoff"] != expected_payoff
        or task["continuous_sampling"]
        != (
            "Independent common/idiosyncratic standard normals give exact GBM log "
            "increments at each contractual date before numerical representation."
        )
        or task["barrier_equality"] != "basket >= H is knocked out; alive uses strict < H"
        or len(task["observation_times"]) != dates
    ):
        raise ValueError(
            "Original positive-average, independent-driver or strict-barrier contract changed"
        )
    return True


def audit_grid_certificate(certificate, task, builder_path=BUILDER):
    case = certificate["case"]
    model = independent_model(case, builder_path)
    audit_task(task, case)
    if certificate["original_model_binding"] != model:
        raise ValueError("Original model provenance or assumptions changed")
    if certificate["ideal_law"] != "independent Phi_inverse((raw+1/2)/2^q) scalar normals":
        raise ValueError("Independent scalar midpoint law required")
    bits, headroom = certificate["uniform_bits"], rational(certificate["headroom_exact"])
    if type(bits) is not int or bits != 32 or headroom != Fraction(11, 2000):
        raise ValueError("Frozen one-grid precision/allowance changed")
    dimension = (model["assets"] + 1) * model["dates"]
    cap = EXPECTED[-1] - EXPECTED[-2]
    if cap != 40 or EXPECTED[3] * EXPECTED[4] <= 0:
        raise ValueError("Discounted payoff cap derivation changed")
    variation = 2 * cap
    bound = Fraction(dimension, 1 << bits) * variation / 2
    if (
        certificate["normal_coordinates"] != dimension
        or rational(certificate["coordinate_total_variation_upper_dollars_exact"]) != variation
        or rational(certificate["all_date_continuous_payoff_grid_law_error_upper_dollars_exact"])
        != bound
        or certificate["ideal_grid_law_term_fits_headroom"] is not (bound <= headroom)
        or certificate["continuous_ideal_grid_law_certificate"] is not True
        or any(certificate[name] is not False for name in FALSE_GUARDS)
    ):
        raise ValueError("Independent BV/telescope bound or transfer guard does not reconcile")
    dt = EXPECTED[4] / model["dates"]
    common_squared, idio_squared = (
        EXPECTED[0] ** 2 * dt * EXPECTED[1],
        EXPECTED[0] ** 2 * dt * (1 - EXPECTED[1]),
    )
    if min(common_squared, idio_squared) <= 0:
        raise ValueError("Positive future-stock coordinate coefficients required")
    return {
        "passed": True,
        "case": case,
        "normal_coordinates": dimension,
        "common_increment_log_coefficient_squared_exact": pair(common_squared),
        "idiosyncratic_increment_log_coefficient_squared_exact": pair(idio_squared),
        "undiscounted_cap_also_bounds_discounted_payoff_exact": pair(cap),
        "coordinate_variation_upper_exact": pair(variation),
        "independently_derived_midpoint_grid_bias_upper_exact": pair(bound),
        "headroom_exact": pair(headroom),
        "ideal_law_term_fits_headroom": bound <= headroom,
        "continuous_ideal_scalar_grid_theorem_only": True,
        "all_native_loader_and_full_price_transfer_guards_preserved": True,
        "native_financial_error_bound": None,
        "loader_or_circuit_adopted": False,
        "complete_continuous_price_certified": False,
        "second_discount_applied": False,
        "financial_price_observations_or_gate_replays": 0,
    }


def step_midpoint_profile(values):
    """Exact quadrature of right-continuous half-cell steps, including strict ties."""
    values = tuple(rational(value) for value in values)
    if not values or len(values) % 2:
        raise ValueError("Two half-cell values per cell required")
    cells = len(values) // 2
    integral = sum(values) / (2 * cells)
    midpoint = sum(values[1::2]) / cells
    variation = sum(abs(right - left) for left, right in zip(values, values[1:]))
    return {
        "integral": integral,
        "midpoint": midpoint,
        "variation": variation,
        "absolute_error": abs(integral - midpoint),
        "midpoint_BV_upper": variation / (2 * cells),
        "strict_midpoint_uses_right_value": True,
    }


def knockout_variation(prefix, cap):
    """An increasing bounded prefix followed by the strict-knockout zero value."""
    prefix, cap = tuple(map(rational, prefix)), rational(cap)
    if not prefix or cap < 0 or any(not 0 <= value <= cap for value in prefix):
        raise ValueError("Nonnegative cap and bounded prefix required")
    if any(right < left for left, right in zip(prefix, prefix[1:])):
        raise ValueError("Monotone surviving payoff required")
    return prefix[-1] - prefix[0] + prefix[-1]


def verify(frozen):
    for name, expected in frozen.items():
        if sha(ROOT / name) != expected:
            raise ValueError("Frozen provenance changed: " + name)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("New prospective independent audit receipt required")
    if not read(SOURCE / "summary.json")["passed"]:
        raise ValueError("Completed source theorem receipt required")
    receipt = read(SOURCE / "manifest.json")
    frozen = {
        name.replace("\\", "/"): digest
        for field in ("files", "frozen_inputs")
        for name, digest in receipt[field].items()
    }
    frozen[relative(SOURCE / "manifest.json")] = sha(SOURCE / "manifest.json")
    for name in CODE:
        path = ROOT / "research/limitation_program_20261001" / name
        frozen[relative(path)] = sha(path)
    frozen[relative(BUILDER)] = sha(BUILDER)
    frozen[relative(Path(__file__).with_name("progress.py"))] = sha(
        Path(__file__).with_name("progress.py")
    )
    for case in CASES:
        path = PROGRAM / "G0_run003" / (case + "_task.json")
        frozen[relative(path)] = sha(path)
    verify(frozen)
    output.mkdir()
    for name in CODE:
        shutil.copy2(ROOT / "research/limitation_program_20261001" / name, output / name)
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "before_tests_and_independent_certificate_reconciliation": True,
        "source": relative(SOURCE),
        "cases": list(CASES),
        "fixed_uniform_bits": 32,
        "same_ideal_law_and_precision_as_source": True,
        "independent_proof": (
            "Check original economic AST/strict barrier and task; derive positive "
            "coordinate coefficients, payoff cap40, variation80, midpoint BV and "
            "independent product telescope using exact rational algebra without "
            "calling law_bound. Exact small step-function fixtures are algebraic only."
        ),
        "native_loader_or_full_price_adoption": False,
        "original_source_fixtures_counted_again": False,
        "financial_price_observations_or_quantum_replays": 0,
        "process_cpu_limit_seconds": 120,
        "frozen_inputs": frozen,
        "python": sys.version,
        "executable": sys.executable,
    }
    save(output / "protocol.json", protocol)
    print("Independent scalar-grid theorem audit prospectively frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    if (output / "summary.json").exists():
        raise FileExistsError("Independent audit already completed")
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    started = time.process_time()
    rc = pytest.main(
        [
            str(ROOT / "research/limitation_program_20261001/test_audit_quantile_grid.py"),
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml=" + str(output / "tests.xml"),
        ]
    )
    if rc:
        save(output / "summary.json", {"passed": False, "fixture_return_code": int(rc)})
        write_manifest(output, protocol)
        raise AssertionError("Frozen independent scalar-grid fixtures failed")
    builder_audit = audit_builder_contract(BUILDER)
    rows = []
    for case in protocol["cases"]:
        row = audit_grid_certificate(
            read(SOURCE / (case + "_certificate.json")),
            read(PROGRAM / "G0_run003" / (case + "_task.json")),
            BUILDER,
        )
        row["source_certificate_path"] = relative(SOURCE / (case + "_certificate.json"))
        row["source_certificate_sha256"] = sha(SOURCE / (case + "_certificate.json"))
        save(output / (case + "_audit.json"), row)
        rows.append(row)
    elapsed = time.process_time() - started
    if elapsed > protocol["process_cpu_limit_seconds"]:
        raise TimeoutError("Independent scalar-grid audit CPU limit")
    suites = ET.parse(output / "tests.xml").getroot()
    tests = sum(int(suite.attrib["tests"]) for suite in suites.iter("testsuite"))
    save(
        output / "summary.json",
        {
            "passed": True,
            "local_only": True,
            "independent_ideal_scalar_midpoint_grid_theorem_audit": True,
            "new_independent_fixtures_passed": tests,
            "original_source_fixture_count_added": 0,
            "builder_economic_template_audit": builder_audit,
            "independent_analytic_proof": THEOREM,
            "cases": rows,
            "conditional_alternative_law_bounds_only": True,
            "accepted_Box_Muller_law_certified": False,
            "native_inverse_CDF_financial_arithmetic_or_loader_certified": False,
            "full_G2_closed": False,
            "quantum_advantage_established": False,
            "original_B4_B8_price_observations_or_gate_replays": 0,
            "elapsed_cpu_seconds": elapsed,
        },
    )
    write_manifest(output, protocol)
    print(
        "Independent ideal scalar-grid theorem audit passed; implementation remains open",
        flush=True,
    )


def write_manifest(output, protocol):
    files = {
        relative(path): sha(path)
        for path in Path(output).rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    save(
        Path(output) / "manifest.json",
        {
            "files": files,
            "frozen_inputs": protocol["frozen_inputs"],
            "manifest_self_hash_excluded": True,
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
