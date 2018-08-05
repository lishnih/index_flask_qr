#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask import render_template

from flask_login import current_user

from ..app import app


@app.route("/")
def index():
#   return app.send_static_file('index.html')
    return render_template('empty.html',
             title = 'Index',
             head = 'Welcome!' if current_user.is_anonymous else \
                    'Welcome, {0}!'.format(current_user.name),
             html = 'Welcome to the QR Index system!',
           )


@app.route('/json', methods=['GET', 'POST'])
def json():
    return 'Response'


@app.route("/form")
def form():
    return app.send_static_file('index.html')
