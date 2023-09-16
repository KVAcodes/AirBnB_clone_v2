#!/usr/bin/python3
""" a Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""
from fabric.api import *
import os.path


env.hosts = ['18.234.253.121', '52.87.220.207']


def do_pack():
    """Fab func."""
    result = local(
        "mkdir -p versions\n"
        "date_format=$(date \"+%Y%m%d%H%M%S\")\n"
        "tar -czvf \"versions/web_static_${date_format}.tgz\" web_static/*",
        capture=True
    )
    if result.return_code == 0:
        return result.stdout.split()[-1]
    else:
        return None


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

    archive_name = archive_path.split('/')[-1]
    archive_name_wt_ext = archive_name.split('.')[0]

    run_result = run(
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
    )
    if run_result.failed:
        return False
    return True


def deploy():
    """makes use of do_pack and do_deploy,
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
