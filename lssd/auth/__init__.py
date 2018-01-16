#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.
from flask import Blueprint

auth = Blueprint('auth',__name__)
from . import views