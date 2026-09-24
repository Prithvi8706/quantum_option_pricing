"""Week-1 H1 decision: measured classical time-to-accuracy vs compiled knock-out oracle depth.

Classical: P3 (compiled, 16 worker processes, one scramble each, first-PC preintegration).
    n(eps) solves t_{.995,15} * A n^-r / sqrt(16) = 0.45 eps (A, r fitted in P3);
    T_C(eps) = per-scramble setup + n(eps) * measured per-point time (16 scrambles run
    concurrently on 16 workers, so wall time = one scramble's time).
Quantum: Q = k * sigma_Q / (0.45 eps) clean-source calls; 10x needs
    D_call <= D_max = T_C / (10 * Q * t_layer).
sigma_Q is the per-sample std of the estimand the Q1 oracle actually computes (plain
knock-out payoff, from P1). A smaller sigma (preintegrated estimand) would require the
oracle to run the Newton roots coherently and is reported only as a sensitivity.
Stop rule fixed in DECISION.md section 6 before this run: stop H1 if
D_min > 10 * D_max($0.001) at t_layer = 100 ns, k = 3, measured classical, every case.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "results", "advantage_frontier_20260923")
p1 = json.load(open(os.path.join(RES, "classical_exponent_pilot.json")))
p3 = json.load(open(os.path.join(RES, "barrier_fast_classical.json")))
q1 = json.load(open(os.path.join(RES, "barrier_oracle_depth.json")))
T995, SHARE = 2.947, 0.45


def classical_seconds(r3, eps):
    e = SHARE * eps
    n = max(2.0 ** 8, (r3["fit_constant"] * T995 / (4 * e)) ** (1 / r3["rate_r"]))
    m_max = max(int(k) for k in r3["median_scramble_seconds_to_prefix"])
    t_full = r3["median_scramble_seconds_to_prefix"][str(m_max)]
    setup = r3["median_setup_seconds"]
    per_point = (t_full - setup) / 2 ** m_max
    return setup + n * per_point, n, per_point


rows = []
for r3 in p3["results"]:
    case = "B%dx%d" % (r3["assets"], r3["dates"])
    p1case = next(r for r in p1["results"] if r["case"]["name"] == case)
    sig_plain = p1case["pointwise_std"]["barrier"]
    sig_pre = p1case["pointwise_std"]["barrier_pre"]
    depths = {(o["gaussians"], o["leaf_costs"]): o["clean_call_t_depth"]
              for o in q1["rows"] if o["case"] == case}
    for eps in (0.10, 0.03, 0.01, 0.001):
        tc, n, cpt = classical_seconds(r3, eps)
        for k in (1, 3, 10):
            for t_layer in (1e-8, 1e-7, 1e-6, 1e-5):
                for sname, sig in (("plain", sig_plain), ("preint_sensitivity", sig_pre)):
                    q = k * sig / (SHARE * eps)
                    dmax = tc / (10 * q * t_layer)
                    rows.append(dict(case=case, eps=eps, k=k, t_layer=t_layer, sigma_kind=sname,
                                     sigma_q=sig, classical_seconds=tc, points_per_scramble=n,
                                     seconds_per_point=cpt, quantum_calls=q, d_max=dmax,
                                     d_min_free_gaussian_favourable=depths[("free", "favourable")],
                                     d_min_boxmuller_favourable=depths[("box-muller",
                                                                        "favourable")],
                                     d_min_boxmuller_representative=depths[("box-muller",
                                                                            "representative")]))

stop = {}
for case in sorted({r["case"] for r in rows}):
    r = next(x for x in rows if x["case"] == case and x["eps"] == 0.001 and x["k"] == 3
             and x["t_layer"] == 1e-7 and x["sigma_kind"] == "plain")
    stop[case] = dict(d_max=r["d_max"], d_min_boxmuller=r["d_min_boxmuller_favourable"],
                      d_min_free_gaussian=r["d_min_free_gaussian_favourable"],
                      ratio_boxmuller=r["d_min_boxmuller_favourable"] / r["d_max"],
                      ratio_free_gaussian=r["d_min_free_gaussian_favourable"] / r["d_max"],
                      classical_seconds=r["classical_seconds"],
                      stop=r["d_min_boxmuller_favourable"] > 10 * r["d_max"])
decision = "STOP H1" if all(v["stop"] for v in stop.values()) else "CONTINUE (region survives)"
json.dump(dict(purpose=__doc__, stop_rule_case_results=stop, decision=decision, grid=rows),
          open(os.path.join(RES, "barrier_decision.json"), "w"), indent=1)

print("Stop rule at eps=$0.001, t_layer=100 ns, k=3, measured compiled classical:")
for case, v in stop.items():
    print("  %s: classical %.1f s; D_max %.3g; oracle %.3g (Box-Muller) / %.3g (free Gaussians);"
          " oracle/D_max = %.0fx / %.0fx; stop=%s" % (case, v["classical_seconds"], v["d_max"],
                                                   v["d_min_boxmuller"], v["d_min_free_gaussian"],
                                                   v["ratio_boxmuller"], v["ratio_free_gaussian"],
                                                   v["stop"]))
print("DECISION:", decision)
print("\nMost favourable corner in the grid (free Gaussians, k=1, 10 ns/T-layer, preint sigma):")
for case in sorted(stop):
    for eps in (0.01, 0.001):
        r = next(x for x in rows if x["case"] == case and x["eps"] == eps and x["k"] == 1
                 and x["t_layer"] == 1e-8 and x["sigma_kind"] == "preint_sensitivity")
        print("  %s eps=%g: D_max %.3g vs oracle %.3g -> %.1fx short" % (
            case, eps, r["d_max"], r["d_min_free_gaussian_favourable"],
            r["d_min_free_gaussian_favourable"] / r["d_max"]))
