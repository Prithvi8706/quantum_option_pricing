"""C11 estimator level: the window (Kaiser) estimator around the compiled U2 iterate at B8x52 $0.001, and M.

Pieces (per shot, P2_DERIVATION.md section 1 and part 4):
  1. window state on g = ceil(log2(2N+1)) qubits (two's-complement n, |n| <= N): <= 2^g rotations (P2 count);
  2. offset phase e^{i n tau}: 2(g+1) rotations;
  3. step code: (sign, low16 bits, top) computed out of place from n, EMITTED here as an X/CX/CCX list and verified
     on every |n| <= N; weights 1, 2, ..., 2^(b-1), remainder = N - (2^b - 1) <= 2^b (P2 subset-sum steps);
  4. controlled powers: step j applies its weight d_j controlled U2 iterates on code bit j (N iterates in all);
  5. direction-select: Q^{-n} = R Q^{n} R (R = the uniform reflection, an involution), so two reflections
     controlled on the sign bit realise n < 0;
  6. uncompute the step code; inverse QFT over Z_G: g(g-1) rotations;
  7. classical readout (u2_wrapper.json readout rule).
Rotations: synthesised to 2^-40 at 130 T each (Ross-Selinger, arXiv:1403.2975, ~3 log2(1/eps) + O(log log);
same per-rotation figure as P2 run002 "rotation_T_per_shot"); they are counted as fully serial (q-).

M at the primary conventions: M = 10 * (layers per shot) * t_layer / T_C (the headline identity
M = k*10*(sigma/e)*D_eff*t_layer/T_C with k*(sigma/e) = N calls), T_C from headline run006.
Run: ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/c11/estimator_compile.py run001
"""
import json
import os
import platform
import sys
from math import ceil, log2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c11_common import ROOT, progress, resources, run_gates, sha, write_new  # noqa: E402

sys.path.insert(0, ROOT)
from research.journal_sprint.reversible_fixed_point import Program, add, constant, copy, less_than, subtract  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"
OUT = ROOT + f"results/claim_debts_20261022/c11/{RUN}/"
IN = dict(
    u2=OUT + "u2_wrapper.json",
    pathA=OUT + "iterate_compile.json",
    pathB=OUT + "iterate_recount_pathB.json",
    p2=ROOT + "results/frontier_probe_20261021/p2/run002/p2_window.json",
    sm=ROOT + "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
    head=ROOT + "results/frontier_probe_20261021/headline/run006/headline_table.json",
)
T_ROT = 130          # T per synthesised rotation at 2^-40 (lit/assm; P2 run002)
SUPPLY_T_PER_LAYER = 1e12 * 1e-7   # 1e12 T/s at 100 ns layers
T_LAYER = 1e-7


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def rows(p):
    d = p.gates.data
    return [tuple(d[4 * i:4 * i + 4]) for i in range(len(p.gates))]


def make_code(g, N):
    """Out-of-place step code from a g-bit two's-complement n with |n| <= N."""
    b = (N + 1).bit_length() - 1            # 2^b - 1 <= N < 2^(b+1) - 1
    rem = N - ((1 << b) - 1)
    if not 0 <= rem <= 1 << b:
        raise ValueError("subset-sum steps do not cover [0, N]")
    p = Program(compact=True)
    n = p.register(g)
    mag, inc, low, kreg, cst = (p.register(g) for _ in range(5))
    top = p.register(1)[0]
    diff, ext, helper = p.register(g + 1), p.register(g + 1), p.register(1)[0]
    sign = n[-1]
    copy(p, n, mag)
    for q in mag:
        p.gate(sign, q)                     # one's complement if negative
    p.gate(sign, inc[0])
    add(p, inc, mag, helper)                # mag = |n|
    constant(p, cst, (1 << b) - 1)
    less_than(p, cst, mag, top, diff, ext, helper)   # top = [2^b - 1 < |n|]
    copy(p, mag, low)
    for i in range(g):
        if (rem >> i) & 1:
            p.gate(top, kreg[i])
    subtract(p, kreg, low, helper)          # low = |n| - top*rem  (< 2^b)
    code = dict(sign=sign, low=low[:b], top=top, weights=[1 << i for i in range(b)] + [rem], b=b, rem=rem)
    return p, n, code, dict(mag=mag, low=low)


def verify_code(g, N):
    p, n, code, regs = make_code(g, N)
    gl = rows(p)
    bad, seen = [], set()
    for v in range(-N, N + 1):
        s0 = sum((((v % (1 << g)) >> i) & 1) << q for i, q in enumerate(n))
        s1 = run_gates(gl, s0)
        low = sum(((s1 >> q) & 1) << i for i, q in enumerate(regs["low"]))
        top = (s1 >> code["top"]) & 1
        sign = (s1 >> code["sign"]) & 1
        ok = low < 1 << code["b"] and low + top * code["rem"] == abs(v) and sign == (1 if v < 0 else 0)
        key = (sign, low, top)
        if not ok or key in seen:
            bad.append(v)
        seen.add(key)
        if run_gates(gl, s1, inverse=True) != s0:
            bad.append(("inverse", v))
    r = resources(gl, p.qubits)
    return dict(g=g, N=N, b=code["b"], remainder=code["rem"], weights_sum=sum(code["weights"]),
                cases=2 * N + 1, failures=bad[:10], passed=not bad, qubits=p.qubits,
                extra_qubits_beyond_n=p.qubits - g, resources_once=r)


def shot(N, it_qf, it_lit, refl, code_res, label):
    g = ceil(log2(2 * N + 1))
    rot = (1 << g) + 2 * (g + 1) + g * (g - 1)
    rot_T = rot * T_ROT
    code_T, code_tof, code_td = 2 * code_res["t_count"], 2 * code_res["toffoli_depth"], 2 * code_res["t_depth"]
    ds_T, ds_tof, ds_td = 2 * refl["t_count"], 2 * refl["toffoli_depth"], 2 * refl["t_depth"]
    out = dict(label=label, N=N, g=g, rotations=rot, rotation_T=rot_T, code_T=code_T, direction_select_T=ds_T)
    for name, it, code_layers, ds_layers in (("qf_floor_convention", it_qf, code_tof, ds_tof),
                                             ("literal_7T", it_lit, code_td, ds_td)):
        t_iter = it["T"]
        d_eff = max(it["reaction"], t_iter / SUPPLY_T_PER_LAYER)
        over_T = rot_T + (code_T + ds_T) * (4 / 7 if name == "qf_floor_convention" else 1)
        over_layers = rot_T + code_layers + ds_layers           # rotations serial, one layer per T (q-)
        layers = N * d_eff + over_layers
        out[name] = dict(T_per_iterate=t_iter, reaction_layers_per_iterate=it["reaction"],
                         supply_layers_per_iterate=t_iter / SUPPLY_T_PER_LAYER, D_eff_iterate=d_eff,
                         binding="reaction" if it["reaction"] >= t_iter / SUPPLY_T_PER_LAYER else "supply",
                         T_total=N * t_iter + over_T, overhead_T=over_T, overhead_layers=over_layers,
                         layers_total=layers, quantum_seconds=layers * T_LAYER,
                         overhead_fraction_of_layers=over_layers / layers)
    return out


def main():
    progress(dict(step="estimator_start", run=RUN))
    u2, pa, pb = load(IN["u2"]), load(IN["pathA"]), load(IN["pathB"])
    head, p2, sm = load(IN["head"]), load(IN["p2"]), load(IN["sm"])
    assert pa["u2_iterate"]["t_count"] == pb["u2_iterate"]["t_count"]
    assert pa["u2_iterate"]["toffoli_depth"] == pb["u2_iterate"]["toffoli_depth"]
    assert pa["u2_iterate"]["t_depth"] == pb["u2_iterate"]["t_depth"]
    it = pa["u2_iterate"]
    cell = next(c for c in head["cells"] if c["case"] == "B8x52" and abs(c["eps"] - 0.001) < 1e-12)
    T_C, D_floor = cell["T_C"], cell["D_eff_primary"]["used"]
    k_win = cell["k"]["window_certified_fail0003"]
    M_floor = cell["M"]["window_certified_fail0003"]["primary"]
    key = "B8x52|0.001|0.45eps|8192/211|price+L1|with_impl_budget|fail 3/1000"
    N_win = p2["k"][key]["N_calls"] if key in p2.get("k", {}) else None
    if N_win is None:
        s = json.dumps(p2)
        assert '"N_calls": 100924' in s
        N_win = 100924
    smb = sm["cells"]["B8x52|0.001"]["best"]
    N1, N2 = smb["N1"], smb["N2"]
    M_floor_check = 10 * N_win * D_floor * T_LAYER / T_C
    assert abs(M_floor_check / M_floor - 1) < 1e-9, (M_floor_check, M_floor)

    refl = pa["u2_parts"]["reflection"]
    refl = dict(refl, toffoli_depth=pa["u2_parts"]["reflection_toffoli_depth"])
    it_qf = dict(T=4 * it["ccx"], reaction=it["toffoli_depth"])
    it_lit = dict(T=it["t_count"], reaction=it["t_depth"])
    dep = pb["dependency_only"]
    it_dep = dict(T=4 * it["ccx"],
                  reaction=2 * dep["forward_toffoli_depth"] + 2 * pa["u2_parts"]["selector_toffoli_depth"] + 1
                  + pa["u2_parts"]["reflection_toffoli_depth"])

    # most favourable reading (mod): dependency-only leaf schedule and a log-depth AND-tree reflection
    # (2*ceil(log2 n) Toffoli layers instead of the emitted linear ladder); not emitted.
    n_rand = pa["u2_parts"]["reflection_random_wires"]
    it_fav = dict(T=4 * it["ccx"], reaction=2 * dep["forward_toffoli_depth"]
                  + 2 * pa["u2_parts"]["selector_toffoli_depth"] + 1 + 2 * ceil(log2(n_rand)))
    codes = {N: verify_code(ceil(log2(2 * N + 1)), N) for N in (N_win, N1, N2)}
    progress(dict(step="estimator_code_verified", ok=all(c["passed"] for c in codes.values())))
    win = shot(N_win, it_qf, it_lit, refl, codes[N_win]["resources_once"], "window certified (U1 + U2 + DS)")
    s1 = shot(N1, it_qf, it_lit, refl, codes[N1]["resources_once"], "quantum-only mean, stage 1")
    s2 = shot(N2, it_qf, it_lit, refl, codes[N2]["resources_once"], "quantum-only mean, stage 2")
    win_dep = shot(N_win, it_dep, it_lit, refl, codes[N_win]["resources_once"], "window, dependency-only depth")
    win_fav = shot(N_win, it_fav, it_lit, refl, codes[N_win]["resources_once"],
                   "window, dependency-only depth + log-depth reflection (mod)")

    def M_of(layers):
        return 10 * layers * T_LAYER / T_C

    M = dict(
        floor_reference=dict(M=M_floor, D_eff=D_floor, N=N_win, k=k_win, T_C=T_C, check=M_floor_check),
        window_qf=M_of(win["qf_floor_convention"]["layers_total"]),
        window_literal=M_of(win["literal_7T"]["layers_total"]),
        window_dependency_only_qf=M_of(win_dep["qf_floor_convention"]["layers_total"]),
        window_most_favourable_qf=M_of(win_fav["qf_floor_convention"]["layers_total"]),
        self_mean_qf=M_of(s1["qf_floor_convention"]["layers_total"] + s2["qf_floor_convention"]["layers_total"]),
        self_mean_literal=M_of(s1["literal_7T"]["layers_total"] + s2["literal_7T"]["layers_total"]),
        supply_only_qf=M_of(N_win * it_qf["T"] / SUPPLY_T_PER_LAYER),
        supply_only_literal=M_of(N_win * it_lit["T"] / SUPPLY_T_PER_LAYER),
    )
    ratios = {k: v / M_floor for k, v in M.items() if k != "floor_reference"}
    width = dict(iterate_logical_qubits=pa["width"]["u2"],
                 estimator_extra=dict(phase_register=win["g"], step_code_and_scratch=codes[N_win]["extra_qubits_beyond_n"]),
                 total_upper=pa["width"]["u2"] + win["g"] + codes[N_win]["extra_qubits_beyond_n"],
                 primary_width_1e7_fits=pa["width"]["u2"] + win["g"] + codes[N_win]["extra_qubits_beyond_n"] <= 10 ** 7,
                 note="upper count: the 17 old-buffer wires left after U2 could host part of the code register")
    out = dict(
        schema="c11-estimator-compile-v1", run=RUN, case="B8x52", eps=0.001,
        iterate=dict(ccx=it["ccx"], t_count_literal=it["t_count"], t_count_qf=4 * it["ccx"], t_depth=it["t_depth"],
                     toffoli_depth=it["toffoli_depth"], dependency_only_reaction=it_dep["reaction"],
                     most_favourable_reaction=it_fav["reaction"],
                     floor_T_per_iterate=D_floor * SUPPLY_T_PER_LAYER, floor_D_eff=D_floor),
        step_code=codes, window_shot=win, window_shot_dependency_only=win_dep, window_shot_most_favourable=win_fav,
        self_mean=dict(stage1=s1, stage2=s2, N_total=N1 + N2), M=M, M_over_floor=ratios, width=width,
        direction_select="Q^{-n} = R Q^{n} R with R the controlled uniform reflection (an involution): two "
                         "reflections controlled on the sign bit per shot",
        labels=dict(iterate="meas (path A = path B)", rotations="mod: 130 T per rotation (lit, Ross-Selinger), serial",
                    step_code="meas (emitted, verified on every |n| <= N)",
                    qf_floor_convention="Toffoli = 4 T, one reaction layer per Toffoli layer (N1 floor conventions)",
                    literal_7T="exact seven-T CCX, reaction layer = T layer",
                    M="mod: M = 10 * layers * t_layer / T_C; T_C meas (run006, QF composition assm)"),
        inputs={k: dict(path=v.replace(ROOT, ""), sha256=sha(v)) for k, v in IN.items()},
        interpreter=platform.python_version(), isolated=bool(sys.flags.isolated),
    )
    write_new(OUT + "estimator_compile.json", out)
    progress(dict(step="estimator_done", M=M, ratios=ratios))
    print(json.dumps(dict(M=M, ratios=ratios, codes={k: (v["passed"], v["cases"]) for k, v in codes.items()},
                          win_qf=win["qf_floor_convention"]["D_eff_iterate"]), indent=1, default=str))


if __name__ == "__main__":
    main()
