import pathlib
from markdown_translator import Markdown
from .configuration import config

class RepositoryTranslator:
    """
    Manager for automatic translations of versioned Markdown files in a
    repository or folder. Replicate repository architecture in translated
    folders.

    Warning: Do not manipulate translation folder for versioning, prefer copies.

    Usage example:
    >>> # Selected languages are defined in settings
    >>> RepositoryTranslator("src_folder", "dest_folder").update()
    """
    BACKUP_DIRECTORY = "backup"
    TRANSLATIONS_DIRECTORY = "translations"

    def __init__(self, source, destination):
        self.source = pathlib.Path(source)
        self.destination = pathlib.Path(destination)
        self.backup_folder = self.destination / self.BACKUP_DIRECTORY
        self.translations_folder =  self.destination / self.TRANSLATIONS_DIRECTORY

        self.files = []
        self._collect_files()

    def update(self):
        """ Generates versioned translations from the source folder. """
        for file_infos in self.files:
            if file_infos["backup"] == file_infos["origin"]:
                continue

            for lang in config.DEST_LANG:
                file_infos[lang].update(
                                file_infos["origin"],
                                lang_to=lang,
                                lang_from=config.SOURCE_LANG
                                )
                if config.VERBOSE:
                    path = file_infos["origin"].filename
                    print(f"{lang} translated: {path.relative_to(self.source)}")

            file_infos["backup"].blocks = file_infos["origin"].blocks
            file_infos["backup"].hashes = file_infos["origin"].hashes
        self._save_translations()

    def _collect_files(self):
        """
        Retrieve all the files to be translated from the source folder with
        their corresponding translation files, either existing or supposed.
        """
        for file in self._discover(self.source, absolute=True):
            relative_source = file.relative_to(self.source)

            file_infos = {
                "origin" : Markdown(filename=file),
                "backup" : Markdown(filename=self.backup_folder / relative_source),
                }
            for lang in config.DEST_LANG:
                translation = self.translations_folder / lang / relative_source
                file_infos[lang] = Markdown(
                    filename=translation,
                    hashes=file_infos["backup"].hashes if translation.exists() else [],
                        )
            self.files.append(file_infos)

    def _discover(self, folder, absolute=False):
        """
        List all filenames from a folders (source folder, backup, translations...)
        on which the RepositoryTranslator will perform manipulations.
        """
        tracked_files = {file for file in folder.rglob("*") if self._valid_file(file)}
        if not absolute:
            tracked_files = {file.relative_to(folder) for file in tracked_files}
        return tracked_files

    @staticmethod
    def _valid_file(file):
        if not file.is_file() or file.name in config.EXCLUDE_FILES:
            return False
        return file.suffix == ".md" or file.name in config.INCLUDE_FILES

    def _save_translations(self):
        if config.KEEP_CLEAN:
            self._clean()

        for file_infos in self.files:
            file_infos["backup"].save()
            for lang in config.DEST_LANG:
                file_infos[lang].save()

    def _clean(self):
        """ Delete untracked files and folders from a previous version. """
        managed_folders = [self.backup_folder]
        for lang in config.DEST_LANG:
            managed_folders.append(self.translations_folder / lang)

        for folder in managed_folders:
            # Remove files available only in a previous version
            delete_list = self._discover(folder) - self._discover(self.source)
            for unwanted_file in delete_list:
                pathlib.Path(folder / unwanted_file).unlink()

            # Remove empty directories
            for sub_folder in folder.rglob('*'):
                if sub_folder.is_dir() and not any(sub_folder.iterdir()):
                    sub_folder.rmdir()
