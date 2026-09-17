"""W2 evidence integrity/replay and fail-closed decision verification."""
import argparse
import json
from pathlib import Path
from .storage import ROOT, sha256, write_json
from .week2_pipeline import choose, ae_schedule


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def verify_archive(path):
    manifest = read(path/'complete.json')['sha256']
    if not {'planned.json','inputs.json','results.json','timings.json'}.issubset(manifest):
        raise ValueError('missing mandatory evidence')
    for name,digest in manifest.items():
        target = (path/name).resolve()
        if path.resolve() not in target.parents or sha256(target)!=digest:
            raise ValueError('artifact mismatch: '+name)
    sources = read(path/'planned.json')['source_sha256']
    for name,digest in sources.items():
        target = (ROOT/name).resolve()
        if ROOT.resolve() not in target.parents or sha256(target)!=digest:
            raise ValueError('source mismatch: '+name)
    inputs = read(path/'inputs.json')
    for name,digest in inputs['archive_sha256'].items():
        if sha256(ROOT/name)!=digest:
            raise ValueError('input mismatch: '+name)
    if sha256(ROOT/'docs/journal_sprint/MINIMAL_PIVOT_WEEK2_PROTOCOL.md')!=inputs['protocol_sha256']:
        raise ValueError('protocol mismatch')
    return dict(artifacts=len(manifest),sources=len(sources))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    base = ROOT/'results/journal_sprint'
    checks = []
    for part in ('tiny','production','classical'):
        a = base/('minimal_pivot_week2_'+part+'_v1')
        b = base/('minimal_pivot_week2_'+part+'_replay_v1')
        records = [verify_archive(p) for p in (a,b)]
        if read(a/'results.json')!=read(b/'results.json'):
            raise ValueError('numeric replay differs: '+part)
        if read(a/'inputs.json')!=read(b/'inputs.json'):
            raise ValueError('input replay differs')
        checks.append(dict(part=part,checks=records,exact_numeric_replay=True,
                           manifest_sha256={p.name:sha256(p/'complete.json') for p in (a,b)}))
    production = read(base/'minimal_pivot_week2_production_v1/results.json')
    if len(production['rows'])!=32:
        raise ValueError('incomplete production matrix')
    for row in production['rows']:
        b = row['budget']
        if b['schedule']!=ae_schedule(b['beta'],b['deterministic_upper']):
            raise ValueError('schedule mismatch')
        if b['physical_execution_error'] is not None or b['confirmation_admitted']:
            raise ValueError('unjustified execution promotion')
    for decision in production['decisions']:
        rows = [r for r in production['rows'] if r['case']['id']==decision['case']]
        if dict(case=decision['case'],**choose(rows))!=decision:
            raise ValueError('selection mismatch')
    write_json(args.output,dict(passed=True,checks=checks,decision_rows_checked=32,
        excluded_from_numeric_equality=['timings.json','planned.json','complete.json'],
        exclusion_reason='wall time, environment and timestamps; all files still integrity checked',
        independent_peer_review=False,verifier_sha256=sha256(Path(__file__))))
    print('All six archives, exact numeric replay and fail-closed decisions verified.')


if __name__=='__main__':
    main()
