#!/usr/bin/env python
# coding=utf-8
# Stan 2016-06-07

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os

from flask import session, request, render_template, redirect, url_for, jsonify, flash

from flask_login import login_required, login_user, logout_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed

from .user_forms import RegistrationForm, LoginForm, ChangePasswordForm

from ..app import app
from .functions import get_next
from .user_models import db, User


# ===== Routes =====

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    form = RegistrationForm(request.form)

    if not current_user.is_anonymous:
        if form.type.data == 'json':
            return jsonify({'result': 'error', 'message': 'Already logged!'})

        return render_template('user/logout.html',
                 title = 'Logout',
                 name = current_user.name,
                 next = url_for('user_signup'),
               )

    if request.method == 'POST':
        if form.validate():
            user = User(
                email = form.email.data,
                name = form.name.data,
                password = form.password.data,
            )
            db.session.add(user)
            db.session.commit()

            login_user(form.user, remember=form.remember.data)
            identity_changed.send(app, identity=Identity(form.user.id))

            if form.type.data == 'json':
                return jsonify({'result': 'ok'})

            flash('Thank you for registering!')
            return redirect(get_next())

        else:
            if form.type.data == 'json':
                return jsonify({'result': 'error', 'message': 'Invalid data!'})

    return render_template('user/signup.html',
             title = 'Registering new user',
             form = form,
             next = get_next(),
           )


@app.route('/signin', methods=['GET', 'POST'])
def user_signin(user=None):
    form = LoginForm(request.form)

    if not current_user.is_anonymous:
        if form.type.data == 'json':
            return jsonify({'result': 'error', 'message': 'Already logged!'})

        return render_template('user/logout.html',
                 title = 'Logout',
                 name = current_user.name,
                 next = url_for('user_signin'),
               )

    if request.method == 'POST':
        if form.validate():
            login_user(form.user, remember=form.remember.data)
            identity_changed.send(app, identity=Identity(form.user.id))

            if form.type.data == 'json':
                return jsonify({'result': 'ok'})

            flash('Successfully logged in as {0}'.format(form.user.name))
            return redirect(get_next())

        else:
            if form.type.data == 'json':
                return jsonify({'result': 'error', 'message': 'Invalid email or password!'})

    return render_template('user/signin.html',
             title = 'Sign in',
             form = form,
             next = get_next(),
           )


@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def user_change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST':
        if form.validate():
            form.user.change_password(form.password.data)
            db.session.commit()

            if form.type.data == 'json':
                return jsonify({'result': 'ok'})

            flash('Successfully changed password')
            return redirect(get_next())

        else:
            if form.type.data == 'json':
                return jsonify({'result': 'error', 'message': 'Invalid data!'})

    return render_template('user/change_password.html',
             title = 'Change Password',
             form = form,
             next = url_for('user_pofile'),
           )


@app.route("/confirm/<code>", methods=['GET', 'POST'])
def user_confirm(code=None):
    user = User.query.filter_by(verified=code).first()
    if user:
        status = 'verified'
        user.verified = ''
        db.session.commit()
    else:
        status = 'not verified'

    if request.method == 'POST':
        return jsonify({'result': 'ok', 'status': status})

    return render_template('user/confirm.html',
             title = 'Confirm email',
             status = status,
           )


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()

    for key in ('identity.id', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(app, identity=AnonymousIdentity())

    if request.method == 'POST':
        return jsonify({'result': 'ok'})

    return redirect(get_next())


@app.route("/delete", methods=['GET', 'POST'])
@login_required
def user_delete():
    current_user.active = -1
    db.session.commit()

    user_logout()

    if request.method == 'POST':
        return jsonify({'result': 'ok'})

    return redirect(get_next())


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        return jsonify({
            'result': 'ok',
            'name': current_user.name,
        })

    return render_template('user/profile.html',
             title = 'Profile',
             cu = current_user,
             verified = 'not verified' if current_user.verified else 'verified'
           )


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def user_edit():
    if request.method == 'POST':
        return jsonify({
            'result': 'ok',
            'name': current_user.name,
        })

    return render_template('user/edit.html',
             title = 'Edit profile',
             cu = current_user,
           )


@app.route("/logged", methods=['GET', 'POST'])
def user_logged():
    if request.method == 'POST':
        return jsonify({
            'result': 'ok',
            'is_anonymous': current_user.is_anonymous,
            'name': '' if current_user.is_anonymous else current_user.name,
        })

    return redirect(get_next())
