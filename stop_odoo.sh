#!/bin/bash

# Change to the directory where your docker-compose.yml is located
cd /opt/odoo/

# Stop and remove the Docker containers
/usr/bin/python3 /home/ubuntu/.local/bin/docker-compose down

