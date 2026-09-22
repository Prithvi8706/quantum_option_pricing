"""Emitted clean XOR arithmetic leaves, with no arithmetic oracle placeholders."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from numba import njit
from research.journal_sprint.reversible_fixed_point import (
    Program,copy,constant,add,subtract,fixed_multiply,less_than,positive_part)
from research.antithetic_feasibility.reversible import constant_product,clean_sqrt


def compare(p,a,b,flag):
    less_than(p,a,b,flag,p.register(len(a)+1),p.register(len(a)+1),p.register(1)[0])


def select(p,flag,a,b,out):
    for x,y,z in zip(a,b,out):
        p.gate(y,z)
        p.gate(flag,z) if x==flag else p.gate(flag,x,z)
        p.gate(flag,z) if y==flag else p.gate(flag,y,z)


def divide(p,a,b,out,f):
    """Restoring unsigned division of a*2**f by b; zero divisor gives all ones."""
    w=len(a);rw=w+1;steps=w+f
    remainders=[p.register(rw) for _ in range(steps+1)]
    divisor=p.register(rw);conditional=p.register(rw);quotient=p.register(steps)
    diff=p.register(rw+1);ext=p.register(rw+1);helper=p.register(1)[0]
    start=len(p.gates);copy(p,b,divisor[:w])
    for stage,j in enumerate(reversed(range(steps))):
        prev,nxt=remainders[stage:stage+2]
        for k in range(w):p.gate(prev[k],nxt[k+1])
        if f<=j<f+w:p.gate(a[j-f],nxt[0])
        less_than(p,nxt,divisor,quotient[j],diff,ext,helper);p.gate(quotient[j])
        for k in range(rw):p.gate(quotient[j],divisor[k],conditional[k])
        subtract(p,conditional,nxt,helper)
        for k in range(rw):p.gate(quotient[j],divisor[k],conditional[k])
    end=len(p.gates);copy(p,quotient[:w],out);p.undo(start,end)


def highest_bit(p,x,out):
    w=len(x);seen=p.register(w+1);highest=p.register(w);start=len(p.gates)
    for i in reversed(range(w)):
        p.gate(seen[i+1],seen[i]);p.gate(x[i],seen[i]);p.gate(seen[i+1],x[i],seen[i])
        p.gate(seen[i+1]);p.gate(seen[i+1],x[i],highest[i]);p.gate(seen[i+1])
    end=len(p.gates)
    for i in range(w):
        for j in range(i.bit_length()):
            if (i>>j)&1:p.gate(highest[i],out[j])
    p.undo(start,end)


def variable_shift(p,x,k,out):
    w=len(x);helper=p.register(1)[0];neg=p.register(w);one=p.register(w);mag=p.register(w)
    start=len(p.gates)
    copy(p,k,neg)
    for bit in neg:p.gate(bit)
    constant(p,one,1);add(p,one,neg,helper);constant(p,one,1)
    select(p,k[-1],neg,k,mag)
    left=x;right=x
    for j in range((w-1).bit_length()):
        distance=1<<j;ll=p.register(w);rr=p.register(w)
        for z in range(w):
            p.gate(left[z],ll[z]);p.gate(mag[j],left[z],ll[z])
            if z>=distance:p.gate(mag[j],left[z-distance],ll[z])
            p.gate(right[z],rr[z]);p.gate(mag[j],right[z],rr[z])
            p.gate(mag[j],right[min(z+distance,w-1)],rr[z])
        left,right=ll,rr
    limit=p.register(w);small=p.register(1)[0];chosen=p.register(w)
    constant(p,limit,w);compare(p,mag,limit,small);select(p,k[-1],right,left,chosen)
    end=len(p.gates)
    for bit,target in zip(chosen,out):p.gate(small,bit,target)
    # Oversized arithmetic right shift gives the sign, oversized left gives zero.
    large_negative=p.register(1)[0];negative=p.register(1)[0]
    p.gate(k[-1],x[-1],negative);p.gate(small)
    p.gate(small,negative,large_negative)
    for target in out:p.gate(large_negative,target)
    p.gate(small,negative,large_negative);p.gate(small);p.gate(k[-1],x[-1],negative)
    p.undo(start,end)


def mcx(p,controls,target,scratch):
    if len(controls)<3:p.gate(*controls,target);return
    p.gate(controls[0],controls[1],scratch[0])
    for i in range(2,len(controls)-1):p.gate(scratch[i-2],controls[i],scratch[i-1])
    p.gate(scratch[len(controls)-3],controls[-1],target)
    for i in reversed(range(2,len(controls)-1)):p.gate(scratch[i-2],controls[i],scratch[i-1])
    p.gate(controls[0],controls[1],scratch[0])


def lookup(p,address,outs,table,bits):
    flag=p.register(1)[0];scratch=p.register(max(1,bits-2));controls=address[:bits]
    for i,row in enumerate(table):
        for j in range(bits):
            if not ((i>>j)&1):p.gate(controls[j])
        mcx(p,controls,flag,scratch)
        for out,value in zip(outs,row):
            for j,wire in enumerate(out):
                if (int(value)>>j)&1:p.gate(flag,wire)
        mcx(p,controls,flag,scratch)
        for j in range(bits):
            if not ((i>>j)&1):p.gate(controls[j])


def build(op,w,f,params=None,table=None):
    params=params or {};arity={'const':0,'add':2,'sub':2,'mul':2,'cmul':1,'lt':2,
        'select':3,'positive':1,'divide':2,'sqrt':1,'msb':1,'shift':2,'bits':1,'lookup':1}[op]
    nout=len(table[0]) if op=='lookup' else 1
    p=Program(compact=True);args=[p.register(w) for _ in range(arity)];outs=[p.register(w) for _ in range(nout)]
    if op=='const':constant(p,outs[0],int(params['value']))
    elif op in ('add','sub'):
        work=p.register(w);helper=p.register(1)[0];start=len(p.gates);copy(p,args[0],work)
        (add if op=='add' else subtract)(p,args[1],work,helper)
        end=len(p.gates);copy(p,work,outs[0]);p.undo(start,end)
    elif op=='mul':fixed_multiply(p,*args,outs[0],f,p.register(2*w),p.register(2*w),p.register(1)[0])
    elif op=='cmul':constant_product(p,args[0],outs[0],int(params['c']),f)
    elif op=='lt':
        for a in args:p.gate(a[-1])
        compare(p,*args,outs[0][0])
        for a in args:p.gate(a[-1])
    elif op=='select':select(p,args[0][0],args[1],args[2],outs[0])
    elif op=='positive':positive_part(p,args[0],outs[0])
    elif op=='divide':divide(p,*args,outs[0],f)
    elif op=='sqrt':clean_sqrt(p,args[0],outs[0],f)
    elif op=='msb':highest_bit(p,args[0],outs[0])
    elif op=='shift':variable_shift(p,*args,outs[0])
    elif op=='bits':
        for j,target in enumerate(outs[0][:params['width']]):
            source=j+params['shift']
            if 0<=source<w:p.gate(args[0][source],target)
            elif source>=w and params.get('signed'):p.gate(args[0][-1],target)
    elif op=='lookup':lookup(p,args[0],outs,table,params['bits'])
    return p,args,outs


@njit(cache=True)
def run_gates(gates,bits,inverse=False):
    for jj in range(len(gates)):
        j=len(gates)-1-jj if inverse else jj
        kind,a,b,c=gates[j]
        if kind==1:bits[a]^=1
        elif kind==2:bits[b]^=bits[a]
        else:bits[c]^=bits[a]&bits[b]
    return bits


@njit(cache=True)
def gate_resources(gates,qubits):
    levels=np.zeros(qubits,np.int64);depth=np.zeros(qubits,np.int64);counts=np.zeros(3,np.int64)
    for gate in gates:
        kind,a,b,c=gate;counts[kind-1]+=1
        if kind==1:depth[a]+=1
        elif kind==2:
            t=max(levels[a],levels[b]);d=max(depth[a],depth[b])+1
            levels[a]=t;levels[b]=t;depth[a]=d;depth[b]=d
        else:
            # Exact seven-T decomposition used elsewhere in this repository.
            wires=((c,c),(b,c),(c,c),(a,c),(c,c),(b,c),(c,c),(a,c),(b,b),(c,c),(c,c),(a,b),(a,a),(b,b),(a,b))
            for j in range(15):
                aa,bb=wires[j];ist=j in (2,4,6,8,9,12,13)
                t=max(levels[aa],levels[bb])+int(ist);d=max(depth[aa],depth[bb])+1
                levels[aa]=t;levels[bb]=t;depth[aa]=d;depth[bb]=d
    return counts,levels.max(),depth.max()


def array_gates(p):return np.frombuffer(p.gates.data,dtype=np.int32).reshape(-1,4)


def resources(p):
    counts,td,depth=gate_resources(array_gates(p),p.qubits);x,cx,ccx=map(int,counts)
    return dict(qubits=p.qubits,source_gates=len(p.gates),x=x,cx=cx,ccx=ccx,
                t_count=7*ccx,t_depth=int(td),clifford_t_depth=int(depth),
                clifford_cx=cx+6*ccx,clifford_h=2*ccx,
                schedule='exact seven-T Toffoli; all-to-all ASAP within each leaf')


def basis_run(p,args,outs,values,output_values=None,inverse=False):
    bits=np.zeros(p.qubits,dtype=np.uint8)
    for reg,value in zip(args,values):
        for j,wire in enumerate(reg):bits[wire]=(int(value)>>j)&1
    for reg,value in zip(outs,output_values or [0]*len(outs)):
        for j,wire in enumerate(reg):bits[wire]=(int(value)>>j)&1
    before=bits.copy();run_gates(array_gates(p),bits,inverse)
    values_out=[sum(int(bits[wire])<<j for j,wire in enumerate(reg)) for reg in outs]
    occupied={wire for reg in args+outs for wire in reg}
    clean=all(bits[j]==0 for j in range(p.qubits) if j not in occupied)
    preserved=all(bits[wire]==before[wire] for reg in args for wire in reg)
    return values_out,clean,preserved,bits


class Library:
    def __init__(self,path,w,f,tables):
        self.path=Path(path);self.path.mkdir(parents=True,exist_ok=True)
        self.w=w;self.f=f;self.tables=tables;self.entries={}
    def get(self,node):
        op=node['op'];params=node['params'];table=self.tables.get(params.get('table'))
        spec=dict(op=op,width=self.w,fraction_bits=self.f,params=params,table=table)
        key=hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':')).encode()).hexdigest()[:20]
        if key not in self.entries:
            meta=self.path/(key+'.json');binary=self.path/(key+'.npy')
            if meta.exists() and binary.exists():entry=json.loads(meta.read_text())
            else:
                p,args,outs=build(op,self.w,self.f,params,table)
                np.save(binary,array_gates(p));entry=dict(key=key,op=op,params=params,
                    args=[list(a) for a in args],outs=[list(o) for o in outs],resources=resources(p),
                    gate_file=binary.name,sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                    table_bits=0 if table is None else len(table)*len(table[0])*self.w)
                meta.write_text(json.dumps(entry,indent=2)+'\n')
            self.entries[key]=entry
        return key,self.entries[key]
