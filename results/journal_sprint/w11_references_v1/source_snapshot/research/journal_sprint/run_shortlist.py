"""Frozen classical shortlist experiments with exclusive archives and numeric replay."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import shutil
import time

import numpy as np
from scipy.stats import t

from .asian_basket import Basket, estimate, fit_control, setup
from .run_encoding_decision import verify_inventory
from .shortlist_diagnostics import heston_grid, nested_diagnostic
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json


PROTOCOL = ROOT / "docs/journal_sprint/PROTOCOL_SHORTLIST_V1.md"
METHODS = ("mc_cv", "rqmc_raw", "rqmc_cv", "conditional_cv")


def contracts():
    return [Basket(d, steps, strike) for d in (2, 4) for steps in (12, 52)
            for strike in (90., 100., 110.)]


def seed_for(*keys):
    return int(rng_for("shortlist_v1", *keys).integers(0, 2**32 - 1))


def run_contract(contract):
    identity = (contract.assets, contract.dates, contract.strike)
    before = time.perf_counter()
    model = setup(contract)
    setup_seconds = time.perf_counter() - before
    pilots = {}
    for mode in ("raw", "conditional"):
        before = time.perf_counter()
        beta, residual = fit_control(contract, model, rng_for("shortlist_v1", *identity,
                                    "training", mode), conditional=mode == "conditional")
        pilots[mode] = dict(beta=beta, count=1024, max_root_residual=residual,
                            seconds=time.perf_counter() - before)
    references = []
    for rep in range(16):
        before = time.perf_counter()
        value, residual = estimate(contract, model, 13, seed_for(*identity, "reference", rep),
                                   "rqmc_cv", pilots["raw"]["beta"])
        references.append(dict(rep=rep, value=value, count=8192,
                               seconds=time.perf_counter() - before))
    reference = float(np.mean([r["value"] for r in references]))
    reference_se = float(np.std([r["value"] for r in references], ddof=1) / 4)
    rows = []
    for power in (10, 12):
        for method in METHODS:
            beta = 0 if method == "rqmc_raw" else pilots[
                "conditional" if method == "conditional_cv" else "raw"
            ]["beta"]
            for rep in range(8):
                before = time.perf_counter()
                value, residual = estimate(contract, model, power,
                                           seed_for(*identity, method, power, rep), method, beta)
                rows.append(dict(power=power, method=method, rep=rep, value=value,
                                 payoff_evaluations=2**power, max_root_residual=residual,
                                 seconds=time.perf_counter() - before))
    summaries = []
    for power in (10, 12):
        for method in METHODS:
            group = [r for r in rows if r["power"] == power and r["method"] == method]
            values = np.array([r["value"] for r in group])
            sd = float(values.std(ddof=1))
            summaries.append(dict(power=power, method=method, mean=float(values.mean()),
                                  between_rep_sd=sd,
                                  approximate_t_halfwidth=float(t.ppf(.975, 7) * sd / math_sqrt8()),
                                  rmse_to_reference=float(np.sqrt(np.mean((values-reference)**2))),
                                  mean_seconds=float(np.mean([r["seconds"] for r in group]))))
    return dict(contract=asdict(contract), setup_seconds=setup_seconds, pilots=pilots,
                reference=reference, reference_se=reference_se, reference_rows=references,
                geometric_control_mean=float(model["expected_control"]), rows=rows,
                summaries=summaries)


def math_sqrt8():
    return 8**0.5


def without_timing(value):
    if isinstance(value, dict):
        return {k: without_timing(v) for k, v in value.items() if not k.endswith("seconds")}
    if isinstance(value, list):
        return [without_timing(v) for v in value]
    return value


def assert_numeric_equal(a, b):
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b):
            raise ValueError("replay keys differ")
        for k in a:
            assert_numeric_equal(a[k], b[k])
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            raise ValueError("replay lengths differ")
        for x, y in zip(a, b):
            assert_numeric_equal(x, y)
    elif isinstance(a, float):
        if not np.isclose(a, b, atol=1e-10, rtol=1e-10):
            raise ValueError("numeric replay mismatch")
    elif a != b:
        raise ValueError("replay mismatch")


def verify(output):
    files = verify_inventory(output)
    plan = json.loads((output / "planned.json").read_text(encoding="utf-8"))
    for relative, digest in plan["config"]["replay_sources"].items():
        if sha256(ROOT / relative) != digest:
            raise ValueError("live source differs from frozen replay source")
    assert_numeric_equal(heston_grid(), json.loads((output / "heston.json").read_text()))
    assert_numeric_equal(nested_diagnostic(), json.loads((output / "nested.json").read_text()))
    count = 0
    for index, contract in enumerate(contracts()):
        saved = json.loads((output / f"basket_{index:02d}.json").read_text())
        assert_numeric_equal(without_timing(run_contract(contract)), without_timing(saved))
        count += len(saved["rows"])
        print(f"verified basket {index+1}/12", flush=True)
    return dict(verified=True, files=files, estimate_rows=count, reference_rows=192,
                heston_rows=72, nested_rows=40, nested_levels=8)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.output)))
        return
    sources = list((ROOT / "research/journal_sprint").glob("*.py")) + [PROTOCOL]
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    output = start_run(args.output, dict(replay_sources=hashes, namespace="shortlist_v1",
                                       quantum_results=False))
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(target) != hashes[str(p.relative_to(ROOT))]:
                raise ValueError("source changed during snapshot")
        write_json(output / "heston.json", heston_grid())
        write_json(output / "nested.json", nested_diagnostic())
        for index, contract in enumerate(contracts()):
            result = run_contract(contract)
            write_json(output / f"basket_{index:02d}.json", result)
            print(f"completed basket {index+1}/12", flush=True)
        finish_run(output)
    except Exception as error:
        write_json(output / "failure.json", dict(error=str(error)))
        raise


if __name__ == "__main__":
    main()
