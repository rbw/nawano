# -*- coding: utf-8 -*-

import io
import ast

from setuptools import setup, find_packages


def get_version():
    with io.open('nawano/__init__.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with io.open('README.rst') as readme:
    setup(
        name='nawano',
        packages=find_packages(),
        version=get_version(),
        description='Nano REPL CLI',
        entry_points={
            'console_scripts': [
                'nawano=nawano.cli:run',
            ]
        },
        long_description=readme.read(),
        install_requires=requirements,
        author='Robert Wikman',
        author_email='rbw@vault13.org',
        maintainer='Robert Wikman',
        maintainer_email='rbw@vault13.org',
        url='https://github.com/rbw/nawano',
        download_url='https://github.com/rbw/nawano/tarball/%s' % get_version(),
        keywords=['nano', 'cryptocurrency', 'cli', 'wallet'],
        platforms='any',
        classifiers=[
            'Topic :: Utilities',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
        license='BSD-2-Clause',
    )
