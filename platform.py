# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import os

from platform import system

from platformio.managers.platform import PlatformBase
from platformio.util import get_systype

class Gd32Platform(PlatformBase):
    # provides fixes for GD32E50x. Mac packages are still t.b.d.
    openocd_gd32 = {
        "windows_amd64": "https://github.com/CommunityGD32Cores/tool-openocd-gd32.git#windows_x64",
        "linux_x86_64": "https://github.com/CommunityGD32Cores/tool-openocd-gd32.git#linux_x64",
    }

    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        board_config = self.board_config(board)
        build_core = variables.get(
            "board_build.core", board_config.get("build.core", "arduino"))
        build_mcu = variables.get("board_build.mcu", board_config.get("build.mcu", ""))

        sys_type = get_systype()
        openocd_pkg = "tool-openocd-gd32"
        # upgrade OpenOCD version if we have a package for it
        if openocd_pkg in self.packages and sys_type in Gd32Platform.openocd_gd32:
            self.packages[openocd_pkg]["version"] = Gd32Platform.openocd_gd32[sys_type]

        frameworks = variables.get("pioframework", [])
        if "arduino" in frameworks:
                self.packages["toolchain-gccarmnoneeabi"]["version"] = "~1.90201.0"
                if build_core == "gd32":
                    self.packages["framework-arduinogd32"]["optional"] = False
        if "mbed" in frameworks:
            deprecated_boards_file = os.path.join(
                self.get_dir(), "misc", "mbed_deprecated_boards.json")
            if os.path.isfile(deprecated_boards_file):
                with open(deprecated_boards_file) as fp:
                    if board in json.load(fp):
                        self.packages["framework-mbed"]["version"] = "~6.51506.0"
            self.packages["toolchain-gccarmnoneeabi"]["version"] = "~1.90201.0"
        if "wifi-sdk" in frameworks:
            self.packages["tool-sreccat"]["optional"] = False

        # include or exclude other packages for different frameworks.. 

        default_protocol = board_config.get("upload.protocol") or ""
        if variables.get("upload_protocol", default_protocol) == "dfu":
            self.packages["tool-dfuutil"]["optional"] = False
        if variables.get("upload_protocol", default_protocol) == "gdlinkcli":
            self.packages["tool-gdlinkcli"]["optional"] = False

        # configure J-LINK tool
        jlink_conds = [
            "jlink" in variables.get(option, "")
            for option in ("upload_protocol", "debug_tool")
        ]
        if board:
            jlink_conds.extend([
                "jlink" in board_config.get(key, "")
                for key in ("debug.default_tools", "upload.protocol")
            ])
        jlink_pkgname = "tool-jlink"
        if not any(jlink_conds) and jlink_pkgname in self.packages:
            del self.packages[jlink_pkgname]

        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get(
            "protocols", [])
        if "tools" not in debug:
            debug["tools"] = {}

        ftdi_based_links = ["sipeed-rv-debugger"]

        # BlackMagic, J-Link, ST-Link, Sipeed RV Debugger
        for link in ("blackmagic", "jlink", "stlink", "cmsis-dap", "sipeed-rv-debugger"):
            if link not in upload_protocols or link in debug["tools"]:
                continue
            if link == "blackmagic":
                debug["tools"]["blackmagic"] = {
                    "hwids": [["0x1d50", "0x6018"]],
                    "require_debug_port": True
                }
            elif link == "jlink":
                assert debug.get("jlink_device"), (
                    "Missed J-Link Device ID for %s" % board.id)
                debug["tools"][link] = {
                    "server": {
                        "package": "tool-jlink",
                        "arguments": [
                            "-singlerun",
                            "-if", "SWD",
                            "-select", "USB",
                            "-device", debug.get("jlink_device"),
                            "-port", "2331"
                        ],
                        "executable": ("JLinkGDBServerCL.exe"
                                       if system() == "Windows" else
                                       "JLinkGDBServer")
                    }
                }
            else:
                server_args = ["-s", "$PACKAGE_DIR/scripts"]
                if debug.get("openocd_board"):
                    server_args.extend([
                        "-f", "board/%s.cfg" % debug.get("openocd_board")
                    ])
                else:
                    assert debug.get("openocd_target"), (
                        "Missed target configuration for %s" % board.id)
                    if link in ftdi_based_links:
                        server_args.extend([
                            "-f", "interface/ftdi/%s.cfg" % link,
                            # JTAG protocol already pre-selected in .cfg file
                            # ..probably allow overriding to SWD based link too?
                        ])
                    else:
                        server_args.extend([
                            "-f", "interface/%s.cfg" % link,
                            "-c", "transport select %s" % (
                                "hla_swd" if link == "stlink" else "swd"),
                        ])
                    # for GD32 chips we need to be able to insert a -c "set CPUTAPID .." command
                    # *before* the target cfg is loaded.                    
                    server_args.extend(debug.get("openocd_extra_pre_target_args", []))
                    server_args.extend([
                        "-f", "target/%s.cfg" % debug.get("openocd_target")
                    ])
                    if str(debug.get("rtos", "no")) in ("true", "yes", "1"):
                        server_args.extend([
                            "-c", "$_TARGETNAME configure -rtos FreeRTOS"
                        ])
                    server_args.extend(debug.get("openocd_extra_args", []))

                debug["tools"][link] = {
                    "server": {
                        "package": "tool-openocd-gd32",
                        "executable": "bin/openocd",
                        "arguments": server_args
                    }
                }
            debug["tools"][link]["onboard"] = link in debug.get("onboard_tools", [])
            debug["tools"][link]["default"] = link in debug.get("default_tools", [])

        board.manifest["debug"] = debug
        return board

    def configure_debug_session(self, debug_config):
        server_executable = (debug_config.server or {}).get("executable", "")
        if debug_config.speed:
            if "openocd" in server_executable:
                 debug_config.server["arguments"].extend(
                    ["-c", "adapter speed %s" % debug_config.speed]
                )
            elif "jlink" in server_executable:
                debug_config.server["arguments"].extend(
                    ["-speed", debug_config.speed]
                )
