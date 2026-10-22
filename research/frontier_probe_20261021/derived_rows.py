"""Derived binding-cell rows for the probe memo (products and ratios of run002 outputs only; mod).

M = k / k_10x with k_10x for each column taken from the explicit_best row of headline run002 (same cell, same T_C,
sigma/e and D_eff), applied to the P2 run002 window constants under each credit combination.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/derived_rows.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "frontier_probe_20261021" / "derived" / (sys.argv[2] if len(sys.argv) > 2 else "run001")
IN = dict(p2=ROOT / "results/frontier_probe_20261021/p2/run002/p2_window.json",
          head=ROOT / f"results/frontier_probe_20261021/headline/{sys.argv[1] if len(sys.argv) > 1 else 'run002'}/headline_table.json")


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    k = json.loads(IN["p2"].read_text(encoding="utf-8"))["k"]
    h = json.loads(IN["head"].read_text(encoding="utf-8"))
    cell = [c for c in h["cells"] if c["case"] == "B8x52" and c["eps"] == 0.001][0]
    kb = cell["k"]["explicit_best"]
    cols = ("primary", "distfree_stageC", "all_free_oracle", "one_lane_one_core", "e_eq_eps")
    k10 = {c: kb / cell["M"]["explicit_best"][c] for c in cols if c != "e_eq_eps"}
    rows = []
    for spl, ml, credits in (("8192/211", "price+L1", "U1+U2"), ("8192/211", "no mean", "U2 only"),
                             ("64", "price+L1", "U1 only"), ("64", "no mean", "none")):
        for fail in ("3/1000", "1/100"):
            for ds in (True, False):
                v = k[f"B8x52|0.001|0.45eps|{spl}|{ml}|with_impl_budget|fail {fail}"]
                kk = v["k_direction_select"] if ds else v["k_without_direction_select"]
                rows.append(dict(credits=credits, fail=fail, direction_select=ds, k=kk,
                                 M={c: kk / k10[c] for c in k10}, label="mod (derived)", direction="q+"))
    out = dict(meta=dict(script="research/frontier_probe_20261021/derived_rows.py", python=sys.version,
                         inputs_sha256={a: hashlib.sha256(b.read_bytes()).hexdigest() for a, b in IN.items()}),
               k10x=k10, rows=rows)
    with open(OUT / "derived.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for r in rows:
        print(f"{r['credits']:8s} fail {r['fail']:7s} DS {str(r['direction_select']):5s} k {r['k']:7.3f} "
              + " ".join(f"{c}={m:.3f}" for c, m in r["M"].items()))


if __name__ == "__main__":
    main()
