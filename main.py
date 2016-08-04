import argparse
import os
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


def project_init(name, vcs=None, ve=False):
    pass


def create_structure(structure):
    test_location = '/home/cactus/Escritorio/test_pypro'
    for dirname in (dirname for dirname in structure if dirname.endswith('/')):
        os.makedirs(os.path.join(test_location, dirname))

a = StructureAnalizer()
a.analize_dir_structure()
print(a.restructure())
# for dirn in (dirname for dirname in a.restructure() if dirname.endswith('/')):
#   print(dirn)
# create_dir_structure(a.restructure())


files_ = (i for i in a.restructure().split('n') if i.endswith('/'))
for i in files_:
    print(i)
