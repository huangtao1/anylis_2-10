#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/16.

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from lssd import db, login_manager
from flask_login import UserMixin
import hashlib
from flask import request


class Role(db.Model):
    """角色"""

    __tablename__ = 'lssd_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index_menu_id = db.Column(db.Integer, db.ForeignKey('lssd_menu.id'))
    index_menu = db.relationship('Menu', backref=db.backref('role'))
    menus = db.Column(db.String(200))

    def __repr__(self):
        return '<Role %r>' % self.name

    def __getitem__(self, item):
        return getattr(self, item)


class User(UserMixin, db.Model):
    """用户"""

    __tablename__ = 'lssd_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(128), unique=True, index=True)
    display_name = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('lssd_role.id'))
    role = db.relationship('Role', backref=db.backref('user', order_by=id))
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.now())
    last_seen = db.Column(db.DateTime(), default=datetime.now())
    active = db.Column(db.Boolean, default=True)
    real_avatar = db.Column(db.String(128))
    menu = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def __getitem__(self, item):
        return getattr(self, item)

    def pass_check(self, pass_hash, password):
        return check_password_hash(pass_hash, password)

    def pass_exchange(self, password):
        return generate_password_hash(password)

    def get_mail_hash(self):
        self.real_avatar = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'

        else:
            url = 'http://www.gravatar.com/avatar'
            hash = self.real_avatar or hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


# 登录必须要加载此装饰器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Menu(db.Model):
    """菜单"""
    __tablename__ = 'lssd_menu'

    id = db.Column(db.Integer, primary_key=True)
    menu_url = db.Column(db.String(64), unique=True)
    menu_desc = db.Column(db.String(64))
    parent_id = db.Column(db.Integer,nullable=True)
    is_parent = db.Column(db.Boolean,default=False)
