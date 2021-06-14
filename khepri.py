#!/usr/bin/env python3

import docker

client = docker.from_env()

running_containers = client.containers.list(all=True, filters={"status":"running"})
all_containers = client.containers.list(all=True)

for i in running_containers:
    container_id = i.short_id
    container = client.containers.get(container_id)
    print(container.attrs.get("Mounts"))
