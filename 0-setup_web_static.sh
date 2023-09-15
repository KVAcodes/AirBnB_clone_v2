#!/usr/bin/env bash
# Sets up my web servers for the deployment of web_static.

# Installs Nginx if not already installed
if ! dpkg -l | grep -q "nginx"
then
sudo apt-get -y update
sudo apt-get -y install nginx
ufw allow 'Nginx HTTP'

# Creates the necessary directories
mkdir -p /data/web_static/releases/test/
mkdir /data/web_static/shared/

# Creates index.html file.
html_content="<html>
\t<head>
\t</head>
\t<body>
\t\tHolberton School
\t/body>
</html>"

echo -e "$html_content" > /data/web_static/releases/test/index.html

# Creates a symbolic link, deletes and recreates it if it exists.
if [ -L /data/web_static/current ]
then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Gives ownership of /data folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data


