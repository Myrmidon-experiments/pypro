import os
from subprocess import call


possibles_vcs = ('git', 'bzr', 'bazaar', 'hg',
                 'mercurial', 'svn', 'subversion')


def init_structure(name, structure=None,
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
    if vcs in possibles_vcs:
        pass
    else:
        print("Vcs not supported")


def init_venv(name, py_3=True, location=None, path_to_rqes=None, **options):
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

    # print(command_line)
    call(command_line, shell=True)


# Define a right way to handle options with parameters
def handle_options_venv(options, options_with_param=None):
    options_as_dict = dict()
    for option in options.split(','):
        options_as_dict[option] = 1
    return options_as_dict
