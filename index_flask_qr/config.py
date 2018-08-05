#!/usr/bin/env python
# coding=utf-8

import os

here = os.path.abspath(os.path.dirname(__file__))
home = os.path.expanduser("~")

APPLICATION_ROOT = '/qr'

CSRF_ENABLED = True
SECRET_KEY = 'secret_\xfb_\x14_\xdf_\x1b'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(here, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(here, 'db_repository')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
