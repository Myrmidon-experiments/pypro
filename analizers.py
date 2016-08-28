import os
from exceptions import PathNotExists
from subprocess import call, STDOUT
from contextlib import contextmanager
from shutil import copy, which


class StructureAnalizer:
    """Class docstring
    """

    def __init__(self, custom_prefixes=None):
        self.exclude_prefixes = ['__', '.']
        self.structure = ""

    def analize_dir_structure(self, path):
        if path is None or not os.path.isdir(path):
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
                self.structure += os.path.join(dirpath[basename_index:],
                                               filename) + '\n'

    def _check_prefixes(self, to_check):
        return to_check.startswith(tuple(self.exclude_prefixes))

    def restructure(self, replace=False):
        basename = self.structure.split('\n')[0][:-1]
        dirname = 'project_name'
        if replace:
            return dirname + self.structure.replace(basename, '+')[1:]
        return self.structure.replace(basename, dirname)


@contextmanager
def my_cd(path):
    prev_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def analize_vcs(path):
    """Similar to analize_vcs2 but more concise
    May be, a dict {'git': (command, function_to_ignore_files)}
    for vcs in command_vcs:
        if which vcs and call
            call function_ignore_files
            return vcs.keys
    """
    pass  # Make a dict with vcs: command; example {'git': 'status'}


def analize_vcs2(path):
    dest = "/home/cactus/Escritorio/test_pypro"  # Temporal
    if not os.path.isdir(path):
        raise PathNotExists("Dir does not exists")
    with my_cd(path):
        if which('git') and call(['git', 'status'], stderr=STDOUT,
                                 stdout=open(os.devnull, 'w')) == 0:
            if os.path.isfile('.gitignore'):
                copy('.gitignore', dest)
            return 'git'
        if which('bzr') and call(['bzr', 'status'], stderr=STDOUT,
                                 stdout=open(os.devnull, 'w')) == 0:
            if os.path.isfile('.bzrignore'):
                copy('.bzrignore', dest)
            return 'bzr'
        if which('hg') and call(['hg', 'root'], stderr=STDOUT,
                                stdout=open(os.devnull, 'w')) == 0:
            if os.path.isfile('.hgignore'):
                copy('.hgignore', dest)
            return 'hg'
        if which('svn') and call(['svn', 'info'], stderr=STDOUT,
                                 stdout=open(os.devnull, 'w')) == 0:
            # Do svn ignore files stuff
            return 'svn'


a = analize_vcs2(os.getcwd())
print(a)
