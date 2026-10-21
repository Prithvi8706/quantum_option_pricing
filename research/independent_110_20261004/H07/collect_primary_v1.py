"""Two preregistered exact PDF snapshots; one request each; failures retained."""
import hashlib
import json
from pathlib import Path
import time
import urllib.request
HERE=Path(__file__).resolve().parent
DIRECTORY=HERE/'primary_sources'
URLS={
 'Guillaud_Mirrahimi_1904_09474v1.pdf':'https://arxiv.org/pdf/1904.09474v1',
 'Guillaud_Mirrahimi_2009_10756v1.pdf':'https://arxiv.org/pdf/2009.10756v1',
}
assert not DIRECTORY.exists()
DIRECTORY.mkdir()
records={};start=time.monotonic()
for name,url in URLS.items():
    try:
        with urllib.request.urlopen(url,timeout=30) as response:
            raw=response.read(8*2**20+1)
            assert len(raw)<=8*2**20
        with (DIRECTORY/name).open('xb') as output:output.write(raw)
        records[name]={'url':url,'retrieved':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    except Exception as error:
        records[name]={'url':url,'retrieved':False,'error_type':type(error).__name__,'error':str(error)}
assert time.monotonic()-start<70
with (HERE/'PRIMARY_RETRIEVAL_run001.json').open('x') as output:json.dump(records,output,indent=2);output.write('\n')
print(json.dumps(records))
