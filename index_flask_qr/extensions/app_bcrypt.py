#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-03

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask_bcrypt import Bcrypt

from ..app import app


bcrypt = Bcrypt(app)
