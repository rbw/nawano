# -*- coding: utf-8 -*-

import io
import ast

from setuptools import setup, find_packages


def get_version():
    with io.open('nawano/__init__.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with io.open('README.md') as readme:
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
        install_requires=[
            'privy==6.0.0',
            'pyblake2==1.1.2',
            'passwordmeter==0.1.8',
            'marshmallow>=2.15.1',
            'simplejson>=3.11.1',
            'click>=6.7',
            'prompt-toolkit>=2.0.4',
            'sqlalchemy>=1.2.7',
            'sqlalchemy-utils>=0.33.3',
            'requests>=2.18.4',
            'texttable>=1.4.0',
            'libn>=0.1.1',
            'crayons>=0.1.2'  # @TODO - remove
        ],
        author='Robert Wikman',
        author_email='rbw@vault13.org',
        maintainer='Robert Wikman',
        maintainer_email='rbw@vault13.org',
        python_requires='>=3.6',
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
