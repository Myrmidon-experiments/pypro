import os
import inspect
from subprocess import call, Popen
from analizers import StructureAnalizer


def create_structure(name, structure=None,
                     location='/home/cactus/Escritorio/test_pypro'):
    real_structure = structure.replace('project_name', name)
    dirs = (d for d in real_structure.split('\n') if d.endswith('/'))
    files = (f for f in real_structure.split('\n')
             if not f.endswith('/') and f)

    try:
        for directory in dirs:
            os.makedirs(os.path.join(location, directory))

        for file_ in files:
            open(os.path.join(location, file_), 'a').close()

    except FileExistsError:
        print('Directory or file already exists')


def init_vcs(vcs, ignore_file=None):
    print('pass')


def init_venv(name, py_3=True, location=None,
              **options):
    command_line = 'virtualenv --python=/usr/bin/python3'
    if not py_3:
        command_line = 'virtualenv --python=/usr/bin/python2.7'
    # TODO: Other options here with **options
    if location:
        command_line += ' ' + os.path.join(location, name)
    else:
        command_line += ' ' + os.path.join(os.getenv('WORKON_HOME'), name)

    print(command_line)
    call(command_line, shell=True)

"""
a = StructureAnalizer()
a.analize_dir_structure()
create_structure('some', structure=a.restructure())

a = inspect.signature(init_venv)
print(type(a))

a.parameters
"""

init_venv('pepe')
