from unittest.mock import patch, mock_open
from pypro.config import ConfigParserHandler


str_file = """
[General]
root_projects_dir: path/to/projects/dir

[Analize]
custom_prefixes: __,.,#
"""


class TestConfigParserHandler:

    def test_when_read_a_value(self):
        handler = ConfigParserHandler(str_file)
        assert handler.read('Analize', 'custom_prefixes') == '__,.,#'

    def test_when_write_a_value(self):
        handler = ConfigParserHandler(str_file)
        handler.write('General', 'root_projects_dir', 'Pepe')
        assert handler.read('General', 'root_projects_dir') == 'Pepe'

    def test_when_save_changes(self):
        """When mock open, mock the open functionality inside
        the function that I testing. This test is not finish.
        """
        handler = ConfigParserHandler(str_file)
        mocked_open = mock_open()
        with patch('builtins.open', mocked_open, create=True):
            with open('fake_file', 'w') as ff:
                handler.save(ff)
        assert mocked_open.called


class TestJsonHandler:
    pass
