"""Contract validation and independent accounting checks; no new experiments."""

from dataclasses import fields, replace

import pytest

from research.journal_sprint.price_contract import (
    BIAS_COMPONENTS, STAGES, BiasComponent, PriceContract, ResourceEntry,
    resource_totals,
)


def contract():
    return PriceContract(
        "example", "discounted discrete-monitoring expectation", "USD", "toy",
        -2, 10, tuple(BiasComponent(n, .01, "test assumption") for n in BIAS_COMPONENTS),
        "test telescoping chain, each term already in USD",
        ("ideal preparation except supplied bounds",),
    )


def resources():
    return [ResourceEntry(s, "measured", "test record", i, 2*i, .1*i)
            for i, s in enumerate(STAGES)]


def test_known_bound_and_adapter():
    c = contract()
    assert c.bias_bound == pytest.approx(.06)
    assert c.readiness(.1) == "eligible_for_statistical_design"
    assert c.readiness(.06) == "bias_bound_exhausts_tolerance"
    e = c.to_encoding(2)
    assert (e.offset, e.sensitivity, e.cost_per_shot) == (-2, 10, 2)
    assert e.bias == c.bias_bound


def test_observed_error_never_substitutes_for_unknown_bound():
    c = contract()
    parts = (replace(c.components[0], bound=None, observed_error=0),) + c.components[1:]
    c = replace(c, components=parts)
    assert c.bias_bound is None
    assert c.readiness(1) == "unknown_bias"
    with pytest.raises(ValueError, match="unknown bias"):
        c.to_encoding(1)


@pytest.mark.parametrize("field,value", [
    ("offset", True), ("offset", "0"), ("sensitivity", 0),
    ("sensitivity", float("inf")), ("currency", " "),
    ("composition_evidence", ""), ("assumptions", []),
    ("assumptions", ("",)), ("components", ()),
])
def test_invalid_contract(field, value):
    with pytest.raises(ValueError):
        replace(contract(), **{field: value})


def test_duplicate_component_rejected():
    c = contract()
    with pytest.raises(ValueError):
        replace(c, components=(c.components[0],) * len(BIAS_COMPONENTS))


@pytest.mark.parametrize("bound", [-1, True, "1", float("nan"), float("inf")])
def test_invalid_bound(bound):
    with pytest.raises(ValueError):
        BiasComponent(BIAS_COMPONENTS[0], bound, "test")


def test_provenance_required_even_for_zero():
    with pytest.raises(ValueError):
        BiasComponent(BIAS_COMPONENTS[0], 0, "")


def test_truth_not_in_controller_interface():
    names = {f.name for f in fields(PriceContract)}
    assert not names & {"true_price", "amplitude", "statevector", "pricing_observations"}
    c = contract()
    changed = replace(c, components=tuple(replace(p, observed_error=999) for p in c.components))
    assert changed.to_encoding(1) == c.to_encoding(1)
    with pytest.raises(TypeError):
        PriceContract(true_price=1)


def test_separate_units_and_all_stages_charged():
    assert resource_totals(resources()) == {
        "kind": "measured", "shots": 10, "logical_cx": 20, "elapsed_seconds": 1.0,
    }


def test_unknown_cost_not_zero_and_other_axes_remain_known():
    rows = resources()
    rows[1] = replace(rows[1], logical_cx=None)
    totals = resource_totals(rows)
    assert totals["logical_cx"] is None
    assert totals["shots"] == 10


def test_forecasts_cannot_be_summed_with_measurements():
    rows = resources()
    rows[1] = replace(rows[1], kind="projected")
    with pytest.raises(ValueError, match="cannot be mixed"):
        resource_totals(rows)


@pytest.mark.parametrize("rows", [[], resources()[:-1], [resources()[0]] * 5])
def test_missing_or_duplicate_stage_rejected(rows):
    with pytest.raises(ValueError):
        resource_totals(rows)


@pytest.mark.parametrize("field,value", [
    ("shots", True), ("shots", 1.5), ("logical_cx", -1),
    ("elapsed_seconds", float("nan")), ("elapsed_seconds", -1),
    ("kind", "actual-ish"), ("stage", "other"), ("evidence", ""),
])
def test_invalid_resource(field, value):
    with pytest.raises(ValueError):
        replace(resources()[0], **{field: value})


def test_overflow_is_explicit():
    c = contract()
    c = replace(c, components=tuple(replace(p, bound=1e308) for p in c.components))
    with pytest.raises(ValueError, match="overflow"):
        _ = c.bias_bound
    with pytest.raises(ValueError, match="overflow"):
        resource_totals([replace(r, elapsed_seconds=1e308) for r in resources()])
