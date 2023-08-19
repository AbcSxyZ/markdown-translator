# Markdown Translator
**[Development mode, prototype creation]**

Automatic translation for versioned Markdown files and repositories.

## Installation

Get an [API key from DeepL](https://support.deepl.com/hc/en-us/articles/360020695820-Authentication-Key) by creating an account.

The project use both Python and Node.Js, with dependencies for each language.

**Node.Js setup :**
```shell
# Node installation
sudo apt-get install nodejs npm

# Node dependencies
npm install turndown
```

**Python setup :**
```shell
pip install requests mistletoe
```

## Getting Started

To translate a single Markdown file
```python
import markdown_translator

markdown_text = """
## First title to translate

This is a paragraph with content to translate.
"""

markdown_translator.config(deepl_key="YOUR-DEEPL-KEY")

source_md = markdown_translator.Markdown(markdown_text)
translated_md = source_md.translate(lang_to="FR", lang_from="EN")
translated_md.save("translated-text.md")
print(translated_md)
```
To update an existing translated file:
```python
# Require to enable versioning
markdown_translator.config(versioning="sql")
markdown_translator.config.set_hashes_adapter(".")

# Perform your first translation as explained previously.
# [first translations...]

# Then to update an already translated file
translated_md = Markdown(filename="translated-text.md", restore_hashes=True)
new_version = Markdown(filename="update.md")

translated_md.update(new_version, lang_to="FR", lang_from="EN")
```

To manage translations of all Markdown files within a folder :
```python
import markdown_translator

markdown_translator.config(
        deepl_key=DEEPL_KEY,
        dest_lang=["fr"],
        include_files=["include1", "file2"],
        edit_links=False,
        versioning="sql",
        #...
      )

repo = markdown_translator.RepositoryTranslator("src-folder", "dest-folder")
repo.update()
```

See source code for available functions and options as it is in development.
## Tests

You need to install `pytest` and `decorator` pip packages in order to execute tests.

API key is needed for some tests. You should configure a `translations.ini` file, see `translations.template.ini`.
```bash
python -m pytest
```

## License

Project licensed under [GNU Affero General Public License](/LICENSE) (GNU AGPL).
