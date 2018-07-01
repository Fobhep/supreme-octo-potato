#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='sop',
      version='0.1',
      description='Supreme Octo Potato',
      author='B. Hopfenmüller & M. Dellweg',
      url='https://github.com/Fobhep/supreme-octo-potato',
      licence='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['click', 'pyperclip'],
      entry_points='''
          [console_scripts]
          sop=sop:main
      '''
      )
