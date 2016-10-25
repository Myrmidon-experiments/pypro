import pytest
import os
import sys
from pypro.exceptions import PathNotExists, WrongProjectStructure
from pypro.initializers import create_structure
from unittest.mock import patch, mock_open, call


wrong_structure = "bad structure, this is gonna fail"
good_structure = """project_name/
project_name/one/
project_name/one/file_1
project_name/one/some_dir/
project_name/one/some_dir/file_2"""


@pytest.fixture
def any_name_struc():
    var = good_structure.replace('project_name', 'any_name').split('\n')
    new_structure = list()
    for i in range(0, len(var)):
        new_structure.insert(i, os.path.join('/some/false/loc', var[i]))
    return new_structure


class TestCreateStructure:

    def test_when_structure_is_wrong(self):
        with pytest.raises(WrongProjectStructure):
            create_structure('any_name', wrong_structure, '/some/false/loc')

    def test_when_location_not_exists(self):
        with pytest.raises(PathNotExists):
            create_structure('any_name', good_structure, '/some/false/loc')

    @patch('os.path.isdir')
    def test_when_create_a_structure(self, mock_isdir, any_name_struc):
        mock_isdir.return_value = True
        m = mock_open()
        dirs_expected = [
            call(any_name_struc[0]),
            call(any_name_struc[1]),
            call(any_name_struc[3])
        ]
        files_expected = [
            call(any_name_struc[2], 'a'),
            call(any_name_struc[4], 'a')
        ]
        with patch('os.makedirs') as mock_mkdir, \
                patch('builtins.open', m, create=True):
            mock_mkdir.return_value = None
            ret = create_structure(
                'any_name', good_structure, '/some/false/loc')
            assert mock_mkdir.call_args_list == dirs_expected
            assert m.call_args_list == files_expected
            assert ret == '/some/false/loc/any_name'

    @patch('os.path.isdir')
    def test_when_create_a_structure_already_existent(self, mock_isdir):
        from io import StringIO
        saved_stdout = sys.stdout
        mock_isdir.return_value = True
        try:
            out = StringIO()
            sys.stdout = out
            with patch('os.makedirs') as mock_isdir:
                mock_isdir.side_effect = FileExistsError('')
                create_structure('any_name', good_structure, '/some/false/loc')
            output = out.getvalue().strip()
            assert output == "Directory or file already exists"
        finally:
            sys.stdout = saved_stdout
