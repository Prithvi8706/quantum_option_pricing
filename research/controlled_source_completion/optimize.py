"""Bit-exact constant folding and common-expression reuse before compilation."""
import json
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.finance import prune


def optimize(data):
    w=data['width'];mask=(1<<w)-1;nodes=[];mapping={};known={};seen={};values=0;folded=0;reused=0
    for n in data['nodes']:
        op=n['op'];args=[mapping[i] for i in n['args']];params=n['params'];outs=n['out']
        if op in ('add','mul'):args.sort()
        if op not in ('input','const') and all(i in known for i in args):
            # Use the independently tested integer semantics, including wraparound.
            miniature=[dict(op='input',args=[],params=dict(name=str(j),bits=w),out=[j]) for j in range(len(args))]
            miniature.append(dict(op=op,args=list(range(len(args))),params=params,out=list(range(len(args),len(args)+len(outs)))))
            small=dict(data,nodes=miniature,outputs={},inputs=list(range(len(args))))
            _,trace=evaluate(small,{str(j):known[a] for j,a in enumerate(args)},True)
            constants=trace[len(args):];folded+=1
        elif op=='const':constants=[int(params['value'])&mask]
        else:constants=None
        if constants is not None:
            for old,raw in zip(outs,constants):
                key=('const',int(raw)&mask)
                if key not in seen:
                    seen[key]=(values,);known[values]=key[1]
                    nodes.append(dict(op='const',args=[],params=dict(value=key[1]),out=[values]));values+=1
                else:reused+=1
                mapping[old]=seen[key][0]
            continue
        alias=None
        if op=='add':
            if known.get(args[0])==0:alias=args[1]
            elif known.get(args[1])==0:alias=args[0]
        elif op=='sub' and known.get(args[1])==0:alias=args[0]
        elif op=='select' and args[1]==args[2]:alias=args[1]
        elif op=='cmul' and params['c']==2**data['fraction_bits']:alias=args[0]
        elif op=='bits' and params['shift']==0 and params['width']==w:alias=args[0]
        if alias is not None:mapping[outs[0]]=alias;reused+=1;continue
        key=(op,tuple(args),json.dumps(params,sort_keys=True))
        if key in seen and op!='input':newouts=seen[key];reused+=1
        else:
            newouts=tuple(range(values,values+len(outs)));values+=len(outs);seen[key]=newouts
            nodes.append(dict(op=op,args=args,params=params,out=list(newouts)))
        mapping.update(zip(outs,newouts))
    result=dict(data,nodes=nodes,inputs=[mapping[i] for i in data['inputs']],outputs={k:mapping[v] for k,v in data['outputs'].items()})
    result=prune(result,list(result['outputs']))
    result['optimization']=dict(original_nodes=len(data['nodes']),final_nodes=len(result['nodes']),constant_folded_nodes=folded,reused_nodes=reused,
        semantics='Exact integer constant folding and common-subexpression reuse; no change to input law, output or finite arithmetic.')
    return result


def main():
    from research.controlled_source_completion.run import ROOT,dump
    from research.controlled_source_completion.compiler import compile_graph
    from research.controlled_source_completion.primitives import Library
    import time
    rows=[]
    for f in (24,40):
        lib=Library(ROOT/'compile_v1'/('leaves_f%d'%f),f+32,f,{})
        for name in ('C4','H8','phase'):
            tic=time.perf_counter();target=ROOT/'compile_v1'/('%s_f%d'%(name,f))/'target.json'
            data=optimize(json.loads(target.read_text()));manifest,lib=compile_graph(data,ROOT/'compile_v2'/('%s_f%d'%(name,f)),lib)
            row=dict(model=name,f=f,optimization=data['optimization'],resources=manifest['resources'],seconds=time.perf_counter()-tic)
            rows.append(row);print(json.dumps(row),flush=True);dump(ROOT/'compile_v2'/'summary.json',rows)


if __name__=='__main__':main()
