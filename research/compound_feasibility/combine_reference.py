"""Use both independent reference acquisitions; no selection by price outcome."""
import json
import math
from pathlib import Path
import numpy as np
from scipy.stats import t
from .model import MODELS,choose_cap


def run():
    root=Path('results/compound_feasibility');out=root/'reference_combined_v1';out.mkdir(exist_ok=False)
    raw=lambda name:[json.loads(line) for line in (root/name/'rows.jsonl').read_text().splitlines()]
    first=raw('reference_stream_v1');second=raw('reference_refine_v1');rows=[]
    for m in MODELS:
        groups=[[r for r in first if r['case']==m.name]]
        if m.name in ('H4','H8'):groups.append([r for r in second if r['case']==m.name])
        cap,tail=choose_cap(m)
        for ki,k in enumerate((3.,6.,9.)):
            estimates=[];radii=[];dfs=[]
            for field in ('lower','upper'):
                arrays=[np.array([r[field][ki] for r in group]) for group in groups];means=[x.mean() for x in arrays]
                v=np.array([x.var(ddof=1)/len(x) for x in arrays]);df=float(v.sum()**2/sum(vv*vv/(len(x)-1) for vv,x in zip(v,arrays)))
                se=math.sqrt(v.sum())/len(groups)
                estimates.append(float(np.mean(means)));radii.append(float(t.ppf(.9975,df)*se));dfs.append(df)
            low=estimates[0]-radii[0];high=estimates[1]+radii[1]+tail
            row=dict(case=m.name,strike=k,lower=estimates[0],upper=estimates[1],interval_low=low,interval_high=high,total_interval_width=high-low,
                     endpoint_radii=radii,welch_degrees_freedom=dfs,independent_groups=len(groups),replicates=sum(len(x) for x in groups),
                     interpretation='Equal-weight mixture of independent valid lower/upper estimators; Welch endpoint intervals are empirical. Different inner M targets remain upper bounds. No stopped matrix-run samples counted twice.')
            rows.append(row);print(json.dumps(row),flush=True)
    (out/'summaries.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':run()
