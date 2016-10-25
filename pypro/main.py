import os
import sys
import pypro.config as cfg
from pypro.cli import get_args
from pypro.analizers import StructureAnalizer
from pypro.initializers import create_structure
from pypro.exceptions import PathNotExists


def _get_scheme_config(scheme):
    # Because argparse return None if the optional argument it's not used
    home_path = os.getenv('HOME')
    if scheme is None:
        scheme = 0
    config_file_name = '.pypro/scheme' + str(scheme)
    dir_config = '.pypro/dir_scheme' + str(scheme)
    config_file_path = os.path.join(home_path, config_file_name)
    dir_config_path = os.path.join(home_path, dir_config)
    if not os.path.isfile(config_file_path):
        os.makedirs(dir_config_path)
        with open(config_file_path, 'w+') as f:
            # This is for the moment. It change in first release, because
            # the file path that contains the config will be different.
            path = '/home/cactus/Devel/pypro/resources/scheme_example'
            with open(path) as ff:
                f.write(ff.read())
    return cfg.ConfigFile(cfg.ConfigParserHandler, config_file_path), \
        dir_config_path


def _init(name, scheme, on_dir=None, vcs=None, venv=None, **kwargs):
    cfg, dir_cfg = _get_scheme_config(scheme)
    structure = cfg.read_config_item('General', 'project_structure')
    if on_dir and os.path.isdir(on_dir):
        location = on_dir
    else:
        location = cfg.read_config_item('General', 'root_projects_dir')
    try:
        create_structure(name, structure, location)
    except PathNotExists:
        # How to define the _error_exit function here
        print("the given path didn't exists.")
        sys.exit()
    if vcs is not None:
        from pypro.initializers import init_vcs
        if vcs:
            if len(vcs) != 2:
                print("You must pass 2 arguments to --vcs")
            else:
                vcs_name = vcs[0]
                ignore_file_name = '.' + vcs_name + 'ignore'
                ignore_file_path = os.path.join(vcs[1], ignore_file_name)
                init_vcs(vcs_name, location,
                         ignore_file_path=ignore_file_name)
        else:
            try:
                vcs_name = cfg.read_config_item('VCS', 'vcs')
                vcs_founded = True if vcs_name else False
            except KeyError:
                print("You must define the vcs in the scheme file")
                vcs_founded = False
            if vcs_founded:
                ignore_file_name = '.' + vcs_name + 'ignore'
                if os.path.isfile(os.path.join(dir_cfg, ignore_file_name)):
                    ignore_file_path = os.path.join(
                        dir_cfg, ignore_file_name)
                else:
                    ignore_file_path = ""
                init_vcs(vcs_name, location,
                         ignore_file_path=ignore_file_path)

    if venv is not None:
        from pypro.initializers import init_venv
        if venv:
            if len(venv) != 4:
                print("You must pass 4 arguments to --venv")
            else:
                # For the moment.
                a = ('py_3', 'path_to_rqes', 'location', 'options')
                venv_args = dict()
                for i in range(0, len(venv)):
                    venv_args[a[i]] = venv[i]
                init_venv(name, **venv_args)
        else:
            venv_args = dict()
            venv_args['location'] = cfg.read_config_item(
                'Virtualenv', 'location')
            if cfg.read_config_item('Virtualenv', 'python_version') == '2':
                venv_args['py_3'] = False
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
        save_on_default = False
        if scheme is None:
            save_flag = input(':: Do you want to save this' +
                              ' analysis in scheme 0? [Y/n] ')
            if save_flag in ('Y', 'y', 'YES', 'yes'):
                save_on_default = True

        if scheme is not None or save_on_default:
            scheme_number = scheme if scheme else 0
            cfg.write_config_item('General', 'project_structure',
                                  structure_analizer.restructure())
            if vcs:
                cfg.write_config_item('VCS', 'vcs', vcs)
            cfg.save_changes()
            print("\x1b[1m:: Analysis saved in scheme {}\x1b[0m".format(
                scheme_number))

    def _print_analysis():
        header = ' Analysis on {} '.format(
            os.path.abspath(path)).center(50, '#')
        border = '-' * len(header)
        template = '{}\n{}\n{}\n\n'.format(border, header, border) + \
            '\x1b[1mStructure\x1b[0m\n---------\n\n' + \
            '{tree}\n\n' + \
            ':: prefixes exclude on analysis -> {prefixes}\n\n'
        template_vcs = '\x1b[1mVersion Control System\x1b[0m\n---------\n' + \
            ':: {vcs_name}\n:: {ignore_file}\n'
        format_args = dict()
        format_args['prefixes'] = structure_analizer.exclude_prefixes
        format_args['tree'] = structure_analizer.restructure_as_tree()
        format_args['vcs_name'] = vcs.upper() if vcs else "Not Found"
        if path_to_ignore_file:
            format_args['ignore_file'] = '{} saved in {}'.format(
                ignore_file_name, path_to_ignore_file)
        else:
            format_args['ignore_file'] = 'ignore file not founded'
        template += template_vcs if analize_vcs else ''
        template += border + '\n'
        print(template.format(**format_args))

    # Starts here
    cfg, dir_cfg = _get_scheme_config(scheme)
    custom_prefixes = cfg.read_config_item('Analize', 'custom_prefixes')
    if custom_prefixes or not custom_prefixes.isspace():
        structure_analizer = StructureAnalizer(custom_prefixes=custom_prefixes)
    else:
        structure_analizer = StructureAnalizer()
    if path is None:
        path = os.getcwd()
    structure_analizer.analize_dir_structure(path)
    if analize_vcs:
        from pypro.analizers import analize_vcs
        vcs, path_to_ignore_file, ignore_file_name = analize_vcs(path, dir_cfg)
    else:
        vcs, path_to_ignore_file, ignore_file_name = None, None, None
    _print_analysis()
    _save_analysis()


def main():
    args = get_args()
    if args.subparser == 'init':
        _init(args.name, args.scheme, args.directory, args.venv, args.vcs)
    else:
        _analize(args.path, args.save, args.novcs)
