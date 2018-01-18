#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/17.
from lssd import db


class Nbadaily(db.model):
    """
    每天nba比赛结果存储
    """
    __tablename__ = 'lssd_hupunba_daily'
    id = db.Column(db.Integer, primary_key=True)
    master_team = db.Column(db.String(64))
    visit_team = db.Column(db.String(64))
    master_score = db.Column(db.String(64))
    visit_score = db.Column(db.string(64))
    competing_time = db.Column(db.Date)

    def __repr__(self):
        return 'NBADaily_report:{0}'.format(self.competing_time)


class Dailysound(db.model):
    """
    每天nba结果转换成mp3存放的地址
    """
    __tablename__ = 'lssd_hupudaily_mp3'
    id = db.Column(db.Integer, primary_key=True)
    daily_mp3_path = db.Column(db.Text)
    competing_time = db.Column(db.Date)

    def __repr__(self):
        return 'NBADaily_mp3:{0}'.format(self.competing_time)


class Dailynews(db.model):
    """
    每天的NBA头条新闻
    """
    __tablename__ = 'lssd_dailynews'
    id = db.Column(db.Integer, primary_key=True)
    today_date = db.Column(db.Date)
    news_content = db.Column(db.Text)

    def __repr__(self):
        return 'Dailynews:{0}'.format(self.today_date)