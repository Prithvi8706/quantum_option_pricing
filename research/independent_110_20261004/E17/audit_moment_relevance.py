"""One preregistered relevance audit; no scientific source imports or draws."""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[3]
DOC = 'docs/independent_110_20261004/E17/'
OUT = ROOT / 'results/independent_110_20261004/E17/audit_run001'
START = time.monotonic()
LOADED = {}


def require(value, message):
    if not value:
        raise ValueError(message)


def guard(admission=False):
    require(time.process_time() < (45 if admission else 60)
            and time.monotonic() - START < 120, 'Fixed E17 administrative budget')


def stable(path):
    guard()
    require(path.is_absolute() and path.resolve(strict=True) == path,
            'Canonical regular input')
    before = path.stat()
    require(path.is_file() and before.st_size <= 8388608, 'Finite input byte cap')
    data = path.read_bytes()
    after = path.stat()
    attrs = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    require(all(getattr(before, k) == getattr(after, k) for k in attrs)
            and len(data) == before.st_size, 'Stable full input bytes')
    return data


def checked(relative, expected):
    path = ROOT / relative
    require(path.resolve(strict=True).is_relative_to(ROOT)
            and path.relative_to(ROOT).as_posix() == relative, 'Canonical workspace path')
    data = stable(path)
    require(hashlib.sha256(data).hexdigest() == expected, 'Frozen input SHA: ' + relative)
    return data


def record(relative):
    return json.loads(LOADED[relative])


def owner(owner_path, member_path):
    manifest = record(owner_path)
    require(manifest['files'][member_path] == FREEZE['files'][member_path]['sha256'],
            'Immutable owner/member join: ' + member_path)


def save(name, value):
    guard()
    data = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    members = [p for p in OUT.iterdir() if p.is_file()]
    require(len(members) + 1 <= 16
            and sum(p.stat().st_size for p in members) + len(data) + 8192 < 16777216,
            'Owned file/byte budget with failure room')
    with (OUT / name).open('xb') as stream:
        stream.write(data)


def emergency(value):
    data = (json.dumps(value, sort_keys=True) + '\n').encode()
    require(len(data) <= 8192, 'Bounded emergency retention')
    with (OUT / 'FAILED_UNSEALED.json').open('wb') as stream:
        stream.write(data)


def models():
    tree = ast.parse(LOADED['research/compound_feasibility/model.py'].decode())
    fields = []
    defaults = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == 'Model':
            for member in node.body:
                if isinstance(member, ast.AnnAssign):
                    fields.append(member.target.id)
                    defaults[member.target.id] = ast.literal_eval(member.value)
    definitions = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'MODELS' for t in node.targets))
    result = []
    for call in definitions.elts:
        require(isinstance(call.func, ast.Name) and call.func.id == 'Model', 'GBM Model constructor')
        data = dict(defaults)
        data.update(zip(fields, (ast.literal_eval(arg) for arg in call.args)))
        data.update({k.arg: ast.literal_eval(k.value) for k in call.keywords})
        result.append(data)
    expected = [('C4', 4, 12, '.2', '.2', '1'), ('C8', 8, 12, '.4', '.2', '1'),
                ('H4', 4, 12, '.4', '.7', '3'), ('H8', 8, 24, '.4', '.2', '3')]
    require(len(result) == len(expected), 'Frozen four-case compound corpus')
    for data, (name, assets, dates, sigma, rho, maturity) in zip(result, expected):
        require((data['name'], data['assets'], data['dates']) == (name, assets, dates),
                'Contract names and dimensions')
        require(Fraction(str(data['sigma'])) == Fraction(sigma)
                and Fraction(str(data['rho'])) == Fraction(rho)
                and Fraction(str(data['maturity'])) == Fraction(maturity), 'Finite GBM parameters')
        require(data['spot'] == data['strike'] == 100
                and Fraction(str(data['rate'])) == Fraction(3, 100), 'Unchanged price literals')
        require(Fraction(-1, assets - 1) <= Fraction(rho) <= 1, 'Valid equicorrelation domain')
    return result


def exact_checks():
    counts = {}
    prices = tuple(map(Fraction, (0, 1, 100, 140, 1000000)))
    count = 0
    for x in prices:
        for y in prices:
            for w in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
                guard()
                average = w*x + (1-w)*y
                gap = w*x*x + (1-w)*y*y - average*average
                require(gap == w*(1-w)*(x-y)**2 and gap >= 0,
                        'Exact weighted second-moment Jensen identity')
                count += 1
    counts['weighted_Jensen_boundary_identities'] = count
    count = 0
    for x in prices:
        for y in prices:
            c = (x + 3*y) / 4
            for strike in (3, 6, 9):
                require(max(c-strike, 0)**2 <= (x*x + 3*y*y)/4,
                        'Conditional-mean/positive-part square domination')
                count += 1
    counts['conditional_Jensen_positive_part_checks'] = count
    cases = (([100, 139], 140, True), ([139, 140], 140, False),
             ([140, 139], 140, False), ([141, 139], 140, False),
             ([99, 99], 100, True), ([89, 89], 90, True), ([140, 140], 140, False))
    for baskets, barrier, expected in cases:
        alive = all(value < barrier for value in baskets)
        require(alive is expected, 'Strict monitored-barrier tie')
        average = Fraction(sum(baskets), len(baskets))
        payoff = max(average-100, 0) if alive else 0
        require(0 <= payoff <= max(barrier-100, 0), 'Survival gives bounded original payoff')
    counts['strict_barrier_boundary_cases'] = len(cases)
    count = 0
    for h in (Fraction(0), Fraction(1, 2), Fraction(1)):
        for residual in (Fraction(0), Fraction(1, 2), Fraction(1)):
            for d in (0, 1):
                require(abs(d*(h-residual)) <= 1, 'Signed residual support endpoints')
                count += 1
    # Removing either support premise destroys this normalized bound.
    require(abs(Fraction(2)-0) > 1 and abs(0-Fraction(2)) > 1,
            'Residual/policy-projection premise is necessary for this proof')
    counts['signed_support_boundary_checks'] = count
    counts['signed_support_missing_premise_counterchecks'] = 2
    # These are identities/boundary diagnostics, not new financial samples or a coverage proof.
    return counts


def native_rows():
    producer = 'results/limitation_program_20261001/E03_support_run001/'
    auditor = 'results/limitation_program_20261001/E03_support_audit_run002/'
    rows = []
    for case, shape in (('B4x12', (4, 12)), ('B8x52', (8, 52))):
        cert_path, audit_path = producer+case+'_certificate.json', auditor+case+'_audit.json'
        target_path = 'results/limitation_program_20261001/A10_coefficient_run001/'+case+'/min-depth/target.json'
        owner(producer+'manifest.json', cert_path)
        owner(auditor+'manifest.json', audit_path)
        cert, audit, target = record(cert_path), record(audit_path), record(target_path)
        require(audit['passed'] is True and cert['payoff_raw_bounds'] == audit['payoff_raw_bounds'],
                'Existing independent all-input support agrees')
        require((cert['assets'], cert['dates']) == shape
                and cert['width'] == target['width'] == 72
                and cert['fraction_bits'] == target['fraction_bits'] == 40
                and cert['target_output'] == target['outputs'], 'Actual native output/precision binding')
        for owner_path in (producer+'manifest.json', auditor+'manifest.json'):
            require(record(owner_path)['frozen_inputs'][target_path] == FREEZE['files'][target_path]['sha256'],
                    'Existing certificate binds actual target bytes')
        low, high = cert['payoff_raw_bounds']
        require(low == 0 and 0 < high < 40*(1<<40)
                and cert['all_original_uniform_word_patterns'] is True
                and audit['all_stock_native_intermediates_no_overflow'] is True,
                'Finite native payoff on all original input words')
        rows.append({'case':case, 'law':'actual finite-word native source', 'output':target['outputs'],
                     'width':72, 'fraction_bits':40, 'support_raw': [low, high],
                     'finite_first_and_second_moments':True, 'all_finite_positive_moments':True,
                     'proof':'Bounded total native output; all-input support certificate and independent audit',
                     'certificate':cert_path, 'independent_audit':audit_path,
                     'continuous_law_bridge_claimed_by_this_audit':False})
    return rows


def main(args):
    global FREEZE
    require(ROOT == Path.cwd().resolve() and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode, 'Fixed workspace and -I -S -B invocation')
    freeze_bytes = stable(ROOT / (DOC+'FREEZE.json'))
    require(hashlib.sha256(freeze_bytes).hexdigest() == args.freeze_sha256, 'Actual prospective freeze pin')
    FREEZE = json.loads(freeze_bytes)
    require(len(FREEZE['files']) <= 32
            and sum(item['bytes'] for item in FREEZE['files'].values()) <= 33554432,
            'Selected frozen corpus cap')
    for relative, item in FREEZE['files'].items():
        LOADED[relative] = checked(relative, item['sha256'])
        require(len(LOADED[relative]) == item['bytes'], 'Frozen byte count')
    for path, expected in FREEZE['selected_runtime'].items():
        require(hashlib.sha256(stable(Path(path))).hexdigest() == expected, 'Selected interpreter pin')
    guard(admission=True)
    require(not OUT.exists(), 'Fresh one-attempt output directory')
    OUT.mkdir(parents=True)
    emergency({'passed':False, 'authoritative_failure':True, 'unfinished':True, 'new_fixture_credit':0})
    try:
        preflight = record(DOC+'PROTOCOL.json')
        require(preflight['sampling'] is False and preflight['corpus']['new_heavy_tail_contract_selected'] is False,
                'No new workload or scientific acquisition')
        save('protocol.json', dict(preflight, prospective_freeze_sha256=args.freeze_sha256,
                                  selected_inputs=FREEZE))
        save('run_started.json', {'scientific_sampling':False, 'one_attempt':True})
        compound = models()
        counts = exact_checks()
        native = native_rows()
        kernel = LOADED['research/frontier_classical_20261001/kernels.py'].decode()
        spec = LOADED['manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md'].decode()
        require('if b / na >= barrier:' in kernel and 'avg /= dim' in kernel
                and 'disc * max(avg - strike, 0.0)' in kernel, 'Original monitored payoff convention')
        require('S0 = 100, K = 100' in spec and '0.3' in spec
                and 'r = 0.03, T = 1, H = 140' in spec, 'Frozen B4/B8 contract')
        finite_source = LOADED['research/controlled_source_completion/finance.py'].decode()
        require("logs=list(guarded)" in finite_source and "g.outputs['Y_%g'%kc]=g.clip" in finite_source
                and "continuous_bridge='NOT CERTIFIED'" in finite_source,
                'Clipped/reset finite compound law stays separate')
        counts['native_existing_certificate_bindings'] = len(native)
        counts['compound_GBM_model_classifications'] = len(compound)
        rows = [{'case':case, 'law':'original continuous finite-parameter GBM',
                 'payoffs':['arithmetic-average positive part','fixed digital','monitored knockout'],
                 'finite_first_and_second_moments':True, 'all_finite_positive_moments':True,
                 'knockout_support_symbolic':'[0, exp(-r*T)*(H-K)+]',
                 'infinite_variance_branch_relevant':False} for case in ('B4x12','B8x52')]
        rows += [{'case':data['name'], 'model':data, 'law':'original continuous GBM compound contract',
                  'compound_strikes':[3,6,9], 'finite_first_and_second_moments':True,
                  'all_finite_positive_moments':True, 'proof':'Conditional Jensen plus finite GBM fixing moments',
                  'H_label_denotes_Heston':False, 'infinite_variance_branch_relevant':False} for data in compound]
        certificate = {'schema':'e17-workload-moment-relevance-certificate-v1', 'passed':True,
                       'E17_single_relevance_audit_complete':True, 'status':'AUDITED_DORMANT_FOR_NOMINATED_PROGRAM',
                       'continuous_rows':rows, 'native_rows':native,
                       'signed_residual':{'finite_moments_under_documented_support_premises':True,
                                          'new_numerical_analytic_bound':None, 'E10_E12_computation_performed':False},
                       'Heston_uncapped_second_moment':None,
                       'Heston_reason':'Parameter/maturity-specific affine moment-domain proof not performed; GBM theorem does not transfer',
                       'likelihood_weighted_transform_second_moment':None,
                       'new_Pareto_or_heavy_tail_contract':False, 'proof':DOC+'MOMENT_PROOF.md',
                       'new_samples':0, 'new_fixture_credit':0, 'new_gate_replay_credit':0,
                       'timing_benchmark':False, 'financial_error_or_confidence_certified':False,
                       'source_adoption':False, 'quantum_advantage':False}
        save('checks.json', {'passed':True, 'check_families':counts,
                            'structural_checks_not_population_proofs_or_finance_fixtures':True})
        save('certificate.json', certificate)
        save('comparison.json', {'current_finite_GBM_or_bounded_native_program': 'Finite first and second moments proved',
                                 'Lp_or_Pareto_module':'Dormant; no G0 heavy-tail selection',
                                 'Heston_uncapped_or_weighted_alternative':'Unresolved distinct model/transform proof',
                                 'divergent_mean':'Would define an undefined nominated price; no such current case established',
                                 'complete_runtime_seconds':None, 'performance_comparison_performed':False,
                                 'administrative_CPU_wall_seconds':[time.process_time(),time.monotonic()-START]})
        for relative, item in FREEZE['files'].items():
            checked(relative, item['sha256'])
        require(hashlib.sha256(stable(ROOT/(DOC+'FREEZE.json'))).hexdigest() == args.freeze_sha256,
                'Freeze unchanged at sealing')
        owned = {p.relative_to(ROOT).as_posix():hashlib.sha256(stable(p)).hexdigest()
                 for p in OUT.iterdir() if p.name != 'FAILED_UNSEALED.json'}
        save('manifest.json', {'files':owned, 'frozen_inputs':{k:v['sha256'] for k,v in FREEZE['files'].items()},
                              'prospective_freeze_sha256':args.freeze_sha256,
                              'selected_runtime':FREEZE['selected_runtime'], 'passed':True,
                              'completed':True, 'budget_censored':False, 'manifest_self_hash_excluded':True,
                              'new_fixture_credit':0, 'quantum_advantage':False})
        guard()
        (OUT/'FAILED_UNSEALED.json').unlink()
        guard()
        print(json.dumps({'passed':True, 'E17_relevance_audit_complete':True,
                          'manifest':(OUT/'manifest.json').relative_to(ROOT).as_posix(),
                          'manifest_sha256':hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest()}))
    except BaseException as exc:
        emergency({'passed':False,'authoritative_failure':True,'error':repr(exc),
                   'trace':traceback.format_exc()[-6000:], 'hard_budget_state_uncertified':True,
                   'new_fixture_credit':0,'quantum_advantage':False})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-sha256', required=True)
    main(parser.parse_args())
