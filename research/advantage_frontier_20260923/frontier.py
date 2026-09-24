"""Frontier calculation from pilot P1 (best classical barrier method = global-PCA preintegration).

For the best classical barrier estimator, T_C(eps) = 16 * n(eps) * c_pt with RQMC error
sd(n) = A n^-r (fitted in P1). A variance-sensitive quantum estimator needs Q = k sigma_q / e_stat
calls. The 10x condition gives the largest T-depth per complete coherent call:
    D_max(eps) = T_C(eps) / (10 * Q * t_layer).
Classical speed-up factor g models a faster classical implementation than single-thread numpy
(g = 1 numpy as measured; g = 16 one 16-core CPU; g = 100 a single modern GPU, cf. STAC-A2).
Then the precision at which D_max reaches a given oracle depth D_oracle is solved for.
"""
import json
import math
import os

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results",
                       "advantage_frontier_20260923")
p1 = json.load(open(os.path.join(RESULTS, "classical_exponent_pilot.json")))
t995, share = 2.947, 0.45
rows = []
for res in p1["results"]:
    m = res["methods"]["barrier/preint"]
    A, r = m["fit_constant"], m["rate_r"]
    c_pt = res["seconds_per_point_with_preint"]
    sig = res["pointwise_std"]["barrier_pre"]
    def dmax(eps, k, t_layer, g):
        e = share * eps
        # continuous n (no power-of-two rounding)
        n = max(64.0, (A / (e * 4 / t995)) ** (1 / r))
        tc = 16 * n * c_pt / g
        return tc / (10 * k * sig / e * t_layer)
    for g in (1, 16, 100):
        for k in (1, 3, 10):
            for tl in (1e-7, 1e-6, 1e-5):
                d01 = dmax(0.01, k, tl, g)
                # eps where D_max = 1e4 (literature-best depth order), 1.2e7 (project best)
                sol = {}
                for D in (1e4, 1.2e7):
                    lo, hi = 1e-12, 0.01
                    if dmax(0.01, k, tl, g) >= D:
                        sol[D] = 0.01
                        continue
                    for _ in range(200):
                        mid = math.sqrt(lo * hi)
                        if dmax(mid, k, tl, g) >= D:
                            lo = mid
                        else:
                            hi = mid
                    sol[D] = lo
                rows.append(dict(case=res["case"]["name"], rate=r, g=g, k=k, t_layer=tl,
                                 Dmax_at_1cent=d01, eps_for_D1e4=sol[1e4],
                                 eps_for_D1p2e7=sol[1.2e7]))
json.dump(rows, open(os.path.join(RESULTS, "frontier.json"), "w"), indent=1)
print("%-6s %5s %4s %3s %7s | %11s | %13s %13s"
      % ("case", "rate", "g", "k", "t_layer", "Dmax@$0.01", "eps(D=1e4)", "eps(D=1.2e7)"))
for x in rows:
    if x["k"] in (1, 10) and x["t_layer"] in (1e-7, 1e-6):
        print("%-6s %5.3f %4d %3d %7.0e | %11.3g | %13.3g %13.3g"
              % (x["case"], x["rate"], x["g"], x["k"], x["t_layer"], x["Dmax_at_1cent"],
                 x["eps_for_D1e4"], x["eps_for_D1p2e7"]))
