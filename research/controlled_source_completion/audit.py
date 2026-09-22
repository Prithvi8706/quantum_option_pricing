"""Independent count/hash reconciliation of the emitted hierarchical artifacts."""
import json
import hashlib
from pathlib import Path
import numpy as np
from collections import Counter
from research.controlled_source_completion.run import ROOT,dump
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.compiler import resolve_library


def main():
    cache={};rows=[]
    for tag in ('C4_f24','H8_f24','C4_f40','H8_f40','phase_f64'):
        root=ROOT/'compile_v2'/tag;manifest=json.loads((root/'source.json').read_text());w=manifest['word_width'];counts=np.zeros(3,dtype=np.int64)
        lib=resolve_library(manifest)
        for call in manifest['forward_calls']:
            key=(str(lib),call['leaf'])
            if key not in cache:
                entry=json.loads((lib/(call['leaf']+'.json')).read_text());file=lib/entry['gate_file'];gates=np.load(file,mmap_mode='r')
                digest=hashlib.sha256(file.read_bytes()).hexdigest();assert digest==entry['sha256']
                cc=np.bincount(gates[:,0],minlength=4)[1:4];assert int(cc.sum())==entry['resources']['source_gates']
                assert int(cc[2])*7==entry['resources']['t_count'];assert np.all((1<=gates[:,0])&(gates[:,0]<=3))
                for kind in (1,2,3):
                    active=gates[gates[:,0]==kind,1:1+kind]
                    assert np.all(active>=0) and np.all(active<entry['resources']['qubits'])
                    if kind>=2:assert np.all(active[:,0]!=active[:,1])
                    if kind==3:assert np.all(active[:,0]!=active[:,2]) and np.all(active[:,1]!=active[:,2])
                cache[key]=dict(counts=cc,sha256=digest,bytes=file.stat().st_size)
            counts+=cache[key]['counts'];counts[1]+=call['argument_copy_cx']
        counts*=2;counts[1]+=len(manifest['outputs'])*w
        r=manifest['resources'];assert list(map(int,counts))==[r['x'],r['cx'],r['ccx']]
        assert int(counts.sum())==r['source_gates'];assert int(counts[2])*7==r['t_count']
        row=dict(tag=tag,source_gates=int(counts.sum()),t_count=int(counts[2])*7,unique_leaves=len(manifest['library_keys']),
                 source_sha256=hashlib.sha256((root/'source.json').read_bytes()).hexdigest(),
                 target_sha256=hashlib.sha256((root/'target.json').read_bytes()).hexdigest())
        if tag!='phase_f64':
            old=json.loads((ROOT/'compile_v1'/tag/'target.json').read_text());new=json.loads((root/'target.json').read_text())
            rng=np.random.default_rng(2026092603);cases=16
            for _ in range(cases):
                inputs={n['params']['name']:int(rng.integers(0,2**n['params']['bits'])) for n in old['nodes'] if n['op']=='input'}
                assert evaluate(old,inputs)==evaluate(new,inputs)
            row['optimizer_paired_cases']=cases
        rows.append(row)
    wrappers=[]
    costfile=ROOT/'cost_v3_phase64'/'ledger.json'
    if not costfile.exists():costfile=ROOT/'cost_v2_phase64'/'ledger.json'
    if costfile.exists():
        ledger=json.loads(costfile.read_text());phase=json.loads((ROOT/'compile_v2'/'phase_f64'/'source.json').read_text())['resources']
        for row in ledger:
            if row['mode']!='continuous_moment_conditional':continue
            tag='%s_f%d'%(row['model'],row['f']);wrapper=json.loads((costfile.parent/(tag+'_controlled_U_gates.json')).read_text())
            source=json.loads((ROOT/'compile_v2'/tag/'source.json').read_text())['resources'];counts=Counter(op['gate'] for op in wrapper['operations'])
            fused=wrapper.get('fused_compute_phase_uncompute',False);factor=1 if fused else 2
            assert counts['call_graph_half' if fused else 'call_clean_hierarchy']==4 and counts['cp']==row['single_U']['controlled_bit_phases']
            removed_copies=(row['f']+32+96) if fused else 0
            assert factor*source['t_count']+factor*phase['t_count']+7*counts['ccx']==row['single_U']['t_count']
            assert factor*source['clifford_cx']+factor*phase['clifford_cx']+6*counts['ccx']+counts['cx']+counts['cz']-removed_copies==row['single_U']['clifford_cx']
            assert factor*source['clifford_h']+factor*phase['clifford_h']+2*counts['ccx']+counts['h']+2*counts['cz']==row['single_U']['clifford_h']
            for op in wrapper['operations']:
                if 'wires' in op:
                    assert len(set(op['wires']))==len(op['wires'])
                    assert all(q=='control' or 0<=q<wrapper['qpe_register_base'] for q in op['wires'])
            wrappers.append(dict(tag=tag,counts=dict(counts),matches_ledger=True))
    dump(ROOT/'validation_v2'/'resource_reconciliation.json',dict(rows=rows,controlled_U_wrappers=wrappers,unique_leaf_files=len(cache),
        unique_gate_library_bytes=sum(c['bytes'] for c in cache.values()),
        method='Independent NumPy gate-kind counts, wire checks and SHA256; composed copy/forward/inverse counts; no analytic operation-count oracle substituted for emitted gates.'))
    print(json.dumps(dict(sources=len(rows),wrappers=len(wrappers),unique_leaves=len(cache),all_counts_agree=True)),flush=True)


if __name__=='__main__':main()
