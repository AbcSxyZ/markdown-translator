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
        self.DEEPL_KEY = ""
        self.SOURCE_LANG = ""
        self.DEST_LANG = []

        self.VERBOSE = True
        self.CODE_TRANSLATED = False
        self.EDIT_LINKS = True
        self.KEEP_CLEAN = True

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
            self._setattr(key.upper(), self._parse_value(value))

    def load_ini(self, ini_path='settings.ini'):
        parser = configparser.ConfigParser()
        parser.read(ini_path)
        for key, value in parser.items('DEFAULT'):
            self._setattr(key.upper(), self._parse_value(value))

    def load_environment(self):
        for key, value in os.environ.items():
            key = key.upper()
            if hasattr(self, key):
                self._setattr(key, self._parse_value(value))

    def _parse_value(self, value):
        """ Convert a setting value to a list or boolean if applicable."""
        if isinstance(value, str):
            if ',' in value:
                value = [item.strip() for item in value.split(',')]
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
        return value

    def _setattr(self, attribute, value):
        """Set an attribute, ensuring that lists do not contain empty strings."""
        attribute = attribute.upper()
        if not hasattr(self, attribute):
            raise MarkdownTranslatorError(f"Invalid configuration : {attribute}")
        if isinstance(value, list):
            value = [item for item in value if item != ""]
        setattr(self, attribute, self._parse_value(value))

config = Configuration()