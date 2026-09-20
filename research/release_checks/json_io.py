"""Strict evidence JSON: duplicate keys and nonfinite literals are errors."""
import json
from pathlib import Path


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key: '+key)
        result[key] = value
    return result


def _invalid(value):
    raise ValueError('nonfinite JSON number: '+value)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      object_pairs_hook=_pairs, parse_constant=_invalid)
