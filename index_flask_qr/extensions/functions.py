#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from flask import request, url_for

from ..app import app


def get_next(url=None):
    base = url_for('index')
    next = request.args.get('next', '')

    return next if next.startswith(base) else \
           url if url else url_for('index')

#   return next if next in [i.rule for i in app.url_map.iter_rules()] else \
#          url if url else url_for('index')


def debug_query(query):
    try:
        return str(query)
    except Exception as e:
        return repr(query)
