"""P3 of the 21 Oct 2026 frontier probe (desk estimate only; no circuit building).

P2 cleared its target, so P3 asks which oracle-cost cuts take the certified window class to M <= 1 at the primary
conventions. At the binding cell M scales with D_eff (same k, T_C, sigma/e), so M(design) = M_window * D / D_primary,
reading the existing modelled designs of the W0 floor (WS-floor variants) and the N1 floor sheet. All values mod, q+
(idealized floors). The limit D_eff <= D_max(k=1) / k is also reported.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/p3_oracle_desk.py [run001|run002]
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"  # run002 reads headline run002
OUT = ROOT / "results" / "frontier_probe_20261021" / "p3" / RUN
IN = dict(
    head=ROOT / f"results/frontier_probe_20261021/headline/{RUN}/headline_table.json",
    w0=ROOT / "results/plan110_w0/ws_floor/floor.json",
    n1=ROOT / "results/plan110_n1/headline/floor_sheet.json",
)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    h = load(IN["head"])
    cell = [c for c in h["cells"] if c["case"] == "B8x52" and c["eps"] == 0.001][0]
    d_prim = cell["D_eff_primary"]["used"]
    out = dict(meta=dict(script="research/frontier_probe_20261021/p3_oracle_desk.py", python=sys.version,
                         inputs_sha256={k: hashlib.sha256(Path(v).read_bytes()).hexdigest() for k, v in IN.items()}),
               D_eff_primary=d_prim, classes={})
    designs = {}
    for name, v in load(IN["w0"])["headline"]["B8x52"]["W1e7"].items():
        if v:
            b = v["comparison"][0]["by_t_layer"]["100ns"]["base"]
            designs[f"W0:{name}"] = dict(D_eff=b["eff_depth_supply_1e12"], reaction=b["eff_depth_supply_1e13"])
    for name, v in load(IN["n1"])["cases"]["B8x52"].items():
        r = v["by_width"]["W1e7"]["1e12|100ns"]
        designs[f"N1:{name}"] = dict(D_eff=r["D_eff"], reaction=r["depth"], T=r["T"])
    for cl in ("window_certified_fail0003", "window_certified_fail001", "explicit_best"):
        k = cell["k"][cl]
        m0 = cell["M"][cl]["primary"]
        k10 = k / m0
        d_lim = d_prim * k10 / k  # D_eff with M = 1
        out["classes"][cl] = dict(k=k, M_primary=m0, D_eff_limit_layers=d_lim, T_limit_per_iterate=d_lim * 1e12 * 1e-7,
                                  designs={n: dict(**v, M=m0 * v["D_eff"] / d_prim) for n, v in designs.items()},
                                  label="mod (idealized floors; q+)")
        print(cl, "k", round(k, 3), "M", round(m0, 3), "D_eff limit", round(d_lim, 1))
        for n, v in sorted(out["classes"][cl]["designs"].items(), key=lambda t: t[1]["M"]):
            print("   ", n, round(v["D_eff"], 1), "M", round(v["M"], 3))
    with open(OUT / "p3_desk.json", "x", encoding="utf-8") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
