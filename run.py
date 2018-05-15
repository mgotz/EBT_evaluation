#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Use this script to execute the EBT evaluation GUI
"""

import os
import sys

sys.path.insert(0,(os.path.dirname(__file__)))

from ebttools.gui.main import run

run()
