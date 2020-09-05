# Drolex - Docker Run Online Extractor

Drolex is a command-line tool (for now) for extracting docker run commands from running containers. At this point it is
meant for simple use cases, so it might miss more advanced parameters.

## Use

You can always run the tool with the `--help` flag to show the usage info:

```shell
usage: drolex.py [-h] [--conn_uri CONN_URI] [--tls_cert TLS_CERT]
                 [--loglevel {DEBUG,INFO,WARNING,ERROR}] --ID ID
                 [--order ORDER]

DROLEX - Docker Run OnLine EXtractor

optional arguments:
  -h, --help            show this help message and exit
  --conn_uri CONN_URI   Address and port of docker server Ex: --conn_uri
                        "tcp://127.0.0.1:1234" (Default:
                        unix://var/run/docker.sock)
  --loglevel {DEBUG,INFO,WARNING,ERROR}
                        LogLevel of the app. (Default: INFO)
  --ID ID               Container ID to check
  --order ORDER         Order in which to print the different parts of the
                        docker run command (Default: Mode,HostConfig,User,NetworkSettings,Exposed,Ports,Mounts,Volumes,Env,Name,Image,Args)

```

Note that, for remote use, the Docker daemon must be listening on it's TCP port.
To configure it you must edit `/etc/sysconfig/docker` and add the following in the `OPTIONS` field:
```shell
-H unix://var/run/docker.sock -H tcp://0.0.0.0:2375
```

after that reload the daemon's config and relaunch it:
```shell
sudo systemctl daemon-reload
sudo systemctl restart docker.service
```

### Running from source

To run from source, the following command can be used to install the app's dependencies:

```shell
pip install -r requirements.txt
```

After that the tool can be run through drolex.py

### Running the container (recommended)

Drolex can also be run as a container by using the following command:

```shell
docker run -m 128m -it --rm -v /var/run/docker.sock:/var/run/docker.sock --name drolex artifactory.qvantel.net/drolex2:1.0.0 --ID zookeeper
```

> Note:
> Even though it's dockerized, the arguments placed after the image parameter behave in the same way as the python
> script when running from source.

## TODO

This application is still in development as the goal is to have it run as a service with a web ui and connect to other
remote server's docker daemons securely. It's progress can be followed through these tickets:

- TLS connection to the docker service
- UI