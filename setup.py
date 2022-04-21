from setuptools import setup, find_packages
import os
import pathlib
import sys
from dataplotter.__version__ import __version__

setup(
    name='dataplotter',
    version=__version__,
    packages=find_packages(),
)

# use this block to create icon on desktop
with open(pathlib.Path('c:/Users',os.environ['USERNAME'],'Desktop','dataplotter.bat'),'w') as f:

    f.write('@echo off\n')
    f.write('"{}" -m dataplotter'.format(sys.executable))
