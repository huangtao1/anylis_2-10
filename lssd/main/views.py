#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from . import main
from flask import render_template, redirect, url_for, request, flash, current_app, jsonify, g, session, send_file
from flask_login import login_user, logout_user, login_required, current_user

@main.route('/')
def home_index():
    return 'aaaa'