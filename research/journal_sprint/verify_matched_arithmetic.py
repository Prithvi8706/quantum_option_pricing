"""Strict manifests, source/input hashes, schedule replay and independent ledgers."""

import argparse
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path
import re
import subprocess

from .claim_assessment import projected_cost, schedule
from .run_matched_arithmetic import (
    CONFIG, PROTOCOL, PRODUCTION, arithmetic_budget, finite_diagnostic,
    full_resources, plan_for, reflected_rows,
)
from .storage import ROOT, sha256, write_json
from .verify_claim_assessment import within


FILES = {'planned.json', 'inputs.json', 'finite.json', 'case_D1.json',
         'case_D2.json', 'results.json'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def normalized(mapping):
    result = {Path(k).as_posix(): v for k, v in mapping.items()}
    if len(result) != len(mapping):
        raise ValueError('duplicate normalized paths')
    return result


def provenance(planned, inputs):
    head = planned['git_head']
    if not re.fullmatch('[0-9a-f]{40}', head):
        raise ValueError('invalid acquisition commit')
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', head,
                                     '--', 'research/journal_sprint'], cwd=ROOT, text=True).splitlines()
    expected = {n for n in names if n.endswith('.py')} | {'docs/journal_sprint/PROTOCOL_V1.md'}
    sources = normalized(planned['source_sha256'])
    mandatory = {'research/journal_sprint/'+name+'.py' for name in
                 ('matched_arithmetic', 'matched_aggregation', 'run_matched_arithmetic', 'verify_matched_arithmetic')}
    if not mandatory <= expected or set(sources) != expected:
        raise ValueError('source inventory differs from frozen committed tree')
    from .run_minimal_pivot_week2 import archives
    _, required = archives()
    required = normalized(required)
    for name in ('results.json', 'planned.json', 'complete.json'):
        key = Path(PRODUCTION).with_name(name).as_posix()
        required[key] = sha256(ROOT/key)
    actual = normalized(inputs)
    if actual != required:
        raise ValueError('input inventory/hash differs')
    for name, digest in sources.items():
        if sha256(within(ROOT, name)) != digest:
            raise ValueError('source hash mismatch: '+name)
        # Do not allow a plausible commit id to conceal uncommitted source edits.
        blob = subprocess.check_output(['git', 'show', head+':'+name], cwd=ROOT)
        # Historical Windows sources use Git's CRLF conversion. Archive hashes
        # remain byte-exact; commit identity separately allows only CRLF/LF.
        disk = (ROOT/name).read_bytes()
        if blob.replace(b'\r\n', b'\n') != disk.replace(b'\r\n', b'\n'):
            raise ValueError('source differs from acquisition commit: '+name)
    for name, digest in actual.items():
        if sha256(within(ROOT, name)) != digest:
            raise ValueError('input hash mismatch: '+name)


@lru_cache(maxsize=2)
def reconstruct_case(case_id):
    """Re-emit/count/check components; cached only within this verifier process."""
    from .asian_basket import setup
    from .matched_arithmetic import arithmetic_components
    from .matched_aggregation import aggregation_resources
    from .run_minimal_pivot_week1 import cost
    from .run_minimal_pivot_week2 import CASES, contract_of
    from .week2_pipeline import loader
    case = next(c for c in CASES[:2] if c['id'] == case_id)
    contract = contract_of(case)
    model = setup(contract)
    plan = plan_for(contract, model, 10)
    components = arithmetic_components(plan)
    marginal, error = loader(10)
    loading = cost(marginal)
    alternatives = reflected_rows(case, model, read(ROOT/PRODUCTION))
    aggregations = {}
    for mode in ('ripple', 'fourier'):
        a = aggregation_resources(plan['width'], len(model['means']), mode, zero_initialized=True)
        aggregations[mode] = a
        budget = arithmetic_budget(contract, model, plan, error, a['angle_error_upper'])
        base = components['native_excluding_aggregation']
        gates = {key: base[key]+2*a['uncontrolled'][key]+len(model['means'])*loading[key]
                 for key in ('u', 'cx')}
        gates['u'] += plan['selector_bits']+1
        wires = components['a_qubits_excluding_aggregation_helper']+int(mode == 'ripple')
        resources = full_resources(gates, wires, budget['schedule'])
        alternatives.append(dict(mode=mode, degree=plan['degree'], budget=budget, resources=resources))
    eligible = [r for r in alternatives if r['resources']['total_cx_projection'] is not None]
    def winner(key):
        if not eligible:
            return None
        best = min(eligible, key=lambda r: r['resources'][key])
        return dict(mode=best['mode'], degree=best['degree'])
    result = dict(case=case, arithmetic_plan=plan, arithmetic_components=components,
                aggregation=aggregations, alternatives=alternatives,
                lowest_projection=winner('total_cx_projection'),
                lowest_control_cancelled_projection=winner('control_cancelled_total_cx_projection'),
                production_choice=None, quantum_advantage=False, confirmation=False)
    return json.loads(json.dumps(result, allow_nan=False))


@lru_cache(maxsize=1)
def reconstruct_finite():
    from .run_minimal_pivot_week2 import CASES, archives
    data, _ = archives()
    return [finite_diagnostic(c, q, data) for c in CASES[:2] for q in (1, 2)]


def verify(path):
    path = Path(path)
    if {p.name for p in path.iterdir()} != FILES | {'complete.json'}:
        raise ValueError('archive inventory differs')
    manifest = read(path/'complete.json')['sha256']
    if set(manifest) != FILES:
        raise ValueError('manifest inventory differs')
    for name, digest in manifest.items():
        if sha256(within(path, name)) != digest:
            raise ValueError('artifact hash mismatch')
    planned = read(path/'planned.json')
    expected_config = {**CONFIG, 'protocol_sha256': sha256(ROOT/PROTOCOL)}
    if planned['config'] != expected_config:
        raise ValueError('protocol/config mismatch')
    provenance(planned, read(path/'inputs.json'))
    if read(path/'finite.json') != reconstruct_finite():
        raise ValueError('finite menu/diagnostics differ from recomputation')
    results = read(path/'results.json')
    if results['confirmation_admitted'] or results['quantum_over_classical_advantage_established']:
        raise ValueError('unsupported promotion')
    from .verify_minimal_pivot_week2 import verify_archive
    if results['prior_archive_integrity'] != verify_archive((ROOT/PRODUCTION).parent):
        raise ValueError('prior archive integrity differs')
    if [c['case']['id'] for c in results['comparisons']] != ['D1', 'D2']:
        raise ValueError('case menu differs')
    checks = 0
    for case in results['comparisons']:
        case_id = case['case']['id']
        if read(path/('case_'+case_id+'.json')) != case:
            raise ValueError('case summary mismatch')
        if case != reconstruct_case(case_id):
            raise ValueError('case/menu/components/budget/winner differ from recomputation')
        for row in case['alternatives']:
            budget, resources = row['budget'], row['resources']
            beta = budget['beta'] if row['mode'] == 'reflection' else budget['beta_upper']
            ae = schedule(F(beta), F(budget['deterministic_upper']))
            if ae != budget['schedule']:
                raise ValueError('schedule mismatch')
            if row['mode'] != 'reflection':
                if sum(map(F, budget['components'].values())) > F(budget['deterministic_upper']):
                    raise ValueError('budget sum underestimated')
            total = (projected_cost(resources, ae['M'], ae['repetitions'])
                     if ae['status'] == 'ideal_plan' else None)
            adjusted = {**resources, 'controlled_a_cx_projection': resources['a_cx_projection']}
            cancelled = (projected_cost(adjusted, ae['M'], ae['repetitions'])
                         if ae['status'] == 'ideal_plan' else None)
            if total != resources['total_cx_projection'] or cancelled != resources['control_cancelled_total_cx_projection']:
                raise ValueError('composition ledger mismatch')
            checks += 1
    if checks != 12 or [c['case']['id'] for c in results['comparisons']] != ['D1', 'D2']:
        raise ValueError('comparison menu differs')
    return dict(passed=True, rows_checked=checks, files_checked=len(FILES),
                source_files_checked=len(planned['source_sha256']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('first', type=Path)
    parser.add_argument('replay', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    checks = [verify(p) for p in (args.first, args.replay)]
    for name in FILES-{'planned.json'}:
        if read(args.first/name) != read(args.replay/name):
            raise ValueError('deterministic replay differs: '+name)
    write_json(args.output, dict(passed=True, exact_replay=True, checks=checks,
                                verifier_sha256=sha256(Path(__file__)),
                                scope='artifact integrity and logical ledger; not human expert signoff'))
    print('Verified both archives, all schedules/ledgers and exact deterministic replay.')


if __name__ == '__main__':
    main()
