import os
from pypro.exceptions import PathNotExists
from pypro.initializers import possibles_vcs
from pypro.utils import my_cd
from subprocess import call, STDOUT
from shutil import copy, which


class StructureAnalizer:
    """Class docstring
    """

    def __init__(self, custom_prefixes=None):
        if custom_prefixes:
            self.exclude_prefixes = custom_prefixes.split(',')
        else:
            self.exclude_prefixes = []
        self.structure = ""

    def analize_dir_structure(self, path):
        if not os.path.isdir(path):
            raise PathNotExists("Dir does not exists")
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
                if filename != '':
                    self.structure += os.path.join(dirpath[basename_index:],
                                                   filename) + '\n'

    def _check_prefixes(self, to_check):
        if to_check == '__init__.py':
            return False
        return to_check.startswith(tuple(self.exclude_prefixes))

    def restructure(self, replace=False):
        basename = self.structure.split('\n')[0][:-1]
        dirname = 'project_name'
        if replace:
            return dirname + self.structure.replace(basename, '+')[1:].rstrip()
        return self.structure.replace(basename, dirname).rstrip()


vcs = tuple(filter(lambda x: len(x) < 4, possibles_vcs))
command_vcs = dict(zip(vcs, ('status', 'status', 'root', 'info')))


def analize_vcs(path, path_for_copy_files):
    """Docstring for analize_vcs.
    """
    if not (os.path.isdir(path) and os.path.isdir(path_for_copy_files)):
        raise PathNotExists

    def handle_ignore_file(vcs, dest, svn_flag=False):
        ignore_file = '.' + vcs + 'ignore'
        if svn_flag:
            pass  # svn ignore files stuff here
        elif os.path.isfile(ignore_file):
            copy(ignore_file, dest)

    with my_cd(path):
        for k, v in command_vcs.items():
            svn_flag = True if k == 'svn' else False
            if which(k) and call([k, v], stderr=STDOUT,
                                 stdout=open(os.devnull, 'w')) == 0:
                handle_ignore_file(k, path_for_copy_files, svn_flag)
                return k
        return
