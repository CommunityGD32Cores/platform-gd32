# Copyright 2021-present CommunityCoresGD32 <maximlian.gerhardt@rub.de>
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

"""
WiFi SDK

The GigaDevice supplied WiFi SDK enables the development of WiFi-enabled
firmwares for GD32W51x series microcontrollers.
"""

from os.path import isdir, isfile, join, dirname, realpath
from string import Template

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.SConscript("_bare.py")

# same semihosting logic as with SPL
activate_semihosting = board.get("debug.semihosting", False)
activate_semihosting = str(activate_semihosting).lower() in ("1", "yes", "true")
if activate_semihosting:
    env.Append(LINKFLAGS=["--specs=rdimon.specs", "--specs=nano.specs"])
    env.Append(LIBS=["rdimon"])
else:
    env.Append(LINKFLAGS=["--specs=nosys.specs", "--specs=nano.specs"])

FRAMEWORK_DIR = platform.get_package_dir("framework-wifi-sdk-gd32")
assert isdir(FRAMEWORK_DIR)

if not board.get("build.mcu").startswith("gd32w51"):
    print("Error! Only GD32W51x chips are supported by this framework")
    env.Exit(-1)

print("Not implemented yet!!")
env.Exit(-1)