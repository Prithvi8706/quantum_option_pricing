import math
import numpy as np
import pytest
from research.controlled_source_completion.primitives import build,basis_run,resources
from research.controlled_source_completion.ir import Graph,evaluate
from research.controlled_source_completion.modern_mean import plan,update,spectral_law,exact_qpe_test_probability


@pytest.mark.parametrize('op',['add','sub','mul','cmul','lt','select','positive','divide','sqrt','msb','shift','bits','lookup','const'])
def test_leaf_permutation_and_clean_workspace(op):
    w=8;f=3;mask=255;rng=np.random.default_rng(2026092601)
    params={'cmul':{'c':-13},'bits':{'shift':3,'width':8,'signed':True},
            'lookup':{'bits':3},'const':{'value':-123}}.get(op,{})
    table=[[i*i-9,17-i] for i in range(8)] if op=='lookup' else None
    p,args,outs=build(op,w,f,params,table)
    def signed(x):return x-256 if x>=128 else x
    cases=[list(map(int,rng.integers(0,256,len(args)))) for _ in range(48)]
    if op=='shift':cases += [[x,k&255] for x in (0,1,127,128,255) for k in (-128,-9,-8,-7,-1,0,1,7,8,9,127)]
    if op=='divide':cases += [[255,0],[0,0],[255,1],[255,255],[0,255]]
    for raw in cases:
        v=list(map(signed,raw))
        if op=='add':expected=[v[0]+v[1]]
        elif op=='sub':expected=[v[0]-v[1]]
        elif op=='mul':expected=[v[0]*v[1]>>f]
        elif op=='cmul':expected=[v[0]*params['c']>>f]
        elif op=='lt':expected=[int(v[0]<v[1])]
        elif op=='select':expected=[raw[1] if raw[0]&1 else raw[2]]
        elif op=='positive':expected=[max(0,v[0])]
        elif op=='divide':expected=[(raw[0]<<f)//raw[1] if raw[1] else 255]
        elif op=='sqrt':expected=[math.isqrt(raw[0]<<f)]
        elif op=='msb':expected=[max(0,raw[0].bit_length()-1)]
        elif op=='shift':expected=[v[0]<<v[1] if v[1]>=0 else v[0]>>-v[1]]
        elif op=='bits':expected=[v[0]>>3]
        elif op=='lookup':expected=table[raw[0]&7]
        else:expected=[-123]
        initial=list(map(int,rng.integers(0,256,len(outs))))
        wanted=[(e&mask)^z for e,z in zip(expected,initial)]
        actual,clean,preserved,_=basis_run(p,args,outs,raw,initial)
        assert actual==wanted,(op,raw,actual,wanted)
        assert clean and preserved
        inv,clean,preserved,_=basis_run(p,args,outs,raw,actual,inverse=True)
        assert inv==initial and clean and preserved


def test_leaf_resource_scheduler_matches_existing():
    from research.antithetic_feasibility.reversible import clifford_t_resources
    p,_,_=build('mul',8,3)
    ours=resources(p);old=clifford_t_resources(p)
    for field in ('t_count','t_depth','clifford_t_depth'):assert ours[field]==old[field]


@pytest.mark.parametrize('fn,domain,tolerance',[
    ('log',(.001,4096),2e-8),('exp',(-8,8),1e-5),('cdf',(-12,12),2e-9),
    ('cos_unit',(0,1),2e-9),('atan',(-100,100),2e-8)])
def test_fixed_functions_against_independent_library(fn,domain,tolerance):
    from scipy.special import ndtr
    g=Graph(40);x=g.input('x',g.w);g.outputs={'y':getattr(g,fn)(x)};data=g.as_dict()
    reference={'log':math.log,'exp':math.exp,'cdf':ndtr,'cos_unit':lambda z:math.cos(2*math.pi*z),'atan':math.atan}[fn]
    xs=np.linspace(*domain,101)
    for xx in xs:
        raw=round(xx*2**g.f);value=evaluate(data,{'x':raw})['y']
        assert abs(value-reference(raw/2**g.f))<tolerance,(fn,xx,value,reference(xx))


def test_interval_contraction_covers_promise_and_gap():
    for left in (-3.,0.,1.25):
        width=4.
        for mu in np.linspace(left,left+width,101):
            outcomes=[False] if mu-left<width/4 else [True] if mu-left>width/2 else [False,True]
            for large in outcomes:
                lo,w=update(left,width,large);assert lo-1e-12<=mu<=lo+w+1e-12


def test_modern_schedule_and_spectral_sign():
    p=plan(.194480643,.002/math.exp(-.015))
    assert p['final_interval_radius']<=p['error']
    assert p['controlled_U_calls']==sum(x['repetitions']*(x['M']-1) for x in p['stages'])
    assert p['value_evaluations_and_inverses']==2*p['controlled_U_calls']
    for value in (0.,.005,-.005,.03):
        phases,weights=spectral_law([value,value],[.3,.7])
        assert abs(sum(weights*np.exp(1j*phases))-np.exp(-2j*math.atan(value)))<1e-12
    # Deterministic small / large promises, without replacing U's reflection by its negative.
    eps=.02;M=2**15
    assert exact_qpe_test_probability([.005],[1.],M,1.42*eps)<1/9
    assert exact_qpe_test_probability([.02],[1.],M,1.42*eps)>8/9


def test_hierarchical_binding_copy_inverse_and_aliases(tmp_path):
    from research.controlled_source_completion.compiler import compile_graph,execute
    g=Graph(3,5);a=g.input('a',8);b=g.input('b',8)
    squared=g.mul(a,a);value=g.sub(g.add(squared,b),g.c(2))
    g.outputs={'value':value,'positive':g.pos(value)}
    manifest,_=compile_graph(g.as_dict(),tmp_path)
    for aa,bb in ((5,7),(100,255),(255,128),(0,0)):
        _,trace=evaluate(g.as_dict(),dict(a=aa,b=bb),True)
        result=execute(manifest,dict(a=aa,b=bb),dict(value=27,positive=39))
        assert result['values']==dict(value=trace[value]^27,positive=trace[g.outputs['positive']]^39)
        assert result['workspace_clean'] and result['inputs_preserved']


@pytest.mark.parametrize('op',['mul','divide','sqrt','shift','lt'])
def test_production_width_emitted_leaves(op):
    w=72;f=40;p,args,outs=build(op,w,f)
    mask=(1<<w)-1
    cases={'mul':[(round(123.456*2**f),round(-2.34*2**f))],
           'divide':[(round(123.456*2**f),round(2.34*2**f))],
           'sqrt':[(round(123.456*2**f),)],'shift':[(round(-123.456*2**f),-17)],
           'lt':[(round(-123.456*2**f),0)]}[op]
    for v in cases:
        expected={'mul':lambda:(v[0]*v[1])>>f,'divide':lambda:(v[0]<<f)//v[1],
                  'sqrt':lambda:math.isqrt(v[0]<<f),'shift':lambda:v[0]>>17,'lt':lambda:int(v[0]<v[1])}[op]()
        actual,clean,preserved,_=basis_run(p,args,outs,[x&mask for x in v])
        assert actual==[expected&mask] and clean and preserved


def test_exact_optimizer_keeps_modular_behavior():
    from research.controlled_source_completion.optimize import optimize
    g=Graph(3,5);x=g.input('x',8);shared=g.add(x,g.c(3));duplicate=g.add(x,g.c(3))
    g.outputs={'y':g.add(g.mul(shared,duplicate),g.sqrt(g.c(9)))};data=g.as_dict();opt=optimize(data)
    assert len(opt['nodes'])<len(data['nodes'])
    for xx in range(256):assert evaluate(data,dict(x=xx))==evaluate(opt,dict(x=xx))


def test_adaptive_controller_on_exact_deterministic_phase():
    from research.controlled_source_completion.modern_mean import controller
    allocation=plan(.25,.002,.003)
    for mu in (-.49,-.01,0.,.01,.49):
        def measurements(stage,raw):
            left=raw/2**allocation['endpoint_bits'];theta=-2*math.atan((mu-left)/stage['normalizer'])
            k=round((theta%(2*math.pi))*stage['M']/(2*math.pi))%stage['M']
            return [k]*stage['repetitions']
        result=controller(allocation,measurements)
        assert abs(result['estimate']-mu)<=.002


def test_explicit_inverse_qft_gate_order():
    from research.controlled_source_completion.envelope import validate_qft
    validate_qft()


def test_machine_readable_reflection_sign_and_cleanup():
    from research.controlled_source_completion.envelope import controlled_U
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator
    source=dict(word_width=1,fraction_bits=0,values=3,resources=dict(logical_qubits=4),path='test-source',
                inputs=[dict(out=[j],params=dict(bits=1)) for j in range(3)])
    phase=dict(word_width=3,fraction_bits=0,values=3,resources=dict(logical_qubits=12),path='test-phase',
               inputs=[dict(out=[j],params=dict(name=name)) for j,name in enumerate(('Y','left','scale_exponent'))])
    wrapper=controlled_U(source,phase);ops=wrapper['operations'];first=next(j for j,op in enumerate(ops) if op['gate']=='h')
    ops=ops[first:];wiremap={x:i for i,x in enumerate(wrapper['random_wires'])}
    others=sorted({q for op in ops for q in op['wires'] if q!='control' and q not in wiremap})
    for q in others:wiremap[q]=len(wiremap)
    wiremap['control']=len(wiremap);qc=QuantumCircuit(len(wiremap))
    for op in ops:getattr(qc,op['gate'])(*[wiremap[q] for q in op['wires']])
    full=Operator(qc).data;indices=list(range(8))+list(range(32,40));block=full[np.ix_(indices,indices)]
    reflection=np.ones((8,8))/4-np.eye(8);expected=np.zeros((16,16));expected[:8,:8]=np.eye(8);expected[8:,8:]=reflection
    assert np.max(np.abs(block-expected))<1e-12
    assert np.max(np.abs(np.sum(np.abs(full[:,indices])**2,axis=0)-np.sum(np.abs(block)**2,axis=0)))<1e-12
