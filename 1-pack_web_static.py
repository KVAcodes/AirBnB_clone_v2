#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static folder.
"""

from fabric.api import local


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
