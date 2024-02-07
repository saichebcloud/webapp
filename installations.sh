#!/bin/bash


dnf -y install python3
yum -y install python3-pip
pip3 install --upgrade pip
yum -y install unzip

dnf -y install mariadb-server

systemctl start mariadb

DEMO_DIR="demo"
ENV_FILE="$DEMO_DIR/.env"

if [ ! -d "$DEMO_DIR" ]; then
    mkdir "$DEMO_DIR"
fi

if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
fi

echo "Installation completed successfully."

