"""Generate complete resource tables, explicitly labeled as logical projections."""
import argparse
import csv
import io
from pathlib import Path
from .audit import ROOT
from .budgets import verify_budget
from .json_io import read
from .ledger import verify_ledger
from .schedules import verify_schedule
from .targets import verify_targets

FIELDS = ['case', 'route', 'degree', 'deterministic_dollar_allowance', 'status',
          'M', 'a_calls', 'projected_CX', 'control_cancelled_projected_CX',
          'qubits', 'scope']


def render(results):
    verify_targets(results)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    for case in results['comparisons']:
        for row in case['alternatives']:
            verify_budget(row)
            verify_schedule(row)
            verify_ledger(row)
            b, r = row['budget'], row['resources']
            s = b['schedule']
            writer.writerow(dict(case=case['case']['id'], route=row['mode'], degree=row['degree'],
                                 deterministic_dollar_allowance=b['deterministic_upper'],
                                 status=s['status'], M=s['M'], a_calls=s['a_calls'],
                                 projected_CX=r['total_cx_projection'],
                                 control_cancelled_projected_CX=r['control_cancelled_total_cx_projection'],
                                 qubits=r['total_qubits'], scope='logical projection; not runtime or quantum advantage'))
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = read(ROOT/'results/journal_sprint/matched_arithmetic_v1/results.json')
    text = render(data)
    with args.output.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)


if __name__ == '__main__':
    main()
