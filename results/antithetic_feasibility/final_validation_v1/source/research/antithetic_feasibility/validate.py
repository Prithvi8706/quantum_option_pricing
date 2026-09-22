"""Final source/artifact receipt and executed test record; no overwrite."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    root=Path('results/antithetic_feasibility');out=root/'final_validation_v1';out.mkdir(exist_ok=False)
    start=time.perf_counter();cmd=[sys.executable,'-m','pytest','research/antithetic_feasibility','-q']
    with (out/'pytest.txt').open('x') as stream:proc=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT)
    sources=list(Path('research/antithetic_feasibility').glob('*.py'))+list(Path('research/antithetic_feasibility').glob('*.md'))+list(Path('docs/antithetic_feasibility').glob('*.md'))
    snap=out/'source';snap.mkdir()
    for path in sources:
        dest=snap/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    artifact_files=[p for p in root.rglob('*') if p.is_file() and out not in p.parents and '__pycache__' not in p.parts]
    versions={name:importlib.metadata.version(name) for name in ('numpy','scipy','numba','llvmlite','qiskit','pytest','psutil','matplotlib')}
    receipt=dict(command=cmd,returncode=proc.returncode,test_wall_seconds=time.perf_counter()-start,python=platform.python_version(),platform=platform.platform(),versions=versions,
                 source_hashes={str(p):digest(p) for p in sources},artifact_hashes={str(p):digest(p) for p in artifact_files},
                 artifact_bytes=sum(p.stat().st_size for p in artifact_files),
                 scope='Executed development validation. No held-out confirmation, hardware run, or complete financial-error certificate.')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print((out/'pytest.txt').read_text());print(json.dumps({k:v for k,v in receipt.items() if not k.endswith('hashes')},indent=2))
    if proc.returncode:raise RuntimeError('tests failed')


if __name__=='__main__':run()
