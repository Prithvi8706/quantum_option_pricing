import pytest
from research.release_checks.hashes import digest
from research.release_checks.sources import verify_sources


def test_protocol_is_separately_verified(tmp_path):
    (tmp_path/'source').write_bytes(b'code')
    (tmp_path/'protocol').write_bytes(b'fixed')
    plan = {'git_head': 'a'*40, 'source_sha256': {'source': digest(tmp_path/'source')},
            'config': {'protocol_sha256': digest(tmp_path/'protocol')}}
    assert verify_sources(tmp_path, plan, 'protocol', ['source'])['source_files'] == 1
    (tmp_path/'protocol').write_bytes(b'changed')
    with pytest.raises(ValueError, match='protocol'):
        verify_sources(tmp_path, plan, 'protocol', ['source'])
    with pytest.raises(ValueError, match='mandatory'):
        verify_sources(tmp_path, plan, 'protocol', ['missing'])
