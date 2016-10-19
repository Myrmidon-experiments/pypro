import pytest
from unittest.mock import patch
from pypro.analizers import StructureAnalizer, analize_vcs
from pypro.exceptions import PathNotExists


@pytest.fixture
def my_instance():
    return StructureAnalizer(custom_prefixes='__,.')


@pytest.fixture
def fake_structure():
    return 'one/\none/file_1\none/file_2\none/some_dir/\none/some_dir/file_3\n'


class TestStructureAnalizer:

    def test_when_analize_non_existent_path(self, my_instance):
        with pytest.raises(PathNotExists):
            my_instance.analize_dir_structure('some/fail/path')

    def test_when_analize_existent_path(self, my_instance, fake_structure):
        with patch('os.walk') as mock_walk, \
                patch('os.path.isdir') as mock_isdir:
            mock_walk.return_value = [
                ('path/one', ['some_dir'], ['file_1', 'file_2']),
                ('path/one/some_dir', [], ['file_3'])
            ]
            mock_isdir.return_value = True
            my_instance.analize_dir_structure('path/one')

            assert mock_isdir.called
            assert mock_walk.called
        assert fake_structure == my_instance.structure

    def test_when_restructure(self, my_instance, fake_structure):
        expected = fake_structure.replace('one', 'project_name').rstrip()
        my_instance.structure = fake_structure.rstrip()
        assert my_instance.restructure() == expected

    def test_when_restructure_with_replace(self, my_instance, fake_structure):
        expected = 'project_name' + \
            fake_structure.replace('one', '+')[1:].rstrip()
        my_instance.structure = fake_structure
        assert my_instance.restructure(replace=True) == expected

    def test_when_restructure_as_tree(self, my_instance, fake_structure):
        expected = 'project_name\n    file_1\n    file_2\n    ' + \
            'some_dir\n        file_3\n'
        my_instance.structure = fake_structure
        assert my_instance.restructure_as_tree() == expected


class TestVCSAnalizer:

    def test_when_analize_with_nonexistent_path(self):
        with pytest.raises(PathNotExists):
            analize_vcs('/some/path', '/other/path')

    @patch('os.path.isdir')
    def test_when_analize_without_ignorefiles(self, mock_isdir):
        mock_isdir.return_value = True
        with patch('os.chdir'), \
                patch('pypro.analizers.which') as mock_which, \
                patch('pypro.analizers.call') as mock_call:
            mock_which.return_value = '/usr/bin/some_vcs'
            mock_call.return_value = 0
            vcs, file_dest, ignore_file_name = analize_vcs(
                '/some/path', '/other/path')
            assert vcs in ('git', 'bzr', 'svn', 'hg')
            assert (file_dest, ignore_file_name) == (None, None)
        assert mock_isdir.called
        assert mock_which.called
        assert mock_call.called

    @patch('os.path.isdir')
    def test_when_analize_with_ignorefiles(self, mock_isdir):
        possible_ignore_file_names = ('.gitignore', '.bzrignore', '.hgignore')
        mock_isdir.return_value = True
        with patch('os.chdir'), \
                patch('pypro.analizers.which') as mock_which, \
                patch('pypro.analizers.copy') as mock_copy, \
                patch('pypro.analizers.call') as mock_call:
            mock_which.return_value = '/usr/bin/some_vcs'
            mock_call.return_value = 0
            mock_copy.return_value = '/other/path'
            vcs, file_dest, ignore_file_name = analize_vcs(
                '/some/path', '/other/path')
        assert vcs in ('git', 'bzr', 'svn', 'hg')
        assert file_dest == '/other/path'
        assert ignore_file_name in possible_ignore_file_names

    @patch('os.path.isdir')
    def test_when_vcs_not_exists(self, mock_isdir):
        mock_isdir.return_value = True
        with patch('os.chdir'), \
                patch('pypro.analizers.which') as mock_which, \
                patch('pypro.analizers.call') as mock_call:
            mock_which.return_value = '/usr/bin/some_vcs'
            mock_call.return_value = 127
            vcs_info = analize_vcs(
                '/some/path', '/other/path')
        assert vcs_info == (None, None, None)
