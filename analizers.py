import os


class StructureAnalizer:
    """Class docstring
    """

    def __init__(self):
        self.exclude_prefixes = ['__', '.']
        self.structure = ""

    def analize_dir_structure(self, path=os.getcwd()):
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

    def restructure(self, replace=False, repl_with='+'):
        basename = self.structure.split('\n')[0][:-1]
        dirname = 'project_name'
        if replace:
            return dirname + self.structure.replace(basename, repl_with)[1:]
        return self.structure.replace(basename, dirname)
