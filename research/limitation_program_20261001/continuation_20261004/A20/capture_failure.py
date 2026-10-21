"""Integrity-only retention of a failed A20 packet; it cannot certify science."""
import hashlib
import json
from pathlib import Path
import time
import traceback

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'results/limitation_program_20261001/A20_continuation_20261004_producer_run002'
OUT=ROOT/'results/limitation_program_20261001/A20_continuation_20261004_failure_capture_run001'
EXPECTED_PROTOCOL='4dd730a2a5af046c45dd68d25908111079fa200cbc0a7d42c30aa64e0cf00db7'
START=time.monotonic()
CPU_START=time.process_time()


def guard():
    if time.process_time()-CPU_START>120 or time.monotonic()-START>300:
        raise TimeoutError('Fixed metadata-only120CPU/300wall')


def sha(path):
    guard()
    before=path.stat()
    actual=path.resolve(strict=True)
    if actual!=path.absolute() or not actual.is_file():raise ValueError('Confined actual regular file required')
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1<<20):guard();h.update(chunk)
    after=path.stat()
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):raise ValueError('Changed input')
    return h.hexdigest()


def save(name,obj):
    data=(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
    if len(data)>8*1024**2:raise ValueError('Fixed8MiB per metadata artifact')
    with (OUT/name).open('xb') as stream:stream.write(data)


def main():
    assert ROOT==Path.cwd().resolve() and not OUT.exists()
    OUT.mkdir()
    save('protocol.json',{'scope':'Integrity-only failed-packet retention. Old FAILED_UNSEALED remains authoritative; no partial science approval.',
         'source':SOURCE.relative_to(ROOT).as_posix(),'expected_prepared_protocol_sha256':EXPECTED_PROTOCOL,
         'limits_CPU_wall_files_metadata_bytes':[120,300,16,33554432],
         'fixed_science_inventory':0,'new_test_credit':0,'stopping_rule':'One capture, two exact fresh unions; preserve failure on mismatch, no expected SHA replacement.'})
    try:
        protocol_path=SOURCE/'protocol.json'
        assert sha(protocol_path)==EXPECTED_PROTOCOL
        packet=json.loads(protocol_path.read_text())
        assert (SOURCE/'FAILED_UNSEALED.json').is_file() and not (SOURCE/'manifest.json').exists()
        error=json.loads((SOURCE/'failure.json').read_text())
        assert error['passed'] is False and error['message']=='Exact shared stock template; no unproved deduplication'
        initial={p.relative_to(SOURCE).as_posix():sha(p) for p in SOURCE.rglob('*') if p.is_file()}
        for k,e in packet['prepared_owned_files_protocol_self_hash_excluded'].items():assert initial[k]==e
        fixed={ROOT/k:e for k,e in packet['frozen_inputs'].items()}
        for k,e in packet['external_runtime_inputs'].items():
            p=Path(k);assert p not in fixed or fixed[p]==e;fixed[p]=e
        for k,e in initial.items():
            p=SOURCE/k;assert p not in fixed or fixed[p]==e;fixed[p]=e
        history={}
        here=Path(__file__).parent
        for name in ('producer_prepare_admission_failure001.json','producer_prepare_launch002.log','producer_prepare_launch003.log',
                     'producer_prepare_launch004.log','producer_run_launch001.log','ROOT_STATIC_REVIEW_v4.json','ROOT_STATIC_REVIEW_v4_corrected.json',
                     'authoring_failure001.json','PRODUCER_ROOT_READY_run001.json','PRODUCER_ROOT_READY_run002.json'):
            p=here/name;history[p.relative_to(ROOT).as_posix()]=sha(p);fixed[p]=history[p.relative_to(ROOT).as_posix()]
        passes=[]
        for _ in range(2):
            assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()}==set(initial)
            for p,e in fixed.items():assert sha(p)==e,(str(p),e)
            for name in packet['runtime_absent']:assert not Path(name).exists()
            assert (SOURCE/'FAILED_UNSEALED.json').exists() and not (SOURCE/'manifest.json').exists()
            passes.append({'paths':len(fixed),'bytes':sum(p.stat().st_size for p in fixed),'mismatches':0,'failed_source_inventory_exact':True})
        save('failed_source_owned_inventory.json',initial)
        save('failed_prepared_expected_maps.json',{'frozen_inputs':packet['frozen_inputs'],'external_runtime_inputs':packet['external_runtime_inputs'],'prepared_owned':packet['prepared_owned_files_protocol_self_hash_excluded']})
        save('launcher_history_sha256.json',history)
        result={'passed':True,'integrity_only':True,'original_scientific_attempt_passed':False,'original_failed_unsealed_authoritative':True,
                'original_hard_budget_state_uncertified':True,'actual_failure':error,'preserved_source_owned_files':len(initial),
                'prepared_owned_files_verified':len(packet['prepared_owned_files_protocol_self_hash_excluded']),
                'two_fresh_union_checks':passes,'new_test_credit':0,'gate_recipes_emitted':0,'component_checks_completed':0,
                'full_G2':False,'adoption':False,'quantum_advantage':False,
                'cpu_wall_observations':[time.process_time()-CPU_START,time.monotonic()-START]}
        guard();save('verification.json',result)
        owned={p.name:sha(p) for p in OUT.iterdir() if p.is_file()}
        save('manifest.json',{'files':owned,'frozen_inputs':{p.relative_to(ROOT).as_posix():e for p,e in fixed.items() if p.is_relative_to(ROOT)},
             'external_runtime_inputs':{str(p):e for p,e in fixed.items() if not p.is_relative_to(ROOT)},
             'passed':True,'integrity_only':True,'original_source_failed':True,'manifest_self_hash_excluded':True,'new_test_credit':0})
        guard();print(json.dumps(result))
    except BaseException as e:
        save('FAILED_UNSEALED.json',{'passed':False,'error':repr(e),'trace':traceback.format_exc(),'old_failure_unchanged':True,'new_test_credit':0})
        raise


if __name__=='__main__':main()
