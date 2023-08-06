import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer
import subprocess
import hashlib
import pathlib
import os
from .translators import translate_deepl
from .renderers import CodeDisabledHTMLRenderer
from .configuration import config

class Markdown:
    """
    Layer to manipulate and translate markdown text through its abstract syntax
    tree. Possibility to update translated files to use with versioning.

    Split content into blocks manipulable blocks, based on hashes.

    Usage examples:
    >>> markdown_obj = Markdown("## Good title")
    >>> markdown_obj.translate(lang_to="FR", lang_from="EN")
    >>> markdown_obj.update(new_version, lang_to="FR")
    >>>
    >>> block_hash = markdown_obj.hashes[0]
    >>> markdown_obj[block_hash] = "Title replacement"
    >>> markdown_obj.save("filename.md")
    """
    def __init__(self, text="", filename="", hashes=[]):
        self.blocks = {}
        self.hashes = []
        self.filename = pathlib.Path(filename)

        if self.filename.is_file():
            text = self.filename.read_text()

        self._split_markdown(text.strip())
        if hashes:
            self._initialize_hashes(hashes)

    def save(self, filename=None):
        """Render markdown content into a file."""
        if filename is None:
            filename = self.filename
        filename = pathlib.Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.write_text(str(self) + "\n")

    def delete(self):
        self.filename.unlink(missing_ok=True)

    def translate(self, lang_to, lang_from=None):
        """
        Translate markdown content using a third-party service.

        Available languages depend on used translator. If not specified,
        source language may be detected.

        See translators.py for available tools.
        """
        html_translation = translate_deepl(self.html, lang_to, lang_from)

        markdown_conversion = self.__class__(
                                    self.html_to_markdown(html_translation),
                                    hashes=self.hashes,
                                        )
        self.blocks.update(markdown_conversion.blocks)
        self._edit_links(lang_to)

    def update(self, new_version, lang_to, lang_from=None):
        """ Update a translated markdown file with its new version. """
        # Retrieve modified content to translate only these blocks
        if (diff_translations := new_version - self) is None:
            return
        diff_translations.translate(lang_to, lang_from)

        # Start from the number of blocks of the new version, add translated content
        new_blocks = new_version.blocks.copy()
        new_blocks.update(diff_translations.blocks)

        # Retrieve already translated content of the old version
        for hash in new_blocks.keys():
            if hash in self.hashes:
                new_blocks[hash] = self[hash]

        self.blocks = new_blocks
        self.hashes = new_version.hashes

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

        # Call javscript library with node to convert html in markdown
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

    def _initialize_hashes(self, hashes):
        """ Replace blocks hashes with a new set (for translated files). """
        if len(self.blocks) != len(hashes):
            err_msg = f"{self.filename} Hash error: "
            err_msg += "having {} block, {} hashes to setup."
            raise Exception(err_msg.format(len(self.blocks), len(hashes)))

        refreshed_blocks = {}
        for new_hash, content in zip(hashes, self.blocks.values()):
            refreshed_blocks[new_hash] = content
        self.blocks = refreshed_blocks

    def _split_markdown(self, markdown_text):
        """ Parse markdown content to divide into blocks, by title, paragraph... """
        self.blocks = {}
        self.hashes = []

        ast = mistletoe.Document(markdown_text)
        for block in ast.children:
            block_content = self._ast_render(block)
            block_hash = hashlib.md5(block_content.encode()).hexdigest()
            self.blocks[block_hash] = block_content
            self.hashes.append(block_hash)

    def _edit_links(self, extension):
        """
        Modify markdown links of an entire document to create subfolder with
        translations. To configure with EDIT_LINKS and EXCLUDE_URLS settings.

        Edit only absolute path, example : /abs/path -> /en/abs/path
        """
        # Transform markdown blocks into ast to edit links inside it.
        for hash in self.blocks:
            block_ast = mistletoe.Document(self[hash])
            self._edit_ast_links(block_ast, extension)
            self.blocks[hash] = self._ast_render(block_ast)

    def _edit_ast_links(self, ast, extension):
        """ Explore and modify recursively all (nested) links of an entire ast. """
        for token in ast.children:
            if self._is_editable_link(token):
                token.target = os.path.join("/" + extension, token.target[1:])

            if hasattr(token, 'children'):
                self._edit_ast_links(token, extension)

    @staticmethod
    def _is_editable_link(ast_token):
        if config.EDIT_LINKS == False: return False
        if not isinstance(ast_token, mistletoe.span_token.Link): return False
        if not ast_token.target.startswith("/"): return False

        for exclude_url in config.EXCLUDE_URLS:
            if ast_token.target.startswith(exclude_url): return False
        return True

    @staticmethod
    def _ast_render(ast):
        with MarkdownRenderer() as renderer:
            return renderer.render(ast).strip()

    def _hashes_render(self, hash_list):
        return "\n\n".join(self[hash] for hash in hash_list)

    def __getitem__(self, block_hash):
        return self.blocks.get(block_hash)

    def __setitem__(self, block_hash, new_content):
        if block_hash not in self.hashes:
            self.hashes.append(block_hash)
        self.blocks[block_hash] = new_content

    def __sub__(self, old_version):
        diff_hashes = set(self.hashes) - set(old_version.hashes)
        if len(diff_hashes) == 0:
            return None
        return Markdown(self._hashes_render(diff_hashes))

    def __eq__(self, other):
        return self.hashes == other.hashes

    def __str__(self):
        return self._hashes_render(self.hashes)
