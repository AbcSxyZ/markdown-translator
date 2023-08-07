import pytest
from pathlib import Path
from markdown_translator import translators

def logtest(content, context=""):
    """ Utils to debug and write tests. """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"{now} : {context}\n"

    with open("tests.log", "a") as logfile:
        print(log_msg, file=logfile)
        if type(content) in [dict, list]:
            content = json.dumps(content, indent=4)
        print(content, file=logfile)

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
        translation_function = translators.translate_deepl.__code__

        # Run the test with translation disabled and re-enabled
        translators.translate_deepl.__code__ = translation_hook.__code__
        result = test_func(tmp_path)
        translators.translate_deepl.__code__ = translation_function

        return result
    return wrapper
