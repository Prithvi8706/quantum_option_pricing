"""Retain static v3 and prospectively freeze its reviewed lifecycle corrections."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
old = Path(__file__).with_name('confidence_allocation_screen_v3.py')
new = old.with_name('confidence_allocation_screen_v4.py')
assert not new.exists()
s = old.read_text()
replacements = [
    ('E08/run003', 'E08/run004'),
    ('RESULTS_run003.txt', 'RESULTS_run004.txt'),
    ('START_CPU = None', 'class RepetitionCapError(ValueError):\n    pass\n\n\nSTART_CPU = None'),
    ('raise ValueError("Frozen E08 repetition cap exhausted.")', 'raise RepetitionCapError("Frozen E08 repetition cap exhausted.")'),
    ('except ValueError as exc:', 'except RepetitionCapError as exc:'),
    ('if (OUT / "RUN_STARTED.json").exists():', 'if (OUT / "FAILED_UNSEALED.json").exists():\n        raise RuntimeError("An existing failure marker prohibits E08 promotion or retry.")\n    if (OUT / "RUN_STARTED.json").exists():'),
    ('report.write_text("\\n".join(lines) + "\\n", encoding="utf-8")', 'guard()\n    report.write_text("\\n".join(lines) + "\\n", encoding="utf-8")\n    guard()'),
    ('assert sum(p.stat().st_size for p in files if p.is_file()) <= protocol["budgets"]["output_bytes"]', 'assert sum(p.stat().st_size for p in files if p.is_file()) + 65536 <= protocol["budgets"]["output_bytes"]'),
    ('print(json.dumps(summary, sort_keys=True))', 'assert (OUT / "manifest.json").stat().st_size <= 49152\n    assert sum(p.stat().st_size for p in OUT.iterdir() if p.is_file()) + report.stat().st_size + 16384 <= protocol["budgets"]["output_bytes"]\n    guard()\n    print(json.dumps(summary, sort_keys=True))'),
]
for a, b in replacements:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
compile(s, str(new), 'exec')
new.write_text(s, encoding='utf-8')
hold = ROOT / 'results/independent_110_20261004/E08/v3_preflight_hold.json'
assert not hold.exists()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
hold.write_text(json.dumps({'decision': 'STATIC_REJECTED_BEFORE_SCIENTIFIC_RUN',
    'source_sha256': sha(old), 'protocol_sha256': sha(ROOT / 'results/independent_110_20261004/E08/run003/protocol.json'),
    'replacement_source_sha256': sha(new), 'scientific_runs': 0,
    'reasons': ['Dedicated repetition-cap exception preserves other failure provenance.',
                'Reserve manifest and bounded emergency marker within frozen output limit.',
                'Existing failure marker prohibits promotion/retry; report writes guarded.'],
    'scientific_geometry_and_main_budgets_unchanged': True}, indent=2) + '\n')
print('V4 author compiled; V3 static hold retained. No scientific run.')
