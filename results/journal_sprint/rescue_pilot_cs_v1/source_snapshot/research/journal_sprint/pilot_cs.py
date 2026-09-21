"""Paid, sample-split beta-mixture CS for direct readout; established method."""

import argparse
import json
import math
import shutil

from scipy.special import betaln, xlogy, xlog1py

from .intervals import ConfidenceSet, clopper_pearson, price_decision
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .verify_rescue import verify


def pilot_interval(successes, shots, pilot_successes, pilot_shots=1024, alpha=0.025):
    for value in (successes, shots, pilot_successes, pilot_shots):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("integer counts required")
    if (
        pilot_shots < 1
        or not 0 <= pilot_successes <= pilot_shots
        or shots < pilot_shots
        or not 0 <= successes - pilot_successes <= shots - pilot_shots
        or not 0 < alpha < 1
    ):
        raise ValueError("invalid pilot or validation observations")
    n, s = shots - pilot_shots, successes - pilot_successes
    if n == 0:
        return 0.0, 1.0
    a, b = pilot_successes + 0.5, pilot_shots - pilot_successes + 0.5
    constant = betaln(s + a, n - s + b) - betaln(a, b)
    threshold = math.log(1 / alpha)

    def accepted(q):
        return constant - xlogy(s, q) - xlog1py(n - s, -q) <= threshold

    center = s / n
    if not accepted(center):
        raise ArithmeticError("invalid mixture minimum")
    left, right = 0.0, center
    for _ in range(60):
        mid = (left + right) / 2
        if accepted(mid):
            right = mid
        else:
            left = mid
    lo = left
    left, right = center, 1.0
    for _ in range(60):
        mid = (left + right) / 2
        if accepted(mid):
            left = mid
        else:
            right = mid
    return max(0.0, lo - 1e-12), min(1.0, right + 1e-12)


def reanalyze(row, profile):
    identity = {k: row[k] for k in ("contract", "encoding", "guard", "axis", "rep")}
    if row["status"] == "refused":
        return dict(
            **identity, status="refused", shots=0, pricing_cx=0, contains=None, erroneous=False
        )
    cal_low, cal_high = clopper_pearson(row["calibration_errors"], [16384, 16384], 0.0125)
    guard = row["guard"]
    fl, gl = [max(0.0, x - guard - 1e-12) for x in cal_low]
    fu, gu = [min(1.0, x + guard + 1e-12) for x in cal_high]
    trace = row["synthetic_path"]
    if trace[0][0] != 1024:
        raise ValueError("unexpected pilot size")
    b = profile["bounds"]
    from research.paper_a.benchmark import by_id
    from research.paper_a.references import black_scholes_call

    contract = by_id(row["contract"])
    truth = float(
        black_scholes_call(contract.S0, contract.K, contract.r, contract.sigma, contract.T)
    )
    for used, count in trace[1:]:
        low, high = pilot_interval(count, used, trace[0][1])
        if fu + gu >= 1:
            interval = ((0.0, 1.0),)
        else:
            lower = max(0.0, (low - fu) / (1 - fu - gl) - 1e-12)
            upper = min(1.0, (high - fl) / (1 - fl - gu) + 1e-12)
            interval = ((lower, upper),) if lower <= upper else ()
        decision = price_decision(
            ConfidenceSet(interval, 0.05), b["sensitivity"], b["offset"], row["bias"]
        )
        if decision["status"] == "precision_met" or used == row["cap"]:
            price_interval = decision["interval"]
            midpoint = None if price_interval is None else sum(price_interval) / 2
            return dict(
                **identity,
                **decision,
                shots=used,
                pilot_shots=1024,
                calibration_shots=32768,
                pricing_cx=used * profile["profiles"]["0"]["gates"]["cx"],
                total_shots=used + 32768,
                contains=bool(
                    price_interval is not None and price_interval[0] <= truth <= price_interval[1]
                ),
                erroneous=bool(decision["status"] == "precision_met" and abs(midpoint - truth) > 1),
            )
    raise ValueError("no post-pilot observations")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    verify(args.source)
    from pathlib import Path

    source = Path(args.source)
    sources = [
        ROOT / "research/journal_sprint/pilot_cs.py",
        ROOT / "docs/journal_sprint/PROTOCOL_PILOT_CS_V1.md",
    ]
    output = start_run(
        args.output,
        dict(
            source=str(source),
            source_manifest=sha256(source / "complete.json"),
            protocol="PROTOCOL_PILOT_CS_V1",
            sources={str(p.relative_to(ROOT)): sha256(p) for p in sources},
        ),
    )
    for p in sources:
        target = output / "source_snapshot" / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    rows = []
    try:
        for line in (source / "records.jsonl").read_text().splitlines():
            row = json.loads(line)
            if row["inference"] != "fixed_cp":
                continue
            profile = json.loads((source / f"profile_{row['contract']}.json").read_text())[
                row["encoding"]
            ]
            rows.append(reanalyze(row, profile))
        write_json(output / "records.json", rows)
        summary = dict(
            rows=len(rows),
            declared=sum(r["status"] == "precision_met" for r in rows),
            misses=sum(r["contains"] is False for r in rows),
            erroneous=sum(r["erroneous"] for r in rows),
            scope="post-result shared-path reanalysis; no independent replication",
        )
        write_json(output / "summary.json", summary)
        finish_run(output)
        print(json.dumps(summary))
    except Exception as exc:
        write_json(output / "failure.json", dict(completed_rows=len(rows), error=str(exc)))
        raise


if __name__ == "__main__":
    main()
