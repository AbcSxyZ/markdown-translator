import markdown_translator
from markdown_translator import RepositoryTranslator
from markdown_translator.hashes_adapters import *
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

@pytest.mark.parametrize("adapter_class", [
    BlockHashesJSONAdapter,
    BlockHashesSQLAdapter,
])
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

@pytest.mark.parametrize("adapter_class", [
    BlockHashesJSONAdapter,
    BlockHashesSQLAdapter,
])
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

@pytest.mark.parametrize("adapter_class", [
    BlockHashesJSONAdapter,
    BlockHashesSQLAdapter,
])
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


@pytest.mark.parametrize("mode", [
    "json",
    "sql",
])
def test_repo_translator_json_adapter(tmp_path, mode):
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
    abs_filename = str(dest_folder / lang / filename)
    create_structure(str(source_folder), test_structure)

    markdown_translator.config(dest_lang=[lang], versioning=mode)
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_hashes = markdown_translator.config.hashes_adapter.get(abs_filename)

    assert result_hashes == expected_hashes
