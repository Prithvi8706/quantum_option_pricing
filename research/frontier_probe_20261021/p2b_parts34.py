"""P2 run002: parts 3 and 4 of the open window problem made explicit, then c and k re-certified.

Part 3 (finite readout, worst case over phase). Register of G = 2^g >= 2N + 1 points; a known offset
tau = 2 pi l / (G K), l uniform on {0..K-1} (classical randomness; applied as the diagonal e^{i n tau} on the window
register, query-free). For eigenphase phi the success probability is the lattice sum
    P(phi) = (h / 2pi) sum_{u in (phi + h Z), |u| <= Delta} F(u),  h = 2pi / (G K),  F = W^2 / ||w||^2,
because outcome j has probability F(phi + tau - 2 pi j / G) / G exactly when G >= 2N + 1. A lattice sum differs from
the integral by at most h (TV_[-D,D] F + sup F), with sup F <= (sum|w|)^2 / sum w^2 <= 2N + 1 and
|F'| <= 2 N (2N + 1), so
    P(phi) >= lambda0 - eps3,   eps3 = (2N + 1)(1 + 4c) / (G K)   for EVERY phi.
Part 4 (implementation precision). Every non-oracle gate is either Clifford+T exact or a rotation synthesised to
operator-norm error eps_r (Ross-Selinger, arXiv:1403.2975: T-count about 3 log2(1/eps_r)). Operator-norm errors add
along the circuit and a success probability moves by at most 2 x (state error):
    window preparation (binary tree of uniformly controlled rotations): <= 2^g rotations, each eps_r, plus angle
        rounding from binary64 (<= 4e-15 rad each);
    offset diagonal: <= 2 (g + 1) rotations;  inverse QFT on g qubits: g (g - 1) / 2 controlled rotations,
        each two rotations.
The controlled powers of Q are the oracle (exact in the cost model; its arithmetic bias sits in the 0.55 eps bias
reserve, not in delta). delta_34 = eps3 + 2 eps_state <= 4e-6 for every cell (asserted) replaces the assumed 1e-4 of run001.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p2b_parts34.py
"""
import hashlib
import json
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2_window_constant as p2  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "results" / "frontier_probe_20261021" / "p2" / "run002"
RUN1 = ROOT / "results" / "frontier_probe_20261021" / "p2" / "run001" / "p2_window.json"
EPS_R = Fraction(1, 2 ** 40)
Q_OFFSET = 40
ANGLE_ROUND = Fraction(4, 10 ** 15)


def budgets(N, c):
    g = math.ceil(math.log2(2 * N + 1))
    G = 2 ** g
    K = 2 ** Q_OFFSET
    eps3 = Fraction(2 * N + 1) * (1 + 4 * Fraction(str(c))) / (G * K)
    n_rot = 2 ** g + 2 * (g + 1) + g * (g - 1)
    eps_state = n_rot * EPS_R + 2 ** g * ANGLE_ROUND
    t_overhead = n_rot * (3 * 40 + 10)  # T per shot for the synthesised rotations (generous O(1))
    return dict(g=g, G=G, K=K, eps3=eps3, n_rotations=n_rot, eps_state=eps_state,
                delta_34=eps3 + 2 * eps_state, T_per_shot_rotations=t_overhead)


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    r1 = json.loads(RUN1.read_text(encoding="utf-8"))
    meta = dict(script="research/frontier_probe_20261021/p2b_parts34.py", python=sys.version,
                flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site),
                inputs_sha256={k: hashlib.sha256(Path(v).read_bytes()).hexdigest()
                               for k, v in dict(run001=RUN1, **p2.IN).items()},
                eps_r=str(EPS_R), q_offset=Q_OFFSET, N0=p2.N0)
    # worst case of delta_34 over every cell's N (largest N gives the largest 2^g term)
    Nmax = max(v["N_calls"] for v in r1["k"].values())
    cmax = max(v["c_certified"] for v in r1["certified"].values())
    b = budgets(Nmax, cmax)
    delta_34 = Fraction(4, 10 ** 6)  # covers g <= 21 (N < 2^20); asserted per cell below
    assert b["delta_34"] <= delta_34, b
    res = dict(meta=meta, parts34=dict(N_max=Nmax, c_max=cmax, **{k: str(v) for k, v in b.items()},
                                       delta_34_used=str(delta_34),
                                       label="mod (explicit; rotation-synthesis guarantee lit)"),
               certified={}, k={})
    designs = [(Fraction(v["delta"]), Fraction(v["gamma"]), v["beta"], v["c_float_continuous"])
               for k, v in r1["certified"].items() if k.endswith("no_impl_budget")]
    for delta, gamma, beta_str, c_float in designs:
        beta2 = Fraction(beta_str) ** 2
        Itot_hi = 2 * p2.PI_HI * p2.int_phi_sq_upper(beta2, gamma)
        dtarget = delta - delta_34
        c_cert, info = p2.certify(beta_str, gamma, dtarget, Itot_hi, c_float - 0.05, c_float + 0.10, Fraction(1, 1000))
        key = f"delta={delta}|gamma={gamma}|with_impl_budget"
        res["certified"][key] = dict(beta=beta_str, gamma=str(gamma), delta=str(delta), delta_target=str(dtarget),
                                     c_certified=float(c_cert), c_float_continuous=c_float, N0=p2.N0,
                                     lambda_lower_N0=str(info["lambda_lower_N0"]),
                                     label="mod (certified; parts 1-4 explicit)", direction="q+")
        print(key, beta_str, float(c_cert), str(info["lambda_lower_N0"])[:12])
    # carry the run001 no-budget rows (unchanged definitions) for completeness
    for k, v in r1["certified"].items():
        if k.endswith("no_impl_budget"):
            res["certified"][k] = {kk: vv for kk, vv in v.items() if kk in ("beta", "gamma", "delta", "c_certified", "N0")}
    sig = p2.load(p2.IN["sigma"])["cases"]
    price = {c: Fraction(str(p2.load(p2.IN["c1"])["port_check"][c]["price"])) for c in ("B4x12", "B8x52")}
    best_c = {}
    for tag in ("no_impl_budget", "with_impl_budget"):
        for delta in (Fraction(3, 1000), Fraction(1, 100)):
            cands = {k: v for k, v in res["certified"].items() if k.startswith(f"delta={delta}|") and k.endswith(tag)}
            kb = min(cands, key=lambda k: cands[k]["c_certified"])
            best_c[(tag, delta)] = (cands[kb]["c_certified"], kb)
    for case in ("B4x12", "B8x52"):
        s = Fraction(str(sig[case]["sigma_q"]))
        for eps in p2.EPS:
            for split, sp in (("0.45eps", Fraction(9, 20)), ("eps", Fraction(1))):
                e = sp * Fraction(str(eps))
                se = s / e
                for spl, S in p2.S_SPAN.items():
                    for ml, m in (("no mean", None), ("price+L1", price[case] + p2.L1)):
                        D_ = p2.delta_phi(m, S, e)
                        for (tag, delta), (c, src) in best_c.items():
                            Nc = math.ceil(Fraction(str(c)) / D_)
                            bb = budgets(Nc, c)
                            assert bb["delta_34"] <= delta_34
                            k_ds = Nc / float(se)
                            res["k"][f"{case}|{eps}|{split}|{spl}|{ml}|{tag}|fail {delta}"] = dict(
                                c=c, design=src, N_calls=Nc, covered_by_N0_certificate=Nc >= p2.N0,
                                k_direction_select=k_ds, k_without_direction_select=2 * k_ds,
                                rotation_T_per_shot=bb["T_per_shot_rotations"], label="mod", direction="q+")
    bc = {k: v for k, v in res["k"].items() if k.startswith("B8x52|0.001|0.45eps|8192/211|price+L1")}
    for k, v in bc.items():
        print(k, round(v["k_direction_select"], 4), "N", v["N_calls"])
    print("parts 3+4 budget at N_max", Nmax, ":", float(b["delta_34"]), "(eps3", float(b["eps3"]), ")")
    with open(OUT / "p2_window.json", "x", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
