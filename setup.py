#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
setup script for ebttools
"""
import os
from setuptools import setup, find_packages, __version__

#check to have setuptools > v36.2
version = __version__.split(".")
if len(version) < 2:
    raise ImportError("unkown version of setuptools, please update")
if int(version[0]) < 36 or (int(version[0]) == 36 and int(version[1]) < 2):
    raise ImportError("setuptools version "+ __version__ +" too low, needs at least 36.2")


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ebttools',
    version='2.0.1a',
    
    packages=find_packages(exclude=("tests")), #automagically include all subfolders as packages, but don't install the tests
    package_data = {"":["*.png"],
					"ebttools":["calibrations/*"]},
	
    license='MIT',
    long_description=read('README.md'),
    
    author='Malte Gotz',
    author_email='malte.gotz@oncoray.de',
    url='https://github.com/mgotz/EBT_evalution',
	
    install_requires=['matplotlib>=1.4.3',
                      'scipy>=0.15.1',
                      'numpy>=1.9.2',
                      'pillow>=2.8.2',
                      'configparser;python_version<"3.2"',
                      'mg_dataprocessing>=1.0.0',
                      'mg_pyguitools>=1.1.1'],
                      
    dependency_links=["https://github.com/mgotz/PyGUITools/tarball/master#egg=mg_pyguitools-1.1.1",
                      "https://github.com/mgotz/PyDataProcessing/tarball/master#egg=mg_dataprocessing-1.0.0"],
                      
    entry_points = {"gui_scripts":["EBT-evaluation = ebttools.gui.main:run"]}


)