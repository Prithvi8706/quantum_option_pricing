"""Rebuild saved diagnostic figures and numerical decision tables."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run():
    root=Path('results/antithetic_feasibility');out=root/'decision_summary_v1';out.mkdir(exist_ok=False)
    read=lambda p:json.loads((root/p).read_text())
    corr=read('classical_corrections_v1/summaries.json')+read('stress_corrections_v1/summaries.json')
    fit=[];fig,ax=plt.subplots(figsize=(7.4,4.8))
    for case,power in [('A1',10),('A4',10),('S4',8),('B8',8)]:
        for method,cond in [('mc',False),('rqmc',True)]:
            rr=sorted([r for r in corr if r['case']==case and r['power']==power and r['method']==method and r['conditional']==cond],key=lambda r:r['level'])
            levels=np.array([r['level'] for r in rr]);var=np.array([r['sample_variance'] for r in rr]);beta=-np.polyfit(levels,np.log2(var),1)[0]
            fit.append(dict(case=case,method=method,conditional=cond,beta=float(beta),levels=levels.tolist(),variances=var.tolist(),scope='Descriptive fit, five development levels, no confidence band or theorem.'))
            if not cond:ax.semilogy(levels,var,'o-',label=f'{case}: fitted beta {beta:.2f}')
    ax.set(xlabel='Refinement level (12 × 2^level steps)',ylabel='Antithetic correction sample variance',title='Variance reduction survives; its rate depends on parameters')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(out/'variance_decay.png',dpi=180);fig.savefig(out/'variance_decay.pdf');plt.close(fig)
    hybrid=read('hybrid_classical_v1/summaries.json')
    fig,ax=plt.subplots(figsize=(7.4,4.8))
    for case in ('A1','A4'):
        rr=[r for r in hybrid if r['case']==case]
        ax.loglog([r['empirical_99pct_radius'] for r in rr],[r['seconds'] for r in rr],'o-',label=case)
    ax.set(xlabel='Empirical 99% sampling half-width ($)',ylabel='Measured CPU seconds (fit included)',title='Classical six-level pricing diagnostics — not a bias certificate')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(out/'classical_precision_cost.png',dpi=180);fig.savefig(out/'classical_precision_cost.pdf');plt.close(fig)
    sens=read('hierarchy_sensitivity_v1/rows.json');fig,ax=plt.subplots(figsize=(7.4,4.8))
    for case in ('A1','A4'):
        rr=[r for r in sens if r['case']==case and r['epsilon']==.01]
        ax.semilogy([r['maximum_level'] for r in rr],[r['ideal_sqrt_only_seconds_at_100ns']/r['quantum_10x_budget_seconds'] for r in rr],'o-',label=case)
    ax.axhline(1,color='black',linestyle='--',label='Meets 10× target')
    ax.set(xlabel='Last included level (bias eligibility granted)',ylabel='Additional cost reduction required (×)',title='Optimistic square-root-only screen at 100 ns per T layer')
    ax.text(.02,.04,'Unit query constant; all other work free.\nNot an algorithm or universal lower bound.',transform=ax.transAxes,fontsize=9)
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(out/'ideal_screen.png',dpi=180);fig.savefig(out/'ideal_screen.pdf');plt.close(fig)
    (out/'variance_fits.json').write_text(json.dumps(fit,indent=2)+'\n')
    print(json.dumps(fit,indent=2))


if __name__=='__main__':run()
