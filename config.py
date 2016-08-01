import configparser


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


a = configparser.ConfigParser()
a.read('example_config_file')
print(a.sections())
for a in a['General']['project_structure'].split('\n'):
    if a == '':
        print('Fine')
