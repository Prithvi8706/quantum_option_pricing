"""Compare deterministic JSON separately from acquisition metadata."""
import json
from .json_io import read
from .paths import normalized, within


def compare_replay(first, second):
    excluded = {'planned.json', 'complete.json', 'timings.json'}
    a = set(normalized(read(first/'complete.json')['sha256']))-excluded
    b = set(normalized(read(second/'complete.json')['sha256']))-excluded
    if a != b or not {'results.json', 'inputs.json'} <= a:
        raise ValueError('replay inventory differs or mandatory results missing')
    exact_bytes = True
    for name in sorted(a):
        left, right = within(first, name), within(second, name)
        # Serialization keeps booleans distinct from integers, unlike Python ==.
        values = [json.dumps(read(p), sort_keys=True, allow_nan=False) for p in (left, right)]
        if values[0] != values[1]:
            raise ValueError('deterministic replay differs: '+name)
        exact_bytes &= left.read_bytes() == right.read_bytes()
    return {'compared': sorted(a), 'exact_json': True, 'exact_bytes': exact_bytes,
            'excluded_from_equality': sorted(excluded)}
