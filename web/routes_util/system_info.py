import platform,socket,re,uuid,json,psutil,logging
import sqlite3
import docker
import datetime
from flask import render_template, Flask,request
from web.models.models import Drolex
from sqlite3 import Error
from web.database import workdir
from web import app
from web.routes_util.containers import docker_client, container_detail, removed_containers

def getSystemInfo():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

json.loads(getSystemInfo())

@app.route('/system')
def system():
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
        section='containers'
    )
