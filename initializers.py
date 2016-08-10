import os
from subprocess import call
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


def init_venv(name, py_3=True, location=None, **options):
    command_line = 'virtualenv --python=/usr/bin/python3'
    if not py_3:
        command_line = 'virtualenv --python=/usr/bin/python2.7'
    if location:
        command_line += ' ' + os.path.join(location, name)
    else:
        command_line += ' ' + os.path.join(os.getenv('WORKON_HOME'), name)

    # Almost finished. Lack PROMPT and EXTRA-SEARCH-DIR
    for option in options.keys():
        command_line += ' --' + option

    print(command_line)
    # call(command_line, shell=True)


def handle_options_venv():
    pass


d = dict()
b = 'no-download,no-pip,no-wheel'
for opt in b.split(','):
    d[opt] = 1

init_venv('pepe', **d)
