from markdown_translator import Markdown, config, adapters
from utils_tests import *

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_basic_keep(tmp_path, create_markdown_file, mode):
    adapters.hashes.select(mode, tmp_path)

    update_content = """
# First title

New update
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
    }
    expected_blocks = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "a70bf5b15f959872a625d3adfcbf7781": "New update",

    }

    translation_path = create_markdown_file("\n\n".join(backup_translation.values()))
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    new_version = Markdown(text=update_content)

    translated_md.update(new_version, lang_to="fr", lang_from="en")

    assert translated_md.blocks.childrens == expected_blocks

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_basic_update(tmp_path, create_markdown_file, mode):
    adapters.hashes.select(mode, tmp_path)

    update_content = """
# First title updated.

New update
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
    }
    expected_blocks = {
        "e607f3fb688460f2d6d06600b3acbe36": "# First title updated.",
        "a70bf5b15f959872a625d3adfcbf7781": "New update",

    }

    translation_path = create_markdown_file("\n\n".join(backup_translation.values()))
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    new_version = Markdown(text=update_content)

    translated_md.update(new_version, lang_to="fr", lang_from="en")

    assert translated_md.blocks.childrens == expected_blocks

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_complex_update(tmp_path, create_markdown_file, mode):
    adapters.hashes.select(mode, tmp_path)

    update_content = """
# First title
First paragraph updated
# Second title
Second paragraph updated
# Third title
Third paragraph updated
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "ca045bcbf99e1c9aeac6658ec3788d90": "First paragraph [translated]",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "98930a9738a61e9d977a37da0e9abd5f": "Second paragraph [translated]",
        "cb432d1bddf0f71484e795a62147b741": "# Third title [translated]",
        "fe7b084b0641d005c87539d37cbe2734": "Third paragraph [translated]",
    }
    expected_blocks = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "fe4603a90c67aab668e5e9ac8e0fc491": "First paragraph updated",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "22ebf1c60e3c855fa541123c8287b6de": "Second paragraph updated",
        "cb432d1bddf0f71484e795a62147b741": "# Third title [translated]",
        "a276c0c7a96443afdb9c9758a7a2347b": "Third paragraph updated",
    }

    translation_path = create_markdown_file("\n\n".join(backup_translation.values()))
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    new_version = Markdown(text=update_content)

    translated_md.update(new_version, lang_to="fr", lang_from="en")

    assert translated_md.blocks.childrens == expected_blocks

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_complex_update(tmp_path, create_markdown_file, mode):
    adapters.hashes.select(mode, tmp_path)

    update_content = """
# First title
First paragraph updated
# Second title
Second paragraph updated
# Third title
Third paragraph updated
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "ca045bcbf99e1c9aeac6658ec3788d90": "First paragraph [translated]",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "98930a9738a61e9d977a37da0e9abd5f": "Second paragraph [translated]",
        "cb432d1bddf0f71484e795a62147b741": "# Third title [translated]",
        "fe7b084b0641d005c87539d37cbe2734": "Third paragraph [translated]",
    }
    expected_blocks = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "fe4603a90c67aab668e5e9ac8e0fc491": "First paragraph updated",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "22ebf1c60e3c855fa541123c8287b6de": "Second paragraph updated",
        "cb432d1bddf0f71484e795a62147b741": "# Third title [translated]",
        "a276c0c7a96443afdb9c9758a7a2347b": "Third paragraph updated",
    }

    translation_path = create_markdown_file("\n\n".join(backup_translation.values()))
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    new_version = Markdown(text=update_content)

    translated_md.update(new_version, lang_to="fr", lang_from="en")

    assert translated_md.blocks.childrens == expected_blocks

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_identical_blocks(tmp_path, create_markdown_file, mode):
    adapters.hashes.select(mode, tmp_path)

    update_content = """
# First title
A paragraph updated
# Second title
A paragraph
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "995e012509ca2c118d0548897f01437d": "A paragraph [translated]",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "995e012509ca2c118d0548897f01437d": "A paragraph [translated]",
    }
    expected_blocks = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "c313c4d19d507c404fd5052a3566189f": "A paragraph updated",
        "636188e240e638f5cce290fecb423ecf": "# Second title [translated]",
        "995e012509ca2c118d0548897f01437d": "A paragraph [translated]",
    }

    translation_path = create_markdown_file("\n\n".join(backup_translation.values()))
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    new_version = Markdown(text=update_content)

    translated_md.update(new_version, lang_to="fr", lang_from="en")

    assert translated_md.blocks.childrens == expected_blocks
