"""This module is used to put general utilities for the development."""

import os
from contextlib import contextmanager


@contextmanager
def my_chdir(path):
    """Function to use chdir in a with statement."""
    prev_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_dir)
