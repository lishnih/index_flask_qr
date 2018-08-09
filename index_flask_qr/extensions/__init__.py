#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os
import glob


py_version = sys.version_info[:2]
PY2 = py_version[0] == 2


files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "*.py")))
modules = [os.path.basename(f)[:-3] for f in files if not f.endswith("__init__.py")]

if PY2:
    modules = [i.encode('utf-8') for i in modules]

__all__ = modules
