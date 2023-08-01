import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer
import subprocess
import hashlib
import requests
import os

class MarkdownTranslator:
    def __init__(self, deepl_key):
        self.deepl_endpoint = "https://api-free.deepl.com/v2/translate"
        self.deepl_key = deepl_key

    def translate(self, html, lang_from, lang_to):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "auth_key": self.deepl_key,
            "text": html,
            "source_lang": lang_from,
            "target_lang": lang_to,
            "tag_handling": "xml",
        }

        response = requests.post(self.deepl_endpoint, headers=headers, data=data)
        translated_text = response.json()
        return translated_text['translations'][0]['text']

    @staticmethod
    def html_to_markdown(html_text):
        # Retrieve javscript file location inside python module
        module_dir = os.path.dirname(os.path.abspath(__file__))
        js_file = os.path.join(module_dir, 'html-converter.js')

        # Call javscript library with node to convert html in markdown
        converter = subprocess.Popen(['node', js_file], \
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        markdown, _ = converter.communicate(input=html_text)
        return markdown

    @staticmethod
    def markdown_to_html(markdown_text):
        return mistletoe.markdown(markdown_text)

    @staticmethod
    def markdown_ast(markdown_text):
        return mistletoe.Document(markdown_text)

    @staticmethod
    def ast_render(ast):
        with MarkdownRenderer() as renderer:
            return renderer.render(ast)

    def standardize(self, raw_markdown):
        """
        Uniform content of raw user markdown by using both converter tools, from
        markdown to html to markdown.

        Standardize markdown list, titles, etc. for hash generation.
        """
        mistletoe_html = self.markdown_to_html(raw_markdown)
        turndown_markdown = self.html_to_markdown(mistletoe_html)
        return turndown_markdown

    def generate_hash(self, ast):
        """ Create hashes for each block of a markdown AST. """
        hash_list = []
        for children in ast.children:
            content = self.ast_render(children)
            hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            hash_list.append(hash)
        return hash_list
