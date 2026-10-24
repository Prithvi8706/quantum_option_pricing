"""C11 path B: independent stdlib recount of the B8x52 iterate (saved and U2), no repository counting code.

Differences from path A (iterate_compile.py):
  * no numpy/numba and no research.* imports; .npy files are parsed by c11_common.read_npy_int32;
  * T-depth, Clifford+T depth and Toffoli depth come from c11_common.resources, a separate implementation of the
    seven-T schedule and of the reaction convention;
  * counts are summed over source.json forward_calls (call multiplicities), not over batches; batches are only used
    for depth, after checking that they partition the calls;
  * argument-copy CX use schedule_capped.json "widths" directly;
  * the reflection is rebuilt from its definition and checked against reflection.npy before widening it.
Path B must agree exactly with path A and with iterate.json.
Run: ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/c11/recount_independent.py run001
"""
import json
import os
import platform
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c11_common import ROOT, progress, read_npy_int32, resources, sha, write_new  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"
OUT = ROOT + f"results/claim_debts_20261022/c11/{RUN}/"
A10 = ROOT + "results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/"
E02 = ROOT + "results/limitation_program_20261001/E02_financial_run002/B8x52/"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def reflection_gates(n):
    """Controlled (2|+><+| - I) on n random wires: H, X, CCX ladder, CZ(scratch_last, control), ladder^-1, X, H, Z."""
    rnd, ctl, scr = list(range(n)), n, list(range(n + 1, 2 * n))
    g = [(4, w, 0, 0) for w in rnd] + [(1, w, 0, 0) for w in rnd]
    lad = [(3, rnd[0], rnd[1], scr[0])] + [(3, scr[j - 2], rnd[j], scr[j - 1]) for j in range(2, n)]
    g += lad + [(5, scr[-1], ctl, 0)] + lad[::-1]
    g += [(1, w, 0, 0) for w in rnd] + [(4, w, 0, 0) for w in rnd] + [(6, ctl, 0, 0)]
    return g, 2 * n


def main():
    progress(dict(step="pathB_start", run=RUN))
    it = load(E02 + "iterate.json")
    source, capped = load(A10 + "source.json"), load(A10 + "schedule_capped.json")
    for name in ("source.json", "schedule_capped.json", "target.json"):
        assert sha(A10 + name) == it["binding"]["hashes"][name]
    widths = capped["widths"]
    leaf = {}
    for key in source["library_keys"]:
        meta = load(A10 + "leaves/" + key + ".json")
        path = A10 + "leaves/" + meta["gate_file"]
        assert sha(path) == meta["sha256"]
        gates = read_npy_int32(path)
        q = meta["resources"]["qubits"]
        leaf[key] = dict(forward=resources(gates, q), inverse=resources(gates, q, inverse=True))
        assert leaf[key]["forward"]["ccx"] == meta["resources"]["ccx"]
    progress(dict(step="pathB_leaves", leaves=len(leaf)))

    # counts over calls (multiplicity), both directions, plus argument copies
    tot = dict(source_gates=0, x=0, cx=0, ccx=0)
    copy_cx_widths, copy_cx_recorded = 0, 0
    for call in source["forward_calls"]:
        r = leaf[call["leaf"]]
        for d in ("forward", "inverse"):
            for k in tot:
                tot[k] += r[d][k]
        copy_cx_widths += 4 * sum(widths[v] for v in call["args"])
        copy_cx_recorded += 2 * call.get("argument_copy_cx", 0)
    tot["source_gates"] += copy_cx_widths
    tot["cx"] += copy_cx_widths
    tot["t_count"] = 7 * tot["ccx"]
    tot["clifford_cx"] = tot["cx"] + 6 * tot["ccx"]
    tot["clifford_h"] = 2 * tot["ccx"]
    # depth over batches
    calls_seen = sorted(i for g in capped["groups"] for i in g["call_indices"])
    assert calls_seen == list(range(len(source["forward_calls"])))
    td = ctd = tofd = 0
    for g in capped["groups"]:
        ks = [source["forward_calls"][i]["leaf"] for i in g["call_indices"]]
        for d in ("forward", "inverse"):
            td += max(leaf[k][d]["t_depth"] for k in ks)
            ctd += max(leaf[k][d]["clifford_t_depth"] for k in ks) + 2 * g["copy_rounds"]
            tofd += max(leaf[k][d]["toffoli_depth"] for k in ks)
    fin = dict(tot, t_depth=td, clifford_t_depth=ctd, toffoli_depth=tofd)
    # dependency-only (unlimited width) forward critical paths over the SSA call graph: a lower bound for any
    # schedule of these leaves (ASAP inside leaves), used only as the quantum-favourable reading.
    arr_t = {v: 0 for node in source["inputs"] for v in node["out"]}
    arr_r = dict(arr_t)
    for call in source["forward_calls"]:
        r = leaf[call["leaf"]]["forward"]
        a_t = max((arr_t[v] for v in call["args"]), default=0) + r["t_depth"]
        a_r = max((arr_r[v] for v in call["args"]), default=0) + r["toffoli_depth"]
        for v in call["out"]:
            arr_t[v], arr_r[v] = a_t, a_r
    dep_only = dict(forward_t_depth=max(arr_t.values()), forward_toffoli_depth=max(arr_r.values()),
                    recorded_forward_t_depth=capped["dependency_only_forward_t_depth"])
    fin_vs_json = {k: fin[k] == it["financial_resources"][k] for k in it["financial_resources"]}

    # reflection replica check, then the two wrappers
    refl_saved_file = read_npy_int32(E02 + "reflection.npy")
    n_saved = len(it["random_wires"])
    rg, rq = reflection_gates(n_saved)
    replica_ok = rg == refl_saved_file
    saved_sel = read_npy_int32(E02 + "selector.npy")
    u2 = load(OUT + "u2_selector_gates.json")
    u2_sel = [tuple(r) for r in u2["gates"]]

    def compose(sel, selq, n_rand):
        f, i = resources(sel, selq), resources(sel, selq, inverse=True)
        g, q = reflection_gates(n_rand)
        rr = resources(g, q)
        t = {k: fin[k] for k in ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h",
                                 "t_depth", "clifford_t_depth")}
        for part in (f, i, rr):
            for k in t:
                t[k] += part[k]
        t["clifford_h"] += 0  # H gates of the reflection are inside rr["clifford_h"]
        t["source_gates"] += 1; t["cz"] = rr["cz"] + 1; t["z"] = rr["z"]; t["h"] = rr["h"]
        t["clifford_t_depth"] += 1
        t["toffoli_depth"] = fin["toffoli_depth"] + f["toffoli_depth"] + i["toffoli_depth"] + 1 + rr["toffoli_depth"]
        return t, dict(selector_forward=f, selector_inverse=i, reflection=rr)

    saved, _ = compose(saved_sel, 72 + 46 + 1 + 47 + 47 + 1, n_saved)
    u2t, u2parts = compose(u2_sel, u2["qubits"], source["resources"]["random_hadamards"] + 53)
    saved_vs_json = {k: saved[k] == it["resources"][k] for k in saved if k in it["resources"]}
    pa_path = OUT + "iterate_compile.json"
    vs_a = None
    if os.path.exists(pa_path):
        pa = load(pa_path)
        vs_a = dict(financial={k: fin[k] == pa["financial_recount"][k] for k in pa["financial_recount"]},
                    saved={k: saved[k] == pa["saved_iterate_recount"][k] for k in saved if k in pa["saved_iterate_recount"]},
                    u2={k: u2t[k] == pa["u2_iterate"][k] for k in u2t if k in pa["u2_iterate"]})
    out = dict(schema="c11-iterate-recount-pathB-v1", run=RUN, case="B8x52",
               financial=fin, financial_matches_iterate_json=fin_vs_json,
               dependency_only=dep_only,
               copy_cx=dict(from_widths=copy_cx_widths, from_call_records_x2=copy_cx_recorded),
               reflection_replica_equals_saved=replica_ok,
               saved_iterate=saved, saved_matches_iterate_json=saved_vs_json,
               u2_iterate=u2t, u2_parts=u2parts, matches_pathA=vs_a,
               interpreter=platform.python_version(), isolated=bool(sys.flags.isolated))
    write_new(OUT + "iterate_recount_pathB.json", out)
    ok = (all(fin_vs_json.values()) and replica_ok and all(saved_vs_json.values())
          and (vs_a is None or all(all(v.values()) for v in vs_a.values())))
    progress(dict(step="pathB_done", ok=ok, pathA_compared=vs_a is not None))
    print(json.dumps(dict(ok=ok, u2_t=u2t["t_count"], u2_t_depth=u2t["t_depth"], u2_tof=u2t["toffoli_depth"],
                          fin_tof=fin["toffoli_depth"], pathA_compared=vs_a is not None,
                          mismatch=[k for k, v in {**fin_vs_json, **saved_vs_json}.items() if not v]), indent=1))


if __name__ == "__main__":
    main()
