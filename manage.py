# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.collect import Collect

from app import app

manager = Manager(app)
collect = Collect()
collect.init_app(app)
collect.init_script(manager)


@manager.command
def freeze():
    from flask.ext.frozen import Freezer
    freezer = Freezer(app)
    freezer.freeze()
    print "Static page created at app/build/"


@manager.command
def deploy():
    print "Freezing page..."
    freeze()
    print "Done..."


if __name__ == "__main__":
    manager.run()
