from pathlib import Path
import pytest
import markdown_translator
from markdown_translator import translators, RepositoryTranslator
from utils_tests import *

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Global configuration for RepositoryTranslator tests."""
    markdown_translator.config(versioning="sql")

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
    result_structure = convert_to_dict(source_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_simple(tmp_path):
    test_structure = {
        'somefile.md': '# Title',
    }
    expected_structure = {
        'hashes.db' : "...binary...",
        'fr': {
            'somefile.md': '# Title',
            },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_with_subfolder(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
        },
        'anotherfile.md': '# Title Outside Subfolder',
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
            'anotherfile.md': '# Title Outside Subfolder',
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_two_languages(tmp_path):
    test_structure = {
        'somefile.md': '# Title',
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'somefile.md': '# Title',
        },
        'es': {
            'somefile.md': '# Title',
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr", "es"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

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
        'hashes.db' : '...binary...',
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
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(dest_lang=["fr", "es"])
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_ignore(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
            'ignored_file' : "A string for a test.",
            'ignored_folder' : {
                "useless" : "really useless",
            }
        },
        'anotherfile.md': '# Title Outside Subfolder',
        'ignored_file2.py' : "import life.cheats",
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
            'anotherfile.md': '# Title Outside Subfolder',
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(
                dest_lang=["fr"],
                include_files=[],
                exclude_files=[],
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_include(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
            'ignored_file' : "A string for a test.",
            'used_folder' : {
                "usefull" : "really usefull",
            }
        },
        'anotherfile.md': '# Title Outside Subfolder',
        'used_file.py' : "import life.cheats",
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
                'used_folder' : {
                    "usefull" : "really usefull",
                }
            },
            'anotherfile.md': '# Title Outside Subfolder',
            'used_file.py' : "import life.cheats",
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(
                dest_lang=["fr"],
                include_files=["usefull", "used_file.py"],
                exclude_files=[],
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_exclude(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
            'ignored_file.md' : "A string for a test.",
        },
        'anotherfile.md': '# Title Outside Subfolder',
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(
                dest_lang=["fr"],
                include_files=[],
                exclude_files=["ignored_file.md", "anotherfile.md"],
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_mix_include_exclude_2lang(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder',
            'ignored_file' : "A string for a test.",
            'used_folder' : {
                "usefull" : "really usefull",
                "secret.md" : "password1234567890",
            }
        },
        'anotherfile.md': '# Title Outside Subfolder',
        'used_file.py' : "import life.cheats",
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
                'used_folder' : {
                    "usefull" : "really usefull",
                }
            },
            'used_file.py' : "import life.cheats",
        },
        'es': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
                'used_folder' : {
                    "usefull" : "really usefull",
                }
            },
            'used_file.py' : "import life.cheats",
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)

    markdown_translator.config(
                dest_lang=["fr", "es"],
                include_files=["usefull", "used_file.py"],
                exclude_files=["secret.md", "anotherfile.md"],
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_keep_clean(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder (updated)',
            'new_version.md' : 'Usefull paragraph',
        },
        'anotherfile.md': '# Title Outside Subfolder (updated)',
        'new_version2.md' : "`Usefull code`",
    }
    old_structure = {
        'fr': {
            'subfolder': {
                'somefile.md': '# Titre de sous-dossier',
                'old_version.md' : 'Paragraphe inutile',
            },
            'anotherfile.md': '# Titre en dehors de sous-dossier',
            'old_version2.md' : "`Code inutile`",
        },
        'es': {
            'subfolder': {
                'somefile.md': '# Title in Subfolde',
                'old_version.md' : 'Useless paragraph',
            },
            'anotherfile.md': '# Title Outside Subfolder',
            'old_version2.md' : "`Useless code`",
        }
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder (updated)',
                'new_version.md' : 'Usefull paragraph',
            },
            'anotherfile.md': '# Title Outside Subfolder (updated)',
            'new_version2.md' : "`Usefull code`",
        },
        'es': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder (updated)',
                'new_version.md' : 'Usefull paragraph',
            },
            'anotherfile.md': '# Title Outside Subfolder (updated)',
            'new_version2.md' : "`Usefull code`",
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)
    create_structure(dest_folder, old_structure)

    markdown_translator.config(
                dest_lang=["fr", "es"],
                include_files=[],
                exclude_files=[],
                keep_clean=True,
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure

@disable_translation
def test_repo_translator_content_update(tmp_path):
    test_structure = {
        'subfolder': {
            'somefile.md': '# Title in Subfolder (updated 1)',
        },
        'anotherfile.md': '# Title Outside Subfolder (updated 2)',
        'not-updated.md': 'Still same paragraph.'
    }
    old_structure = {
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
            'anotherfile.md': '# Title Outside Subfolder',
            'not-updated.md': 'Still same paragraph.'
        },
        'es': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder',
            },
            'anotherfile.md': '# Title Outside Subfolder',
            'not-updated.md': 'Still same paragraph.'
        }
    }
    expected_structure = {
        'hashes.db' : '...binary...',
        'fr': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder (updated 1)',
            },
            'anotherfile.md': '# Title Outside Subfolder (updated 2)',
            'not-updated.md': 'Still same paragraph.'
        },
        'es': {
            'subfolder': {
                'somefile.md': '# Title in Subfolder (updated 1)',
            },
            'anotherfile.md': '# Title Outside Subfolder (updated 2)',
            'not-updated.md': 'Still same paragraph.'
        },
    }
    source_folder = str(tmp_path / "source")
    dest_folder = str(tmp_path / "destination")
    create_structure(source_folder, test_structure)
    create_structure(dest_folder, old_structure)

    markdown_translator.config(
                dest_lang=["fr", "es"],
                include_files=[],
                exclude_files=[],
                keep_clean=True,
                )
    repo = RepositoryTranslator(source_folder, dest_folder)
    repo.update()

    result_structure = convert_to_dict(dest_folder)
    assert result_structure == expected_structure
