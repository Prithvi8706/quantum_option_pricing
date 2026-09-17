"""Download primary sources to an ignored cache; archive provenance, not PDFs."""
import hashlib
import json
from pathlib import Path
import sys
import requests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.context/four_paper_reader_deps'))
from pypdf import PdfReader


def main():
    cache = ROOT / '.context/four_papers_v1'
    cache.mkdir(parents=True, exist_ok=True)
    sources = {
        'autocallable': 'https://arxiv.org/pdf/2507.19039v1',
        'arithmetic': 'https://arxiv.org/pdf/2509.07015v1',
        'regression': 'https://arxiv.org/pdf/2505.17713v1',
        'walsh': 'https://arxiv.org/pdf/2502.05193v1',
    }
    # Pin author versions. Publisher Walsh PDF was inaccessible (403); never
    # relabel a cached preprint as the different publisher version.
    records = []
    for name, url in sources.items():
        path = cache / (name + '.pdf')
        if not path.exists():
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            if not response.content.startswith(b'%PDF'):
                raise ValueError('Not a PDF: ' + url)
            path.write_bytes(response.content)
        reader = PdfReader(path)
        text = '\n'.join('\n=== PAGE %d ===\n%s' % (i+1, p.extract_text())
                         for i, p in enumerate(reader.pages))
        (cache / (name + '.txt')).write_text(text, encoding='utf8')
        records.append(dict(name=name, url=url, pages=len(reader.pages),
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        print(name, len(reader.pages), url, flush=True)
    out = ROOT / 'results/journal_sprint/four_paper_audit_v1'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'sources.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf8')
    if sources['walsh'].startswith('https://arxiv.org'):
        print('Walsh: author preprint; publisher-version equivalence NOT verified.')


if __name__ == '__main__':
    main()
