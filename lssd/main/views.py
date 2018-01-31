#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from . import main
from flask import render_template, redirect, url_for, request, flash, current_app, jsonify, g, session, send_file
from flask_login import login_user, logout_user, login_required, current_user


@main.route('/')
@login_required
def home_index():
    return redirect(url_for(current_user.role.index_menu.menu_url))

@main.route('/admin_home')
@login_required
def admin_home():
    return render_template('main/admin.html')


@main.route('/user_home')
@login_required
def user_home():
    return render_template('main/user.html')

