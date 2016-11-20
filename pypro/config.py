"""Help on module config:

This module contains the current classes to load and manipulate
the content of a config file (scheme file).
"""

from configparser import ConfigParser
from pypro.exceptions import HandlerNotImplement


class ConfigFile:
    """Class used to change the current state of the config file
    (scheme file) through the implementation for the file type
    (.ini, .json, .yml, etc.) called Handler."""

    def __init__(self, file_handler_cls, file_):
        """ConfigFile __init__ method:

        Args:
            file_handler_cls (class): The class of the Handler.
            file_ (str): The config name.
        """

        self.methods = ('read', 'write', 'save')
        """Methods that the Handler must be implement."""

        self.file_ = file_
        with open(file_) as f:
            self.file_handler = file_handler_cls(f.read())

    @property
    def file_handler(self):
        """Class name of the implemented Handler for the config file,
        must be implement the previously named methods. If not the
        HandlerNotImplement exception is raised.
        """
        return self._file_handler

    @file_handler.setter
    def file_handler(self, real_file_handler):
        for method in self.methods:
            if not hasattr(real_file_handler, method):
                raise HandlerNotImplement
        self._file_handler = real_file_handler

    def read_config_item(self, section, item_name):
        """
        Args:
            section (str): Config file section.
            item_name: Item of the current section on the config file.
        Returns:
            The content of the given item_name
        Raises:
            KeyError: If section or item_name does not exists
        """
        return self.file_handler.read(section, item_name)

    def write_config_item(self, section, item_name, input_):
        """
        Read the content of a item on the current section.

        Args:
            section (str): Config file section.
            item_name (str): Item of the current section on the config file.
            input_ (str): The content.
        Raises:
            KeyError: If section or item_name does not exists
        """
        self.file_handler.write(section, item_name, input_)

    def save_changes(self):
        """
        Save the changes made to the file."""
        self.file_handler.save(self.file_)


class ConfigParserHandler:
    """Handler for the .ini file type, use the ConfigParser module."""

    def __init__(self, file_content):
        self.parser = ConfigParser()
        self.parser.read_string(file_content)

    def read(self, section, item_name):
        return self.parser[section][item_name]

    def write(self, section, item_name, input_):
        self.parser.set(section, item_name, input_)

    def save(self, file_):
        with open(file_, 'w') as f:
            self.parser.write(f)
