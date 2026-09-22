"""Reconcile references, quantum screens and statistical evidence; make plot."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run():
    root=Path('results/controlled_residual_feasibility');out=root/'decision_v1';out.mkdir(exist_ok=False)
    def read(p):return json.loads(p.read_text())
    ref=read(Path('results/compound_feasibility/decision_v1/reference_table.json'))
    old=read(root/'pilot_v1/summaries.json');parity=read(root/'parity_pilot_v1/summaries.json');cert=read(root/'parity_iid_v1/summaries.json')
    costs=read(root/'cost_v1/costs.json');sensitivity=read(root/'cost_v1/sensitivity.json')
    classical=read(root/'parity_classical_v1/summaries.json');cold=read(root/'cold_v1/receipts.json')
    comparison=[]
    for x in classical:
        y=next(r for r in ref if r['case']==x['case'] and r['strike']==x['strike'])
        comparison.append(dict(case=x['case'],strike=x['strike'],inner_power=x['inner_power'],
                               interval_low=x['interval_low'],interval_high=x['interval_high'],
                               empirical_radius=x['total_interval_width']/2,
                               reference_midpoint=y['midpoint'],reference_empirical_radius=y['empirical_radius'],
                               intervals_overlap=x['interval_high']>=y['midpoint']-y['empirical_radius'] and x['interval_low']<=y['midpoint']+y['empirical_radius'],
                               penny_empirical_target_pass=x['total_interval_width']<=.02))
    (out/'reference_checks.json').write_text(json.dumps(comparison,indent=2)+'\n')
    crossover=[]
    for receipt in cold:
        case=receipt['case'];prices=read(root/'cold_v1'/case/'summaries.json')
        maxwidth=max(r['total_interval_width'] for r in prices)
        if maxwidth>.02:raise AssertionError('Cold classical selected allocation missed penny target; revise comparison explicitly')
        for price in prices:
            c=next(r for r in costs if r['case']==case and r['strike']==price['strike'] and r['fraction_bits']==32)
            ss=next(r for r in sensitivity if r['case']==case and r['strike']==price['strike'] and r['fraction_bits']==32 and r['T_layer_ns']==100)
            # Strongest cold implementation keeps its own setup and uncertainty.
            comparator=min(receipt['cold_seconds'],c['previous_cold_classical_seconds'])
            q=c['ideal_unit_constant_queries']
            crossover.append(dict(case=case,strike=price['strike'],new_cold_seconds=receipt['cold_seconds'],
                new_empirical_radius=price['total_interval_width']/2,strongest_measured_cold_seconds=comparator,
                quantum_10x_budget_seconds=comparator/10,ideal_queries=q,
                ideal_source_budget_seconds=comparator/(10*q),
                ideal_T_layer_budget_seconds_if_only_one_exp=comparator/(10*q*c['one_exp_T_depth']),
                ideal_one_exp_seconds_at_100ns=ss['ideal_one_exp_seconds'],
                empirical_moment_ideal_one_exp_seconds_at_100ns=ss['empirical_ideal_one_exp_seconds'],
                preprocessing_seconds=c['preprocessing_seconds'],
                explicit_A_and_inverse_calls=c['explicit_A_and_inverse_calls'],
                quantum_screen_pass=False,
                scope='No complete quantum price is implemented. Favorable residual-only sensitivities and measured classical whole-price costs.'))
    (out/'crossover.json').write_text(json.dumps(crossover,indent=2)+'\n')
    labels=[r['case']+' / '+str(int(r['strike'])) for r in parity]
    a=np.array([r['statistics']['flat_residual_second_moment']['mean'] for r in old])
    b=np.array([r['statistics']['flat_residual_second_moment']['mean'] for r in parity])
    c=np.array([r['second_moment_upper'] for r in cert]);xx=np.arange(len(labels))
    fig,ax=plt.subplots(figsize=(11,4.8),layout='constrained')
    ax.bar(xx-.25,a,.25,label='Geometric-call control: pilot moment',color='#627d98')
    ax.bar(xx,b,.25,label='Parity control: pilot moment',color='#157f6b')
    ax.bar(xx+.25,c,.25,label='Parity: iid upper confidence bound',color='#b77022')
    ax.set_yscale('log');ax.set_ylabel('Single-sample residual second moment (dollars squared)')
    ax.set_xticks(xx,labels,rotation=40,ha='right');ax.set_xlabel('Model / compound strike')
    ax.set_title('Residual reduction helps; a pilot moment is not a certified query budget')
    ax.grid(axis='y',which='major',alpha=.22);ax.legend(loc='upper left',fontsize=8)
    fig.savefig(out/'residual_moments.png',dpi=170);fig.savefig(out/'residual_moments.pdf');plt.close(fig)
    final=dict(development_contracts=len(parity),fixed_iid_outer_samples_per_model=cert[0]['samples'],
               regret_budget_passes=sum(r['regret_upper']<=.003 for r in cert),
               maximum_regret_upper=max(r['regret_upper'] for r in cert),
               all_256_inner_classical_empirical_penny_pass=all(r['penny_empirical_target_pass'] for r in comparison if r['inner_power']==8),
               all_classical_intervals_overlap_independent_references=all(r['intervals_overlap'] for r in comparison),
               status='No defensible significant quantum advantage established yet.',
               bounds_scope='Statistical guarantees idealize iid sampling and real evaluation; full pricing and hardware guarantees remain unestablished.')
    (out/'decision.json').write_text(json.dumps(final,indent=2)+'\n');print(json.dumps(final,indent=2))


if __name__=='__main__':run()
