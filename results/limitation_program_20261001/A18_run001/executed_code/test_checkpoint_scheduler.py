"""Independent lifetime negatives and exhaustive small-word schedule replay."""

from copy import deepcopy
from itertools import product

import pytest

from research.limitation_program_20261001.checkpoint_scheduler import (
    HEURISTICS,
    LIMITS,
    minimum_required,
    plan_checkpoint,
    retain_all,
    retain_all_plan,
    schedule,
    validate_schedule,
)


def chain(count=3, aliases=1):
    return dict(
        floor=2 + 2 * aliases,
        groups=[
            dict(
                id=gid,
                preds=[gid - 1] if gid else [],
                width=2,
                private=1,
                cost=10 + gid,
                outputs=[gid],
            )
            for gid in range(count)
        ],
        outputs=[
            dict(outputname=f"out{index}", value=count - 1, group=count - 1)
            for index in range(aliases)
        ],
    )


def physical(spans):
    return [
        wire for span in spans for wire in range(span["offset"], span["offset"] + span["width"])
    ]


def small_word_replay(plan, result, raw, dirty):
    """Execute XOR semantics on actual scheduled wires, independently of planner."""
    bits = [0] * result["logical_qubits"]
    bits[0], bits[1] = raw & 1, (raw >> 1) & 1
    for index, initial in enumerate(dirty):
        bits[2 + index * 2] = initial & 1
        bits[3 + index * 2] = (initial >> 1) & 1
    groups = {group["id"]: group for group in plan["groups"]}
    registers = {}
    output_index = {binding["outputname"]: index for index, binding in enumerate(plan["outputs"])}

    def read(wires):
        return sum(bits[wire] << index for index, wire in enumerate(wires))

    for move in result["moves"]:
        gid = move["group"]
        if move["kind"] == "copy_output":
            value = read(registers[gid])
            index = output_index[move["outputname"]]
            for bit in range(2):
                bits[2 + index * 2 + bit] ^= (value >> bit) & 1
            continue
        group = groups[gid]
        operand = read(registers[group["preds"][0]]) if group["preds"] else raw
        value = (operand * operand + gid + 1) % 4
        wires = physical(move["storage"])
        for bit, wire in enumerate(wires):
            bits[wire] ^= (value >> bit) & 1
        if move["kind"] == "compute":
            registers[gid] = wires
        else:
            assert read(wires) == 0, "erase used a different recomputed predecessor"
            del registers[gid]
    assert not registers
    assert bits[:2] == [raw & 1, raw >> 1]
    assert not any(bits[plan["floor"] :]), "checkpoint or reused scratch left dirty"
    return [
        sum(bits[2 + index * 2 + bit] << bit for bit in range(2)) for index in range(len(dirty))
    ]


@pytest.mark.parametrize("heuristic", HEURISTICS)
@pytest.mark.parametrize("aliases", (1, 2))
def test_exhaustive_small_chain_dirty_outputs_inverse_and_width_saving(heuristic, aliases):
    plan = chain(aliases=aliases)
    baseline = retain_all(plan)
    candidate = schedule(plan, baseline["cap"] - 2, heuristic)
    assert candidate["passed"], candidate
    assert candidate["logical_qubits"] < baseline["logical_qubits"]
    inverse = deepcopy(candidate)
    inverse["moves"] = list(reversed(inverse["moves"]))
    for move in inverse["moves"]:
        if move["kind"] != "copy_output":
            move["kind"] = "erase" if move["kind"] == "compute" else "compute"
    validate_schedule(plan, inverse)
    for raw in range(4):
        reference = raw
        for gid in range(3):
            reference = (reference * reference + gid + 1) % 4
        for dirty in product(range(4), repeat=aliases):
            actual = small_word_replay(plan, candidate, raw, dirty)
            assert actual == [initial ^ reference for initial in dirty]
            assert small_word_replay(plan, inverse, raw, actual) == list(dirty)


@pytest.mark.parametrize("heuristic", HEURISTICS)
def test_atomic_multioutput_and_repeated_predecessor(heuristic):
    plan = dict(
        floor=8,
        groups=[
            dict(id=0, preds=[], width=4, private=1, cost=3, outputs=[0, 1]),
            dict(id=1, preds=[0, 0], width=2, private=1, cost=4, outputs=[2]),
            dict(id=2, preds=[0, 1], width=2, private=1, cost=7, outputs=[3]),
        ],
        outputs=[
            dict(outputname="first", value=3, group=2),
            dict(outputname="alias", value=3, group=2),
            dict(outputname="shared", value=1, group=0),
        ],
    )
    result = schedule(plan, retain_all(plan)["cap"], heuristic)
    assert result["passed"]
    assert result["legality"]["copied_outputs"] == 3
    assert plan["groups"][1]["preds"] == [0, 0]
    for move in result["moves"]:
        if move["group"] == 0 and move["kind"] != "copy_output":
            assert sum(span["width"] for span in move["storage"]) == 4


@pytest.mark.parametrize("heuristic", HEURISTICS)
def test_infeasible_cap_is_proved_without_emitting_dirty_partial_schedule(heuristic):
    plan = chain()
    result = schedule(plan, minimum_required(plan)["total"] - 1, heuristic)
    assert not result["passed"]
    assert result["infeasible_proved"]
    assert not result["moves"]


def test_scope_adapters_preserve_original_ids_and_prospective_heuristic_names():
    plan = chain()
    scope = dict(
        fixed_floor=plan["floor"],
        groups=[dict(group, out=group["outputs"]) for group in plan["groups"]],
        outputs=[dict(binding, name=binding["outputname"]) for binding in plan["outputs"]],
    )
    baseline = retain_all_plan(scope)
    for name in ("block-checkpointing", "cost-aware"):
        candidate = plan_checkpoint(scope, baseline["cap"] - 2, name)
        assert candidate["feasible"] and candidate["heuristic"] == name


def test_search_limit_discards_nonexecutable_partial_moves(monkeypatch):
    monkeypatch.setitem(LIMITS, "max_events", 0)
    result = schedule(chain(), retain_all(chain())["cap"], "cost-aware")
    assert not result["passed"]
    assert not result["infeasible_proved"]
    assert result["reason"] == "recursive event limit"
    assert result["moves"] == []


def test_paid_invocation_limit_is_checked_before_final_append(monkeypatch):
    monkeypatch.setitem(LIMITS, "max_moves", 2)
    result = schedule(chain(), retain_all(chain())["cap"], "cost-aware")
    assert not result["passed"]
    assert result["reason"] == "paid invocation limit"
    assert result["moves"] == []


@pytest.mark.parametrize(
    "damage",
    (
        "missing-pred",
        "dirty-overwrite",
        "partial-atomic-output",
        "duplicate-copy",
        "missing-copy",
        "unknown-kind",
        "cap-overflow",
        "floor-overwrite",
        "dirty-compute",
        "wrong-erase-register",
        "missing-cleanup",
    ),
)
def test_independent_legality_negative_controls(damage):
    plan = chain()
    result = retain_all(plan)
    moves = result["moves"]
    if damage == "missing-pred":
        del moves[0]
    elif damage == "dirty-overwrite":
        moves[1]["storage"] = deepcopy(moves[0]["storage"])
    elif damage == "partial-atomic-output":
        moves[0]["storage"][0]["width"] -= 1
    elif damage == "duplicate-copy":
        moves.insert(4, deepcopy(moves[3]))
    elif damage == "missing-copy":
        del moves[3]
    elif damage == "unknown-kind":
        moves[0]["kind"] = "overwrite"
    elif damage == "cap-overflow":
        moves[0]["private_storage"][0]["offset"] = result["cap"]
    elif damage == "floor-overwrite":
        moves[0]["storage"][0]["offset"] = 0
    elif damage == "dirty-compute":
        moves.insert(1, deepcopy(moves[0]))
    elif damage == "wrong-erase-register":
        moves[4]["storage"][0]["offset"] += 1
    elif damage == "missing-cleanup":
        moves.pop()
    with pytest.raises(ValueError):
        validate_schedule(plan, result)


@pytest.mark.parametrize(
    "damage", ("forward", "duplicate-producer", "wrong-owner", "duplicate-name")
)
def test_invalid_graph_bindings_fail_before_planning(damage):
    plan = chain()
    if damage == "forward":
        plan["groups"][0]["preds"] = [1]
    elif damage == "duplicate-producer":
        plan["groups"][1]["outputs"] = [0]
    elif damage == "wrong-owner":
        plan["outputs"][0]["group"] = 0
    elif damage == "duplicate-name":
        plan["outputs"].append(deepcopy(plan["outputs"][0]))
    with pytest.raises(ValueError):
        schedule(plan, 100, "block")


def test_undeclared_heuristic_is_not_an_extra_candidate():
    with pytest.raises(ValueError):
        schedule(chain(), 100, "third-search")
