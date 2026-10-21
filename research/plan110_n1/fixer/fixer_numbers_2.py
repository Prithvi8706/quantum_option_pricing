"""N2-fixer addendum: oracle thresholds under the symmetric distribution-free convention.

Run from the repository root:
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/fixer/fixer_numbers_2.py

Reads results/plan110_n1/fixer/fixer_numbers.json and the N1 hw card, writes
results/plan110_n1/fixer/fixer_numbers_2.json (exclusive create), appends rows.
Modelled arithmetic only.
"""
import hashlib
import json
import os
import sys

ROOT = os.getcwd()
F = {"FX": "results/plan110_n1/fixer/fixer_numbers.json",
     "HW": "results/plan110_n1/hwclassical/hw_classical_card_v2.json"}
OUT = "results/plan110_n1/fixer/fixer_numbers_2.json"
ROWS = "results/plan110_n1/fixer/rows.jsonl"


def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as fh:
        return json.load(fh)


def sha(p):
    with open(os.path.join(ROOT, p), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


FX, HW = load(F["FX"]), load(F["HW"])
thr = FX["d2_thresholds_B8_0.001"]
fac = FX["d4_c09"]["factor_total"]
W0_allfree = 114.0
out = {"meta": {"script": "research/plan110_n1/fixer/fixer_numbers_2.py", "python": sys.version,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site},
                "inputs_sha256": {k: sha(p) for k, p in F.items()},
                "label": "modelled (derived)", "direction": "q+ (symmetric convention slows the classical side)"},
       "c09_factor_B8_0.001": fac, "symmetric_thresholds": {}}
for name in ("explicit_best", "certified", "certified_dirsel", "window_fail001"):
    d = thr[name]["max_D_eff_layers"] * fac
    out["symmetric_thresholds"][name] = {"max_D_eff_layers": d, "max_T_per_iterate": d * 1e12 * 1e-7,
                                         "W0_allfree_over_threshold": W0_allfree / d}
with open(os.path.join(ROOT, OUT), "x", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
with open(os.path.join(ROOT, ROWS), "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"ws": "n2_fixer", "defect": [2, 4], "sub": "symmetric_thresholds",
                         "value": out["symmetric_thresholds"], "label": "modelled (derived)",
                         "direction": "q+", "source": OUT}) + "\n")
print(json.dumps(out, indent=1))
