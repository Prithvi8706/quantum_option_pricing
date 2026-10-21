"""Fresh V4 operational copy: actual namespace-package absence and failed history."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = ROOT / 'research/limitation_program_20261001'
HERE = Path(__file__).resolve().parent
NAMES = {
    'a20_signal_receipt_continuation_v3.py': 'a20_signal_receipt_continuation_v4.py',
    'experiment_arithmetic_free_basket_signal_continuation_v3.py': 'experiment_arithmetic_free_basket_signal_continuation_v4.py',
    'audit_arithmetic_free_basket_signal_continuation_v3.py': 'audit_arithmetic_free_basket_signal_continuation_v4.py',
    'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V3.md': 'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V4.md',
    'a20_comparator_phase_continuation_preflight_v3.json': 'a20_comparator_phase_continuation_preflight_v4.json',
}


def main():
    assert ROOT == Path.cwd().resolve()
    failed = {
        p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (HERE / 'PRODUCER_ROOT_READY_run001.json', HERE / 'producer_prepare_admission_failure001.json',
                  HERE / 'producer_prepare_launch002.log', HERE / 'ROOT_STATIC_REVIEW_v3.json',
                  RESEARCH / 'a20_signal_receipt_continuation_v3.py',
                  RESEARCH / 'experiment_arithmetic_free_basket_signal_continuation_v3.py')
    }
    record = {'science_executed':False, 'failed_history':failed, 'changes':{}}
    for old, new in NAMES.items():
        data = (RESEARCH / old).read_bytes()
        text = data.decode('utf-8')
        for before, after in NAMES.items():
            text = text.replace(before, after)
            if before.endswith('.py'):
                text = text.replace(before[:-3], after[:-3])
        text = text.replace('A20_continuation_20261004_producer_run001', 'A20_continuation_20261004_producer_run002')
        text = text.replace('A20_continuation_20261004_audit_run001', 'A20_continuation_20261004_audit_run002')
        text = text.replace('A20-comparator-phase-static-READY-v3', 'A20-comparator-phase-static-READY-v4')
        if old.startswith('a20_signal_receipt_'):
            before = '''        self.add(INTERPRETER, self.ready["interpreter_sha256"])'''
            assert text.count(before)==1
            text = text.replace(before, '''        for key, expected in self.ready["prior_attempt_sha256"].items():
            require((ROOT / key).relative_to(ROOT).as_posix() == key, "Exact retained prior-attempt key")
            self.add(ROOT / key, expected)
''' + before)
            before = '''        for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
            found.add(self.canonical(source))
            cache = Path(importlib.util.cache_from_source(str(source)))
            if cache.exists():
                found.add(self.canonical(cache))
            else:
                absent.add(str(cache))'''
            assert text.count(before)==1
            after = '''        for source in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
            cache = Path(importlib.util.cache_from_source(str(source)))
            if source.exists():
                found.add(self.canonical(source))
                if cache.exists():
                    found.add(self.canonical(cache))
                else:
                    absent.add(str(cache))
            else:
                require(not cache.exists(), "Absent namespace initializer has no orphan bytecode")
                absent.add(str(source))
                absent.add(str(cache))'''
            text = text.replace(before, after)
        elif old.endswith('.json'):
            obj=json.loads(text)
            obj['schema']='A20-comparator-phase-continuation-preflight-v4'
            obj['operational_changes_only'].extend([
                'Fresh V4 operational files/routes after failed pre-mkdir V3 runtime admission.',
                'Actual namespace __init__.py/cache absence is recorded and rechecked, no initializer fabricated.',
                'ROOT-pinned prior CLI failure bytes join strict frozen actual-SHA union.',
            ])
            obj['prior_attempt_sha256']=failed
            obj['required_ROOT_READY_fields'].extend(['base_interpreter_sha256','prior_attempt_sha256'])
            text=json.dumps(obj,sort_keys=True,indent=2)+'\n'
        elif old.endswith('.md'):
            text = ('# V4 namespace-package operational correction\n\n'
                    'V3 actual prepare failed before mkdir or scientific import because the runtime enumerator required a nonexistent namespace-package initializer. V4 admits the actual absent initializer only while also requiring absent cache bytes, records both absences and rechecks them between prepare/run. Existing files are unchanged; no __init__.py is fabricated. Fresh V4 routes and strict prior-attempt bytes preserve both CLI failures. Mathematical functions, native72/F40 domain, all2608 checks and180CPU/150admission/600wall remain unchanged.\n\n' + text)
        out=text.encode('utf-8')
        if new.endswith('.py'):
            compile(ast.parse(text),new,'exec')
        with (RESEARCH/new).open('xb') as stream:stream.write(out)
        record['changes'][new]={'source':old,'source_sha256':hashlib.sha256(data).hexdigest(),'new_sha256':hashlib.sha256(out).hexdigest()}
    with (HERE/'release_authoring_v4.json').open('x',encoding='utf-8') as stream:
        json.dump(record,stream,sort_keys=True,indent=2);stream.write('\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
