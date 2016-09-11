import pytest
from unittest.mock import patch
from pypro.analizers import StructureAnalizer
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


class TestAnalizeVCS:
    pass
