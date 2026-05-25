"""
Precompute QAE option prices over a 54-point parameter grid and save to
data/qae_grid.pkl.

Usage
-----
  python app/precompute_qae.py             # full 54-point grid
  python app/precompute_qae.py --dry-run   # 3-point smoke-test with timing

The grid is:
  S0    : [80, 100, 120]
  K     : [95, 100, 105]
  T     : [0.5, 1.0]
  r     : 0.05  (fixed)
  sigma : [0.15, 0.20, 0.30]

Total: 3 × 3 × 2 × 3 = 54 combinations.

Each entry in the pickle is keyed by (S0, K, T, r, sigma) and stores:
  {
    "price":          float,
    "conf_int":       (float, float),
    "elapsed":        float,   # wall-clock seconds for that single QAE run
    "oracle_queries": int,     # IAE oracle call count (for log-log speedup chart)
  }

The script is resumable: existing results in the pkl are kept and
already-completed keys are skipped.
"""

import argparse
import itertools
import os
import pickle
import sys
import time

# Allow running from project root or from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tqdm import tqdm

from src.quantum import quantum_call

# ---------------------------------------------------------------------------
# Grid definition (matches design doc)
# ---------------------------------------------------------------------------

S0_VALUES = [80.0, 100.0, 120.0]
K_VALUES = [95.0, 100.0, 105.0]
T_VALUES = [0.5, 1.0]
R_FIXED = 0.05
SIGMA_VALUES = [0.15, 0.20, 0.30]

FULL_GRID = list(itertools.product(S0_VALUES, K_VALUES, T_VALUES, [R_FIXED], SIGMA_VALUES))

# 3 representative points that span low/mid/high vol and short/long expiry
DRY_RUN_POINTS = [
    (100.0, 100.0, 0.5, R_FIXED, 0.15),
    (100.0, 100.0, 1.0, R_FIXED, 0.30),
    (80.0, 95.0, 0.5, R_FIXED, 0.20),
]

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "qae_grid.pkl")


def load_existing(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}


def save(results: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(results, f)


def run_grid(points: list, results: dict, desc: str) -> dict:
    pending = [p for p in points if p not in results]
    skipped = len(points) - len(pending)
    if skipped:
        print(f"Skipping {skipped} already-computed point(s).")

    with tqdm(total=len(pending), desc=desc, unit="pt") as bar:
        for key in pending:
            S0, K, T, r, sigma = key
            bar.set_postfix(S0=S0, K=K, T=T, sigma=sigma)
            try:
                price, conf_int, elapsed, oracle_queries = quantum_call(S0, K, r, sigma, T)
                results[key] = {
                    "price": price,
                    "conf_int": conf_int,
                    "elapsed": elapsed,
                    "oracle_queries": oracle_queries,
                }
            except Exception as exc:
                tqdm.write(f"  ERROR {key}: {exc}")
                results[key] = {
                    "price": None,
                    "conf_int": (None, None),
                    "elapsed": None,
                    "oracle_queries": None,
                }
            save(results, OUTPUT_PATH)
            bar.update(1)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Precompute QAE prices for the dashboard grid.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run 3 representative points only to validate timing.",
    )
    args = parser.parse_args()

    points = DRY_RUN_POINTS if args.dry_run else FULL_GRID
    desc = "dry-run (3 pts)" if args.dry_run else "full grid (54 pts)"

    print(f"Output: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Mode:   {desc}")

    results = load_existing(OUTPUT_PATH)
    t_wall = time.perf_counter()

    results = run_grid(points, results, desc)

    total = time.perf_counter() - t_wall
    completed = sum(1 for v in results.values() if v["price"] is not None)
    failed = sum(1 for v in results.values() if v["price"] is None)

    print(f"\nDone — {completed} ok, {failed} failed, {total:.1f}s total.")
    if args.dry_run and completed:
        sample = next(v for v in results.values() if v["price"] is not None)
        print(f"Sample elapsed per point: {sample['elapsed']:.1f}s")
        est_full = sample["elapsed"] * 36
        print(f"Estimated full-grid time: ~{est_full / 60:.0f} min")


if __name__ == "__main__":
    main()
