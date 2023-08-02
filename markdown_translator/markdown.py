import mistletoe
from mistletoe.markdown_renderer import MarkdownRenderer
import subprocess
import hashlib
import os
from .translators import translate_deepl

class Markdown:
    """
    Layer to manipulate and translate markdown text through its abstract syntax
    tree. Possibility to update translated files to use with versionning.

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
    def __init__(self, text="", filename=None, type="md", hashes=[]):
        self.blocks = {}

        if filename:
            with open(filename) as file_stream:
                text = file_stream.read()

        if type == "html":
            text = self.html_to_markdown(text)

        self._split_markdown(text)
        if hashes:
            self._initialize_hashes(hashes)

    def save(self, filename):
        """Render markdown content into a file."""
        with open(filename, "w") as file_stream:
            print(self, file=file_stream)

    def translate(self, lang_to, lang_from=None):
        """
        Translate markdown content using a third-party service.

        Available languages depend on used translator. If not specified,
        source language may be detected.

        See translators.py for available tools.
        """
        html_translation = translate_deepl(self.html, lang_to, lang_from)
        markdown_conversion = self.__class__(
                                    html_translation,
                                    type="html",
                                    hashes=self.hashes,
                                        )
        self.blocks.update(markdown_conversion.blocks)

    def update(self, new_version, lang_to, lang_from=None):
        """ Update a translated markdown file with its new version. """
        # Retrieve modified content to modify only these blocks
        diff_translations = new_version - self
        diff_translations.translate(lang_to, lang_from)

        # Start from the number of blocks the new version, add translated content
        new_blocks = new_version.blocks.copy()
        new_blocks.update(diff_translations.blocks)

        # Retrieve already translated content of the old version
        for hash in new_blocks.keys():
            if hash in self.hashes:
                new_blocks[hash] = self[hash]

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

        # Call javscript library with node to convert html in markdown
        converter = subprocess.Popen(['node', js_file], \
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        markdown, _ = converter.communicate(input=html_text)
        return markdown

    @property
    def hashes(self):
        """ Get all blocks hashes of a markdown text, represent its structure."""
        return list(self.blocks.keys())

    @property
    def html(self):
        """ Get HTML representation of the markdown """
        return mistletoe.markdown(str(self))

    def _initialize_hashes(self, hashes):
        """ Replace blocks hashes with a new set (for translated files). """
        if len(self.blocks) != len(hashes):
            err_msg = "Hash error : having {} block, {} hashes to setup."
            raise Exception(err_msg.format(len(self.blocks), len(hashes)))

        refreshed_blocks = {}
        for new_hash, content in zip(hashes, self.blocks.values()):
            refreshed_blocks[new_hash] = content
        self.blocks = refreshed_blocks

    def _split_markdown(self, markdown_text):
        """ Parse markdown content to divide into blocks, by title, paragraph... """
        self.blocks = {}

        ast = mistletoe.Document(markdown_text)
        for block in ast.children:
            block_content = self._ast_render(block)
            block_hash = hashlib.md5(block_content.encode()).hexdigest()
            self.blocks[block_hash] = block_content

    @staticmethod
    def _ast_render(ast):
        with MarkdownRenderer() as renderer:
            return renderer.render(ast).strip()

    def _hashes_render(self, hash_list):
        return "\n\n".join(self[hash] for hash in hash_list)

    def __getitem__(self, block_hash):
        return self.blocks.get(block_hash)

    def __setitem__(self, block_hash, new_content):
        self.blocks[block_hash] = new_content

    def __sub__(self, old_version):
        diff_hashes = set(self.hashes) - set(old_version.hashes)
        return Markdown(self._hashes_render(diff_hashes))

    def __str__(self):
        return self._hashes_render(self.hashes)
