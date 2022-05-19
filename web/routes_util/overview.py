import platform,socket,re,uuid,json,psutil,logging
import sqlite3
import docker
import datetime
from flask import render_template, Flask,request
from sqlite3 import Error
from web.models.models import Drolex
from web.database import workdir
from web import app
from web.routes_util.containers import docker_client, container_detail, removed_containers
from web.routes_util.system_info import getSystemInfo


@app.route('/overview')
def overview():
    # Get container IDs
    # container_id = []
    # containerz = docker_client().containers(all=True)

    """
    print("List of containers: \n" + str(containerz))
    for container in containerz:

        container_id.append(container["Id"])
    print("container IDs: " + str(container_id))
    """
    # Get Commands
    params = container_detail()

    return render_template(
        "containers/index.html",
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
        dockerweb = params[6],
        removed_containers=removed_containers,
        section='null'
    )
