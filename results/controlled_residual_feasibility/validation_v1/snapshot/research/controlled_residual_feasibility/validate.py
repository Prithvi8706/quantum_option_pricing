"""Final tests and append-only evidence hashes; never mutates prior evidence."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


def run():
    out=Path('results/controlled_residual_feasibility/validation_v1');out.mkdir(exist_ok=False)
    cmd=[sys.executable,'-m','pytest','research/controlled_residual_feasibility',
         'research/compound_feasibility','research/antithetic_feasibility','-q']
    start=time.perf_counter()
    with (out/'pytest.txt').open('x') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    roots=[Path('research/controlled_residual_feasibility'),Path('docs/controlled_residual_feasibility'),
           Path('research/compound_feasibility'),Path('research/antithetic_feasibility')]
    sources={}
    for root in roots:
        for f in root.rglob('*'):
            if f.is_file() and f.suffix in ('.py','.md'):
                sources[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
                if 'controlled_residual_feasibility' in str(root):
                    dest=out/'snapshot'/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(f.read_bytes())
    artifacts={}
    for f in Path('results/controlled_residual_feasibility').rglob('*'):
        if f.is_file() and 'validation_v1' not in str(f):artifacts[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
    receipt=dict(command=cmd,returncode=p.returncode,seconds=time.perf_counter()-start,python=sys.version,platform=platform.platform(),
                 source_hashes=sources,artifact_hashes=artifacts,
                 status='Completed controlled-residual feasibility investigation; no hardware execution or end-to-end advantage claim.')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if not k.endswith('_hashes')},indent=2))
    if p.returncode:raise RuntimeError('validation failed; see retained test output')


if __name__=='__main__':run()
