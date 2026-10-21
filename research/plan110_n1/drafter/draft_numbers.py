"""N2-drafter number extraction and consistency check (plan110 branch N).

Reads only the N1 result files and pulls out every number the draft
manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md quotes,
with a few arithmetic identities checked (M = k / k_10x, the 75 x 3.1 split, the
distribution-free products). It computes nothing new that enters a decision: every
value is copied from an N1 JSON file or is a product/ratio of copied values, and is
labelled as such.

Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/drafter/draft_numbers.py
Writes (exclusive create): results/plan110_n1/drafter/draft_numbers.json
Appends: results/plan110_n1/drafter/rows.jsonl
"""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
N1 = ROOT / 'results' / 'plan110_n1'
OUT = N1 / 'drafter' / 'draft_numbers.json'
ROWS = N1 / 'drafter' / 'rows.jsonl'

INPUTS = {
    'headline_table': N1 / 'headline' / 'headline_table.json',
    'keff': N1 / 'headline' / 'keff.json',
    'floor_sheet': N1 / 'headline' / 'floor_sheet.json',
    'estimator': N1 / 'estimator' / 'estimator_recompute.json',
    'hw_v2': N1 / 'hwclassical' / 'hw_classical_card_v2.json',
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name):
    return json.loads(INPUTS[name].read_text(encoding='utf-8'))


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def row(sub, value, label, direction, source, note=''):
    r = {'ws': 'n2_drafter', 'sub': sub, 'value': value, 'label': label,
         'direction': direction, 'source': source}
    if note:
        r['note'] = note
    with ROWS.open('a', encoding='utf-8') as f:
        f.write(json.dumps(r, sort_keys=True) + '\n')
    return r


def main():
    if OUT.exists():
        sys.exit(f'refusing to overwrite {OUT}')
    ht, kf, fs, es, hw = (load(n) for n in INPUTS)
    out = {'meta': {'script': 'research/plan110_n1/drafter/draft_numbers.py',
                    'python': sys.version,
                    'flags': {'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site,
                              'dont_write_bytecode': sys.flags.dont_write_bytecode},
                    'inputs_sha256': {k: sha(p) for k, p in INPUTS.items()},
                    'labels': 'all values copied from N1 results or products/ratios of them; labels and directions as in the source files'}}
    checks = []

    # --- headline: binding cell and the B4x12 $0.001 cell
    cells = {(c['case'], c['eps']): c for c in ht['cells']}
    b8 = cells[('B8x52', 0.001)]
    b4 = cells[('B4x12', 0.001)]
    t_layer = 1e-7
    for name, c in (('B8x52_0.001', b8), ('B4x12_0.001', b4)):
        d_used = c['D_eff_primary']['used']
        d_max_k1 = c['T_C'] / (10 * c['sigma_over_e'] * t_layer)
        k10 = d_max_k1 / d_used
        m_expl = c['k']['explicit_best'] / k10
        checks.append({'check': f'{name} M_explicit = k/k_10x', 'recomputed': m_expl,
                       'file': c['M']['explicit_best']['primary'],
                       'rel_err': rel(m_expl, c['M']['explicit_best']['primary'])})
        out[name] = {'T_C_s': c['T_C'], 'sigma_over_e': c['sigma_over_e'],
                     'h16_ratio': c['h16_ratio'], 'D_eff': c['D_eff_primary'],
                     'D_max_k1_layers': d_max_k1, 'k_10x': k10, 'k': c['k'],
                     'M_primary': {k: v['primary'] for k, v in c['M'].items()},
                     'M_N1_floor_only_primary': c['M_N1_floor_only_primary']}
    out['min_M_summary'] = ht['summary_min_M_eligible_non_overhead']
    out['stacked_departures'] = ht['stacked_departures']
    out['h16_one_core_ratio'] = ht['h16_one_core_ratio']

    # --- E07 reproduction
    out['e07_reproduction'] = kf['reproduction_eps0.01']
    kc = [c['k_eff'] for c in kf['cells'] if c['split'] == '0.45eps']
    out['certified_k_range_0.45eps'] = [min(kc), max(kc)]

    # --- floor sheet
    fsum = {}
    for case in ('B4x12', 'B8x52'):
        p = fs['cases'][case]['primary_n72']
        bm = p['stages']['2_box_muller']['d']
        ent = {'compute_depth': p['compute_depth'], 'compute_T': p['compute_T'],
               'box_muller_depth': bm, 'box_muller_share_of_compute_path': bm / p['compute_depth'],
               'persistent_outputs': p['persistent_outputs']}
        for w in ('W1e7', 'unlimited'):
            e = p['by_width'][w]['1e12|100ns']
            ent[w + '_1e12_100ns'] = {k: e[k] for k in ('depth', 'T', 'D_eff', 'binding', 'width')}
        ent['all_free_compute_depth'] = fs['cases'][case]['all_free_n48_f32']['compute_depth']
        fsum[case] = ent
    out['floor_sheet_summary'] = fsum

    # --- estimator
    p7 = [r for r in es['part7_M_primary'] if r['case'] == 'B8x52' and r['eps'] == 0.001][0]
    out['estimator_B8x52_0.001_M'] = p7
    lb = es['part3_counting_lower_bound']
    sup = [r for r in lb if r['class'].startswith('support') and r['delta'] == 0.01]
    out['counting_bound_support_delta0.01'] = {
        case: [min(r['k_LB_Q_plus_one_A'] for r in sup if r['case'] == case),
               max(r['k_LB_Q_access'] for r in sup if r['case'] == case)]
        for case in ('B4x12', 'B8x52')}
    out['lanes_W1e7'] = es['part6_lanes_W1e7']['rows']
    out['patel_thm2_offset_k'] = [r['k'] for r in es['part5_patel_thm2_randomised_offset']['rows']]
    checks.append({'check': 'estimator M_W0_explicit_best == headline explicit primary (B8x52 0.001)',
                   'rel_err': rel(p7['M_W0_explicit_best'], b8['M']['explicit_best']['primary'])})

    # --- hardware / classical
    nc = [r for r in hw['necessary_conditions'] if r['case'] == 'B8x52' and r['eps'] == 0.001]
    out['hw_binding_cell_necessary'] = [
        {k: r.get(k) for k in ('k_class', 'k', 'floor_design', 'floor_layers', 't_layer_required_s',
                               't_layer_required_over_100ns', 'T_per_s_required',
                               'T_per_s_required_over_budget', 'logical_width')} for r in nc]
    md = hw['classical']['M_distfree']
    b8df = [r for r in md if r['case'] == 'B8x52' and r['eps'] == 0.001]
    out['hw_M_distfree_B8x52_0.001'] = b8df
    fac = [r['factor_df'] for r in b8df][0]
    # identity: M_distfree = M_practice / factor
    for r in b8df:
        checks.append({'check': f"distfree M = M_practice/factor ({r['design']}, {r['k_class']})",
                       'rel_err': rel(r['M_distfree'], r['M_practice'] / r['factor_df'])})
    # 232 = (100 ns / t_req) x (D_eff / Box-Muller floor)
    bm_expl = [r for r in nc if r['k_class'] == 'explicit_best' and r['floor_design'] == 'box_muller_current_law'][0]
    lay = 1 / bm_expl['t_layer_required_over_100ns']
    supf = b8['D_eff_primary']['used'] / bm_expl['floor_layers']
    out['M232_split'] = {'layer_time_factor': lay, 'supply_factor': supf, 'product': lay * supf}
    checks.append({'check': '232 = layer factor x supply factor',
                   'rel_err': rel(lay * supf, b8['M']['explicit_best']['primary'])})
    out['hw_self_check_max_rel_err'] = hw['self_check_max_rel_err']

    out['checks'] = checks
    worst = max(c['rel_err'] for c in checks)
    out['max_rel_err'] = worst
    with OUT.open('x', encoding='utf-8') as f:
        json.dump(out, f, indent=1, sort_keys=True)

    src_h = 'results/plan110_n1/headline/headline_table.json'
    row('binding_cell_k10x', out['B8x52_0.001']['k_10x'], 'modelled (T_C measured, D_eff modelled)', 'neutral', src_h)
    row('binding_cell_D_max_k1', out['B8x52_0.001']['D_max_k1_layers'], 'modelled (T_C measured)', 'neutral', src_h)
    row('M_primary_min', {k: v['primary'] for k, v in out['min_M_summary'].items()}, 'modelled', 'neutral', src_h)
    row('stacked_departures_explicit', out['stacked_departures']['explicit_best']['min_departures_to_M_le_1'],
        'modelled', 'neutral', src_h, 'uses assumed C09 x2/x5; see hw distfree for the Stage-C factor')
    row('floor_sheet_summary', fsum, 'modelled', 'quantum-favourable (idealized)', 'results/plan110_n1/headline/floor_sheet.json')
    row('M232_split', out['M232_split'], 'modelled', 'neutral', 'results/plan110_n1/hwclassical/hw_classical_card_v2.json')
    row('distfree_factor_binding_cell', fac, 'modelled from measured inputs', 'quantum-favourable column (slows classical)',
        'results/plan110_n1/hwclassical/hw_classical_card_v2.json')
    row('consistency_checks', {'n': len(checks), 'max_rel_err': worst}, 'arithmetic check', 'neutral', str(OUT.relative_to(ROOT)))
    print(json.dumps({'max_rel_err': worst, 'n_checks': len(checks),
                      'k10x': out['B8x52_0.001']['k_10x'], 'Dmax': out['B8x52_0.001']['D_max_k1_layers'],
                      'split': out['M232_split'], 'factor': fac,
                      'certified_k_range': out['certified_k_range_0.45eps'],
                      'lb': out['counting_bound_support_delta0.01'],
                      'distfree': [(r['design'], r['k_class'], round(r['M_distfree'], 3)) for r in b8df],
                      'necessary': [(r['k_class'], r['floor_design'], r['t_layer_required_s'], r['T_per_s_required']) for r in out['hw_binding_cell_necessary']],
                      'floor': fsum}, indent=1, default=str))


if __name__ == '__main__':
    main()
