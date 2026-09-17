"""Fresh-process regeneration plus an additional positive-flag workspace check."""

import argparse
import hashlib
import json
from pathlib import Path
from .arithmetic_plan import raw_plan
from .decimal_enclosure import Interval
from .fixed_exp_budget import evaluate_integer
from .normal_loader_budget import loader_plan
from .reversible_fixed_point import Program, basis, raw_payoff_flag
from .run_arithmetic_development import CONFIG, INPUT, SOURCES
from .storage import ROOT, sha256, write_json


def verify(archive, receipt):
    archive = Path(archive)
    planned = json.loads((archive/"planned.json").read_text())
    complete = json.loads((archive/"complete.json").read_text())
    expected_files = {"planned.json", "arithmetic_plan.json", "loader.json", "encoding_bounds.json",
                      "prospective_bias.json", "resources.json", "basis_checks.json"}
    if set(complete["sha256"]) != expected_files or {p.name for p in archive.iterdir()} != expected_files | {"complete.json"}:
        raise ValueError("archive inventory mismatch")
    if planned["config"] != CONFIG or set(planned["source_sha256"]) != set(SOURCES+(INPUT,)):
        raise ValueError("configuration/source inventory mismatch")
    for name, expected in complete["sha256"].items():
        if sha256(archive/name) != expected:
            raise ValueError("artifact checksum mismatch")
    for name, expected in planned["source_sha256"].items():
        if sha256(ROOT/name) != expected:
            raise ValueError("source checksum mismatch")
    case = json.loads((ROOT/INPUT).read_text())
    discount = (-Interval(str(case["basket"]["rate"]))*Interval(str(case["basket"]["maturity"]))).exp()
    plan = raw_plan(case["means"], case["factor"], discount=discount,
                    **{k: CONFIG[k] for k in ("cutoff", "normal_bits", "fraction_bits", "width", "degree")})
    loader = loader_plan(CONFIG["normal_bits"], CONFIG["cutoff"])
    for name, regenerated in (("arithmetic_plan.json", plan), ("loader.json", loader)):
        if json.loads(json.dumps(regenerated)) != json.loads((archive/name).read_text()):
            raise ValueError("deterministic plan regeneration mismatch")
    print("Plans regenerated exactly; rebuilding gate program", flush=True)
    p = Program(compact=True)
    inputs, selector, flag = p.register(plan["normal_qubits"]), p.register(plan["selector_bits"]), p.register(1)
    raw_payoff_flag(p, inputs, selector, flag[0], plan["width"], plan["fraction_bits"],
                    plan["affine_rows"], plan["exp_budget"]["coefficients"], plan["strike_sum"])
    recorded = json.loads((archive/"resources.json").read_text())
    digest = hashlib.sha256(p.gates.data.tobytes()).hexdigest()
    if digest != recorded["gate_record_sha256"] or p.resources() != recorded["payoff_compute_flag_uncompute"]:
        raise ValueError("gate regeneration mismatch")
    print("Gates regenerated exactly; testing a nonzero payoff/positive flag", flush=True)
    packed = (1 << plan["normal_qubits"])-1
    logs = [a+sum(cs) for a, cs in plan["affine_rows"]]
    payoff = max(sum(evaluate_integer(x, plan["exp_budget"]["coefficients"], plan["fraction_bits"]) for x in logs)-plan["strike_sum"], 0)
    if not payoff > 0:
        raise ArithmeticError("positive-flag test was vacuous")
    initial = basis(inputs, packed)
    if p.run(initial) != initial | basis(flag, 1):
        raise ArithmeticError("positive flag or clean workspace failed")
    # Preserve a receipt only after success; archive is never edited.
    write_json(receipt, dict(archive=str(archive), archive_manifest_sha256=sha256(archive/"complete.json"),
                            verifier_sha256=sha256(Path(__file__)), deterministic_plans_equal=True,
                            emitted_gate_hash_equal=True, resources_equal=True,
                            additional_positive_flag_clean_workspace=True, payoff_integer=payoff,
                            quantum_statevector=False, independent_human_review=False,
                            qualification="artifact hashes checked; plans and gates regenerated, encoding bound formulas not independently rederived here"))
    print("Verification passed", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("receipt")
    args = parser.parse_args()
    verify(args.archive, args.receipt)
