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
EXCLUDE_FROM_PACKAGES = ('tests', 'todo.org')


setup(
    name="pypro",
    version="0.0.1",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    description=description,
    license='GPLv3',
    include_package_data=True,
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
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ]
)
