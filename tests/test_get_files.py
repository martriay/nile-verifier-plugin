from nile_verifier.main import get_files, get_import_search_paths


def test_get_files():
    result = get_files("tests/resources/contracts/A.cairo", get_import_search_paths("tests/resources/contracts:tests/resources/lib"))
    assert len(result) == 3

    assert "namespace A" in result['A.cairo']
    assert "namespace B" in result['subdir/B.cairo']
    assert "namespace C" in result['C.cairo']