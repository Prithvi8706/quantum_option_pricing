"""Overrides for headline run006 = run005 overrides + float32-GEMM challenger at the cell where it is faster.
preint_fast32 passes the spec's eps/10 admission check (f32/run001.json: mean shift ~1e-9, max point 1e-5) and is
1.22x faster than preint_fast at B8x52 $0.001 (timing_f32/run001, paired, 10 reps; no gain at B4x12). Its speedup over
Stage C is composed as (run005 QF speedup) x (paired f32/fast ratio) where the ratio exceeds 1; other cells unchanged.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/build_overrides_run006.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/c10_challengers_20261022"
SRC = dict(run005=R / "overrides_run005.json", f32=R / "timing_f32/run001/c10_timing_f32.json", check=R / "f32/run001.json")


def main():
    o5 = json.loads(SRC["run005"].read_text())
    f32 = json.loads(SRC["f32"].read_text())["cells"]
    chk = json.loads(SRC["check"].read_text())
    assert all(v["passes_eps_over_10"] for v in chk.values())
    ov = json.loads(json.dumps(o5["overrides"]))
    used = {}
    for k, v in f32.items():
        ratio = v["f32_over_fast"]
        if ratio > 1:
            ov["tc_speedup"][k] = o5["overrides"]["tc_speedup"][k] * ratio
            used[k] = dict(f32_over_fast=ratio, speedup_run005=o5["overrides"]["tc_speedup"][k],
                           speedup_run006=ov["tc_speedup"][k])
    with open(R / "overrides_run006.json", "x", encoding="utf-8") as f:
        json.dump(dict(overrides=ov, f32_applied=used,
                       sources_sha256={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in SRC.items()},
                       label="meas inputs; f32 admitted by the eps/10 check; composition assumes ratio invariance (assm)"),
                  f, indent=1)
    print(json.dumps(used, indent=1))


if __name__ == "__main__":
    main()
