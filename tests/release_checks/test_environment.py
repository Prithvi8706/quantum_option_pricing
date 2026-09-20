from importlib.metadata import PackageNotFoundError
from research.release_checks.environment import compare_environment


def test_missing_and_mismatched_versions_are_visible():
    def lookup(name):
        if name == 'missing':
            raise PackageNotFoundError(name)
        return '2'
    result = compare_environment({'missing': '1', 'old': '1', 'ok': '2'}, lookup)
    assert not result['matches']
    assert len(result['differences']) == 2
    assert compare_environment({'ok': '2'}, lookup)['matches']
