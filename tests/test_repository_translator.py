from pathlib import Path
import pytest
import markdown_translator
from markdown_translator import translators, RepositoryTranslator
from utils_tests import *

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

@disable_translation
def test_repo_translator_with_subfolder(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
        },
        'anotherfile.md': '# Title Outside Subfolder',
    }
    expected_structure = {
        'backup': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
            'anotherfile.md': '# Title Outside Subfolder',
        },
        'translations': {
            'fr': {
                'subfolder': {
                    'somefile.md': '# Title in Subfolder',
                },
                'anotherfile.md': '# Title Outside Subfolder',
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

@disable_translation
def test_repo_translator_two_languages(tmp_path):
    test_structure = {
        'somefile.md': '# Title',
    }
    expected_structure = {
        'backup': {
            'somefile.md': '# Title',
        },
        'translations': {
            'fr': {
                'somefile.md': '# Title',
            },
            'es': {
                'somefile.md': '# Title',
            },
        }
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr", "es"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    verify_structure(dest_folder, expected_structure)

@disable_translation
def test_repo_translator_nested_folders_with_files_two_languages(tmp_path):
    test_structure = {
        'file0.md': '# Title Level 0',
        'folder1': {
            'file1.md': '# Title Level 1',
            'folder2': {
                'file2.md': '# Title Level 2',
            },
        },
    }
    expected_structure = {
        'backup': {
            'file0.md': '# Title Level 0',
            'folder1': {
                'file1.md': '# Title Level 1',
                'folder2': {
                    'file2.md': '# Title Level 2',
                },
            },
        },
        'translations': {
            'fr': {
                'file0.md': '# Title Level 0',
                'folder1': {
                    'file1.md': '# Title Level 1',
                    'folder2': {
                        'file2.md': '# Title Level 2',
                    },
                },
            },
            'es': {
                'file0.md': '# Title Level 0',
                'folder1': {
                    'file1.md': '# Title Level 1',
                    'folder2': {
                        'file2.md': '# Title Level 2',
                    },
                },
            },
        }
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr", "es"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    verify_structure(dest_folder, expected_structure)
