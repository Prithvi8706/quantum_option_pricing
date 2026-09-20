"""Independent integer CX ledger checks, including IQFT swaps and inverses."""


def count(value):
    if type(value) is not int or value < 0:
        raise ValueError('nonnegative integer count required')
    return value


def total(resources, schedule, cancelled=False):
    size, runs, bits = (count(schedule[k]) for k in ('M', 'repetitions', 'phase_qubits'))
    if size < 2 or size & (size-1) or bits != size.bit_length()-1 or runs < 1:
        raise ValueError('invalid AE size or repetition count')
    a = count(resources['a_cx_projection'])
    ca = a if cancelled else count(resources['controlled_a_cx_projection'])
    zero = count(resources['zero_reflection_cx_projection'])
    return runs*(a+(size-1)*(2*ca+zero+1)+bits*(bits-1)+3*(bits//2))


def verify_ledger(row):
    resources, schedule = row['resources'], row['budget']['schedule']
    for key, cancelled in [('total_cx_projection', False),
                           ('control_cancelled_total_cx_projection', True)]:
        expected = total(resources, schedule, cancelled) if schedule['status'] == 'ideal_plan' else None
        if resources[key] != expected:
            raise ValueError('CX ledger mismatch: '+key)
    return True
