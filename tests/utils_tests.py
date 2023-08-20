import decorator
import pytest
from pathlib import Path
from markdown_translator import config, adapters

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
    def wrapper(test_func, *args, **kwargs):
        # Switch (and backup) of the original translation function
        configured_engine = config.TRANSLATION_ENGINE
        config(translation_engine="disabled")

        # Run test
        result = test_func(*args, **kwargs)

        # Restore translation function
        config(translation_engine=configured_engine)
        return result
    return decorator.decorator(wrapper, test_func)

def get_hashes_adapters(include_disabled=False):
    adapters_list = []
    for name in adapters.hashes.options:
        if name == "disabled" and not include_disabled:
            continue
        adapters_list.append(adapters.hashes._adapters_list[name])
    return adapters_list
