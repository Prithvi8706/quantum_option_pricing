"""Inspect installed versions without installing or upgrading anything."""
from importlib.metadata import PackageNotFoundError, version
import platform


def compare_environment(required, lookup=version):
    if not required:
        raise ValueError('dependency scope required')
    differences = []
    for name, expected in sorted(required.items()):
        try:
            actual = lookup(name)
        except PackageNotFoundError:
            actual = None
        if actual != expected:
            differences.append({'package': name, 'expected': expected, 'actual': actual})
    return {'python': platform.python_version(), 'packages_checked': len(required),
            'matches': not differences, 'differences': differences,
            'scope': 'version inventory only; not wheel hashes or ABI portability'}
