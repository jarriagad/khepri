#!/usr/bin/env python3

"""
Script: khepri.py
Usage: ./khepri.py
Author: Javier Arriagada
Created: 6/13/2021
Version: 0.1.0
Description: Tool to assit with back up of docker containers
"""

"""
Steps:
    1. Identify volumes to back up
    2. Identify backup storage location
    3. Incremental changes only using rsync or something
    4. clean up after itself
"""
from pprint import pprint as print
import docker
import os

client = docker.from_env()
# target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.

target_containers = [
        "pihole05",
        ]

# Parses provided list for special keywords, or container names, returns list of all real selected containers target_containers 
if not target_containers:
    print("No explicitly listed containers to back up.")
    print("Backing up all containers...")
    target_containers = client.containers.list(all="True")
elif "running" in target_containers:
    print("Only backing up running containers")
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
for containers in target_containers:
    mounts = containers.attrs.get("Mounts")
    for x in mounts:
        volume_name = x["Name"]
        volume_dir = x["Destination"]
        print(volume_name)
        print(volume_dir)

# Function to complete the backup
def backup(container, volume_dir):
    """
    Runs container that attaches to volumes from target_containers and backs them up locally
    docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
    """
    pwd = os.getcwd()
    volume_list = [container]
    command_list = ["tar", "cvf", "/backup/backup1.tar", volume_dir]
    client.containers.run(
            'alpine',
            name="Backerup02",
            volumes_from=["plex02"],
            volumes={"/home/javier/": {'bind':'/backup', 'mode': 'rw'}},
            command=["tar", "cvf", "/backup/backup2.tar", "/config"]
            )

backup("plex02", "/config")





