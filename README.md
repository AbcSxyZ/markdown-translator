# Markdown Translator
**[Development mode, prototype creation]**

Translate versionned markdown files using DeepL.

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

1. **Clone the repository locally:**
```shell
git clone https://github.com/AbcSxyZ/markdown_translator.git
```

2. **Create and configure your `config.py` (with API key), following `config-example.py` variables.**

3. **Run some code !**
```python
from markdown_translator import Markdown

markdown_text = """
## First title to translate

This is a paragraph with content to translate.
"""

markdown_obj = Markdown(markdown_text)
markdown_obj.translate(lang_to="FR", lang_from="EN")
markdown_obj.save("translated-text.md")
print(translated_md)
```
See source code for available functions as it is in development.
## License

Project licensed under [GNU Affero General Public License](/LICENSE) (GNU AGPL).
