#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from . import auth
from flask import render_template, redirect, url_for, request, current_app, flash, session
from models import User
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from lssd import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录模块
    """
    if request.method == 'POST':
        user_name = request.form['username']
        user_password = request.form['password']
        user = User.query.filter(User.username == user_name).first()
        if user is not None and user.pass_check(user.password_hash, user_password):
            # 登录成功

            login_user(user, True)
            user.last_seen = datetime.now()
            db.session.add(user)
            db.session.commit()
            # 添加session
            session['user'] = {'username': user.username, 'display_name': user.display_name, 'email': user.email,
                               'role': user.role.name}
            return redirect(request.args.get('next') or url_for(user.role.index_menu.menu_url))
        flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')


@auth.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    添加用户
    """
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['email']
        if User.query.filter(db.or_(User.username == user_name, User.email == user_email)).first():
            flash('User has been exisit!!!', 'warning')
        user = User()
        user_password = request.form['password']
        user_display = request.form['nickname']
        user_location = request.form['location']
        user_role_id = 2
        user.username = user_name
        user.password_hash = user.pass_exchange(user_password)
        user.member_since = datetime.now()
        user.active = True
        user.email = user_email
        user.display_name = user_display
        user.role_id = user_role_id
        user.location = user_location
        db.session.add(user)
        db.session.commit()
        flash('Add user successful', 'success')
        return redirect(url_for('main.admin_home'))
    return render_template('auth/regist.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have loged out successful', 'success')
    return redirect(url_for('auth.login'))
