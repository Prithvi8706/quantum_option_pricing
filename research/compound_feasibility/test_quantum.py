import numpy as np
from .quantum_schedule import *


def test_nested_schedule_error_and_invocation_identity():
    s=nested_schedule(128.,.01)
    assert s['dollar_bound']<=.00800000001
    assert s['conditional_primitive_and_inverse_calls']==sum(r['conditional_primitive_and_inverse_calls'] for r in s['rows'])
    for r in s['rows']:
        for b in [r['inner']]+([r['previous_inner']] if r['previous_inner'] else []):
            assert b['mse_bound']<=2.**(-2*b['level'])
            assert np.pi/b['M']+np.pi**2/b['M']**2<=b['error']
    improved=nested_schedule(128.,.01,normalizer=1.,target_second_moment=114.3)
    assert improved['dollar_bound']<=.00800000001
    assert improved['rows'][0]['outer']['second_moment']<128**2
    for r in improved['rows']:
        b=r['inner'];assert b['bound']*(np.pi/b['M']+np.pi**2/b['M']**2)<=b['error']


def test_enumerated_quantum_inner_telescoping_and_moments():
    ps=[.1,.45,.8];px=np.array([.2,.3,.5]);strike=.4;truth=np.maximum(np.array(ps)-strike,0)
    previous=None;telescoping=0.
    for l in range(5):
        distributions=[exact_inner_distribution(p,strike,l) for p in ps]
        means=np.array([np.dot(v,q) for v,q in distributions]);second=np.array([np.dot(v*v,q) for v,q in distributions])
        mse=second-2*means*truth+truth**2
        assert np.max(mse)<=2.**(-2*l)+1e-12
        if l==0:telescoping=np.dot(px,means)
        else:
            pm,ps2=previous
            delta_m2=np.dot(px,second+ps2-2*means*pm)
            assert delta_m2<=10*2.**(-2*l)+1e-12
            telescoping+=np.dot(px,means-pm)
        assert abs(telescoping-np.dot(px,means))<1e-12
        assert abs(telescoping-np.dot(px,truth))<=2.**(-l)+1e-12
        previous=(means,second)
