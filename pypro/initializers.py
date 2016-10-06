import os
from subprocess import call, STDOUT
from shutil import which, copy
from pypro.utils import my_chdir
from pypro.exceptions import PathNotExists


possibles_vcs = ('git', 'bzr', 'bazaar', 'hg',
                 'mercurial', 'svn', 'subversion')


def create_structure(name, structure, location):
    """Create the directory structure with the given name as root directory
    under given location.
    """
    if not os.path.isdir(structure):
        raise PathNotExists
    real_structure = structure.replace('project_name', name)
    dirs = (d for d in real_structure.split('\n') if d.endswith('/'))
    files = (f for f in real_structure.split('\n') if not f.endswith('/'))
    try:
        for directory in dirs:
            os.makedirs(os.path.join(location, directory))

        for file_ in files:
            open(os.path.join(location, file_), 'a').close()
        return os.path.join(location, name)

    except FileExistsError:
        print('Directory or file already exists')


def init_vcs(vcs, location, ignore_file_path=""):
    """Initialize the given version control system on the given location."""
    if vcs in possibles_vcs:
        if vcs in ('svn', 'subversion'):
            call(['svnadmin', 'create', location])
            if ignore_file_path:
                pass  # Do svn stuff here
        else:
            with my_chdir(location):
                call([vcs, 'init'], stderr=STDOUT,
                     stdout=open(os.devnull, 'w'))
            if ignore_file_path:
                copy(ignore_file_path, location)
    else:
        print("Vcs not supported.")


def init_venv(name, location=None, py_3=True, path_to_rqes='',
              options=None, **kwargs):
    """Initialize a virtualenv with the given name on the location if given,
    if not, location is $WORKON_HOME env variable.
    """
    command_line = 'virtualenv --python={pyversion}'
    if py_3:
        command_line = command_line.format(pyversion=which('python3'))
    else:
        command_line = command_line.format(pyversion=which('python2.7'))
    try:
        if location and os.path.isdir(location):
            command_line += ' ' + os.path.join(location, name)
        else:
            location = ' ' + os.path.join(os.getenv('WORKON_HOME'), name)
            command_line += location
    except TypeError:
        raise Exception("Location or WORKON_HOME env variable does not exists")

    for option in options.split(','):
        command_line += ' --' + option

    call(command_line, shell=True)
    if path_to_rqes:
        try:
            venv = os.path.join(location, name, 'bin/activate_this.py')
            with open(venv) as activate_file:
                exec(activate_file.read())
                call(['pip', 'install', '-r', path_to_rqes])
        except FileNotFoundError:
            print("Requirements not found.")
