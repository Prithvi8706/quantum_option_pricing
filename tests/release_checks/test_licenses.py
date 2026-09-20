import pytest
from research.release_checks.licenses import license_inventory


def test_presence_is_not_legal_clearance(tmp_path):
    (tmp_path/'LICENSE').write_text('Notice', encoding='utf-8')
    result = license_inventory(tmp_path, ['LICENSE'])
    assert result['files'][0]['bytes'] == 6
    assert not result['compatibility_review_complete']
    with pytest.raises(ValueError):
        license_inventory(tmp_path, ['LICENSE', 'LICENSE'])
