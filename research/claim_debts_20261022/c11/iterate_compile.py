"""C11 path A: recount the B8x52 controlled Grover iterate from the raw A10 leaves with the repository's own
counting functions (read-only imports), then compose the U2 variant.

Path A re-executes the E02 counting logic (native_payoff_estimator_v2.emit_iterate) on the worktree copies of the
bound A10 min-depth source, without writing anything into the limitation-program folders:
  * every financial leaf is re-loaded and re-costed with checkpoint_circuit._native_cost (forward and inverse);
  * batch T-depth = max over the batch's calls, summed over batches and directions; copies 4*sum(arg widths);
  * selector and reflection costs are recomputed from the gate arrays.
It must reproduce iterate.json "resources" exactly for the saved wrapper. The U2 variant then replaces the selector
pair by the emitted U2 selector (u2_wrapper.py) and widens the reflection to 14,976 + 53 random wires.
A Toffoli (reaction) depth per leaf is added with a separate numba kernel (Cliffords free, one layer per CCX), the
N1 floor's reaction convention.

Needs numpy + numba, so it runs without -I/-S (same as the Stage C harness):
  ../../../.context/frontier_t0_env/Scripts/python.exe -B -m research.claim_debts_20261022.c11.iterate_compile run001
"""
import json
import platform
import sys
from collections import Counter

import numpy as np
from numba import njit

from research.claim_debts_20261022.c11.c11_common import ROOT, progress, sha, write_new
from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.limitation_program_20261001.checkpoint_circuit import _native_cost, fingerprint
from research.limitation_program_20261001.native_payoff_estimator_v2 import extended_resources, make_reflection

RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"
OUT = ROOT + f"results/claim_debts_20261022/c11/{RUN}/"
A10 = ROOT + "results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/"
E02 = ROOT + "results/limitation_program_20261001/E02_financial_run002/B8x52/"
IN = dict(source=A10 + "source.json", target=A10 + "target.json", capped=A10 + "schedule_capped.json",
          iterate=E02 + "iterate.json", selector=E02 + "selector.npy", reflection=E02 + "reflection.npy",
          u2=OUT + "u2_selector_gates.json")
FIELDS = ("source_gates", "x", "cx", "ccx", "t_count", "clifford_cx", "clifford_h")


@njit(cache=True)
def toffoli_depth(gates, qubits):
    lev = np.zeros(qubits, np.int64)
    for g in range(gates.shape[0]):
        kind, a, b, c = gates[g, 0], gates[g, 1], gates[g, 2], gates[g, 3]
        if kind == 2 or kind == 5:
            m = max(lev[a], lev[b]); lev[a] = m; lev[b] = m
        elif kind == 3:
            m = max(lev[a], max(lev[b], lev[c])) + 1; lev[a] = m; lev[b] = m; lev[c] = m
    return lev.max() if qubits else 0


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def financial(source, target, capped):
    metadata = entries(source)
    # compact_parallel_v7._storage cannot be re-run in this checkout: it stops at a lookup-leaf key provenance
    # check (the current LOOKUP_LOWERING constant no longer hashes to the archived lookup keys). That check does
    # not affect counts; the widths are read from schedule_capped.json, whose sha256 equals the E02 binding and
    # which the E02 emission asserted equal to _storage(...) at emission time.
    storage = dict(widths=capped["widths"])
    assert (capped["source_fingerprint"], capped["target_fingerprint"]) == (fingerprint(source), fingerprint(target))
    library = resolve_library(source)
    costs, tof, totals = {}, {}, Counter()
    seen = []
    for group in capped["groups"]:
        calls = group["call_indices"]
        seen += calls
        for index in calls:
            call = source["forward_calls"][index]
            key = call["leaf"]
            if key not in costs:
                entry = metadata[key]
                f = library / entry["gate_file"]
                assert sha(str(f)) == entry["sha256"], "leaf changed"
                gates = np.load(f)
                q = entry["resources"]["qubits"]
                costs[key] = dict(forward=_native_cost(gates, q, False), inverse=_native_cost(gates, q, True))
                tof[key] = int(toffoli_depth(gates, q))
                for fld in FIELDS + ("t_depth", "clifford_t_depth"):
                    assert costs[key]["forward"][fld] == entry["resources"][fld], (key, fld)
            for d in ("forward", "inverse"):
                for fld in FIELDS:
                    totals[fld] += costs[key][d][fld]
            copies = 4 * sum(storage["widths"][v] for v in call["args"])
            for fld in ("source_gates", "cx", "clifford_cx"):
                totals[fld] += copies
        for d in ("forward", "inverse"):
            totals["t_depth"] += max(costs[source["forward_calls"][i]["leaf"]][d]["t_depth"] for i in calls)
            totals["clifford_t_depth"] += (max(costs[source["forward_calls"][i]["leaf"]][d]["clifford_t_depth"]
                                               for i in calls) + 2 * group["copy_rounds"])
            totals["toffoli_depth"] += max(tof[source["forward_calls"][i]["leaf"]] for i in calls)
    assert sorted(seen) == list(range(len(source["forward_calls"]))), "groups do not partition the calls"
    return dict(totals), costs, tof


def compose(fin, sel_gates, sel_qubits, n_random):
    sel = dict(forward=_native_cost(sel_gates, sel_qubits, False), inverse=_native_cost(sel_gates, sel_qubits, True))
    sel_tof = int(toffoli_depth(sel_gates, sel_qubits))
    refl, spec = make_reflection(n_random)
    rc = extended_resources(refl, spec["qubits"])
    refl_tof = int(toffoli_depth(refl, spec["qubits"]))
    t = Counter({k: v for k, v in fin.items() if k != "toffoli_depth"})
    for c in (*sel.values(), rc):
        for k, v in c.items():
            t[k] += v
    t["source_gates"] += 1; t["cz"] += 1; t["clifford_cz"] += 1; t["clifford_t_depth"] += 1
    t = dict(t)
    # reaction depth: financial batches, both selector directions, CZ(control, flag) (+1), reflection
    t["toffoli_depth"] = fin["toffoli_depth"] + 2 * sel_tof + 1 + refl_tof
    return t, dict(selector=sel, selector_toffoli_depth=sel_tof, reflection=rc, reflection_toffoli_depth=refl_tof,
                   reflection_random_wires=n_random)


def main():
    progress(dict(step="pathA_start", run=RUN))
    it = load(IN["iterate"])
    for name in ("source.json", "target.json", "schedule_capped.json"):
        local = A10 + name
        assert sha(local) == it["binding"]["hashes"][name], f"{name} differs from the E02 binding"
    assert sha(IN["selector"]) == it["selector_sha256"] and sha(IN["reflection"]) == it["reflection_sha256"]
    source, target, capped = load(IN["source"]), load(IN["target"]), load(IN["capped"])
    fin, costs, tof = financial(source, target, capped)
    fin_match = {k: fin[k] == it["financial_resources"][k] for k in it["financial_resources"]}
    progress(dict(step="pathA_financial", match=all(fin_match.values()), t_count=fin["t_count"]))

    saved_sel = np.load(IN["selector"])
    n_rand_saved = len(it["random_wires"])
    sel_q_saved = 72 + 46 + 1 + 47 + 47 + 1
    saved, saved_parts = compose(fin, saved_sel, sel_q_saved, n_rand_saved)
    saved_match = {k: saved[k] == it["resources"][k] for k in it["resources"] if k in saved}
    u2 = load(IN["u2"])
    u2_gates = np.asarray(u2["gates"], dtype=np.int32)
    n_rand_u2 = source["resources"]["random_hadamards"] + 53
    assert n_rand_saved == source["resources"]["random_hadamards"] + 46
    u2_tot, u2_parts = compose(fin, u2_gates, u2["qubits"], n_rand_u2)
    width = dict(saved=it["resources"]["logical_qubits"],
                 u2=it["resources"]["logical_qubits"],  # U2 scratch fits the private bank; selector bits in old buffer
                 u2_scratch_fits_private_bank=(u2["qubits"] - 72 - 53 - 1) <= it["private_capacity"]
                 and n_rand_u2 - 1 <= it["private_capacity"],
                 note="reflection scratch (n_random - 1) and selector scratch reuse the financial private bank after F")
    out = dict(
        schema="c11-iterate-compile-pathA-v1", run=RUN, case="B8x52",
        financial_recount=fin, financial_matches_iterate_json=fin_match,
        saved_iterate_recount=saved, saved_matches_iterate_json=saved_match, saved_parts=saved_parts,
        u2_iterate=u2_tot, u2_parts=u2_parts, width=width,
        leaf_toffoli_depth=tof, leaves=len(costs), batches=len(capped["groups"]), calls=len(source["forward_calls"]),
        dependency_only_forward_t_depth=capped["dependency_only_forward_t_depth"],
        depth_convention=it["depth_convention"],
        ws_small_check=dict(f_fwd_plus_inv=fin["t_depth"], selector_pair=2 * 752, reflection=105148,
                            sum=fin["t_depth"] + 2 * 752 + 105148, recorded=it["resources"]["t_depth"]),
        labels=dict(counts="meas (exact counts of the emitted gate arrays)",
                    t_depth="meas under the E02 depth convention (memory-capped batches, all-to-all ASAP inside "
                            "leaves; layout and routing unproved)",
                    toffoli_depth="meas under the N1 reaction convention (Cliffords free; one layer per CCX layer)"),
        inputs={k: dict(path=v.replace(ROOT, ""), sha256=sha(v)) for k, v in IN.items()},
        interpreter=platform.python_version(), numpy=np.__version__,
    )
    write_new(OUT + "iterate_compile.json", out)
    ok = all(fin_match.values()) and all(saved_match.values())
    progress(dict(step="pathA_done", ok=ok, u2_t_count=u2_tot["t_count"], u2_t_depth=u2_tot["t_depth"],
                  u2_toffoli_depth=u2_tot["toffoli_depth"]))
    print(json.dumps(dict(ok=ok, saved_t=saved["t_count"], u2_t=u2_tot["t_count"], u2_t_depth=u2_tot["t_depth"],
                          u2_tof_depth=u2_tot["toffoli_depth"], fin_tof=fin["toffoli_depth"],
                          mismatches=[k for k, v in {**fin_match, **saved_match}.items() if not v]), indent=1))


if __name__ == "__main__":
    main()
