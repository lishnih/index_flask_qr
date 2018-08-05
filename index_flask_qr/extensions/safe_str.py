#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-03

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from jinja2 import evalcontextfilter

from ..core.types23 import *
from ..app import app


@app.template_filter()
@evalcontextfilter
def safe_str(eval_ctx, value):
    if isinstance(value, string_types):
        if not isinstance(value, unicode):
            value = value.decode('utf8', 'ignore')

    elif not isinstance(value, all_types) and value is not None:
        try:
            value = str(value).decode('utf8', 'ignore')
        except:
            value = "[ {0} ]".format(type(value))

    return value
