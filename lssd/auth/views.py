#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from . import auth
from flask import render_template, redirect, url_for, request, current_app

@auth.route('login',methods=['GET','POST'])
def login():
    """

    :return:
    """
    return render_template('auth/login.html')