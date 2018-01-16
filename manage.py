#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.

#!/usr/bin/env python
import os
from lssd import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from lssd.auth.models import User,Role
app = create_app(os.getenv('tms') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()