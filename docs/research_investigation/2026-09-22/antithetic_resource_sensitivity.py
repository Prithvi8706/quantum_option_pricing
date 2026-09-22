"""Sensitivity coordinate from saved pilot variances, not a resource estimate.

Reads existing pilot outputs without rerunning or overwriting them. Illustrative
oracle weights omit fixed costs, and estimator constants remain unknown.
"""
from pathlib import Path
import hashlib
import json
import math


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    folder = Path(__file__).resolve().parent
    correction_path = folder/'antithetic_logheston_pilot.json'
    base_path = folder/'antithetic_logheston_level0.json'
    correction = json.loads(correction_path.read_text(encoding='utf-8'))
    base = json.loads(base_path.read_text(encoding='utf-8'))
    epsilon = 0.01
    epsilon_stat = 0.45*epsilon
    minimum_speedup = 10.
    classical_seconds = [0.1, 1., 10.]
    estimator_constants = [1., 10., 100.]
    cases = []
    for assets in (1, 4):
        base_summary = next(x for x in base['summaries'] if x['assets']==assets)
        entries = [dict(level=0, variance=base_summary['variance'], weight=1.)]
        entries += [dict(level=x['level'], variance=x['antithetic']['variance'],
                         weight=2.5*2**x['level'])
                    for x in correction['summaries'] if x['assets']==assets]
        entries.sort(key=lambda x: x['level'])
        for row in entries:
            row['sigma'] = math.sqrt(row['variance'])
            row['weight_times_sigma'] = row['weight']*row['sigma']
            row['sqrt_weight_times_sigma'] = math.sqrt(row['weight_times_sigma'])
        root_sum = math.fsum(x['sqrt_weight_times_sigma'] for x in entries)
        coefficient = root_sum**2
        base_only_coefficient = entries[0]['weight_times_sigma']
        for row in entries:
            row['formal_additive_error_allocation'] = epsilon_stat*row['sqrt_weight_times_sigma']/root_sum
        thresholds = [dict(classical_total_seconds=tc, unknown_estimator_constant=k,
                           maximum_c0_seconds=tc*epsilon_stat/(minimum_speedup*k*coefficient),
                           maximum_c0_microseconds=tc*epsilon_stat/(minimum_speedup*k*coefficient)*1e6)
                      for tc in classical_seconds for k in estimator_constants]
        cases.append(dict(assets=assets, levels=entries,
                          sum_sqrt_weight_times_sigma=root_sum,
                          B=coefficient, base_only_B=base_only_coefficient,
                          base_share_of_root_sum=entries[0]['sqrt_weight_times_sigma']/root_sum,
                          thresholds=thresholds))
    result = dict(status='Illustrative sensitivity coordinate; not a lower bound, compiled resource estimate, or feasibility result',
        inputs={str(p.name):dict(sha256=sha256(p)) for p in (correction_path, base_path)},
        epsilon=epsilon, epsilon_stat=epsilon_stat, minimum_speedup=minimum_speedup,
        coherent_weights='w0=1; wl=2.5*2^l for l>=1; two fine paths plus one coarse divided by base step count',
        assumed_model='Tq = k*c0*B/epsilon_stat; B=(sum_l sqrt(w_l*sqrt(V_l)))^2; additive per-level statistical error allocation',
        c0_units='seconds per illustrative level-zero coherent oracle; w_l and k dimensionless',
        caveats=[
            'Uses empirical sample variances; no certified variance bounds or remaining-bias proof.',
            'Weights are an uncompiled arithmetic step-count model ignoring fixed overhead and reversibility details.',
            'Unknown k stands in for estimator constants, logarithmic factors, repetitions, and confidence allocation; k=1 is not guaranteed.',
            'No loading, phase, quantile, truncation, precision, or query-floor cost is separately included.',
            'No classical controls or quantum controls are included; changing controls changes every variance.',
            'Only levels 0..5 are included, with no justified terminal level or bias certificate.',
            'Classical total runtimes are illustrative coordinates, not measured strong-comparator price delivery times.',
            'No fixed setup, measurement, decoding, or physical failure budget is charged; any such costs reduce available c0.',
            'This conditional algebra is neither a lower bound nor evidence of feasible quantum advantage.'],
        cases=cases, source_sha256=sha256(Path(__file__)))
    output = folder/'antithetic_resource_sensitivity.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    lines = ['# Antithetic resource sensitivity coordinate', '',
        'Date: 2026-09-22. This calculation reads the preserved development pilot variances; it reruns no paths.', '',
        '**This is an uncompiled sensitivity model, not a lower bound, resource estimate, or feasibility result.**', '',
        'Let sigma_l=sqrt(V_l), where V_l is the observed antithetic correction variance, and include the independent level-zero payoff variance. Assume oracle costs c_l=c0*w_l with w0=1 and w_l=2.5*2^l for l>=1. The latter counts two fine paths plus one coarse path relative to a 12-step base path; it ignores fixed overhead and all differences in reversible implementation.', '',
        'If, illustratively, an estimator costs k*c_l*sigma_l/e_l to achieve additive statistical error e_l, minimizing the sum of those costs subject to sum(e_l)=epsilon_stat gives e_l proportional to sqrt(w_l*sigma_l), and', '',
        '```',
        'B = (sum_l sqrt(w_l*sqrt(V_l)))^2',
        'Tq = k*c0*B/epsilon_stat',
        'c0_allowed = Tc*epsilon_stat/(10*k*B).',
        '```', '',
        'This algebra assumes a particular additive error allocation; it does not establish that an implemented quantum estimator attains the model. Statistical error budget is 0.45*0.01=0.0045 price units. The remainder is reserved but has not been shown sufficient for bias or any other error. The chosen 10-fold latency criterion is a practical target, not statistical significance.', '',
        '| Case | Base V0 | Exact base sigma0 term in B expansion | Base sqrt(sigma0) term inside sum | Full B, levels 0--5 |',
        '|---|---:|---:|---:|---:|']
    for case in cases:
        row = case['levels'][0]
        lines.append(f"| A{case['assets']} | {row['variance']:.12g} | {row['weight_times_sigma']:.12g} | {row['sqrt_weight_times_sigma']:.12g} | {case['B']:.12g} |")
    lines += ['', 'The base contribution is included exactly as the saved sample estimate permits: w0*sigma0=sqrt(V0), plus its cross terms with the other levels after squaring the sum. Full precision values and all six per-level terms are retained in the JSON.', '',
        'Allowed c0 below is in **microseconds per illustrative base coherent oracle**, before any fixed overhead:', '',
        '| Classical total Tc (seconds) | k | A1 allowed c0 (microseconds) | A4 allowed c0 (microseconds) |',
        '|---:|---:|---:|---:|']
    for left, right in zip(cases[0]['thresholds'], cases[1]['thresholds']):
        lines.append(f"| {left['classical_total_seconds']:g} | {left['unknown_estimator_constant']:g} | {left['maximum_c0_microseconds']:.9g} | {right['maximum_c0_microseconds']:.9g} |")
    lines += ['', 'Caveats:', '']
    lines += ['- '+x for x in result['caveats']]
    lines += ['', 'The entries specify a budget to compare with a separately compiled and physically scheduled coherent oracle. They do not predict its duration. Level-zero classical diagnostic CPU timings cannot be substituted for c0. Strong classical methods receive the same controls and problem information.', '',
        'Reproduce with `python docs/research_investigation/2026-09-22/antithetic_resource_sensitivity.py`.', '',
        'Artifacts: [source](antithetic_resource_sensitivity.py), [full-precision JSON](antithetic_resource_sensitivity.json), [underlying pilot protocol/results](antithetic_logheston_pilot.md).', '']
    (folder/'antithetic_resource_sensitivity.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(dict(epsilon_stat=epsilon_stat, cases=[dict(assets=x['assets'], B=x['B'], base_only_B=x['base_only_B'], thresholds=x['thresholds']) for x in cases]), indent=2))


if __name__ == '__main__':
    run()
