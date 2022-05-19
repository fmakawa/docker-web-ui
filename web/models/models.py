"""
Copyright (c) 2018, Qvantel
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL QVANTEL BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

DROLEX - Docker Run OnLine EXtractor

This service reads a currently running docker and shows the command line used to run it.

"""
# System Imports
import logging
import sys
import importlib
import docker
from functools import reduce
# Self project imports
from web.errors import DrolexException
# Non default packages test to run import


class Drolex:

    def __init__(self, conn_uri='unix://var/run/docker.sock', tls_conf=False, loglevel='DEBUG', logfile=None):
        self.__setlogging(level=loglevel, logfile=logfile)
        self.__setclient(conn_uri=conn_uri, tls_conf=tls_conf)

    def __setlogging(self, level='DEBUG', logfile=None):
        self.debug = False
        if level == 'DEBUG':
            self.debug = True
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(getattr(logging, level))
        formatstyle = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        if not logfile:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatstyle)
            self.log.addHandler(ch)
            self.log.debug("Logging system setup done to STDOUT")
        else:
            # Used if need to write to a logfile
            try:
                fh = logging.FileHandler(logfile)
                fh.setFormatter(formatstyle)
                self.log.addHandler(fh)
                self.log.debug("Logging system setup done to %s", logfile)
            except Exception:
                if self.debug:
                    logging.exception("Error logging to logfile", exc_info=True)
                else:
                    logging.exception("Error logging to logfile", exc_info=False)

    '''
       Create the connection to the docker daemon API
    '''
    def __setclient(self, conn_uri='unix://var/run/docker.sock', tls_conf=False):
        try:
            self.client = docker.APIClient(
                base_url=conn_uri,
                tls=tls_conf,
                user_agent="SWAT/Drolex",
                version='auto'
            )
            self.log.debug("Connected to DockerDaemon on {0}".format(conn_uri))
            self.log.debug("Server version is: {0}".format(self.client.version()))
        except Exception as e:
            if self.debug:
                self.log.error("Unable to create DockerClient", exc_info=True)
            else:
                self.log.error("Unable to create DockerClient", exc_info=False)

            raise DrolexException("Unable to instance the DockerClient: {0}".format(e))

    '''
        Get the configuration dictionary from a specific container name or ID
        INPUT:
            str - Container ID or Name
        OUTPUT:
            {dict} - Container config dictionary
    '''
    def get_config(self, dockerID):
        # Check that dockerID is a String
        config = ""
        if not isinstance(dockerID, str):
            self.log.error("DockerID provided is not a valid String")
            raise DrolexException("DockerID must be a valid String: {0}".format(dockerID))
        try:
            config = self.client.inspect_container(dockerID)
            image_config = self.client.inspect_image(config["Image"])
            config["Config"].update({
                "ImageEnv": image_config["Config"]["Env"],
                "ImageUser": image_config["Config"]["User"],
                "ImagePorts": image_config["Config"].get("ExposedPorts", [])
            })
            image_cmd = (image_config["Config"]["Entrypoint"] or []) + (image_config["Config"]["Cmd"] or [])
            config["Args"] = {"ImageCmd": image_cmd, "Cmd": config["Args"]}
            config["NetworkSettings"].update({"NetworkMode": config["HostConfig"]["NetworkMode"]})
            if self.debug:
                import pprint
                pprinter = pprint.PrettyPrinter(indent=4)
                pprinter.pprint(config)

        except docker.errors.NotFound:
            self.log.error("Unable to find DockerID: {0}".format(dockerID))
        except docker.errors.APIError as error:
            self.log.error("Error in Docker API call.")
            if self.debug:
                self.log.debug("DOCKER API TRACEBACK: {0}".format(error))
        except docker.errors.InvalidVersion as versioning:
            self.log.error("Missmatch in Docker API client->Server version")
            if self.debug:
                self.log.debug("DOCKER API TRACEBACK: {0}".format(versioning))
        return config

    '''
      Generate a docker run command following a template. It will use the given order then add any
      remaining elements to the end.
      INPUT:
        {dict} - Docker command parts
        list - Order in which the parts of the command should be arranged
      OUTPUT:
        str - Docker run command
    '''
    def to_docker_run(self, parts, order):
        rest = reduce(lambda acc, key: acc + (parts[key] if key not in order and
                      key != "ExtraNetworks" else ""), parts, "")
        command = "docker run " + reduce(lambda acc, key: acc + parts[key], order, "") + rest
        return command

    '''
      Generate a docker network connect command.
      INPUT:
        list - List of networks to create docker network connect commands for
        str - Name of the container to connect
      OUTPUT:
        str - Docker network connect command
    '''
    def to_docker_network_connect(self, networks, container):
        result = reduce(lambda acc, item: acc + "; docker network connect " + item["Options"]
                        + " " + item["Name"] + " " + container + " ", networks, "")
        result = result + "; docker restart " + container + " "
        return result

    '''
      Dynamically get the content of a docker config output and look in the utils available to
      proccess every key to generate the desired command line
      If no util/KEY is available write in debug but not in error a message
      INPUT:
        {dict} -  An output object from docker.APIClient.inspect_container call
      OUTPUT:
        {dict} - A join of all the available dinamic objects for the input dict
    '''
    def rerun(self, configdata, order):
        out_cmd = {}
        for key in configdata:
            # self.log.debug("Available Key in config: {0}".format(key))
            try:
                module_name = "web.utils." + key
                dynmod = importlib.import_module(module_name)
                self.log.debug("Module {0} imported".format(key))
                dynclass = getattr(dynmod, key)
                self.log.debug("Class loaded")
                processor = dynclass(configdata[key])
                self.log.debug("Running processor for config key: {0}".format(key))
                out_cmd.update(processor.run())
            except ImportError:
                self.log.debug("No processor found for config key: {0}".format(key))
            except Exception as e:
                self.log.exception(e)
        # print(self.to_docker_run(out_cmd, order.split(",")))
        if out_cmd["ExtraNetworks"]:
            # print(self.to_docker_network_connect(out_cmd["ExtraNetworks"],
                                                 # configdata["Name"].replace("/", "")))
            return(self.to_docker_network_connect(out_cmd["ExtraNetworks"],
                                                  configdata["Name"].replace("/", "")))
        else:
            return(
                self.to_docker_run(out_cmd,
                                   order.split(",")
                                   )
            )


"""
# Self test use
if __name__ == '__main__':
    # from drolex import Drolex
    import argparse

    # Prepare the argparse
    parser = argparse.ArgumentParser(description='DROLEX - Docker Run OnLine EXtractor')
    parser.add_argument('--conn_uri',
                        help=f'Address and port of docker server Ex: --conn_uri '
                             f'"tcp://127.0.0.1:1234" (Default: %(default)s)',
                        default='unix://var/run/docker.sock')
    # parser.add_argument('--tls_cert', help='Client TLS cert to connect to server',
    #                    required=False)
    parser.add_argument('--loglevel', help='LogLevel of the web. (Default: %(default)s)',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO')
    parser.add_argument('--ID', help="Container ID to check", required=True)
    parser.add_argument('--order',
                        help=f'Order in which to print the different parts of '
                             f'the docker run command (Default: %(default)s)',
                        default='Mode,HostConfig,User,NetworkSettings,Exposed,Ports,Mounts,Volumes,Env,Name,Image,Args')

    # Run the code
    try:
        # Process the arguments
        args = vars(parser.parse_args())

    # Some error occurred
    except Exception:
        sys.exit(1)

    drolex = Drolex(conn_uri=args['conn_uri'],
                    loglevel=args['loglevel'])
    # Run the update method
    drolex.rerun(drolex.get_config(dockerID=args['ID']), args['order'])
"""