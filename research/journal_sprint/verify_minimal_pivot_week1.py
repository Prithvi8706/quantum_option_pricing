"""Read-only archive/source integrity and exact cross-environment replay check."""
import argparse
import json
from pathlib import Path
from .storage import ROOT, sha256, write_json


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_archive(path, required):
    complete = read(path/'complete.json')['sha256']
    if not set(required+['planned.json']).issubset(complete):
        raise ValueError('missing required artifact hash')
    for name, digest in complete.items():
        target = (path/name).resolve()
        if path.resolve() not in target.parents or sha256(target) != digest:
            raise ValueError('artifact integrity: '+name)
    planned = read(path/'planned.json')
    for name, digest in planned['source_sha256'].items():
        target = (ROOT/name).resolve()
        if ROOT.resolve() not in target.parents or sha256(target) != digest:
            raise ValueError('source integrity: '+name)
    if 'inputs.json' in required:
        inputs = read(path/'inputs.json')
        if inputs['protocol_sha256'] != sha256(ROOT/'docs/journal_sprint/MINIMAL_PIVOT_STUDY_PLAN.md'):
            raise ValueError('protocol integrity')
        for name, digest in inputs['archive_sha256'].items():
            if sha256(ROOT/'results/journal_sprint/normalization_approximation_v1'/name) != digest:
                raise ValueError('input integrity: '+name)
    return dict(artifacts=len(complete),sources=len(planned['source_sha256']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    base = ROOT/'results/journal_sprint'
    groups = [('minimal_pivot_week1_v2','minimal_pivot_week1_replay_v2',
               ['inputs.json','circuits.json','structure.json','production.json','payoff.json']),
              ('minimal_pivot_week1_subset_v2','minimal_pivot_week1_subset_replay_v2',['results.json'])]
    records = []
    for original,replay,files in groups:
        a,b = base/original,base/replay
        checks = [check_archive(p,files) for p in (a,b)]
        for name in files:
            if read(a/name) != read(b/name):
                raise ValueError('nonidentical numeric replay: '+name)
        records.append(dict(original=original,replay=replay,checks=checks,
                            identical_payloads=files,
                            manifest_sha256={p.name:sha256(p/'complete.json') for p in (a,b)}))
    write_json(args.output,dict(passed=True,records=records,
        verifier_sha256=sha256(Path(__file__)),
        scope='integrity and deterministic replay; not independent scientific review'))
    print('Verified all recorded sources/artifacts and exact numeric payload replay.')


if __name__ == '__main__':
    main()
