import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop


class CustomDevelop(develop):

    def run(self):
        location = os.path.join(os.getenv("HOME"), '.pypro')
        if not (os.path.isdir(location)):
            os.makedirs(location)
        develop.run(self)

description = "Description here... "


setup(
    name="pypro",
    version="0.0.1",
    packages=find_packages(),
    description=description,
    license='GPLv3',
    cmdclass={
        'develop': CustomDevelop,
    },

    entry_points={
        'console_scripts': [
            'pypro=pypro.main:main',
        ],
    },

    # Author info
    author='cactus',
    author_email='correa.francisco.21@gmail.com',
)
