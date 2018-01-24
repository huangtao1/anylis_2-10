#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/16.

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from lssd import db, login_manager
from flask_login import UserMixin


class Role(db.Model):
    """角色"""

    __tablename__ = 'lssd_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)
    index_page = db.Column(db.String(64))
    menu = db.Column(db.String(200))

    def __repr__(self):
        return '<Role %r>' % self.name

    def __getitem__(self, item):
        return getattr(self, item)


class User(UserMixin,db.Model):
    """用户"""

    __tablename__ = 'lssd_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    display_name = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('lssd_role.id'))
    role = db.relationship('Role', backref=db.backref('user', order_by=id))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.now())
    last_seen = db.Column(db.DateTime(), default=datetime.now())
    active = db.Column(db.Boolean, default=True)
    real_avatar =db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    def __getitem__(self, item):
        return getattr(self, item)
    def pass_check(self,pass_hash,password):
        return check_password_hash(pass_hash,password)
    def pass_exchange(self,password):
        return generate_password_hash(password)

#登录必须要加载此装饰器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))