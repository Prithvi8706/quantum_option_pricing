"""Verify bounded acquisitions, critical sources and numerical replay."""
import argparse
import importlib.metadata
import json
from pathlib import Path
from .storage import ROOT, sha256, write_json


def verify_archive(path, payload):
    complete = json.loads((path/'complete.json').read_text())
    for name, digest in complete['sha256'].items():
        if sha256(path/name) != digest:
            raise AssertionError('artifact mismatch: '+str(path/name))
    planned = json.loads((path/'planned.json').read_text())
    # Other research files are listed by generic start_run but are not producer
    # dependencies. This explicit set covers this bounded acquisition.
    names = ['four_paper_probes.py','normal_loader_budget.py','decimal_enclosure.py',
             'storage.py', 'run_four_paper_baselines.py' if payload == 'results.json'
             else 'run_four_paper_probes.py']
    for name in names:
        rel = 'research/journal_sprint/'+name
        expected = planned['source_sha256'].get(rel, planned['source_sha256'].get(rel.replace('/','\\')))
        if expected is None or sha256(ROOT/rel) != expected:
            raise AssertionError('source mismatch: '+rel)
    return len(complete['sha256'])+len(names)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('original',type=Path)
    parser.add_argument('replay',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--baselines',action='store_true')
    args = parser.parse_args()
    names = ['results.json'] if args.baselines else ['identities.json','loader.json']
    checked = sum(verify_archive(p,names[0]) for p in (args.original,args.replay))
    for name in names:
        left = json.loads((args.original/name).read_text())
        right = json.loads((args.replay/name).read_text())
        if left != right:
            raise AssertionError('nonidentical replay: '+name)
        if name == 'loader.json':
            archived = ROOT/'results/journal_sprint/normalization_approximation_v1/loader.json'
            if sha256(archived) != left['archived_plan_sha256']:
                raise AssertionError('archived angle plan mismatch')
    write_json(args.output,dict(numeric_payloads_identical=names,hash_entries_checked=checked,
        qiskit_terra=importlib.metadata.version('qiskit-terra'),
        scope='same-producer separate-environment replay, not independent scientific review'))


if __name__ == '__main__':
    main()
