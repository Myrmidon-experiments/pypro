import pytest
from unittest.mock import patch, mock_open
from pypro.config import ConfigParserHandler, ConfigFile, JsonHandler
from pypro.exceptions import HandlerNotImplement


str_file = """[General]
root_projects_dir: path/to/projects/dir

[Analize]
custom_prefixes: __,.,#
"""


@pytest.fixture
def my_instance_cp():
    return ConfigParserHandler(str_file)


class TestConfigFile:

    def test_when_handler_has_not_right_methods(self):
        with pytest.raises(HandlerNotImplement):
            m = mock_open(read_data='fake_data')
            with patch('builtins.open', m, create=True):
                ConfigFile(JsonHandler, 'fake_file.ini')

    def test_when_read_a_value(self):
        m = mock_open(read_data=str_file)
        with patch('builtins.open', m, create=True):
            cf = ConfigFile(ConfigParserHandler, 'fake_file.ini')
            assert cf.read_config_item(
                'General', 'root_projects_dir') == 'path/to/projects/dir'

    def test_when_write_a_value(self):
        m = mock_open(read_data=str_file)
        with patch('builtins.open', m, create=True):
            cf = ConfigFile(ConfigParserHandler, 'fake_file.ini')
            cf.write_config_item('General', 'root_projects_dir', 'Pepe')
            assert cf.read_config_item(
                'General', 'root_projects_dir') == 'Pepe'

    def test_when_save_changes(self):
        m = mock_open(read_data=str_file)
        with patch('builtins.open', m, create=True):
            cf = ConfigFile(ConfigParserHandler, 'fake_file.ini')
            cf.write_config_item('General', 'root_projects_dir', 'Pepe')
            cf.save_changes()
        m.assert_called_with('fake_file.ini', 'w')


class TestConfigParserHandler:

    def test_when_read_a_value(self, my_instance_cp):
        assert my_instance_cp.read('Analize', 'custom_prefixes') == '__,.,#'

    def test_when_write_a_value(self, my_instance_cp):
        my_instance_cp.write('General', 'root_projects_dir', 'Pepe')
        assert my_instance_cp.read('General', 'root_projects_dir') == 'Pepe'

    def test_when_save_changes(self, my_instance_cp):
        m = mock_open()
        with patch('builtins.open', m, create=True):
            my_instance_cp.save('fake_file.ini')

        m.assert_called_once_with('fake_file.ini', 'w')
