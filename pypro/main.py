import os
from pypro.cli import get_args
from pypro.analizers import StructureAnalizer
from pypro.initializers import init_structure
# from config import ConfigFile, ConfigParserHandler


def init(name, scheme, vcs=None, venv=None, **kwargs):
    init_structure(name,)


def analize(path, save_in, novcs=None, **kwargs):
    structure_analizer = StructureAnalizer()
    if path is None:
        path = os.getcwd()
    structure_analizer.analize_dir_structure(path)
    print(structure_analizer.restructure())
    # Save in given scheme here with restructure() function


# With argparse
def main():
    args = get_args()
    if args.subparser == 'init':
        init(args.name, args.scheme, args.venv, args.vcs)
    else:
        analize(args.path, args.save, args.novcs)
