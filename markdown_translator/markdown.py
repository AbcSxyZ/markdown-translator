import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer
import subprocess
import pathlib
import os
from . import adapters
from .renderers import CodeDisabledHTMLRenderer
from .configuration import config
from .markdown_blocks import MarkdownBlocks

class Markdown:
    """
    Layer to manipulate and translate markdown text through its abstract syntax
    tree. Possibility to update translated files to use with versioning.

    Split content into blocks manipulable blocks, based on hashes.
    """
    def __init__(self, text="", filename="", directory=".", restore_hashes=False):
        self.blocks = MarkdownBlocks()
        # Filename could be relative to directory, path ensure file access
        self.filename = self.path = pathlib.Path(filename)
        if directory != ".":
            self.path = directory / self.filename

        if self.path.is_file():
            text = self.path.read_text()

        self._split_markdown(text.strip())
        if restore_hashes:
            old_hashes = adapters.hashes.get(self.filename)
            self.blocks.refresh_hashes(old_hashes)

    def save(self, filename=None, save_hashes=True):
        """ Render markdown content into a file and store hashes. """
        if filename is not None:
            self.filename = self.path = pathlib.Path(filename)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(str(self) + "\n")

        if save_hashes:
            adapters.hashes.set(self.filename, self.blocks.hashes)

    def delete(self):
        self.path.unlink(missing_ok=True)
        adapters.hashes.delete(self.filename)

    def translate(self, lang_to, lang_from=None):
        """
        Translate markdown content using a third-party service.

        Available languages depend on used translator. If not specified,
        source language may be detected.

        See translators.py for available tools.
        """
        html_translation = adapters.translator(self.html, lang_to, lang_from)
        translated_md = Markdown(self.html_to_markdown(html_translation))

        # Keep same hashes from the untranslated version
        translated_md.blocks.refresh_hashes(self.blocks.hashes)

        translated_md._edit_links(lang_to)
        return translated_md

    def update(self, new_version, lang_to, lang_from=None):
        """ Update a translated markdown file with its new version. """
        # Retrieve modified content to translate only these blocks
        if (diff_blocks := new_version.blocks - self.blocks) is None:
            return
        translations = __class__(str(diff_blocks)).translate(lang_to, lang_from)

        # Start from a non-translated state of the new version,
        # then recover old unchanged translations and add new ones.
        new_blocks = new_version.blocks.copy()
        new_blocks.pick_translations(self.blocks)
        new_blocks.pick_translations(translations.blocks)

        self.blocks = new_blocks

    def standardize(self):
        """
        Uniform content of raw user markdown by using both converter tools, from
        markdown to html to markdown.

        Standardize markdown list, titles, etc. for hash generation.
        """
        standardized_markdown = self.html_to_markdown(self.html)
        self._split_markdown(standardized_markdown)

    @staticmethod
    def html_to_markdown(html_text):
        """ Convert HTML representation in pure markdown. """
        # Retrieve javscript file location inside python module
        module_dir = os.path.dirname(os.path.abspath(__file__))
        js_file = os.path.join(module_dir, 'html-converter.js')

        # Call javascript library with node to convert html in markdown
        converter = subprocess.Popen(['node', js_file], \
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        markdown, _ = converter.communicate(input=html_text)
        return markdown

    @property
    def html(self):
        """ Get HTML representation of the markdown """
        # Need of special attributes in HTML to avoid translations on some tags
        if config.CODE_TRANSLATED:
            renderer = mistletoe.HTMLRenderer
        else:
            renderer = CodeDisabledHTMLRenderer
        return mistletoe.markdown(str(self), renderer)

    def _split_markdown(self, markdown_text):
        """ Parse markdown content to divide into blocks, by title, paragraph... """
        self.blocks.clean()

        ast = mistletoe.Document(markdown_text)
        for block in ast.children:
            block_content = self._ast_render(block)
            self.blocks.add(block_content)

    def _edit_links(self, extension):
        """
        Modify markdown links of an entire document to create subfolder with
        translations. To configure with EDIT_LINKS and EXCLUDE_URLS settings.

        Edit only absolute path, example : /abs/path -> /en/abs/path
        """
        # Transform markdown blocks into ast to edit links inside it.
        for hash in self.blocks:
            block_ast = mistletoe.Document(self.blocks[hash])
            self._edit_ast_links(block_ast, extension)
            self.blocks[hash] = self._ast_render(block_ast)

    def _edit_ast_links(self, ast, extension):
        """ Explore and modify recursively all (nested) links of an entire ast. """
        for token in ast.children:
            if self._is_editable_link(token):
                link_parts = (config.URLS_ROOT, extension, token.target[1:])
                token.target = os.path.join(*link_parts)

            if hasattr(token, 'children'):
                self._edit_ast_links(token, extension)

    @staticmethod
    def _is_editable_link(ast_token):
        if config.EDIT_LINKS == False: return False
        if not isinstance(ast_token, mistletoe.span_token.Link): return False
        if not ast_token.target.startswith("/"): return False

        for exclude_url in config.EXCLUDE_URLS:
            if ast_token.target.startswith(exclude_url): return False

        ## Avoid links to translations folders
        if config.URLS_ROOT != "/":
            if ast_token.target.startswith(config.URLS_ROOT): return False
        # README.md could be used as home to the source language
        if ast_token.target.startswith("/README.md"): return False

        base_folder = ast_token.target.split("/")[1]
        for lang in config.DEST_LANG:
            if lang.lower() == base_folder.lower(): return False
        return True

    def is_updated(self):
        return adapters.hashes.get(self.filename) != self.blocks.hashes

    @staticmethod
    def _ast_render(ast):
        with MarkdownRenderer() as renderer:
            return renderer.render(ast).strip()

    def __str__(self):
        return str(self.blocks)
