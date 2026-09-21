"""Compare inventoried original SHA256 values with staged Git blobs; read only."""
from pathlib import Path
import hashlib
import json
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).parent
rows = [json.loads(line) for line in (HERE / 'consolidated_files.jsonl').read_text().splitlines()]
selected = [r for r in rows if r['disposition'] == 'consolidate-historical-project-artifact']
index = {}
for entry in subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=ROOT).split(b'\0'):
    if entry:
        meta, name = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        if stage != b'0':
            raise ValueError('Unmerged index')
        index[name.decode('utf-8')] = oid
process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def feed():
    for row in selected:
        process.stdin.write(index[row['path']] + b'\n')
    process.stdin.close()

worker = threading.Thread(target=feed)
worker.start()
total = 0
for row in selected:
    oid, kind, size = process.stdout.readline().split()
    if kind != b'blob':
        raise ValueError('Expected a staged blob')
    size = int(size)
    data = process.stdout.read(size)
    if process.stdout.read(1) != b'\n':
        raise ValueError('Invalid batch framing')
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Staged bytes differ from inventoried original: ' + row['path'])
    total += size
worker.join()
if process.wait() != 0:
    raise RuntimeError('git cat-file failed')
report = {'date':'2026-09-21', 'original_files_matched_to_git_index':len(selected),
          'original_bytes_preserved':total, 'all_matched':True,
          'scope':'Byte preservation only, not new scientific validation of historical artifacts.'}
with (HERE/'preservation_verification.json').open('x',encoding='utf-8') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(report))
