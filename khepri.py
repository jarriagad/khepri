#!/usr/bin/env python3

"""
Script: khepri.py
Usage: ./khepri.py
Author: Javier Arriagada
Created: 6/13/2021
Version: 1.1.0
Description: Tool to assit with back up of docker containers
"""

import sys
import docker
from functions import createBackupDir, backupContainer, getVolumeList, sanitizeContainerList, getImage, fixTroubleChild

def main():
    # target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.
    target_containers = []
    #Custom backup path is set here!
    custom_backup_path = False


    client = docker.from_env()
    #Fetch image
    getImage()
    #Function returns list of workable container IDs 
    target_containers = sanitizeContainerList(target_containers)
    arg_list = ["-t", "-tz", "-s", "-sync", "-h", "-l"]
    #This following section will be used to construct the CLI flags allowed
    # Flag 1. "-l" lists selected containers in "target_container" list and displays attached volumes
    if len(sys.argv) == 1 or sys.argv[1] not in arg_list:
        print("Invalid argument\nFor help: $ khepri -h")
        exit(99)
    elif sys.argv[1] == "-l":
        getVolumeList(target_containers)
        exit(0)
    elif sys.argv[1] == "-h":
        print("""
        Welcome to Khrepi, container volume back up system.

        Khepri has been designed with ease of use in mind.

        Simply run:
        $ ./khepri -s <-- This will back up all volumes attached to any container

        Arguments:
        -t ----> Create a tarball for each volume volume backed up.
        -tz ----> Creates a compressed tarball for each volume backed up.
        -s or -sync ----> Uses rsync "archive" which will create incremental back ups of the volumes.

        A custom back up destination can be set as a second argument:
        $ khepri -sync /backup/destination

        """)
        exit(0)

    if len(sys.argv) == 3:
       custom_backup_path = sys.argv[2] 
    elif len(sys.argv) > 3:
        print("Too many arguments\nFor help: $ khepri -h")
        exit(99)

    #Loop through each container and find any attached volumes
    for container in target_containers:
        mounts = container.attrs.get("Mounts")
        target_container_name = container.name
        full_path = createBackupDir(target_container_name, custom_backup_path)
        for x in mounts:
            try:
                try:
                    volume_name = x["Name"]
                except:
                    volume_name = fixTroubleChild(x["Source"])
                volume_dir = x["Destination"]
            except:
                print("Failure: Issue finding volume attributes")
                exit(99)
            print("Backing up " + target_container_name + ":" + volume_dir)
            backupContainer(target_container_name, volume_name, volume_dir, full_path, sys.argv[1])

if __name__ == "__main__":
    main()

