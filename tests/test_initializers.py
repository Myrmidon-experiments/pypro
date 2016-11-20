import pytest
import os
import sys
from pypro.exceptions import PathNotExists, SchemeConfigWrong
from pypro.initializers import create_structure, init_vcs, init_venv
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
        with pytest.raises(SchemeConfigWrong):
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


class TestInitVCS:

    def test_when_vcs_not_supported(self):
        from io import StringIO
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            init_vcs('gitt', '/some/false/loc')
            output = out.getvalue().strip()
            assert output == "Vcs not supported."
        finally:
            sys.stdout = saved_stdout

    def test_when_location_not_exists(self):
        with pytest.raises(FileNotFoundError):
            init_vcs('git', '/some/false/loc')

    def test_when_vcs_init_without_ignore_file(self):
        with patch('os.chdir') as mock_chdir, \
                patch('pypro.initializers.call') as mock_call:
            mock_call.return_value = 0
            init_vcs('git', '/some/false/loc')
            args, kwargs = mock_call.call_args
            assert args[0] == ['git', 'init']

    def test_when_vcs_init_with_ignore_file(self):
        pass


class TestInitVenv:

    @patch('os.getenv')
    def test_when_env_variable_workon_home_not_exists(self, mock_getenv):
        mock_getenv.return_value = None
        with pytest.raises(Exception):
            init_venv('any_name')

    @patch('os.getenv')
    def test_when_workon_home_exists(self, mock_getenv):
        expected_cmd = 'virtualenv --python=python3 {}/{}'.format(
            '/path/to/virtualenvs', 'any_name')
        mock_getenv.return_value = '/path/to/virtualenvs'
        with patch('pypro.initializers.call') as mock_call, \
                patch('pypro.initializers.which') as mock_which:
            mock_which.return_value = 'python3'
            init_venv('any_name')
            mock_call.assert_called_with(expected_cmd, shell=True)

    def test_when_options_is_wrong_defined(self):
        wrong_options = "option1,option2"
        with pytest.raises(SchemeConfigWrong):
            init_venv('any_name', '/path/to/virtualenvs',
                      options=wrong_options)

    @patch('os.getenv')
    def test_when_options_is_well_defined(self, mock_getenv):
        options = 'no-pip,download'
        mock_getenv.return_value = '/path/to/virtualenvs'
        expected_cmd = 'virtualenv --python=python3 {}/{} {}'.format(
            '/path/to/virtualenvs', 'any_name', '--no-pip --download')
        with patch('pypro.initializers.call') as mock_call, \
                patch('pypro.initializers.which') as mock_which:
            mock_which.return_value = 'python3'
            init_venv('any_name', options=options)
            mock_call.assert_called_with(expected_cmd, shell=True)

    @patch('os.getenv')
    def test_when_install_dependencies_from_rqes(self, mock_getenv):
        m = mock_open(read_data='tada')
        mock_getenv.return_value = '/path/to/virtualenvs'
        expected_exec = '/path/to/virtualenvs/any_name/bin/activate_this.py'
        with patch('pypro.initializers.call') as mock_call, \
                patch('builtins.exec') as mock_exec, \
                patch('builtins.open', m, create=True) as mo:
            init_venv('any_name', path_to_rqes='rqes.txt')
            mo.assert_called_once_with(expected_exec)
            mock_exec.assert_called_with('tada')
            mock_call.assert_called_with(['pip', 'install', '-r', 'rqes.txt'])

    def test_when_rqes_not_founded(self):
        """print statement"""
        pass
