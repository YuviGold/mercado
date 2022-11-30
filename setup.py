#!/usr/bin/env python

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='mercado',
      version='0.1.3',
      description='Open Source market for utilities',
      author='YuviGold',
      url='https://github.com/YuviGold/mercado/',
      packages=find_packages(),
      install_requires=requirements,
      setup_requires=['wheel'],
      entry_points={
          'console_scripts': ['mercado=mercado.cli:main']
      }
      )
