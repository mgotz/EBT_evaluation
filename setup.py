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
    version='0.2.0',
    
    packages=find_packages(), #automagically include all subfolders as packages
    
    license='MIT',
    long_description=read('README.txt'),
    
    author='Malte Gotz',
    author_email='malte.gotz@oncoray.de',
    url='https://github.com/mgotz/EBT_evalution',
    
    install_requires=['matplotlib',
                      'scipy',
                      'numpy',
                      'mg.dataprocessing',
                      'mg.guitools'],
                      
    dependency_links=["https://github.com/mgotz/PyGUITools.git",
                      "https://github.com/mgotz/PyDataProcessing.git"]
)