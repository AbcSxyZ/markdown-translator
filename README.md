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

markdown_translator.config(deepl_key=DEEPL_KEY)

markdown_obj = markdown_translator.Markdown(markdown_text)
markdown_obj.translate(lang_to="FR", lang_from="EN")
markdown_obj.save("translated-text.md")
print(markdown_obj)
```
To update an existing translated file:
```python
old_version = Markdown(filename="backup.md")
# Hashes of the old (non-translated) version are needed to manipulates blocks
fr_version = Markdown(filename="FR-version.md", hashes=old_version.hashes)
new_version = Markdown(filename="update.md")

fr_version.update(new_version, lang_to="FR", lang_from="EN")
```
To manage translations of all Markdown files within a folder :
```python
import markdown_translator

markdown_translator.config(
        deepl_key=DEEPL_KEY,
        dest_lang=["fr"],
        include_files=["include1", "file2"],
        edit_links=False,
        #...
      )

repo = markdown_translator.RepositoryTranslator("src-folder", "dest-folder")
repo.update()
```
See source code for available functions and options as it is in development.
## License

Project licensed under [GNU Affero General Public License](/LICENSE) (GNU AGPL).
