"""Record the final focused test run and environment; no quantum timing inference."""
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import time
from research.controlled_source_completion.run import ROOT,dump


def main():
    command=[sys.executable,'-m','pytest','research/controlled_source_completion/test_completion.py',
        'research/controlled_residual_feasibility','research/compound_feasibility','-q']
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1');start=time.perf_counter()
    result=subprocess.run(command,capture_output=True,text=True,env=env)
    directory=ROOT/'validation_v2';directory.mkdir(parents=True,exist_ok=True)
    (directory/'pytest.txt').write_text(result.stdout+'\n'+result.stderr)
    record=dict(command=command,returncode=result.returncode,seconds=time.perf_counter()-start,
        python=sys.version,platform=platform.platform(),versions={p:importlib.metadata.version(p) for p in ('numpy','scipy','numba','qiskit','mpmath','pytest')},
        pytest_summary=result.stdout.splitlines()[-1] if result.stdout else '',
        context='CPU test/compilation validation; these seconds are not quantum hardware timing.')
    dump(directory/'tests.json',record);print(json.dumps(record),flush=True)
    if result.returncode:raise SystemExit(result.returncode)


if __name__=='__main__':main()
