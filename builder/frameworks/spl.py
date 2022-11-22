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

"""
SPL

The ST Standard Peripheral Library provides a set of functions for
handling the peripherals on the GD32 ARM chip family.
The idea is to save the user (the new user, in particular) having to deal
directly with the registers.
"""

from os.path import isdir, isfile, join, dirname, realpath
from string import Template

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

env.SConscript("_bare.py")

def get_flag_value(flag_name:str, default_val:bool):
    flag_val = board.get("build.%s" % flag_name, default_val)
    flag_val = str(flag_val).lower() in ("1", "yes", "true")
    return flag_val

# by default, add newlibnano into linker flags.
# otherwise many standard C functions won't be accessible without using a own syscall
# implementation.
# but we also check if need to add semhosting here
activate_semihosting = board.get("debug.semihosting", False)
activate_semihosting = str(activate_semihosting).lower() in ("1", "yes", "true")
if activate_semihosting:
    env.Append(LINKFLAGS=["--specs=rdimon.specs", "--specs=nano.specs"])
    env.Append(LIBS=["rdimon"])
else:
    env.Append(LINKFLAGS=["--specs=nosys.specs", "--specs=nano.specs"])

# make it easure to enable LTO
if get_flag_value("use_lto", False):
    env.Append(LINKFLAGS=["-flto"])

FRAMEWORK_DIR = platform.get_package_dir("framework-spl-gd32")
assert isdir(FRAMEWORK_DIR)

# hardcoded -- only gd32 chips 
spl_chip_type = "gd32"
if not board.get("build.mcu").startswith("gd32"):
    print("Error! This is a non GD32 chip in the GD32 repository. Don't know which SPL implementation to use.")
    env.Exit(-1)

# the SPL series key in the JSON is mixed case to match the vendor convention, 
# but our directory names are lowercase. 
spl_series = board.get("build.spl_series").lower()

def process_standard_library_configuration(cpp_defines):
    if "PIO_FRAMEWORK_SPL_STANDARD_LIB" in cpp_defines or get_flag_value("spl_std_lib", False):
        env["LINKFLAGS"].remove("--specs=nano.specs")
    if "PIO_FRAMEWORK_SPL_NANOLIB_FLOAT_PRINTF" in cpp_defines or get_flag_value("spl_printf_float", False):
        env.Append(LINKFLAGS=["-u_printf_float"])
    if "PIO_FRAMEWORK_SPL_NANOLIB_FLOAT_SCANF" in cpp_defines or get_flag_value("spl_scanf_float", False):
        env.Append(LINKFLAGS=["-u_scanf_float"])

def get_linker_script(mcu):
    # naming convention is to take the MCU name but without the package name
    # e.g., GD32F103RC (without "T6" at the end)
    ldscript = join(FRAMEWORK_DIR, "platformio",
                    "ldscripts", mcu[:-2].upper() + "_FLASH.ld")

    if isfile(ldscript):
        return ldscript

    default_ldscript = join(FRAMEWORK_DIR, "platformio",
                            "ldscripts", mcu[:-2].upper() + "_DEFAULT.ld")

    ram = board.get("upload.maximum_ram_size", 0)
    ccram = board.get("upload.closely_coupled_ram_size", 0)
    flash = board.get("upload.maximum_size", 0)
    flash_start = int(board.get("upload.offset_address", "0x8000000"), 0)
    template_file = join(FRAMEWORK_DIR, "platformio",
                         "ldscripts", "tpl", "linker.tpl")
    content = ""
    with open(template_file) as fp:
        data = Template(fp.read())
        content = data.substitute(
            stack=hex(0x20000000 + ram), # 0x20000000 - start address for RAM
            ram=str(int(ram/1024)) + "K",
            ccram=str(int(ccram/1024)) + "K", # Closely coupled RAM - not all parts have this
            flash=str(int(flash/1024)) + "K",
            flash_start=hex(flash_start)
        )

    with open(default_ldscript, "w") as fp:
        fp.write(content)

    return default_ldscript

def get_startup_filename(board):
    # try to figure out which built-in startup file to use.
    startup_file = None
    # series and SPL series are always present.
    series = board.get("build.series", "")
    spl_series = board.get("build.spl_series", "")
    if series == "":
        print("Error: build.series was not defined in the board manifest.")
        env.Exit(-1)
    if spl_series == "":
        print("Error: build.spl_series was not defined in the board manifest.")
        env.Exit(-1)
    # some have a SPL subseries.
    spl_sub_series = board.get("build.spl_sub_series", "")
    # handle special cases
    if series in ("GD32F425", "GD32F405"):
        return "startup_gd32f405_425.S" 
    if series in ("GD32F427", "GD32F407"):
        return "startup_gd32f407_427.S" 
    if series in ("GD32F450", "GD32F470"):
        return "startup_gd32f450_470.S" 
    if series == "GD32E508":
        return "startup_gd32e508.S"
    if spl_sub_series != "":
        # all boards which have a sub-series follow a common patter 
        startup_file = f"startup_{spl_series.lower()}_{spl_sub_series.lower()}.S" 
    else:
        # all others are either jsut the SPL series or the original series name
        startup_file = f"startup_{series.lower()}.S" 
        if not isfile(join(FRAMEWORK_DIR, "gd32", "cmsis", "startup_files", startup_file)):
            startup_file = f"startup_{spl_series.lower()}.S" 
    return startup_file

env.Append(
    CPPPATH=[
        join(FRAMEWORK_DIR, spl_chip_type,
             "cmsis", "cores", spl_chip_type),
        join(FRAMEWORK_DIR, spl_chip_type,
             "cmsis", "startup_files"),
        join(FRAMEWORK_DIR, spl_chip_type, "cmsis",
             "variants", spl_series),
        join(FRAMEWORK_DIR, spl_chip_type, "spl",
             "variants", spl_series, "inc"),
        join(FRAMEWORK_DIR, spl_chip_type, "spl",
             "variants", spl_series, "src")
    ]
)

env.Append(
    CPPDEFINES=[
        "USE_STDPERIPH_DRIVER"
    ]
)

if not board.get("build.ldscript", ""):
    env.Replace(
        LDSCRIPT_PATH=get_linker_script(board.get("build.mcu")))

# Configure standard library
cpp_defines = env.Flatten(env.get("CPPDEFINES", []))
process_standard_library_configuration(cpp_defines)
#
# Target: Build SPL Library
#

extra_flags = board.get("build.extra_flags", "")
src_filter_patterns = ["+<*>"]
# could come in handy later to exclude certain files, not needed / trigger now
if "STM32F40_41xxx" in extra_flags:
    src_filter_patterns += ["-<stm32f4xx_fmc.c>"]
if "STM32F427_437xx" in extra_flags:
    src_filter_patterns += ["-<stm32f4xx_fsmc.c>"]
elif "STM32F303xC" in extra_flags:
    src_filter_patterns += ["-<stm32f30x_hrtim.c>"]
elif "STM32L1XX_MD" in extra_flags:
    src_filter_patterns += ["-<stm32l1xx_flash_ramfunc.c>"]

libs = []

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkCMSISVariant"),
    join(
        FRAMEWORK_DIR, spl_chip_type, "cmsis",
        "variants", spl_series
    )
))

# Build built-in startup file if wanted
use_builtin_startup_file = board.get("build.spl_build_startup_file", True)
use_builtin_startup_file = str(use_builtin_startup_file).lower() in ("1", "yes", "true")

if use_builtin_startup_file:
    startup_file = get_startup_filename(board)
    startup_file_filter = "-<*> +<%s>" % startup_file
    startup_file_path =  join(
            FRAMEWORK_DIR, spl_chip_type, "cmsis",
            "startup_files", startup_file)
    print("==== STARTUP FILE: %s ======" % startup_file)
    if not isfile(startup_file_path):
        print("Error: Startup file not found at expected place (%s)" % startup_file_path)
        env.Exit(-1)
    env.BuildSources(
        join("$BUILD_DIR", "FrameworkCMSISStartup"),
        join(
            FRAMEWORK_DIR, spl_chip_type, "cmsis",
            "startup_files"
        ),
        startup_file_filter
    )

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkSPL"),
    join(FRAMEWORK_DIR, spl_chip_type,
         "spl", "variants", spl_series, "src"),
    src_filter=" ".join(src_filter_patterns)
))

env.Append(LIBS=libs)

# include optional SPL libraries into the library search path for the LDF
# can be put in board def file, or overridden in the platformio.ini with
# board_build.spl_libs = no
def configure_builtin_spl_libs(board):
    SPL_LIBRARIES_PATH = join(FRAMEWORK_DIR, spl_chip_type, "spl", "libraries", spl_series)
    should_include_spl_libs = board.get("build.spl_libs", True)
    should_include_spl_libs = str(should_include_spl_libs).lower() in ("1", "yes", "true")
    print("SPL libraries are included: " + str(should_include_spl_libs))
    if isdir(SPL_LIBRARIES_PATH) and should_include_spl_libs:
        env.Append(
            LIBSOURCE_DIRS = SPL_LIBRARIES_PATH
        )

configure_builtin_spl_libs(board)

def configure_builtin_cmsis_libs(board):
    CMSIS_LIBRARIES_PATH = join(FRAMEWORK_DIR, "gd32", "cmsis", "libraries")
    should_include_cmsis_libs = board.get("build.cmsis_libs", True)
    should_include_cmsis_libs = str(should_include_cmsis_libs).lower() in ("1", "yes", "true")
    print("CMSIS libraries are included: " + str(should_include_cmsis_libs))
    if isdir(CMSIS_LIBRARIES_PATH) and should_include_cmsis_libs:
        env.Append(
            LIBSOURCE_DIRS = CMSIS_LIBRARIES_PATH
        )

configure_builtin_cmsis_libs(board)

# Configure possible FPU / DSP / VFP
# see https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
def configure_floatingpoint(board):
    # default settings: Soft-FP for Cortex-M33, Soft-FP for Cortex-M4(F).
    # CMSIS-DSP requires hardfloat for Cortex-M33
    # FreeRTOS requires softfloat for Cortex-M33
    # project has to select the right one... 
    should_use_cm33_hardfloat = board.get("build.cm33_hardfloat", False)
    should_use_cm33_hardfloat = str(should_use_cm33_hardfloat).lower() in ("1", "yes", "true")
    should_use_cm4_hardfloat = board.get("build.cm4_hardfloat", False)
    should_use_cm4_hardfloat = str(should_use_cm4_hardfloat).lower() in ("1", "yes", "true")
    # deduce flags
    board_cpu = board.get('build.cpu', "")
    core_type_to_fpu_flags = {
        "cortex-m33": [
            "-mfloat-abi=%s" % ("hard" if should_use_cm33_hardfloat else "softfp") , 
            "-march=armv8-m.main+dsp+fp" # E50x and W51x all have DSP + FPU
        ],
        "cortex-m4": [
            "-mfloat-abi=%s" % ("hard" if should_use_cm4_hardfloat else "softfp") , 
            "-mfpu=fpv4-sp-d16",
            "-march=armv7e-m+fp" # so that correct thumb\v7e-m+fp GCC library is selected
        ],
    }
    # inject
    if board_cpu in core_type_to_fpu_flags.keys():
        flags = core_type_to_fpu_flags[board_cpu]
        # add FPU/DSP/Float ABI flags to both compilation and linking stage
        env.Append(CCFLAGS=flags, LINKFLAGS=flags)

configure_floatingpoint(board)

def configure_printf_lib():
    # allows wrapping of printf functions though, e.g., printf-minimal library.
    if get_flag_value("use_minimal_printf", False):
        env.Append(LINKFLAGS=[
            "-Wl,--wrap,printf",
            "-Wl,--wrap,sprintf",
            "-Wl,--wrap,snprintf",
            "-Wl,--wrap,vprintf",
            "-Wl,--wrap,vsprintf",
            "-Wl,--wrap,vsnprintf",
            "-Wl,--wrap,fprintf",
            "-Wl,--wrap,vfprintf"
        ])

configure_printf_lib()
