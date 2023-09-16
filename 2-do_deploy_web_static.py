#!/usr/bin/python3
""" A Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to my web servers, using the function
do_deploy:
"""
from fabric.api import *


env.hosts = ['18.234.253.121', '52.87.220.207']


def do_deploy(archive_path):
    """Deploys the archive containing the web_static of thr
    Airbnb project.
    """
    put_result = put(
        archive_path,
        '/tmp/'
    )
    if put_result.failed:
        return False

    archive_name = archive_path.split('/')[-1]
    archive_name_wt_ext = archive_name.split('.')[0]

    sudo_result = sudo(
        f"mkdir -p /data/web_static/releases/{archive_name_wt_ext}\n"
        f"tar -xzf /tmp/{archive_name} -C "
        f"/data/web_static/releases/{archive_name_wt_ext}\n"
        f"mv /data/web_static/releases/{archive_name_wt_ext}/web_static/* "
        f"/data/web_static/releases/{archive_name_wt_ext}/\n"
        f"rm -rf /data/web_static/releases/{archive_name_wt_ext}/web_static\n"
        f"rm /tmp/{archive_name}\n"
        f"rm -rf /data/web_static/current\n"
        f"ln -s /data/web_static/releases/{archive_name_wt_ext}/ "
        f"/data/web_static/current\n"
        f"nginx -s reload\n"
    )
    if sudo_result.failed:
        return False
    return True
