import pytest

from research.journal_sprint.fixed_costs import fixed_allocation, schedule_cost


def profiles():
    return {
        k: {"gates": {"cx": cx, "u": 2 * cx}, "depth": 3 * cx, "total_qubits": 13}
        for k, cx in ((0, 280), (1, 13124), (2, 25968))
    }


def test_query_matching_does_not_match_gates():
    p = profiles()
    direct, multi = fixed_allocation(p, 294912, "A_equivalents")
    d, m = schedule_cost(p, [0], direct), schedule_cost(p, [0, 1, 2], multi)
    assert d["pricing_A_equivalents"] == m["pricing_A_equivalents"] == 294912
    assert m["pricing_logical_cx"] > 15 * d["pricing_logical_cx"]
    assert d["calibration_shots"] == m["calibration_shots"] == 8192


def test_cx_matching_respects_cap_and_records_shots():
    p = profiles()
    direct, multi = fixed_allocation(p, 294912, "logical_cx")
    d, m = schedule_cost(p, [0], direct), schedule_cost(p, [0, 1, 2], multi)
    slack = d["pricing_logical_cx"] - m["pricing_logical_cx"]
    assert 0 <= slack < sum(p[k]["gates"]["cx"] for k in p)
    assert m["total_shots"] == sum(multi) + 8192


@pytest.mark.parametrize("depths,shots", [([], []), ([0], [0]), ([True], [1]), ([0, 1], [1])])
def test_invalid_schedules(depths, shots):
    with pytest.raises(ValueError):
        schedule_cost(profiles(), depths, shots)


def test_missing_profile_rejected():
    with pytest.raises(ValueError, match="missing"):
        schedule_cost(profiles(), [3], [1])
