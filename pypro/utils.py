import os
from contextlib import contextmanager


@contextmanager
def my_chdir(path):
    prev_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_dir)
