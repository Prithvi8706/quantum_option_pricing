"""Snapshot this investigation's code/docs and record immutable artifact hashes."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from research.controlled_source_completion.run import ROOT,dump


def main():
    destination=ROOT/'validation_v2'/'snapshot';rows=[]
    for root in (Path('research/controlled_source_completion'),Path('docs/controlled_source_completion')):
        for file in sorted(root.rglob('*')):
            if file.is_file() and file.suffix in ('.py','.md'):
                target=destination/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,target)
                rows.append(dict(path=str(file),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),bytes=file.stat().st_size))
    records=[]
    for file in sorted(ROOT.rglob('*')):
        if file.is_file() and destination not in file.parents and file.name!='artifact_manifest.json':
            records.append(dict(path=str(file),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),bytes=file.stat().st_size))
    reused=[Path('results/compound_feasibility/pilot_v1/training.json'),Path('results/controlled_residual_feasibility/parity_iid_v1/summaries.json'),
        Path('results/controlled_residual_feasibility/cold_v1/receipts.json'),Path('docs/controlled_residual_feasibility/RESULTS.md'),
        Path('research/journal_sprint/reversible_fixed_point.py'),Path('research/antithetic_feasibility/reversible.py')]
    tracked_diff=subprocess.run(['git','diff','--name-only'],capture_output=True,text=True,check=True).stdout
    head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
    dump(ROOT/'validation_v2'/'artifact_manifest.json',dict(git_head=head,tracked_diff=tracked_diff,source_snapshot=rows,artifacts=records,
        reused_read_only=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in reused],
        scope='This completion experiment only; earlier untracked research directories are preserved and are not adopted or modified by this snapshot.'))
    print(json.dumps(dict(source_files=len(rows),artifacts=len(records),artifact_bytes=sum(r['bytes'] for r in records),tracked_diff=tracked_diff)),flush=True)


if __name__=='__main__':main()
