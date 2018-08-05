#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask import Flask

from werkzeug.wsgi import DispatcherMiddleware

from . import config


app = Flask(__name__, static_url_path='')

app.config.from_object(config)
# app.config.from_pyfile('app.cfg')


if app.config["APPLICATION_ROOT"] != '/':
    def simple(env, resp):
        resp(b'200 OK', [(b'Content-Type', b'text/plain')])

        if app.debug:
#           r = env['werkzeug.request']
#           return [bytes("{0}: {1}\n".format(i, getattr(r, i)), 'ascii') for i in r.__dir__()]
            return [bytes("{0}: {1}\n".format(k, v), 'ascii') for k, v in env.items()]
        else:
            return [b'Hello WSGI World\n']

    app.wsgi_app = DispatcherMiddleware(simple, {
        app.config["APPLICATION_ROOT"]: app.wsgi_app,
    })
