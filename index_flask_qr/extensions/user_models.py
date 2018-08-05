#!/usr/bin/env python
# coding=utf-8
# Stan 2016-06-07

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

from datetime import datetime

from .app_db import db
from .app_bcrypt import bcrypt


class User(db.Model):         # Rev. 2018-08-03
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    verified = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = self.get_password(password)

        self.init_verification()

    def __repr__(self):
        return '<User {0!r}>'.format(self.name)

    def get_id(self):
        return self.email

    def get_password(self, password):
        pw_hash = bcrypt.generate_password_hash(password)
        return pw_hash

    def change_password(self, password):
        self.password = self.get_password(password)

    def init_verification(self):
        self.verified = self.suit_code(self.email)
        self.send_verification()

    def send_verification(self):
        # send verified code
        pass

    def suit_code(self, email):
        double = True
        while double:
            verified = self.get_verification(email)
            double = User.query.filter_by(verified=verified).first()

        return verified

    def get_verification(self, email):
        return bcrypt.generate_password_hash(email)


db.create_all()
