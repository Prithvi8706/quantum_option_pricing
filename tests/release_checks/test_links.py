import pytest
from research.release_checks.links import verify_links


def test_links_spaces_and_fences(tmp_path):
    (tmp_path / "a b.md").write_text("target", encoding="utf-8")
    p = tmp_path / "index.md"
    p.write_text(
        "[ok](a%20b.md)\n[external](https://example.com)\n```\n[x](missing)\n```", encoding="utf-8"
    )
    assert verify_links(tmp_path, ["index.md"])["local_targets_checked"] == 1
    p.write_text("[bad](../outside)", encoding="utf-8")
    with pytest.raises(ValueError, match="escaping"):
        verify_links(tmp_path, ["index.md"])
