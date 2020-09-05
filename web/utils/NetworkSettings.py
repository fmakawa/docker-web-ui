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

  Plugin for extracting the command for the NetworkSettings section
"""


class NetworkSettings:
    def __init__(self, config):
        self.config = config

    def run(self):
        if not self.config["Networks"]:
            return {"NetworkSettings": "--net=\"" + self.config["NetworkMode"] + "\" ", "ExtraNetworks": []}
        main, *rest = list(map(lambda key: {
            "Name": key,
            "Options": extract_network_options(key, self.config["Networks"][key])
        }, self.config["Networks"]))
        return {"NetworkSettings": "--net=\"" + main["Name"] + "\" " + main["Options"], "ExtraNetworks": rest}


def extract_network_options(name, values):
    response = ""
    if values["IPAMConfig"]:
        response = response + "--ip=" + values["IPAddress"] + " "
    return response
