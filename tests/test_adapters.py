import markdown_translator
from markdown_translator import RepositoryTranslator, config, adapters
from markdown_translator.adapters.hashes_adapters import *
from utils_tests import *

def test_adapters_parent_class(tmp_path):
    # Configuration
    filename = "somefile.md"
    reference_hashes = ["hash1", "hash2", "hash3"]
    adapter = BlockHashesAdapter()

    # Test of set and get
    adapter.set(filename, reference_hashes)
    result_hashes = adapter.get(filename)
    assert result_hashes == None

    # Test of deletion
    adapter.delete(filename)
    result_hashes_deleted = adapter.get(filename)
    assert result_hashes_deleted == None

@pytest.mark.parametrize("adapter_class", get_hashes_adapters())
def test_adapters_basic(tmp_path, adapter_class):
    # Configuration
    filename = "somefile.md"
    reference_hashes = ["hash1", "hash2", "hash3"]
    second_reference_hashes = ["hashA", "hashB", "hashC"]
    adapter = adapter_class(tmp_path)

    # Test of set and get
    adapter.set(filename, reference_hashes)
    result_hashes = adapter.get(filename)
    assert result_hashes == reference_hashes

    # Test of update
    adapter.set(filename, second_reference_hashes)
    result_hashes = adapter.get(filename)
    assert result_hashes == second_reference_hashes

    # Test of deletion
    adapter.delete(filename)
    result_hashes_deleted = adapter.get(filename)
    assert result_hashes_deleted == None

@pytest.mark.parametrize("adapter_class", get_hashes_adapters())
def test_adapters_multi_hashes(tmp_path, adapter_class):
    adapter = adapter_class(tmp_path)

    # Store multiple files with hashes
    hash_list = []
    for number in range(10):
        filename = f"somefile-{number}"
        hash_list.append(f"hash-{number}")
        adapter.set(filename, hash_list.copy())

    # Control stored hashes
    reference_hashes = []
    for number in range(10):
        filename = f"somefile-{number}"
        reference_hashes.append(f"hash-{number}")
        result_hashes = adapter.get(filename)
        assert result_hashes == reference_hashes

@pytest.mark.parametrize("adapter_class", get_hashes_adapters())
def test_adapters_unexisting(tmp_path, adapter_class):
    # Configuration
    filename = "somefile.md"
    unexisting_filename = "some-unexisting.md"
    reference_hashes = ["hash1", "hash2", "hash3"]
    adapter = adapter_class(tmp_path)

    # Test part
    adapter.set(filename, reference_hashes)
    result_hashes = adapter.get(unexisting_filename)
    assert result_hashes == None

    # Test of deletion
    adapter.delete(unexisting_filename)

@pytest.mark.parametrize("adapter_class", get_hashes_adapters())
def test_adapters_persistency(tmp_path, adapter_class):
    # Configuration
    filename = "somefile.md"
    reference_hashes = ["hash1", "hash2", "hash3"]
    adapter = adapter_class(tmp_path)
    adapter.set(filename, reference_hashes)
    del adapter

    # Test part
    new_adapter = adapter_class(tmp_path)
    result_hashes = new_adapter.get(filename)
    assert result_hashes == reference_hashes

@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_repo_translator_with_adapter(tmp_path, mode):
    filename = "somefile.md"
    lang = "fr"
    test_structure = {
        filename: '# Title\n\nParagraph',
    }
    expected_hashes = [
        "38cdd67987afb67a4af89ea02044a00e",
        "feaf0a320c3d678ad30dd179b7d21584",
    ]

    source_folder = tmp_path / "source"
    dest_folder = tmp_path / "destination"
    create_structure(str(source_folder), test_structure)

    markdown_translator.config(dest_lang=[lang], versioning=mode)
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_hashes = adapters.hashes.get(filename)

    assert result_hashes == expected_hashes
