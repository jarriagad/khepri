#!/usr/bin/env python3

from datetime import datetime
from pprint import pprint as print
import random
import string
import docker
import os


def sanitizeContainerList(target_containers):
    # Sanitizes list and returns list of container objects
    if not target_containers:
        message = "No explicitly listed containers to back up. \nBacking up all containers..."
        target_containers = client.containers.list(all="True")
    elif "running" in target_containers:
        message = "Selecing RUNNING containers:"
        target_containers = client.containers.list(all="True", filters={"status":"running"})
    else:
        message = "Custom list: Checking containers...   "
        target_containers_temp = []
        for i in target_containers:
            try:
                target_containers_temp.append(client.containers.get(i))
            except:
                print("Container {0} not found. Skipping.".format(i))
                pass
        target_containers = target_containers_temp
    return target_containers



def createBackupDir(target_container, local_backup_path=False):
    """
    Checks for a specified back up path, if no path cwd is used.
    Checks for a directory to save backup to, if none one is created
    """
    pwd = os.getcwd()
    backup_dir = target_container + "_backups"
    # Check if local path is set
    if not local_backup_path:
        local_backup_path = pwd

    full_path = local_backup_path + "/" + backup_dir
    if not os.path.isdir(full_path):
        print("Back up directory for {0} not found.".format(target_container))
        os.makedirs(full_path)
        print( full_path + " has been created") 
    else:
        pass

    return full_path

def getRandomString(length, name_prefix = "khe-worker"):
    """
    Generates name + random string
    """
    letters = string.ascii_lowercase
    random_str = ''.join(random.choice(letters) for i in range(length))
    result_str = name_prefix + "-" + random_str
    return result_str

"""
docker run --rm --volumes-from <target_container> -v <full_backup_path>:/backup alpine tar cvf /backup/backup.tar /<target_backup_dir>
"""

client = docker.from_env()
def backupContainer(target_container_name, volume_name, volume_dir, full_dir):
    worker_container_name = getRandomString(5)
    my_date = datetime.now()
    timestamp = my_date.strftime('%Y-%m-%D_%H-%M-%S')
    internal_backup_dir = "/backup/" + target_container_name + "_" + volume_name + ".bak.tar"
    command_list = ["tar", "cvf", internal_backup_dir, volume_dir]
    client.containers.run(
            'jarriagada/alpine-sync',
            name=worker_container_name,
            volumes_from=[target_container_name],
            volumes={full_dir: {'bind':'/backup', 'mode': 'rw'}},
            command=command_list,
            detach=True,
            auto_remove=True,
            remove=True,
            )


def getVolumeList(target_containers_list):
    #Purpose is to have a "-l" flag that only prints the found volumes.
    for container in target_containers_list:
        mounts = container.attrs.get("Mounts")
        target_container_name = container.name
        print("Container: " + target_container_name)
        for vol in mounts:
            print("  Volume: " + vol['Name'])
            print("  Source: " + vol['Source'])



