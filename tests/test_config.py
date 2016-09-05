from unittest.mock import patch, mock_open
from pypro.config import ConfigParserHandler
from io import StringIO


str_file = """
[General]
project_structure:
 project_name/
 +/docs/
 +/main.py
root_projects_dir: path/to/projects/dir

[Analize]
custom_prexifes: separado por comas
"""


class TestConfigParserHandler:

    handler = ConfigParserHandler('../resources/config_example')

    def test_when_read_a_value(self):
        value_readed = self.handler.read('General', 'root_projects_dir')
        assert value_readed == 'path/to/projects/dir'

    def test_2(self):
        with patch('pypro.config.ConfigParserHandler.read'):
            pass

    def test_when_write_a_value(self):
        pass
