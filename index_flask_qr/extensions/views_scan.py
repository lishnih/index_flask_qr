#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import time
import base64

from flask import request

from flask_login import current_user

import boto3

from ..app import app


base = "snapshots"
os.makedirs(base, exist_ok=True)


def detect_texts(raw, region="us-east-2"):
    rekognition = boto3.client('rekognition', region)
    response = rekognition.detect_text(
        Image = {
            'Bytes': raw,
        }
    )

    for i in response['TextDetections']:
        yield i


def get_unique(filename, id=0):
    root, ext = os.path.splitext(filename)

    filename_id = "{0}_{1}{2}".format(root, id, ext) if id else filename
    if os.path.exists(filename_id):
        filename_id = get_unique(filename, id+1)

    return filename_id


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if current_user.is_anonymous:
        return render_template('empty.html',
                 title = 'Index',
                 html = 'Authorization required!',
               )

    else:
        if request.method == 'POST':
#             head, raw = request.data.split(b',', 1)
#             data = base64.b64decode(raw)

            user_snapshots = "{0}/id_{1}".format(base, current_user.id)
            os.makedirs(user_snapshots, exist_ok=True)

#             tstamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
#             filename = "{0}/scan_{1}.png".format(user_snapshots, tstamp)
#             with open(get_unique(filename), 'wb') as snapshot:
#                 snapshot.write(data)

            filename = "{0}/scan_20180809_154443.png".format(user_snapshots)
            with open(filename, 'rb') as snapshot:
                data = snapshot.read()

            for text in detect_texts(data):
            	   print(text['DetectedText'])

            return ""

        return app.send_static_file('scan.html')
