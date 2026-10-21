"""Fresh verifier for newly completed packets only; older passes stay immutable."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
old=Path(__file__).with_name('verify_handoffs_v2.py')
new=old.with_name('verify_handoffs_v3.py')
assert not new.exists()
s=old.read_text()
s=s.replace('handoff_integrity_run002','handoff_integrity_run003')
a=s.index('SPECS={');b=s.index('\ndef sha',a)
s=s[:a]+'''SPECS={
 'E01':('E01/audit_run001',None),
 'C15':('C15/run002',None),
 'E15':('E15/run002','E15/coherent_inner_toy_v2.py'),
}
EXTRA={
 'docs/independent_110_20261004/E01/HANDOFF.md':'4057fd08ba366c4c32a2f4471a11c1519464b0542ad67cec1d6882094eec188f',
}
'''+s[b:]
s=s.replace("'frozen_corpus_sha256']", "'frozen_corpus_sha256','corpus_sha256']")
s=s.replace("key=='files' and len(file.parts)==1", "key=='files' and file.parts[0] not in ('docs','research','results')")
s=s.replace("len(path.parts)==1", "path.parts[0] not in ('docs','research','results')")
s=s.replace("if path.parent==run:declared.add(path.name)", "if path.is_relative_to(run):declared.add(str(path.relative_to(run)).replace('\\\\','/'))")
s=s.replace("{p.name for p in run.iterdir() if p.is_file() and p.name!='manifest.json'}", "{str(p.relative_to(run)).replace('\\\\','/') for p in run.rglob('*') if p.is_file() and p.name!='manifest.json'}")
s=s.replace("if item=='E17':expected", "if item=='E01':expected[ROOT/'docs/independent_110_20261004/E01/FREEZE.json']=manifest['freeze_sha256']\n        if item=='C15':expected[ROOT/'research/independent_110_20261004/C15/claims_v1.json']=manifest['claim_release_sha256']\n        if item=='E17':expected")
compile(s,str(new),'exec');new.write_text(s)
print('Fresh integrity V3 compiled for E01/C15/E15 only.')
