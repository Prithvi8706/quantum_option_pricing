"""Parse a deliberately restricted exact-version replay dependency inventory."""
import re


def canonical(name):
    return re.sub('[-_.]+', '-', name).lower()


def pins(text):
    result = {}
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9_.-]*)==([A-Za-z0-9][A-Za-z0-9.!+_-]*)', line)
        if not match:
            raise ValueError('only exact package==version pins supported: '+line)
        name, version = canonical(match[1]), match[2]
        if name in result:
            raise ValueError('duplicate dependency: '+name)
        result[name] = version
    if not result:
        raise ValueError('empty dependency inventory')
    return result
