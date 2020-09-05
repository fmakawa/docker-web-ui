# docker-web-ui

A Docker UI to manage containers in a Web interface.
## Running with Source

To run from source, the following command can be used to install the app's dependencies:

```shell
pip install -r requirements.txt
```  
To run after dependencies have been installed:

```shell
. start_source.sh
```

## Running with docker (recommended)

To run with docker as a container:

```shell
docker run -p 3675:5000 --rm -v /var/run/docker.sock:/var/run/docker.sock -d --name docker-web docker-web:latest 
```

localhost:3675

Naturally you can change the port from 3675 to another if you have that port assigned to another service.


This project is a fork of the drolex project from qvantel located here: https://github.com/qvantel/drolex  

## Context
I used to work for Qvantel and the forked project (link above) was developed internally and released for open source use and development. The original is a commandline docker that prints the docker run command of the stated container. The project however did not print the full command but rather printed the parts that were important internaly. I decided to intially expand this to print the full command but excluding the defaults and making it backwards compatable to previous versions of docker. Furthermore, I decided to add a UI so rather than requesting  a specific container though the commandline it automatically shows all running, stopped, paused  and removed containers as well as the docker run command. It additionally allows basic interaction with the containers such as inspect, stop, restart, pause, unpause and remove. It however does not allow running a container that was not already running.
I've changed the name from drolex to docker-web-ui is this is no longer just a run command extract tool and is and will be much more. The name change better reflect what it is now and will be its focus. Furthermore, the open source version of the original repo has not been maintained in several years and the name change allows for greater delineation.
I will continue development of this to allow full docker analysis as a docker UI and management and systems analysis tool. I would also like to add permissions (read only vs write) and depending on which permissions limit interaction with the app. Additionally I want to add a limitation on the remove option.

## Features


## Roadmap (Not in order of importance or implementation date)
- (Immediately) add logic to prevent removal of the docker-web-ui container. It will still be shown as it is part of the systems management data set. 
- adjust error handling pages 
- container CPU usage and performance metrics and graphs
- backwards compatability with older versions of docker
- re-enable commandline interface for docker run extraction
- re-add help commands which have been disabled
- add security and permissions control
- limit remove permissions and add warnings for containers that have autoremove enabled and/or do not have mounted volumes so all data would be lost.
- add secure remote docker connections
- shift to a react front end (last thing likely) 
- add tests
- add better logging

## Docs
For full documentation of Docker and the meanings of the commands you can find the docs here ->https://docs.docker.com/engine/reference/run/