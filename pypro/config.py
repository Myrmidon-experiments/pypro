import json
from configparser import ConfigParser
from exceptions import HandlerNotImplement


class ConfigFile:

    def __init__(self, file_handler):
        self.methods = ('read', 'write')
        self.file_handler = file_handler

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


class ConfigParserHandler:

    def __init__(self, file_):
        self.parser = ConfigParser()
        self.parser.read(file_)

    def read(self, section, item_name):
        return self.parser[section][item_name]

    def write(self, section, item_name, input_):
        self.parser[section][item_name] = input_


class JsonHandler:

    def __init__(self, file_):
        pass

    def read(self, section, item_name):
        pass

    def write(self, section, item_name, input_):
        pass

"""
with open('config_example.json', 'r') as f:
    config = json.load(f)

a = ""
for i in config['General']['project_structure']:
    print(i)
    a += i + '\n'

print("###")
print(a)
"""
import sys

for i in sys.path:
    print(i)
