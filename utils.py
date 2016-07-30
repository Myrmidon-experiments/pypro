import os
import configparser


class StructureAnalizer:
    """Class docstring
    """

    def __init__(self):
        self.exclude_prefixes = ['__', '.']
        self.structure = ""

    # Not finish yet
    def analize(self, path=os.getcwd()):
        if path.endswith('/'):
            path = path[:-1]
        basename_index = path.find(os.path.basename(path))
        for dirpath, dirnames, filenames in os.walk(path):
            filenames = [filename
                         for filename in filenames
                         if not self._check_prefixes(filename)]
            dirnames[:] = [dirname
                           for dirname in dirnames
                           if not self._check_prefixes(dirname)]

            self.structure += dirpath[basename_index:] + '/\n'
            for filename in filenames:
                self.structure += os.path.join(dirpath[basename_index:],
                                               filename) + '\n'

    def _check_prefixes(self, to_check):
        return to_check.startswith(tuple(self.exclude_prefixes))

    def restructure(self, replace=False, replace_with='+'):
        basename = self.structure.split('\n')[0][:-1]
        return self.structure.replace(basename, 'new_project')


class ConfigFile:

    def __init__(self, reader_writer):
        self.methods = ('read', 'write')
        self.reader_writer = reader_writer

    @property
    def reader_writer(self):
        return self._reader_writer

    @reader_writer.setter
    def reader_writer(self, real_reader_writer):
        for method in self.methods:
            if not hasattr(real_reader_writer, method):
                raise Exception("Make my own exception for this")
        self._reader_writer = real_reader_writer

    def read_config_item(self, section, item_name):
        return self.reader_writer.read(section, item_name)

    def write_config_item(self, section, item_name, input_):
        self.reader_writer.write(input_)


obj2 = StructureAnalizer()
obj2.analize('/home/cactus/Devel/pypro')


print(obj2.restructure())
