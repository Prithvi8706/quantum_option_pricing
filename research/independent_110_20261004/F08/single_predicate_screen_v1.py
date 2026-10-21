"""Exact finite-law single-predicate proof diagnostics; no sampler or finance draws."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import time
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/independent_110_20261004/F08/run001"
DOC = ROOT / "docs/independent_110_20261004/F08"
AUTHOR = Path(__file__).resolve()
CORPUS = ["docs/limitation_audit_20261001/implementation_plan/roadmap.json",
          "docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md",
          "research/limitation_audit_20261001/experiment_bounded_probabilities.py",
          "results/limitation_audit_20261001/bounded_probabilities_v1/summary.json"]
A_VALUES = [Q(x) for x in [0, 1, 2, 3, 5, 8, 13]]
LAWS = [[Q(1, 7)] * 7, [Q(x, 18) for x in [0, 1, 2, 0, 3, 5, 7]], [Q(1, 2)] + [Q(0)] * 5 + [Q(1, 2)]]
STRIKES = [Q(x) for x in range(16)] + [Q(1, 2), Q(3, 2), Q(13, 2)]
M_VALUES = [1, 2, 4, 16, 64]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair(x):
    return [x.numerator, x.denominator]


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def prepare():
    if OUT.exists():
        raise ValueError("Fresh F08 screen required.")
    OUT.mkdir(parents=True)
    dump(OUT / "protocol.json", {"schema": "f08-one-predicate-preregistration-v1",
        "author_sha256": sha(AUTHOR), "corpus": {p: sha(ROOT / p) for p in CORPUS},
        "law_values": [pair(a) for a in A_VALUES], "law_count": len(LAWS),
        "survival_masks": 128, "strike_count": len(STRIKES), "M_values": M_VALUES,
        "case_count": len(LAWS) * 128 * len(STRIKES),
        "scope": "General finite-law identity and finite-uniform rounding; one predicate and reciprocal normalization ledgers on the archived development case.",
        "assumptions": ["A>=0, K>=0, deterministic survival indicator; finite probability weights sum to1.", "m=E_P A is known exactly for the rational diagnostic laws.", "A continuous independent U gives the exact one-predicate identity; a fixed finite grid must pay its rounding bias.", "Production interval/quantum preparation/source/statistical constants are not supplied by the toy or archived floating m."],
        "acceptance": ["All masks/strikes/laws exactly reproduce reciprocal and continuous-uniform conditional probabilities.", "For M=1,2,4,16,64, fixed-grid error is nonnegative and bounded by m/M; M<=4 tails agree with explicit enumeration.", "A=0, m=0, K=0, A=K and strict finite-uniform endpoints are covered.", "Archived losing two-probability and shifted-grid branches stay closed; absent full99% schedule/error inputs stay unresolved.", "Sampler compilation requires a certified full99% cost >=20% below direct estimation, not a normalization-only calculation."],
        "budgets": {"cpu_seconds": 90, "wall_seconds": 180, "output_bytes": 16 * 1024 * 1024},
        "stopping_rule": "One fixed exhaustive rational grid and the two named candidate ledgers once; no sampler compilation, Gaussian draw, retuning or old failed-branch retry.",
        "finance_draws": 0, "new_global_fixture_credit": 0})
    print("F08 rational grid and bounded two-ledger screen frozen.")


PROOF = """F08: FINITE SIZE-BIASED LAW, ONE PREDICATE AND ROUNDING

For a finite source Omega with probabilities p_x, A_x>=0 and survival I_x,
let m=sum_x p_x A_x. If m>0 define Q_A(x)=p_x A_x/m. For K>=0,
 E_P[(A-K)+ I] = m E_Q[(1-K/A)+ I]
               = m P_(Q times Uniform[0,1])(U A>K and I).
A=0 states have zero Q mass and contribute zero to the original payoff.
The reciprocal expression is defined as0 there. If m=0 then A=0 P-almost
surely and the original price is0; Q_A is undefined and is not constructed.
These identities follow by cancelling A in each finite summand. They are
not a claim that a coherent Q sampler, reciprocal or variable-width uniform
register is free.

For a fixed grid U=j/M, j=1,...,M, the strict predicate j*A>K*M has
c_M(A,K)=max(0,min(M,M-floor(K*M/A))) accepted indices for A>0.
Thus 0<=c_M/M-(1-K/A)+<=1/M. Multiplication by m and summation over
Q gives price overstatement between0 and m/M (before discount). Exact
event endpoints include j*A=K*M, which is rejected. Replacing > by >=
without an endpoint proof changes the finite-grid event.
For integer A,K an alternative conditional register J uniform on1,...,A
would give exactly (A-K)+/A; its size/state dependence and preparation must
be explicitly implemented. It is not the fixed M register used here.

Error and normalization ledger
Let discount and m have certified intervals D_L..D_U and m_L..m_U,
and estimates Dhat,mhat within them. A conservative dollar budget is
 D_U*(m_U*(e_stat + eta_preparation + eta_arithmetic + eta_synthesis
                + 1/M) + e_m) + m_U*e_discount + b_law <= epsilon.
Here eta terms are explicit bounds on event-probability errors, not observed
sample differences. A total-variation preparation certificate bounds event
error; a coherent operator-error/synthesis certificate must first imply such
a bound over the complete estimator. e_m is the normalizer error. The
reciprocal alternative substitutes its separately certified evaluation error
for1/M. Failure probability has a separate joint99% estimator/acquisition/
hardware allocation. Missing terms are unresolved, never set to zero.
The archived floating normalizer103.04884928817364 is a diagnostic value,
not a rigorous production m interval. No full G2 or G3 budget is issued here.

Retained evidence and screen
The previous two-probability finite identity/mixture result is retained
without rerunning or crediting its131072 samples. Its equal-cost inverse-
precision screen was10.15187018795802 times direct estimation; its naive
shifted finite-grid branch changed the law. Both losing shortcuts stay closed.
For that SAME archived barrier development case, the direct bounded range is
D*(140-100), whereas the one-predicate/reciprocal scale is D*m. Under the
explicit equal-source/equal-estimator-constant diagnostic assumption,
the ratio is m/40=2.576221232204341. This normalization-only change cannot
meet the20% improvement gate. It is not a measured ratio, a certified
production m bound, a universal source-cost lower bound or a B4/B8 result.
A truly cheaper preparation/predicate would need a new quantified complete
cost premise; none is supplied. No sampler is emitted.

Both candidate ledgers charge normalization setup, Q preparation/inverse,
Gaussian/path stock work, arithmetic or predicate, every barrier observation,
cleanup, estimator confidence/repetition, rotations/synthesis and readout.
Their production cost/error fields remain null. Keep direct bounded-payoff
estimation and the exact mathematical identity. No financial contract,
shared progress/source or quantum-advantage claim is changed by this screen.
"""


def run():
    tc, tw = time.process_time(), time.monotonic()
    p = json.loads((OUT / "protocol.json").read_text())
    if (OUT / "RUN_STARTED.json").exists():
        raise ValueError("F08 one-attempt rule.")
    assert sha(AUTHOR) == p["author_sha256"]
    for path, expected in p["corpus"].items():
        assert sha(ROOT / path) == expected
    dump(OUT / "RUN_STARTED.json", {"finance_draws": 0})
    checks = []
    for law_index, law in enumerate(LAWS):
        assert sum(law) == 1 and all(x >= 0 for x in law)
        m = sum(x * a for x, a in zip(law, A_VALUES))
        assert m > 0
        tilted = [x * a / m for x, a in zip(law, A_VALUES)]
        assert sum(tilted) == 1 and tilted[0] == 0
        for mask in range(128):
            survival = [bool(mask & (1 << i)) for i in range(7)]
            for K in STRIKES:
                direct = sum(prob * max(a - K, Q()) * int(alive) for prob, a, alive in zip(law, A_VALUES, survival))
                reciprocal = m * sum(prob * (max(1 - K / a, Q()) if a else Q()) * int(alive) for prob, a, alive in zip(tilted, A_VALUES, survival))
                assert direct == reciprocal
                grid_errors = []
                for M in M_VALUES:
                    predicate_p = Q()
                    for prob, a, alive in zip(tilted, A_VALUES, survival):
                        count = 0 if a == 0 else max(0, min(M, M - math.floor(K * M / a)))
                        if M <= 4:
                            assert count == sum(j * a > K * M for j in range(1, M + 1))
                        predicate_p += prob * Q(count, M) * int(alive)
                    error = m * predicate_p - direct
                    assert 0 <= error <= m / M
                    grid_errors.append(pair(error))
                checks.append({"law": law_index, "survival_mask": mask, "strike": pair(K), "direct_price": pair(direct), "fixed_grid_overstatement": grid_errors, "passed": True})
        assert time.process_time() - tc <= p["budgets"]["cpu_seconds"]
        assert time.monotonic() - tw <= p["budgets"]["wall_seconds"]
    assert len(checks) == p["case_count"]
    zero_cases = [{"strike": pair(k), "price": [0, 1], "Q_defined": False} for k in STRIKES]
    assert all(max(Q() - k, Q()) == 0 for k in STRIKES)
    old = json.loads((ROOT / CORPUS[-1]).read_text())
    assert old["passed"] and old["simple_query_screen"]["decomposition_over_direct"] > 1
    normalization_ratio = Q(str(old["finite_normalization"])) / 40
    assert normalization_ratio > Q(4, 5)
    candidates = []
    for name in ["one_predicate_fixed_uniform", "bounded_reciprocal"]:
        candidates.append({"candidate": name, "source_family": "archived_two_asset_128x128_barrier_development",
            "diagnostic_equal_cost_normalization_ratio_exact": pair(normalization_ratio),
            "diagnostic_equal_cost_twenty_percent_gate": False,
            "complete_actual99pct_cost": None, "certified_production_normalizer_interval": None,
            "certified_sampler_error": None, "certified_arithmetic_error": None,
            "certified_law_error": None, "sampler_compilation_authorized": False,
            "cost_terms": ["normalizer setup", "finite tilted state preparation and inverse", "all Gaussian/path stock work", "all barrier dates", "predicate or reciprocal", "cleanup", "confidence/repetitions", "rotation synthesis", "readout"],
            "decision": "normalization_only_equal_cost_screen_rejected_full_candidate_unresolved"})
    dump(OUT / "diagnostics.json", {"rational_laws": [[pair(x) for x in law] for law in LAWS], "all_fixed_checks": checks, "zero_mean_cases": zero_cases})
    dump(OUT / "candidate_ledgers.json", candidates)
    summary = {"passed": True, "completed": True,
        "scope": "F08 single-predicate algebra/rounding and bounded two-ledger normalization screen; not full financial adoption.",
        "rational_cases": len(checks), "finite_uniform_scales_per_case": len(M_VALUES), "zero_mean_cases": len(zero_cases),
        "old_two_probability_samples_rerun": 0, "old_branches_reopened": False,
        "finance_draws": 0, "samplers_emitted": 0, "new_global_fixture_credit": 0,
        "normalization_ratio_diagnostic": float(normalization_ratio),
        "full_G2": False, "complete99pct_cost_certified": False, "quantum_advantage": False,
        "decision": "retain_identity_and_direct_source_no_sampler_compilation",
        "remaining": ["Certified production m/discount/error enclosures.", "Actual coherent Q preparation/inverse and one-predicate/reciprocal source.", "Full unchanged-contract99% estimator cost with >=20% improvement."]}
    dump(OUT / "summary.json", summary)
    DOC.mkdir(parents=True, exist_ok=True)
    proof = DOC / "PROOF_AND_SCREEN.txt"
    if proof.exists():
        raise ValueError("Fresh F08 proof required.")
    proof.write_text(PROOF, encoding="utf-8")
    for path, expected in p["corpus"].items():
        assert sha(ROOT / path) == expected
    files = list(OUT.iterdir()) + [proof]
    assert sum(f.stat().st_size for f in files if f.is_file()) <= p["budgets"]["output_bytes"]
    dump(OUT / "manifest.json", {"files": {str(f.relative_to(ROOT)).replace('\\', '/'): {"sha256": sha(f), "bytes": f.stat().st_size} for f in sorted(files) if f.is_file()}, "author_sha256": p["author_sha256"], "input_pins": p["corpus"]})
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args()
    prepare() if args.mode == "prepare" else run()
