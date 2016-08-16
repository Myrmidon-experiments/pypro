import argparse
import os


usage = "%(prog)s [-h] [-v] <command> [<args>]"
version = "0.0.1"


def init(args):
    print("First \n%s" % args.name)
    print("scheme %d" % args.scheme)
    print("vcs %s" % args.vcs)
    print("venv %s" % args.venv)


def analize(args):
    print("Second")
    print("save %d" % args.save)
    print("path %s" % args.path)
    print("novcs", args.novcs)


def get_args():
    parser = argparse.ArgumentParser(prog='pypro',
                                     add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        help="show this help message and exit")
    parser.add_argument('-v', '--version', action="version",
                        version="%(prog)s " + version,
                        help="show the current version")
    subparsers = parser.add_subparsers()

    sp_analize = subparsers.add_parser('analize',
                                       help="%(prog)s analize --help")
    sp_analize.add_argument('path', nargs='?', default=os.getcwd(),
                            help="full or relative path. \
                            If not given cwd is default")
    sp_analize.add_argument('--save', nargs='?', const=1, type=int,
                            metavar="SCHEME", help="save on scheme file")
    sp_analize.add_argument('--no-vcs', action="store_true", dest="novcs",
                            help="analize ignoring the version control system")
    sp_analize.set_defaults(func=analize)

    sp_init = subparsers.add_parser('init', help="pypro init --help")
    sp_init.add_argument('name',
                         help="initialize a new project with a given name")
    sp_init.add_argument('--venv', nargs='*', metavar='venv_args',
                         help="create a virtualenv with the same project name")
    sp_init.add_argument('--vcs', nargs='*', metavar="vcs_args",
                         help="choose a vcs and give a path for ignorefile")
    sp_init.add_argument('-s', '--scheme', nargs='?', const=1, type=int,
                         help="select scheme number. Default 1")
    sp_init.set_defaults(func=init)

    return parser.parse_args()


def main(args=get_args()):
    args.func(args)

main()
