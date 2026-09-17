"""Read-only pinned author-source acquisition; does NOT execute author code."""
import hashlib
import requests
from .storage import ROOT, write_json


def main():
    cache = ROOT/'.context/four_papers_v1/code'
    cache.mkdir(parents=True,exist_ok=True)
    selections = [
        ('qcpolimi/WSL','9f4e633fb8a1acf2ea9fa8b288105545302a98ff',
         ['walsh_series_loader.ipynb','LICENSE']),
        ('fedimser/quant-arith-re','cc31e48d0eb62ab5b4f7893501b2ca36e584be95',
         ['resource_estimate/re_utils.py','lib/src/QuantumArithmetic/ConstAdder.qs',
          'test/superposition_test_utils.py']),
        ('Classiq/classiq-library','d09ddcbd5ffe6d853241e00f460f0f4006c4dc3f',
         ['applications/finance/autocallable_options/partial_exponential_state_preparation.ipynb',
          'applications/finance/autocallable_options/quantum_autocallable_option_pricing.ipynb']),
    ]
    records = []
    for repo, commit, names in selections:
        for name in names:
            url = 'https://raw.githubusercontent.com/%s/%s/%s' % (repo,commit,name)
            response = requests.get(url,timeout=60)
            response.raise_for_status()
            filename = repo.replace('/','_')+'_'+name.replace('/','_')
            (cache/filename).write_bytes(response.content)
            records.append(dict(url=url,commit=commit,
                sha256=hashlib.sha256(response.content).hexdigest(),executed=False))
    write_json(ROOT/'results/journal_sprint/four_paper_audit_v1/author_code_v2.json',records)


if __name__ == '__main__':
    main()
