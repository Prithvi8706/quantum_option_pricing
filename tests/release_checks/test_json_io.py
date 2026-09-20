import pytest
from research.release_checks.json_io import read


@pytest.mark.parametrize('text', ['{"x":1,"x":2}', '[NaN]', '[Infinity]', '[-Infinity]', '[1e999]'])
def test_ambiguous_json_is_rejected(tmp_path, text):
    path = tmp_path/'data.json'
    path.write_text(text, encoding='utf-8')
    with pytest.raises(ValueError):
        read(path)


def test_valid_nested_json(tmp_path):
    path = tmp_path/'data.json'
    path.write_text('{"x":[1,null,false]}', encoding='utf-8')
    assert read(path) == {'x': [1, None, False]}
