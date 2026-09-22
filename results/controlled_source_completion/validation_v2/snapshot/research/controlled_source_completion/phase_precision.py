"""Compile and check the higher-precision complex phase, including full gates."""
import math
import json
import mpmath as mp
from research.controlled_source_completion.compiler import compile_graph,phase_graph,execute
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.optimize import optimize
from research.controlled_source_completion.run import ROOT,dump
from research.controlled_source_completion.cost import phase_error_bound


def main():
    f=64;g=phase_graph(f);data=optimize(g.as_dict());manifest,_=compile_graph(data,ROOT/'compile_v2'/'phase_f64')
    mp.mp.dps=90;rows=[];maxerror=mp.mpf(0)
    # Exercise signs, reciprocal branch and the branch boundary at |z|=1.
    for y in (-98.5,-16.,-1.,-.0001,0.,.0001,1.,16.,98.5):
        for left in (-.441,0.,.441):
            raw_y=round(y*2**40)<<24;raw_left=int(mp.nint(mp.mpf(str(left))*2**f));exponent=4
            given=dict(Y=raw_y,left=raw_left,scale_exponent=exponent)
            out,trace=evaluate(data,given,True);raw=trace[data['outputs']['angle']]
            signed=raw-(1<<data['width']) if raw>>(data['width']-1) else raw
            reference=-2*mp.atan((mp.mpf(raw_y)-raw_left)/2**(f+exponent));error=abs(mp.mpf(signed)/2**f-reference);maxerror=max(maxerror,error)
            if y in (-98.5,0.,98.5) and left==0.:
                gate=execute(manifest,given)
                assert gate['values']['angle']==raw and gate['workspace_clean'] and gate['inputs_preserved']
            rows.append(dict(y=y,left=left,absolute_error=str(error)))
    assert float(maxerror)<=phase_error_bound(f)
    # The CP decomposition is checked as a complex matrix; relative phases count.
    import numpy as np
    for theta in (-4.,1e-10,.5,2.):
        P=lambda a:np.diag([1.,np.exp(1j*a)])
        cx=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
        actual=cx@np.kron(np.eye(2),P(-theta/2))@cx@np.kron(P(theta/2),P(theta/2))
        assert np.max(np.abs(actual-np.diag([1,1,1,np.exp(1j*theta)])))<1e-14
    dump(ROOT/'validation_v2'/'phase64.json',dict(fraction_bits=f,rows=rows,max_observed_error=str(maxerror),
        analytic_conservative_bound=phase_error_bound(f),full_gate_cases=3,controlled_phase_matrix_cases=4,
        resources=manifest['resources'],scope='Tests of digital phase arithmetic and CP identity; arbitrary rotation synthesis and physical implementation remain open.'))
    print(json.dumps(dict(max_observed_error=str(maxerror),analytic_bound=phase_error_bound(f),resources=manifest['resources'])),flush=True)


if __name__=='__main__':main()
