import os
from subprocess import call
from shutil import which


possibles_vcs = ('git', 'bzr', 'bazaar', 'hg',
                 'mercurial', 'svn', 'subversion')


def init_structure(name, structure=None,
                   location='/home/cactus/Escritorio/test_pypro'):
    real_structure = structure.replace('project_name', name)
    dirs = (d for d in real_structure.split('\n') if d.endswith('/'))
    files = (f for f in real_structure.split('\n')
             if not f.endswith('/'))

    try:
        for directory in dirs:
            os.makedirs(os.path.join(location, directory))

        for file_ in files:
            open(os.path.join(location, file_), 'a').close()

    except FileExistsError:
        print('Directory or file already exists')


def init_vcs(vcs, ignore_file=None):
    if vcs in possibles_vcs:
        pass
    else:
        print("Vcs not supported")


def init_venv(name, location=None, py_3=True, path_to_rqes='', options=None):
    """Docstring for init_venv here...
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
