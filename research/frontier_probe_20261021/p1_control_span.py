"""P1 of the 21 Oct 2026 frontier probe: control-variate residual span (register F20/F04, v3 sec 6 lever 5).

Bounded amplitude estimation's call count scales with the span of the encoded variable (and, with the U1
mean credit, with sqrt(m (S - m))). This script bounds, for each candidate control g with a classically
certifiable mean, the worst-case span S_res of the residual payoff - beta * g over the oracle's support, for
EVERY beta, from explicit in-support witness paths (lower bounds, the kill direction). It then forms the net
factor (S / S_res) * (D_eff / D_eff,res) against the thresholds M = 232 / 11.5 / 6.29.

Two levels:
  raw   residual f - beta g with f the knock-out payoff (one-factor oracle model, |Z| <= 4.7 per normal);
        the witness pair (w_hi, w_ko_*) straddles the arithmetic-basket barrier, where f jumps by ~$38.5
        while every listed control is continuous there, so S_res >= ~38.5 for every beta;
  pre   F04 "structured integration of the residual": the first canonical PCA direction is integrated
        analytically (the classical comparator's preintegration), so the encoded variable is
        h(y) - beta g_hat(y), h = E[f | y], g_hat = E[g | y], y in the PCA coordinates with |y| <= 4.7.

Witness values of f and of the raw controls are evaluated in decimal arithmetic at 50 digits (exp, ln and
sqrt are correctly rounded in the decimal module); the preintegrated level uses binary64 with math.erfc,
and its witness lower bound on sup h is re-derived from below by a monotone quadrature in decimal.
Labels follow the v3 number rule: meas / mod / assm / lit and q+ / q- / 0.

Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p1_control_span.py
"""
import hashlib
import json
import math
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 50
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "frontier_probe_20261021" / "p1" / "run001"
IN = dict(
    sigma=ROOT / "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    c1=ROOT / "results/frontier_classical_20261001/c1/c1_summary.json",
    floor_n1=ROOT / "results/plan110_n1/headline/floor_sheet.json",
    headline=ROOT / "results/plan110_n1/headline/headline_table.json",
    hw=ROOT / "results/plan110_n1/hwclassical/hw_classical_card_v2.json",
    kb=ROOT / "results/plan110_w0/ws_k/k_bracket.json",
)
SIG, RHO, RATE, MAT, S0, K, H = 0.3, 0.4, 0.03, 1.0, 100.0, 100.0, 140.0
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
S_SPAN = Fraction(8192, 211)  # U2 support-tight span (v3 sec 4.2)
L1 = 0.045202052  # #43 L1 display value used by the U1 credit (estimator card sec 2b)
ZCLIP = 4.7  # every witness normal satisfies |Z| <= 4.7: inside the q32 inverse-CDF grid (|Z| <= 6.5) and any
#              Box-Muller pairing (radius 4.7 * sqrt 2 = 6.65 < sqrt(-2 ln 2^-32) = 6.66)
DISC = math.exp(-RATE * MAT)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def row(d):
    with open(OUT / "rows.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(d, sort_keys=True) + "\n")


def Phi(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


# ---------------------------------------------------------------- oracle model (one-factor, per date)
def params(na, nt):
    dt = MAT / nt
    return dict(na=na, nt=nt, dt=dt, a=SIG * math.sqrt(RHO * dt), b=SIG * math.sqrt((1 - RHO) * dt),
                m=(RATE - SIG * SIG / 2) * dt)


def logpaths(P, Zc, Zi, dec=False):
    """x[i][j] = ln S0 + (j+1) m + a sum_{l<=j} Zc_l + b sum_{l<=j} Zi[i][l]."""
    na, nt = P["na"], P["nt"]
    cv = Decimal if dec else float
    a, b, m = cv(repr(P["a"])), cv(repr(P["b"])), cv(repr(P["m"]))
    l0 = cv(S0).ln() if dec else math.log(S0)
    x = []
    for i in range(na):
        s = l0
        row_ = []
        for j in range(nt):
            s = s + m + a * cv(repr(Zc[j])) + b * cv(repr(Zi[i][j]))
            row_.append(s)
        x.append(row_)
    return x


def payoffs_dec(P, x):
    """Knock-out payoff and the raw controls at one path, in decimal (50 digits)."""
    na, nt = P["na"], P["nt"]
    disc = (Decimal(-3) / Decimal(100)).exp()  # e^{-r T} with r T = 0.03
    Kd, Hd = Decimal(K), Decimal(H)
    e = [[x[i][j].exp() for j in range(nt)] for i in range(na)]
    baskets = [sum(e[i][j] for i in range(na)) / na for j in range(nt)]
    A = sum(baskets) / nt
    alive = all(bj < Hd for bj in baskets)
    G = (sum(x[i][j] for i in range(na) for j in range(nt)) / (na * nt)).exp()
    S1T = e[0][nt - 1]
    pos = lambda v: v if v > 0 else Decimal(0)
    f = disc * pos(A - Kd) if alive else Decimal(0)
    g = dict(
        C1_geo_call=disc * pos(G - Kd),
        C2a_linear_avg=disc * A,
        C2b_arith_call=disc * pos(A - Kd),
        C3a_asset1_terminal_ko=disc * pos(S1T - Kd) if S1T < Hd else Decimal(0),
        C3b_geo_avg_ko=disc * pos(G - Kd) if G < Hd else Decimal(0),
    )
    return f, g, dict(A=A, G=G, max_basket=max(baskets), S1T=S1T, alive=alive)


def control_means(P, arith_call_mc):
    """Closed-form means (binary64, mod) of the raw controls; C2b from Monte Carlo (assm)."""
    na, nt, a, b, m = P["na"], P["nt"], P["a"], P["b"], P["m"]
    w2 = sum(((nt - l) / nt) ** 2 for l in range(nt))
    mG = math.log(S0) + m * (nt + 1) / 2
    sG = math.sqrt((a * a + b * b / na) * w2)

    def lognormal_call(mu, s, k, hcap=None):
        d2 = (mu - math.log(k)) / s
        val = math.exp(mu + s * s / 2) * Phi(d2 + s) - k * Phi(d2)
        if hcap is not None:
            d2h = (mu - math.log(hcap)) / s
            val -= math.exp(mu + s * s / 2) * Phi(d2h + s) - k * Phi(d2h)
        return DISC * val

    mT = math.log(S0) + m * nt
    sT = SIG * math.sqrt(MAT)
    return dict(
        C1_geo_call=lognormal_call(mG, sG, K),
        C2a_linear_avg=DISC * sum(S0 * math.exp(RATE * (j + 1) * P["dt"]) for j in range(nt)) / nt,
        C2b_arith_call=arith_call_mc,
        C3a_asset1_terminal_ko=lognormal_call(mT, sT, K, H),
        C3b_geo_avg_ko=lognormal_call(mG, sG, K, H),
    ), dict(mG=mG, sG=sG)


# ---------------------------------------------------------------- witnesses (raw level)
def witnesses(P):
    """Explicit normals (|Z| <= ZCLIP). w_hi: alive, every date basket just below H (high payoff).
    w_ko_idio: w_hi with the last-date idiosyncratic normals of assets 2..na raised so the last basket
    crosses H (asset 1, G and the barrier-free controls barely move). w_ko_common: w_hi with the
    last-date common normal raised. w_low / w_zero / w_top: all normals -4.7 / 0 / +4.7."""
    na, nt, a, b, m = P["na"], P["nt"], P["a"], P["b"], P["m"]
    target = math.log(H) - 2e-4  # every date basket at 139.97
    Zc, Zi = [0.0] * nt, [[0.0] * nt for _ in range(na)]
    level = math.log(S0)
    for j in range(nt):
        need = (target - level - m) / (a + b)
        z = max(-ZCLIP, min(ZCLIP, need))
        Zc[j] = z
        for i in range(na):
            Zi[i][j] = z
        level += m + (a + b) * z
    hi = (Zc, Zi)
    # knock-out by idiosyncratic moves of assets 2..na at the last date
    bump = math.log((H * 1.0002 * na - math.exp(level)) / ((na - 1) * math.exp(level))) / b
    Zi2 = [r[:] for r in Zi]
    for i in range(1, na):
        Zi2[i][nt - 1] += bump
    Zc3 = Zc[:]
    Zc3[nt - 1] += 6e-4 / a
    W = dict(w_hi=hi, w_ko_idio=(Zc, Zi2), w_ko_common=(Zc3, Zi),
             w_low=([-ZCLIP] * nt, [[-ZCLIP] * nt for _ in range(na)]),
             w_zero=([0.0] * nt, [[0.0] * nt for _ in range(na)]),
             w_top=([ZCLIP] * nt, [[ZCLIP] * nt for _ in range(na)]))
    for k, (zc, zi) in W.items():
        assert max(abs(v) for v in zc) <= ZCLIP and max(abs(v) for r in zi for v in r) <= ZCLIP, k
    return W


# ---------------------------------------------------------------- span lower bounds over every beta
def min_over_beta_span(vals):
    """vals: list of (f_w, g_w) as Fractions. F(beta) = max_{p,q} |(f_p - f_q) - beta (g_p - g_q)| is a
    lower bound on the residual span for that beta; it is convex piecewise linear, so its minimum is
    attained at a breakpoint. Returns (min F, argmin beta, F(0))."""
    pieces = []
    n = len(vals)
    for p in range(n):
        for q in range(n):
            if p != q:
                df, dg = vals[p][0] - vals[q][0], vals[p][1] - vals[q][1]
                pieces.append((df, dg))  # affine df - beta dg; abs handled by including (q,p)

    def F(beta):
        return max(df - beta * dg for df, dg in pieces)

    cands = {Fraction(0)}
    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            (f1, g1), (f2, g2) = pieces[i], pieces[j]
            if g1 != g2:
                cands.add((f1 - f2) / (g1 - g2))
    best = min(((F(c), c) for c in cands), key=lambda t: t[0])
    return best[0], best[1], F(Fraction(0))


def u1_gain_sup(vals, mean_f_lo, mean_f_hi, mean_g, m_b, S, beta_max=20.0, step=1e-3):
    """Upper bound, over every beta, on sqrt(m_b (S - m_b)) / sqrt(m' (S' - m')) where m' = E r - inf r and
    S' - m' = sup r - E r for r = f - beta g. On each beta cell both factors are bounded below by the
    endpoint minima of the per-witness affine lower bounds; |beta| > beta_max handled by linear growth."""
    base = math.sqrt(m_b * (S - m_b))
    fw = [float(v[0]) for v in vals]
    gw = [float(v[1]) for v in vals]
    worst = (0.0, None)
    for mu_f in (mean_f_lo, mean_f_hi):
        def lows(beta):
            mu = mu_f - beta * mean_g
            return [mu - (f - beta * g) for f, g in zip(fw, gw)], [(f - beta * g) - mu for f, g in zip(fw, gw)]
        nstep = int(round(2 * beta_max / step))
        prev = lows(-beta_max)
        for s in range(1, nstep + 1):
            beta = -beta_max + s * step
            cur = lows(beta)
            lo_m = max(min(p, c) for p, c in zip(prev[0], cur[0]))
            lo_s = max(min(p, c) for p, c in zip(prev[1], cur[1]))
            prod = max(lo_m, 0.0) * max(lo_s, 0.0)
            g = math.inf if prod <= 0 else base / math.sqrt(prod)
            if g > worst[0]:
                worst = (g, round(beta - step / 2, 6), mu_f)
            prev = cur
        # tails: both factors grow at least linearly beyond beta_max
        for sgn in (-1, 1):
            slopes_m = [sgn * (g - mean_g) for g in gw]  # d/d|beta| of (mu - r_w)
            slopes_s = [sgn * (mean_g - g) for g in gw]
            assert max(slopes_m) > 0 and max(slopes_s) > 0, "tail not controlled"
            m0, s0 = lows(sgn * beta_max)
            lo_m = max(m0[i] for i in range(len(fw)) if slopes_m[i] > 0)
            lo_s = max(s0[i] for i in range(len(fw)) if slopes_s[i] > 0)
            if lo_m <= 0 or lo_s <= 0:
                worst = (math.inf, f"tail {sgn}", mu_f)
            else:
                g = base / math.sqrt(lo_m * lo_s)
                if g > worst[0]:
                    worst = (g, f"tail {sgn}", mu_f)
    return worst


# ---------------------------------------------------------------- preintegrated level (canonical PCA)
def pca_factor(na, nt):
    """Canonical PCA factor (research/frontier_classical_20261001/basis.py closed forms), coordinates
    c = asset * nt + date, columns sorted by eigenvalue desc, ties by asset then time index."""
    av = [[0.0] * na for _ in range(na)]
    for i in range(na):
        av[i][0] = 1 / math.sqrt(na)
    for k in range(1, na):
        nr = math.sqrt(k * (k + 1))
        for i in range(k):
            av[i][k] = 1.0 / nr
        av[k][k] = -k / nr
    al = [SIG ** 2 * (1 - RHO)] * na
    al[0] = SIG ** 2 * (1 + (na - 1) * RHO)
    tv = [[math.sin((i + 1) * (2 * k + 1) * math.pi / (2 * nt + 1)) for k in range(nt)] for i in range(nt)]
    for k in range(nt):
        nr = math.sqrt(sum(tv[i][k] ** 2 for i in range(nt)))
        for i in range(nt):
            tv[i][k] /= nr
    tl = [(MAT / nt) / (4 * math.sin((2 * k + 1) * math.pi / (2 * (2 * nt + 1))) ** 2) for k in range(nt)]
    order = sorted(((-al[a] * tl[t], a, t) for a in range(na) for t in range(nt)))
    cols, lam = [], []
    for negl, a, t in order:
        s = math.sqrt(-negl)
        cols.append([av[i][a] * tv[j][t] * s for i in range(na) for j in range(nt)])
        lam.append(-negl)
    return cols, lam


def drift(na, nt):
    return [math.log(S0) + (RATE - SIG ** 2 / 2) * (j + 1) * MAT / nt for i in range(na) for j in range(nt)]


def newton_root(a, v, idx, w, target):
    num = sum(a[i] * w for i in idx)
    den = sum(v[i] * w for i in idx)
    z = (math.log(target) - num) / den
    for _ in range(100):
        s = ds = 0.0
        for i in idx:
            t = w * math.exp(a[i] + v[i] * z)
            s += t
            ds += t * v[i]
        step = (math.log(s) - math.log(target)) * s / ds
        z -= step
        if abs(step) < 1e-15 * (1 + abs(z)):
            break
    return z


def pre_values(na, nt, a, v, c1):
    """h(y) and the preintegrated controls g_hat(y) at the line x(z) = a + v z (binary64; mod)."""
    dim = na * nt
    zs = newton_root(a, v, range(dim), 1 / dim, K)
    zh = min(newton_root(a, v, [i * nt + j for i in range(na)], 1 / na, H) for j in range(nt))
    hi = max(zh, zs)
    h = DISC * (sum(math.exp(a[c] + v[c] ** 2 / 2) * (Phi(hi - v[c]) - Phi(zs - v[c])) for c in range(dim)) / dim
                - K * (Phi(hi) - Phi(zs)))
    call_pre = DISC * (sum(math.exp(a[c] + v[c] ** 2 / 2) * Phi(v[c] - zs) for c in range(dim)) / dim - K * Phi(-zs))
    lin = DISC * sum(math.exp(a[c] + v[c] ** 2 / 2) for c in range(dim)) / dim
    ab, vb = sum(a) / dim, sum(v) / dim

    def ln_call(mu, s, k, hcap=None):  # E[(e^{mu + s z} - k)^+ 1{e^{..} < hcap}], z ~ N(0,1), s > 0
        zk = (math.log(k) - mu) / s
        zu = math.inf if hcap is None else (math.log(hcap) - mu) / s
        if zu <= zk:
            return 0.0
        up = 1.0 if hcap is None else Phi(zu - s)
        upz = 1.0 if hcap is None else Phi(zu)
        return DISC * (math.exp(mu + s * s / 2) * (up - Phi(zk - s)) - k * (upz - Phi(zk)))

    return h, dict(C1_geo_call=ln_call(ab, vb, K), C2a_linear_avg=lin, C2b_arith_call=call_pre,
                   C3a_asset1_terminal_ko=ln_call(a[c1], v[c1], K, H), C3b_geo_avg_ko=ln_call(ab, vb, K, H)), \
        dict(z_K=zs, z_H=zh)


def h_lower_bound_decimal(na, nt, a, v, zK, zH, cells=1500):
    """Certified-from-below h(y) (decimal, 50 digits): on [zl, zu] inside (z_K, z_H), verified alive and in
    the money at the endpoints (baskets and the average are increasing in z since every v_c > 0),
    h >= disc * sum_cells (A(left) - K) * (Phi(right) - Phi(left)) with Phi from an alternating erf
    series whose truncation is bounded by the first omitted term."""
    Dd = Decimal
    assert all(t > 0 for t in v)
    pi = Dd("3.14159265358979323846264338327950288419716939937510")

    def erf(x):
        x = Dd(x)
        term, s, n = x, x, 0
        while True:
            n += 1
            term = -term * x * x / n
            add = term / (2 * n + 1)
            s += add
            if abs(add) < Dd(10) ** -45 and n > 5:
                break
        return 2 / pi.sqrt() * s, abs(add)

    def Phi_lo_hi(z):
        e, err = erf(Dd(z) / Dd(2).sqrt())
        return (1 + e - 2 * err) / 2, (1 + e + 2 * err) / 2

    ad = [Dd(repr(t)) for t in a]
    vd = [Dd(repr(t)) for t in v]
    dim = na * nt

    def A(z):
        return sum((ad[c] + vd[c] * z).exp() for c in range(dim)) / dim

    def maxb(z):
        return max(sum((ad[i * nt + j] + vd[i * nt + j] * z).exp() for i in range(na)) / na for j in range(nt))

    zl = Dd(repr(zK)) + Dd("1e-9")
    zu = Dd(repr(zH)) - Dd("1e-9")
    assert A(zl) > K and maxb(zu) < H, "endpoint verification failed"
    disc = (Dd(-3) / Dd(100)).exp()
    tot = Dd(0)
    step = (zu - zl) / cells
    left = zl
    pl = Phi_lo_hi(left)
    for i in range(cells):
        right = zl + step * (i + 1)
        pr = Phi_lo_hi(right)
        tot += (A(left) - Dd(K)) * (pr[0] - pl[1])
        left, pl = right, pr
    return disc * tot


def pre_witnesses(na, nt, cols, lam, mu):
    """PCA-coordinate witnesses (|y| <= ZCLIP): y_hi, every date basket at H when z0 = z_H with
    half/half log dispersion (maximises h at a reachable y); y_ko: y_hi with the date-1 log prices
    raised by 0.2 (knocked out for z > z_H - 0.2 / v_1); y_low, y_zero, y_top: all y = -4.7 / 0 / +4.7."""
    d = na * nt
    v = cols[0]
    tgt = [math.log(H) for _ in range(d)]
    y0 = sum(v[c] * (tgt[c] - mu[c]) for c in range(d)) / lam[0]

    def from_profile(x, zH):
        resid = [x[c] - mu[c] - v[c] * zH for c in range(d)]
        y = [sum(cols[k][c] * resid[c] for c in range(d)) / lam[k] for k in range(d)]
        y[0] = 0.0
        return y

    best = None
    for zH in [0.5 + 0.05 * i for i in range(41)]:
        lc = lam[0] * (y0 - zH) / sum(v)
        if lc < 0:
            continue
        dl = math.acosh(math.exp(lc))
        x = [math.log(H * (1 - 1e-7)) - lc + (dl if i % 2 == 0 else -dl) for i in range(na) for j in range(nt)]
        y = from_profile(x, zH)
        if max(abs(t) for t in y) > ZCLIP:
            continue
        a = [mu[c] + sum(cols[k][c] * y[k] for k in range(1, d)) for c in range(d)]
        hval = pre_values(na, nt, a, v, nt - 1)[0]
        if best is None or hval > best[0]:
            best = (hval, zH, y, x)
    _, zH, y_hi, x_hi = best
    x_ko = [x_hi[c] + (0.2 if c % nt == 0 else 0.0) for c in range(d)]
    y_ko = from_profile(x_ko, zH)
    # sign-aligned witnesses move every log price the same way (all-equal y does not, in PCA coordinates)
    sgn = [0.0] + [math.copysign(1.0, sum(cols[k])) if abs(sum(cols[k])) > 1e-12 else 0.0 for k in range(1, d)]
    W = dict(y_hi=y_hi, y_ko=y_ko, y_low=[0.0] + [-ZCLIP] * (d - 1), y_zero=[0.0] * d,
             y_top=[0.0] + [ZCLIP] * (d - 1))
    for s in (-ZCLIP, -2.0, -1.0, 1.0, 2.0, ZCLIP):
        W[f"y_aligned_{s:+.1f}"] = [s * t for t in sgn]
    for k, y in W.items():
        assert max(abs(t) for t in y) <= ZCLIP + 1e-12, (k, max(abs(t) for t in y))
    return W, zH


def hstar_max(vdates, nt):
    """Rigorous-in-structure upper bound on sup_y h for the PCA direction: for z < z_H every date basket is
    basket_j(z_H) e^{v_j (z - z_H)} <= H e^{-v_j (z_H - z)}, so h(y) <= h*(z_H(y)); maximise over z_H.
    With vdates = sigma sqrt(t_j) it is instead a LOWER bound on sup_y h for any monotone direction."""
    best = (0.0, None)
    for zi in range(-300, 500):
        zH = zi / 100

        def A(z):
            return sum(H * math.exp(-vj * (zH - z)) for vj in vdates) / nt
        if A(zH) <= K:
            continue
        lo, hi = zH - 60, zH
        for _ in range(200):
            mid = (lo + hi) / 2
            if A(mid) > K:
                hi = mid
            else:
                lo = mid
        zK = hi
        s = sum(H * math.exp(-vj * zH + vj * vj / 2) * (Phi(zH - vj) - Phi(zK - vj)) for vj in vdates) / nt
        val = DISC * (s - K * (Phi(zH) - Phi(zK)))
        if val > best[0]:
            best = (val, zH)
    return best


# ---------------------------------------------------------------- Monte Carlo sigma (meas)
def mc_sigma(P, n, seed):
    """Measured sigma of f and of f - beta* g (beta* = Cov/Var) under the one-factor model; plain MC."""
    rng = random.Random(seed)
    na, nt, a, b, m = P["na"], P["nt"], P["a"], P["b"], P["m"]
    names = ("C1_geo_call", "C2a_linear_avg", "C2b_arith_call", "C3a_asset1_terminal_ko", "C3b_geo_avg_ko")
    acc = {k: [0.0] * 5 for k in names}  # sum g, sum g^2, sum f g, (unused), (unused)
    sf = sf2 = 0.0
    fmin, fmax = math.inf, -math.inf
    l0 = math.log(S0)
    for _ in range(n):
        xs = [l0] * na
        tot = 0.0
        logsum = 0.0
        alive = True
        for j in range(nt):
            zc = rng.gauss(0.0, 1.0)
            bsum = 0.0
            for i in range(na):
                xs[i] += m + a * zc + b * rng.gauss(0.0, 1.0)
                e = math.exp(xs[i])
                bsum += e
                logsum += xs[i]
            tot += bsum
            if bsum / na >= H:
                alive = False
        A = tot / (na * nt)
        G = math.exp(logsum / (na * nt))
        s1 = math.exp(xs[0])
        f = DISC * max(A - K, 0.0) if alive else 0.0
        g = dict(C1_geo_call=DISC * max(G - K, 0.0), C2a_linear_avg=DISC * A, C2b_arith_call=DISC * max(A - K, 0.0),
                 C3a_asset1_terminal_ko=DISC * max(s1 - K, 0.0) if s1 < H else 0.0,
                 C3b_geo_avg_ko=DISC * max(G - K, 0.0) if G < H else 0.0)
        sf += f
        sf2 += f * f
        for k in names:
            acc[k][0] += g[k]
            acc[k][1] += g[k] ** 2
            acc[k][2] += f * g[k]
    mf = sf / n
    vf = sf2 / n - mf * mf
    out = dict(n=n, seed=seed, mean_f=mf, sigma_f=math.sqrt(vf), controls={})
    for k in names:
        mg = acc[k][0] / n
        vg = acc[k][1] / n - mg * mg
        cov = acc[k][2] / n - mf * mg
        beta = cov / vg if vg > 0 else 0.0
        vr = vf - 2 * beta * cov + beta * beta * vg
        out["controls"][k] = dict(mean_g=mg, beta_star=beta, sigma_res=math.sqrt(max(vr, 0.0)),
                                  sigma_ratio=math.sqrt(vf) / math.sqrt(max(vr, 1e-300)))
    return out


# ---------------------------------------------------------------- desk estimate of D_eff,res / D_eff (mod)
def desk_deff(floor):
    """B8x52 iterate is supply-bound at the primary conventions, so D_eff scales with the iterate T count;
    the reaction-depth addition is reported separately. Toffoli counts per stage from the N1 floor sheet."""
    st = floor["cases"]["B8x52"]["primary_n72"]["stages"]
    tof = floor["cases"]["B8x52"]["primary_n72"]["compute_toffolis"]
    na, nt = 8, 52
    per_exp = st["4c_exp"]["t"] / (na * nt)
    per_ln = st["2_box_muller"]["poly"]["ln"]["t"]
    word = 72
    tree = na * nt * word  # Dadda tree over na*nt words: about one Toffoli per full adder bit
    mul = word * word // 2  # one truncated constant-coefficient multiply (beta), generous
    add = {
        "C1_geo_call": tree + per_exp + mul + 2 * word,
        "C2a_linear_avg": mul + 2 * word,
        "C2b_arith_call": mul + 3 * word,
        "C3a_asset1_terminal_ko": mul + 4 * word,
        "C3b_geo_avg_ko": tree + per_exp + mul + 4 * word,
    }
    out = {k: dict(extra_toffoli=v, D_ratio=(tof + v) / tof,
                   extra_reaction_layers="<= 30 (residual multiply-subtract after the payoff; tree and one exp in "
                                         "parallel with the existing exp stage)") for k, v in add.items()}
    # coherent preintegration: >= 3 Newton iterations (from a good start; the classical kernel allows 8) for
    # the strike root over all na*nt coordinates and for nt barrier roots over na coordinates, each iteration
    # one exp per coordinate plus a ln; then the closed form needs na*nt exps and 2 (na*nt + 1) normal CDFs,
    # each costed at one ln-class polynomial. One normal fewer is loaded (one Box-Muller output saved).
    iters = 3
    exps = iters * (na * nt + nt * na) + na * nt
    cdfs = 2 * (na * nt + 1)
    lns = iters * (nt + 1)
    saved = st["2_box_muller"]["t"] / (nt * (na + 1))
    extra = exps * per_exp + (cdfs + lns) * per_ln - saved
    newton_layers = iters * (st["4c_exp"]["d"] + st["2_box_muller"]["per_pair_depth_parts"]["ln"] + 8 + 50)
    out["pre_h_replacement"] = dict(
        extra_toffoli=extra, D_ratio=(tof + extra) / tof,
        extra_reaction_layers=newton_layers,
        reaction_ratio=(floor["cases"]["B8x52"]["primary_n72"]["compute_depth"] + newton_layers)
        / floor["cases"]["B8x52"]["primary_n72"]["compute_depth"],
        assumptions=f"{iters} Newton iterations, exp/ln/Phi at the floor-sheet polynomial cost, division ~50 layers")
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    sig = load(IN["sigma"])["cases"]
    price = {c: load(IN["c1"])["port_check"][c]["price"] for c in CASES}
    floor = load(IN["floor_n1"])
    hd = load(IN["headline"])["summary_min_M_eligible_non_overhead"]
    hw = load(IN["hw"])["classical"]["M_minima"]
    thresholds = dict(
        box_muller_primary=hd["explicit_best"]["primary"][0],
        all_free=hd["explicit_best"]["all_free_oracle"][0],
        symmetric_distfree=hw["box_muller_current_law|explicit_best"]["min_M_distfree"],
    )
    kq = {r["method"]: r["k_total"] for r in load(IN["kb"])["part3_k_lo_methods"]
          if r["case"] == "B8x52" and r["eps"] == 0.001 and r["split"] == "0.45eps"}
    k_ratio = (kq["canonical + medians, span 8192/211 (211,53), no mean, non-dyadic M"]
               / kq["canonical + medians, span 8192/211 (211,53), price+L1, non-dyadic M"])
    meta = dict(script="research/frontier_probe_20261021/p1_control_span.py", python=sys.version,
                flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site),
                inputs_sha256={k: sha(v) for k, v in IN.items()}, zclip=ZCLIP, S=float(S_SPAN),
                thresholds_M=thresholds, k_ratio_noU1_over_U1=k_ratio, labels="see per-field label")
    S = float(S_SPAN)
    result = dict(meta=meta, cases={})
    deff = desk_deff(floor)
    for case, (na, nt) in CASES.items():
        P = params(na, nt)
        mc = mc_sigma(P, 1 << 14 if case == "B8x52" else 1 << 15, seed=20261021)
        row(dict(step="mc_sigma", case=case, **{k: mc[k] for k in ("n", "mean_f", "sigma_f")},
                 label="meas (plain MC, one-factor model)", direction="0"))
        means, gpar = control_means(P, mc["controls"]["C2b_arith_call"]["mean_g"])
        m_b = price[case] + L1
        # ---- raw level
        W = witnesses(P)
        wv = {}
        for k, (zc, zi) in W.items():
            f, g, info = payoffs_dec(P, logpaths(P, zc, zi, dec=True))
            wv[k] = (f, g, info)
        raw = {}
        for cname in means:
            vals = [(Fraction(str(wv[k][0])), Fraction(str(wv[k][1][cname]))) for k in W]
            smin, bstar, s0 = min_over_beta_span(vals)
            u1 = u1_gain_sup(vals, price[case] - L1, price[case] + L1, means[cname], m_b, S)
            raw[cname] = dict(S_res_lower_bound=float(smin), at_beta=float(bstar), span_beta0=float(s0),
                              gain_linear_max=S / float(smin), gain_U1_max=u1[0], gain_U1_argmax=u1[1:],
                              mean_g=means[cname],
                              mean_label="assm (MC estimate; no closed form)" if cname == "C2b_arith_call"
                              else "mod (closed form, binary64)",
                              sigma_res_mc=mc["controls"][cname]["sigma_res"], beta_star_mc=mc["controls"][cname]["beta_star"],
                              sigma_ratio_mc=mc["controls"][cname]["sigma_ratio"],
                              label="mod (certified lower bound on span from decimal witness values); sigma meas",
                              direction="0")
            row(dict(step="raw_span", case=case, control=cname, **{k: v for k, v in raw[cname].items()
                                                                     if not isinstance(v, tuple)}))
        # preintegrated payoff used as a control on the raw payoff (its mean is the price itself)
        cols, lam = pca_factor(na, nt)
        mu = drift(na, nt)
        v = cols[0]
        flat = lambda x: [x[i][j] for i in range(na) for j in range(nt)]
        vals_h = []
        for k, (zc, zi) in W.items():
            x = flat(logpaths(P, zc, zi))
            z0 = sum(v[c] * (x[c] - mu[c]) for c in range(na * nt)) / lam[0]
            a = [x[c] - v[c] * z0 for c in range(na * nt)]
            hval = pre_values(na, nt, a, v, nt - 1)[0]
            vals_h.append((Fraction(str(wv[k][0])), Fraction(repr(hval))))
        smin, bstar, s0 = min_over_beta_span(vals_h)
        raw["C4_preint_as_control"] = dict(S_res_lower_bound=float(smin), at_beta=float(bstar),
                                           gain_linear_max=S / float(smin),
                                           note="E[h] = price, so this is not a control with a known mean; "
                                                "shown only to confirm the jump argument covers smooth controls",
                                           label="mod", direction="0")
        row(dict(step="raw_span", case=case, control="C4_preint_as_control", **raw["C4_preint_as_control"]))
        # ---- preintegrated level (F04)
        Wp, zH_used = pre_witnesses(na, nt, cols, lam, mu)
        pv = {}
        for k, y in Wp.items():
            a = [mu[c] + sum(cols[kk][c] * y[kk] for kk in range(1, na * nt) if y[kk] != 0.0) for c in range(na * nt)]
            hval, gh, roots = pre_values(na, nt, a, v, nt - 1)
            pv[k] = (hval, gh, roots, a)
        h_hi_cert = h_lower_bound_decimal(na, nt, pv["y_hi"][3], v, pv["y_hi"][2]["z_K"], pv["y_hi"][2]["z_H"])
        vdates = [v[j] for j in range(nt)]
        hstar_pca = hstar_max(vdates, nt)
        hstar_univ = hstar_max([SIG * math.sqrt((j + 1) * MAT / nt) for j in range(nt)], nt)
        h_floor = min(pv[k][0] for k in Wp)
        pre = dict(h_at_witnesses={k: pv[k][0] for k in Wp}, h_hi_certified_lower=float(h_hi_cert),
                   z_H_profile=zH_used, max_abs_y_hi=max(abs(t) for t in Wp["y_hi"]),
                   sup_h_upper_bound_pca=hstar_pca[0], sup_h_upper_at_zH=hstar_pca[1],
                   sup_h_lower_bound_any_monotone_direction_unclamped=hstar_univ[0],
                   sigma_h_meas=sig[case]["sigma_preint"])
        S_h_lo = float(h_hi_cert) - max(0.0, h_floor)
        pre["replacement"] = dict(
            S_h_lower_bound=S_h_lo, S_h_upper_bound=hstar_pca[0],
            gain_linear_max=S / S_h_lo,
            gain_U1_max=math.sqrt(m_b * (S - m_b)) / math.sqrt(m_b * (S_h_lo - m_b)),
            gain_linear_min=S / hstar_pca[0],
            label="mod (lower bound certified in decimal at an explicit |y| <= 4.7 witness; upper bound analytic)",
            direction="0")
        pre_res = {}
        for cname in means:
            vals = [(Fraction(repr(pv[k][0])), Fraction(repr(pv[k][1][cname]))) for k in Wp]
            smin, bstar, s0 = min_over_beta_span(vals)
            u1 = u1_gain_sup(vals, price[case] - L1, price[case] + L1, means[cname], m_b, S)
            pre_res[cname] = dict(S_res_lower_bound=float(smin), at_beta=float(bstar), span_beta0=float(s0),
                                  gain_linear_max=S / float(smin), gain_U1_max=u1[0], label="mod", direction="0")
            row(dict(step="pre_residual_span", case=case, control=cname,
                     **{k: v for k, v in pre_res[cname].items()}))
        pre["residual_on_h"] = pre_res
        row(dict(step="pre_replacement", case=case, **pre["replacement"], z_H_profile=zH_used,
                 sup_h_upper_bound_pca=hstar_pca[0], sup_h_lower_any_monotone=hstar_univ[0]))
        # ---- net factors (binding cell is B8x52; desk D ratio is B8x52's)
        # The linear gain S/S_res applies to the no-U1 constant (k 353.0 at the binding cell), the U1 gain to
        # the U1 constant (k 197.6) that the thresholds use; M after a route is the smaller of the two.
        def net_row(gl, gu, dr):
            gmax = max(gl, gu)
            m_at = {t: min(v / gu, v * k_ratio / gl) for t, v in thresholds.items()}
            return dict(gain_linear=gl, gain_U1=gu, gain_max=gmax, D_ratio_floor=1.0, D_ratio_desk=dr,
                        net_max_at_D_floor=gmax, net_max_desk=gmax / dr,
                        M_after_at_D_floor=m_at, M_after_desk={t: v * dr for t, v in m_at.items()},
                        label="mod (gain bounds certified; D_ratio floor 1 is q+, desk ratio mod)")
        net = {}
        for cname, r in raw.items():
            if cname == "C4_preint_as_control":
                continue
            net[cname] = net_row(r["gain_linear_max"], r["gain_U1_max"], deff[cname]["D_ratio"])
        net["pre_h_replacement"] = net_row(pre["replacement"]["gain_linear_max"], pre["replacement"]["gain_U1_max"],
                                           deff["pre_h_replacement"]["D_ratio"])
        for cname, r in pre_res.items():
            net["pre_residual_" + cname] = net_row(r["gain_linear_max"], r["gain_U1_max"],
                                                   deff["pre_h_replacement"]["D_ratio"])
        best = max(net.items(), key=lambda t: t[1]["net_max_at_D_floor"])
        verdict = dict(best_route=best[0], best_net_factor_upper_bound=best[1]["net_max_at_D_floor"],
                       kill_threshold=4.0, killed=best[1]["net_max_at_D_floor"] < 4.0,
                       M_after_best_at_D_floor=best[1]["M_after_at_D_floor"],
                       M_after_best_desk=best[1]["M_after_desk"],
                       note="thresholds are the binding cell's (B8x52 $0.001); B4x12 rows are for completeness")
        result["cases"][case] = dict(
            witnesses={k: dict(f=float(wv[k][0]), controls={c: float(x) for c, x in wv[k][1].items()},
                               A=float(wv[k][2]["A"]), G=float(wv[k][2]["G"]),
                               max_basket=float(wv[k][2]["max_basket"]), S1T=float(wv[k][2]["S1T"]),
                               alive=wv[k][2]["alive"]) for k in W},
            control_means=means, geo_params=gpar, mc=mc, raw=raw, pre=pre, net=net, verdict=verdict,
            price=price[case], m_b=m_b)
        row(dict(step="verdict", case=case, **verdict, label="mod", direction="0"))
        print(case, "raw:", {k: round(r["gain_linear_max"], 4) for k, r in raw.items()})
        print(case, "raw U1:", {k: round(r.get("gain_U1_max", float("nan")), 4) for k, r in raw.items()})
        print(case, "pre replacement:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in pre["replacement"].items()})
        print(case, "pre residual:", {k: (round(r["gain_linear_max"], 3), round(r["gain_U1_max"], 3)) for k, r in pre_res.items()})
        print(case, "sup h: cert lower", float(h_hi_cert), "pca upper", hstar_pca, "any-monotone lower", hstar_univ)
        print(case, "verdict", verdict)
    result["desk_D_ratio_B8x52"] = deff
    with open(OUT / "p1_span.json", "x", encoding="utf-8") as f:
        json.dump(result, f, indent=1, default=str)


if __name__ == "__main__":
    main()
