import argparse
from analizers import StructureAnalizer


def get_args():
    parser = argparse.ArgumentParser(prog='pypro')
    parser.add_argument(
        '-n', '--new', help="Initialize a directory for a new project")
    parser.add_argument(
        '-a', '--analize', metavar="PATH",
        help="Analize a dir structure and save it as your default dir \
        structure for future projects")
    return parser.parse_args()


def main():
    args = get_args()
    if args.new:
        print("New", args.new)
    if args.analize:
        sa = StructureAnalizer()
        sa.analize(args.analize)
        print("Analize", args.analize)
