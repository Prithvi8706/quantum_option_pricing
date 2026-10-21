from pathlib import Path
import hashlib,json,urllib.request
here=Path(__file__).resolve().parent
dest=here/'primary_sources';assert not dest.exists();dest.mkdir()
url='https://arxiv.org/pdf/2308.07915v1'
p=dest/'Bravyi_2308_07915v1.pdf'
try:
 with urllib.request.urlopen(url,timeout=30) as response:raw=response.read(8388609)
 assert len(raw)<=8388608 and raw.startswith(b'%PDF')
 p.write_bytes(raw)
 record={'url':url,'retrieved':True,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'attempts':1}
except BaseException as error:
 record={'url':url,'retrieved':False,'error':str(error),'attempts':1}
 (here/'PRIMARY_RETRIEVAL_run001.json').write_text(json.dumps(record,indent=2)+'\n');raise
(here/'PRIMARY_RETRIEVAL_run001.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
