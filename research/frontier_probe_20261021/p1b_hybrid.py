"""P1 run002: the routes the R2 review found uncovered by run001 (results/frontier_probe_20261021/review/p1_review.jsonl).

(a) Clipped / hybrid preintegration. The oracle encodes min(h, tau) (span tau); the tail E[(h - tau)^+] is either
    estimated classically, with its error e_c and time T_tail charged, or absorbed in the spare deterministic-bias
    reserve when it is small enough. Measured on the binding case B8x52 by plain MC over y (meas), with
    h(y) = E_z0[f] by the closed form of p1_control_span.pre_values.
    Gains (consistent pairing): linear S / tau against the no-U1 constant, sqrt((S - m)/(tau - m)) against the U1
    constant; the quantum error budget shrinks to e_q = e - e_c. Classical tail time (assm, q+ because the tail is less
    smooth than h): T_tail / T_C = (sigma_tail / sigma_preint)^2 (e / e_c)^2; both parts must fit T_C / 10 (run in
    parallel, q+).
(b) Preintegration over k > 1 directions (PCA directions 0..k-1). Directions after the first have no closed form,
    so the oracle needs at least n >= 2 nodes per extra direction: D ratio >= D_1 * 2^(k-1). The span is bounded from
    below by an explicit witness, h_k(y_hi) evaluated with 20-node Gauss-Hermite in the extra directions (mod).
(c) Corrected desk D ratio for 1-direction preintegration. The first PCA loading is constant across assets within a
    date, so the 52 barrier roots are closed form (one ln each), the strike root is a 52-term Newton, and the closed
    form needs 2 * 52 + 2 normal CDFs; the PCA loader change is bracketed (0 to +1.2 of the iterate, review row 6).
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p1b_hybrid.py
"""
import hashlib
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p1_control_span as p1  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "results" / "frontier_probe_20261021" / "p1" / "run002"
IN = dict(run001=ROOT / "results/frontier_probe_20261021/p1/run001/p1_span.json", **p1.IN)
NA, NT = 8, 52
EPS = 0.001
E = 0.45 * EPS
BIAS_USED = 0.000473  # [BD] modelled clamp-tightening bias at B8x52 $0.001 (v3 sec 2)
BIAS_SPARE = 0.55 * EPS - BIAS_USED


def h_fast(a, v, vd):
    """h(y) at the line x(z) = a + v z for the first PCA direction, using date-constant loadings vd[j]:
    barrier roots closed form, strike root by Newton on the 52 date baskets."""
    nt, na = NT, NA
    bsum = [sum(math.exp(a[i * nt + j]) for i in range(na)) for j in range(nt)]
    zh = min((math.log(na * p1.H) - math.log(bsum[j])) / vd[j] for j in range(nt))
    target = na * nt * p1.K
    z = 0.0
    for _ in range(100):
        s = ds = 0.0
        for j in range(nt):
            t = bsum[j] * math.exp(vd[j] * z)
            s += t
            ds += t * vd[j]
        step = (math.log(s) - math.log(target)) * s / ds
        z -= step
        if abs(step) < 1e-14 * (1 + abs(z)):
            break
    zs = z
    if zh <= zs:
        return 0.0
    part = sum(bsum[j] * math.exp(vd[j] ** 2 / 2) * (p1.Phi(zh - vd[j]) - p1.Phi(zs - vd[j])) for j in range(nt))
    return p1.DISC * (part / (na * nt) - p1.K * (p1.Phi(zh) - p1.Phi(zs)))


def mc_h(n, seed, v, vd, lam0, mu):
    P = p1.params(NA, NT)
    rng = random.Random(seed)
    a_, b_, m_ = P["a"], P["b"], P["m"]
    out = []
    l0 = math.log(p1.S0)
    d = NA * NT
    for _ in range(n):
        x = [0.0] * d
        lv = [l0] * NA
        for j in range(NT):
            zc = rng.gauss(0.0, 1.0)
            for i in range(NA):
                lv[i] += m_ + a_ * zc + b_ * rng.gauss(0.0, 1.0)
                x[i * NT + j] = lv[i]
        z0 = sum(v[c] * (x[c] - mu[c]) for c in range(d)) / lam0
        a = [x[c] - v[c] * z0 for c in range(d)]
        out.append(h_fast(a, v, vd))
    return out


def gauss_hermite(n):
    """Nodes/weights for E[g(Z)], Z ~ N(0,1): roots of the probabilists' He_n by bisection on sign changes,
    weights n! / (n^2 He_{n-1}(x)^2)."""
    def he(x, k):
        p0, p1_ = 1.0, x
        if k == 0:
            return 1.0
        for j in range(1, k):
            p0, p1_ = p1_, x * p1_ - j * p0
        return p1_
    R = math.sqrt(4 * n + 2) + 1
    grid = [-R + 2 * R * i / 20000 for i in range(20001)]
    nodes = []
    for lo, hi in zip(grid, grid[1:]):
        if he(lo, n) == 0 or he(lo, n) * he(hi, n) < 0:
            for _ in range(200):
                mid = (lo + hi) / 2
                if he(lo, n) * he(mid, n) <= 0:
                    hi = mid
                else:
                    lo = mid
            nodes.append((lo + hi) / 2)
    assert len(nodes) == n, len(nodes)
    weights = [math.factorial(n) / (n * n * he(x, n - 1) ** 2) for x in nodes]
    return nodes, weights


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    r1 = json.loads(IN["run001"].read_text(encoding="utf-8"))
    sig = p1.load(p1.IN["sigma"])["cases"]["B8x52"]
    price = p1.load(p1.IN["c1"])["port_check"]["B8x52"]["price"]
    m_b = price + p1.L1
    S = float(p1.S_SPAN)
    hd = p1.load(p1.IN["headline"])["summary_min_M_eligible_non_overhead"]
    M_U1 = hd["explicit_best"]["primary"][0]
    kq = {r["method"]: r["k_total"] for r in p1.load(p1.IN["kb"])["part3_k_lo_methods"]
          if r["case"] == "B8x52" and r["eps"] == 0.001 and r["split"] == "0.45eps"}
    M_noU1 = M_U1 * (kq["canonical + medians, span 8192/211 (211,53), no mean, non-dyadic M"]
                     / kq["canonical + medians, span 8192/211 (211,53), price+L1, non-dyadic M"])
    cols, lam = p1.pca_factor(NA, NT)
    mu = p1.drift(NA, NT)
    v = cols[0]
    vd = [v[j] for j in range(NT)]
    assert all(abs(v[i * NT + j] - vd[j]) < 1e-15 for i in range(NA) for j in range(NT))
    meta = dict(script="research/frontier_probe_20261021/p1b_hybrid.py", python=sys.version,
                flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site),
                inputs_sha256={k: p1.sha(p) for k, p in IN.items()}, M_U1=M_U1, M_noU1=M_noU1, m_b=m_b, S=S,
                bias_spare=BIAS_SPARE)
    res = dict(meta=meta)
    # ---- (c) corrected D ratio
    floor = p1.load(p1.IN["floor_n1"])["cases"]["B8x52"]["primary_n72"]
    st = floor["stages"]
    tof = floor["compute_toffolis"]
    per_exp = st["4c_exp"]["t"] / (NA * NT)
    per_ln = st["2_box_muller"]["poly"]["ln"]["t"]
    iters = 3
    extra = (NT + iters * (NT + 1)) * per_ln + iters * NT * per_exp + (2 * NT + 2) * per_ln \
        - st["2_box_muller"]["t"] / (NT * (NA + 1))
    d_struct = (tof + extra) / tof
    res["D_ratio_pre"] = dict(structure_aware=d_struct, loader_change_bracket=[0.0, 1.2],
                              range=[d_struct, d_struct + 1.2], run001_value=r1["desk_D_ratio_B8x52"]["pre_h_replacement"]["D_ratio"],
                              label="mod (desk); loader bracket from review row 6 (assm)")
    print("D ratio (structure-aware):", round(d_struct, 3), "range", [round(d_struct, 3), round(d_struct + 1.2, 3)])
    # ---- (a) hybrid / clipped
    n = 1 << 15
    hs = mc_h(n, 20261022, v, vd, lam[0], mu)
    mh = sum(hs) / n
    sh = math.sqrt(sum((x - mh) ** 2 for x in hs) / (n - 1))
    hs_sorted = sorted(hs)
    res["h_mc"] = dict(n=n, mean=mh, sigma=sh, max=hs_sorted[-1], q999=hs_sorted[int(0.999 * n)],
                       q9999=hs_sorted[int(0.9999 * n)], sigma_preint_ref=sig["sigma_preint"],
                       label="meas (plain MC over y, one-factor generator, closed-form preintegration)")
    print("h MC: mean", round(mh, 4), "sigma", round(sh, 4), "max", round(hs_sorted[-1], 3), "q999", round(hs_sorted[int(0.999 * n)], 3))
    rows = []
    for tau in [m_b + 0.25 * i for i in range(1, 60)]:
        tail = [max(x - tau, 0.0) for x in hs]
        mt = sum(tail) / n
        st_ = math.sqrt(max(sum((t - mt) ** 2 for t in tail) / (n - 1), 0.0))
        ntail = sum(1 for t in tail if t > 0)
        g_lin = S / tau
        g_u1 = math.sqrt((S - m_b) / (tau - m_b))
        opts = []
        # option 1: tail absorbed in the spare bias reserve (no classical work)
        if mt + 3 * st_ / math.sqrt(n) <= BIAS_SPARE:
            opts.append(("bias_absorbed", 1.0, 0.0))
        # option 2: tail estimated classically within T_C / 10
        if st_ > 0:
            frac_c = math.sqrt(10) * st_ / sig["sigma_preint"]  # e_c / e needed for T_tail <= T_C / 10
            if frac_c < 1:
                opts.append(("classical_tail", 1 - frac_c, frac_c))
        else:
            opts.append(("no_tail", 1.0, 0.0))
        for name, eq_frac, ec_frac in opts:
            m_after = min(M_U1 / (g_u1 * eq_frac), M_noU1 / (g_lin * eq_frac))
            rows.append(dict(tau=tau, option=name, tail_mean=mt, tail_sigma=st_, tail_count=ntail,
                             gain_linear=g_lin, gain_U1=g_u1, e_q_over_e=eq_frac, e_c_over_e=ec_frac,
                             net_at_D1=M_U1 / m_after, M_after_D1=m_after,
                             net_at_D_lo=M_U1 / m_after / d_struct, net_at_D_hi=M_U1 / m_after / (d_struct + 1.2),
                             label="mod from meas tail; classical tail time model assm"))
    best = max(rows, key=lambda r: r["net_at_D1"])
    best_lo = max(rows, key=lambda r: r["net_at_D_lo"])
    res["hybrid"] = dict(rows=rows, best_at_D1=best, best_at_D_structure=best_lo)
    print("hybrid best @D=1:", {k: (round(v_, 4) if isinstance(v_, float) else v_) for k, v_ in best.items() if k != "label"})
    print("hybrid best @D_struct:", {k: (round(v_, 4) if isinstance(v_, float) else v_) for k, v_ in best_lo.items() if k != "label"})
    # ---- (b) k > 1 directions: witness lower bound on sup h_k at the run001 preintegration witness profile
    W, zH = p1.pre_witnesses(NA, NT, cols, lam, mu)
    y = W["y_hi"]
    nodes, weights = gauss_hermite(20)
    assert abs(sum(weights) - 1) < 1e-12 and abs(sum(w * x * x for x, w in zip(nodes, weights)) - 1) < 1e-10
    d = NA * NT

    def h_at(yv):
        a = [mu[c] + sum(cols[k][c] * yv[k] for k in range(1, d) if yv[k] != 0.0) for c in range(d)]
        return h_fast(a, v, vd)
    kres = {}
    base = h_at(y)
    kres[1] = base
    y2 = y[:]
    y2[1] = 0.0
    acc2 = 0.0
    for x1, w1 in zip(nodes, weights):
        y2[1] = x1
        acc2 += w1 * h_at(y2)
    kres[2] = acc2
    y3 = y[:]
    acc3 = 0.0
    for x1, w1 in zip(nodes, weights):
        for x2, w2 in zip(nodes, weights):
            y3[1], y3[2] = x1, x2
            acc3 += w1 * w2 * h_at(y3)
    kres[3] = acc3
    krows = []
    for k_dir, hk in kres.items():
        d_lo = d_struct * 2 ** (k_dir - 1)
        g_lin = S / hk
        g_u1 = math.sqrt((S - m_b) / (hk - m_b)) if hk > m_b else math.inf
        m_after = min(M_U1 / g_u1, M_noU1 / g_lin)
        krows.append(dict(k=k_dir, sup_h_k_witness=hk, D_ratio_floor=d_lo, gain_linear=g_lin, gain_U1=g_u1,
                          net_at_D1=M_U1 / m_after, net_at_D_floor=M_U1 / m_after / d_lo,
                          label="mod (witness lower bound on sup h_k; GH-20 quadrature; node-count cost floor)"))
        print("k", k_dir, "h_k(witness)", round(hk, 4), "net@D1", round(M_U1 / m_after, 3), "net@Dfloor", round(M_U1 / m_after / d_lo, 3))
    # general k: the floor 2^(k-1) D_1 needs gain_U1 >= 4 * 2^(k-1) D_1, i.e. sup h_k <= m + (S - m) / (4 2^(k-1) D_1)^2
    res["multi_direction"] = dict(rows=krows, z_H_profile=zH, general_condition=[
        dict(k=kk, sup_h_k_must_be_below=m_b + (S - m_b) / (4 * 2 ** (kk - 1) * d_struct) ** 2) for kk in range(1, 9)])
    overall = max([r["net_at_D_lo"] for r in rows] + [r["net_at_D_floor"] for r in krows])
    res["verdict"] = dict(best_net_with_structure_D=overall, kill_threshold=4.0, killed=overall < 4.0,
                          best_net_at_D1_any=max([r["net_at_D1"] for r in rows] + [r["net_at_D1"] for r in krows]),
                          label="mod")
    print("verdict", res["verdict"])
    with open(OUT / "p1b_hybrid.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
