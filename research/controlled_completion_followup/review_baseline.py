"""Independent focused checks of the pre-followup controlled-source candidate.

Writes only this review's own JSON; never refreshes the source experiment.
"""
from fractions import Fraction
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.stats import binom

from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.modern_mean import (
    controller, exact_qpe_test_probability, plan,
)
from research.controlled_source_completion.phase_certificate import (
    atan_bounds, exact_coefficient,
)


ROOT = Path('results/controlled_source_completion')


def main():
    phase = json.loads((ROOT / 'compile_v2/phase_f64/target.json').read_text())
    checked = 0
    for i, row in enumerate(phase['tables']['atan']):
        c = Fraction(2 * i + 1, 64)
        lo, hi = atan_bounds(c)
        assert round(lo * 2**64) == round(hi * 2**64) == row[0]
        checked += 1
        for n in range(1, 9):
            assert round(exact_coefficient(c, n) * 2**64) == row[n]
            checked += 1

    mp.mp.dps = 85
    h = mp.mpf(1)/64
    phase_bound = mp.mpf(32) / 2**64 + 2*h**9/(9*(1-h)) + mp.mpf('2e-16')
    # Segment endpoints, the reciprocal branch boundary, signs, actual normalizers,
    # and the maximum certified |Y-left|. Raw integer offsets include one ulp.
    pairs = set()
    for exponent in (4, 5, 6, 12):
        scale = 1 << exponent
        for numerator in range(-32, 33):
            for offset in (-1, 0, 1):
                y = numerator * scale * 2**64 // 32 + offset
                if abs(y) <= 100 * 2**64:
                    pairs.add((y, 0, exponent))
        for y in (-100, -1, 0, 1, 100):
            for left in (-100, -1, 0, 1, 100):
                pairs.add((y*2**64, left*2**64, exponent))
    worst = mp.mpf(0)
    worst_input = None
    for y, left, exponent in sorted(pairs):
        _, trace = evaluate(phase, dict(Y=y, left=left, scale_exponent=exponent), True)
        actual = trace[phase['outputs']['angle']]
        if actual >= 2**95:
            actual -= 2**96
        expected = -2*mp.atan(mp.mpf(y-left)/2**(64+exponent))
        error = abs(mp.mpf(actual)/2**64-expected)
        if error > worst:
            worst, worst_input = error, [y, left, exponent]
        assert error <= phase_bound, (y, left, exponent, error)

    # Construct non-Gaussian laws with rare, arbitrarily large normalized values.
    # The theorem assumes RMS, not a per-value bound.
    rng = np.random.default_rng(2026092217)
    eps = .02
    m = 2**15
    spectral = []
    for rare in (1e-8, 1e-5, .01, .1):
        p = np.array([rare, .2, .8-rare])
        for mean in (-eps, -eps/2, 0., eps/2, eps):
            for _ in range(3):
                values = rng.normal(size=3)
                values[0] /= math.sqrt(rare)
                values -= values @ p
                values *= math.sqrt((1/16)**2-mean**2) / math.sqrt((values*values) @ p)
                values += mean
                large = exact_qpe_test_probability(values, p, m, 1.42*eps)
                success = large if abs(mean) >= eps else 1-large
                assert success >= 2/3-1e-9, (values, p, mean, success)
                spectral.append(success)

    ledgers = json.loads((ROOT / 'cost_v3_phase64/ledger.json').read_text())
    count_rows = []
    for row in ledgers:
        schedule = json.loads((ROOT / 'cost_v3_phase64' / (
            '%s_f%d_%s_schedule.json' % (row['model'], row['f'], row['mode']))).read_text())
        calls = sum(s['repetitions']*(2**s['qpe_bits']-1) for s in schedule['stages'])
        union = sum(float(binom.sf(s['repetitions']//2, s['repetitions'], 1/3))
                    for s in schedule['stages'])
        assert calls == row['ledger']['controlled_U_calls']
        assert union <= .003
        assert 2*calls*float(phase_bound) <= .0005
        count_rows.append(dict(model=row['model'], fraction=row['f'], mode=row['mode'],
                               calls=calls, majority_union=union))

    allocation = plan(.25, .002, .003)
    max_controller_error = 0.
    for mean in np.linspace(-.5, .5, 1001):
        def measurements(stage, raw):
            left = raw/2**allocation['endpoint_bits']
            theta = -2*math.atan((mean-left)/stage['normalizer'])
            k = round((theta % (2*math.pi))*stage['M']/(2*math.pi)) % stage['M']
            return [k]*stage['repetitions']
        outcome = controller(allocation, measurements)
        error = abs(outcome['estimate']-mean)
        max_controller_error = max(error, max_controller_error)
        assert error <= .002

    result = dict(stored_coefficients_exactly_checked=checked,
                  phase_boundary_cases=len(pairs), maximum_phase_error=str(worst),
                  worst_phase_input=worst_input, conservative_phase_bound=str(phase_bound),
                  heavy_tail_spectral_cases=len(spectral), minimum_spectral_success=min(spectral),
                  audited_schedule_rows=count_rows, deterministic_controller_cases=1001,
                  maximum_controller_error=max_controller_error,
                  limitations='Independent focused checks; not a continuous financial bridge, '
                              'global financial arithmetic certificate, or hardware demonstration.')
    target = Path('results/controlled_completion_followup/review_baseline.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
