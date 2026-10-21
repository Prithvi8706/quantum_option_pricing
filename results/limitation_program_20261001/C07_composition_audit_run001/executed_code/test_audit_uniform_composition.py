"""Formula audit guards, using no financial observations."""

from fractions import Fraction

import pytest

from research.limitation_program_20261001 import audit_uniform_composition as audit


def screen():
    return dict(
        dates=[dict(date=j) for j in range(1, 13)],
        omitted_terms_credited_as_certified_zero=False,
        full_path_stock_or_basket_discrepancy_certified=False,
        complete_continuous_price_certificate=False,
        methods={
            "density": dict(
                actual_probability_lower_bound_claimed=False,
                actual_price_bias_lower_bound_claimed=False,
            )
        },
    )


@pytest.mark.parametrize("date", [1, 6, 12])
def test_independent_centered_formula_is_tighter_than_density(date):
    result = audit.independent_formula(Fraction(date, 40000), Fraction(3 * date, 1000))
    assert 0 < result["centered_interval_maximum"][1] < result["density"][0] < 1


@pytest.mark.parametrize("dates", [1, 52])
def test_wrong_date_contract_rejected(dates):
    data = screen()
    data["dates"] = [dict(date=j) for j in range(1, dates + 1)]
    with pytest.raises(ValueError, match="12 dates"):
        audit.check_scope_flags(data)


@pytest.mark.parametrize(
    "flag",
    [
        "omitted_terms_credited_as_certified_zero",
        "full_path_stock_or_basket_discrepancy_certified",
        "complete_continuous_price_certificate",
        "actual_price_bias_lower_bound_claimed",
    ],
)
def test_optimistic_formula_cannot_be_promoted_to_actual_error(flag):
    data = screen()
    if flag.startswith("actual"):
        data["methods"]["density"][flag] = True
    else:
        data[flag] = True
    with pytest.raises(ValueError):
        audit.check_scope_flags(data)


def test_formula_upper_below_independent_reference_rejected():
    with pytest.raises(ValueError):
        audit.receipt.enclose_claim([[0, 1], [1, 4]], [[0, 1], [1, 3]], "Upper")


def test_coefficients_are_read_from_actual_typed_graph_without_replay():
    source = audit.receipt.read(audit.RESULTS / "C06_pair_run001/certificate.json")
    candidate = next(x for x in source["candidates"] if x["cutoff_bits"] == 20)
    target = audit.receipt.read(audit.ROOT / source["source_bindings"]["B4x12"]["target"])
    common, idio = audit.actual_coefficients(target, candidate)
    assert common > 0 and idio > 0
