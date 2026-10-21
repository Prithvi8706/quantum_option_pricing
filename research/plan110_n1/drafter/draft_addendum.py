"""N2-drafter addendum: combine the N1 direction-select credit with the N1 departure results.

The three N1 workstreams each report one part of the picture:
  - headline: stacked departures (with W0's assumed C09 x2/x5 factors),
  - estimator: a new conditional direction-select credit (M 232 -> 200, 801 -> 401),
  - hwclassical: the Stage-C-quantified C09 factor (36.9 at the binding cell).
No N1 file multiplies them together. This script does only that arithmetic, at the
binding cell B8x52 $0.001, so the draft can state whether the combination crosses M = 1.
Every input is copied from an N1 file; every output is a product/ratio of copied values
(label: modelled, derived arithmetic; direction: quantum-favourable).

Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/drafter/draft_addendum.py
Writes (exclusive create): results/plan110_n1/drafter/addendum.json; appends rows.jsonl.
"""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
N1 = ROOT / 'results' / 'plan110_n1'
OUT = N1 / 'drafter' / 'addendum.json'
ROWS = N1 / 'drafter' / 'rows.jsonl'
INPUTS = {
    'headline_table': N1 / 'headline' / 'headline_table.json',
    'estimator': N1 / 'estimator' / 'estimator_recompute.json',
    'hw_v2': N1 / 'hwclassical' / 'hw_classical_card_v2.json',
}


def main():
    if OUT.exists():
        sys.exit(f'refusing to overwrite {OUT}')
    ht, es, hw = (json.loads(p.read_text(encoding='utf-8')) for p in INPUTS.values())
    p7 = [r for r in es['part7_M_primary'] if r['case'] == 'B8x52' and r['eps'] == 0.001][0]
    r_expl = p7['M_N1_explicit_best_dirsel'] / p7['M_W0_explicit_best']
    r_cert = p7['M_certified_today_dirsel'] / p7['M_certified_today']
    sd = ht['stacked_departures']
    pair_expl = {tuple(s['departures']): s['min_M'] for s in sd['explicit_best']['best_pairs']}
    pair_cert = {tuple(s['departures']): s['min_M'] for s in sd['certified']['best_pairs']}
    df = {(r['design'], r['k_class']): r['M_distfree'] for r in hw['classical']['M_distfree']
          if r['case'] == 'B8x52' and r['eps'] == 0.001}
    c = ht['cells']
    b8 = [x for x in c if x['case'] == 'B8x52' and x['eps'] == 0.001][0]
    out = {
        'meta': {'script': 'research/plan110_n1/drafter/draft_addendum.py', 'python': sys.version,
                 'flags': {'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site},
                 'inputs_sha256': {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in INPUTS.items()},
                 'cell': 'B8x52 $0.001 (binding cell)',
                 'label': 'modelled, derived arithmetic on N1 values (not an N1 result)',
                 'direction': 'quantum-favourable'},
        'dirsel_ratio_explicit': r_expl,
        'dirsel_ratio_certified': r_cert,
        'explicit_dirsel': {
            'primary': p7['M_N1_explicit_best_dirsel'],
            'all_free': b8['M']['explicit_best']['all_free_oracle'] * r_expl,
            'one_lane_one_core': b8['M']['explicit_best']['one_lane_one_core'] * r_expl,
            'all_free+one_lane_one_core': pair_expl[('all_free', 'one_lane_one_core')] * r_expl,
            'distfree_stageC': df[('box_muller_current_law', 'explicit_best')] * r_expl,
            'all_free+distfree_stageC': df[('all_free_and_narrow', 'explicit_best')] * r_expl,
        },
        'certified_dirsel': {
            'primary': p7['M_certified_today_dirsel'],
            'all_free+one_lane_one_core': pair_cert[('all_free', 'one_lane_one_core')] * r_cert,
            'distfree_stageC': df[('box_muller_current_law', 'certified_today')] * r_cert,
            'all_free+distfree_stageC': df[('all_free_and_narrow', 'certified_today')] * r_cert,
        },
        'caveat': ('direction-select call cost is assumed equal to one controlled Grover iterate '
                   '(estimator card 2b); the 1-lane and distribution-free columns are applied as '
                   'multiplicative T_C factors exactly as in the N1 files; the cross-products of '
                   'the H16 ratio with the Stage-C C09 factor were not formed because the C09 '
                   'factor was measured at 16 workers'),
    }
    with OUT.open('x', encoding='utf-8') as f:
        json.dump(out, f, indent=1, sort_keys=True)
    with ROWS.open('a', encoding='utf-8') as f:
        for grp in ('explicit_dirsel', 'certified_dirsel'):
            f.write(json.dumps({'ws': 'n2_drafter', 'sub': 'addendum_' + grp, 'value': out[grp],
                                'label': out['meta']['label'], 'direction': 'quantum-favourable',
                                'source': 'results/plan110_n1/drafter/addendum.json',
                                'note': out['caveat']}, sort_keys=True) + '\n')
    print(json.dumps({k: out[k] for k in ('dirsel_ratio_explicit', 'dirsel_ratio_certified',
                                           'explicit_dirsel', 'certified_dirsel')}, indent=1))


if __name__ == '__main__':
    main()
