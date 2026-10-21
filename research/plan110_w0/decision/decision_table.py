"""plan110 W0 decision table (R0 screen): M = k_achievable / k_10x per cell and convention.

M <= 1 means a tenfold win is reached under that convention; GO needs M <= 1 in an eligible
non-overhead cell, GREY 1 < M <= 3, NO-GO M > 3 (PLAN_110_EFFICIENT.md section 4).
k_10x comes from the WS-floor idealized floor (results/plan110_w0/ws_floor/floor.json headline);
k_achievable comes from WS-k (results/plan110_w0/ws_k/k_bracket.json part3_k_lo_methods).
Stdlib only; run with .context/frontier_t0_env/Scripts/python.exe -I -S -B from the repo root.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
FLOOR = ROOT / 'results/plan110_w0/ws_floor/floor.json'
KB = ROOT / 'results/plan110_w0/ws_k/k_bracket.json'
H16 = ROOT / 'results/plan110_w0/ws_small/h16_grid'
OUT = ROOT / 'results/plan110_w0/decision' / (sys.argv[1] if len(sys.argv) > 1 else 'run001')

OVERHEAD = {('B8x52', 0.1), ('B4x12', 0.1), ('B8x52', 0.03), ('B4x12', 0.03)}  # small-n or envelope T_C
C09_FACTORS = (2.0, 5.0)  # distribution-free classical coverage, C09 triage row range (modelled)
SUPPLIES = ('supply_1e11', 'supply_1e12', 'supply_1e13', 'unlimited_supply')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def k_classes(kb):
    """Per (case, eps, split): certified-today k, best explicit-constant k, best no-explicit-constant k."""
    out = {}
    for row in kb['part3_k_lo_methods']:
        key = (row['case'], row['eps'], row['split'])
        slot = out.setdefault(key, {})
        status = row['constant_status']
        if status == 'explicit (certified schedule)':
            slot['certified_today'] = min(slot.get('certified_today', float('inf')), row['k_total'])
        elif status.startswith('explicit'):
            if row['k_total'] < slot.get('explicit_best', (float('inf'), ''))[0]:
                slot['explicit_best'] = (row['k_total'], row['method'])
        else:
            if row['k_total'] < slot.get('no_explicit_constant', (float('inf'), ''))[0]:
                slot['no_explicit_constant'] = (row['k_total'], row['method'])
    return out


def h16_ratio():
    """T_C(1 worker) / T_C(16 workers) per (case, eps) from the H16 grid, if it has run."""
    ratios = {}
    for path in sorted(H16.glob('*/**/*.json')) if H16.exists() else []:
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (ValueError, UnicodeDecodeError):
            continue
        rows = data if isinstance(data, list) else data.get('rows', [data])
        for r in rows:
            if isinstance(r, dict) and {'case', 'eps', 'workers', 't_c'} <= set(r):
                ratios.setdefault((r['case'], float(r['eps'])), {})[int(r['workers'])] = float(r['t_c'])
    return {k: v[1] / v[16] for k, v in ratios.items() if 1 in v and 16 in v}


def main():
    floor = json.loads(FLOOR.read_text(encoding='utf-8'))
    kb = json.loads(KB.read_text(encoding='utf-8'))
    kc = k_classes(kb)
    one_core = h16_ratio()
    rows = []
    for case, by_w in floor['headline'].items():
        for width, by_design in by_w.items():
            for design, rec in by_design.items():
                for comp in rec.get('comparison', []):
                    eps = float(comp['eps'])
                    for tl, by_sigma in comp['by_t_layer'].items():
                        for sigma, ks in by_sigma.items():
                            if sigma not in ('base', 'e_eq_eps'):
                                continue  # F20 sigma credit needs a sigma-normalised estimator; bounded AE does not gain
                            split = '0.45eps' if sigma == 'base' else 'eps'
                            classes = kc.get((case, eps, split)) or kc.get((case, eps, '0.45eps'))
                            if not classes:
                                continue
                            for supply in SUPPLIES:
                                k10 = ks[f'k_10x_{supply}']
                                for kname in ('certified_today', 'explicit_best', 'no_explicit_constant'):
                                    kv = classes.get(kname)
                                    if kv is None:
                                        continue
                                    k = kv[0] if isinstance(kv, tuple) else kv
                                    row = dict(case=case, eps=eps, width=width, design=design, t_layer=tl,
                                               sigma=sigma, supply=supply, k_class=kname, k=k, k_10x=k10,
                                               M_practice_16core=k / k10,
                                               M_distfree_x2=k / (k10 * C09_FACTORS[0]),
                                               M_distfree_x5=k / (k10 * C09_FACTORS[1]),
                                               overhead_T_C=(case, eps) in OVERHEAD, T_C=comp['T_C'],
                                               T_C_conv=comp['T_C_conv'])
                                    r1 = one_core.get((case, eps))
                                    row['M_1lane_1core'] = k / (k10 * r1) if r1 else None
                                    row['one_core_ratio'] = r1
                                    rows.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    primary = [r for r in rows if r['width'] == 'W1e7' and r['design'] == 'box_muller_current_law'
               and r['t_layer'] == '100ns' and r['sigma'] == 'base' and r['supply'] == 'supply_1e12']
    summary = {
        'inputs_sha256': {str(p.relative_to(ROOT)): sha(p) for p in (FLOOR, KB)},
        'h16_one_core_ratios': {f'{c}|{e}': v for (c, e), v in one_core.items()},
        'primary_convention': 'W=1e7, Box-Muller current law, 100 ns, e=0.45eps, 1e12 T/s, practice CI, 16-core classical',
        'primary_rows': sorted(primary, key=lambda r: (r['k_class'], r['M_practice_16core'])),
        'min_M_primary_eligible_non_overhead': {
            kname: min((r['M_practice_16core'] for r in primary if r['k_class'] == kname and not r['overhead_T_C']),
                       default=None)
            for kname in ('certified_today', 'explicit_best', 'no_explicit_constant')},
        'min_M_any_convention_explicit_constants': min(
            (min(x for x in (r['M_practice_16core'], r['M_distfree_x5'], r['M_1lane_1core']) if x is not None)
             for r in rows if r['k_class'] != 'no_explicit_constant' and not r['overhead_T_C']), default=None),
        'labels': 'All values modelled (R0 screen); k classes from WS-k, k_10x from WS-floor; C09 factors modelled range',
    }
    for name, data in (('decision_rows.json', rows), ('decision_summary.json', summary)):
        target = OUT / name
        with target.open('x', encoding='utf-8') as f:
            json.dump(data, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in summary.items() if k != 'primary_rows'}, indent=1))
    for r in summary['primary_rows']:
        print(f"{r['k_class']:22s} {r['case']} eps={r['eps']:<6} k={r['k']:8.1f} k10x={r['k_10x']:7.3f} "
              f"M={r['M_practice_16core']:9.2f} distfree5={r['M_distfree_x5']:8.2f} overhead={r['overhead_T_C']}")


if __name__ == '__main__':
    sys.exit(main())
