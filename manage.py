#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2018/1/15.

#!/usr/bin/env python
import os
from lssd import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()