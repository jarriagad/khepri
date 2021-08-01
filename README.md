# Khepri

[![forthebadge](https://forthebadge.com/images/badges/just-plain-nasty.svg)](https://forthebadge.com)

## Script to automate backup of docker volumes

Khepri uses the Docker python SDK to find desired containers / volumes and back them up to a specified directory.

How-to: 

By default, Khepri will try to back up all containers' volumes as it is impartial to container status.
If you would like to backup specific containers, edit the list named `target_containers` and include all containers you want backed up

By default, the script stores the backups in the directory that it was executed from ($PWD).
To change this, change the variable `custom_backup_path` to a desired path or add the path as the last CLI argument.

IE: `custom_backup_path = "/path/to/backup"`

Note: Make sure that last "/" in path is not included.

Once config has been set, initiate script with:
`./khepri -[stzhl] [Backup_path]`

Script must be run by user in docker group.

CLI parameter flags:
- `-l` --> Used to list specified containers along with attached volumes.
- `-h` --> Used to show help page.
- `-t' --> Creates a tarball for each volume that is backed up.
- `-tz` --> Creates a compressed tarball for each volume.
- `-s` or `-sync` --> Incremental backups of volumes. This is also the fastes option. 

Usage:
1. Back up volumes to working directory:
`khepri -s`

2. Compress volumes and store them in custom directory:
`khepri -tz /backup/path`

Dependencies:
- Docker SDK
- jarriagada/alpine-sync (will be downloaded automatically if not available)

TODO:
- Fix timestamp feature
