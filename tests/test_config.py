import pytest
from unittest.mock import patch, mock_open
from pypro.config import ConfigParserHandler


str_file = """[General]
root_projects_dir: path/to/projects/dir

[Analize]
custom_prefixes: __,.,#
"""


@pytest.fixture
def my_instance():
    return ConfigParserHandler(str_file)


class TestConfigParserHandler:

    def test_when_read_a_value(self, my_instance):
        assert my_instance.read('Analize', 'custom_prefixes') == '__,.,#'

    def test_when_write_a_value(self, my_instance):
        my_instance.write('General', 'root_projects_dir', 'Pepe')
        assert my_instance.read('General', 'root_projects_dir') == 'Pepe'

    def test_when_save_changes(self, my_instance):
        m = mock_open()
        with patch('builtins.open', m, create=True):
            my_instance.save('fake_file.ini')

        m.assert_called_once_with('fake_file.ini', 'w')


class TestJsonHandler:
    pass
