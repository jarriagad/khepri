#!/usr/bin/env python3

"""
Script: khepri.py
Usage: ./khepri.py
Author: Javier Arriagada
Created: 6/13/2021
Version: 0.1.0
Description: Tool to assit with back up of docker containers
"""

import os
import docker
from functions import createBackupDir, backupContainer

""" For Testing """
from pprint import pprint as print

# target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.
target_containers = [
        ]

custom_backup_path = False
""""""

client = docker.from_env()

# Sanitizes list and returns list of container objects
if not target_containers:
    print("No explicitly listed containers to back up.")
    print("Backing up all containers...")
    target_containers = client.containers.list(all="True")
elif "running" in target_containers:
    print("Selecing RUNNING containers:")
    target_containers = client.containers.list(all="True", filters={"status":"running"})
else:
    print("Custom list: Checking containers...   ")
    target_containers_temp = []
    for i in target_containers:
        print("Trying: %s" % (i))
        try:
            target_containers_temp.append(client.containers.get(i))
            print("OK.")
        except:
            print("Container not found. Skipping.")
            pass
    target_containers = target_containers_temp

#Loop through each container and find any attached volumes
for container in target_containers:
    mounts = container.attrs.get("Mounts")
    target_container_name = container.name
    full_path = createBackupDir(target_container_name, custom_backup_path)
    print(full_path)
    for x in mounts:
        try:
            volume_name = x["Name"]
            volume_dir = x["Destination"]
        except:
            exit(99)
        print("Backing up " + target_container_name + ":" + volume_dir)
        backupContainer(target_container_name, volume_name, volume_dir, full_path)

