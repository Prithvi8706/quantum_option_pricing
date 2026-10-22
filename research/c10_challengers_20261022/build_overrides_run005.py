"""Overrides for headline run005, after the C10/C09 R2 review (results/c10_challengers_20261022/review/c10_review.jsonl).
- tc_speedup: QF minimum over today's same-state measurements of Stage C preint / preint_fast (paired timing run001;
  h16_fast 16-worker medians; for B8x52 $0.001 also the unchanged C2 harness re-time vs the paired fast median).
- h16_ratio: QF maximum of (a) today's same-state 1/16 ratio of preint_fast and (b) the review's ratio-transfer value
  H16run001_ratio x speedup16 / speedup1 (a smaller ratio is q-).
- distfree_factor: minimum over distribution-free methods (iid EB, C09; replicated RQMC EB, C09b) per cell.
- apply_before_envelope: the T_C speedup is applied to the raw candidate before the monotone envelope (review 6).
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/build_overrides_run005.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/c10_challengers_20261022"
SRC = dict(timing=R / "timing/run001/c10_timing.json", h16=R / "h16_fast/run001/h16_fast.json",
           harness=R / "c2_harness_today/run001.json",
           h16_run001=ROOT / "results/frontier_probe_20261021/headline/run002/headline_table.json")
C09 = {"B8x52_H140|0.001": ("c09/B8x52_0.001_run001/c09_g4.json", "c09b/B8x52_0.001_run001/c09b_rep.json"),
       "B4x12_H140|0.001": ("c09/case0_0.001_run001/c09_g4.json", "c09b/case0_0.001_run001/c09b_rep.json"),
       "B8x52_H140|0.01": ("c09/case1_0.01_run001/c09_g4.json", "c09b/case1_0.01_run001/c09b_rep.json"),
       "B4x12_H140|0.01": ("c09/case0_0.01_run001/c09_g4.json", "c09b/case0_0.01_run001/c09b_rep.json")}


def main():
    t = json.loads(SRC["timing"].read_text())["cells"]
    h = json.loads(SRC["h16"].read_text())["cells"]
    hv = json.loads(SRC["harness"].read_text())
    old = json.loads(SRC["h16_run001"].read_text())["h16_one_core_ratio"]
    speed, ratio, df, detail = {}, {}, {}, {}
    for k in t:
        cands = {"paired": t[k]["speedup_median"]["preint_fast"],
                 "h16_16w": h[k]["preint"]["w16"] / h[k]["preint_fast"]["w16"]}
        if k == "B8x52_H140|0.001":
            cands["c2_harness_vs_paired_fast"] = hv["median"] / t[k]["methods"]["preint_fast"]["median_wall"]
        speed[k] = min(cands.values())
        s1 = h[k]["preint"]["w1"] / h[k]["preint_fast"]["w1"]
        r_today = h[k]["preint_fast"]["ratio_1_over_16"]
        r_transfer = old[k.replace("_H140", "")] * speed[k] / s1
        ratio[k] = max(r_today, r_transfer)
        f_iid = json.loads((R / C09[k][0]).read_text())
        f_rep = json.loads((R / C09[k][1]).read_text())
        assert f_iid["success"] and f_rep["success"]
        df[k] = min(f_iid["factor_df_over_practice"], f_rep["factor_df_over_practice"])
        detail[k] = dict(speed_candidates=cands, speed_used=speed[k], ratio_today=r_today, ratio_transfer=r_transfer,
                         ratio_used=ratio[k], factor_iid=f_iid["factor_df_over_practice"],
                         factor_rep=f_rep["factor_df_over_practice"], factor_used=df[k])
    out = R / "overrides_run005.json"
    srcs = dict(SRC, **{f"c09_{k}": R / v[0] for k, v in C09.items()}, **{f"c09b_{k}": R / v[1] for k, v in C09.items()})
    with open(out, "x", encoding="utf-8") as f:
        json.dump(dict(overrides=dict(tc_speedup=speed, h16_ratio=ratio, distfree_factor=df, apply_before_envelope=True),
                       detail=detail, sources_sha256={k: hashlib.sha256(Path(p).read_bytes()).hexdigest()
                                                      for k, p in srcs.items()},
                       label="meas inputs; QF choices where uncertain (spec 0.5); distfree = min over methods"), f, indent=1)
    for k, d in detail.items():
        print(k, {a: (round(b, 3) if isinstance(b, float) else {c: round(e, 3) for c, e in b.items()}) for a, b in d.items()})


if __name__ == "__main__":
    main()
