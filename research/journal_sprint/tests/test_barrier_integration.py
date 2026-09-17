from research.journal_sprint.verify_barrier_integration import nonuniform_check


def test_nonuniform_loader_endianness_and_hadamard():
    result = nonuniform_check([.2, -.3, .1])
    assert result["preparation_probability_error"] < 1e-12
    assert result["bit_reversed_probability_l1"] > .1
    assert result["discrepancy"] < 1e-10
