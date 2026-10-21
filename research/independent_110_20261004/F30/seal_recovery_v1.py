"""Exact-byte metadata seal recovery; does not execute scientific work."""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[3]
OLD=ROOT/'results/independent_110_20261004/F30/run002'
OUT=ROOT/'results/independent_110_20261004/F30/seal_recovery_run001'
SCIENCE_INPUTS=[
    'research/release_checks/targets.py',
    'research/journal_sprint/asian_basket.py',
    'research/independent_110_20261004/F30/primary_sources/Sakurai_Takahashi_Miyamoto_2405_00701v1.html',
    'research/independent_110_20261004/F30/rank_screen_v2.py',
    'docs/independent_110_20261004/F30/ASSUMPTIONS_run002.txt',
    'research/independent_110_20261004/F30/corpus_run002/fixed_data.npz']
OLD_NAMES=['ATTEMPT.json','SUCCESS.json','manifest.json','protocol.json',
    'rank_2_cores.npz','rank_4_cores.npz','rank_8_cores.npz','summary.json','training_and_validation.npz']
INPUTS=SCIENCE_INPUTS+['results/independent_110_20261004/F30/run002/'+n for n in OLD_NAMES]+[
    'docs/independent_110_20261004/F30/SEAL_FAILURE_run002.json',
    'docs/independent_110_20261004/F30/STATIC_REVIEW_run002.json',
    'docs/independent_110_20261004/F30/SEAL_ASSUMPTIONS_run001.txt',
    'research/independent_110_20261004/F30/seal_recovery_v1.py']
CAPS=dict(cpu_seconds=2,wall_seconds=10,input_bytes=2*1024**2,output_bytes=128*1024,output_files=8)

def sha(b):return hashlib.sha256(b).hexdigest()
def encoded(data):return (json.dumps(data,indent=2,sort_keys=True)+'\n').encode('utf-8')
def record(path):
    p=ROOT/path;b=p.read_bytes()
    return dict(path=path,bytes=len(b),sha256=sha(b))
def write(name,data):
    p=OUT/name
    if p.exists():raise ValueError('Refuse overwrite')
    p.write_bytes(encoded(data))
def prepare():
    if OUT.exists():raise ValueError('Fresh recovery output required')
    OUT.mkdir(parents=True)
    corpus=[record(p) for p in INPUTS];size=sum(r['bytes'] for r in corpus)
    if size>CAPS['input_bytes']:raise ValueError('Frozen input cap')
    write('protocol.json',dict(corpus=corpus,corpus_bytes=size,budgets=CAPS,
        scientific_invocations=0,kind='metadata_only_seal_recovery',
        acceptance='Actual raw output bytes plus retained original failed manifest; no new scientific credit'))
    print(json.dumps(dict(prepared=True,files=len(corpus),bytes=size,protocol_sha256=sha((OUT/'protocol.json').read_bytes()))))
def run():
    if (OUT/'ATTEMPT.json').exists():raise ValueError('One recovery invocation only')
    p=json.loads((OUT/'protocol.json').read_text());cpu=time.process_time();wall=time.monotonic()
    write('ATTEMPT.json',dict(kind='metadata_only',scientific_invocations=0))
    def guard():
        if time.process_time()-cpu>CAPS['cpu_seconds'] or time.monotonic()-wall>CAPS['wall_seconds']:raise ValueError('Recovery budget cap')
    def check_frozen():
        for r in p['corpus']:
            if record(r['path'])!=r:raise ValueError('Frozen input changed')
        guard()
    try:
        if p['budgets']!=CAPS or [r['path'] for r in p['corpus']]!=INPUTS or p['scientific_invocations']!=0:raise ValueError('Recovery protocol changed')
        if p['corpus_bytes']!=sum(r['bytes'] for r in p['corpus']) or p['corpus_bytes']>CAPS['input_bytes']:raise ValueError('Recovery corpus cap')
        check_frozen()
        if {f.name for f in OLD.iterdir()}!=set(OLD_NAMES):raise ValueError('Original output membership changed')
        failure=json.loads((ROOT/'docs/independent_110_20261004/F30/SEAL_FAILURE_run002.json').read_text())
        if sha((OLD/'manifest.json').read_bytes())!=failure['original_manifest_sha256'] or sha((OLD/'summary.json').read_bytes())!=failure['original_summary_sha256']:raise ValueError('Original failure binding changed')
        old_manifest=json.loads((OLD/'manifest.json').read_text())
        if {r['path'] for r in old_manifest['files']}!=set(OLD_NAMES)-{'manifest.json'} or len(old_manifest['files'])!=8:raise ValueError('Original manifest membership changed')
        mismatches=[]
        for r in old_manifest['files']:
            b=(OLD/r['path']).read_bytes();actual_sha=sha(b)
            if len(b)!=r['bytes'] or actual_sha!=r['sha256']:
                mismatches.append(dict(path=r['path'],recorded_bytes=r['bytes'],actual_bytes=len(b),recorded_sha256=r['sha256'],actual_sha256=actual_sha))
        if mismatches!=failure['mismatches'] or [r['path'] for r in mismatches]!=['SUCCESS.json']:raise ValueError('Mismatch outside declared newline defect')
        success=(OLD/'SUCCESS.json').read_bytes()
        if sha(success.replace(b'\r\n',b'\n'))!=mismatches[0]['recorded_sha256']:raise ValueError('Not solely newline translation')
        science=json.loads((OLD/'protocol.json').read_text())
        if [r['path'] for r in science['corpus']]!=SCIENCE_INPUTS:raise ValueError('Original science input membership changed')
        for r in science['corpus']:
            if record(r['path'])!=r:raise ValueError('Original frozen science input changed')
        external=[record('results/independent_110_20261004/F30/run002/'+n) for n in OLD_NAMES]
        write('summary.json',dict(status='PASS_METADATA_ONLY_EXACT_BYTE_RECOVERY',external_artifacts=external,
            original_manifest_valid=False,retained_mismatches=mismatches,scientific_invocations=0,
            scientific_reruns=0,new_scientific_credit=False,full_F30_acceptance=False))
        check_frozen()
        write('SUCCESS.json',dict(status='PASS_METADATA_ONLY_EXACT_BYTE_RECOVERY',scientific_invocations=0,full_F30_acceptance=False))
        files=sorted(f for f in OUT.iterdir() if f.is_file())
        owned=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in files]
        manifest=dict(files=owned,external_artifacts=external,provenance='Original failed LF-planned seal retained; actual bytes recovered without science execution',scientific_invocations=0)
        if len(files)+1>CAPS['output_files'] or sum(f.stat().st_size for f in files)+len(encoded(manifest))>CAPS['output_bytes']:raise ValueError('Recovery output cap')
        guard();write('manifest.json',manifest)
        print(json.dumps(dict(status='PASS_METADATA_ONLY_EXACT_BYTE_RECOVERY',manifest_sha256=sha((OUT/'manifest.json').read_bytes()),scientific_invocations=0)))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():write('FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc),scientific_invocations=0))
        raise
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','run']);mode=a.parse_args().mode
    prepare() if mode=='prepare' else run()
