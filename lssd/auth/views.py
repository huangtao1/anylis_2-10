#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from . import auth

@auth.route('login',methods=['GET','POST'])
def login():
    return "login"