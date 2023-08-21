import pytest
import pathlib

@pytest.fixture
def create_markdown_file(tmp_path):
    def _create_markdown_file(content, path=None):
        if path is not None:
            markdown_file = pathlib.Path(path)
        else:
            markdown_file = tmp_path / "test.md"
        markdown_file.parent.mkdir(exist_ok=True, parents=True)
        markdown_file.write_text(content)
        return str(markdown_file)
    return _create_markdown_file
