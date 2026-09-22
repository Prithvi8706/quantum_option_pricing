"""Saved tables/figures from executed compound acquisitions."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run():
    root=Path('results/compound_feasibility');out=root/'decision_v1';out.mkdir(exist_ok=False)
    read=lambda name:json.loads((root/name).read_text())
    pilot=read('pilot_v1/summaries.json');ref=read('reference_combined_v1/summaries.json');cost=read('cost_v3/costs.json');cold=read('cold_timing_v1/receipts.json')
    fig,axes=plt.subplots(1,2,figsize=(11,4.4))
    for case in ('C4','C8','H4','H8'):
        rr=[r for r in pilot if r['case']==case and r['strike']==6]
        n=[2**r['inner_power'] for r in rr]
        axes[0].loglog(n,[r['mean_gap'] for r in rr],'o-',label=case)
        axes[1].loglog(n,[r['total_interval_width'] for r in rr],'o-',label=case)
    axes[0].set(title='Policy-to-Jensen gap at compound strike $6',xlabel='Shared inner scenarios',ylabel='Estimated expectation gap ($)')
    axes[1].set(title='Sampling uncertainty remains after nesting shrinks',xlabel='Shared inner scenarios',ylabel='Empirical endpoint interval width ($)')
    axes[1].axhline(.02,ls='--',color='black',label='Width for ±$0.01')
    for ax in axes:ax.grid(alpha=.2);ax.legend()
    fig.tight_layout();fig.savefig(out/'classical_nesting.png',dpi=180);fig.savefig(out/'classical_nesting.pdf');plt.close(fig)
    records=[]
    for c in cold:
        rr=read('cold_timing_v1/'+c['case']+'/summaries.json');q=next(r for r in cost if r['case']==c['case'] and r['epsilon']==.01 and r['fraction_bits']==32)
        records.append(dict(case=c['case'],cold_seconds=c['cold_seconds'],maximum_empirical_interval_width=max(r['total_interval_width'] for r in rr),
                            quantum_10x_seconds=c['cold_seconds']/10,explicit_source_calls=q['conditional_source_and_inverse_calls'],
                            explicit_maximum_seconds_per_conditional_source=c['cold_seconds']/(10*q['conditional_source_and_inverse_calls']),
                            ideal_source_calls=q['ideal_conditional_calls_no_constants_logs'],
                            ideal_maximum_seconds_per_conditional_source=c['cold_seconds']/(10*q['ideal_conditional_calls_no_constants_logs']),
                            ideal_one_multiply_seconds=q['ideal_one_multiply_seconds_at_100ns'],
                            scope='Zero quantum setup assumed. Conditional source budgets are coordinates for these schedules, not algorithm-independent lower bounds.'))
    (out/'crossover.json').write_text(json.dumps(records,indent=2)+'\n')
    (out/'reference_table.json').write_text(json.dumps([dict(case=r['case'],strike=r['strike'],midpoint=(r['interval_low']+r['interval_high'])/2,empirical_radius=r['total_interval_width']/2) for r in ref],indent=2)+'\n')
    for r in records:print(json.dumps(r))


if __name__=='__main__':run()
