#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
setup script for ebttools
"""
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ebttools',
    version='1.0.0',
    
    packages=find_packages(), #automagically include all subfolders as packages
    package_data = {"":["*.png"],
					"ebttools":["calibrations/*"]},
	
    license='MIT',
    long_description=read('README.md'),
    
    author='Malte Gotz',
    author_email='malte.gotz@oncoray.de',
    url='https://github.com/mgotz/EBT_evalution',
	
    install_requires=['matplotlib',
                      'scipy',
                      'numpy',
                      'pillow',
                      'mg_dataprocessing>=1.0.0',
                      'mg_pyguitools>=1.0.0'],
                      
    dependency_links=["https://github.com/mgotz/PyGUITools/tarball/master#egg=mg_pyguitools-1.0.0",
                      "https://github.com/mgotz/PyDataProcessing/tarball/master#egg=mg_dataprocessing-1.0.0"],
                      
    entry_points = {"gui_scripts":["EBT-evaluation = ebttools.gui.main:run"]}


)