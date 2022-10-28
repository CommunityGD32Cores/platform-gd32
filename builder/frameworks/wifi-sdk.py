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

from os.path import isdir, isfile, join, dirname, realpath, splitext
from os import walk
from string import Template

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
PROJECT_SRC_DIR = env.subst("$PROJECT_SRC_DIR")

# same semihosting logic as with SPL
activate_semihosting = board.get("debug.semihosting", False)
activate_semihosting = str(activate_semihosting).lower() in ("1", "yes", "true")
if activate_semihosting:
    env.Append(LINKFLAGS=["--specs=rdimon.specs", "--specs=nano.specs"])
    env.Append(LIBS=["rdimon"])
else:
    env.Append(LINKFLAGS=["--specs=nano.specs"])

FRAMEWORK_DIR = platform.get_package_dir("framework-wifi-sdk-gd32")
assert isdir(FRAMEWORK_DIR)

if not board.get("build.mcu").startswith("gd32w51"):
    print("Error! Only GD32W51x chips are supported by this framework")
    env.Exit(-1)

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],
    CFLAGS=["-std=c99"],
    CXXFLAGS=[
        "-std=gnu++14",
        "-fno-threadsafe-statics",
        "-fno-rtti",
        "-fno-exceptions",
        "-fno-use-cxa-atexit",
    ],
    CCFLAGS=[
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mcpu=cortex-m33",
        "-mthumb",
        "-mfpu=fpv5-sp-d16",
        "-mfloat-abi=hard",
        "-Wall",
        "-Wno-format",
        "-Wno-return-type",
        "-Wno-unused-but-set-variable",
        "-Wno-address-of-packed-member",
        "-Wno-unused-variable",
        "-Wno-maybe-uninitialized",
        "-Wno-unused-function",
        "-fno-builtin",
        "-fno-short-enums",
        "-funsigned-char",
        "-nostdlib",
        "--param",
        "max-inline-insns-single=500",
    ],
    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        ("BOARD_NAME", '\\"%s\\"' % env.subst("$BOARD").upper()),
        env.subst("$BOARD").upper(),
        "PLATFORM_GDM32",
        "PLATFORM_OS_FREERTOS", # hardcode to FreeRTOS for now
    ],
    CPPPATH=[
        join(FRAMEWORK_DIR, "config"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "CMSIS", "ARM", "cmsis"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "CMSIS", "GD", "GD32W51x", "Include"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "CMSIS", "DSP_Lib_v1.6.0", "include"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "app"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "bsp"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "common"),
        join(FRAMEWORK_DIR, "MBL", "platform"),
        join(FRAMEWORK_DIR, "ROM-EXPORT", "platform"),
        join(FRAMEWORK_DIR, "ROM-EXPORT", "source"),
        join(FRAMEWORK_DIR, "ROM-EXPORT", "mbedtls-2.17.0-rom", "include"),
        # for now, only support CONFIG_TZ_ENABLED = 0.
        join(FRAMEWORK_DIR, "MBL", "source_ns"),
    ],
    LINKFLAGS=[
        #"-Os",
        "-mcpu=cortex-m33",
        "-mthumb",
        "-mfpu=fpv5-sp-d16",
        "-mfloat-abi=hard",
        "-u", "_printf_float",
        "-Wl,-fatal-warnings",
        "-Wl,--no-wchar-size-warning",
        "-Wl,-no-enum-size-warning",
        #"-Wl,--cref",
        "-Wl,--just-symbols=%s" % join(FRAMEWORK_DIR, "ROM-EXPORT", "symbol", "rom_symbol.gcc"),
        "-Wl,--gc-sections",
        "-Wl,--check-sections",
        "-Wl,--entry=Reset_Handler",
        "-Wl,--unresolved-symbols=report-all",
    ],
    LIBS=["c", "gcc", "m", "stdc++"]
)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

def get_objects_for_path(target_env, source_path:str, target_prefix:str, only_allow:list = None):
    objs = []
    for (dirpath, dirnames, filenames) in walk(source_path):
        for f in filenames:
            allowed = True if only_allow is None else f in only_allow
            _, ext = splitext(f)
            if ext in [".c", ".S", ".s"] and allowed:
                objs.append(
                    target_env.StaticObject(
                        target=join(target_prefix, f.replace(ext, ".o")),
                        source=realpath(join(source_path, f))
                    )
                )
    return objs

saved_mbl_env = None

def compile_bootloader_sources(default_env):
    is_build_type_debug = "debug" in default_env.GetBuildType()
    mbl_env = default_env.Clone()
    mbl_env.Append(ASFLAGS=mbl_env.get("CCFLAGS", [])[:])
    mbl_env.ProcessUnFlags(default_env.get("BUILD_UNFLAGS"))
    if is_build_type_debug:
        mbl_env.ConfigureDebugFlags()
    mbl_env.Append(CPPPATH=[
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_standard_peripheral", "Include")
    ])
    action = [
        '"$CC"',
        "-E",
        "-P", "-xc"
    ]
    for x in mbl_env["CPPPATH"]:
        action.extend(["-I", '"%s"' % x])
    action.extend(mbl_env["CCFLAGS"])
    action.extend(["-DPLATFORM_GDM32"])
    action.extend(["-o", "$TARGET", "$SOURCE"])

    linkerscript_cmd = mbl_env.Command(
        join("$BUILD_DIR", "mbl_gdm32_ns_processed.ld"),  # $TARGET
        join(FRAMEWORK_DIR, "MBL", "platform" ,"gdm32", "gcc", "mbl_gdm32_ns.ld"),  # $SOURCE
        mbl_env.VerboseAction(" ".join(action), 
        "Generating linkerscript $BUILD_DIR/mbl_gdm32_ns_processed.ld")
    )
    mbl_env.Depends("$BUILD_DIR/${PROGNAME}.elf", linkerscript_cmd)
    #mbl_env.Append()
    mbl_build_dir = join("$BUILD_DIR", "mbl")
    objs = get_objects_for_path(mbl_env, join(FRAMEWORK_DIR, "MBL", "source_ns"), mbl_build_dir)
    objs += get_objects_for_path(
        mbl_env, 
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_standard_peripheral", "Source"),
        mbl_build_dir,
        [
            "gd32w51x_fmc.c",
            "gd32w51x_fwdgt.c",
            "gd32w51x_gpio.c",
            "gd32w51x_icache.c",
            "gd32w51x_misc.c",
            "gd32w51x_qspi.c",
            "gd32w51x_rcu.c",
            "gd32w51x_usart.c",
        ]
    )
    objs += get_objects_for_path(
        mbl_env, 
        join(FRAMEWORK_DIR, "MBL", "platform", "gdm32", "cmsis_core"),
        mbl_build_dir,
        [
            "mbl_system_gdm32.c"
        ]
    )
    objs += get_objects_for_path(
        mbl_env, 
        join(FRAMEWORK_DIR, "MBL", "platform", "gdm32", "gcc"),
        mbl_build_dir,
        [
            "mbl_startup_gdm32.S"
        ]
    )
    saved_mbl_env = mbl_env
    return objs

env.Append(
    PIOBUILDFILES=[
        compile_bootloader_sources(env), # all build files for mbl.elf
        # firmware files etc will be added by BuildProgram()
    ]
)

# for further building the main program
env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_standard_peripheral", "Include"), 
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2", "port","arch"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2", "src", "include"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2", "src", "include", "lwip"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2", "port"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2", "apps"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "mbedtls-2.17.0-ssl", "include"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "mbedtls-2.17.0-ssl", "ns_interface"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_wifi_driver", "cmn"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_wifi_driver", "inc"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_wifi_driver", "osal"),
        join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_wifi_driver", "soc"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os", "FreeRTOSv10.3.1", "Source", "include"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os", "FreeRTOSv10.3.1", "Source", "portable" ,"GCC", "ARM_CM33_NTZ", "non_secure"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os", "FreeRTOSv10.3.1", "CMSIS", "RTOS2", "FreeRTOS", "Include"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os", "FreeRTOSv10.3.1", "CMSIS", "RTOS2", "FreeRTOS", "Source"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os"),
        join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "wifi"),
    ],
    LIBPATH=[join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "lib", "GCC")],
    LIBS=["gd32w51x_wifi"]
)

envC = env.Clone()
libs = []
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "gd32w51x_peripheral"),
    join(FRAMEWORK_DIR, "NSPE", "Firmware", "GD32W51x_standard_peripheral")
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "bsp"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "bsp"),
    src_filter=["+<*>", "-<bsp_gd32w51x.c>"]
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "common"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "common"),
    src_filter=["+<*>", "-<wrapper_os.c>"] # include in os later
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "lwIP"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "lwip-2.1.2"),
    src_filter=[
        "+<*>",
        "-<test/*>",
        "-<apps/*>",
        "+<apps/ping/ping.c>",
        "-<src/core/ipv6/*>",
        "-<src/netif/*>",
        "+<src/netif/ethernet.c>",
    ]
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "mbedtls_ssl"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "network", "mbedtls-2.17.0-ssl")
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "wifi"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "wifi")
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "os"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "common"),
    # only build this single file
    src_filter=[
        "+<wrapper_os.c>"
    ]
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "freertos"),
    join(FRAMEWORK_DIR, "NSPE", "WIFI_IOT", "os", "FreeRTOSv10.3.1"),
    src_filter=[
        "+<CMSIS/RTOS2/FreeRTOS/Source/*>",
        "-<CMSIS/RTOS2/FreeRTOS/Source/cmsis_os1.c>",
        "-<CMSIS/RTOS2/FreeRTOS/Source/handlers.c>",
        "+<Source/*>",
        "-<Source/portable/*>",
        "+<Source/portable/Common/tickless_sleep.c>",
        "+<Source/portable/GCC/ARM_CM33_NTZ/non_secure/*>",
    ]
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "cmsis"),
    join(FRAMEWORK_DIR, "NSPE", "Firmware", "CMSIS"),
    src_filter=[
        "+<*>",
        "-<GD/GD32W51x/Source/ARM/*>"
        "-<GD/GD32W51x/Source/IAR/*>"
    ]
))
libs.append(envC.BuildLibrary(
    join("$BUILD_DIR", "cmsis"),
    join(FRAMEWORK_DIR, "NSPE", "Firmware", "CMSIS"),
    src_filter=[
        "+<*>",
        "-<GD/GD32W51x/Source/ARM/*>"
        "-<GD/GD32W51x/Source/IAR/*>"
    ]
))
action = [
    '"$CC"',
    "-E",
    "-P", "-xc"
]
for x in envC["CPPPATH"]:
    action.extend(["-I", '"%s"' % x])
action.extend(envC["CCFLAGS"])
action.extend(["-DPLATFORM_GDM32"])
action.extend(["-o", "$TARGET", "$SOURCE"])

linkerscript_cmd = envC.Command(
    join("$BUILD_DIR", "nspe_gdm32_ns_processed.ld"),  # $TARGET
    join(FRAMEWORK_DIR, "NSPE", "Project", "WIFI_IOT", "GCC", "nspe_gdm32_ns.ld"),  # $SOURCE
    envC.VerboseAction(" ".join(action), 
    "Generating linkerscript $BUILD_DIR/nspe_gdm32_ns_processed.ld")
)
envC.Depends("$BUILD_DIR/${PROGNAME}.elf", linkerscript_cmd)

env.Append(LIBS=libs)
