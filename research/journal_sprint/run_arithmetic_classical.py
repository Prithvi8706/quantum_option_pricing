"""Same-continuous-contract development comparator, not confirmation/inference."""

import argparse
import json
import time
import platform
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import scipy

from .asian_basket import Basket, setup, fit_control, estimate
from .storage import ROOT, sha256, write_json, rng_for


CONFIG = dict(methods=["mc_cv", "rqmc_cv", "conditional_cv"], powers=[10, 12],
              repetitions=16, pilot_per_method=1024,
              stream="arithmetic-classical-development-v1", confirmation=False)
SOURCES = ["research/journal_sprint/"+name for name in (
    "run_arithmetic_classical.py", "asian_basket.py", "storage.py")]
INPUT = "results/journal_sprint/w13_encoding_v1/case_3.json"


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    hashes = {name: sha256(ROOT/name) for name in SOURCES+[INPUT]}
    write_json(output/"planned.json", dict(config=CONFIG, source_sha256=hashes,
               started_utc=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
               numpy=np.__version__, scipy=scipy.__version__))
    try:
        case = json.loads((ROOT/INPUT).read_text())
        basket = Basket(**case["basket"])
        start = time.perf_counter()
        model = setup(basket)
        setup_seconds = time.perf_counter()-start
        records, pilots = [], []
        for method in CONFIG["methods"]:
            start = time.perf_counter()
            beta, residual = fit_control(basket, model, rng_for(CONFIG["stream"], "pilot", method),
                                         method == "conditional_cv", CONFIG["pilot_per_method"])
            pilots.append(dict(method=method, beta=beta, root_residual=residual,
                               seconds=time.perf_counter()-start, paths=CONFIG["pilot_per_method"]))
            for power in CONFIG["powers"]:
                for replicate in range(CONFIG["repetitions"]):
                    seed = int(rng_for(CONFIG["stream"], method, power, replicate).integers(0, 2**32))
                    start = time.perf_counter()
                    value, residual = estimate(basket, model, power, seed, method, beta)
                    records.append(dict(method=method, power=power, replicate=replicate,
                                        seed=seed, price=value, root_residual=residual,
                                        seconds=time.perf_counter()-start, paths=2**power))
        summaries = []
        for method in CONFIG["methods"]:
            for power in CONFIG["powers"]:
                rows = [r for r in records if r["method"] == method and r["power"] == power]
                prices = np.array([r["price"] for r in rows])
                summaries.append(dict(method=method, power=power, mean=float(prices.mean()),
                                      replicate_sd=float(prices.std(ddof=1)),
                                      mean_standard_error=float(prices.std(ddof=1)/len(rows)**.5),
                                      total_seconds=sum(r["seconds"] for r in rows),
                                      paths_per_replicate=2**power, replicates=len(rows)))
        write_json(output/"results.json", dict(basket=case["basket"], setup_seconds=setup_seconds,
                   pilots=pilots, records=records, summaries=summaries,
                   qualification="continuous target; independent replicates conditional on paid fixed pilots; floating numerics; no certified interval, speedup ratio or confirmation"))
        if hashes != {name: sha256(ROOT/name) for name in hashes}:
            raise RuntimeError("source changed during comparator")
        write_json(output/"complete.json", dict(sha256={p.name: sha256(p) for p in output.iterdir() if p.is_file()}))
        print(json.dumps(summaries), flush=True)
    except BaseException as error:
        write_json(output/"failed.json", dict(type=type(error).__name__, message=str(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    run(parser.parse_args().output)
