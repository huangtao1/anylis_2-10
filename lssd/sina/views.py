#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/17.
from . import sina
from flask import render_template, redirect, url_for, request, current_app
from flask_login import login_required
from datetime import datetime
from models import Nbadaily, Dailynews, Dailysound
from lssd import db
from ..utils.Sinanba import get_nba_data


@sina.route('nbadaily', methods=['GET', 'POST'])
@login_required
def nbadaily():
    # 获取今天是几号
    today_date = ''
    # 获取今天所有的比分
    all_matches = get_nba_data()
    # 获取今天比分的MP3的url
    today_mp3_url = Dailysound.query.filter(Dailysound.competing_time == today_date).first().daily_mp3_path
    # 获取今天的十条新闻展示
    all_news = Dailynews.query.filter(Dailynews.today_date == today_date).all()
    return render_template()
