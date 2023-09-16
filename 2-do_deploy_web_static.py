#!/usr/bin/python3
""" A Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to my web servers, using the function
do_deploy:
"""
from fabric.api import *
import os.path

env.hosts = ['18.234.253.121', '52.87.220.207']


def do_deploy(archive_path):
    """Deploys the archive containing the web_static of thr
    Airbnb project.
    """
    if os.path.isfile(archive_path) is False:
        return False

    put_result = put(
        archive_path,
        '/tmp/'
    )
    if put_result.failed:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
