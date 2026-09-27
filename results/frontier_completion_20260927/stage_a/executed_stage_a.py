"""Prospectively specified generic knock-out source compilation; no estimator claim.

Run from the repository root with the isolated pinned Python environment:
    python -m research.frontier_completion_20260927.stage_a
Archives are read only. All new artifacts are written to OUT.
"""

from collections import Counter
from importlib import metadata
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from types import SimpleNamespace

import numpy as np

from research.advantage_frontier_20260923.barrier_oracle_depth import build, leaf_costs, score
from research.controlled_completion_followup.truncated_multiplier import TruncatedLibrary
from research.controlled_priority_completion.parallel_source import make_schedule
from research.controlled_priority_completion.parallel_source import execute as wave_execute
from research.controlled_source_completion.compiler import compile_graph, execute, resolve_library
from research.controlled_source_completion.ir import evaluate
from research.controlled_source_completion.optimize import optimize

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/frontier_completion_20260927/stage_a'
ARCHIVE = ROOT / 'results/controlled_priority_completion/range_compile_v1'


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_dag(source):
    """Call-specific forward weighted DAG; not a physically scheduled circuit."""
    lib = resolve_library(source)
    entries = {k: json.loads((lib / (k + '.json')).read_text()) for k in source['library_keys']}
    arrival = {v: 0 for n in source['inputs'] for v in n['out']}
    counts = Counter()
    for call in source['forward_calls']:
        entry = entries[call['leaf']]
        end = max((arrival[a] for a in call['args']), default=0) + entry['resources']['t_depth']
        for v in call['out']:
            if v in arrival:
                raise ValueError('SSA output reused')
            arrival[v] = end
        counts['forward_t_count'] += entry['resources']['t_count']
        counts['forward_calls'] += 1
    counts['forward_dependency_t_depth'] = max(arrival[v] for v in source['outputs'].values())
    return dict(counts)


def score_target(target):
    graph = SimpleNamespace(nodes=target['nodes'], outputs=target['outputs'])
    return {name: score(graph, costs) for name, costs in zip(('cheapest', 'median'), leaf_costs())}


def archive_accounting():
    rows = []
    for case in ('C4_f40', 'H8_f40'):
        directory = ARCHIVE / case
        source = json.loads((directory / 'source.json').read_text())
        target = json.loads((directory / 'target.json').read_text())
        exact = exact_dag(source)
        estimates = score_target(target)
        rows.append(dict(case=case, exact=exact, operation_scores=estimates,
                         ratios={name: s['forward_critical_t_depth'] /
                                 exact['forward_dependency_t_depth'] for name, s in estimates.items()},
                         source_sha256=digest(directory / 'source.json'),
                         target_sha256=digest(directory / 'target.json')))
    dump(OUT / 'archive_accounting.json', rows)
    return rows


def selected_inputs(source, rng, random_count, big=False):
    names = [n['params']['name'] for n in source['inputs']]
    for j in range(random_count):
        yield 'random_%02d' % j, dict(zip(names, map(int, rng.integers(0, 2**32, len(names)))))
    yield 'all_zero', dict.fromkeys(names, 0)
    yield 'all_maximum', dict.fromkeys(names, 2**32 - 1)
    if not big:
        yield 'midpoint', dict.fromkeys(names, 2**31)
        yield 'alternating_endpoints', {name: (2**32 - 1 if i % 2 else 0) for i, name in enumerate(names)}


def basis_replay(case, original, target, source, schedules, rng, random_count, big):
    rows = []
    mask = 2**source['word_width'] - 1
    initial = {'Y': int('a5' * 9, 16) & mask}
    for name, inputs in selected_inputs(source, rng, random_count, big):
        started = time.perf_counter()
        _, trace = evaluate(target, inputs, True)
        _, original_trace = evaluate(original, inputs, True)
        raw = trace[target['outputs']['Y']]
        if raw != original_trace[original['outputs']['Y']]:
            raise AssertionError('Optimizer changed target on ' + case + '/' + name)
        expected = {'Y': raw ^ initial['Y']}
        serial = execute(source, inputs, initial)
        wave = wave_execute(source, schedules['all'], inputs, initial)
        passed = (serial['values'] == wave['values'] == expected and serial['workspace_clean']
                  and serial['inputs_preserved'] and wave['all_input_and_workspace_bits_restored'])
        row = dict(name=name, inputs=inputs, initial_outputs=initial, expected=expected,
                   serial=serial, wave=wave, passed=passed, seconds=time.perf_counter() - started)
        rows.append(row)
        dump(OUT / case / 'basis_replay.json', rows)
        print(case, name, 'PASS' if passed else 'FAIL', '%.2fs' % row['seconds'], flush=True)
        if not passed:
            raise AssertionError('Gate replay failed on ' + case + '/' + name)
    return rows


def compile_case(na, nt, rng):
    name = 'B%dx%d' % (na, nt)
    path = OUT / name
    started = time.perf_counter()
    original = build(na, nt).as_dict()
    target = optimize(original)
    dump(path / 'original_target.json', original)
    # A fresh task-local generic base prevents cache misses mutating older evidence.
    lib = TruncatedLibrary(OUT / 'leaves_f40', 72, 40, target['tables'], OUT / 'base_leaves_f40')
    source, _ = compile_graph(target, path, lib)
    exact = exact_dag(source)
    schedules = {label: make_schedule(source, limit) for label, limit in (('all', None), ('128', 128), ('32', 32))}
    for label, schedule in schedules.items():
        assert exact['forward_dependency_t_depth'] == schedule['dependency_only_forward_t_depth']
        assert 2 * exact['forward_dependency_t_depth'] <= schedule['resources']['t_depth']
        assert 2 * exact['forward_t_count'] == source['resources']['t_count'] == schedule['resources']['t_count']
        dump(path / ('schedule_' + label + '.json'), schedule)
    operation_scores = score_target(target)
    row = dict(case=name, original_nodes=len(original['nodes']), optimized_nodes=len(target['nodes']),
               optimization=target.get('optimization'), exact=exact, operation_scores=operation_scores,
               serial_resources=source['resources'],
               schedules={label: s['resources'] for label, s in schedules.items()},
               logical_width_caps={label: {str(cap): s['resources']['logical_qubits'] <= cap
                                          for cap in (10000, 100000)} for label, s in schedules.items()},
               compile_and_schedule_seconds=time.perf_counter() - started)
    dump(path / 'accounting.json', row)
    print(name, 'compiled', json.dumps(exact), flush=True)
    checks = basis_replay(name, original, target, source, schedules, rng, 16 if na == 4 else 2, na == 8)
    row['basis_cases_passed'] = sum(r['passed'] for r in checks)
    row['all_basis_cases_passed'] = all(r['passed'] for r in checks)
    row['elapsed_seconds'] = time.perf_counter() - started
    dump(path / 'accounting.json', row)
    return row


def historical_frontier(rows):
    file = ROOT / 'results/advantage_frontier_20260923/barrier_decision.json'
    old = json.loads(file.read_text())
    grid = []
    for row in rows:
        for entry in old['grid']:
            if entry['case'] != row['case'] or entry['sigma_kind'] != 'plain':
                continue  # The compiled oracle does not compute the preintegrated estimand.
            for label, resources in row['schedules'].items():
                depth = resources['t_depth']
                quantum_seconds = entry['quantum_calls'] * depth * entry['t_layer']
                grid.append(dict(case=row['case'], schedule=label, eps=entry['eps'], k=entry['k'],
                                 t_layer_seconds=entry['t_layer'], sigma_q=entry['sigma_q'],
                                 hypothetical_calls=entry['quantum_calls'],
                                 historical_classical_model_seconds=entry['classical_seconds'],
                                 source_only_model_seconds=quantum_seconds,
                                 clean_source_t_depth=depth, historical_d_max=entry['d_max'],
                                 ratio_to_10x_budget=depth / entry['d_max'],
                                 max_layer_seconds_for_10x=entry['classical_seconds'] /
                                 (10 * entry['quantum_calls'] * depth),
                                 required_T_per_second_for_10x=10 * entry['quantum_calls'] *
                                 resources['t_count'] / entry['classical_seconds']))
    result = dict(scope='Historical classical model substituted unchanged; not new timing or a certified estimator.',
                  classical_input_sha256=digest(file), grid=grid)
    dump(OUT / 'historical_frontier.json', result)
    return result


def main():
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
                   packages={d.metadata['Name']: d.version for d in metadata.distributions()},
                   git_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                   script_sha256=digest(Path(__file__)),
                   analysis_spec_sha256=digest(ROOT / 'manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC.md'),
                   seed=2026092701, environment_scope='Existing isolated version-pinned environment; not fresh/hash-pinned T0.')
    dump(OUT / 'environment.json', receipt)
    archive = archive_accounting()
    rng = np.random.Generator(np.random.PCG64(2026092701))
    rows = [compile_case(na, nt, rng) for na, nt in ((4, 12), (8, 52))]
    frontier = historical_frontier(rows)
    # Inventory includes emitted gates and all generated dependencies, excludes itself.
    files = {}
    for file in sorted(OUT.rglob('*')):
        if file.is_file() and file.name not in ('artifact_hashes.json', 'summary.json'):
            files[file.relative_to(OUT).as_posix()] = digest(file)
    for row in rows:
        source = json.loads((OUT / row['case'] / 'source.json').read_text())
        lib = resolve_library(source)
        for key in source['library_keys']:
            entry = json.loads((lib / (key + '.json')).read_text())
            assert digest(lib / entry['gate_file']) == entry['sha256']
    dump(OUT / 'artifact_hashes.json', files)
    selected = [r for r in frontier['grid'] if r['eps'] == .001 and r['k'] == 3
                and r['t_layer_seconds'] == 1e-7 and r['schedule'] == 'all']
    dump(OUT / 'summary.json', dict(archive_accounting=archive, cases=rows, primary_frontier=selected,
                                  elapsed_seconds=time.perf_counter() - started, artifact_count=len(files),
                                  scientific_status='No defensible significant quantum advantage established yet'))
    print(json.dumps(selected, indent=2), flush=True)


if __name__ == '__main__':
    main()
