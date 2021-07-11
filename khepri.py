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
import os
import docker
from test_khe import createBackupDir, backupContainer

""" For Testing """
from pprint import pprint as print

# target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.
target_containers = [
        ]
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
    full_path = createBackupDir(target_container_name)
    print(full_path)
    for x in mounts:
        volume_name = x["Name"]
        volume_dir = x["Destination"]
        backupContainer(target_container_name, volume_name, volume_dir, full_path)

# Function to complete the backup
def backup(container, volume_dir):
    #Runs container that attaches to volumes from target_containers and backs them up locally - (to working directory)
    #docker run --rm --volumes-from <container-to-be-backedup> -v $(pwd):/backup alpine tar cvf /backup/backup.tar /dbdata
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



def backup_test(container, external_backup_dir):
    container_name = "bu-" + container
    internal_backup_dir = "/backup/backup.tar"
    command_list = ["tar", "cvf", internal_backup_dir, external_backup_dir]
    client.containers.run(
            'alpine',
            name=container_name,
            volumes_from=[container],
            volumes={pwd: {'bind':'/backup', 'mode': 'rw'}},
            command=command_list,
            )



