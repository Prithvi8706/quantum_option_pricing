"""Check finite diagnostic coverage without calling it continuous confirmation."""
from fractions import Fraction as F


def verify_finite(rows):
    if [(r['case'], r['q']) for r in rows] != [('D1', 1), ('D1', 2), ('D2', 1), ('D2', 2)]:
        raise ValueError('finite case/precision menu differs')
    count = 0
    for row in rows:
        expected = 2**(row['q']*(2 if row['case'] == 'D1' else 4))
        if type(row['paths']) is not int or row['paths'] != expected:
            raise ValueError('finite coverage mismatch')
        if row['overflow_safe'] is not True:
            raise ValueError('finite overflow guard failed')
        error = F(row['arithmetic_max_pointwise_error'])
        if not 0 <= error <= F(row['arithmetic_price_error_upper']):
            raise ValueError('diagnostic exceeds declared allowance')
        if abs(F(row['target_price'])-F(row['arithmetic_price'])) > error:
            raise ValueError('mean discrepancy exceeds maximum pointwise discrepancy')
        if [r['degree'] for r in row['reflection']] != [16, 32, 64, 128]:
            raise ValueError('reflection diagnostic menu differs')
        count += expected
    return {'grid_inputs': count, 'independent_trials': False, 'continuous_confirmation': False}
