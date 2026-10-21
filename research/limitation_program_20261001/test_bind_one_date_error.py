"""Exact source-claim join guards; all fixture radii are synthetic."""

import copy

import pytest

from research.limitation_program_20261001 import bind_one_date_error as bridge


def fixture():
    normals = [1, 2, 3, 4, 5, 6]
    scope = {"case": "B4x12", "date": 1}
    eta = dict(
        kind="basket-absolute-error",
        upper_exact=[1, 10000],
        scope=scope,
        coupling_id=bridge.COUPLING_ID,
        measure=bridge.MEASURE,
        proved=True,
        native_exp_and_clipping_included=True,
        event="First three radial uniforms are at least delta",
    )
    bad = dict(
        kind="bad-event-probability",
        upper_exact=[3, 1 << 20],
        scope=scope,
        coupling_id=bridge.COUPLING_ID,
        measure=bridge.MEASURE,
        proved=True,
    )
    date = dict(
        date=1,
        observation_time_exact=[1, 12],
        assets=4,
        Gaussian_pairs_used=3,
        clipping_inactive_on_good_event=True,
        exp_final_shift_signed_overflow_excluded=True,
        unchanged_exp_templates_certified_by_independent_E03_audit=True,
        first_asset_template_bound_applies_to_all_four_assets=True,
        all_four_asset_date1_scopes=[dict(asset=i, normal_values=[1, i + 2]) for i in range(4)],
        basket_discrepancy_dollars_exact=[1, 10000],
    )
    return dict(
        uniform_bits=32,
        fraction_bits=40,
        native_width=72,
        claims={bridge.ETA_CLAIM: eta, bridge.BAD_CLAIM: bad},
        source_bindings={"B4x12": dict(normal_values=normals, pair_count=30, scalar_count=60)},
        candidates=[
            dict(
                cutoff_bits=20,
                delta_exact=[1, 1 << 20],
                coupling_id=bridge.COUPLING_ID,
                B4_date1=date,
                tail_probability_union_upper_exact={"B4_all30_pairs": [30, 1 << 20]},
                tail_payoff_difference_dollars_upper_exact={
                    "B4_all30_pairs_bad_event_only": [1200, 1 << 20]
                },
            )
        ],
    )


def test_same_domain_and_joint_pairs_join_exactly():
    _, eta, bad = bridge.validate_selected(fixture())
    assert eta["upper_exact"] == [1, 10000]
    assert bad["upper_exact"] == [3, 1 << 20]


@pytest.mark.parametrize(
    "change",
    [
        "cutoff",
        "coupling",
        "wrong_date",
        "bad_as_full_tail",
        "raw_log_as_stock_ratio",
        "missing_clipping",
        "wrong_normal",
        "independent_scalars",
        "changed_eta",
        "missing_asset",
        "wrong_measure",
    ],
)
def test_mismatched_contracts_are_rejected(change):
    source = copy.deepcopy(fixture())
    row, eta, bad = (
        source["candidates"][0],
        source["claims"][bridge.ETA_CLAIM],
        source["claims"][bridge.BAD_CLAIM],
    )
    if change == "cutoff":
        row["delta_exact"] = [1, 1 << 24]
    elif change == "coupling":
        bad["coupling_id"] = "different-coupling"
    elif change == "wrong_date":
        eta["scope"] = {"case": "B4x12", "date": 2}
    elif change == "bad_as_full_tail":
        bad["upper_exact"] = [30, 1 << 20]
    elif change == "raw_log_as_stock_ratio":
        eta["kind"] = "all-stocks-log-relative-error"
    elif change == "missing_clipping":
        eta["native_exp_and_clipping_included"] = False
    elif change == "wrong_normal":
        row["B4_date1"]["all_four_asset_date1_scopes"][0]["normal_values"] = [2, 3]
    elif change == "independent_scalars":
        source["source_bindings"]["B4x12"]["pair_count"] = 60
    elif change == "changed_eta":
        eta["upper_exact"] = [1, 1000]
    elif change == "missing_asset":
        row["B4_date1"]["all_four_asset_date1_scopes"].pop()
    elif change == "wrong_measure":
        eta["measure"] = "finite-digital-Gaussian-independent"
    with pytest.raises(ValueError):
        bridge.validate_selected(source)
