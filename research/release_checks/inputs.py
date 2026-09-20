"""Bridge named-role and flat-path input manifests without dropping entries."""
from .hashes import verify_hashes
from .paths import normalized


def input_entries(data):
    if set(data) == {'paths', 'sha256'}:
        if set(data['paths']) != set(data['sha256']):
            raise ValueError('input role inventory mismatch')
        names = list(data['paths'].values())
        if len(set(names)) != len(names):
            raise ValueError('duplicate input roles resolve to one path')
        data = {name: data['sha256'][role] for role, name in data['paths'].items()}
    return normalized(data)


def verify_inputs(root, data, required):
    entries = input_entries(data)
    if not required or set(entries) != set(required):
        raise ValueError('input inventory differs from release scope')
    return verify_hashes(root, entries)
