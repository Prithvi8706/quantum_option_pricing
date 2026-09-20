"""Check local inline Markdown link targets; no network or anchor validation."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from .paths import within


def verify_links(root, documents):
    root = Path(root).resolve()
    checked = 0
    for document in documents:
        source = within(root, document)
        text = source.read_text(encoding='utf-8')
        text = re.sub(r'(?ms)^```.*?^```[^\n]*', '', text)
        for match in re.finditer(r'\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)\)', text):
            target = match[1].strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (source.parent/unquote(parsed.path)).resolve()
            if root not in path.parents or not path.exists():
                raise ValueError('missing or escaping link: '+document+' -> '+target)
            checked += 1
    return {'local_targets_checked': checked, 'external_urls_checked': False,
            'anchors_checked': False, 'syntax_scope': 'inline links outside backtick fences'}
