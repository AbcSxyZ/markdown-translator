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

Clone the repository locally:
```shell
git clone https://github.com/AbcSxyZ/markdown_translator.git
```

Basic example to translate some markdown content:
```python
from markdown_translator import MarkdownTranslator

translator = MarkdownTranslator("YOUR-DEEPL-API-KEY")

markdown = """
## First title to translate

This is a paragraph with content to translate.
"""

converted_html = translator.markdown_to_html(markdown)
translated_html = translator.translate(converted_html, "EN", "FR")
translated_md = translator.html_to_markdown(translated_html)

print(translated_md)
```
DeepL need to receive html content to avoid breaking markdown syntax during
translations.

## License

Project licensed under [GNU Affero General Public License](/LICENSE) (GNU AGPL).
