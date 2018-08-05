#!/usr/bin/env python
# coding=utf-8
# Stan 2016-04-24

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os

from flask import (g, request, render_template, url_for, session,
                   abort, __version__)

from flask_login import current_user
from flask_principal import Permission, RoleNeed

from ..core.dump_html import html

from ..app import app


# ===== Roles =====

# debug_permission = Permission(RoleNeed('debug'))
debug_permission = Permission()


# ===== Routes =====

@app.route('/debug/')
def debug():
    if not debug_permission.can():
        abort(404)

    output = []
    for rule in app.url_map.iter_rules():
        options, options_str = {}, {}
        for seq, arg in enumerate(rule.arguments, 1):
            options[arg] = seq
            options_str[arg] = "<{0}>".format(arg)

        url = url_for(rule.endpoint, **options)
        args = rule.arguments if rule.arguments else ''
        methods = ','.join(rule.methods)
        f = app.view_functions.get(rule.endpoint)
#       loc = f.__code__.co_filename if f else ''   # f.func_code.co_filename
        m = sys.modules.get(f.__module__)
        loc = m.__file__ if m else ''
        output.append([url, args, methods, rule.endpoint, loc])

    return render_template('views/views_debug/index.html',
             title = 'Url mapping',
#            urls = sorted(output),
             urls = sorted(output, key=lambda url: url[0])
           )


@app.route('/debug/app')
def debug_app():
    if not debug_permission.can():
        abort(404)

    return html(app)


@app.route('/debug/current_user')
def debug_current_user():
    if not debug_permission.can():
        abort(404)

    return html(current_user)


@app.route('/debug/g')
def debug_g():
    if not debug_permission.can():
        abort(404)

    return html(g)


@app.route('/debug/request')
def debug_request():
    if not debug_permission.can():
        abort(404)

    return html(request)


@app.route('/debug/session')
def debug_session():
    if not debug_permission.can():
        abort(404)

    d = {key: val for key, val in session.items()} if session else '<empty>'
    return html((session, d))


@app.route('/debug/ver')
def debug_ver():
    if not debug_permission.can():
        abort(404)

    return __version__
