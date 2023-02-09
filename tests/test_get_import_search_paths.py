import os
from nile_verifier.main import get_import_search_paths
from unittest.mock import patch


def test_none_cairo_path_param():
    result = get_import_search_paths(None)
    assert len(result) == 2

    cwd = os.getcwd()
    assert result[0] == cwd
    assert "site-packages" in result[1]


def test_empty_cairo_path_param():
    result = get_import_search_paths("")
    assert len(result) == 2

    cwd = os.getcwd()
    assert result[0] == cwd
    assert "site-packages" in result[1]


def test_cairo_path_param():
    result = get_import_search_paths("aaa:/bbb")
    assert len(result) == 4

    cwd = os.getcwd()
    assert result[0] == os.path.join(cwd, "aaa")
    assert result[1] == "/bbb"
    assert result[2] == cwd
    assert "site-packages" in result[3]


def test_env_var():
    with patch.dict(os.environ, {"CAIRO_PATH":"ccc:/ddd"}, clear=True):
        result = get_import_search_paths(None)
        assert len(result) == 4

        cwd = os.getcwd()
        assert result[0] == os.path.join(cwd, "ccc")
        assert result[1] == "/ddd"
        assert result[2] == cwd
        assert "site-packages" in result[3]


def test_all():
    with patch.dict(os.environ, {"CAIRO_PATH":"ccc:/ddd"}, clear=True):
        result = get_import_search_paths("aaa:/bbb")
        assert len(result) == 6

        cwd = os.getcwd()
        assert result[0] == os.path.join(cwd, "aaa")
        assert result[1] == "/bbb"
        assert result[2] == os.path.join(cwd, "ccc")
        assert result[3] == "/ddd"
        assert result[4] == cwd
        assert "site-packages" in result[5]
