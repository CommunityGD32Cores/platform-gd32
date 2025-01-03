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

import sys
from platform import system
from os import makedirs
from os.path import basename, isdir, join, isfile, realpath
import re

from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, AlwaysBuild,
                          Builder, Default, DefaultEnvironment)

from platformio.util import get_serial_ports


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621
    env.AutodetectUploadPort()

    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    if not bool(upload_options.get("disable_flushing", False)):
        env.FlushSerialBuffer("$UPLOAD_PORT")

    before_ports = get_serial_ports()

    if bool(upload_options.get("use_1200bps_touch", False)):
        env.TouchSerialPort("$UPLOAD_PORT", 1200)

    if bool(upload_options.get("wait_for_upload_port", False)):
        env.Replace(UPLOAD_PORT=env.WaitForNewSerialPort(before_ports))

def check_debugger_config_file():
    global platform
    expected_filepath = join(platform.get_package_dir("tool-openocd-gd32"), "scripts", "interface", "ftdi", "sipeed-rv-debugger.cfg")
    expected_filecontents = """adapter driver ftdi
ftdi_device_desc "JTAG Debugger"
ftdi_vid_pid 0x0403 0x6010

transport select jtag
ftdi_layout_init 0x0008 0x001b
ftdi_layout_signal nSRST -oe 0x0020 -data 0x0020
"""
    if not isfile(expected_filepath):
        print("Writing config to %s" % expected_filepath)
        with open(expected_filepath, "w") as fp:
            fp.write(expected_filecontents)

# safely evaluates a e.g. mathematical expression
# no global variables or functions allowed
def s_eval(input_string):
     code = compile(input_string, "<int>", "eval")
     if code.co_names:
         raise NameError(f"Use of names not allowed")
     return eval(code, {"__builtins__": {}}, {})

def _update_max_upload_size(env):
    # only invoked for wifi-sdk projects
    # get the generated linkerscript again
    genned_ldscript = join(env.subst("$BUILD_DIR"), "nspe_gdm32_ns_processed.ld")
    if not isfile(genned_ldscript):
        print("Warning: Failed to retrieve linker script for size update from file '%s'." % str(genned_ldscript))
        return
    ldscript = ""
    with open(genned_ldscript, 'r') as fp:
        ldscript = fp.read()
    # parse the "MEMORY" sections out of it
    # example:
    #  FLASH (rx) : ORIGIN = (0x08000000 + 0xA000 + 0), LENGTH = (0x100000 - 0xA000)
    #  RAM (xrw) : ORIGIN = ((0x20000000 + 0x200)), LENGTH = (0x00070000 - 0x200)
    flash_matches = re.findall(r"FLASH \(rx\) : ORIGIN = \(([0-9xA-Fa-f +-]+)\), LENGTH = \(([0-9xA-Fa-f +-]+)\)", ldscript)
    if flash_matches is None or len(flash_matches) != 1:
        print("Warning: Failed to retrieve flash memory details from linker script for size update from file '%s'." % str(genned_ldscript))
        print("Flash matches: %s" % str(flash_matches))
        return
    flash_origin, flash_len = flash_matches[0]
    ram_matches = re.findall(r"RAM \(xrw\) : ORIGIN = \(\(([0-9xA-Fa-f +-]+)\)\), LENGTH = \(([0-9xA-Fa-f +-]+)\)", ldscript)
    if ram_matches is None or len(ram_matches) != 1:
        print("Warning: Failed to retrieve RAM memory details from linker script for size update from file '%s'." % str(genned_ldscript))
        return
    ram_origin, ram_len = ram_matches[0]
    # due to the regexes, all extracted strings can can only be expressions involving hex numbers.
    # especially, no paranthesis are possible, so no function calls etc.
    # use a hardened of eval() anyways.
    flash_origin, flash_len, ram_origin, ram_len = s_eval(flash_origin), s_eval(flash_len), s_eval(ram_origin), s_eval(ram_len)
    print(f"Partition table: Flash at {hex(flash_origin)}, {flash_len} bytes. RAM at {hex(ram_origin)}, {ram_len} bytes.")
    board.update("upload.maximum_ram_size", ram_len)
    board.update("upload.maximum_size", flash_len)

env = DefaultEnvironment()
env.SConscript("compat.py", exports="env")
platform = env.PioPlatform()
board = env.BoardConfig()

is_riscv = board.get("build.mcu", "").startswith("gd32vw")
toolchain_triple = "arm-none-eabi" if not is_riscv else "riscv64-unknown-elf"

env.Replace(
    AR="%s-gcc-ar" % toolchain_triple,
    AS="%s-as" % toolchain_triple,
    CC="%s-gcc" % toolchain_triple,
    CXX="%s-g++" % toolchain_triple,
    GDB="%s-gdb" % toolchain_triple,
    OBJCOPY="%s-objcopy" % toolchain_triple,
    OBJDUMP="%s-objdump" % toolchain_triple,
    RANLIB="%s-gcc-ranlib" % toolchain_triple,
    SIZETOOL="%s-size" % toolchain_triple,

    ARFLAGS=["rc"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.preinit_array|\.init_array|\.fini_array|\.code_to_sram|\.vectors|\.text.align|\.ARM.exidx|\.ccram_data)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit|\.stack|\.code_to_sram|\.memory_layout)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGSUFFIX=".elf"
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        ),
        BinsToCombinedBin=Builder(
            action=env.VerboseAction(" ".join([
                '"%s"' % join(platform.get_package_dir("tool-sreccat") or "",
                    "srec_cat"),
                "${SOURCES[1]}", # master bootloader (mbl)
                "-Binary",
                "-offset",
                "0",
                "${SOURCES[0]}", # firmware.bin (nspe)
                "-Binary",
                "-offset",
                "0xa000",
                "-fill",
                "0xFF",
                "0x7FFC",
                "0xA000",
                "-o",
                "$TARGET",
                "-Binary"
            ]), "Generating $TARGET"),
        )
    )
)

pioframework = env.get("PIOFRAMEWORK", [])
if not pioframework:
    env.SConscript("frameworks/_bare.py", exports="env")

#
# Target: Build executable and linkable firmware
#

if "wifi-sdk" in pioframework:
    env.SConscript(
        join("frameworks", "wifi-sdk-pre.py"),
        exports={"env": env}
    )
if "zephyr" in pioframework:
    env.SConscript(
        join(platform.get_package_dir(
            "framework-zephyr"), "scripts", "platformio", "platformio-build-pre.py"),
        exports={"env": env}
    )

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.bin")
else:
    target_elf = env.BuildProgram()
    target_firm = env.ElfToBin(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

    if "zephyr" in pioframework and "mcuboot-image" in COMMAND_LINE_TARGETS:
        target_firm = env.MCUbootImage(
            join("$BUILD_DIR", "${PROGNAME}.mcuboot.bin"), target_firm)

    env.Depends(target_firm, "checkprogsize")

# replace target_firm variable with *combined* .bin image
# of master bootloader and firmware.
# this self-referential thing actually works.
if "wifi-sdk" in pioframework:
    target_firm = env.BinsToCombinedBin(
        join("$BUILD_DIR", "image-all.bin"),
        [
            target_firm,
            join("$BUILD_DIR", "mbl.bin")
        ]
    )
    # update max upload size based on linker file
    if env.get("PIOMAINPROG"):
        env.AddPreAction(
            "checkprogsize",
            env.VerboseAction(
                lambda source, target, env: _update_max_upload_size(env),
                "Retrieving maximum program size $SOURCES"))

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload by default .bin file
#

upload_protocol = env.subst("$UPLOAD_PROTOCOL")
debug_tools = board.get("debug.tools", {})
upload_source = target_firm
upload_actions = []

if upload_protocol == "mbed":
    upload_actions = [
        env.VerboseAction(env.AutodetectUploadPort, "Looking for upload disk..."),
        env.VerboseAction(env.UploadToDisk, "Uploading $SOURCE")
    ]

elif upload_protocol.startswith("blackmagic"):
    env.Replace(
        UPLOADER="$GDB",
        UPLOADERFLAGS=[
            "-nx",
            "--batch",
            "-ex", "target extended-remote $UPLOAD_PORT",
            "-ex", "monitor %s_scan" %
            ("jtag" if upload_protocol == "blackmagic-jtag" else "swdp"),
            "-ex", "attach 1",
            "-ex", "load",
            "-ex", "compare-sections",
            "-ex", "kill"
        ],
        UPLOADCMD="$UPLOADER $UPLOADERFLAGS $SOURCE"
    )
    upload_source = target_elf
    upload_actions = [
        env.VerboseAction(env.AutodetectUploadPort, "Looking for BlackMagic port..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
    ]

elif upload_protocol.startswith("jlink"):

    def _jlink_cmd_script(env, source):
        build_dir = env.subst("$BUILD_DIR")
        if not isdir(build_dir):
            makedirs(build_dir)
        script_path = join(build_dir, "upload.jlink")
        commands = [
            "h",
            "loadbin %s, %s" % (source, board.get(
                "upload.offset_address", "0x08000000")),
            "r",
            "q"
        ]
        with open(script_path, "w") as fp:
            fp.write("\n".join(commands))
        return script_path

    env.Replace(
        __jlink_cmd_script=_jlink_cmd_script,
        UPLOADER="JLink.exe" if system() == "Windows" else "JLinkExe",
        UPLOADERFLAGS=[
            "-device", board.get("debug", {}).get("jlink_device"),
            "-speed", env.GetProjectOption("debug_speed", "4000"),
            "-if", ("jtag" if upload_protocol == "jlink-jtag" else "swd"),
            "-autoconnect", "1",
            "-NoGui", "1"
        ],
        UPLOADCMD='$UPLOADER $UPLOADERFLAGS -CommanderScript "${__jlink_cmd_script(__env__, SOURCE)}"'
    )
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]


elif upload_protocol == "dfu":
    hwids = board.get("build.hwids", [["0x0483", "0xDF11"]])
    vid = hwids[0][0]
    pid = hwids[0][1]

    # default tool for all boards with embedded DFU bootloader over USB
    _upload_tool = '"%s"' % join(platform.get_package_dir(
        "tool-dfuutil") or "", "bin", "dfu-util")
    _upload_flags = [
        "-d", ",".join(["%s:%s" % (hwid[0], hwid[1]) for hwid in hwids]),
        "-a", "0", "-s",
        "%s:leave" % board.get("upload.offset_address", "0x08000000"), "-D"
    ]

    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

    if "arduino" in env.get("PIOFRAMEWORK"):
        if env.subst("$BOARD").startswith("portenta"):
            upload_actions.insert(
                0,
                env.VerboseAction(BeforeUpload, "Looking for upload port...")
            )
        elif board.get("build.mcu").startswith("gd32f103") or board.get("build.mcu").startswith("gd32f303"):
            # F103 and F303 series doesn't have embedded DFU over USB
            # stm32duino bootloader (v1, v2) is used instead
            def __configure_upload_port(env):
                return basename(env.subst("$UPLOAD_PORT"))

            _upload_tool = "maple_upload"
            _upload_flags = [
                "${__configure_upload_port(__env__)}",
                board.get("upload.boot_version", 2),
                "%s:%s" % (vid[2:], pid[2:])
            ]

            env.Replace(__configure_upload_port=__configure_upload_port)

            upload_actions.insert(
                0, env.VerboseAction(env.AutodetectUploadPort,
                                     "Looking for upload port..."))

    if "dfu-util" in _upload_tool:
        # Add special DFU header to the binary image
        env.AddPostAction(
            join("$BUILD_DIR", "${PROGNAME}.bin"),
            env.VerboseAction(
                " ".join([
                    '"%s"' % join(platform.get_package_dir("tool-dfuutil") or "",
                         "bin", "dfu-suffix"),
                    "-v %s" % vid,
                    "-p %s" % pid,
                    "-d 0xffff", "-a", "$TARGET"
                ]), "Adding dfu suffix to ${PROGNAME}.bin"))

    env.Replace(
        UPLOADER=_upload_tool,
        UPLOADERFLAGS=_upload_flags,
        UPLOADCMD='$UPLOADER $UPLOADERFLAGS "${SOURCE.get_abspath()}"')

    upload_source = target_firm

elif upload_protocol == "serial":
    def __configure_upload_port(env):
        return env.subst("$UPLOAD_PORT")

    env.Replace(
        __configure_upload_port=__configure_upload_port,
        UPLOADER=join(
            '"%s"' % platform.get_package_dir("tool-stm32duino") or "",
            "stm32flash", "stm32flash"),
        UPLOADERFLAGS=[
            "-g", board.get("upload.offset_address", "0x08000000"),
            "-b", "115200", "-w"
        ],
        UPLOADCMD='$UPLOADER $UPLOADERFLAGS "$SOURCE" "${__configure_upload_port(__env__)}"'
    )

    upload_actions = [
        env.VerboseAction(env.AutodetectUploadPort, "Looking for upload port..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
    ]

elif upload_protocol == "hid":
    def __configure_upload_port(env):
        return basename(env.subst("$UPLOAD_PORT"))

    env.Replace(
        __configure_upload_port=__configure_upload_port,
        UPLOADER="hid-flash",
        UPLOADCMD='$UPLOADER "$SOURCES" "${__configure_upload_port(__env__)}"'
    )
    upload_actions = [
        env.VerboseAction(env.AutodetectUploadPort, "Looking for upload port..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
    ]

elif upload_protocol == "gdlinkcli":
    def _gdlinkcli_cmd_script(env, source):
        build_dir = env.subst("$BUILD_DIR")
        if not isdir(build_dir):
            makedirs(build_dir)
        script_path = join(build_dir, "upload.gdlinkcli")
        # halt, load binary, reset, quit.
        commands = [
            "c 0", # use first GDLink device
            "h",
            "load %s %s" % (source, board.get(
                "upload.offset_address", "0x08000000")),
            "r",
            "q"
        ]
        with open(script_path, "w") as fp:
            fp.write("\n".join(commands))
        return script_path

    env.Replace(
        __gdlinkcli_cmd_script=_gdlinkcli_cmd_script,
        UPLOADER="gdlink.bat", # wrapper script that calls into GD_Link_CLI.exe and corrects error code
        UPLOADERFLAGS=[],
        UPLOADCMD='$UPLOADER $UPLOADERFLAGS -commandfile "${__gdlinkcli_cmd_script(__env__, SOURCE)}"'
    )
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

elif upload_protocol in debug_tools:

    # quick fix: add config file on-the-fly
    if upload_protocol == "sipeed-rv-debugger":
        check_debugger_config_file()

    openocd_args = [
        "-d%d" % (2 if int(ARGUMENTS.get("PIOVERBOSE", 0)) else 1)
    ]
    openocd_args.extend(
        debug_tools.get(upload_protocol).get("server").get("arguments", []))
    if env.GetProjectOption("debug_speed"):
        openocd_args.extend(
            ["-c", "adapter speed %s" % env.GetProjectOption("debug_speed")]
        )
    openocd_args.extend([
        "-c", "program {$SOURCE} %s verify reset; shutdown;" %
        board.get("upload.offset_address", "")
    ])
    openocd_args = [
        f.replace("$PACKAGE_DIR",
                  platform.get_package_dir("tool-openocd-gd32") or "")
        for f in openocd_args
    ]
    env.Replace(
        UPLOADER="openocd",
        UPLOADERFLAGS=openocd_args,
        UPLOADCMD="$UPLOADER $UPLOADERFLAGS")

    if not board.get("upload").get("offset_address"):
        upload_source = target_elf
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

# custom upload tool
elif upload_protocol == "custom":
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

else:
    sys.stderr.write("Warning! Unknown upload protocol %s\n" % upload_protocol)

AlwaysBuild(env.Alias("upload", upload_source, upload_actions))

#
# Information about obsolete method of specifying linker scripts
#

if any("-Wl,-T" in f for f in env.get("LINKFLAGS", [])):
    print("Warning! '-Wl,-T' option for specifying linker scripts is deprecated. "
          "Please use 'board_build.ldscript' option in your 'platformio.ini' file.")

#
# Default targets
#

Default([target_buildprog, target_size])
