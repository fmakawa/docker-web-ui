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

  Plugin for extracting the command for the HostConfig section
"""
from functools import reduce
from decimal import Decimal


class HostConfig:
    def __init__(self, config):
        self.config = config

    def run(self):
        cmd_out = ""
        if self.config["AutoRemove"]:
            cmd_out = cmd_out + "--rm "

        if self.config["Privileged"]:
            cmd_out = cmd_out + "--privileged "

        if self.config["CapAdd"]:
            cmd_out = cmd_out + reduce(lambda acc, item: acc + "--cap-add=" + item + " ", self.config["CapAdd"], "")

        if self.config["CapDrop"]:
            cmd_out = cmd_out + reduce(lambda acc, item: acc + "--cap-drop=" + item + " ", self.config["CapDrop"], "")

        if self.config["RestartPolicy"]["Name"] != "no":
            cmd_out = cmd_out + "--restart=" + self.config["RestartPolicy"]["Name"]
            if self.config["RestartPolicy"]["MaximumRetryCount"] != 0:
                cmd_out = cmd_out + ":" + str(self.config["RestartPolicy"]["MaximumRetryCount"])
            cmd_out = cmd_out + " "

        cmd_out = f"{cmd_out}--log-driver {self.config['LogConfig']['Type']}  " \
                  + reduce(
                    lambda acc, key:
                    f"{acc}--log-opt {key}={self.config['LogConfig']['Config'][key]} ",
                    self.config["LogConfig"]["Config"],
                    ""
                    )

        if self.config["Dns"]:
            cmd_out = cmd_out + "--dns " + ",".join(self.config["Dns"]) + " "

        if self.config["ExtraHosts"]:
            cmd_out = cmd_out + reduce(
                lambda acc, item:
                f'{acc}--add-host "{item}" ',
                self.config["ExtraHosts"],
                ""
            )

        cmd_out = cmd_out + extract_memory_params(self.config)
        cmd_out = cmd_out + extract_cpu_params(self.config)
        cmd_out = cmd_out + extract_blkio_devices(self.config)
        cmd_out = cmd_out + extract_ulimits(self.config)
        cmd_out = cmd_out + extract_user_groups(self.config)
        ports = str(extract_port_bindings(self.config))
        return {"HostConfig": str(cmd_out), "Ports": str(ports)}


def to_human_readable(bytez):
    if bytez >= (1 * 1024**3):
        return str(Decimal(bytez/1024**3)) + "g"
    else:
        return str(Decimal(bytez/1024**2)) + "m"


def extract_memory_params(config):
    response = ""
    if config["Memory"] != 0:
        response = f"{response}-m {to_human_readable(config['Memory'])} "
    if config["MemoryReservation"] != 0:
        response = f"{response}--memory-reservation {to_human_readable(config['MemoryReservation'])} "
    if config["MemorySwap"] != config["Memory"]:
        response = f"{response}--memory-swap {to_human_readable(config['MemorySwap'])} "
    if config["MemorySwappiness"] is not None and config["MemorySwappiness"] != -1:
        response = f"{response}--memory-swappiness={str(config['MemorySwappiness'])} "
    return response


def extract_blkio_devices(config):
    response = ""
    if config["BlkioWeightDevice"]:
        response = f"{response}--blkio-weight-device={config['BlkioWeightDevice']} "
    return response


def extract_cpu_params(config):
    response = ""
    if config["CpuShares"] != 0:
        response = response + "--cpu-shares=" + str(config["CpuShares"]) + " "
    return response


def extract_user_groups(config):
    response = ""
    if config["GroupAdd"]:
        for x in config["GroupAdd"]:
            response = f'{response}--group-add="{x}" '
    return response


def extract_ulimits(config):
    response = ""
    if config["Ulimits"]:
        for ulimits in config["Ulimits"]:
            response = f'{response}--ulimit {ulimits["Name"]}={ulimits["Soft"]}:{ulimits["Hard"]} '
    return response


def port_binding_to_string(port, binding):
    response = "-p "
    if binding[0]["HostIp"] != "":
        response = response + binding[0]["HostIp"] + ":"
    if binding[0]["HostPort"] != "":
        response = response + binding[0]["HostPort"] + ":"
    elif binding[0]["HostIp"] != "":
        response = response + ":"
    response = response + port.replace("/tcp", "")
    return response


def extract_port_bindings(config):
    response = ""
    if config["PublishAllPorts"]:
        response = response + "-P "
    if config["PortBindings"]:
        response = response + reduce(
            lambda acc, key: f"{acc}{port_binding_to_string(key, config['PortBindings'][key])} ",
            config["PortBindings"],
            ""
        )
    return response
