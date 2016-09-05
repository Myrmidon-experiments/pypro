import json
from configparser import ConfigParser
from pypro.exceptions import HandlerNotImplement


class ConfigFile:

    def __init__(self, file_handler_cls, file_):
        self.methods = ('read', 'write', 'save')
        self.file_ = file_
        with open(file_):
            self.file_handler = file_handler_cls(file_.read())

    @property
    def file_handler(self):
        return self._file_handler

    @file_handler.setter
    def file_handler(self, real_file_handler):
        for method in self.methods:
            if not hasattr(real_file_handler, method):
                raise HandlerNotImplement
        self._file_handler = real_file_handler

    def read_config_item(self, section, item_name):
        return self.file_handler.read(section, item_name)

    def write_config_item(self, section, item_name, input_):
        self.file_handler.write(section, item_name, input_)

    def save_changes(self):
        self.file_handler.save(self.file_)


class ConfigParserHandler:

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


class JsonHandler:

    def __init__(self, file_content):
        pass

    def read(self, section, item_name):
        pass

    def write(self, section, item_name, input_):
        pass
