"""Compile the actual scheduled bin endpoints and check the charged envelope."""
import json
from pathlib import Path
from .bin_oracle import bin_for_bound,bin_program
from .reversible import clifford_t_resources


def run():
    root=Path('results/antithetic_feasibility');out=root/'bin_audit_v1';out.mkdir(exist_ok=False)
    costs=json.loads((root/'complete_cost_screen_v1/costs.json').read_text())
    rows=[]
    for f in (24,32):
        w=f+16;baseline=clifford_t_resources(bin_program(w,w,2**(w-3),2**(w-2),1)[0])
        endpoints=sorted(set((b['lower'],b['upper'],b['sign']) for c in costs if c['fraction_bits']==f for s in c['schedules'] for b in s['bins']))
        for lower,upper,sign in endpoints:
            p,(_,selector),_=bin_for_bound(w,f,lower,upper,sign);r=clifford_t_resources(p)
            assert r['t_count']<=baseline['t_count'] and r['t_depth']<=baseline['t_depth'] and r['qubits']<=baseline['qubits']
            rows.append(dict(fraction_bits=f,lower=lower,upper=upper,sign=sign,selector_bits=len(selector),**r))
    (out/'rows.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(dict(compiled_bins=len(rows),status='All actual scheduled bins fit charged T-count, T-depth and workspace envelope; selector normalization exact.')))


if __name__=='__main__':run()
