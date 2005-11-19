#!/usr/bin/env python

"""
Standard setup.py file using Python's native distutils module for installation.

To build and install Famms and SystemFamms, type:
python setup.py install

To check your installation, change directory to ./tests/Famms, and run 
python checkPythonCB.py

Ola Skavhaug
"""

from distutils.core import setup
import distutils
from  sys import argv
import os
from os.path import join as pjoin, sep as psep

os.chdir("src")


setup(name='Famms',
    version='0.1',
    description='Fully Automatic Method of Manufactured Solutions',
    author='Ola Skavhaug',
    author_email='skavhaug@simula.no',
    packages=["Famms", "SystemFamms"]
    )
