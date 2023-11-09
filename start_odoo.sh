#!/bin/bash

# Change to the directory where your docker-compose.yml is located
cd /opt/odoo/

# Start your Docker containers
/usr/bin/python3 /home/ubuntu/.local/bin/docker-compose up -d

