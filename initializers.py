import os


def create_structure(name, structure=None,
                     location='/home/cactus/Escritorio/test_pypro'):
    real_structure = structure.replace('project_name', name)
    dirs = (d for d in real_structure.split('\n') if d.endswith('/'))
    files = (f for f in real_structure.split('\n')
             if not f.endswith('/') and f)

    for directory in dirs:
        os.makedirs(os.path.join(location, directory))

    for file_ in files:
        open(os.path.join(location, file_), 'a').close()


def init_vcs():
    pass


def init_venv():
    pass
