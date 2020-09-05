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

    Plugin for extracting the command for the Config section
"""
from functools import reduce


class Config:

    def __init__(self, config):
        self.config = config

    def run(self):
        env = ""
        mode = ""
        exposed = ""
        user = ""
        volumes = ""

        run_vars = filter(lambda item: item not in self.config["ImageEnv"], self.config["Env"])
        env = env + reduce(lambda acc, x: acc + "-e \"" + x + "\" ", run_vars, "")

        if self.config["Tty"]:
            mode = "-t " if not self.config["OpenStdin"] else "-it "
        elif self.config["OpenStdin"]:
            mode = mode + "-i "

        if self.config["User"] and self.config["User"] != self.config["ImageUser"]:
            user = f'--user="{self.config["User"]}" '

        if not self.config["AttachStdout"] and not self.config["AttachStderr"]:
            mode = mode + "-d "

        if self.config["Volumes"]:
            for volume in self.config["Volumes"]:
                volumes = volumes + f'-v {volume} '

        if "ExposedPorts" in self.config:
            run_exposed = filter(lambda item: item not in self.config["ImagePorts"], self.config["ExposedPorts"])
            exposed = exposed + reduce(lambda acc, x: f'{acc}--expose={x} ', run_exposed, "")

        return {
            "Env": env,
            "Mode": mode,
            "Exposed": exposed,
            "User": user,
            "Volumes": volumes,
            "Image": self.config["Image"] + " "
        }
