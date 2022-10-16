#!/usr/bin/env python

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='mercado',
      version='0.1',
      description='Open Source market for utilities',
      author='YuviGold',
      packages=find_packages(),
      install_requires=requirements,
      entry_points={
          'console_scripts': ['mercado=mercado.cli:main']
      }
      )
