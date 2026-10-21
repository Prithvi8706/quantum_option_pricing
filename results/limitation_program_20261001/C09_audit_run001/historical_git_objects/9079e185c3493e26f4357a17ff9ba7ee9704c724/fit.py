"""Rate fits, whole-scramble bootstrap and n(eps) for item C1 (ANALYSIS_SPEC_STAGE_C.md).

prefix: array (scrambles, len(ms)) of per-scramble prefix means at n = 2^m.
"""

import numpy as np
from scipy.stats import t as student_t

T995_15 = float(student_t.ppf(0.995, 15))
SHARE = 0.45
EPS = (0.10, 0.03, 0.01, 0.001)
BOOTSTRAP = 4000
BOOT_ROOT = 2026100112


def windows(m_top):
    """Primary window first, then the sensitivity windows of the spec."""
    out = {"primary": (10, m_top), "w8": (8, m_top), "w12": (12, m_top)}
    if m_top >= 19:
        out["w14"] = (14, m_top)
    return out


def ols_rate(ms, sd, window):
    """OLS of log sd on log n over m in [lo, hi]; returns (A, r) with sd ~ A n^-r."""
    lo, hi = window
    sel = [i for i, m in enumerate(ms) if lo <= m <= hi]
    x = np.log(2.0 ** np.asarray(ms, dtype=float)[sel])
    slope, icpt = np.polyfit(x, np.log(np.asarray(sd)[sel]), 1)
    return float(np.exp(icpt)), float(-slope)


def bootstrap_index(case_index, scrambles):
    rng = np.random.default_rng([BOOT_ROOT, case_index, 0, 0, 0])
    return rng.integers(0, scrambles, size=(BOOTSTRAP, scrambles))


def bootstrap_rates(ms, prefix, window, index):
    """Joint (A, r) for every resample of whole scrambles (rows of `index`)."""
    out = np.empty((len(index), 2))
    for b, rows in enumerate(index):
        out[b] = ols_rate(ms, prefix[rows].std(0, ddof=1), window)
    return out


def n_eps(A, r, eps):
    """Points per scramble with t_{.995,15} A n^-r / sqrt(16) = 0.45 eps (no floor)."""
    return (T995_15 * A / (4.0 * SHARE * eps)) ** (1.0 / r)


def c2_label(r_lo, r_hi, threshold=0.9):
    """Claim C2 rule on the primary-window bootstrap 95% interval."""
    if r_lo >= threshold:
        return "restores"
    if r_hi < threshold:
        return "does_not_restore"
    return "inconclusive"


def summarize(ms, prefix, case_index, reference_prefix=None):
    """Fits, intervals, n(eps) and flags for one (case, basis, estimand).

    reference_prefix: the canonical-basis prefix array of the same case and estimand, for
    the paired interval of r - r_canonical (same bootstrap index matrix)."""
    m_top = max(ms)
    sd = prefix.std(0, ddof=1)
    index = bootstrap_index(case_index, prefix.shape[0])
    fits = {name: ols_rate(ms, sd, w) for name, w in windows(m_top).items()}
    A, r = fits["primary"]
    boot = bootstrap_rates(ms, prefix, windows(m_top)["primary"], index)
    r_lo, r_hi = np.percentile(boot[:, 1], [2.5, 97.5])
    out = dict(
        price=float(prefix[:, -1].mean()),
        std_error=float(prefix[:, -1].std(ddof=1) / np.sqrt(prefix.shape[0])),
        sd_one_scramble=sd.tolist(),
        fits={k: dict(A=a, r=rr) for k, (a, rr) in fits.items()},
        local_slopes=(-np.diff(np.log(sd)) / np.log(2.0)).tolist(),
        r_ci95=[float(r_lo), float(r_hi)],
        A_ci95=[float(x) for x in np.percentile(boot[:, 0], [2.5, 97.5])],
        c2_label=c2_label(r_lo, r_hi),
        n_eps={},
    )
    for eps in EPS:
        n = n_eps(A, r, eps)
        draws = n_eps(boot[:, 0], boot[:, 1], eps)
        out["n_eps"][str(eps)] = dict(
            point=float(n), ci95=[float(x) for x in np.percentile(draws, [2.5, 97.5])],
            flag="extrapolated-high" if n > 2.0 ** m_top else
                 "extrapolated-low" if n < 2.0 ** 10 else "in-range",
            fraction_outside=float(np.mean((draws > 2.0 ** m_top) | (draws < 2.0 ** 10))))
    if reference_prefix is not None:
        ref = bootstrap_rates(ms, reference_prefix, windows(m_top)["primary"], index)
        diff = boot[:, 1] - ref[:, 1]
        out["r_minus_canonical_ci95"] = [float(x) for x in np.percentile(diff, [2.5, 97.5])]
    return out
