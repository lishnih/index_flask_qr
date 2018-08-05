#!/usr/bin/env python
# coding=utf-8
# Stan 2016-04-24

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os

from flask import render_template, send_from_directory, url_for, abort
from flask_principal import Permission, RoleNeed

from ..core.fileman import list_files
from ..app import app


# ===== Options =====

dir_name = 'test'
url = '/{0}/'.format(dir_name)


# ===== Roles =====

# debug_permission = Permission(RoleNeed('debug'))
debug_permission = Permission()


# ===== Routes =====

@app.route(url)
@app.route('{0}<path:path>'.format(url))
def debug_test(path=''):
    if not debug_permission.can():
        abort(404)

    abspath = os.path.join(app.root_path, dir_name)

    if not os.path.isdir(abspath):
        return render_template('empty.html',
                 head = 'Test dir not found!',
                 text = 'Test dir not found!',
               )

    if not path or path[-1] == '/':
        test_url = '/{0}/{1}'.format(dir_name, path)
        dirlist, filelist = list_files(test_url, app.root_path, url_for('debug_test'))

        return render_template('views/views_debug/test.html',
                 title = 'Testing directory',
                 path = test_url,
                 dirlist = dirlist,
                 filelist = filelist,
               )

    else:
        return send_from_directory(abspath, path)
