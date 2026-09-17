from research.journal_sprint.analyze_week2 import corrected_cost


def test_explicit_iqft_swap_cost():
    row = dict(budget=dict(schedule=dict(repetitions=17,phase_qubits=9)),
               resources=dict(total_cx_projection=1000))
    assert corrected_cost(row)==(1204,204)
    row['budget']['schedule']['phase_qubits']=8
    assert corrected_cost(row)==(1204,204)
