"""Exclusive deterministic development audit; never unlocks confirmation seeds."""

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .arithmetic_plan import raw_plan
from .asian_basket import Basket
from .decimal_enclosure import Interval
from .encoding_enclosure import base_enclosure, at_precision
from .fixed_exp_budget import evaluate_integer
from .normal_loader_budget import loader_plan
from .reversible_fixed_point import Program, basis, raw_payoff_flag
from .storage import ROOT, sha256, write_json


SOURCES = tuple("research/journal_sprint/" + name for name in (
    "reversible_fixed_point.py", "fixed_exp_budget.py", "arithmetic_plan.py",
    "normal_loader_budget.py", "run_arithmetic_development.py", "decimal_enclosure.py",
    "encoding_enclosure.py", "asian_basket.py", "storage.py", "price_contract.py",
    "encoding_decision.py")) + ("docs/journal_sprint/REVERSIBLE_ARITHMETIC_PROTOCOL.md",)
INPUT = "results/journal_sprint/w13_encoding_v1/case_3.json"
CONFIG = dict(case=3, cutoff=4, normal_bits=10, fraction_bits=24, width=40, degree=32,
              scope="development: raw, exact logical controlled-RY/X/CX/CCX/H")


def run(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES+(INPUT,)}
    write_json(path/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               python=platform.python_version(), started_utc=datetime.now(timezone.utc).isoformat(),
               git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               working_diff=subprocess.check_output(["git", "status", "--short", "--untracked-files=no"], cwd=ROOT, text=True)))
    try:
        case = json.loads((ROOT/INPUT).read_text())
        basket = Basket(**case["basket"])
        discount = (-Interval(str(basket.rate))*Interval(str(basket.maturity))).exp()
        plan = raw_plan(case["means"], case["factor"], discount=discount,
                        **{k: CONFIG[k] for k in ("cutoff", "normal_bits", "fraction_bits", "width", "degree")})
        if not plan["overflow_safe"]:
            raise ArithmeticError("development word width failed certificate")
        write_json(path/"arithmetic_plan.json", plan)
        loader = loader_plan(CONFIG["normal_bits"], CONFIG["cutoff"])
        write_json(path/"loader.json", loader)
        model = dict(means=case["means"], factor=case["factor"], expected_control=0)
        enclosure = at_precision(base_enclosure(basket, model, CONFIG["cutoff"], "raw"), CONFIG["normal_bits"])
        write_json(path/"encoding_bounds.json", enclosure)
        preparation = Interval(plan["sensitivity_upper"])*4*Interval(loader["operator_error_upper"])
        bias = Interval(enclosure["partial_sum"]["upper"]) + Interval(plan["arithmetic_price_error_upper"]) + preparation
        write_json(path/"prospective_bias.json", dict(total_upper=str(bias.hi),
                   preparation_price_error_upper=str(preparation.hi),
                   ideal_payoff_flag_error=0, physical_synthesis_error=None,
                   application_admitted=False, confirmation_unblocked=False,
                   qualification="analytic logical-design bound, not a validated PriceContract or delivery interval"))
        print("Bounds generated; building explicit compact gate program", flush=True)
        p = Program(compact=True)
        inputs, selector, flag = p.register(plan["normal_qubits"]), p.register(plan["selector_bits"]), p.register(1)
        raw_payoff_flag(p, inputs, selector, flag[0], plan["width"], plan["fraction_bits"],
                        plan["affine_rows"], plan["exp_budget"]["coefficients"], plan["strike_sum"])
        resources = p.resources()
        # Same permutation is its own inverse once work is clean. Full gate
        # inverse always has identical counts even away from clean workspace.
        write_json(path/"resources.json", dict(payoff_compute_flag_uncompute=resources,
                   inverse_same_counts=True, logical_gate_count=len(p.gates),
                   gate_record_sha256=hashlib.sha256(p.gates.data.tobytes()).hexdigest(),
                   gate_record_byteorder=__import__("sys").byteorder,
                   gate_record_itemsize=p.gates.data.itemsize,
                   gaussian_controlled_ry=4*len(loader["nodes"]), selector_h=plan["selector_bits"],
                   full_A_compiled=False, hardware_transpiled=False,
                   qualification="actual emitted logical payoff gates; loading, reflections and hardware decomposition separate"))
        print("Gate program counted; checking two basis states including workspace", flush=True)
        checks = []
        for packed, u in ((0, 0), ((1 << plan["normal_qubits"])-1, (1 << plan["selector_bits"])-1)):
            logs = [a+sum(((packed >> i)&1)*c for i, c in enumerate(cs)) for a, cs in plan["affine_rows"]]
            payoff = max(sum(evaluate_integer(x, plan["exp_budget"]["coefficients"], plan["fraction_bits"]) for x in logs)-plan["strike_sum"], 0)
            initial = basis(inputs, packed) | basis(selector, u)
            actual = p.run(initial)
            expected = initial ^ basis(flag, int(u < payoff))
            if actual != expected:
                raise ArithmeticError("large basis/workspace check failed")
            checks.append(dict(packed_input=packed, selector=u, payoff_integer=payoff, passed=True))
        write_json(path/"basis_checks.json", dict(checks=checks, exhaustive=False, statevector=False))
        if hashes != {name: sha256(ROOT/name) for name in hashes}:
            raise RuntimeError("source changed during audit")
        write_json(path/"complete.json", dict(finished_utc=datetime.now(timezone.utc).isoformat(),
                   sha256={f.name: sha256(f) for f in sorted(path.iterdir()) if f.is_file()}))
        print(json.dumps(dict(bias_upper=str(bias.hi), resources=resources, confirmation_unblocked=False)), flush=True)
    except BaseException as error:
        write_json(path/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
