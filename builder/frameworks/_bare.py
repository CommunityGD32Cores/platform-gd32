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

#
# Default flags for bare-metal programming (without any framework layers)
#

from SCons.Script import DefaultEnvironment
from os.path import join

env = DefaultEnvironment()

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall"
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        ("BOARD_NAME", '\\"%s\\"' % env.subst("$BOARD").upper()),
        env.subst("$BOARD").upper()
    ],

    LINKFLAGS=[
        "-Os",
        '-Wl,-Map="%s"' % join("${BUILD_DIR}", "${PROGNAME}.map"),
        "-Wl,--gc-sections,--relax"
    ],

    LIBS=["c", "gcc", "m", "stdc++"]
)

if "BOARD" in env:
    board = env.BoardConfig()
    is_riscv = board.get("build.mcu", "").startswith("gd32vw")

    if is_riscv:
        env.Append(
            CCFLAGS=[
                "-march=%s" % board.get("build.cpu"),
                "-mabi=ilp32"
            ],
            LINKFLAGS=[
                "-march=%s" % board.get("build.cpu"),
                "-mabi=ilp32",
                "-nostartfiles",
                "-Wl,--no-warn-rwx-segments"
            ]
        )
    else: #arm
        env.Append(
            CCFLAGS=[
                "-mcpu=%s" % board.get("build.cpu"),
                "-mthumb"
            ],
            LINKFLAGS=[
                "-mcpu=%s" % board.get("build.cpu"),
                "-mthumb"
            ]
        )

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

# create .lst file
env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJDUMP", "-drwC",
        "$BUILD_DIR/${PROGNAME}.elf", ">", "$BUILD_DIR/${PROGNAME}.lst"
    ]), "Building .pio/build/$PIOENV/${PROGNAME}.lst")
)