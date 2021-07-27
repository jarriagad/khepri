#!/usr/bin/env python3

"""
Script: khepri.py
Usage: ./khepri.py
Author: Javier Arriagada
Created: 6/13/2021
Version: 0.1.0
Description: Tool to assit with back up of docker containers
"""

import sys
import docker
from functions import createBackupDir, backupContainer, getVolumeList, sanitizeContainerList

""" For Testing """
#from pprint import pprint as print



""""""
def main():
    # target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.
    target_containers = [
        "pihole05"
        ]
    client = docker.from_env()
    custom_backup_path = False

    #Function returns list of workable container IDs 
    target_containers = sanitizeContainerList(target_containers)

    #This following section will be used to construct the CLI flags allowed
    # Flag 1. "-l" lists selected containers in "target_container" list and displays attached volumes
    if sys.argv[-1] == "-l":
        getVolumeList(target_containers)
        exit(0)
    else:
        pass

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

if __name__ == "__main__":
    main()

