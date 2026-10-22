"""M rows for the self-bootstrapped (quantum-only) mean credit: k from p2/run003_self_mean, k_10x per column from the
explicit_best row of headline run004 (all measured inputs). mod, derived.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/derived_selfmean.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = dict(sm=ROOT / "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
          head=ROOT / f"results/frontier_probe_20261021/headline/{sys.argv[1] if len(sys.argv) > 1 else 'run004'}/headline_table.json")
OUT = ROOT / "results/frontier_probe_20261021/derived" / (sys.argv[2] if len(sys.argv) > 2 else "run003_self_mean")


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    sm = json.loads(IN["sm"].read_text())
    h = json.loads(IN["head"].read_text())
    rows = {}
    for c in h["cells"]:
        if c["overhead_T_C"]:
            continue
        key = f"{c['case']}|{c['eps']}"
        k = sm["cells"][key]["best"]["k"]
        kb = c["k"]["explicit_best"]
        rows[key] = dict(k=k, M={col: k * c["M"]["explicit_best"][col] / kb
                                 for col in ("primary", "all_free_oracle", "one_lane_one_core", "distfree_stageC",
                                             "all_free_distfree_stageC", "e_eq_eps")})
    best = {col: min((v["M"][col], key) for key, v in rows.items()) for col in rows[next(iter(rows))]["M"]}
    out = dict(inputs_sha256={a: hashlib.sha256(b.read_bytes()).hexdigest() for a, b in IN.items()}, cells=rows,
               min_over_eligible=best, label="mod (derived; window certified, U2 + direction-select, quantum-only mean)")
    with open(OUT / "derived_selfmean.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for col, (m, key) in best.items():
        print(col, round(m, 3), key)


if __name__ == "__main__":
    main()
