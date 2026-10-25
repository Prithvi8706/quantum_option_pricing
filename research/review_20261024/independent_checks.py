"""Independent numerical checks for the 24 October 2026 review of P2, A2a and U1.

This is an AI review aid, not a human review. It recomputes the key numbers by different routes from the authors':
  P2  (a) DPSS optimality: no window of 2N+1 taps can beat the top eigenvalue of the band-limiting matrix, so the
          Kaiser leakage must lie above it, and both must lie below the certified target;
      (b) exact discrete Kaiser leakage by FFT autocorrelation at N from 800 to 2.98e5;
      (c) the parts 1-2 lower bound re-implemented in mpmath from P2_DERIVATION.md (adaptive quadrature, not the
          authors' midpoint rule), compared with the recorded certified value;
      (d) N and k at the binding cell from the closed-form root of the Delta quadratic;
      (e) the parts 3-4 budget with a more conservative rotation count (3 per controlled phase).
  U1  (f) EB upper bound recomputed at 60 digits from the saved totals, and the headroom before N changes;
      (g) a fresh sample from a different generator family (Philox) to test the iid premise empirically.
  A2a (h) total and Bernstein exponents recomputed from the certificate's component values.

Run (repo root; numpy/scipy/mpmath needed, so no -S):
  .context/frontier_t0_env/Scripts/python.exe -I -B research/review_20261024/independent_checks.py run001
"""
import hashlib
import json
import math
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.linalg import eigh
from scipy.signal.windows import dpss

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "review_20261024"
IN = dict(
    p2=ROOT / "results/frontier_probe_20261021/p2/run002/p2_window.json",
    sigma=ROOT / "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
    c1=ROOT / "results/frontier_classical_20261001/c1/c1_summary.json",
    eb=ROOT / "results/claim_debts_20261022/u1/run001/eb_sample.json",
    u1=ROOT / "results/claim_debts_20261022/u1/run001/u1_certificate.json",
    a2a=ROOT / "results/claim_debts_20261022/a2a/run001/certificate.json",
)
BETA, C, DELTA, RESERVE = 3.87, 4.179, 0.003, 4e-6
TARGET = DELTA - RESERVE
N_BIND = 100924
S = F(8192, 211)
E = F(9, 20) * F(1, 1000)
READOUT = F(1, 2 ** 39)
L1 = F(45202052, 10 ** 9)
A2A_BIAS = F(6703058386012589, 2 ** 64)


def kaiser(N, beta=BETA):
    n = np.arange(-N, N + 1, dtype=np.float64)
    w = np.i0(beta * np.sqrt(np.maximum(0.0, 1.0 - (n / N) ** 2)))
    w[0] = w[-1] = 0.5
    return w


def leak_fft(w, D):
    """1 - (in-band energy fraction) for taps w and half-band D (radians), exact up to float64 rounding."""
    L = w.size
    f = np.fft.rfft(w, n=2 * L)
    r = np.fft.irfft(f * np.conj(f), n=2 * L)[:L]
    d = np.arange(1, L, dtype=np.float64)
    inband = r[0] * D / math.pi + 2.0 * np.sum(r[1:] * np.sin(d * D) / (math.pi * d))
    return 1.0 - inband / r[0]


def dense_checks(N):
    """Top eigenvalue of the (2N+1)-tap band-limiting matrix and the Kaiser Rayleigh quotient on the same matrix."""
    D = C / N
    idx = np.arange(-N, N + 1)
    diff = (idx[:, None] - idx[None, :]).astype(np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        A = np.where(diff == 0, D / math.pi, np.sin(D * diff) / (math.pi * diff))
    M = A.shape[0]
    lam_opt = eigh(A, eigvals_only=True, subset_by_index=[M - 1, M - 1])[0]
    w = kaiser(N)
    lam_k = float(w @ A @ w / (w @ w))
    return dict(N=N, dpss_leak_dense=1 - lam_opt, kaiser_leak_dense=1 - lam_k, kaiser_leak_fft=leak_fft(w, D))


def dpss_leak(N):
    M = 2 * N + 1
    NW = M * (C / N) / (2 * math.pi)
    _, ratio = dpss(M, NW, Kmax=1, return_ratios=True)
    return 1 - float(ratio[0])


def p2_bound(N, c=C, beta=BETA):
    """Parts 1-2 lower bound on lambda0(N, c/N) for gamma = 0, written from P2_DERIVATION.md section 3."""
    mp.mp.dps = 40
    N, c, b = mp.mpf(N), mp.mpf(str(c)), mp.mpf(str(beta))
    b2 = b * b

    def Phi(eta):
        q = b2 - eta * eta
        if q > 0:
            s = mp.sqrt(q)
            return 2 * mp.sinh(s) / s
        if q < 0:
            s = mp.sqrt(-q)
            return 2 * mp.sin(s) / s
        return mp.mpf(2)

    phi0 = Phi(mp.mpf(0))
    I_tot = 2 * mp.pi * mp.quad(lambda x: mp.besseli(0, b * mp.sqrt(1 - x * x)) ** 2, [-1, 0, 1])
    I_c = 2 * mp.quad(lambda e: Phi(e) ** 2, [0, min(c, b), c] if c > b else [0, c])
    eta_min = N * mp.pi
    s_min = mp.sqrt(eta_min ** 2 - b2)
    kappa = (1 + 1 / s_min) / (1 - b2 / eta_min ** 2)
    alias = b2 * kappa / (4 * N)
    C_R = alias + 2 / mp.pi
    eta1 = 2 * b
    A1 = 2 / ((1 + mp.sqrt(3) / 2) * (mp.sqrt(3) / 2)) * b2 * (1 + 2 / (mp.sqrt(3) * eta1))
    phi1_0 = phi0 - 2
    L1Phi = 2 * (eta1 * phi1_0 + A1 / eta1) + 4 * (1 + mp.log(N * mp.pi))
    L1etaPhi = 2 * (eta1 ** 2 * phi1_0 / 2 + A1 * mp.log(N * mp.pi / eta1)) + 8 * N
    X = (alias * L1Phi + (2 / mp.pi ** 2) * L1etaPhi / N) / mp.pi
    X_band = (alias + (2 / mp.pi ** 2) * c / N) * 2 * c * phi0 / mp.pi
    lam = (N * I_c / (2 * mp.pi) - X_band) / (N * I_tot / (2 * mp.pi) + X + C_R ** 2)
    return lam, dict(I_tot=I_tot, I_c=I_c, A1=A1, C_R=C_R, X=X, X_band=X_band)


def delta_closed(m):
    """Largest Delta with sqrt(m (S - m)) Delta + S Delta^2 / 4 + 2^-39 <= e: the positive root, at 60 digits."""
    mp.mp.dps = 60
    A = mp.sqrt(mp.mpf(m.numerator) / m.denominator * (mp.mpf(S.numerator) / S.denominator - mp.mpf(m.numerator) / m.denominator))
    Sm = mp.mpf(S.numerator) / S.denominator
    r = mp.mpf((E - READOUT).numerator) / (E - READOUT).denominator
    return (-A + mp.sqrt(A * A + Sm * r)) / (Sm / 2)


def budget34(N, c=C, per_cphase=3):
    g = math.ceil(math.log2(2 * N + 1))
    G, K = 2 ** g, 2 ** 40
    eps3 = (2 * N + 1) * (1 + 4 * c) / (G * K)
    n_rot = 2 ** g + 2 * (g + 1) + per_cphase * g * (g - 1) // 2
    eps_state = n_rot * 2.0 ** -40 + 2 ** g * 4e-15
    return dict(N=N, g=g, eps3=eps3, eps3_worst_case_over_G=(1 + 4 * c) / K, n_rotations=n_rot,
                delta_34=eps3 + 2 * eps_state, within_4e_6=eps3 + 2 * eps_state <= 4e-6)


def philox_sample(n, seed):
    """Same contract as u1/eb_sample.py, but an independent generator family (Philox) and seed."""
    na, nt, s0, k, h, sig, rho, r, T = 8, 52, 100.0, 100.0, 140.0, 0.3, 0.4, 0.03, 1.0
    rng = np.random.Generator(np.random.Philox(seed))
    dt = T / nt
    t = dt * np.arange(1, nt + 1)
    s1, s2, done = [], [], 0
    while done < n:
        m = min(2 ** 15, n - done)
        w0 = np.cumsum(rng.standard_normal((m, nt)), axis=1) * math.sqrt(dt)
        wi = np.cumsum(rng.standard_normal((m, na, nt)), axis=2) * math.sqrt(dt)
        x = math.log(s0) + (r - 0.5 * sig * sig) * t + sig * (math.sqrt(rho) * w0[:, None, :] + math.sqrt(1 - rho) * wi)
        b = np.exp(x).mean(axis=1)
        y = math.exp(-r * T) * np.maximum(b.mean(axis=1) - k, 0.0) * (b < h).all(axis=1)
        s1.append(math.fsum(y.tolist()))
        s2.append(math.fsum((y * y).tolist()))
        done += m
    S1, S2 = math.fsum(s1), math.fsum(s2)
    return dict(n=n, mean=S1 / n, var=(S2 - S1 * S1 / n) / (n - 1), seed=seed, generator="Philox")


def main(run):
    sys.set_int_max_str_digits(0)
    out = OUT / run
    out.mkdir(parents=True, exist_ok=False)
    data = {k: json.loads(p.read_text(encoding="utf-8")) for k, p in IN.items()}
    res = dict(meta=dict(script="research/review_20261024/independent_checks.py", python=sys.version,
                         numpy=np.__version__, mpmath=mp.__version__,
                         inputs_sha256={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in IN.items()},
                         label="AI review aid (not a human review); float64 unless stated"))
    t0 = time.perf_counter()

    # P2 (a)+(b): optimality and exact discrete leakage
    dense = [dense_checks(N) for N in (800, 2000)]
    for d in dense:
        d["dpss_leak_scipy"] = dpss_leak(d["N"])
    sweep = []
    for N in (800, 1000, 4096, 20000, N_BIND, 298456):
        lk = leak_fft(kaiser(N), C / N)
        sweep.append(dict(N=N, kaiser_leak=lk, dpss_leak=dpss_leak(N), below_target=lk <= TARGET))
    res["p2_optimality_and_leakage"] = dict(c=C, beta=BETA, target=TARGET, dense=dense, sweep=sweep,
                                            kaiser_above_dpss=all(s["kaiser_leak"] >= s["dpss_leak"] for s in sweep),
                                            all_below_target=all(s["below_target"] for s in sweep))

    # P2 (c): re-implemented analytic bound vs recorded certified value
    rec = F(data["p2"]["certified"]["delta=3/1000|gamma=0|with_impl_budget"]["lambda_lower_N0"])
    lam800, parts = p2_bound(800)
    lam_bind, _ = p2_bound(N_BIND)
    true800 = 1 - dense[0]["kaiser_leak_dense"]
    res["p2_bound_reimplemented"] = dict(
        lambda_lower_N800_mine=float(lam800), lambda_lower_N800_recorded=float(rec),
        recorded_le_mine=float(rec) <= float(lam800), mine_le_true=float(lam800) <= true800,
        lambda_true_N800=true800, lambda_lower_Nbind_mine=float(lam_bind),
        mine_meets_target_at_800=float(lam800) >= 1 - TARGET,
        parts={k: float(v) for k, v in parts.items()})

    # P2 (d): N and k at the binding cell
    sig = F(str(data["sigma"]["cases"]["B8x52"]["sigma_q"]))
    m_p2 = F(str(data["c1"]["port_check"]["B8x52"]["price"])) + L1
    D = delta_closed(m_p2)
    N = int(mp.ceil(mp.mpf(str(C)) / D))
    res["p2_k"] = dict(m_p2=float(m_p2), Delta=float(D), N=N, N_matches=N == N_BIND,
                       k=float(N * E / sig), sigma_over_e=float(sig / E))

    # P2 (e): parts 3-4 with 3 rotations per controlled phase
    res["p2_parts34"] = [budget34(n) for n in (N_BIND, 298456, 2 ** 19, 2 ** 20 - 1)]

    # U1 (f): EB bound at 60 digits from the saved totals
    mp.mp.dps = 60
    eb = data["eb"]
    n = eb["n"]
    s1, s2 = F(eb["sum"]), F(eb["sum_sq"])
    mean = s1 / n
    var = (s2 - s1 * s1 / n) / (n - 1)
    lg = mp.log(mp.mpf(2) / mp.mpf("1e-4"))
    hw = mp.sqrt(2 * (mp.mpf(var.numerator) / var.denominator) * lg / n) + 7 * 40 * lg / (3 * (n - 1))
    ucb = mp.mpf(mean.numerator) / mean.denominator + mp.mpf("1e-9") + hw
    m_cert = ucb + mp.mpf(A2A_BIAS.numerator) / A2A_BIAS.denominator
    rec_m = F(int(data["u1"]["m_cert"][0]), int(data["u1"]["m_cert"][1]))
    # largest mean that still gives N <= N_BIND at c = 4.179
    Dstar = mp.mpf(str(C)) / N_BIND
    Sm = mp.mpf(S.numerator) / S.denominator
    Amax = (mp.mpf((E - READOUT).numerator) / (E - READOUT).denominator - Sm * Dstar ** 2 / 4) / Dstar
    m_max = (Sm - mp.sqrt(Sm * Sm - 4 * Amax ** 2)) / 2
    res["u1_recompute"] = dict(mean=float(mean), var_unbiased=float(var), half_width=float(hw), ucb=float(ucb),
                               m_cert=float(m_cert),
                               m_cert_recorded=float(rec_m), agrees=abs(float(rec_m) - float(m_cert)) < 1e-12,
                               m_max_same_N=float(m_max), headroom=float(m_max - m_cert),
                               headroom_in_half_widths=float((m_max - m_cert) / hw))

    # U1 (g): independent generator family
    ph = philox_sample(2 ** 22, seed=20261024)
    se = math.sqrt(ph["var"] / ph["n"])
    se_pcg = math.sqrt(float(var) / n)
    ph["z_vs_pcg64"] = (ph["mean"] - float(mean)) / math.hypot(se, se_pcg)
    ph["below_m_cert"] = ph["mean"] <= float(m_cert)
    res["u1_philox"] = ph

    # A2a (h): total and tail exponents from the certificate's own component values
    case = data["a2a"]["cases"]["B8x52"]
    ex = {k: F(*case[k]["exact"]) for k in ("H_price", "zeta_noclip", "switch_noclip", "P_fin_C_upper", "total_clip_split")}
    total = ex["H_price"] + ex["zeta_noclip"] + 40 * min(F(1), ex["P_fin_C_upper"] + ex["switch_noclip"])
    Bmax = data["a2a"]["constants"]["B_internal_radius_upper"]["float"]
    Mb = Bmax * math.sqrt(2 * 27 / (500 * 52))
    exps = []
    for srow in case["sites"]:
        if srow.get("clipable_sites"):
            s, V = srow["s_lower"], srow["variance_upper"]
            exps.append(dict(elapsed_dates=srow["elapsed_dates"], sites=srow["clipable_sites"],
                             exponent=s * s / (2 * (V + Mb * s / 3))))
    pc = sum(r["sites"] * math.exp(-r["exponent"]) for r in exps)
    res["a2a_recompute"] = dict(total=float(total), total_matches=total == ex["total_clip_split"],
                                meets_0p55eps=total <= F(11, 20000), clipable_sites=sum(r["sites"] for r in exps),
                                min_exponent=min(r["exponent"] for r in exps), P_C_float=pc,
                                P_C_le_1e_29=pc <= 1e-29, exponents=exps)
    res["wall_s"] = time.perf_counter() - t0
    with open(out / "checks.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in res.items() if k != "meta"}, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main(sys.argv[1])
