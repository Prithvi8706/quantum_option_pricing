"""U3/U5 design helper: exact pure-constant law identities and premise pins.

Design-only. This script evaluates NO scientific bound: no exp, log, sqrt,
normal CDF, price, moment, probability or estimator cost. It derives exact
rational law constants of the B4x12 contract (sigma=3/10, rho=2/5, r=3/100,
T=1, dates j/12, 4 equal-weight assets, 48 equal-weight fixings), checks a
pointwise algebraic inequality on a few hand-written deterministic vectors
(algebra sanity only, not samples of the law), reads one saved support
rational, and records SHA256 pins of the premise files it cites.

Run: python -I -B research/parallel_E11_unblock_20261010/U3_U5/u3_u5_pure_constants.py
Output: research/parallel_E11_unblock_20261010/U3_U5/u3_u5_pure_constants_run001.json
(exclusive create; an existing file is never overwritten).
"""

import hashlib
import json
import os
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "u3_u5_pure_constants_run001.json"
SCRATCH = Path(
    "C:/Users/prith/AppData/Local/Temp/claude/C--Users-prith-quantum-option-pricing/"
    "3cc032fb-36f0-4c77-b733-779e62fbfea3/scratchpad/wf1"
)

SIGMA2 = F(9, 100)
RHO = F(2, 5)
R = F(3, 100)
NA, NT = 4, 12
TIMES = [F(j, NT) for j in range(1, NT + 1)]
FIX = [(i, j) for i in range(NA) for j in range(NT)]  # 48 fixings


def corr(i, k):
    return F(1) if i == k else RHO


def cov_log(a, b):
    (i, j), (k, l) = a, b
    return SIGMA2 * corr(i, k) * min(TIMES[j], TIMES[l])


def law_constants():
    n = len(FIX)
    w = F(1, n)
    s_min = sum(min(s, t) for s in TIMES for t in TIMES)
    assert s_min == F(325, 6)
    assert sum(min(j, k) for j in range(1, 13) for k in range(1, 13)) == 650
    v_lambda = sum(cov_log(a, b) for a in FIX for b in FIX) * w * w
    assert v_lambda == F(143, 7680), v_lambda
    drift_lambda = sum((R - SIGMA2 / 2) * TIMES[j] for (_, j) in FIX) * w
    assert drift_lambda == F(-13, 1600), drift_lambda
    gamma = {}
    for j in range(NT):
        g = sum(cov_log((0, j), b) for b in FIX) * w
        jj = j + 1
        assert g == F(11 * jj * (25 - jj), 64000), (jj, g)
        gamma[jj] = g
    assert sum(gamma.values()) / NT == v_lambda
    # terminal basket (KO/Doob component)
    last = NT - 1
    var_s_T = SIGMA2 * TIMES[last]
    var_lam_T = sum(cov_log((i, last), (k, last)) for i in range(NA) for k in range(NA)) / (NA * NA)
    cov_s_lam_T = sum(cov_log((0, last), (k, last)) for k in range(NA)) / NA
    assert var_lam_T == F(99, 2000) and cov_s_lam_T == var_lam_T
    kappa0 = (var_s_T - var_lam_T) / 2
    assert kappa0 == F(81, 4000)
    # distinct exact-constant exponents in E[A^2] (spot^2 factored out) and E[A G]
    e_a2 = {R * (TIMES[a[1]] + TIMES[b[1]]) + cov_log(a, b) for a in FIX for b in FIX}
    e_ag = set()
    for a in FIX:
        mu_a = (R - SIGMA2 / 2) * TIMES[a[1]]
        var_a = cov_log(a, a)
        e_ag.add(mu_a + drift_lambda + (var_a + v_lambda + 2 * gamma[a[1] + 1]) / 2)
    return {
        "contract_constants": {"sigma2": "9/100", "rho": "2/5", "r": "3/100", "T": "1",
                               "K": "100", "S0": "100", "H": "140", "dates": "j/12, j=1..12",
                               "A": "equal-weight mean of 48 fixings",
                               "survival": "every date basket (mean of 4) strictly below 140"},
        "sum_min_t_years": str(s_min),
        "asset_corr_row_sum_1_plus_3rho": str(1 + 3 * RHO),
        "Var_lnG_v_lambda": str(v_lambda),
        "E_lnG_minus_ln100": str(drift_lambda),
        "Cov_lnX_ij_lnG_gamma_j": {str(k): str(v) for k, v in gamma.items()},
        "gamma_j_closed_form": "11*j*(25-j)/64000",
        "mean_gamma_equals_v_lambda": True,
        "terminal_basket": {"Var_lnS_i_T": str(var_s_T), "Var_lnGB_T": str(var_lam_T),
                            "Cov_lnS_i_T_lnGB_T": str(cov_s_lam_T), "beta": "1",
                            "E[B_T|G_B(T)] = G_B(T)*exp(kappa0), kappa0": str(kappa0),
                            "E_lnGB_T_minus_ln100": str(R - SIGMA2 / 2)},
        "distinct_exact_exponents_E_A2_spot2_factored": len(e_a2),
        "distinct_exact_exponents_E_AG_spot2_factored": len(e_ag),
        "max_abs_exponent_E_A2": str(max(abs(x) for x in e_a2)),
    }


def pointwise_algebra_sanity():
    """f >= d*[(A-K)1_D - (A-K-c)^+] - d*c*1_KO on hand-written vectors (not law samples)."""
    d = F(97, 100)  # placeholder in (0,1]; the inequality holds for every d >= 0
    K, H = F(100), F(140)
    vectors = {
        "survive_itm": [[F(110)] * 12] * 4,
        "survive_otm": [[F(90)] * 12] * 4,
        "ko_late_itm": [[F(110)] * 11 + [F(150)]] * 4,
        "ko_one_date_exact_140": [[F(100)] * 5 + [F(140)] + [F(100)] * 6] * 4,
        "survive_just_below": [[F(139)] * 12] * 4,
        "mixed": [[F(80 + 5 * j) for j in range(12)], [F(120)] * 12,
                  [F(60)] * 12, [F(100 + j) for j in range(12)]],
    }
    rows = []
    for name, x in vectors.items():
        baskets = [sum(x[i][j] for i in range(4)) / 4 for j in range(12)]
        ko = any(b >= H for b in baskets)
        A = sum(sum(r) for r in x) / 48
        f = F(0) if ko else d * max(A - K, F(0))
        for c in (F(0), F(10), F(40)):
            for in_d in (True, False):
                rhs = d * ((A - K) * (1 if in_d else 0) - max(A - K - c, F(0))) - d * c * (1 if ko else 0)
                assert f >= rhs, (name, c, in_d)
                rows.append([name, str(c), in_d, True])
    return {"inequality": "f >= d*[(A-K)*1_D - (A-K-c)^+] - d*c*1_KO",
            "checked_cases": len(rows), "all_hold": True,
            "nature": "algebra sanity on hand-written vectors; not a sample of the law; not a bound"}


def saved_support():
    p = ROOT / "results/limitation_program_20261001/E03_support_run001/summary.json"
    case = json.loads(p.read_text())["cases"][0]
    lo, hi = case["payoff_raw_bounds"]
    num, den = case["selector_span_dollars_rational"]
    assert case["case"] == "B4x12" and lo == 0
    m_g = F(hi, 2 ** 40)
    span = F(num, den)
    assert span == 64 and m_g < span
    return {"M_g_digital_support_upper": f"{hi}/2^40", "M_g_over_2": f"{hi}/2^41",
            "M_g_squared_over_4_exact": f"{hi * hi}/2^82",
            "selector_span_dollars": str(span), "M_g_lt_span": True}


PREMISES = [
    "docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_UNIFORM_FEASIBILITY_RESULTS_20261008.md",
    "docs/limitation_program_20261001/E11_FIXED_POLAR_SAFE_PAYOFF_L2_RESULTS_20261009.md",
    ".context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json",
    "results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/manifest.json",
    "results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json",
    "results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001/independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json",
    ".context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run001.md",
    ".context/E11_B4X12_FIXED_POLAR_SAFE_UNIFORM_ERROR_FEASIBILITY_run002.md",
    "results/limitation_program_20261001/E07_schedule_run001/schedule.json",
    "results/limitation_program_20261001/E03_support_run001/summary.json",
    "results/limitation_program_20261001/E03_support_audit_run002/summary.json",
    "docs/limitation_program_20261001/STATUS.md",
    "docs/limitation_program_20261001/E10_CONTINUOUS_MOMENT_RESULTS.md",
    "results/limitation_program_20261001/E10_continuous_moment_only_run002/summary.json",
    "results/limitation_program_20261001/E10_continuous_moment_only_run002/manifest.json",
    "research/limitation_program_20261001/experiment_e10_continuous_moment_only_v2.py",
    "research/limitation_program_20261001/E10_CONTINUOUS_MOMENT_ONLY_PREFLIGHT_V2.md",
    ".context/ROOT_E11_ANY_H_CERTIFICATE_FOUR_TARGET_CONDITIONAL_REVIEW_run001.json",
    "manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md",
    "docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md",
    "results/frontier_classical_20261001/c1/c1_summary.json",
    "research/controlled_priority_completion/estimator_hadamard.py",
    ".context/advantage_frontier_replay/research/advantage_frontier_20260923/barrier_fast_classical.py",
    "docs/limitation_audit_20261001/implementation_plan/ESTIMATION.md",
    "docs/limitation_program_20261001/E11_B4X12_ALL48_STOCK_MATRIX_RESULTS_20261007.md",
    "docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md",
]
SCRATCH_PREMISES = ["PLAN_43.md", "moment_estimator_inventory.json"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    record = {
        "label": "U3_U5_pure_constant_identities_and_premise_pins",
        "design_only": True,
        "scientific_bound_evaluated": False,
        "transcendental_functions_evaluated": False,
        "law_constants": law_constants(),
        "pointwise_algebra_sanity": pointwise_algebra_sanity(),
        "saved_support": saved_support(),
        "premise_sha256": {p: sha(ROOT / p) for p in PREMISES},
        "session_scratch_premise_sha256": {
            str(SCRATCH / n): (sha(SCRATCH / n) if (SCRATCH / n).exists() else None)
            for n in SCRATCH_PREMISES},
    }
    data = json.dumps(record, indent=1, sort_keys=True).encode()
    fd = os.open(OUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0))
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    print(OUT, hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
