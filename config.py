#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    # email config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SMTP_USER')
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWD')
    # database config
    DB_NAME = os.environ.get('LSSD_DB_NAME')
    DB_HOST = os.environ.get('LSSD_DB_HOST')
    DB_USER = os.environ.get('LSSD_DB_USER')
    DB_PASSWD = os.environ.get('LSSD_DB_PASSWD')
    # 球队数据
    NBA_TEAM_INFO = {''}
    # 每日比分存放目录
    NBA_SCORE_MP3=os.path.join(basedir,'lssd/static/NBA')
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(Config.DB_USER, Config.DB_PASSWD,
                                                                                 Config.DB_HOST, Config.DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://{0}:{1}@{2}:3306/{3}?charset=utf8'.format(Config.DB_USER, Config.DB_PASSWD,
                                                                                 Config.DB_HOST, Config.DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
    'production': ProductConfig,
    'default': DevelopmentConfig,
}