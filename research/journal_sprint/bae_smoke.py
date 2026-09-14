"""Local source smoke; external checkout is not redistributed."""

import argparse
import hashlib
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import types

import numpy as np

from .storage import finish_run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("checkout", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    checkout = args.checkout.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, output / "wrapper.py")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    if subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=checkout, text=True
    ).strip():
        raise RuntimeError("BAE checkout is not clean")
    if head != "4e1e13d6b151c9a3ca02157ebf6963c1c29ea793":
        raise RuntimeError("unexpected BAE source revision")
    metadata = {
        "commit": head,
        "seed": 317,
        "wrapper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "a": 0.17,
        "maxPT": 200,
        "scope": "ideal response smoke, no confidence or performance validation",
        "source_sha256": {
            str(p.relative_to(checkout)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in checkout.glob("src/**/*.py")
        },
    }
    (output / "planned.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    sys.path.insert(0, str(checkout))
    # Upstream src is a namespace directory; the host repository has a regular
    # src package that would otherwise take precedence. Isolate this subprocess.
    namespace = types.ModuleType("src")
    namespace.__path__ = [str(checkout / "src")]
    sys.modules["src"] = namespace
    np.random.seed(317)
    random.seed(317)
    try:
        from src.algorithms.BAE import BAE
        from src.algorithms.samplers import get_sampler
        from src.utils.models import QAEmodel

        model = QAEmodel(0.17, Tc=None, Tcrange=None)
        # Audit all measurements, including calibration if later enabled.
        measurements = []
        original = model.measure

        def measured(ctrl, shots, *pos, **kw):
            outcome = original(ctrl, shots, *pos, **kw)
            measurements.append(
                {"ctrl": float(ctrl), "shots": int(shots), "outcome": int(outcome), "kwargs": kw}
            )
            return outcome

        model.measure = measured
        estimator = BAE(model, False, None)
        sampler = get_sampler(
            "RWM",
            model,
            {
                "Npart": 200,
                "thr": 0.5,
                "var": "theta",
                "ut": "var",
                "log": True,
                "res_ut": False,
                "plot": False,
                "c": 2.38,
            },
        )
        means, stds, nqs = estimator.adapt_inference(
            sampler,
            {
                "wNs": 10,
                "Ns": 1,
                "TNs": 0,
                "k": 2,
                "Nevals": 10,
                "erefs": 3,
                "ethr": 3,
                "cap": False,
                "capk": 2,
            },
            maxPT=200,
        )
        total = sum((2 * m["ctrl"] + 1) * m["shots"] for m in measurements)
        if not np.isclose(total, nqs[-1]):
            raise RuntimeError("measurement ledger and reported cost differ")
        result = {
            "means": list(map(float, means)),
            "posterior_stds": list(map(float, stds)),
            "reported_costs": list(map(float, nqs)),
            "measurements": measurements,
            "total_A_equivalents": total,
            "budget_overshoot": total - 200,
            "note": (
                "Posterior SD is not a 95% confidence interval. Upstream resampling "
                "uses an unseeded default_rng; seed alone does not ensure replay."
            ),
        }
        (output / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        finish_run(output)
    except Exception as error:
        (output / "failure.json").write_text(
            json.dumps({"type": type(error).__name__, "message": str(error)}, indent=2),
            encoding="utf-8",
        )
        raise


if __name__ == "__main__":
    main()
