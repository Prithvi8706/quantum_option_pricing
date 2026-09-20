"""Trace precise reported values to JSON evidence without inferring novelty."""
import re
from .json_io import read
from .paths import within


def pointer(data, path):
    if path == '':
        return data
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('absolute JSON pointer required')
    for token in path[1:].split('/'):
        if re.search(r'~(?![01])', token):
            raise ValueError('invalid pointer escape')
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(data, list):
            if not re.fullmatch('0|[1-9][0-9]*', token):
                raise ValueError('invalid array index')
            data = data[int(token)]
        else:
            data = data[token]
    return data


def verify_claims(root, claims):
    ids = [c['id'] for c in claims]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('nonempty unique claim IDs required')
    for claim in claims:
        if claim['kind'] not in ('logical_projection', 'limitation') or not claim['scope']:
            raise ValueError('unsupported claim type or missing scope')
        value = pointer(read(within(root, claim['evidence'])), claim['pointer'])
        if type(value) is not type(claim['expected']) or value != claim['expected']:
            raise ValueError('claim differs from evidence: '+claim['id'])
    return {'claims_checked': len(claims), 'novelty_assessed': False}
