#!/usr/bin/env python3

from datetime import datetime
from pprint import pprint as print
import random
import string
import docker
import os



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

def getRandomString(length):
    """
    Generates random string
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

"""
docker run --rm --volumes-from <target_container> -v <full_backup_path>:/backup alpine tar cvf /backup/backup.tar /<target_backup_dir>
"""

client = docker.from_env()
def backupContainer(target_container_name, volume_name, volume_dir, full_dir):
    worker_container_name = "khe-worker-" + getRandomString(5)
    my_date = datetime.now()
    timestamp = my_date.strftime('%Y-%m-%D_%H-%M-%S')
    internal_backup_dir = "/backup/" + target_container_name + "_" + volume_name + ".bak"
    command_list = ["tar", "cvf", internal_backup_dir, volume_dir]
    client.containers.run(
            'alpine',
            name=worker_container_name,
            volumes_from=[target_container_name],
            volumes={full_dir: {'bind':'/backup', 'mode': 'rw'}},
            command=command_list,
            detach=True,
            auto_remove=True,
            remove=True,
            )



