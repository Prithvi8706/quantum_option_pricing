"""C10 screen: control variates on top of the classical preintegration (iid sigma ratio, B8x52 and B4x12).

h(y) = E[f | y] (first PCA direction integrated) and preintegrated controls g_hat(y) with closed-form means:
geometric Asian call, linear average, arithmetic call (mean by MC; assm), asset-1 terminal knock-out, geometric-average
knock-out, plus all of them jointly (multiple regression). Reports sigma_h / sigma_residual (meas, plain MC over y).
A ratio rho means about rho^2 fewer iid points for the same error; under RQMC the gain is indicative only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/cv_screen.py <out_json>
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "frontier_probe_20261021"))
import p1_control_span as p1  # noqa: E402


def solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[c][c] != 0:
                fac = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= fac * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def main(out):
    res = {}
    for case, (na, nt) in p1.CASES.items():
        P = p1.params(na, nt)
        cols, lam = p1.pca_factor(na, nt)
        mu = p1.drift(na, nt)
        v = cols[0]
        d = na * nt
        rng = random.Random(20261022)
        n = 4096
        H, G = [], []
        l0 = math.log(p1.S0)
        for _ in range(n):
            x = [0.0] * d
            lv = [l0] * na
            for j in range(nt):
                zc = rng.gauss(0.0, 1.0)
                for i in range(na):
                    lv[i] += P["m"] + P["a"] * zc + P["b"] * rng.gauss(0.0, 1.0)
                    x[i * nt + j] = lv[i]
            z0 = sum(v[c] * (x[c] - mu[c]) for c in range(d)) / lam[0]
            a = [x[c] - v[c] * z0 for c in range(d)]
            h, g, _ = p1.pre_values(na, nt, a, v, nt - 1)
            H.append(h)
            G.append(g)
        names = list(G[0])
        mh = sum(H) / n
        vh = sum((h - mh) ** 2 for h in H) / (n - 1)
        out_c = dict(n=n, sigma_h=math.sqrt(vh), mean_h=mh, single={}, label="meas (plain MC over y)")
        for k in names:
            g = [x[k] for x in G]
            mg = sum(g) / n
            cov = sum((h - mh) * (gi - mg) for h, gi in zip(H, g)) / (n - 1)
            vg = sum((gi - mg) ** 2 for gi in g) / (n - 1)
            beta = cov / vg if vg > 0 else 0.0
            vr = vh - beta * cov
            out_c["single"][k] = dict(beta=beta, corr=cov / math.sqrt(vg * vh) if vg > 0 else 0.0,
                                      sigma_ratio=math.sqrt(vh / max(vr, 1e-300)))
        # joint regression on all controls
        X = [[x[k] for k in names] for x in G]
        mx = [sum(r[i] for r in X) / n for i in range(len(names))]
        C = [[sum((r[i] - mx[i]) * (r[j] - mx[j]) for r in X) / (n - 1) for j in range(len(names))] for i in range(len(names))]
        c = [sum((r[i] - mx[i]) * (h - mh) for r, h in zip(X, H)) / (n - 1) for i in range(len(names))]
        try:
            beta = solve(C, c)
            vr = vh - sum(bi * ci for bi, ci in zip(beta, c))
            out_c["joint"] = dict(beta=dict(zip(names, beta)), sigma_ratio=math.sqrt(vh / max(vr, 1e-300)))
        except ZeroDivisionError:
            out_c["joint"] = None
        res[case] = out_c
        print(case, "sigma_h", round(out_c["sigma_h"], 4),
              {k: round(v_["sigma_ratio"], 3) for k, v_ in out_c["single"].items()},
              "joint", round(out_c["joint"]["sigma_ratio"], 3) if out_c["joint"] else None, flush=True)
    with open(out, "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
