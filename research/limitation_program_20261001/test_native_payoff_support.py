"""Independent SSA exhaustions and binding guards for exact digital support."""

import json
import math
from pathlib import Path

import pytest

from research.advantage_frontier_20260923.barrier_oracle_depth import exp_estrin
from research.controlled_source_completion.ir import Graph, evaluate
from research.limitation_program_20261001.prove_native_payoff_support import (
    certify,
    product_bounds,
    stock_support,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("fraction", (4, 8, 12))
def test_every_small_clipped_integer_against_original_ssa_exp(fraction):
    Q = 1 << fraction
    graph = Graph(f=fraction, integer_bits=8)
    x = graph.input("x", graph.w, preparation="free")
    graph.outputs = {"stock": exp_estrin(graph, x)}
    target = graph.as_dict()
    proof = stock_support(
        graph.w,
        fraction,
        -2 * Q,
        2 * Q,
        round(Q / math.log(2)),
        round(math.log(2) * Q),
        [round(Q / math.factorial(j)) for j in range(13)],
    )
    for word in range(-2 * Q, 2 * Q + 1):
        _, trace = evaluate(target, {"x": word % (1 << graph.w)}, True)
        row = next(
            c
            for c in proof["cells"]
            if c["clipped_log_interval"][0] <= word <= c["clipped_log_interval"][1]
        )
        value = trace[graph.outputs["stock"]]
        assert row["stock_interval"][0] <= value <= row["stock_interval"][1]


@pytest.mark.parametrize("assets,dates,case", ((4, 12, "B4x12"), (8, 52, "B8x52")))
def test_actual_whole_financial_binding_and_strict_barrier_support(assets, dates, case):
    path = (
        ROOT
        / "results/limitation_program_20261001/A10_coefficient_run001"
        / case
        / "min-depth/target.json"
    )
    target = json.loads(path.read_text(encoding="utf-8"))
    certificate = certify(target, assets, dates)
    assert certificate["payoff_raw_bounds"][0] == 0
    assert 0 < certificate["payoff_raw_bounds"][1] < 40 * (1 << 40)
    assert certificate["selector_random_bits"] == 46
    assert len(certificate["stock_ids"]) == assets * dates


@pytest.mark.parametrize("mutation", ("discount", "barrier", "output"))
def test_mismatched_actual_target_rejected(mutation):
    path = (
        ROOT
        / "results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json"
    )
    target = json.loads(path.read_text(encoding="utf-8"))
    if mutation == "output":
        target["outputs"]["Y"] -= 1
    elif mutation == "discount":
        next(n for n in reversed(target["nodes"]) if n["op"] == "cmul")["params"]["c"] += 1
    else:
        next(
            n
            for n in target["nodes"]
            if n["op"] == "const" and n["params"]["value"] == 140 * (1 << 40)
        )["params"]["value"] += 1
    with pytest.raises(ValueError, match="actual financial target"):
        certify(target, 4, 12)


def test_square_refinement_requires_exact_same_operand():
    with pytest.raises(ValueError, match="same exact operand"):
        product_bounds((-4, 7), (0, 7), 4, square=True)


def test_square_refinement_contains_all_pairs_on_diagonal():
    for lo in range(-6, 7):
        for hi in range(lo, 7):
            a, b = product_bounds((lo, hi), (lo, hi), 3, square=True)
            assert all(a <= x * x // 8 <= b for x in range(lo, hi + 1))


def test_invalid_coefficients_and_unbounded_shift_rejected():
    with pytest.raises(ValueError, match="coefficient"):
        stock_support(12, 4, -32, 32, 23, 11, [16, -1])
    with pytest.raises(ArithmeticError):
        stock_support(12, 4, -1024, 1024, 23, 11, [16, 16])
