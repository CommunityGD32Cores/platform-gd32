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

import os

from SCons.Script import AlwaysBuild

Import("env")

platform = env.PioPlatform()
FRAMEWORK_DIR = platform.get_package_dir("framework-wifi-sdk-gd32")

def WiFiSDKBuildProgram(env):
    env["LDSCRIPT_PATH"] = None
    env.ProcessProgramDeps()
    env.ProcessProjectDeps()

    # append into the beginning a main LD script
    env.Prepend(LINKFLAGS=["-T", "$LDSCRIPT_PATH"])

    # enable "cyclic reference" for linker
    if env.get("LIBS") and env.GetCompilerType() == "gcc":
        env.Prepend(_LIBFLAGS="-Wl,--start-group ")
        env.Append(_LIBFLAGS=" -Wl,--end-group")

    mbl_program = env.Program(
        os.path.join("$BUILD_DIR", "mbl"), env["PIOBUILDFILES"][0],
        LDSCRIPT_PATH=os.path.join("$BUILD_DIR", "mbl_gdm32_ns_processed.ld"),
        LIBS=[], # fix to stop making env.BuildLibrary() files appear in bootloader
        LIBPATH=[],
        LINKFLAGS= env["LINKFLAGS"] + ["-Wl,--print-memory-usage", "-Wl,-Map=$BUILD_DIR/mbl/mbl.map"],
        _LIBFLAGS=[]
    )
    mbl_bin = env.ElfToBin(os.path.join("$BUILD_DIR", "mbl"), mbl_program)

    program = env.Program(
        os.path.join("$BUILD_DIR", env.subst("$PROGNAME")),
        env["PIOBUILDFILES"][1:],
        LDSCRIPT_PATH=os.path.join("$BUILD_DIR", "nspe_gdm32_ns_processed.ld")
    )

    env.Depends(program, mbl_bin)

    env.Replace(PIOMAINPROG=program)

    AlwaysBuild(
        env.Alias(
            "checkprogsize",
            program,
            env.VerboseAction(env.CheckUploadSize, "Checking size $PIOMAINPROG"),
        )
    )

    print("Building in %s mode" % env.GetBuildType())

    return program

env.AddMethod(WiFiSDKBuildProgram, "BuildProgram")
