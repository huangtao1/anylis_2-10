#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/17.
from flask import Blueprint

hupu = Blueprint('hupu',__name__)
from . import views