from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
old=here/'peer_a13_seal_review_v1.py';new=here/'peer_a13_seal_review_v2.py'
record=here/'PEER_REVIEW_LAUNCH_FAILED_run001.json'
assert not new.exists() and not record.exists()
record.write_text(json.dumps({'status':'STATIC_REVIEW_AUTHOR_SYNTAX_FAILURE','source':old.name,
 'source_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
 'error':'SyntaxError at dictionary path key; no source imports, artifact reads or scientific/recovery invocation occurred.',
 'preserved':True,'next':'Fresh peer reviewer v2 corrects dictionary quotation only.'},indent=2)+'\n')
text=old.read_text();bad=chr(39)+'path:f.name,';good=chr(39)+'path'+chr(39)+':f.name,'
assert text.count(bad)==1
new.write_text(text.replace(bad,good))
print(json.dumps({'fresh_source':new.name,'sha256':hashlib.sha256(new.read_bytes()).hexdigest()}))
