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

def convert_to_dict(directory):
    """Converts the folder structure starting from the given directory to a dictionary."""
    directory = Path(directory)
    structure = {}
    for path in sorted(directory.iterdir()):
        if path.is_dir():
            structure[path.name] = convert_to_dict(path)
        else:
            with open(path, 'r') as file:
                try:
                    structure[path.name] = file.read().strip()
                except UnicodeDecodeError:
                    structure[path.name] = "...binary..."
    return structure

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
