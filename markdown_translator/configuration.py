import configparser
import os
import sys
from .exceptions import MarkdownTranslatorError

class Configuration:
    """
    Interface for dynamic configuration of the module, allowing settings from
    various entries: configure method, ini file or/and environment variables.

    Friendly reminder: never share confidential crendentials online!
    """
    def __init__(self):
        # Default configuration settings
        self.API_KEY = ""
        self.TRANSLATION_ENGINE = "deepl"
        self.SOURCE_LANG = ""
        self.DEST_LANG = []

        # Available versioning method (see adapters) : json, sql.
        self.VERSIONING = "disabled"

        self.VERBOSE = True
        self.CODE_TRANSLATED = False
        self.KEEP_CLEAN = False

        self.EDIT_LINKS = True
        self.URLS_ROOT = "/"

        self.INCLUDE_FILES = []
        self.EXCLUDE_FILES = []
        self.EXCLUDE_URLS = []

        self.load_ini()
        self.load_environment()

    @property
    def values(self):
        """ Retrieve all available configuration settings. """
        return self.__dict__

    def __call__(self, **kwargs):
        """ Change any available setting of the configuration. """
        for key, value in kwargs.items():
            self._setattr(key, value)

    def load_ini(self, ini_path='translations.ini'):
        parser = configparser.ConfigParser()
        parser.read(ini_path)
        for key, value in parser.items('settings'):
            self._setattr(key, value)

    def load_environment(self):
        for key, value in os.environ.items():
            if hasattr(self, key.upper()):
                self._setattr(key, value)

    def _setattr(self, attribute, value):
        """Set an attribute, ensuring that lists do not contain empty strings."""
        attribute = attribute.upper()
        if not hasattr(self, attribute):
            raise MarkdownTranslatorError(f"Unexisting configuration : {attribute}")

        try:
            attribute_type = type(getattr(self, attribute))
            value = self._parse_value(value, attribute_type)
            setattr(self, attribute, value)
        except MarkdownTranslatorError:
            raise MarkdownTranslatorError(f"Invalid configuration for {attribute}: {value}")

    def _parse_value(self, value, attribute_type):
        """ Convert a value to the expected type of the setting."""
        if type(value) == attribute_type:
            return value
        elif type(value) != str:
            raise MarkdownTranslatorError

        if attribute_type == bool:
            return self._get_boolean(value)
        elif attribute_type == list:
            return [item.strip() for item in value.split(',')] if value else []

    @staticmethod
    def _get_boolean(value):
        true_values = ["true", "1", "yes", "on"]
        false_values = ["false", "0", "no", "off"]

        if value.lower() in true_values:
            return True
        elif value.lower() in false_values:
            return False
        raise MarkdownTranslatorError

config = Configuration()
