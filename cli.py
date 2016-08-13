import argparse
import os


usage = "%(prog)s [-h] [-v] <command> [<args>]"
version = "0.0.1"


def get_args():
    parser = argparse.ArgumentParser(prog='pypro',
                                     add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        help="show this help message and exit")
    parser.add_argument('-v', '--version', action="version",
                        version="%(prog)s " + version,
                        help="show the current version")
    subparsers = parser.add_subparsers()

    sp_analize = subparsers.add_parser('analize', help="Analize help")
    sp_analize.add_argument('path', nargs='?', default=os.getcwd(),
                            help="Full or relative path. \
                            If not given cwd is default")
    sp_analize.add_argument('--save', nargs='?', const=1, type=int,
                            metavar="SCHEME", help="Save on scheme file")
    sp_analize.add_argument('--no-vcs', action="store_true",
                            help="Analize ignoring the version control system")

    sp_init = subparsers.add_parser('init', help="Init help")
    sp_init.add_argument('name', help="Create a new project with a given name")
    sp_init.add_argument('--venv', nargs='*', metavar='venv_args',
                         help="New project", required=False)
    sp_init.add_argument('--vcs', nargs='*', metavar="vcs_args",
                         help="Choose a vcs and give a path for ignorefile")
    sp_init.add_argument('-s', '--scheme', nargs='?', const=1, type=int,
                         help="Select scheme number. Default 1")

    return parser.parse_args()
    """parser.print_help()
    print('\n###\n')
    sp_init.print_help()
    print('\n###\n')
    sp_analize.print_help()
    """

get_args()
