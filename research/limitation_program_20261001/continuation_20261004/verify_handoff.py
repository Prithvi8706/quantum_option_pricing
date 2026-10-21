"""Fresh independent SHA/inventory verification; no scientific module imports."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

ROOT = Path(__file__).resolve().parents[3]
START = time.monotonic()
CPU_START = time.process_time()


def guard():
    if time.process_time()-CPU_START > 120 or time.monotonic()-START > 300:
        raise TimeoutError('Fixed integrity-only120CPU/300wall cap')


def read_sha(path):
    guard()
    lexical=Path(path).absolute()
    actual=lexical.resolve(strict=True)
    if lexical!=actual or not actual.is_file():
        raise ValueError('Alias/nonfile input:'+str(path))
    before=actual.stat()
    state=hashlib.sha256()
    with actual.open('rb') as stream:
        while chunk:=stream.read(1<<20):
            guard();state.update(chunk)
    after=actual.stat()
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
        raise ValueError('Input changed during fresh SHA:'+str(path))
    return state.hexdigest(),before.st_size


def new_json(path,obj):
    with path.open('x',encoding='utf-8') as stream:
        json.dump(obj,stream,indent=2,sort_keys=True);stream.write('\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    source=(ROOT/args.source).resolve(strict=True)
    out=(ROOT/args.out).resolve(strict=False)
    assert source.is_relative_to(ROOT/'results/limitation_program_20261001')
    assert out.parent==ROOT/'results/limitation_program_20261001' and not out.exists()
    out.mkdir()
    protocol={'scope':'Independent byte/inventory integrity only; no arithmetic/financial theorem or runtime completeness certification.',
              'source':args.source,'manifest_sha256':args.manifest_sha256,'cpu_wall_caps':[120,300],
              'acceptance':'Exact supplied manifest hash, exact observed owned inventory, every canonical unique owned/frozen/external expected SHA, no authoritative failure marker, two uncached fresh passes.',
              'stop_rule':'One fixed source, no retries/waivers/partial promotion; failures retained.',
              'controller_sha256':read_sha(Path(__file__))[0],'new_test_credit':0}
    new_json(out/'protocol.json',protocol)
    try:
        manifest=source/'manifest.json'
        if read_sha(manifest)[0]!=args.manifest_sha256:raise ValueError('Supplied source manifest pin mismatch')
        obj=json.loads(manifest.read_text(encoding='utf-8'))
        union={manifest:args.manifest_sha256}
        expected_owned={manifest}
        def add(path,value):
            if isinstance(value,dict):value=value['sha256']
            if not isinstance(value,str) or len(value)!=64:raise ValueError('Exact expected SHA required')
            path=Path(path).absolute()
            if path in union and union[path]!=value:raise ValueError('Conflicting canonical expectation')
            union[path]=value
        if 'files' in obj:
            for name,value in obj['files'].items():
                path=source/name
                if not path.resolve(strict=True).is_relative_to(source):raise ValueError('Owned path escapes source')
                add(path,value);expected_owned.add(path.absolute())
        elif 'owned_files' in obj:
            for name,value in obj['owned_files'].items():
                path=ROOT/name
                if not path.resolve(strict=True).is_relative_to(source):raise ValueError('Owned path escapes source')
                add(path,value);expected_owned.add(path.absolute())
        else:raise ValueError('Unknown owned map format')
        for field in ('frozen_inputs','external_runtime_inputs'):
            for name,value in obj.get(field,{}).items():
                path=Path(name) if Path(name).is_absolute() else ROOT/name
                add(path,value)
        passes=[]
        for _ in range(2):
            guard()
            if any((source/name).exists() for name in ('FAILED_UNSEALED.json','FAILED.json','failure.json','run_failure.json','prepare_failure.json')):
                raise ValueError('Failed source cannot receive integrity release')
            observed={p.absolute() for p in source.rglob('*') if p.is_file()}
            if observed!=expected_owned:raise ValueError('Exact source-owned inventory mismatch')
            total=0
            for path,expected in union.items():
                actual,size=read_sha(path)
                if actual!=expected:raise ValueError('Fresh SHA mismatch:'+str(path))
                total+=size
                if total>8*1024**3:raise MemoryError('Unique8GiB input cap')
            if read_sha(manifest)[0]!=args.manifest_sha256:raise ValueError('Source manifest changed')
            passes.append({'fresh_unique_paths':len(union),'fresh_unique_bytes':total,'sha_mismatches':0,'inventory_exact':True})
        result={'passed':True,'completed':True,'budget_censored':False,'source_manifest_sha256':args.manifest_sha256,
                'scope':protocol['scope'],'two_uncached_fresh_passes':passes,'new_test_credit':0,
                'financial_source_adoption':False,'full_G2':False,'quantum_advantage':False,
                'administrative_cpu_seconds':time.process_time()-CPU_START,'administrative_wall_seconds':time.monotonic()-START}
        guard();new_json(out/'verification.json',result)
        owned={p.name:read_sha(p)[0] for p in out.iterdir() if p.is_file()}
        guard();new_json(out/'manifest.json',{'files':owned,'frozen_inputs':{str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):v for p,v in union.items()},'manifest_self_hash_excluded':True,'integrity_only':True,'passed':True,'new_test_credit':0})
        guard();print(json.dumps(result))
    except BaseException as error:
        new_json(out/'FAILED_UNSEALED.json',{'passed':False,'source_approval':False,'error':repr(error),'trace':traceback.format_exc(),'new_test_credit':0})
        raise


if __name__=='__main__':main()
