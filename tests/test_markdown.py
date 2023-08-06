import pathlib
import pytest
from markdown_translator import Markdown, config
from datetime import datetime
import json

def log(content, context=""):
    """ Utils to debug and write tests. """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"{now} : {context}\n"

    with open("tests.log", "a") as logfile:
        print(log_msg, file=logfile)
        if type(content) in [dict, list]:
            content = json.dumps(content, indent=4)
        print(content, file=logfile)

@pytest.fixture
def create_markdown_file(tmp_path):
    def _create_markdown_file(content):
        markdown_file = tmp_path / "test.md"
        markdown_file.write_text(content)
        return str(markdown_file)
    return _create_markdown_file

def test_markdown_save(create_markdown_file):
    content = """# A nice title

With a nice paragraph.
"""
    markdown_file = pathlib.Path(create_markdown_file(""))
    markdown_file.unlink()

    md = Markdown(text=content)
    md.save(markdown_file)
    assert markdown_file.exists()

    writed_content = markdown_file.read_text()
    assert writed_content == content

def test_markdown_delete(create_markdown_file):
    markdown_file = pathlib.Path(create_markdown_file(""))

    assert markdown_file.exists()
    md = Markdown(filename=str(markdown_file))
    md.delete()
    assert not markdown_file.exists()

def test_markdown_block(create_markdown_file):
    content = "# Test title"
    expected_blocks = {
        "c23c32da6aa9560c467665b27cf6218f": "# Test title"
        }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_spaces(create_markdown_file):
    content = """

# Test spaced title



One sentence with extra         space



##### Lost Title

    """
    expected_blocks = {
        "7d8e9c4ae9c5cefb74824609206a9927": "# Test spaced title",
        "e9e61d2bd0c4b5252fbe700eba04e232": "One sentence with extra         space",
        "b57d1617abec91f70b59d497ee470542": "##### Lost Title"
        }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_syntax(create_markdown_file):
    content = """
# Heading 1
## Heading 2
### Heading 3

This is a paragraph with `code`.

- List item 1
- List item 2 with [link](link/to/project)

[Link text](http://example.com)

![Image Alt Text](http://example.com/image.jpg)

```python
code block
```

> Blockquote

**Bold Text** *Italic Text*
    """
    expected_blocks = {
        "0723a75a60f75a0e4b8060ace6dd602c": "# Heading 1",
        "697a79fc42a84ecf965037be2441dbba": "## Heading 2",
        "5ecdc23839268e2187c052103c770832": "### Heading 3",
        "4b8e686f9a4dbe2db2eaaad8d8c45047": "This is a paragraph with `code`.",
        "629ceb8f6b897f33dedf6aa4e04fb07d": "- List item 1\n- List item 2 with [link](link/to/project)",
        "6fe4dbe996c586928fba55b02f0a5d24": "[Link text](http://example.com)",
        "c22828ed0b22491fc511cb92447abf17": "![Image Alt Text](http://example.com/image.jpg)",
        "1b7dc0ef084ade191433e13e1a3c51fe": "```python\ncode block\n```",
        "388407dfdd2b9cb3585fb095e3fb9119": "> Blockquote",
        "a95d391d65d69dd8157cfe8494af5f54": "**Bold Text** *Italic Text*"
        }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_syntax_html(create_markdown_file):
    content = """
# Heading 1
## Heading 2
### Heading 3

This is a paragraph with `code`.

- List item 1
- List item 2 with [link](link/to/project)

[Link text](http://example.com)

![Image Alt Text](http://example.com/image.jpg)

```python
code block
```

> Blockquote

**Bold Text** *Italic Text*
    """

    expected_html = """
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<p>This is a paragraph with <code translate="no">code</code>.</p>
<ul>
<li>List item 1</li>
<li>List item 2 with <a href="link/to/project">link</a></li>
</ul>
<p><a href="http://example.com">Link text</a></p>
<p><img src="http://example.com/image.jpg" alt="Image Alt Text" /></p>
<pre><code translate="no" class="language-python">code block
</code></pre>
<blockquote>
<p>Blockquote</p>
</blockquote>
<p><strong>Bold Text</strong> <em>Italic Text</em></p>
"""
    config(code_translated=False)
    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.html.strip() == expected_html.strip()

def test_markdown_standardization(create_markdown_file):
    content = """
The title
========

- item 1
    + sub-item1
    + sub-item2
        * sub-sub-item1

Broker title
--------------
- One
- entire
- list

# Atx header
    """
    expected_blocks = {
        "341c5ce963599ccc51a82b7a580a1eb2": "# The title",
        "85ce862fd99674e420d59b8f1772ea9e": "* item 1\n  * sub-item1\n  * sub-item2\n    * sub-sub-item1",
        "c72cee9474bc9a459d00b3e86d9deb9a": "## Broker title",
        "dc7c5348f9fc8961531c672b5a32e38f": "* One\n* entire\n* list",
        "112b02633f270b4e7fa3c1969ba9596e": "# Atx header"
        }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    md.standardize()
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_with_html(create_markdown_file):
    content = """
# Test title

<div>
    <iframe width="559" height="315" src="https://www.youtube.com/embed/oq2Oq1J6t70" title="YouTube video player"
    frameborder="-1" allow="accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture;web-share"
    allowfullscreen></iframe>
</div>
"""
    expected_blocks = {
        "c23c32da6aa9560c467665b27cf6218f": "# Test title",
        "bbca0d5933e8b5bf1a189b5516e4af38": "<div>\n<iframe width=\"559\" height=\"315\" src=\"https://www.youtube.com/embed/oq2Oq1J6t70\" title=\"YouTube video player\"\nframeborder=\"-1\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture;web-share\"\nallowfullscreen></iframe>",
        "0a3a0b592b9c285e050805307cee87c2": "</div>"
        }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_with_multi_html(create_markdown_file):
    content = """
#### Test title

<div>
    <iframe width="559" height="315" src="https://www.youtube.com/embed/oq2Oq1J6t70" title="YouTube video player"
    frameborder="-1" allow="accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture;web-share"
    allowfullscreen></iframe>
</div>
#### Splitting title
<div>
    <img src="/media/cc0-images/grapefruit-slice-332-332.jpg"/>
</div>
"""
    expected_blocks = {
        "07bc4579e034b5d785cfe3b68e1c94ae": "#### Test title",
        "bbca0d5933e8b5bf1a189b5516e4af38": "<div>\n<iframe width=\"559\" height=\"315\" src=\"https://www.youtube.com/embed/oq2Oq1J6t70\" title=\"YouTube video player\"\nframeborder=\"-1\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media;gyroscope; picture-in-picture;web-share\"\nallowfullscreen></iframe>",
        "0a3a0b592b9c285e050805307cee87c2": "</div>",
        "3356cf77429ea4e7800748554d0d36f5": "#### Splitting title",
        "a9cdd8c87bdd7c1b1e611bc8eeae8ce6": "<div>\n<img src=\"/media/cc0-images/grapefruit-slice-332-332.jpg\"/>"
    }
    expected_hashes = [
        "07bc4579e034b5d785cfe3b68e1c94ae",
        "bbca0d5933e8b5bf1a189b5516e4af38",
        "0a3a0b592b9c285e050805307cee87c2",
        "3356cf77429ea4e7800748554d0d36f5",
        "a9cdd8c87bdd7c1b1e611bc8eeae8ce6",
        "0a3a0b592b9c285e050805307cee87c2"
        ]

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    assert md.blocks == expected_blocks
    assert md.hashes == expected_hashes

def test_markdown_link_edit(create_markdown_file):
    content = """
First link, edited, [absolute path](/one/absolute/path).

Second link, non edited, [relative path](local/link).

Third link, non edited, [Wikipedia](https://www.wikipedia.org/).
    """
    expected_blocks = {
        "2e3282f35f34e831b0549516d9b3b6ab": "First link, edited, [absolute path](/en/one/absolute/path).",
        "870954ebd85be3346296f6eded1a6bf9": "Second link, non edited, [relative path](local/link).",
        "d7f78cebfe47d371ecd51986fbb846e3": "Third link, non edited, [Wikipedia](https://www.wikipedia.org/)."
    }

    markdown_file = create_markdown_file(content)
    md = Markdown(filename=markdown_file)
    md._edit_links("en")
    assert md.blocks == expected_blocks
    assert md.hashes == list(expected_blocks.keys())

def test_markdown_translate():
    content = "# An easy title"
    expected_blocks = {
        "d766839ca6ea342eb05dba1ce81d1c86": "# Un titre facile"
        }

    md = Markdown(text=content)

    first_hash = md.hashes[0]
    md.translate(lang_to="fr")
    final_hash = md.hashes[0]

    assert md.blocks == expected_blocks
    assert first_hash == final_hash

def test_markdown_basic_update():
    old_backup = Markdown(text="# An easy title")
    old_translated = Markdown(text="# Un titre facile", hashes=old_backup.hashes)
    new_version = Markdown(text="# An easy title\nFirst paragraph\n")

    old_translated.update(new_version, lang_to="fr", lang_from="en")

    expected_blocks = {
        "d766839ca6ea342eb05dba1ce81d1c86": "# Un titre facile",
        "ca045bcbf99e1c9aeac6658ec3788d90": "Premier paragraphe"
        }

    assert old_translated.blocks == expected_blocks
    assert old_translated.hashes == new_version.hashes

def test_markdown_complex_update():
    old_backup_content = """
# A first title

A first paragraph.

## A second heading

Second paragraph.

## A third heading

A third paragraph.
"""
    new_version_content = """
# A first title

A first paragraph.

## A second heading, with a paragraph

Second paragraph.

## A third heading

* A new list.

A third paragraph.
"""
    old_translated_content = """
# Un premier titre

Un premier paragraphe.

## Un deuxième titre

Un deuxième paragraphe.

## Un troisième titre

Un troisième paragraphe.
    """

    expected_blocks = {
        "5b923625584690d2fc07c1c2234bf64f": "# Un premier titre",
        "bddbee052b954ec98004b898b5d6c29e": "Un premier paragraphe.",
        "9fec2ad9fc925e8c25227ff77d9811c2": "## Un deuxi\u00e8me titre, avec un paragraphe",
        "1c43011c2f7619648251ed0e4709bbe4": "Un deuxi\u00e8me paragraphe.",
        "a96299757204ab5c9f8c23a53f2f0daf": "## Un troisi\u00e8me titre",
        "35931c5eb07639cd4d3d053aef43b729": "* Une nouvelle liste.",
        "715292b428b4f0ecbb16b9bd605db3f9": "Un troisi\u00e8me paragraphe."
        }

    old_backup = Markdown(text=old_backup_content)
    old_translated = Markdown(text=old_translated_content, hashes=old_backup.hashes)
    new_version = Markdown(text=new_version_content)

    old_translated.update(new_version, lang_to="fr", lang_from="en")

    assert old_translated.blocks == expected_blocks
    assert old_translated.hashes == new_version.hashes
