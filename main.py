import argparse
import os


usage = "%(prog)s [-h] [-v] <command> [<args>]"
save_help = ""
new_help = ""


def get_args():
    parser = argparse.ArgumentParser(prog='pypro',
                                     usage=usage,
                                     add_help=False)
    parser.add_argument('-h', '--help', action='help',
                        help="Show this message and exit")
    parser.add_argument('-v', '--version', action="version",
                        version="%(prog)s 0.0.1",
                        help="Show the current version")
    subparsers = parser.add_subparsers()

    sp_analize = subparsers.add_parser('analize', help="Analize help")
    sp_analize.add_argument('-a', '--analize', nargs='?',
                            const=os.getcwd(), metavar="PATH",
                            help="Some help here...")

    sp_init = subparsers.add_parser('init', help="Init help")
    sp_init.add_argument('-n', '--new', metavar="NAME",
                         help="New project")
    return parser.parse_args()


"""
def get_args():
    parser = argparse.ArgumentParser(prog='pypro',
                                     usage=usage,
                                     add_help=False)

    miscellaneous = parser.add_argument_group("Miscellaneous")
    miscellaneous.add_argument('-h', '--help', action='help',
                               help="Show this message and exit")
    miscellaneous.add_argument('-v', '--version', action="store_true",
                               help="Show the current version")
    analize_group = parser.add_argument_group("Analizer Options")
    analize_group.add_argument('-a', '--analize', nargs='?', required=True,
                               const=os.getcwd(), metavar="PATH",
                               help="Some help here...")
    analize_group.add_argument('--save', nargs='?', const=1, type=int,
                               metavar="SCHEME", help=save_help)
    analize_group.add_argument('--no-vcs', action="store_true",
                               help="Analize ignoring the version \
                               control system")
    init_group = parser.add_argument_group("Initializer Options")
    init_group.add_argument('-n', '--new', metavar="NAME", required=True,
                            help="New project")

    return parser.parse_args()
"""


def main():
    args = get_args()
    if args.analize:
        print("Analize", args.analize)
    if args.save:
        print(args.save)


main()
