"""Q0 attribution diagnostic: is the unmodified pooled P3 run repeatable in one environment?"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402
p3.OUT = str(HERE / f"pooled_repeat_{sys.argv[1]}.json")
if __name__ == "__main__":
    p3.main()
    r = json.loads(Path(p3.OUT).read_text())["results"][1]
    print(sys.argv[1], "8x52 rate", r["rate_r"], "price", r["price"])
