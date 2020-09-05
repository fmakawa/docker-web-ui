import sqlite3
from os import path, environ
import os 

workdir = os.environ['DOCKER_WEB_HOME']

def createdb():
    if not path.isfile(workdir + "/database/removedcontainers.db"):
        con = sqlite3.connect(workdir + "/database/removedcontainers.db")
        print("Database opened successfully")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS RemovedContainers \
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, command TEXT NOT NULL, date TEXT NOT NULL)"
        )

        print("Table created successfully")
        con.commit()
        con.close()
    else:
        print("Database already existed")
