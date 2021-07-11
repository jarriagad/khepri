# Khepri

[![forthebadge](https://forthebadge.com/images/badges/just-plain-nasty.svg)](https://forthebadge.com)

## Script to automate backup of docker volumes

Khepri uses the Docker python SDK to find desired containers / volumes and back them up to a specified directory.

How-to: (Current usage for *develop* branch)

By default, Khepri will try to back up all containers as it is impartial to container status
If you would like to backup select containers, edit the list named `target_containers` and include all containers you want backed up

By default, the script stored the backups in the directory that it was executed from.
To change this, change the variable `custom_backup_path` to a desired path.
IE: `custom_backup_path = "/path/to/backup"`

Once config has been set, initiate script with:
`./khepri`


TODO:
- Implement config / .env file
- Fix stdout
- Fix timestamp feature
