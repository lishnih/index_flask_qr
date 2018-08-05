#!/usr/bin/env python
# coding=utf-8
# Stan 2018-08-02

from flask_login import LoginManager, current_user
from flask_principal import (Principal, RoleNeed, UserNeed,
                             Identity, identity_loaded)

from ..app import app


# ===== login_manager =====

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()


# ===== principal =====

principal = Principal(app)


@principal.identity_loader
def load_identity_when_session_expires():
    if hasattr(current_user, 'id'):
        return Identity(current_user.id)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if identity.id:
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        user = User.query.filter_by(id=identity.id).first()
        if user:
            for i in user.groups:
                identity.provides.add(RoleNeed(i.name))
