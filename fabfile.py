from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['dot@kapsi.fi']


def deploy():
    local("git push")
    code_dir = '/home/users/dot/django_apps/graffathon'
    with cd(code_dir):
        run("git pull")
    with warn_only():
        run("ps aux |grep gunicorn |grep graffathon | awk '{ print $2 }' |grep -E '[0-9]{2,}' |xargs kill -HUP")

    print("Project deployed")