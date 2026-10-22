"""F06 / F07 screens (register: activated by TRIG-F31-10x), CPU, plain MC in the canonical factor.

F07 (rare-event proposals): is the price rare-event dominated? Knock-out probability, P(f > 0), and the share of the
price carried by the top 1% / 0.1% of payoffs. Importance sampling pays only if a small-probability region carries
most of the price (it does not if the share is spread).
F06 (active barrier-date switching surface): for the preintegrated estimand, which date's barrier root binds
(argmin_j z_j), how concentrated that is, and how often the two smallest roots are within 0.05 in z (the switching
surface where h has kinks, which is what limits the RQMC rate after preintegration).
Run (repo root, Stage C env without -I):
  .context/frontier_t0_env/Scripts/python.exe -m research.c10_challengers_20261022.f06_f07_screen <out_json>
"""
import research.frontier_classical_20261001.scrambles as sc  # noqa: I001

import json
import math
import sys

import numpy as np

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_plain


def main(out):
    res = {}
    for case in (sc.Case(0, 4, 12), sc.Case(1, 8, 52)):
        rng = np.random.default_rng([2026102201, case.case_index, 11, 0, 0])
        L, _ = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)
        mu = sc.drift(case)
        disc = math.exp(-case.rate * case.maturity)
        n = 1 << 18
        v = L[:, 0]
        vdate = v[:case.nt]
        fl, kol, Al, actl, gapl = [], [], [], [], []
        for _ in range(n // 8192):
            z = rng.standard_normal((8192, case.dim))
            x = z @ L.T + mu
            fl.append(knockout_plain(x, case.na, case.nt, disc, case.strike, case.barrier))
            bask = np.exp(x).reshape(8192, case.na, case.nt).mean(axis=1)
            Al.append(bask.mean(axis=1))
            kol.append((bask >= case.barrier).any(axis=1))
            a = x - np.outer(z[:, 0], v)
            bs = np.exp(a).reshape(8192, case.na, case.nt).sum(axis=1)
            roots = (np.log(case.na * case.barrier) - np.log(bs)) / vdate[None, :]
            order = np.argsort(roots, axis=1)
            actl.append(order[:, 0])
            gapl.append(np.take_along_axis(roots, order[:, 1:2], 1)[:, 0] - np.take_along_axis(roots, order[:, :1], 1)[:, 0])
        f, ko, A, act, gap = (np.concatenate(t) for t in (fl, kol, Al, actl, gapl))
        fs = np.sort(f)[::-1]
        price = f.mean()
        top = {q: float(fs[: int(q * n)].sum() / fs.sum()) for q in (0.001, 0.01, 0.1)}
        hist = np.bincount(act, minlength=case.nt) / n
        res[case.name] = dict(
            n=n, price=float(price), p_knockout=float(ko.mean()), p_payoff_positive=float((f > 0).mean()),
            p_in_money_no_barrier=float((A > case.strike).mean()), top_share_of_price=top,
            F07_rare_event_dominated=bool(top[0.01] > 0.5),
            active_date_hist=hist.tolist(), active_date_top3=[int(i) for i in np.argsort(hist)[::-1][:3]],
            active_date_top3_share=float(np.sort(hist)[::-1][:3].sum()),
            p_root_gap_lt_0_05=float((gap < 0.05).mean()), p_root_gap_lt_0_2=float((gap < 0.2).mean()),
            label="meas (plain MC, 2^18 iid paths)")
        r = res[case.name]
        print(case.name, "price", round(r["price"], 4), "P(KO)", round(r["p_knockout"], 3), "P(f>0)",
              round(r["p_payoff_positive"], 3), "top1%", round(top[0.01], 3), "active top3", r["active_date_top3"],
              round(r["active_date_top3_share"], 3), "P(gap<0.05)", round(r["p_root_gap_lt_0_05"], 3), flush=True)
    with open(out, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
