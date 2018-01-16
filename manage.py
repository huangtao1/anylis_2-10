#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.

# !/usr/bin/env python
import os
from lssd import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from lssd.auth.models import User, Role

app = create_app(os.getenv('tms') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def profile(length=25, profile_dir=None):
    """
    Start the application under the code profiler.
    在代码分析器中运行应用
    """
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """执行部署任务"""
    from flask.ext.migrate import upgrade

    upgrade()


if __name__ == '__main__':
    manager.run()
