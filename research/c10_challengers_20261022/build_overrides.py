"""Collect the measured C10/H16/C09 quantities into one overrides file for headline_m_probe.py run004.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/build_overrides.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "results/c10_challengers_20261022"
SRC = dict(timing=R / "timing/run001/c10_timing.json", h16=R / "h16_fast/run001/h16_fast.json",
           c09_B8_0001=R / "c09/B8x52_0.001_run001/c09_g4.json", c09_B4_0001=R / "c09/case0_0.001_run001/c09_g4.json",
           c09_B8_001=R / "c09/case1_0.01_run001/c09_g4.json", c09_B4_001=R / "c09/case0_0.01_run001/c09_g4.json")


def main():
    t = json.loads(SRC["timing"].read_text())
    h = json.loads(SRC["h16"].read_text())
    ov = dict(tc_speedup={k: v["speedup_median"]["preint_fast"] for k, v in t["cells"].items()},
              h16_ratio={k: v["preint_fast"]["ratio_1_over_16"] for k, v in h["cells"].items()},
              distfree_factor={})
    for key in ("c09_B8_0001", "c09_B4_0001", "c09_B8_001", "c09_B4_001"):
        d = json.loads(SRC[key].read_text())
        assert d["success"], key
        ov["distfree_factor"][f"{d['meta']['case']}|{d['meta']['eps']}"] = d["factor_df_over_practice"]
    out = R / "overrides_run004.json"
    with open(out, "x", encoding="utf-8") as f:
        json.dump(dict(overrides=ov, sources={k: str(p.relative_to(ROOT)) for k, p in SRC.items()},
                       sources_sha256={k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in SRC.items()},
                       label="meas (paired speedup; same-state 1/16 ratio; same-state distribution-free factor)"),
                  f, indent=1)
    print(json.dumps(ov, indent=1))


if __name__ == "__main__":
    main()
