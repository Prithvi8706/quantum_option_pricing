"""Scope #44 R2 sealed-run steps. Each step runs in its own process, launched by sealed_run.py:

    <pinned python> <flags> research/r2_scope44/steps.py STEP ROOT SEED_HEX

STEP is p2, a2a, u1_sample, u1_bound or headline (in that order); ROOT is the sealed output root. Definitions,
constants and decision rules are those of docs/r2_scope44/PREREGISTRATION.md. Reused R1 code is loaded by file
path, and only after its sha256 matches research/r2_scope44/manifest.json. Every output is created exclusively.
"""
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MANIFEST = json.loads((REPO / "research/r2_scope44/manifest.json").read_text(encoding="utf-8"))

P2_SRC = "research/frontier_probe_20261021/p2_window_constant.py"
P2B_SRC = "research/frontier_probe_20261021/p2b_parts34.py"
A2A_SRC = [("research/claim_debts_20261022/a2a/clip_split_certificate.py", "a2a_primary"),
           ("research/claim_debts_20261022/a2a/independent_recompute.py", "a2a_independent"),
           ("research/claim_debts_20261022/a2a/summarize.py", "a2a_summarize")]
U1_SRC = "research/claim_debts_20261022/u1/u1_certificate.py"
IN = dict(
    eb_r1="results/claim_debts_20261022/u1/run001/eb_sample.json",
    a2a_r1="results/claim_debts_20261022/a2a/run001/summary.json",
    sigma="results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    c1="results/frontier_classical_20261001/c1/c1_summary.json",
    c2="results/frontier_classical_20261001/c2/c2_timing.json",
    c5="results/frontier_classical_20261001/c5/timing/c5_timing.json",
    overrides="results/c10_challengers_20261022/overrides_run006.json",
    floor_w0="results/plan110_w0/ws_floor/floor.json",
    floor_n1="results/plan110_n1/headline/floor_sheet.json",
    c11="results/claim_debts_20261022/c11/run001/summary.json",
    scope44_r1="results/claim_debts_20261022/scope44/run001/scope44_receipt.json",
)

# Preregistered constants (PREREGISTRATION.md sections 3-5).
DELTA34 = F(4, 10 ** 6)
N_MAX = 1048575  # parts 3-4 reserve holds while g <= 21
CERTS = [  # key, beta, delta, R1 value (must reproduce exactly)
    ("window", "3.87", F(3, 1000), F(4179, 1000)),
    ("stage1", "5.72", F(1, 10000), F(6052, 1000)),
    ("stage2", "3.88", F(29, 10000), F(4197, 1000)),
]
D1 = F(7, 2000)  # quantum-only mean class: stage-1 phase half-width (R1 optimum, fixed)
DELTA_L = F(1, 10000)  # lower confidence bound on E[g], for the quantum-favourable cost rows
EPS = F(1, 1000)
CASE, KEY = "B8x52", "B8x52_H140|0.001"
T_LAYER = 1e-7
EXPLICIT = ("primary", "all_free_oracle", "one_lane_one_core", "symmetric_distfree")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pinned(rel):
    p = REPO / rel
    if sha(p) != MANIFEST["files"][rel]:
        raise SystemExit(f"hash mismatch: {rel}")
    return p


def load_module(rel, name, argv=None):
    """Execute a pinned module from its path; argv stands in for scripts that read sys.argv at import."""
    path = pinned(rel)
    saved = sys.argv
    if argv is not None:
        sys.argv = [str(path)] + argv
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    finally:
        sys.argv = saved
    return mod


def read_in(key):
    return json.loads(pinned(IN[key]).read_text(encoding="utf-8"))


def read_out(root, name):
    return json.loads((root / name).read_text(encoding="utf-8"))


def frac(x):
    x = F(x)
    return [str(x.numerator), str(x.denominator)]


def write(root, name, obj):
    with open(root / name, "x", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, default=str)


# ---------------------------------------------------------------------------------------------------- p2
def step_p2(root, _seed):
    p2 = load_module(P2_SRC, "p2_window_constant")
    out = {}
    for key, beta, delta, r1 in CERTS:
        itot_hi = 2 * p2.PI_HI * p2.int_phi_sq_upper(F(beta) ** 2, F(0))
        c, info = p2.certify(beta, F(0), delta - DELTA34, itot_hi, float(r1) - 0.05, float(r1) + 0.10, F(1, 1000))
        out[key] = dict(beta=beta, gamma="0", delta=str(delta), delta_target=str(delta - DELTA34), c=str(c),
                        c_R1=str(r1), reproduces_R1=c == r1, lambda_lower_N0=str(info["lambda_lower_N0"]),
                        N0=p2.N0, I_c_lower=str(info["I_c_lower"]))
    ok = all(v["reproduces_R1"] for v in out.values())
    write(root, "p2.json", dict(step="p2", certificates=out, all_reproduce_R1=ok,
                                label="cert (parts 1-2 certified at N0, all N >= N0; parts 3-4 reserve 4e-6)"))
    if not ok:
        raise SystemExit("P2 constant did not reproduce R1")


# --------------------------------------------------------------------------------------------------- a2a
def step_a2a(root, _seed):
    base = root / "a2a"
    mods = [load_module(rel, name) for rel, name in A2A_SRC]
    for m in mods:
        m.OUT = base
    for m in mods:
        m.main("run")
    sys.set_int_max_str_digits(0)
    s = json.loads((base / "run" / "summary.json").read_text())
    r1 = read_in("a2a_r1")
    bias = s["cases"][CASE]["certified_total_upper_rounded_up_2^-64"]
    same = bias == r1["cases"][CASE]["certified_total_upper_rounded_up_2^-64"]
    eligible = F(int(bias[0]), int(bias[1])) <= F(11, 20) * EPS
    write(root, "a2a.json", dict(step="a2a", all_checks_pass=s["all_checks_pass"], bias_upper=bias,
                                 bias_float=int(bias[0]) / int(bias[1]), reproduces_R1=same,
                                 eligible_0p55eps=eligible))
    if not (s["all_checks_pass"] and same and eligible):
        raise SystemExit("A2a did not pass or did not reproduce R1")


# ------------------------------------------------------------------------------------------------- u1 sample
# Contract and loop copied unchanged from research/claim_debts_20261022/u1/eb_sample.py (R1); the R1-seed
# reproduction below proves the copy is equivalent in this environment.
NA, NT = 8, 52
S0, K, H, SIG, RHO, R, T = 100.0, 100.0, 140.0, 0.3, 0.4, 0.03, 1.0
N_TOTAL = 2 ** 23
CHUNK = 2 ** 15
SEED_R1 = [2026102231, 8, 52]


def chunk_payoffs(np, rng, m):
    dt = T / NT
    t = dt * np.arange(1, NT + 1)
    w0 = np.cumsum(rng.standard_normal((m, NT)), axis=1) * math.sqrt(dt)
    wi = np.cumsum(rng.standard_normal((m, NA, NT)), axis=2) * math.sqrt(dt)
    x = math.log(S0) + (R - 0.5 * SIG * SIG) * t + SIG * (math.sqrt(RHO) * w0[:, None, :] + math.sqrt(1 - RHO) * wi)
    s = np.exp(x)
    b = s.mean(axis=1)
    alive = (b < H).all(axis=1)
    a = b.mean(axis=1)
    return math.exp(-R * T) * np.maximum(a - K, 0.0) * alive


def draw(np, seed):
    rng = np.random.default_rng(seed)
    n, s1, s2, lo, hi = 0, [], [], math.inf, -math.inf
    while n < N_TOTAL:
        y = chunk_payoffs(np, rng, min(CHUNK, N_TOTAL - n))
        s1.append(math.fsum(y.tolist()))
        s2.append(math.fsum((y * y).tolist()))
        lo, hi = min(lo, float(y.min())), max(hi, float(y.max()))
        n += y.size
    return dict(n=n, sum=math.fsum(s1), sum_sq=math.fsum(s2), min=lo, max=hi, seed=seed)


def step_u1_sample(root, seed_hex):
    import numpy as np
    import time

    r1 = read_in("eb_r1")
    t0 = time.perf_counter()
    rep = draw(np, SEED_R1)
    rep_ok = rep["n"] == r1["n"] and rep["sum"] == r1["sum"] and rep["sum_sq"] == r1["sum_sq"]
    rec = dict(step="u1_sample", numpy=np.__version__, generator="numpy PCG64 default_rng, standard_normal",
               n_fixed=N_TOTAL, chunk=CHUNK, reproduction_R1=dict(rep, matches_R1_bit_for_bit=rep_ok),
               contract=dict(na=NA, nt=NT, spot=S0, strike=K, barrier=H, sigma=SIG, rho=RHO, rate=R, maturity=T))
    if rep_ok:
        seed = [int(seed_hex[8 * i:8 * i + 8], 16) for i in range(8)]
        rec["fresh"] = draw(np, seed)
    rec["wall_s"] = time.perf_counter() - t0
    write(root, "u1_sample.json", rec)
    if not rep_ok:
        raise SystemExit("sampler did not reproduce the R1 totals; fresh sample not drawn")


# -------------------------------------------------------------------------------------------------- u1 bound
def step_u1_bound(root, _seed):
    u1 = load_module(U1_SRC, "u1_certificate", argv=["r2_import"])
    smp = read_out(root, "u1_sample.json")["fresh"]
    n = int(smp["n"])
    s1, s2 = F(smp["sum"]), F(smp["sum_sq"])
    mean = s1 / n
    var = (s2 - s1 * s1 / n) / (n - 1)
    if not (0 <= smp["min"] and smp["max"] <= float(u1.R_RAW)):
        raise SystemExit("sample outside [0, R]")
    ucb, half_u = u1.eb_ucb(mean + u1.FLOAT_SLACK, var, n, u1.R_RAW, u1.DELTA_U)
    _, half_l = u1.eb_ucb(F(0), var, n, u1.R_RAW, DELTA_L)
    lcb = mean - u1.FLOAT_SLACK - half_l
    bias = F(*map(int, read_out(root, "a2a.json")["bias_upper"]))
    m_u, m_l = ucb + bias, lcb - bias
    rec = dict(step="u1_bound", n=n, mean=frac(mean), var_unbiased=frac(var), delta_U=str(u1.DELTA_U),
               delta_L=str(DELTA_L), R=str(u1.R_RAW), float_slack=str(u1.FLOAT_SLACK),
               half_width_upper=frac(half_u), half_width_lower=frac(half_l), ucb=frac(ucb), lcb=frac(lcb),
               a2a_bias=frac(bias), m_U=frac(m_u), m_L=frac(m_l), m_U_float=float(m_u), m_L_float=float(m_l),
               m_U_le_S_over_2=m_u <= F(8192, 211) / 2)
    write(root, "u1_bound.json", rec)
    if not rec["m_U_le_S_over_2"]:
        raise SystemExit("m_U exceeds S/2")


# -------------------------------------------------------------------------------------------------- headline
def classical_inputs():
    """T_C, sigma/e, D_eff and departure factors, with the definitions of SCOPE44_PROSPECTUS.md."""
    sigma_q = read_in("sigma")["cases"][CASE]["sigma_q"]
    ov = read_in("overrides")
    speed = ov["f32_applied"][KEY]["speedup_run005"] * ov["f32_applied"][KEY]["f32_over_fast"]
    walls = []
    for key in ("c2", "c5"):
        for block, val in read_in(key)["blocks"].items():
            case, method = block.split("/")
            if case != CASE:
                continue
            for e_key, rec in val["t_c"].items():
                if float(e_key) == float(EPS):
                    walls.append((rec["primary"] / (speed if method == "preint" else 1.0), key, method))
    t_c, t_src, t_method = min(walls)
    w0 = read_in("floor_w0")["headline"][CASE]
    n1 = read_in("floor_n1")["cases"][CASE]

    def d_eff(n1_design, w0_design):
        a = n1[n1_design]["by_width"]["W1e7"]["1e12|100ns"]["D_eff"]
        b = w0["W1e7"][w0_design]["comparison"][0]["by_t_layer"]["100ns"]["base"]["eff_depth_supply_1e12"]
        return min(a, b)

    c11 = read_in("c11")
    return dict(sigma_q=sigma_q, sigma_over_e=sigma_q / (0.45 * float(EPS)), T_C=t_c, T_C_source=[t_src, t_method],
                speedup=speed, h16_ratio=ov["overrides"]["h16_ratio"][KEY],
                distfree_factor=ov["overrides"]["distfree_factor"][KEY],
                D_primary=d_eff("primary_n72", "box_muller_current_law"),
                D_all_free=d_eff("all_free_n48_f32", "all_free_and_narrow"),
                D_compiled=c11["D_eff"]["qf_floor_convention"] if c11.get("all_checks_pass") else None)


def step_headline(root, _seed):
    p2 = load_module(P2_SRC, "p2_window_constant")
    p2b = load_module(P2B_SRC, "p2b_parts34")
    cert = read_out(root, "p2.json")["certificates"]
    u = read_out(root, "u1_bound.json")
    c_w, c_1, c_2 = (F(cert[k]["c"]) for k in ("window", "stage1", "stage2"))
    S, e = p2.S_SPAN["8192/211"], F(9, 20) * EPS
    price = F(str(read_in("c1")["port_check"][CASE]["price"]))
    m_p2, m_u, m_l = price + p2.L1, F(*map(int, u["m_U"])), F(*map(int, u["m_L"]))
    ci = classical_inputs()
    se = F(str(read_in("sigma")["cases"][CASE]["sigma_q"])) / e

    def stage(c, m):
        n = math.ceil(c / p2.delta_phi(m, S, e))
        return n, c

    n1 = max(math.ceil(c_1 / D1), p2.N0)
    err = D1 / 2 + D1 * D1 / 4
    rows = {
        "W_cont": dict(m=m_p2, stages=[stage(c_w, m_p2)], valid=m_u <= m_p2,
                       definition="window, U1 credit at P2's m = price + L1 (v4 continuity; valid iff m_U <= it)"),
        "W_proto": dict(m=m_u, stages=[stage(c_w, m_u)], valid=True,
                        definition="window, U1 credit at m_U from this run's fresh sample (the protocol as run)"),
        "W_oracle": dict(m=m_l, stages=[stage(c_w, m_l)], valid=True,
                         definition="window with the exact mean known for free (lower bound via m_L)"),
        "Q_cont": dict(m=price + 2 * S * err, stages=[(n1, c_1), stage(c_2, price + 2 * S * err)], valid=True,
                       definition="quantum-only mean, worst case over stage-1 successes at the RQMC price (R1)"),
        "Q_lower": dict(m=m_l, stages=[(n1, c_1), stage(c_2, m_l)], valid=True,
                        definition="quantum-only mean, fewest calls over stage-1 successes, at m_L"),
    }

    def M(k, D, tc):
        return k * 10.0 * ci["sigma_over_e"] * D * T_LAYER / tc

    budgets_ok = True
    out_rows = {}
    for name, r in rows.items():
        n_total = sum(n for n, _ in r["stages"])
        k = float(F(n_total) / se)
        bud = []
        for n, c in r["stages"]:
            b = p2b.budgets(n, float(c))
            ok = b["delta_34"] <= DELTA34 and n <= N_MAX and n >= p2.N0
            budgets_ok = budgets_ok and ok
            bud.append(dict(N=n, c=str(c), delta_34=float(b["delta_34"]), ok=ok))
        cols = {"primary": M(k, ci["D_primary"], ci["T_C"]),
                "all_free_oracle": M(k, ci["D_all_free"], ci["T_C"]),
                "one_lane_one_core": M(k, ci["D_primary"], ci["T_C"] * ci["h16_ratio"]),
                "symmetric_distfree": M(k, ci["D_primary"], ci["T_C"] * ci["distfree_factor"]),
                "all_free_plus_symmetric": M(k, ci["D_all_free"], ci["T_C"] * ci["distfree_factor"])}
        if ci["D_compiled"]:
            cols["compiled_iterate_primary"] = M(k, ci["D_compiled"], ci["T_C"])
        out_rows[name] = dict(definition=r["definition"], m=frac(r["m"]), m_float=float(r["m"]), valid=r["valid"],
                              N_total=n_total, k=k, budgets=bud, M=cols)

    r1 = read_in("scope44_r1")["M_binding_cell"]
    cont = {}
    for mine, theirs in (("W_cont", "window_certified_fail0003"), ("Q_cont", "window_quantum_only_mean")):
        cont[mine] = {c: abs(out_rows[mine]["M"][c] - v) / v for c, v in r1[theirs].items()}
    cont_ok = all(d <= 1e-9 for v in cont.values() for d in v.values())

    decided = [r for r in out_rows.values() if r["valid"]]
    no_go = all(r["M"][c] > 1 for r in decided for c in EXPLICIT)
    eligible = read_out(root, "a2a.json")["eligible_0p55eps"]
    outcome = "NO_GO_CERTIFIED" if (no_go and eligible and budgets_ok) else "NO_GO_NOT_CERTIFIED"
    write(root, "headline.json", dict(
        step="headline", classical_inputs=ci, D1=str(D1), N1_stage1=n1, rows=out_rows,
        continuity_rel_diff_vs_R1=cont, continuity_1e9=cont_ok, budgets_ok=budgets_ok,
        decision=dict(rule="NO-GO iff every valid row has M > 1 in every explicit single-departure column",
                      explicit_columns=list(EXPLICIT), no_go=no_go, eligible_on_certified_bias=eligible,
                      min_M_primary=min(r["M"]["primary"] for r in decided),
                      min_M_any_explicit=min(r["M"][c] for r in decided for c in EXPLICIT),
                      headline_M_primary_W_proto=out_rows["W_proto"]["M"]["primary"], outcome=outcome)))
    if not cont_ok:
        raise SystemExit("continuity rows do not reproduce the R1 scope #44 receipt")


STEPS = dict(p2=step_p2, a2a=step_a2a, u1_sample=step_u1_sample, u1_bound=step_u1_bound, headline=step_headline)

if __name__ == "__main__":
    STEPS[sys.argv[1]](Path(sys.argv[2]), sys.argv[3])
