import os
from mimetypes import guess_type
from contextlib import contextmanager


@contextmanager
def my_chdir(path):
    prev_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def get_mimetype(file_):
    return guess_type(file_)[0]
