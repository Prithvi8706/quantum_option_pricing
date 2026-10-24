"""C11/U2 run summary: collect the checks and headline numbers of a run into summary.json.
Run: ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/c11/summary.py run001
"""
import glob
import json
import os
import platform
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c11_common import ROOT, progress, sha, write_new  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"
OUT = ROOT + f"results/claim_debts_20261022/c11/{RUN}/"


def load(name):
    with open(OUT + name, encoding="utf-8") as f:
        return json.load(f)


u2, pa, pb, est = (load(n) for n in ("u2_wrapper.json", "iterate_compile.json", "iterate_recount_pathB.json",
                                       "estimator_compile.json"))
checks = dict(
    u2_ir_restatement_equals_saved_selector=u2["ir_equal_saved"],
    u2_builder_c1_b46_equals_saved_selector=u2["u2_c1_equals_saved"],
    u2_exhaustive_small=all(s["passed"] for s in u2["exhaustive_small"]),
    u2_exhaustive_cases=sum(s["cases"] for s in u2["exhaustive_small"]),
    u2_full_width_cases=u2["full_width"]["cases"], u2_full_width_failures=len(u2["full_width"]["failures"]),
    u2_support_holds=u2["support"]["holds"], u2_readout_within_2_pow_m39=u2["readout"]["within_placeholder"],
    pathA_financial_equals_iterate_json=all(pa["financial_matches_iterate_json"].values()),
    pathA_saved_iterate_equals_iterate_json=all(pa["saved_matches_iterate_json"].values()),
    pathB_financial_equals_iterate_json=all(pb["financial_matches_iterate_json"].values()),
    pathB_saved_iterate_equals_iterate_json=all(pb["saved_matches_iterate_json"].values()),
    pathB_reflection_replica_equals_saved=pb["reflection_replica_equals_saved"],
    pathA_equals_pathB=all(all(v.values()) for v in pb["matches_pathA"].values()),
    pathB_dependency_only_equals_recorded=pb["dependency_only"]["forward_t_depth"]
    == pb["dependency_only"]["recorded_forward_t_depth"],
    step_code_verified_all_n=all(c["passed"] for c in est["step_code"].values()),
    floor_M_reproduced=abs(est["M"]["floor_reference"]["check"] / est["M"]["floor_reference"]["M"] - 1) < 1e-9,
)
it = est["iterate"]
summary = dict(
    schema="c11-u2-summary-v1", run=RUN, case="B8x52", eps=0.001, rigour="R1 (two independent recount paths; "
    "no peer review or lifecycle receipt; not R2)",
    all_checks_pass=all(v for k, v in checks.items() if isinstance(v, bool)) and checks["u2_full_width_failures"] == 0,
    checks=checks,
    u2_delta_per_iterate=dict(selector_pair=u2["delta_selector_pair"],
                              t_count_total=it["t_count_literal"] - pa["saved_iterate_recount"]["t_count"],
                              t_depth_total=it["t_depth"] - pa["saved_iterate_recount"]["t_depth"],
                              relative_t=(it["t_count_literal"] / pa["saved_iterate_recount"]["t_count"]) - 1,
                              extra_logical_qubits=0),
    iterate=dict(it, floor_ratio_T_literal=it["t_count_literal"] / it["floor_T_per_iterate"],
                 floor_ratio_T_qf=it["t_count_qf"] / it["floor_T_per_iterate"]),
    D_eff=dict(floor=it["floor_D_eff"],
               qf_floor_convention=est["window_shot"]["qf_floor_convention"]["D_eff_iterate"],
               literal_7T=est["window_shot"]["literal_7T"]["D_eff_iterate"],
               dependency_only_qf=est["window_shot_dependency_only"]["qf_floor_convention"]["D_eff_iterate"],
               most_favourable_qf=est["window_shot_most_favourable"]["qf_floor_convention"]["D_eff_iterate"],
               supply_only_qf=est["window_shot"]["qf_floor_convention"]["supply_layers_per_iterate"],
               supply_only_literal=est["window_shot"]["literal_7T"]["supply_layers_per_iterate"]),
    M=est["M"], M_over_floor=est["M_over_floor"], width=est["width"],
    shot_T_total=dict(qf=est["window_shot"]["qf_floor_convention"]["T_total"],
                      literal=est["window_shot"]["literal_7T"]["T_total"]),
    scripts={os.path.basename(p): sha(p) for p in sorted(glob.glob(ROOT + "research/claim_debts_20261022/c11/*.py"))},
    outputs={n: sha(OUT + n) for n in ("u2_wrapper.json", "u2_selector_gates.json", "iterate_compile.json",
                                       "iterate_recount_pathB.json", "estimator_compile.json")},
    interpreter=platform.python_version(),
)
write_new(OUT + "summary.json", summary)
progress(dict(step="summary_done", all_checks_pass=summary["all_checks_pass"]))
print(json.dumps(dict(all_checks_pass=summary["all_checks_pass"], checks=checks), indent=1))
