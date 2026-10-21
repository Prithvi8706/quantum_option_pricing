"""Decision-point table (claim C4) from the Stage C evidence available so far
(ANALYSIS_SPEC_STAGE_C.md, "Decision-point table"). INTERIM until items C5 and C6 and the
plain-MC anchors exist: the section 0.3 minimum is then taken over C1 rqmc and preint on the
CPU only, which is quantum-favourable (a missing faster comparator can only lower T_C).
  python -m research.frontier_classical_20261001.decision --res <results dir> --out <dir>
"""

import argparse
import json
from pathlib import Path

from research.frontier_classical_20261001.fit import SHARE, T995_15

T_LAYER, K, EPS0 = 1e-7, 3, 0.001
ROOT = Path(__file__).resolve().parents[2]
STAGE_A = ROOT / "results/frontier_completion_20260927/stage_a"
METHODS = {"preint": "knockout_pre", "rqmc": "knockout"}


def d_max(t_c, sigma, eps=EPS0, k=K, t_layer=T_LAYER, share=SHARE):
    return t_c / (10 * k * sigma / (share * eps) * t_layer)


def depths(case):
    arch = json.loads((ROOT / "results/advantage_frontier_20260923/barrier_oracle_depth.json")
                      .read_text())
    fav = next(r["clean_call_t_depth"] for r in arch["rows"] if r["case"] == case
               and r["gaussians"] == "box-muller" and r["leaf_costs"] == "favourable")
    acc = json.loads((STAGE_A / case / "accounting.json").read_text())
    return {"favourable_leaf_table (QF)": fav,
            "clean_dependency_only (headline)": 2 * acc["exact"]["forward_dependency_t_depth"],
            "clean_scheduled": acc["schedules"]["all"]["t_depth"],
            # Chakrabarti et al.'s per-Q-operator T-depth for a smaller 3-asset payoff: a
            # labelled hypothetical optimistic end (L1 N3), not a floor and not our oracle.
            "hypothetical_9.5e3 (not a floor)": 9.5e3}


def model_t(block, n):
    a, b = block["fits"]["all16"]
    return a + b * n


def table(res):
    c1 = json.loads((res / "c1/c1_summary.json").read_text())
    c2 = json.loads((res / "c2/c2_timing.json").read_text())["blocks"]
    sig = json.loads((res / "sigma_dev/sigma_dev.json").read_text())["cases"]
    out = {}
    for case in ("B4x12", "B8x52"):
        sigma = sig[case]["sigma_q"]
        cands = {m: c2[f"{case}/{m}"]["t_c"][str(EPS0)]["primary"] for m in METHODS}
        best = min(cands, key=cands.get)
        t_c = cands[best]
        block = c2[f"{case}/{best}"]
        est = c1["cases"][case]["summary"]
        rows = {"primary": t_c,
                "fresh_cached (QF)": c2[f"{case}/{best}"]["t_c"][str(EPS0)]["fresh_cached"],
                "canonical on model convention": model_t(block, est["canonical"][METHODS[best]]
                                                         ["n_eps"][str(EPS0)]["point"])}
        by_basis = {b: model_t(block, s[METHODS[best]]["n_eps"][str(EPS0)]["point"])
                    for b, s in est.items()}
        qf = max(by_basis, key=by_basis.get)
        cf = min(by_basis, key=by_basis.get)
        rows[f"basis QF ({qf})"] = by_basis[qf]
        rows[f"basis CF ({cf}, selected after outcomes)"] = by_basis[cf]
        fit = est["canonical"][METHODS[best]]["fits"]["primary"]
        n_cf = (T995_15 * fit["A"] / (4 * 0.9 * EPS0)) ** (1 / fit["r"])
        rows["e_C = 0.9 eps (CF)"] = model_t(block, n_cf)
        n_ci = est["canonical"][METHODS[best]]["n_eps"][str(EPS0)]["ci95"]
        t_ci = [model_t(block, n) for n in n_ci]          # deviation D10: model-based
        ratios = {}
        for label, t in rows.items():
            dm = d_max(t, sigma)
            ratios[label] = {"t_c_s": t, "d_max": dm,
                             **{f"oracle/D_max [{d}]": v / dm for d, v in depths(case).items()}}
        out[case] = dict(sigma_q=sigma, comparator=best, candidates_s=cands,
                         t_c_model_ci95_from_n_ci=t_ci,
                         pending_candidates=["C5 OSS-BB", "C5 OSS", "C6 GPU", "plain-MC anchors"],
                         depths=depths(case), rows=ratios,
                         stop=all(r["oracle/D_max [favourable_leaf_table (QF)]"] > 10
                                  for r in ratios.values()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=False)
    result = dict(status="INTERIM: C5, C6 and anchors pending; comparator minimum is QF",
                  eps=EPS0, k=K, t_layer=T_LAYER, cases=table(Path(args.res)))
    (out_dir / "decision_interim.json").write_text(json.dumps(result, indent=1))
    for case, v in result["cases"].items():
        print(case, "comparator", v["comparator"], "sigma", round(v["sigma_q"], 4),
              "STOP", v["stop"])
        for label, r in v["rows"].items():
            print(f"  {label:45s} T_C={r['t_c_s']:8.3f}s D_max={r['d_max']:9.1f} "
                  + " ".join(f"{k.split('[')[1][:-1]}={x:,.0f}x" for k, x in r.items()
                             if k.startswith("oracle")))


if __name__ == "__main__":
    main()
