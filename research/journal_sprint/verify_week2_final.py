"""Final W2 verification: corrected tiny v2 plus frozen production/classical v1."""
import argparse
from pathlib import Path
from .verify_minimal_pivot_week2 import read, verify_archive
from .storage import ROOT, sha256, write_json
from .week2_pipeline import choose, ae_schedule


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    base = ROOT/'results/journal_sprint'
    checks = []
    for part,version in [('tiny',2),('production',1),('classical',1)]:
        a = base/f'minimal_pivot_week2_{part}_v{version}'
        b = base/f'minimal_pivot_week2_{part}_replay_v{version}'
        records = [verify_archive(p) for p in (a,b)]
        for name in ('results.json','inputs.json'):
            if read(a/name)!=read(b/name):
                raise ValueError('numeric/input replay differs: '+part)
        checks.append(dict(part=part,version=version,checks=records,exact_numeric_replay=True,
            manifest_sha256={p.name:sha256(p/'complete.json') for p in (a,b)}))
    production = read(base/'minimal_pivot_week2_production_v1/results.json')
    if len(production['rows'])!=32:
        raise ValueError('incomplete production grid')
    for row in production['rows']:
        b = row['budget']
        if b['schedule']!=ae_schedule(b['beta'],b['deterministic_upper']):
            raise ValueError('schedule mismatch')
        if b['physical_execution_error'] is not None or b['confirmation_admitted']:
            raise ValueError('unjustified physical promotion')
    for decision in production['decisions']:
        rows = [r for r in production['rows'] if r['case']['id']==decision['case']]
        if dict(case=decision['case'],**choose(rows))!=decision:
            raise ValueError('decision mismatch')
    write_json(args.output,dict(passed=True,checks=checks,decision_rows_checked=32,
        excluded_from_equality=['timings.json','planned.json','complete.json'],
        reason='wall time/environment/timestamps; all files still hash checked',
        independent_peer_review=False,verifier_sha256=sha256(Path(__file__))))
    print('All final archive/source hashes, exact numeric replays and32 decisions passed.')


if __name__=='__main__':
    main()
