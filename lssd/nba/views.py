#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/17.
from . import nba
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required
from datetime import datetime
from models import Nbadaily, Dailynews
from ..utils.Sinanba import exchange_nba_data
import json


@nba.route('/nbadaily', methods=['GET', 'POST'])
@login_required
def nbadaily():
    """
    可能会存在加载慢,为了保证每次都是新的数据需要刷新
    :return:
    """
    exchange_nba_data()
    # 获取数据加载到页面
    today_data = Nbadaily.query.filter(Nbadaily.competing_time == datetime.now().strftime('%Y-%m-%d')).first()
    # print datetime.now().strftime('%Y-%m-%d')
    # [{"score": "102:104", "match": "u7070u718a:u6d3bu585e"}
    return render_template('nba/nbadaily.html', all_match=json.loads(today_data.today_content))
