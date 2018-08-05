#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

import logging

from index_flask_qr.main import app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app.run(host='0.0.0.0')
