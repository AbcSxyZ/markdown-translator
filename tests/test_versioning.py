import markdown_translator
from markdown_translator import Markdown, adapters, RepositoryTranslator
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

@disable_translation
@pytest.mark.parametrize("mode", adapters.hashes.options - {"disabled"})
def test_versioning_standardized(tmp_path, create_markdown_file, mode):
    update_content = """
First title
===========

+ A list

Second title updated
----------------
    """
    backup_translation = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "e5cc3ab82f1a30ad26090d480b04714b": "* A list [translated]",
        "c64528a60571e4fd165cf97f212e7be2": "## Second title [translated]",
    }
    expected_blocks = {
        "378cc1d0bb9779ff6c7ee1bffae4571b": "# First title [translated]",
        "e5cc3ab82f1a30ad26090d480b04714b": "* A list [translated]",
        "dd6c68887a8306bc38ca2a9815639f5e": "## Second title updated",
    }

    test_structure = {
        'somefile.md': update_content,
    }

    ## Prepare base file for testing
    # Settings
    lang = "fr"
    source_folder = tmp_path / "source"
    dest_folder = tmp_path / "destination"
    translation_path = dest_folder / lang / "somefile.md"

    dest_folder.mkdir()
    adapters.hashes.select(mode, dest_folder)

    # Create source folder for RepositoryTranslator
    create_structure(source_folder, test_structure)

    # Create old translation
    translation_path_content = "\n\n".join(backup_translation.values())
    create_markdown_file(translation_path_content, path=translation_path)
    adapters.hashes.set(translation_path, list(backup_translation.keys()))

    hashes = adapters.hashes.get(translation_path)

    ## Perform test action
    markdown_translator.config(dest_lang=[lang])
    RepositoryTranslator(source_folder, dest_folder).update()

    ## Control results
    translated_md = Markdown(filename=translation_path, restore_hashes=True)
    assert translated_md.blocks.childrens == expected_blocks
