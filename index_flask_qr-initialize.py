#!/usr/bin/env python
# coding=utf-8
# Stan 2016-06-20

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from index_flask_qr.main import app_db, user_models


def init_admin():
    user_id = 1

    user = user_models.User.query.filter_by(id=user_id).first()
    if not user:
        user = user_models.User(
            email = 'root@localhost',
            name = 'root',
            password = '1234',
        )
        user.set_verified()
        app_db.db.session.add(user)

    app_db.db.session.commit()


if __name__ == '__main__':
    init_admin()
