import pathlib
from . import adapters, Markdown
from .configuration import config

class RepositoryTranslator:
    """
    Manager for automatic translations of versioned Markdown files in a
    repository or folder. Replicate repository architecture in translated
    folders.

    Warning: Do not manipulate translation folders for versioning, prefer copies.

    Usage example:
    >>> # Selected languages are defined in settings
    >>> RepositoryTranslator("src_folder", "dest_folder").update()
    """
    def __init__(self, source, destination):
        self.source = pathlib.Path(source)
        self.destination = pathlib.Path(destination)

        self.destination.mkdir(parents=True, exist_ok=True)
        adapters.hashes.select(config.VERSIONING, self.destination)

    def update(self):
        """ Generates versioned translations from the source folder. """
        if config.KEEP_CLEAN:
            self._clean()

        # Explore all mardown files from the source repository
        for source_path in self._discover(self.source, absolute=True):
            source_md = Markdown(filename=source_path)
            source_md.standardize()
            relative_source = source_path.relative_to(self.source)

            # Retrieve and update translations of the file in each language
            for lang in config.DEST_LANG:
                translated_md = Markdown(
                    filename=relative_source,
                    directory=self.destination / lang,
                    restore_hashes=True,
                        )
                translated_md.update(
                                source_md,
                                lang_to=lang,
                                lang_from=config.SOURCE_LANG
                                )
                if config.VERBOSE and translated_md.is_updated():
                    print(f"{lang} translated: {relative_source}")

                translated_md.save(save_hashes=False)
            adapters.hashes.set(relative_source, source_md.blocks.hashes)

    def _discover(self, folder, absolute=False, is_traduction=False):
        """
        List all filenames from a folders (source folder, backup, translations...)
        on which the RepositoryTranslator will perform manipulations.
        """
        required_files = []
        for file in folder.rglob("*"):
            if self._valid_file(file, is_traduction):
                required_files.append(file)

        if not absolute:
            required_files = [file.relative_to(folder) for file in required_files]
        return set(required_files)

    def _valid_file(self, file, is_traduction):
        if not is_traduction and self._contained(file, config.DEST_LANG): return False
        if self._contained(file, config.EXCLUDE_FILES): return False
        if not file.is_file(): return False

        return file.suffix == ".md" or self._contained(file, config.INCLUDE_FILES)

    @staticmethod
    def _contained(filename, controlled_paths):
        """
        Verify if a filename match a file pattern of an include or exclude list,
        controlling indistinctly files or folders.
        """
        filename_parts = filename.parts
        for path in controlled_paths:
            pattern = pathlib.Path(path).parts
            for index in range(len(filename_parts)):
                if pattern == filename_parts[index:index + len(pattern)]:
                    return True
        return False

    def _clean(self):
        """ Delete untracked files and folders from a previous version. """
        managed_folders = [self.destination / lang for lang in config.DEST_LANG]
        for folder in managed_folders:
            # Remove files available only in a previous version
            delete_list = self._discover(folder, is_traduction=True) - \
                                                    self._discover(self.source)
            for unwanted_file in delete_list:
                pathlib.Path(folder / unwanted_file).unlink()

            # Remove empty directories
            for sub_folder in folder.rglob('*'):
                if sub_folder.is_dir() and not any(sub_folder.iterdir()):
                    sub_folder.rmdir()
