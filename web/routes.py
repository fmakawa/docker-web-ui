import json
import sqlite3
import docker
import datetime
from flask import render_template, Flask,request
from web.models.models import Drolex
from sqlite3 import Error
from web.database import workdir
from web import app


removed_containers = []


def docker_client():
    clientdoc = docker.APIClient(
        base_url='unix://var/run/docker.sock',
        tls=False,
        user_agent="SWAT/Drolex",
        version='auto'
    )
    return clientdoc


def container_detail():
    containerz = docker_client().containers(all=True)
    container_id = []
    for container in containerz:
        container_id.append(container["Id"])

    # Get Commands
    data = []
    running_con = []
    restarting_con = []
    stopped_con = []
    paused_con = []
    web_con = []
    for ids in container_id:
        drolex = Drolex(conn_uri='unix://var/run/docker.sock',
                        loglevel='INFO')
        # Run the update method
        command = drolex.rerun(drolex.get_config(
            dockerID=ids),
            'Mode,HostConfig,User,NetworkSettings,Exposed,Ports,Mounts,Volumes,Env,Name,Image,Args'
        )
        config = docker_client().inspect_container(ids)
        # print("Container Config: \n" + str(config))
        status = ""
        for container in containerz:
            if ids == container["Id"]:
                status = container["Status"]
                # print("Status: " + status)
        json_con = {
            "Name": config["Name"].replace("/", "", 1),
            "Command": command,
            "Auto Remove": config["HostConfig"]["AutoRemove"],
            "Status": status,
            "Id": config["Id"],
            "Image": config["Config"]["Image"]
            }
        # print(json)
        # print("State: " + config["State"]["Status"])
        if "docker-web" in config["Config"]["Image"]:
            web_con.append(json_con)
        elif config["State"]["Status"] == "running":
            running_con.append(json_con)
        elif config["State"]["Status"] == "restarting":
            restarting_con.append(json_con)
        elif config["State"]["Status"] == "exited":
            stopped_con.append(json_con)
        elif config["State"]["Status"] == "paused":
            paused_con.append(json_con)
        else:
            data.append(json_con)

    # print(data)
    # print("running: \n" + str(running))
    # print("restarting: \n" + str(restarting))
    # print("stopped: \n" + str(stopped))
    # print("paused: \n" + str(paused))
    # print("other: \n" + str(data))
    states = ["running", "restarting", "stopped", "paused", "data"]

    return paused_con, data, running_con, restarting_con, stopped_con, states, web_con


@app.route('/')
@app.route('/index')
def index():
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
        "index.html",
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
        dockerweb = params[6],
        removed_containers=removed_containers
    )


@app.route('/inspect/<container>')
def inspect(container):
    config = docker_client().inspect_container(container)
    inspect_data=json.dumps(config)
    return render_template(
        "after_commands/after_inspect.html",
        inspect=config,
        inspect_data=inspect_data)


@app.route('/pause/<container>')
def pause(container):
    paused_config = docker_client().inspect_container(container)
    pause_cmd = docker_client().pause(container)
    params = container_detail()

    return render_template(
        "after_commands/after_paused.html",
        paused_config=paused_config,
        pause=pause_cmd,
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5]
    )


@app.route('/unpause/<container>')
def unpause(container):
    config = docker_client().inspect_container(container)
    unpause_cmd = docker_client().unpause(container)
    params = container_detail()
    return render_template(
        "after_commands/after_unpaused.html",
        unpaused_config=config,
        unpause_cmd=unpause_cmd,
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
    )


@app.route('/stop/<container>')
def stop(container):
    config = docker_client().inspect_container(container)
    stop_cmd = docker_client().stop(container)
    params = container_detail()
    return render_template(
        "after_commands/after_stopped.html",
        stopped_config=config,
        stopped_cmd=stop_cmd,
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
    )


@app.route('/restart/<container>')
def restart(container):
    config = docker_client().inspect_container(container)
    restart_cmd = docker_client().restart(container, timeout=10)
    params = container_detail()
    return render_template(
        "after_commands/after_restarted.html",
        restarted_config=config,
        restart_cmd=restart_cmd,
        paused=params[0],
        data=params[1],
        running=params[2],
        restarting=params[3],
        stopped=params[4],
        states=params[5],
    )


# cache removal so we know the commands. database perhaps? Or simply persist in a list.
# Safe to have it stored somewhere so we don't lose persistance if container/server is stopped
@app.route('/remove/<container>')
def remove(container):
    config = docker_client().inspect_container(container)
    drolex = Drolex(conn_uri='unix://var/run/docker.sock',
                    loglevel='INFO')
    # Run the update method
    command = drolex.rerun(drolex.get_config(
        dockerID=container),
        'Mode,HostConfig,NetworkSettings,Exposed,Ports,Mounts,Env,Name,Image,Args'
    )
    name = config["Name"].replace("/", "", 1)
    removed_containers.append({
        "Name": name,
        "Run_Command": command
    })
    remove_cmd = docker_client().remove_container(container, force=True)
    currentdt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    params = container_detail()
    msg = "msg"
    try:
        with sqlite3.connect(workdir + "/database/removedcontainers.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into RemovedContainers (name, command, date) values (?,?,?)", (name, command, currentdt))
            con.commit()
            msg = "Removed container successfully added to db"
    except Error as e:
        con.rollback()
        print(e)
        msg = "We can not add the removed container to the database"
    finally:
        return render_template(
            "after_commands/after_removed.html",
            removed_config=config,
            remove_cmd=remove_cmd,
            paused=params[0],
            data=params[1],
            running=params[2],
            restarting=params[3],
            stopped=params[4],
            states=params[5],
            msg=msg
        )


@app.route('/running')
def running():
    params = container_detail()

    return render_template(
        "all_containers/running_all.html",
        running=params[2]
    )


@app.route('/paused')
def paused():
    params = container_detail()

    return render_template(
        "all_containers/paused_all.html",
        paused=params[0]
    )


@app.route('/removed')
def removed():
    # params = container_detail()
    msg = "msg"
    rows = ""
    try:
        with sqlite3.connect(workdir + "/database/removedcontainers.db") as con:
            cur = con.cursor()
            #n_estimate = cur.execute("SELECT COUNT() FROM RemovedContainers").fetchone()[0]
            cur.execute("SELECT * FROM RemovedContainers ORDER BY id DESC LIMIT 20")
            rows = cur.fetchall()
            con.commit()
            msg = "Collected the most recent 20 records, if existing"
            #print(str(rows))
    except Error as e:
        con.rollback()
        print(e)
        msg = "We can not add the removed container to the database"
    finally:
        return render_template(
            "all_containers/removed_all.html",
            removed_containers=removed_containers,
            msg=msg,
            database=rows
        )


@app.route('/stopped')
def stopped():
    params = container_detail()

    return render_template(
        "all_containers/stopped_all.html",
        stopped=params[4]
    )


@app.route('/health')
def health():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return "This route does not exist '{}'".format(request.url), 404


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error. Check the server logs.', 500