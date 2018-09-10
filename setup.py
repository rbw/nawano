# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='nawano',
    packages=find_packages(),
    version='0.1',
    description='Nano REPL CLI',
    entry_points={
        'console_scripts': [
            'nawano=nawano.cli:run',
        ]
    },
)
