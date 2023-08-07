import pytest

@pytest.fixture
def create_markdown_file(tmp_path):
    def _create_markdown_file(content):
        markdown_file = tmp_path / "test.md"
        markdown_file.write_text(content)
        return str(markdown_file)
    return _create_markdown_file
