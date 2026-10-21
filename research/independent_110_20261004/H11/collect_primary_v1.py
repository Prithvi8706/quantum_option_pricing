from pathlib import Path
import hashlib,json,urllib.request
here=Path(__file__).resolve().parent
dest=here/'primary_sources';assert not dest.exists();dest.mkdir()
url='https://arxiv.org/pdf/2502.01864v1';p=dest/'He_2502_01864v1.pdf'
try:
 with urllib.request.urlopen(url,timeout=30) as response:raw=response.read(16777217)
 assert len(raw)<=16777216 and raw.startswith(b'%PDF');p.write_bytes(raw)
 record={'url':url,'retrieved':True,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'attempts':1,
  'browser_screenshot_failures':[{'page':17,'error':'TimeoutError'},{'page':41,'error':'TimeoutError'}],
  'primary_text_read_locators':['Theorems1.1/3.1/6.1','Section6.1 proof n3=4*n0*t^3 for fully addressable intrablock qubit gates','Introduction non-LDPC caveat']}
except BaseException as error:
 record={'url':url,'retrieved':False,'error':str(error),'attempts':1}
 (here/'PRIMARY_RETRIEVAL_run001.json').write_text(json.dumps(record,indent=2)+'\n');raise
(here/'PRIMARY_RETRIEVAL_run001.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
