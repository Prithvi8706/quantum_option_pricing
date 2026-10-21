"""Retain the complete failed independent attempt; no science or retry."""
import hashlib
import json
from pathlib import Path
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'results/limitation_program_20261001/A20_continuation_20261004_audit_run004'
OUT = ROOT / 'results/limitation_program_20261001/A20_continuation_20261004_audit_failure_capture_run001'
EXPECTED = '8e7262889645d39f6d80e5cb46a1bf93957f4f351298643ce7c99f4b6776af9f'
CPU, WALL = time.process_time(), time.monotonic()


def guard():
    assert time.process_time() - CPU < 120 and time.monotonic() - WALL < 300


def sha(path):
    guard()
    assert path.resolve(strict=True) == path.absolute() and path.is_file()
    before = path.stat()
    state = hashlib.sha256()
    with path.open('rb') as stream:
        while blob := stream.read(1024 * 1024):
            guard()
            state.update(blob)
    after = path.stat()
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns) == (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    return state.hexdigest()


def save(name, obj):
    guard()
    data = (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode()
    assert len(data) < 8 * 1024**2
    existing = [p for p in OUT.iterdir() if p.is_file()]
    assert len(existing) + 1 <= 16 and sum(p.stat().st_size for p in existing) + len(data) + 16384 <= 33554432
    with (OUT / name).open('xb') as stream:
        stream.write(data)


def emergency(obj):
    # This bounded emergency marker must remain writable after a spent guard.
    data = (json.dumps(obj, sort_keys=True) + '\n').encode()
    assert len(data) < 16384
    with (OUT / 'FAILED_UNSEALED.json').open('wb') as stream:
        stream.write(data)


def join(mapping, path, expected):
    assert path not in mapping or mapping[path] == expected
    mapping[path] = expected


def main():
    assert ROOT == Path.cwd().resolve() and not OUT.exists()
    preflight = HERE / 'AUDIT_FAILURE_CAPTURE_PREFLIGHT_run001.json'
    policy = json.loads(preflight.read_text())
    assert policy['expected_prepared_protocol_sha256'] == EXPECTED
    OUT.mkdir()
    emergency({'passed':False,'unfinished_capture':True,'original_failure_unchanged':True,
               'capture_hard_budget_state_uncertified':True,'new_test_credit':0})
    save('protocol.json', policy | {'preflight_sha256':sha(preflight), 'controller_sha256':sha(Path(__file__))})
    try:
        assert sha(SOURCE / 'protocol.json') == EXPECTED
        protocol_bytes = (SOURCE / 'protocol.json').read_bytes()
        marker_bytes = (SOURCE / 'FAILED_UNSEALED.json').read_bytes()
        error_bytes = (SOURCE / 'failure.json').read_bytes()
        assert hashlib.sha256(protocol_bytes).hexdigest() == EXPECTED
        packet = json.loads(protocol_bytes)
        marker = json.loads(marker_bytes)
        error = json.loads(error_bytes)
        assert marker['authoritative_failure'] is True and marker['hard_budget_state_uncertified'] is True
        assert marker['budget_censored'] is None and error['message'] == 'Fixed A20 process CPU/wall guard'
        assert not (SOURCE / 'manifest.json').exists()
        initial = {p.relative_to(SOURCE).as_posix():sha(p) for p in SOURCE.rglob('*') if p.is_file()}
        assert initial['protocol.json'] == EXPECTED
        assert initial['FAILED_UNSEALED.json'] == hashlib.sha256(marker_bytes).hexdigest()
        assert initial['failure.json'] == hashlib.sha256(error_bytes).hexdigest()
        group_names = ('independent_source_binding.json','independent_native_truth.json',
                       'independent_component_checks.json','independent_counting_and_structural_proof.json',
                       'independent_resource_ledger.json','summary.json','completion_outcome.json','manifest.json')
        assert all(name not in initial for name in group_names)
        prepared = packet['prepared_owned_files_protocol_self_hash_excluded']
        assert all(initial[k] == e for k,e in prepared.items())
        fixed = {}
        for k,e in packet['frozen_inputs'].items():
            join(fixed, ROOT / k, e)
        for k,e in packet['external_runtime_inputs'].items():
            join(fixed, Path(k), e)
        for k,e in initial.items():
            join(fixed, SOURCE / k, e)
        history = {}
        for path in (preflight, Path(__file__), HERE / 'AUDIT_ROOT_READY_run004.json',
                     HERE / 'audit_prepare_run004_launch001.log', HERE / 'audit_run004_launch001.log'):
            expected = sha(path)
            history[path.relative_to(ROOT).as_posix()] = expected
            join(fixed, path, expected)
        passes = []
        for _ in range(2):
            guard()
            assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()} == set(initial)
            total = 0
            for path, expected in fixed.items():
                assert sha(path) == expected, str(path)
                total += path.stat().st_size
                assert total < 8 * 1024**3
            assert all(not Path(p).exists() for p in packet['runtime_absent'])
            assert (SOURCE / 'FAILED_UNSEALED.json').exists() and not (SOURCE / 'manifest.json').exists()
            assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()} == set(initial)
            passes.append({'paths':len(fixed),'bytes':total,'mismatches':0,'failed_source_inventory_exact':True})
        save('failed_source_owned_inventory.json', initial)
        save('failed_prepared_expected_maps.json', {'frozen_inputs':packet['frozen_inputs'],
             'external_runtime_inputs':packet['external_runtime_inputs'],'prepared_owned':prepared})
        save('launcher_history_sha256.json', history)
        result = {'passed':True,'integrity_only':True,'original_audit_passed':False,
             'original_failed_unsealed_authoritative':True,'original_budget_censored':None,
             'original_hard_budget_state_uncertified':True,'completed_audit_component_checks':None,
             'published_independent_group_files':0,'actual_failure':error,
             'preserved_source_owned_files':len(initial),'prepared_owned_files_verified':len(prepared),
             'two_fresh_union_checks':passes,'new_test_credit':0,'full_G2':False,
             'adoption':False,'quantum_advantage':False,
             'administrative_CPU_wall_seconds':[time.process_time()-CPU,time.monotonic()-WALL]}
        save('verification.json', result)
        owned = {p.name:sha(p) for p in OUT.iterdir() if p.is_file() and p.name != 'FAILED_UNSEALED.json'}
        save('manifest.json', {'files':owned,'frozen_inputs':{p.relative_to(ROOT).as_posix():e for p,e in fixed.items() if p.is_relative_to(ROOT)},
             'external_runtime_inputs':{str(p):e for p,e in fixed.items() if not p.is_relative_to(ROOT)},
             'passed':True,'integrity_only':True,'original_source_failed':True,
             'manifest_self_hash_excluded':True,'new_test_credit':0})
        guard()
        (OUT / 'FAILED_UNSEALED.json').unlink()
        guard()
        print(json.dumps(result))
    except BaseException as exc:
        emergency({'passed':False,'error':repr(exc),'trace':traceback.format_exc(),
                   'capture_hard_budget_state_uncertified':True,'original_failure_unchanged':True})
        raise


if __name__ == '__main__':
    main()
