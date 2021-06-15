# Khepri

[![forthebadge](https://forthebadge.com/images/badges/just-plain-nasty.svg)](https://forthebadge.com)

## Script to automate backup of docker volumes

Khepri uses the Docker python SDK to find desired containers / volumes and back them up to a specified directory.

How-to:

First, make sure that you have edited the .env file to your liking.
If .env is left as default, or not existant, Khepri will back up all volumes found in the node that it is running on.

`vim .env'
`./khepri.py`


TODO:
- Implement config / .env file
- Fix backup() function
