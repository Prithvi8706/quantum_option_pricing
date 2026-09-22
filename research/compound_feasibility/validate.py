"""Final tests, immutable source snapshot and artifact provenance receipt."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def run():
    root=Path('results/compound_feasibility');out=root/'validation_v1';out.mkdir(exist_ok=False);start=time.perf_counter()
    command=[sys.executable,'-m','pytest','research/compound_feasibility','research/antithetic_feasibility','-q']
    with (out/'pytest.txt').open('x') as stream:p=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
    sources=list(Path('research/compound_feasibility').glob('*.py'))+list(Path('research/compound_feasibility').glob('*.md'))+list(Path('docs/compound_feasibility').glob('*.md'))
    deps=[Path('research/antithetic_feasibility')/s for s in ('classical.py','estimator.py','fixed_point.py','reversible.py','cost_model.py')]
    deps+=[Path('research/journal_sprint/reversible_fixed_point.py'),Path('research/stronger_arithmetic/circuits.py'),Path('results/antithetic_feasibility/compiled_blocks_v1/blocks.json'),Path('results/antithetic_feasibility/compiled_blocks_v1/loaders.json')]
    for src in sources:
        target=out/'source'/src;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
    artifacts=[q for q in root.rglob('*') if q.is_file() and out not in q.parents]
    versions={name:importlib.metadata.version(name) for name in ('numpy','scipy','numba','llvmlite','qiskit','pytest','matplotlib')}
    receipt=dict(command=command,returncode=p.returncode,validation_seconds=time.perf_counter()-start,versions=versions,python=platform.python_version(),platform=platform.platform(),
                 source_hashes={str(q):sha(q) for q in sources},dependency_hashes={str(q):sha(q) for q in deps},artifact_hashes={str(q):sha(q) for q in artifacts},
                 artifact_bytes=sum(q.stat().st_size for q in artifacts),
                 status='Completed development feasibility screen. No hardware pricing execution, held-out confirmation or complete financial arithmetic certificate.')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print((out/'pytest.txt').read_text());print(json.dumps({k:v for k,v in receipt.items() if not k.endswith('hashes')},indent=2))
    if p.returncode:raise RuntimeError('validation failed')


if __name__=='__main__':run()
