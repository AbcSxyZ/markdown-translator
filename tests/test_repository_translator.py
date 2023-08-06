from pathlib import Path
import pytest
import markdown_translator
from markdown_translator import translators, RepositoryTranslator

def create_structure(folder, structure):
    """ Create a directory structure given a folder description. """
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    for name, content in structure.items():
        path = folder / name
        if isinstance(content, dict):
            path.mkdir()
            create_structure(path, content)
        else:
            path.write_text(content + "\n")

def verify_structure(folder, structure):
    """ Verification function of folders architectures for tests. """
    folder = Path(folder)
    for name, content in structure.items():
        path = folder / name
        if isinstance(content, dict):
            assert path.is_dir()
            verify_structure(path, content)
        else:
            assert path.is_file()
            try:
                assert path.read_text().strip() == content.strip()
            except AssertionError as error:
                print(str(path))
                raise error

def translation_hook(html, *args, **kwargs):
    return html

def disable_translation(test_func):
    """ Hook to avoid API calls during testing. """
    @pytest.mark.usefixtures("request")
    def wrapper(request, *args, **kwargs):
        # Access tests fixtures
        tmp_path = request.getfixturevalue('tmp_path')

        # Backup of the original translation function
        translation_function = translators.translate_deepl

        # Run the test with translation disabled and re-enabled
        translators.translate_deepl = translation_hook
        result = test_func(tmp_path)
        translators.translate_deepl = translation_function

        return result
    return wrapper

@disable_translation
def test_create_and_verify_structure(tmp_path):
    """
    Test to verify the creation and verification functions using a predefined structure.
    """
    test_structure = {
        'file1.txt': 'Content of file1',
        'subfolder': {
            'file2.txt': 'Content of file2',
            'subsubfolder': {
                'file3.txt': 'Content of file3'
            }
        }
    }
    expected_structure = test_structure
    source_folder = str(tmp_path / "source")
    create_structure(source_folder, test_structure)
    verify_structure(source_folder, expected_structure)

@disable_translation
def test_repo_translator_simple(tmp_path):
    test_structure = {
        'somefile.md': '# Title',
        'code.py' : 'import life.cheats',
    }
    expected_structure = {
        'backup': {
            'somefile.md': '# Title',
            },
        'translations' : {
            'fr': {
                'somefile.md': '# Title',
                },
            }
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    verify_structure(dest_folder, expected_structure)
