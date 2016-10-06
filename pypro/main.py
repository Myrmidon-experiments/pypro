import os
import sys
import pypro.config as cfg
from pypro.cli import get_args
from pypro.analizers import StructureAnalizer
from pypro.initializers import create_structure
from pypro.exceptions import PathNotExists


def _get_config_file(scheme):
    # Because argparse return None if the optional argument it's not used
    if scheme is None:
        scheme = 0
    config_file_name = '.pypro/scheme' + str(scheme)
    dir_config = '.pypro/dir_scheme' + str(scheme)
    config_file_location = os.path.join(os.getenv('HOME'), config_file_name)
    return cfg.ConfigFile(cfg.ConfigParserHandler, config_file_location), \
        os.path.join(os.getenv('HOME', dir_config))


def _error_exit():
    print()


def _init(name, scheme, on_dir=None, vcs=None, venv=None, **kwargs):
    cfg, dir_cfg = _get_config_file(scheme)
    structure = cfg.read_config_item('General', 'project_structure')
    if on_dir and os.path.isdir(on_dir):
        location = on_dir
    else:
        location = cfg.read_config_item('General', 'root_projects_dir')
    try:
        create_structure(name, structure, location)
    except PathNotExists:
        # How to define the _error_exit function here
        print("algo con respecto a que la ruta no existe")
        sys.exit()
    if vcs is not None:
        from pypro.initializers import init_vcs
        try:
            vcs_name = vcs[0]
            vcs_founded = True
        except TypeError:
            try:
                vcs_name = cfg.read_config_item('VCS', 'vcs')
                vcs_founded = True
            except KeyError:
                vcs_founded = False
        if vcs_founded:
            ignore_file_name = '.' + vcs_name + 'ignore'
            try:
                ignore_file_path = os.path.join(vcs[1], ignore_file_name)
            except IndexError:
                if os.path.isfile(os.path.join(dir_cfg, ignore_file_name)):
                    ignore_file_path = os.path.join(dir_cfg, ignore_file_name)
                else:
                    ignore_file_path = ""
            init_vcs(vcs_name, location,
                     ignore_file_path=ignore_file_path)
        else:
            print("You must define your vcs")
    # Falta mejorar venv
    if venv is not None:
        from pypro.initializers import init_venv
        if venv:
            # For the moment
            a = ('py_3', 'path_to_rqes', 'location', 'options')
            venv_args = dict()
            for i in range(0, len(venv)):
                venv_args[a[i]] = venv[i]
            init_venv(name, **venv_args)
        else:
            # Python 3 default, location from config file o WORKON_HOME
            # options from config file, requirements.txt from config dir
            venv_args = dict()
            venv_args['location'] = cfg.read_config_item(
                'Virtualenv', 'location')
            possible_rqes = os.path.join(dir_cfg, 'requirements.txt')
            if os.path.isfile(possible_rqes):
                venv_args['path_to_rqes'] = possible_rqes
            try:
                venv_args['options'] = cfg.read_config_item(
                    'Virtualenv', 'options')
            except KeyError:
                pass
            init_venv(name, **venv_args)


def _analize(path, scheme, analize_vcs=True, **kwargs):
    def _save_analysis():
        pass

    cfg, dir_cfg = _get_config_file(scheme)
    custom_prefixes = cfg.read_config_item('Analize', 'custom_prefixes')
    if custom_prefixes or not custom_prefixes.isspace():
        structure_analizer = StructureAnalizer(custom_prefixes=custom_prefixes)
    else:
        structure_analizer = StructureAnalizer()
    if path is None:
        path = os.getcwd()
    structure_analizer.analize_dir_structure(path)

    # Save in given scheme here with restructure() function


def main():
    args = get_args()
    if args.subparser == 'init':
        _init(args.name, args.scheme, args.directory, args.venv, args.vcs)
    else:
        _analize(args.path, args.save, args.novcs)
