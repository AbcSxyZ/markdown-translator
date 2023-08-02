import html
import mistletoe

class CodeDisabledHTMLRenderer(mistletoe.HTMLRenderer):
    """ Disabler of DeepL translation for Markdown code (inline and blocks). """
    def render_block_code(self, token):
        template = '<pre><code translate="no"{attr}>{inner}</code></pre>'
        if token.language:
            attr = ' class="{}"'.format('language-{}'.format(html.escape(token.language)))
        else:
            attr = ''
        inner = self.escape_html_text(token.content)
        return template.format(attr=attr, inner=inner)

    def render_inline_code(self, token):
        template = '<code translate="no">{}</code>'
        inner = self.escape_html_text(token.children[0].content)
        return template.format(inner)
