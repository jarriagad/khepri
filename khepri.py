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

client = docker.from_env()
# target list can be left empty, as "running", or select explicit container names or short_ids... long IDs might also work.
target_containers = [
        "pihole05",
        ]

def name_2_id(container_name):
    """
    Turns container name into container short_ID
    """
    container_id = client.containers.get(container_name).short_id
    return container_id


# Parses provided list for special keywords, or container names
if not target_containers:
    print("No explicitly listed containers to back up.")
    print("Backing up all containers...")
    target_containers = client.containers.list(all="True")
elif "running" in target_containers:
    print("Only backing up running containers")
    target_containers = client.containers.list(all="True", filters={"status":"running"})
else:
    print("Custom list: Checking containers...   ")
    target_containers2 = []
    for i in target_containers:
        print("Trying: %s" % (i))
        try:
            target_containers2.append(client.containers.get(i))
            print("OK.")
        except:
            print("Container not found. Skipping.")
            pass

    target_containers = target_containers2   

print(target_containers)

#Loop through each container and find any attached volumes
for containers in target_containers:
    mounts = containers.attrs.get("Mounts")
    for x in mounts:
        volume_name = x["Name"]
        volume_dir = x["Destination"]
        print(volume_name)
        print(volume_dir)
