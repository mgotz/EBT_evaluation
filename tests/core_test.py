#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:18:22 2018

@author: gotzm

an incomplete suite of unit tests, still under developement
DON'T RELY ON THIS IN ANY WAY
"""

#get ready for python 3
from __future__ import (print_function, division, absolute_import,
                        unicode_literals)

import numpy as np
import os
import sys

#add base to path and load
sys.path.insert(0,os.path.join(sys.path[0],".."))
from ebttools.core import DoseArray

import unittest

class TestUniformDose(unittest.TestCase):

    def setUp(self):
        self.dose = np.ones((470,470)).view(DoseArray)
    
    def test_centered(self):
        self.assertEqual(self.dose.rectangle_stats(1.0,1.0,0.5,0.5,0,False),
                         (13924.0,1.0,0.0,1.0,1.0))

    def test_edge(self):
        self.assertEqual(self.dose.rectangle_stats(0.0,1.0,0.5,0.5,0,False),
                         (6962.0,1.0,0.0,1.0,1.0))

if __name__ == '__main__':
    unittest.main()

