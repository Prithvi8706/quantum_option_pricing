"""Q0 attribution diagnostic: P3 scramble_run in-process (no pool) for 8x52 scrambles 0-2."""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402
if len(sys.argv) > 2:
    L0 = np.load(HERE / "dump_conda_1264.npz")["L"]; _s = p3.setup
    p3.setup = lambda na, nt: (np.ascontiguousarray(L0), _s(na, nt)[1])
out = {s: p3.scramble_run((8, 52, s))["prefix"] for s in range(3)}
Path(HERE / f"inproc_{sys.argv[1]}.json").write_text(json.dumps(out))
print(sys.argv[1], {s: out[s][17] for s in out})
