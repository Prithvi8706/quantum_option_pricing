"""Exact integer witnesses and limited arithmetic range checks, not a proof sweep."""

from __future__ import annotations

import json
from pathlib import Path

import mpmath as mp

from research.compound_feasibility.model import MODELS
from research.controlled_source_completion.finance import build_finance, float_reference
from research.controlled_source_completion.ir import evaluate
from research.controlled_completion_followup.financial_bridge import iv, upper


def certified_low_precision_witness():
    """Enclose an actual 24-bit arithmetic error, without a float price oracle."""
    import math

    mp.iv.dps = 70
    model = MODELS[-1]
    f, bits = 24, 16
    n, d = model.dates // 2, model.assets
    dt = iv(model.maturity) / model.dates
    rate, sigma = iv(model.rate), iv(model.sigma)
    h = iv(2) ** -bits
    radius = mp.iv.sqrt(-2 * mp.iv.log(h / 2))
    angle = 2 * mp.iv.pi * (iv(1) / 8 + h / 2)
    normals = [radius * mp.iv.cos(angle), radius * mp.iv.sin(angle)]
    logs = [mp.iv.log(iv(model.spot)) for _ in range(d)]
    lo, hi = mp.iv.log(iv(2) ** -16), mp.iv.log(iv(4096))
    stock_sum = iv(0)
    for j in range(n):
        common = normals[(j * (d + 1)) % 2]
        for asset in range(d):
            independent = normals[(j * (d + 1) + asset + 1) % 2]
            logs[asset] += (rate - sigma * sigma / 2) * dt + sigma * mp.iv.sqrt(dt) * (
                mp.iv.sqrt(iv(model.rho)) * common + mp.iv.sqrt(1 - iv(model.rho)) * independent
            )
            if float(logs[asset].a) > float(hi.b):
                guarded = hi
            elif float(logs[asset].b) < float(lo.a):
                guarded = lo
            elif float(logs[asset].a) > float(lo.b) and float(logs[asset].b) < float(hi.a):
                guarded = logs[asset]
            else:
                raise ArithmeticError("Interval straddles a guard: refine before certifying")
            stock_sum += mp.iv.exp(guarded)
    assert all(float(x.a) > float(hi.b) for x in logs)
    accrued = stock_sum / (d * model.dates)
    assert float(accrued.a) > model.strike
    discount = mp.iv.exp(-rate * iv(model.maturity) / 2)
    mean_return = sum(mp.iv.exp(rate * dt * j) for j in range(1, n + 1)) / n
    forward = discount / 2 * (iv(4096) * mean_return - 2 * (iv(model.strike) - accrued))
    # For k<0 all puts vanish and both continuation bounds equal forward.
    exact_base = discount * (forward - 6)
    graph = build_finance(model, f=f, q=bits)
    data = graph.as_dict()
    words = [0 if i % 2 == 0 else 8192 for i in range(len(graph.inputs))]
    output = evaluate(data, {"uniform_%d" % i: value for i, value in enumerate(words)})
    # A dyadic with this magnitude and f=24 is exactly representable in binary64.
    digital = iv(int(round(output["base_6"] * 2**f))) / (iv(2) ** f)
    error = abs(exact_base - digital)
    return {
        "model": model.name,
        "fraction_bits": f,
        "random_bits": bits,
        "all_radial_words": 0,
        "all_angular_words": 8192,
        "digital_base_6": output["base_6"],
        "digital_Y_6": output["Y_6"],
        "exact_real_base_interval": [
            math.nextafter(float(exact_base.a), -math.inf),
            upper(exact_base),
        ],
        "absolute_arithmetic_error_lower": math.nextafter(float(error.a), -math.inf),
        "absolute_arithmetic_error_upper": upper(error),
        "meaning": (
            "A reachable input refutes a uniform $0.002 arithmetic bound for f=24; "
            "it does not imply an expectation error of that size"
        ),
    }


def overflow_witnesses(data, values):
    """Reconstruct pre-reduction signed arithmetic using Python integers."""
    w, f = data["width"], data["fraction_bits"]
    modulus = 1 << w
    limit = 1 << (w - 1)

    def signed(x):
        return x - modulus if x >= limit else x

    found = []
    for index, node in enumerate(data["nodes"]):
        raw = [values[i] for i in node["args"]]
        val = [signed(x) for x in raw]
        op, p = node["op"], node["params"]
        if op == "add":
            result = val[0] + val[1]
        elif op == "sub":
            result = val[0] - val[1]
        elif op == "mul":
            result = val[0] * val[1] >> f
        elif op == "cmul":
            result = val[0] * p["c"] >> f
        elif op == "divide":
            result = (raw[0] << f) // raw[1] if raw[1] else modulus - 1
        elif op == "shift":
            shift = val[1]
            if abs(shift) > w:
                continue
            result = val[0] << shift if shift >= 0 else val[0] >> -shift
        else:
            continue
        if result < -limit or result >= limit:
            found.append(
                {
                    "node": index,
                    "op": op,
                    "arguments_integer": val,
                    "pre_modulus_integer": result,
                    "pre_modulus_value": result / (1 << f),
                    "stored_value": signed(values[node["out"][0]]) / (1 << f),
                }
            )
    return found


def run():
    rows = []
    for f, bits in ((24, 16), (40, 32)):
        for model in MODELS:
            graph = build_finance(model, f=f, q=bits)
            data = graph.as_dict()
            cases = []
            for radial in (0, (1 << bits) - 1):
                for eighth in range(8):
                    angle = eighth * (1 << bits) // 8
                    words = [radial if i % 2 == 0 else angle for i in range(len(graph.inputs))]
                    inputs = {"uniform_%d" % i: value for i, value in enumerate(words)}
                    output, values = evaluate(data, inputs, trace=True)
                    reference = float_reference(model, words, bits)
                    cases.append(
                        {
                            "radial_word": radial,
                            "angular_word": angle,
                            "overflow_witnesses": overflow_witnesses(data, values),
                            "max_abs_financial_output_difference": max(
                                abs(output[key] - reference[key]) for key in output
                            ),
                            "max_abs_Y_difference": max(
                                abs(output["Y_%g" % k] - reference["Y_%g" % k]) for k in (3, 6, 9)
                            ),
                            "max_abs_base_difference": max(
                                abs(output["base_%g" % k] - reference["base_%g" % k])
                                for k in (3, 6, 9)
                            ),
                        }
                    )
            rows.append(
                {"model": model.name, "fraction_bits": f, "random_bits": bits, "cases": cases}
            )
    report = {
        "status": (
            "128 deterministic edge diagnostics; not exhaustive range or arithmetic certification"
        ),
        "overflow_witness_count": sum(
            len(c["overflow_witnesses"]) for r in rows for c in r["cases"]
        ),
        "rows": rows,
        "certified_f24_counterexample": certified_low_precision_witness(),
    }
    path = Path("results/controlled_completion_followup/financial_arithmetic_edges.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "overflow_witness_count": report["overflow_witness_count"],
                "worst_output_difference": max(
                    c["max_abs_financial_output_difference"] for r in rows for c in r["cases"]
                ),
                "worst_Y_difference": max(
                    c["max_abs_Y_difference"] for r in rows for c in r["cases"]
                ),
                "worst_base_difference": max(
                    c["max_abs_base_difference"] for r in rows for c in r["cases"]
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    run()
