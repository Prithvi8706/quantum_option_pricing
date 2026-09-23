"""Q1: minimal-depth coherent knock-out basket oracle in the project's reversible IR.

Builds the digital source Y = disc * (A - K)^+ * 1{max_j basket_j < H} with the SSA IR of
research/controlled_source_completion (same Box-Muller Gaussian generator, correlated
GBM increments, spot guard, fixed-point exp), but with depth-minimising choices:
  * Estrin (not Horner) evaluation of the degree-12 exp polynomial;
  * parallel-prefix (Hillis-Steele) accumulation of log-price increments over dates;
  * balanced-tree sums and a tree maximum over dates.
Each IR operation is charged the T-depth / T-count of certified leaves from the
range-specialised f=40 library of the controlled priority study:
  favourable     = cheapest leaf of that operation type (any operand ranges)
  representative = median leaf of that operation type
Critical path = longest weighted dependency path (unlimited parallelism, no routing,
no factory or reaction limits). A clean source call is charged forward + inverse = 2x.
These are compiler-specific sensitivity numbers, not lower bounds on all circuits.
"""

import glob
import json
import math
import os
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
from research.controlled_source_completion.ir import Graph  # noqa: E402
from research.controlled_source_completion.finance import normals_graph  # noqa: E402

LIB = os.path.join(ROOT, "results", "controlled_priority_completion", "range_compile_v1",
                   "leaves_f40")
OUT = os.path.join(ROOT, "results", "advantage_frontier_20260923", "barrier_oracle_depth.json")
SIGMA, CORR, S0, RATE, T, K, H = .3, .4, 100., .03, 1., 100., 140.


def tree(g, xs, op):
    xs = list(xs)
    while len(xs) > 1:
        nxt = [op(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
        if len(xs) % 2:
            nxt.append(xs[-1])
        xs = nxt
    return xs[0]


def exp_estrin(g, x):
    """Same range reduction as ir.Graph.exp; degree-12 Taylor polynomial by Estrin."""
    k = g.bits(g.cmul(x, 1 / math.log(2)), g.f, signed=True)
    r = g.sub(x, g.cmul(g.bits(k, -g.f), math.log(2)))
    coeffs = [g.c(1 / math.factorial(j)) for j in range(13)]
    level, power = coeffs, r
    while len(level) > 1:
        nxt = [g.add(level[i], g.mul(level[i + 1], power)) for i in range(0, len(level) - 1, 2)]
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
        if len(level) > 1:
            power = g.mul(power, power)
    return g.shift(level[0], k)


def build(na, nt, free_gaussians=False, q=32):
    g = Graph(40)
    count = nt * (na + 1)
    if free_gaussians:
        zs = [g.input("normal_%d" % i, 40, preparation="free") for i in range(count)]
    else:
        zs = normals_graph(g, count, q)
    dt = T / nt
    lo, hi = g.c(math.log(2 ** -16)), g.c(math.log(4096.))
    logs = []
    for i in range(na):
        steps = []
        for j in range(nt):
            common = g.cmul(zs[j * (na + 1)], SIGMA * math.sqrt(dt * CORR))
            idio = g.cmul(zs[j * (na + 1) + 1 + i], SIGMA * math.sqrt(dt * (1 - CORR)))
            steps.append(g.add(g.add(common, idio), g.c((RATE - .5 * SIGMA ** 2) * dt)))
        steps[0] = g.add(steps[0], g.c(math.log(S0)))
        d = 1                                                   # Hillis-Steele prefix sum
        while d < nt:
            steps = [steps[j] if j < d else g.add(steps[j], steps[j - d]) for j in range(nt)]
            d *= 2
        logs.append([g.clip(x, lo, hi) for x in steps])
    stocks = [[exp_estrin(g, logs[i][j]) for j in range(nt)] for i in range(na)]
    baskets = [g.cmul(tree(g, [stocks[i][j] for i in range(na)], g.add), 1 / na) for j in range(nt)]
    alive = g.lt(tree(g, baskets, g.maximum), g.c(H))
    average = g.cmul(tree(g, [s for row in stocks for s in row], g.add), 1 / (na * nt))
    payoff = g.cmul(g.pos(g.sub(average, g.c(K))), math.exp(-RATE * T))
    g.outputs = dict(Y=g.select(alive, payoff, g.c(0)))
    return g


def leaf_costs():
    by = {}
    for f in glob.glob(os.path.join(LIB, "*.json")):
        m = json.load(open(f))
        if "op" in m:
            r = m["resources"]
            by.setdefault(m["op"], []).append((r["t_depth"], r["t_count"]))
    fav = {op: (min(d for d, _ in v), min(c for _, c in v)) for op, v in by.items()}
    rep = {op: (statistics.median(d for d, _ in v), statistics.median(c for _, c in v))
           for op, v in by.items()}
    for table in (fav, rep):
        table["sub"] = table["add"]
        table["input"] = table["const"] = (0, 0)
    return fav, rep


def score(g, table):
    arrival = {}
    tcount = 0
    ops = {}
    for node in g.nodes:
        d, c = table[node["op"]]
        start = max((arrival[a] for a in node["args"]), default=0)
        for o in node["out"]:
            arrival[o] = start + d
        tcount += c
        ops[node["op"]] = ops.get(node["op"], 0) + 1
    forward = max(arrival[v] for v in g.outputs.values())
    return dict(forward_critical_t_depth=forward, clean_call_t_depth=2 * forward,
                forward_t_count=tcount, clean_call_t_count=2 * tcount, op_counts=ops)


def main():
    fav, rep = leaf_costs()
    rows = []
    for na, nt in ((4, 12), (8, 52)):
        for free in (False, True):
            g = build(na, nt, free_gaussians=free)
            for name, table in (("favourable", fav), ("representative", rep)):
                s = score(g, table)
                gauss = "free" if free else "box-muller"
                rows.append(dict(case="B%dx%d" % (na, nt), gaussians=gauss,
                                 leaf_costs=name, nodes=len(g.nodes), **s))
                print("%-6s %-10s %-14s forward depth %10.4g  clean call depth %10.4g"
                      "  call T-count %10.4g"
                      % (rows[-1]["case"], gauss, name, s["forward_critical_t_depth"],
                         s["clean_call_t_depth"], s["clean_call_t_count"]))
    json.dump(dict(purpose=__doc__, leaf_library=os.path.relpath(LIB, ROOT),
                   leaf_costs=dict(favourable=fav, representative=rep), rows=rows),
              open(OUT, "w"), indent=1, default=float)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
