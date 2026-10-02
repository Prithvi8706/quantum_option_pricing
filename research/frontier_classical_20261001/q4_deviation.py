"""Q4 deviation D2 (ANALYSIS_SPEC_STAGE_C.md deviation log): delta_fp over non-clip draws.

The literal Q4 run (results/frontier_classical_20261001/q4) took delta_fp over all draws,
including the 20 constructed spot-clip draws, where the IR clips log spots and the float
reference by design does not; delta_fp became 9.7e3 (4x12) and 2.9e6 (8x52), the flip band
covered every path, and the bound failed for that reason alone. The spec counts clip events
separately, so this post-hoc deviation recomputes delta_fp over draws without a clip event
and redoes the flip-band count. Same draws and seeds as the literal run; the literal result
stays primary in the record and both are reported.
  python -m research.frontier_classical_20261001.q4_deviation --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import math
import multiprocessing as mp
import subprocess
from pathlib import Path

import numpy as np
from scipy.stats import beta

from research.frontier_classical_20261001 import q4_payoff as q4


def recompute(case, pool):
    data, _, digest = q4.load_target(case)
    n_uniform = sum(1 for n in data["nodes"] if n["op"] == "input")
    sets, _ = q4.draws(case, n_uniform)
    errors, clip_count = [], 0
    for raw in sets.values():
        ir = pool.map(q4.ir_task, [(case, row) for row in raw], chunksize=8)
        ref = q4.ref_raw(case, raw)
        keep = ref[:, 3] == 0
        clip_count += int((~keep).sum())
        m_ir = np.array([x[1] for x in ir])
        errors.append(np.abs(m_ir - ref[:, 1])[keep])
    delta_fp = float(np.concatenate(errors).max())
    delta = 10 * delta_fp
    rows = pool.map(q4.law_task, [(case, w, delta) for w in range(q4.WORKERS)], chunksize=1)
    n = sum(r[0] for r in rows)
    band = sum(r[3] for r in rows)
    p_u = float(beta.ppf(0.99, band + 1, n - band)) if band < n else 1.0
    jump = math.exp(-case.rate * case.maturity) * (case.barrier - case.strike + delta)
    return dict(target_sha256=digest, clip_draws_excluded=clip_count, delta_fp_nonclip=delta_fp,
                delta=delta, flip=dict(paths=n, band_count=band, p_upper99=p_u,
                                       bound=jump * p_u, plug_in=jump * band / n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out_dir = Path(ap.parse_args().out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    literal = json.loads((out_dir.parent / "q4" / "q4.json").read_text())["cases"]
    result = dict(deviation="D2", commit=subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=sc.ROOT, capture_output=True, text=True).stdout.strip(),
        cases={})
    with mp.Pool(q4.WORKERS) as pool:
        for case in q4.DEV:
            name = f"B{case.na}x{case.nt}"
            row = recompute(case, pool)
            lit = literal[name]
            total = lit["law"]["bound"] + row["flip"]["bound"] + lit["arithmetic_max_unflipped"]
            row.update(law_bound=lit["law"]["bound"], arithmetic=lit["arithmetic_max_unflipped"],
                       total=total, passed=total <= 1e-4)
            result["cases"][name] = row
            (out_dir / "q4_deviation_d2.json").write_text(json.dumps(result, indent=1))
            print(name, json.dumps(row)[:400], flush=True)


if __name__ == "__main__":
    main()
