import json
import sqlite3
import docker
import datetime
from flask import render_template, Flask,request
from web.database import workdir
from web import app
from web.routes_util import containers, overview, system_info
from web.routes_util.containers import docker_client, container_detail, removed_containers

@app.route('/health')
def health():
    pass

@app.route('/help')
def help():
    return render_template(
        "help.html"
    )

@app.errorhandler(404)
def page_not_found(error):
    return "This route does not exist '{}'".format(request.url), 404


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error. Check the server logs.', 500

@app.route('/test')
def test():
    params = container_detail()
    return render_template(
        "test.html",
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
