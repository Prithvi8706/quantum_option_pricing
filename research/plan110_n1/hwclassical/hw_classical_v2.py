"""plan110 N1 hardware/classical card (R1 numbers for items H01/H02/C15/H17/H14/H04/H07/C09/C10/H16).
v2 (2026-10-12): uses the gap-ledger monotone envelope T_C_env (as WS-floor/decision do) instead of the raw T_C;
v1 failed its self-check (0.64) only in the eps=0.03 overhead cells for that reason. v1 output is kept, superseded.

Part 2: necessary-condition columns. For a tenfold win the quantum latency must satisfy
    k * (sigma/e) * F * t_layer <= T_C / 10,
so with the W0 floor F (reaction layers per call) and k class, the required layer time is
    t_req = T_C / (10 * k * (sigma/e) * F) = Dmax_k1(100 ns) * 100 ns / (k * F)
and the accepted magic-state rate while running at t_req is T_call / (F * t_req).
This is a different path from WS-floor/decision (which divides k_10x by k): here sigma/e and T_C are
read from the gap ledger and the identity t_req / 100 ns = k_10x(unlimited) / k is a self-check.

Part 3 (C09): distribution-free 99% classical time from Stage C data. Empirical Bernstein
(Maurer & Pontil 2009, Thm 4), two-sided at delta = 0.01:
    half-width(n) = sqrt(2 sigma^2 L / n) + 7 S L / (3 (n - 1)),  L = ln(4 / delta),
with S = 40 (payoff range: strike 100, knock-out barrier 140 on the basket average), e = 0.45 eps
(the same split as the Stage C practice CI and the quantum). The factor is T_df / T_C(practice).

Stdlib only; run from the repo root with
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/hwclassical/hw_classical.py
Writes results/plan110_n1/hwclassical/hw_classical_card.json with exclusive create.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path.cwd()
P = {
    'floor': ROOT / 'results/plan110_w0/ws_floor/floor.json',
    'decision_rows': ROOT / 'results/plan110_w0/decision/run002/decision_rows.json',
    'gap_ledger': ROOT / 'docs/program_plan_20261010/supporting/gap_ledger.json',
    'sigma_dev': ROOT / 'results/frontier_classical_20261001/sigma_dev/sigma_dev.json',
    'c1_summary': ROOT / 'results/frontier_classical_20261001/c1/c1_summary.json',
    'c2_timing': ROOT / 'results/frontier_classical_20261001/c2/c2_timing.json',
    'h16_summary': ROOT / 'results/plan110_w0/ws_small/h16_grid/run001/summary.json',
}
OUT = ROOT / 'results/plan110_n1/hwclassical' / (sys.argv[1] if len(sys.argv) > 1 else 'hw_classical_card_v2.json')

T100 = 1e-7
W0_WIDTH, W0_SUPPLY = 1e7, 1e12
DELTA = 0.01
S_RANGE = 40.0           # payoff range in $ (assumed from contract: max(avg-100,0) with avg<140 alive)
S_RANGE_SENS = 64.0      # quantum span (dyadic), sensitivity
SHARE = 0.45
FLOORS = ('box_muller_current_law', 'all_free_and_narrow')
K_CLASSES = ('certified_today', 'explicit_best', 'no_explicit_constant')
OVERHEAD = {('B8x52', 0.1), ('B4x12', 0.1), ('B8x52', 0.03), ('B4x12', 0.03)}

# Verified anchors (rows A01-A12 in rows.jsonl). value_s is the anchor's own timing definition.
ANCHORS = [
    dict(id='A01', what='complete readout-end -> feedback-start loop, live d=3 surface code (FPGA NN decoder)',
         value_s=550e-9, d=3, platform='superconducting', year=2026, status='demonstrated',
         cite='Yang et al., arXiv:2605.04892'),
    dict(id='A02', what='decoding-feedback pipeline, syndrome bits -> correction ready; NO qubits, no readout/DAC',
         value_s=446e-9, d=3, platform='RFSoC control prototype (loopback)', year=2026,
         status='demonstrated (partial loop)', cite='Liu et al., arXiv:2603.16203'),
    dict(id='A03a', what='surface-code QEC cycle (memory)', value_s=1.1e-6, d=7, platform='superconducting (Willow)',
         year=2024, status='demonstrated', cite='Google Quantum AI, arXiv:2408.13687'),
    dict(id='A03b', what='average real-time decoder latency (no logical feedback loop closed)', value_s=63e-6, d=5,
         platform='superconducting (Willow)', year=2024, status='demonstrated', cite='arXiv:2408.13687'),
    dict(id='A06', what='fast-feedback response time (8-qubit stability experiment)', value_s=9.6e-6, d=None,
         platform='superconducting (Rigetti Ankaa-2)', year=2024, status='demonstrated',
         cite='Caune et al., arXiv:2410.05202'),
    dict(id='A05a', what='assumed syndrome round = reaction time (options-pricing table I)', value_s=1e-6, d=None,
         platform='superconducting (projection)', year=2025, status='projected', cite='McArdle et al., arXiv:2510.26078'),
    dict(id='A04a', what='surface-code cycle', value_s=1e-6, d=25, platform='superconducting (projection)', year=2025,
         status='projected', cite='Gidney, arXiv:2505.15917'),
    dict(id='A04b', what='reaction time', value_s=10e-6, d=25, platform='superconducting (projection)', year=2025,
         status='projected', cite='arXiv:2505.15917'),
    dict(id='A04c', what='lattice-surgery / CCZ period', value_s=25e-6, d=25, platform='superconducting (projection)',
         year=2025, status='projected', cite='arXiv:2505.15917'),
    dict(id='A07', what='cat-qubit cycle (a logical gate spans >= 1 cycle)', value_s=500e-9, d=None,
         platform='repetition-cat (projection)', year=2023, status='projected', cite='Gouzien et al., arXiv:2302.06639'),
]
# Rate / width anchors (literature, verified in rows A04, A05, A09)
RATE_ANCHORS = [
    dict(id='A04d', what='CCZ states per second, 6 factories at one CCZ per 25 us (derived)', value=6 / 25e-6,
         status='projected', cite='arXiv:2505.15917 (derived: 6 x 1/25us)'),
    dict(id='A05b', what='options-pricing T rate implied by 1e10 T in 3.7 days', value=1e10 / (3.7 * 86400),
         status='projected', cite='arXiv:2510.26078 Table I (derived)'),
]
WIDTH_ANCHORS = [
    dict(id='A09', what='largest demonstrated logical-qubit count (d=3-7 codes, 280 atoms)', value=48,
         status='demonstrated', cite='Bluvstein et al., arXiv:2312.03982'),
    dict(id='A05c', what='logical qubits in the options-pricing projection', value=1e4, status='projected',
         cite='arXiv:2510.26078 Table I'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads(P[name].read_text(encoding='utf-8'))


def eb_n(sigma, e, s_range, delta=DELTA):
    """Smallest n with sqrt(2 sigma^2 L/n) + 7 S L/(3(n-1)) <= e (two-sided, empirical Bernstein)."""
    lg = math.log(4 / delta)

    def hw(n):
        return math.sqrt(2 * sigma * sigma * lg / n) + 7 * s_range * lg / (3 * (n - 1))
    lo, hi = 2.0, 2.0
    while hw(hi) > e:
        hi *= 2
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if hw(mid) > e else (lo, mid)
    return math.ceil(hi)


def hoeffding_n(e, s_range, delta=DELTA):
    return math.ceil(s_range ** 2 * math.log(2 / delta) / (2 * e * e))


def median(xs):
    xs = sorted(xs)
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def per_point_cost(c2, case, method):
    """Median marginal wall time per point at 16 workers, from the C2 warm runs (2^18 -> 2^19 points per scramble)."""
    block = c2['blocks'][f'{case}/{method}']
    slopes = [(w['all16']['524288'] - w['all16']['262144']) / (16 * 262144) for w in block['warm']]
    return median(slopes)


def part2(floor, gl, drows):
    gl_rows = {(r['case'], float(r['eps'])): r for r in gl['rows']}
    kc = {}
    for r in drows:
        if (r['width'] == 'W1e7' and r['design'] == 'box_muller_current_law' and r['t_layer'] == '100ns'
                and r['sigma'] == 'base' and r['supply'] == 'supply_1e12'):
            kc[(r['case'], float(r['eps']), r['k_class'])] = r['k']
    out = []
    checks = []
    for case in ('B4x12', 'B8x52'):
        for design in FLOORS:
            rec = floor['headline'][case]['W1e7'][design]
            F = rec['call_reaction_layers']['value']
            t_call = rec['call_T_count']['value']
            width = rec['width_qubits']['value']
            for comp in rec['comparison']:
                eps = float(comp['eps'])
                g = gl_rows[(case, eps)]
                base = comp['by_t_layer']['100ns']['base']
                # independent path: T_C and sigma/e from the gap ledger
                dt_budget = g['T_C_env'] / (10 * g['sigma_over_e'])       # seconds of quantum latency per (sigma/e) call
                checks.append(abs(dt_budget / (base['Dmax_k1'] * T100) - 1))
                for kname in K_CLASSES:
                    k = kc.get((case, eps, kname))
                    if k is None:
                        continue
                    t_req = dt_budget / (k * F)
                    rate_req = t_call / (F * t_req)
                    k10_unl = base['k_10x_unlimited_supply']
                    checks.append(abs((t_req / T100) / (k10_unl / k) - 1))
                    out.append(dict(
                        case=case, eps=eps, floor_design=design, k_class=kname, k=k,
                        overhead_T_C=(case, eps) in OVERHEAD, T_C_s=g['T_C_env'], T_C_raw_s=g['T_C'], sigma_over_e=g['sigma_over_e'],
                        floor_layers=F, call_T=t_call,
                        t_layer_required_s=t_req, t_layer_required_over_100ns=t_req / T100,
                        T_per_s_required=rate_req, T_per_s_required_over_budget=rate_req / W0_SUPPLY,
                        logical_width=width, width_over_budget=width / W0_WIDTH,
                        loop_550ns_over_required=550e-9 / t_req,
                        label='modelled (floor modelled; T_C measured; k modelled)',
                        direction='quantum-favourable (idealized floor, zero Clifford/routing cost)'))
    return out, max(checks)


def part3(gl, sd, c1, c2, h16, drows):
    gl_rows = {(r['case'], float(r['eps'])): r for r in gl['rows']}
    cost = {(case, m): per_point_cost(c2, case, m) for case in ('B4x12', 'B8x52') for m in ('preint', 'rqmc')}
    rows = []
    for (case, eps), g in sorted(gl_rows.items()):
        e = SHARE * eps
        sig_pre = sd['cases'][case]['sigma_preint']
        sig_q = sd['cases'][case]['sigma_q']
        routes = {}
        for s_range, tag in ((S_RANGE, 'S40'), (S_RANGE_SENS, 'S64')):
            n1 = eb_n(sig_pre, e, s_range)
            n2 = eb_n(sig_q, e, s_range)
            # RQMC blocks of m points (preint), EB over iid block means; sd per block measured in C1 (eigh basis)
            c1c = c1['cases'][case]
            sds = c1c['summary']['eigh']['knockout_pre']['sd_one_scramble']
            best_blk = None
            for m_exp, sdm in zip(c1c['ms'], sds):
                m = 2 ** m_exp
                r_blocks = eb_n(sdm, e, s_range)
                pts = r_blocks * m
                if best_blk is None or pts < best_blk[1]:
                    best_blk = (m, pts, r_blocks)
            routes[tag] = {
                'iid_preint_EB': dict(n=n1, t_s=n1 * cost[(case, 'preint')]),
                'iid_plain_EB': dict(n=n2, t_s=n2 * cost[(case, 'rqmc')]),
                'rqmc_blocks_preint_EB': dict(block_m=best_blk[0], blocks=best_blk[2], n=best_blk[1],
                                              t_s=best_blk[1] * cost[(case, 'preint')]),
                'hoeffding_plain': dict(n=hoeffding_n(e, s_range),
                                        t_s=hoeffding_n(e, s_range) * cost[(case, 'rqmc')]),
            }
        best = min(routes['S40'].items(), key=lambda kv: kv[1]['t_s'])
        factor = best[1]['t_s'] / g['T_C_env']
        n_practice_equiv = g['T_C_candidates'][g['classical_best']]['n_eps'] * 16
        rows.append(dict(case=case, eps=eps, e=e, T_C_practice_s=g['T_C_env'], T_C_conv=g['T_C_conv'],
                         practice_method=g['classical_best'], practice_points=n_practice_equiv,
                         overhead_T_C=(case, eps) in OVERHEAD,
                         sigma_preint=sig_pre, sigma_q=sig_q, routes=routes, best_route_S40=best[0],
                         T_df_s=best[1]['t_s'], factor_df_over_practice=factor,
                         factor_S64=min(v['t_s'] for v in routes['S64'].values()) / g['T_C_env'],
                         label='modelled from measured inputs (sigma, per-point cost, T_C measured; EB bound analytic)',
                         direction='quantum-favourable if adopted (classical slows; quantum k already worst-case 99%)'))
    # M under distribution-free classical, primary convention otherwise
    fac = {(r['case'], r['eps']): r['factor_df_over_practice'] for r in rows}
    m_df = []
    for r in drows:
        if (r['width'] == 'W1e7' and r['t_layer'] == '100ns' and r['sigma'] == 'base' and r['supply'] == 'supply_1e12'
                and r['design'] in FLOORS):
            f = fac[(r['case'], float(r['eps']))]
            m_df.append(dict(case=r['case'], eps=r['eps'], design=r['design'], k_class=r['k_class'],
                             overhead_T_C=r['overhead_T_C'], M_practice=r['M_practice_16core'],
                             factor_df=f, M_distfree=r['M_practice_16core'] / f,
                             M_1lane_1core=r['M_1lane_1core']))
    mins = {}
    for design in FLOORS:
        for kname in K_CLASSES:
            sel = [x for x in m_df if x['design'] == design and x['k_class'] == kname and not x['overhead_T_C']]
            if sel:
                b = min(sel, key=lambda x: x['M_distfree'])
                p = min(sel, key=lambda x: x['M_practice'])
                mins[f'{design}|{kname}'] = dict(min_M_practice=p['M_practice'], at_practice=(p['case'], p['eps']),
                                                 min_M_distfree=b['M_distfree'], at_distfree=(b['case'], b['eps']))
    h = h16['summary']
    h16_rows = [dict(cell=k, t_c_by_workers=v['t_c_by_workers'], speedup_16_vs_1=v['speedup_vs_1']['16'],
                     parallel_efficiency_16=v['speedup_vs_1']['16'] / 16, w16_vs_c2=v['t_c_by_workers']['16'] /
                     v['c2_primary_w16'], label='measured (H16 grid run001, preint, idle machine)',
                     direction='quantum-favourable if 1-core convention used (factor 6.4-10.2, not 16)')
                for k, v in h.items()]
    return dict(per_point_cost_s_16w=({f'{c}|{m}': v for (c, m), v in cost.items()}), rows=rows, M_distfree=m_df,
                M_minima=mins, h16=h16_rows)


def main():
    floor, gl, drows = load('floor'), load('gap_ledger'), load('decision_rows')
    sd, c1, c2, h16 = load('sigma_dev'), load('c1_summary'), load('c2_timing'), load('h16_summary')
    nec, self_check = part2(floor, gl, drows)
    cls = part3(gl, sd, c1, c2, h16, drows)
    anchors = [dict(a, over_100ns=a['value_s'] / T100) for a in ANCHORS]
    card = dict(
        inputs_sha256={str(p.relative_to(ROOT)): sha(p) for p in P.values()},
        python=sys.version, isolated_flags=dict(isolated=sys.flags.isolated, no_site=sys.flags.no_site,
                                                dont_write_bytecode=sys.flags.dont_write_bytecode),
        conventions=dict(t_layer_primary_s=T100, width_budget=W0_WIDTH, supply_budget=W0_SUPPLY, delta=DELTA,
                         S_range=S_RANGE, S_range_sens=S_RANGE_SENS, share=SHARE),
        anchors_time=anchors, anchors_rate=RATE_ANCHORS, anchors_width=WIDTH_ANCHORS,
        necessary_conditions=nec, self_check_max_rel_err=self_check,
        classical=cls,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('x', encoding='utf-8') as f:
        json.dump(card, f, indent=1, sort_keys=True)
    print('self-check max rel err', self_check)
    for r in nec:
        if r['floor_design'] == 'box_muller_current_law' or r['k_class'] != 'no_explicit_constant':
            print(f"{r['case']} eps={r['eps']:<6} {r['floor_design'][:12]:12s} {r['k_class'][:12]:12s} k={r['k']:7.1f} "
                  f"t_req={r['t_layer_required_s'] * 1e9:9.4f} ns  T/s={r['T_per_s_required']:.3g} "
                  f"w={r['logical_width']:.3g} ovh={r['overhead_T_C']}")
    for r in cls['rows']:
        print(r['case'], r['eps'], 'T_C', round(r['T_C_practice_s'], 3), 'best', r['best_route_S40'],
              'T_df', round(r['T_df_s'], 1), 'factor', round(r['factor_df_over_practice'], 1),
              'S64', round(r['factor_S64'], 1))
    print(json.dumps(cls['M_minima'], indent=1))
    print(json.dumps(cls['per_point_cost_s_16w'], indent=1))


if __name__ == '__main__':
    sys.exit(main())
