import copy

import pytest

from research.journal_sprint.fixed_costs import fixed_allocation, schedule_cost
from research.journal_sprint.run_fixed_discovery import COST_FIELDS, designs_for, summarize_cell


def fixture_inputs():
    profiles = {
        k: {"gates": {"cx": cx, "u": cx * 2}, "depth": cx * 3, "total_qubits": 13}
        for k, cx in ((0, 280), (1, 13124), (2, 25968))
    }
    ledger = []
    for axis in ("A_equivalents", "logical_cx"):
        direct, multi = fixed_allocation(profiles, 294912, axis)
        ledger.append(
            {
                "contract": "E001",
                "n": 6,
                "scale": 0.125,
                "reference_A_budget": 294912,
                "axis": axis,
                "direct_shots": direct,
                "multi_shots": multi,
                "direct": schedule_cost(profiles, [0], direct),
                "multi": schedule_cost(profiles, [0, 1, 2], multi),
            }
        )
    return ledger, profiles


def test_exactly_three_designs_not_duplicate_direct():
    ledger, profiles = fixture_inputs()
    result = designs_for("E001", 294912, ledger, profiles)
    assert set(result) == {"direct", "A_matched", "CX_capped"}
    assert result["A_matched"]["shots"] == [32768] * 3
    assert result["CX_capped"]["shots"] == [2097] * 3


@pytest.mark.parametrize("defect", ["allocation", "cost", "duplicate"])
def test_tampered_ledger_rejected(defect):
    ledger, profiles = fixture_inputs()
    if defect == "allocation":
        ledger[0]["multi_shots"][0] += 1
    elif defect == "cost":
        ledger[0]["direct"]["calibration_shots"] = 0
    else:
        ledger[1] = copy.deepcopy(ledger[0])
    with pytest.raises(ValueError):
        designs_for("E001", 294912, ledger, profiles)


def test_all_refusals_keep_denominator_and_undefined_conditional_rate():
    row = {"status": "pre_refusal", "cost": {k: 0 for k in COST_FIELDS}}
    summary = summarize_cell([row] * 100)
    assert summary["attempts"] == 100
    assert summary["executed"] == summary["declared"] == 0
    assert summary["false_per_attempt"] == 0
    assert summary["false_per_executed"] is None
    assert summary["false_given_declaration"] is None


def test_summary_does_not_sum_depth_or_qubits_as_acquisition_costs():
    ledger, _ = fixture_inputs()
    row = {"status": "unresolved", "radius": 2.0, "cost": ledger[0]["direct"]}
    summary = summarize_cell([row, row])
    assert "max_qubits" not in summary["acquisition_totals"]
    assert summary["acquisition_totals"]["calibration_shots"] == 16384
