import os
from pypro.exceptions import PathNotExists
from pypro.initializers import possibles_vcs
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

vcs = tuple(filter(lambda x: len(x) < 4, possibles_vcs))
command_vcs = dict(zip(vcs, ('status', 'status', 'root', 'info')))


def analize_vcs(path):
    def handle_ignore_file(vcs, dest, svn_flag=False):
        ignore_file = '.' + vcs + 'ignore'
        if svn_flag:
            pass  # svn ignore files stuff here
        elif os.path.isfile(ignore_file):
            copy(ignore_file, dest)

    dest = "/home/cactus/Escritorio/test_pypro"  # Temporal
    with my_cd(path):
        for k, v in command_vcs.items():
            svn_flag = True if k == 'svn' else False
            if which(k) and call([k, v], stderr=STDOUT,
                                 stdout=open(os.devnull, 'w')) == 0:
                handle_ignore_file(k, dest, svn_flag)
                return k


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
