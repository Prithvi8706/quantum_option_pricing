"""Fresh metadata verification; does not rerun or credit scientific fixtures."""
from pathlib import Path
import hashlib
import json
import datetime

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/independent_110_20261004/handoff_integrity_run001'
SPECS = {
    'F16': ('results/independent_110_20261004/F16/run001/manifest.json', 'research/independent_110_20261004/F16/factor_reuse_audit_v1.py'),
    'F08': ('results/independent_110_20261004/F08/run001/manifest.json', 'research/independent_110_20261004/F08/single_predicate_screen_v1.py'),
    'F13': ('results/independent_110_20261004/F13/run001/manifest.json', 'research/independent_110_20261004/F13/non_lipschitz_transfer_audit_v1.py'),
    'E17': ('results/independent_110_20261004/E17/audit_run001/manifest.json', None),
}

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():
        raise ValueError('Fresh integrity directory required')
    OUT.mkdir(parents=True)
    checks = []
    rows = []
    for item, (manifest_path, author_path) in SPECS.items():
        manifest = json.loads((ROOT / manifest_path).read_text())
        expected = {}
        for key in ('files', 'input_pins', 'frozen_inputs', 'selected_runtime'):
            for path, spec in manifest.get(key, {}).items():
                expected[path] = spec
        if author_path:
            expected[author_path] = manifest['author_sha256']
        if item == 'E17':
            expected['docs/independent_110_20261004/E17/FREEZE.json'] = manifest['prospective_freeze_sha256']
            overlay = json.loads((ROOT / 'docs/independent_110_20261004/E17/INTEGRITY_AND_ERRATUM_run001.json').read_text())
            expected['docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md'] = overlay['corrected_proof_sha256']
            original = (ROOT / 'docs/independent_110_20261004/E17/MOMENT_PROOF.md').read_text()
            corrected = (ROOT / 'docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md').read_text()
            # Independent root reading approved only the single citation correction.
            assert len(original.splitlines()) == len(corrected.splitlines())
            differences = [(a, b) for a, b in zip(original.splitlines(), corrected.splitlines()) if a != b]
            assert len(differences) == 1
            assert 'first two moments' in differences[0][0]
            assert 'first two moments' not in differences[0][1]
        failure_markers = list((ROOT / manifest_path).parent.glob('*FAIL*'))
        for relative, spec in expected.items():
            path = Path(relative) if Path(relative).is_absolute() else ROOT / relative
            wanted = spec if isinstance(spec, str) else spec['sha256']
            observed = digest(path)
            size_ok = not isinstance(spec, dict) or path.stat().st_size == spec['bytes']
            checks.append({'item': item, 'path': relative, 'bytes': path.stat().st_size,
                           'expected': wanted, 'observed': observed, 'passed': observed == wanted and size_ok})
        rows.append({'item': item, 'manifest': manifest_path, 'manifest_sha256': digest(ROOT / manifest_path),
                     'failure_markers': [str(p.relative_to(ROOT)) for p in failure_markers]})
    passed = all(x['passed'] for x in checks) and not any(r['failure_markers'] for r in rows)
    result = {'passed': passed, 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'metadata_only': True, 'checks': checks, 'receipts': rows,
              'new_scientific_runs': 0, 'new_fixture_credit': 0,
              'scope': 'Root fresh hash, selected-input and citation-overlay verification; not a second mathematical proof or full runtime census.'}
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    (OUT / 'manifest.json').write_text(json.dumps({'author_sha256': digest(Path(__file__)),
        'verification_sha256': digest(OUT / 'verification.json')}, indent=2) + '\n')
    print(json.dumps({'passed': passed, 'fresh_hash_checks': len(checks), 'items': list(SPECS), 'mismatches': sum(not c['passed'] for c in checks)}))
    if not passed:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
