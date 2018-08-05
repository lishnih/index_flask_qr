#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-03

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask_sqlalchemy import SQLAlchemy

from ..app import app


db = SQLAlchemy(app)
