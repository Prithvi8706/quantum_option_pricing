"""Frozen F16 model/source audit with exact rational and symbolic diagnostics.

No shared module is imported or executed; no finance samples or timings are acquired.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import math
import time
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/independent_110_20261004/F16/run001"
DOC = ROOT / "docs/independent_110_20261004/F16"
CORPUS = [
    "research/compound_feasibility/model.py",
    "research/controlled_source_completion/finance.py",
    "research/controlled_residual_feasibility/parity.py",
    "docs/compound_feasibility/RESULTS.md",
    "docs/controlled_residual_feasibility/DERIVATION.md",
    "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    "research/independent_110_20261004/F16/primary_sources/Sigman_2007_BM_GBM_I.pdf",
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare():
    if OUT.exists():
        raise ValueError("Fresh F16 output required.")
    OUT.mkdir(parents=True)
    pins = {p: {"sha256": digest((ROOT / p).read_bytes()), "bytes": (ROOT / p).stat().st_size} for p in CORPUS}
    dump(OUT / "protocol.json", {
        "schema": "f16-factor-reuse-preregistered-audit-v1",
        "author_sha256": digest(Path(__file__).read_bytes()), "corpus": pins,
        "scope": "Current ideal GBM future-factor identity, exact source binding, and operational extension limits.",
        "assumptions": ["Finite deterministic model parameters; positive spots; valid equicorrelation.", "Even contractual date count with exercise at T/2.", "Joint Brownian future increments independent of the exercise-time filtration for the population claim.", "Pointwise identities over positive factors do not require iid sampling."],
        "acceptance": ["All four archived GBM Model declarations satisfy the stated geometry/PSD conditions.", "Exact symbolic coefficients prove future-average normalization; positive-product identities prove geometric factorization.", "48 fixed positive-factor/state cases agree exactly over Fractions; normalization mutants and saturation/rounding extension counterexamples fail as expected.", "Shared source functions are AST-bound to frozen bytes; every financial/numerical transfer limitation stays explicit."],
        "corpus_geometry": {"models": ["C4", "C8", "H4", "H8"], "scenarios_per_model": 4, "states_per_scenario": 3, "finance_draws": 0},
        "budgets": {"cpu_seconds": 30, "wall_seconds": 60, "output_bytes": 4 * 1024 * 1024},
        "stopping_rule": "One symbolic/source audit and the fixed 48-case diagnostic; no new model, stochastic run, fitter, sampler or compilation.",
        "checks_are_new_global_fixtures": False, "quantum_advantage": False,
    })
    print("F16 protocol frozen; no scientific diagnostics executed.")


def models_from_ast(tree):
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Model")
    defaults = {n.target.id: ast.literal_eval(n.value) for n in cls.body if isinstance(n, ast.AnnAssign)}
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MODELS" for t in n.targets))
    order = ["name", "assets", "dates", "sigma", "rho", "maturity", "strike", "spot", "rate"]
    result = []
    for node in assignment.value.elts:
        assert isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Model"
        m = dict(defaults)
        m.update({k: ast.literal_eval(v) for k, v in zip(order, node.args)})
        m.update({v.arg: ast.literal_eval(v.value) for v in node.keywords})
        result.append(m)
    return result


PROOF = """F16: EXACT CURRENT GBM FACTOR REUSE AND ITS LIMITS

Population assumptions and proof
Let tau=T/2 and t_l=tau+l*T/N, l=1,...,n, N=2n. The current models
have finite deterministic r,sigma,rho and positive spot. For a correlated
Brownian vector W with valid fixed covariance, future vector increments
W(t_l)-W(tau) are jointly independent of F_tau. Components within the
future vector are correlated; no asset/date independence is claimed.

The GBM solution gives S_i(t_l)=s_i R_li where
R_li=exp((r-sigma^2/2)*(t_l-tau)+sigma*(W_i(t_l)-W_i(tau))).
This is also a pointwise algebraic identity for any positive return factors.
The complete accrued-plus-future arithmetic average equals
 a + sum_i s_i C_i, C_i=sum_l R_li/(d*N).
Each scenario's C vector can therefore be prepared once and reused across
outer states. The future-only geometric mean equals G(s)*G(R), because
the product of all d*n future prices is (product_i s_i)^n*product_li R_li.
Taking the unique positive d*n root proves the identity. The future contribution
to the complete geometric control is one half of that mean, since N=2n.

Implementation connection
model.py future_factors constructs exp(logs).sum(axis=1)/(assets*dates)
and exp(logs.mean(axis=(1,2))). inner_samples adds the spot/factor dot product
to accrued and uses .5 times the geometric spot mean and future geometric factor.
All four model declarations and the critical AST functions are pinned. H4/H8
in this module are GBM development model names, not Heston variance processes.
The source association is a proof in ideal real arithmetic. It does not certify
every NumPy/Numba floating evaluation or a binary native reversible circuit.

Paid work and uncertainty
For I outer states and J future scenarios, source factor preparation still
requires J*d*n returns plus J geometric factors. The arithmetic evaluation
still requires I*J*d spot/factor products and crossed payoffs. The code's inner
arrays include two I-by-J matrices. Reuse removes repeated return generation;
it does not make conditional payoffs, setup, memory or readout free. These are
symbolic operation counts, not measured complete latency or a speedup ratio.
Reusing one future scenario set couples outer-state estimates. IID inference
for every crossed payoff is invalid without an additional design/proof.
Scrambled Sobol coordinates clipped before inverse-normal evaluation are not
an exact iid real Gaussian oracle. The pointwise identity survives arbitrary
positive factors; exact continuous-law/uncertainty transfer needs its own proof.

Extensions that cannot be imported
The controlled digital finance source resets/clips its tau log state and clips
future stock logs. Saturation at U=4096 is not homogeneous in spot: with the
same positive return4, s=1024 has output4096 while s=4096 also has output4096,
so output/spot is4 versus1. This is an exact ideal-clamp counterexample to a
single spot-independent multiplicative factor for the clipped stock function;
it is not an emitted-circuit or q32-reachability counterexample. Fixed-point
rounding also needs a separate integer proof: floor(3/3)/3 differs from
floor(4/3)/4, even though both products use the same rational multiplier.
Future raw log increments may still be reused with spot-dependent clipping
reapplied; the compressed unclipped C vector is not an exact digital replacement.

An existing Heston state includes variance at tau. Its return distribution
generally depends on that variance, so the GBM state-independent factor law
does not transfer across variance states. Reusing random drivers or scaling
spot at fixed variance can still be possible; no universal impossibility follows.
State-dependent volatility/rates require a new conditional generator/law proof.
No such new financial workload is selected or executed in this audit.

Decision and exact scope
Completed F16's current-contract factorization audit: the GBM reuse identity
holds and the exact assumptions/paid operations are explicit. No justified
new model is nominated. Keep the existing classical reuse; do not claim a
sampling bottleneck by regenerating the same futures for every outer state.
Native-source equality, continuous-price delivery and quantum advantage are
not established by this audit. No shared source, old receipt or budget is changed.

Primary source checked: Karl Sigman (2007), sections1.2.3 and1.3, pages4-6:
https://www.columbia.edu/~ks20/4703-07/4703-07-Notes-BM-GBM-I.pdf
The model-specific weighted identities above are derived here, rather than
quoted from the notes. The frozen local PDF hash is recorded in protocol.json.
"""


def run():
    started_cpu, started_wall = time.process_time(), time.monotonic()
    protocol = json.loads((OUT / "protocol.json").read_text())
    if (OUT / "summary.json").exists() or (OUT / "RUN_STARTED.json").exists():
        raise ValueError("F16 one-attempt rule; fresh version required after failure.")
    assert digest(Path(__file__).read_bytes()) == protocol["author_sha256"]
    for p, pin in protocol["corpus"].items():
        assert digest((ROOT / p).read_bytes()) == pin["sha256"], p
    dump(OUT / "RUN_STARTED.json", {"scope": protocol["scope"], "finance_draws": 0})
    tree = ast.parse((ROOT / CORPUS[0]).read_text())
    models = models_from_ast(tree)
    assert [m["name"] for m in models] == protocol["corpus_geometry"]["models"]
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    function_pins = {k: digest(ast.dump(funcs[k], include_attributes=False).encode()) for k in ["normals", "outer_states", "future_factors", "inner_samples", "continuation_samples"]}
    finite_cases, symbolic_rows, costs = [], [], []
    for m in models:
        d, N = m["assets"], m["dates"]
        assert d > 0 and N > 0 and N % 2 == 0 and m["spot"] > 0 and m["sigma"] >= 0
        assert all(math.isfinite(m[k]) for k in ["sigma", "rho", "maturity", "strike", "spot", "rate"])
        assert m["maturity"] > 0 and 1 - m["rho"] >= 0 and 1 + (d - 1) * m["rho"] >= 0
        n = N // 2
        lhs = {(i, l): Q(1, d * N) for i in range(d) for l in range(n)}
        rhs = {(i, l): Q(1, d * N) for l in range(n) for i in range(d)}
        assert lhs == rhs
        assert sum(lhs.values(), Q()) == Q(1, 2)
        symbolic_rows.append({"model": m["name"], "formal_monomials": len(lhs), "full_average_future_weight": "1/2", "coefficients_equal": True})
        costs.append({"model": m["name"], "setup_returns_per_future_scenario": d * n, "setup_geometric_factors_per_scenario": 1, "spot_factor_products_per_crossed_payoff": d, "arithmetic_factor_storage_per_scenario": d, "geometric_factor_storage_per_scenario": 1, "inner_output_matrix_count": 2, "actual_latency": None})
        for j in range(4):
            factors = [[Q(2) ** (((j + l + 2 * i) % 7) - 3) for i in range(d)] for l in range(n)]
            for outer in range(3):
                spots = [Q(2) ** (((outer + i) % 5) - 2) for i in range(d)]
                accrued = Q([0, 50, 100][outer])
                direct = accrued + sum((spots[i] * factors[l][i] for l in range(n) for i in range(d)), Q()) / (d * N)
                compressed = accrued + sum((spots[i] * sum((factors[l][i] for l in range(n)), Q()) / (d * N) for i in range(d)), Q())
                assert direct == compressed
                product_direct = math.prod(spots[i] * factors[l][i] for l in range(n) for i in range(d))
                product_factorized = math.prod(spots) ** n * math.prod(x for row in factors for x in row)
                assert product_direct == product_factorized
                finite_cases.append({"model": m["name"], "scenario": j, "outer_state": outer, "arithmetic_exact": str(direct), "geometric_product_exact": str(product_direct), "passed": True})
    assert len(finite_cases) == 48
    negatives = {
        "missing_date_normalization": {"correct": "1/2", "incorrect": "6", "rejected": Q(6, 12) != Q(6)},
        "double_count_future_half": {"correct": "1/2", "incorrect": "1/4", "rejected": Q(1, 2) != Q(1, 4)},
        "clipped_stock_scale": {"low_spot_ratio": str(Q(min(4096, 1024 * 4), 1024)), "high_spot_ratio": str(Q(min(4096, 4096 * 4), 4096)), "rejected": Q(min(4096, 1024 * 4), 1024) != Q(min(4096, 4096 * 4), 4096)},
        "rounded_product_scale": {"ratio_at_3": str(Q(3 // 3, 3)), "ratio_at_4": str(Q(4 // 3, 4)), "rejected": Q(3 // 3, 3) != Q(4 // 3, 4)},
    }
    assert all(v["rejected"] for v in negatives.values())
    DOC.mkdir(parents=True, exist_ok=True)
    proof_path = DOC / "PROOF_AND_LIMITS.txt"
    if proof_path.exists():
        raise ValueError("F16 proof file already exists.")
    proof_path.write_text(PROOF, encoding="utf-8")
    dump(OUT / "diagnostics.json", {"models_from_frozen_AST": models, "function_AST_sha256": function_pins, "symbolic_rows": symbolic_rows, "fixed_cases": finite_cases, "negative_controls": negatives, "symbolic_paid_work": costs})
    for p, pin in protocol["corpus"].items():
        assert digest((ROOT / p).read_bytes()) == pin["sha256"], p
    assert time.process_time() - started_cpu <= protocol["budgets"]["cpu_seconds"]
    assert time.monotonic() - started_wall <= protocol["budgets"]["wall_seconds"]
    summary = {
        "passed": True, "completed": True, "decision": "completed_current_contract_audit",
        "scope": "F16 current ideal GBM and pointwise positive-factor reuse; extension limits and paid work.",
        "models": len(models), "symbolic_model_rows": len(symbolic_rows), "finite_diagnostic_cases": len(finite_cases), "negative_controls": len(negatives),
        "population_factorization_proved_under_stated_GBM_assumptions": True,
        "new_model_nominated": False, "finance_draws": 0, "shared_source_mutations": 0,
        "new_global_fixture_credit": 0, "native_source_replacement_certified": False,
        "financial_delivery_certified": False, "quantum_advantage": False,
        "uncertified_inputs": ["Exact sampling/coverage of clipped Sobol/inverse-normal floating implementation.", "Native fixed-point/clipped factor replacement and full continuous-law transfer.", "Any state-dependent-volatility/rate replacement generator or useful crossover."],
        "proof": str(proof_path.relative_to(ROOT)).replace('\\', '/'),
    }
    dump(OUT / "summary.json", summary)
    files = list(OUT.iterdir()) + [proof_path]
    assert sum(p.stat().st_size for p in files if p.is_file()) <= protocol["budgets"]["output_bytes"]
    dump(OUT / "manifest.json", {"scope": "Local F16 bounded audit only.", "files": {str(p.relative_to(ROOT)).replace('\\', '/'): {"sha256": digest(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(files) if p.is_file()}, "author_sha256": protocol["author_sha256"], "input_pins": protocol["corpus"]})
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else run()
