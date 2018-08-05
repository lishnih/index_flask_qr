#!/usr/bin/env python
# coding=utf-8
# Stan 2016-06-07

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os

from flask import session, request, render_template, redirect, flash

from flask_login import login_required, login_user, logout_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from .user_forms import RegistrationForm, LoginForm, ChangePasswordForm

from ..app import app
from .functions import get_next
from .user_models import db, User


# ===== Routes =====

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if not current_user.is_anonymous:
        return render_template('user/logout.html',
                 title = 'Logout',
                 name = current_user.name,
                 next = "/signup",
               )

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            email = form.email.data,
            name = form.name.data,
            password = form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        flash('Thank you for registering!')
        return redirect(get_next('/signin'))

    return render_template('user/signup.html',
             title = 'Registering new user',
             form = form,
             next = request.args.get('next', '/signin'),
           )


@app.route('/signin', methods=['GET', 'POST'])
def user_signin(user=None):
    if not current_user.is_anonymous:
        return render_template('user/logout.html',
                 title = 'Logout',
                 name = current_user.name,
                 next = "/signin",
               )

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_user(form.user, remember=form.remember.data)

        identity_changed.send(app, identity=Identity(form.user.id))

        flash('Successfully logged in as {0}'.format(form.user.name))
        return redirect(get_next())

    return render_template('user/signin.html',
             title = 'Sign in',
             form = form,
             next = request.args.get('next', '/'),
           )


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def user_change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        form.user.change_password(form.password.data)
        db.session.commit()

        flash('Successfully changed password')
        return redirect(get_next())

    return render_template('user/change_password.html',
             title = 'Change Password',
             form = form,
             next = request.args.get('next', '/profile'),
           )


@app.route("/confirm/<code>")
def user_confirm(code=None):
    user = User.query.filter_by(verified=code).first()
    if user:
        status = 'verified'
        user.verified = ''
        db.session.commit()
    else:
        status = 'not verified'

    return render_template('user/confirm.html',
             title = 'Confirm email',
             status = status,
           )


@app.route("/logout")
@login_required
def user_logout():
    logout_user()

    for key in ('identity.id', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(app, identity=AnonymousIdentity())

    return redirect(get_next())


@app.route("/profile")
@login_required
def user_profile():
#   return html(current_user)

    return render_template('user/profile.html',
             title = 'Profile',
             cu = current_user,
             groups = current_user.groups,
             databases = current_user.databases,
             verified = 'not verified' if current_user.verified else 'verified'
           )


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def user_edit():
    return render_template('user/edit.html',
             title = 'Edit profile',
             cu = current_user,
           )
