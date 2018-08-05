#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask import render_template

from ..app import app


@app.route("/")
def index():
#   return app.send_static_file('index.html')
    return render_template('empty.html',
             title = 'Index',
             head = 'Welcome',
             html = 'Welcome to the index system!',
           )


@app.route('/json', methods=['GET', 'POST'])
def json():
    return 'Response'


@app.route("/form")
def form():
    return app.send_static_file('index.html')
