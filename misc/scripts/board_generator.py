#!/usr/bin/env python3
import csv
import os
import json
from typing import Tuple, List
import shutil

# This script converts CSV files, obtainable from the "Export to CSV" 
# button at e.g. https://www.gigadevice.com/products/microcontrollers/gd32/arm-cortex-m3/ 
# to PlatformIO board JSON definition.

# notes on SRAM situation on GD32F4xx devices:
# per GD32F4xx_User_Manual_Rev2.5.pdf p41 & 42
# 0x1000 0000 - 0x1000 FFFF   TCMSRAM(64KB)
# 0x2000 0000 - 0x2001 BFFF   SRAM0(112KB)
# 0x2001 C000 - 0x2001 FFFF   SRAM1(16KB)
# 0x2002 0000 - 0x2002 FFFF   SRAM2(64KB)
# 0x2003 0000 - 0x2006 FFFF   ADDSRAM(256KB)
# 0x4002 4000 - 0x4002 4FFF   BKP SRAM (4KB) [Backup/RTC Mem]

# -> we can treat all SRAMx sections as one continuous SRAM section
# however tightly-coupled memory SRAM (TCMSRAM) needs to be separated from that.

class GD32MCUInfo:
    def __init__(self, name, series, line, speed_mhz, flash_kb, sram_kb, core_type) -> None:
        self.name : str = name
        self.name_no_package = self.name[:-2]
        self.series = series
        self.line = line
        self.speed_mhz = speed_mhz
        self.flash_kb = flash_kb
        self.sram_kb = sram_kb
        self.core_type = core_type
        # information that will be filled out later
        self.core_coupled_memory_kb = 0
        self.spl_series = None 
        self.sub_series = None
        self.mcu_url = None
        self.svd_path = None
        self.compile_flags = None
        self.arduino_variant = None
        self.mbedos_variant = None
        self.usb_dfu_supported = False
        self.openocd_target = None
        self.hwids = None
        self.infer_missing_info()
    
    def __str__(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return "GD32MCUInfo(%s)" % ",".join(["%s=\"%s\"" % (key,val) for key,val in list(self.__dict__.items())])

    series_to_spl_series = {
        "GD32F101": "GD32F10x",
        "GD32F103": "GD32F10x",
        "GD32F105": "GD32F10x",
        "GD32F107": "GD32F10x",
        "GD32F130": "GD32F1x0",
        "GD32F150": "GD32F1x0",
        "GD32F170": "GD32F1x0",
        "GD32F190": "GD32F1x0",
        "GD32F205": "GD32F20x",
        "GD32F207": "GD32F20x",
        "GD32F303": "GD32F30x",
        "GD32F305": "GD32F30x",
        "GD32F307": "GD32F30x",
        "GD32F330": "GD32F3x0",
        "GD32F350": "GD32F3x0",
        "GD32F403": "GD32F403", # yes, this is correct. special SPL package for only that chip.
        "GD32F405": "GD32F4xx",
        "GD32F407": "GD32F4xx",
        "GD32F450": "GD32F4xx",
        "GD32E103": "GD32E10X", # uppercase X here is *wanted*.
        "GD32E230": "GD32E23x",
        "GD32E231": "GD32E23x",
        "GD32E232": "GD32E23x", # MCU not yet available
        "GD32E503": "GD32E50X", # uppercase X here is *wanted*.
        "GD32E505": "GD32E50X",
        "GD32E507": "GD32E50X",
        "GD32E508": "GD32E50X"  # listed in SPL header but no chip listed yet..
    }

    spl_series_to_openocd_target = {
        "GD32F10x": "stm32f1x",
        "GD32F1x0": "stm32f1x",
        "GD32F20x": "stm32f2x", # guess
        "GD32E23x": "stm32f2x", # guess, these are cortex-m23. probably needs https://github.com/GigaDevice-Semiconductor/openocd/blob/xpack/tcl/target/gd32e23x.cfg
        "GD32E50X": "stm32f4x", # guess, these are cortex-m33. will likely not work, needs custom OpenOCD expansion..
        "GD32F30x": "stm32f1x",
        "GD32F3x0": "stm32f1x",
        "GD32E10X": "stm32f1x",
        "GD32F20x": "stm32f2x",
        "GD32F4xx": "stm32f4x",
        "GD32F450": "stm32f4x"
    }

    known_arduino_variants = {
        "GD32F303CCT6": "GD32F303CC_GENERIC",
        "GD32F190C8T6": "GD32F190C8_GENERIC",
        "GD32F350G8U6": "GD32350G_START"
    }

    known_mbedos_variants = {
        "GD32F450ZIT6": "GD32_F450ZI",
        "GD32E103VBT6": "GD32_E103VB",
        "GD32F307VGT6": "GD32_F307VG"
    }   

    # stm32duino bootloader hwid's PID/VID
    leaf_hwids = [
      [
        "0x1EAF",
        "0x0003"
      ],
      [
        "0x1EAF",
        "0x0004"
      ]
    ]

    def infer_sub_series(self):
        sub_series = None
        if self.spl_series == "GD32F30x":
            # per GD32F30x user manual page 114. 
            # all 305xx and 307xx are conenctivity line (CL)
            # other devs strictly over 512 kByte flash are XD (extra-density)
            # else HD (high-density)
            sub_series = "CL" if self.name.startswith("GD32F305") or self.name.startswith(
                "GD32F307") else "HD" if self.flash_kb <= 512 else "XD"
        if self.spl_series == "GD32F20x":
            # all GD32F20x parts are CL parts, evident by the gd32f20x.h header file.
            sub_series = "CL"
        if self.spl_series == "GD32F10x":
            # determine whether it's a CL, HD, MD or XD series chip.
            # per GD32F10x_User_Manual_EN_V2.3-3.pdf page 112.
            if self.name.startswith("GD32F105") or self.name.startswith("GD32F107"):
                sub_series = "CL"
            else:
                # 16-128kByte: MD
                # 256-512kByte: HD
                # >512kByte: XD
                sub_series = "MD" if self.flash_kb <= 128 else "HD" if self.flash_kb <= 512 else "XD"
        if self.spl_series == "GD32E50X":
            # there are GD32EPRT, GD32E50X_HD, GD32E50X_XD, GD32E50X_CL and GD32E508..
            # however, only CL, XD and HD are explained
            if self.name.startswith("GD32E505") or self.name.startswith("GD32E507"):
                sub_series = "CL"
            elif not self.name.startswith("GD32E508"):
                # 256-512kByte: HD
                # >512kByte: XD
                sub_series = "HD" if self.flash_kb <= 512 else "XD"
        self.sub_series = sub_series

    def infer_spl_series(self):
        if self.series in GD32MCUInfo.series_to_spl_series:
            self.spl_series = GD32MCUInfo.series_to_spl_series[self.series]

    def infer_svd_path(self):
        svd = None
        if self.sub_series is None:
            svd = f"{self.spl_series}.svd"
        else:
            svd = f"{self.spl_series}_{self.sub_series}.svd"
        # special case for E23x series
        if self.spl_series == "GD32E23x":
            svd = f"{self.series}.svd"
        self.svd_path = svd

    def infer_compile_flags(self):
        compile_flags = [] 
        compile_flags += ["-D" + self.series[0:6]]
        compile_flags += ["-D" + self.series]
        compile_flags += ["-D" + self.spl_series]
        if self.sub_series is not None:
            compile_flags += ["-D" + self.spl_series.upper() + "_" + self.sub_series]
        # todo add more series specific compile flags
        if self.spl_series == "GD32F1x0":
            if self.name.startswith("GD32F170") or self.name.startswith("GD32F190"):
                compile_flags += ["-DGD32F170_190"]
            else:
                compile_flags += ["-DGD32F130_150"]
        if self.spl_series == "GD32E10X":
            # SPL needs to know about crystal setup, else #error
            compile_flags += ["-DHXTAL_VALUE=8000000U" ,"-DHXTAL_VALUE_8M=HXTAL_VALUE"]
        self.compile_flags = compile_flags

    def infer_arduino_variant(self):
        if self.name in GD32MCUInfo.known_arduino_variants:
            self.arduino_variant = GD32MCUInfo.known_arduino_variants[self.name]
        # generated by gd32_genpinmap.py
        elif any([self.name.startswith(x) for x in ["GD32F190", "GD32F170", "GD32F150", "GD32F130", "GD32E230C"]]):
            self.arduino_variant = self.name_no_package + "_GENERIC"

    def infer_mbedos_variant(self):
        if self.name in GD32MCUInfo.known_mbedos_variants:
            self.mbedos_variant =  GD32MCUInfo.known_mbedos_variants[self.name]

    def infer_openocd_target(self):
        if self.spl_series in GD32MCUInfo.spl_series_to_openocd_target:
            self.openocd_target = GD32MCUInfo.spl_series_to_openocd_target[self.spl_series]

    def infer_usb_dfu_supported(self):
        # TODO better logic. 
        # should return whether the device supports
        # native USB upload *or* supported by e.g.
        # STM32Duino bootloader.
        # USB bootloader created at later stage
        # GD32F305xx and GD32F307xx have native DFU
        # see user manual page 41.
        self.usb_dfu_supported = any( [
            self.name.startswith("GD32F103"), # STM32Duino bootloader
            self.name.startswith("GD32F105"), # native DFU (CL)
            self.name.startswith("GD32F107"), # native DFU (CL)
            self.name.startswith("GD32F303"), # STM32Duino bootloader
            self.name.startswith("GD32F305"), # native DFU (CL)
            self.name.startswith("GD32F307"), # native DFU (CL)
        ])
        # assume for now all USB DFU enabled boards have the PID/VID of the 
        # leafpad / STM32Duino bootloader.
        if self.usb_dfu_supported: 
            self.hwids = GD32MCUInfo.leaf_hwids
        pass

    def infer_correct_sram_allocation(self):
        # the reported "SRAM" size from the CSV file is not the full truth.
        # SRAM is split into many regions, non-contiguous in some cases.
        # PlatformIO (and the linker script generator) assumes the "upload.maximum_ram_size"
        # is the length of contiguous SRAM and sets the initial stack pointer (SP) at the end
        # of RAM. 
        # However, for some series (GD32F4xx), the MCU has special "core-coupled memory" (CCM), 
        # or also called "tightly-coupled memory" (TCM), which is not contiguous with the normal 
        # SRAM banks (SRAM0, SRAM1, etc.)
        # Hence we need to adjust the upoad.maximum_ram_size so that the linker script doesn't
        # set the SP into memory that doesn't exist.
        # the only F4 series that does not have TCMSRAM is GD32F403xx.
        if self.series == "GD32F405" or self.series == "GD32F407" or self.series == "GD32F450":
            # subtract size of TCM SRAM
            # SRAM0 and SRAM1 are contiguous (112 + 16 kB)
            # from GD32F407xx_Datasheet_Rev2.1.pdf page 71
            # or GD32F405xx_Datasheet_Rev2.1.pdf page 52 respectively
            # GD32F450xx_Datasheet_Rev2.1.pdf pages 56, 17
            # SRAM0,1,2 and ADDSRAM are contiguous, TCSRAM (64Kbyte is not)
            self.sram_kb -= 64
            self.core_coupled_memory_kb += 64

    def infer_missing_info(self):
        self.infer_correct_sram_allocation()
        self.infer_spl_series()
        self.infer_sub_series()
        self.infer_svd_path()
        self.infer_compile_flags()
        self.infer_arduino_variant()
        self.infer_mbedos_variant()
        self.infer_openocd_target()
        self.infer_usb_dfu_supported()
        self.mcu_url = f"https://www.gigadevice.com/microcontroller/{self.name.lower()}/"

    def set_val_if_exists(self, d, key, val):
        if val is not None:
            d[key] = val
    
    def add_val_to_arr_if_true(self, d, key, check_value, add_value):
        if check_value is True:
            d[key] += [add_value]

    def generate_board_def(self) -> Tuple[str,str]:
        # cut off last 2 chars for name
        output_filename = f"generic{self.name_no_package}.json"
        board = {
            "build": {
                "core": "gd32",
                "cpu": self.core_type,
                "extra_flags": " ".join(self.compile_flags),
                "f_cpu": str(self.speed_mhz * 1_000_000) + "L",
                "mcu": self.name.lower(),
                "spl_series": self.spl_series,
                "series": self.series
            },
            "debug": {
                "jlink_device": self.name_no_package.upper(),
                "openocd_target": self.openocd_target if self.openocd_target != None else "unknown",
                "svd_path": self.svd_path,
                "default_tools": [
                    "stlink"
                ],
                # todo: think about how to handle set CPUTAPID better.. just set to 0 for "ignore". 
                # for the gd32f30x series it is known to be 0x2ba01477
                "openocd_extra_pre_target_args": [
                    "-c",
                    "set CPUTAPID %s" % ("0x2ba01477" if self.spl_series == "GD32F30x" else "0")
                ]
            },
            "frameworks": [
                "spl"
            ],
            "name": f"{self.name_no_package} ({self.sram_kb + self.core_coupled_memory_kb}k RAM, {self.flash_kb}k Flash)",
            "upload": {
                "disable_flushing": False,
                "maximum_ram_size": self.sram_kb * 1024,
                "maximum_size": self.flash_kb * 1024,
                "protocol": "stlink",
                "protocols": [
                    "jlink",
                    "cmsis-dap",
                    "stlink",
                    "blackmagic",
                    "sipeed-rv-debugger",
                    "serial"
                ],
                # todo check if these make sense...
                "require_upload_port": True,
                "use_1200bps_touch": False,
                "wait_for_upload_port": False,
            },
            "url": self.mcu_url,
            "vendor": "GigaDevice"
        }
        self.set_val_if_exists(board["build"], "hwids", self.hwids)
        self.set_val_if_exists(board["build"], "spl_sub_series", self.sub_series)
        self.set_val_if_exists(board["build"], "variant", self.arduino_variant)
        self.add_val_to_arr_if_true(board, "frameworks", self.arduino_variant != None, "arduino")
        self.add_val_to_arr_if_true(board, "frameworks", self.mbedos_variant != None, "mbed")
        self.set_val_if_exists(board["build"], "mbed_variant", self.mbedos_variant)
        self.add_val_to_arr_if_true(board["upload"], "protocols", self.usb_dfu_supported, "dfu")
        self.set_val_if_exists(board["upload"], "closely_coupled_ram_size", self.core_coupled_memory_kb * 1024 if self.core_coupled_memory_kb != 0 else None)

        board_def = json.dumps(board, indent=2)
        return output_filename, board_def

def read_csv(filename, core_type) -> List[GD32MCUInfo]:
    mcus = []
    with open(filename) as csvfile:
        csv_reader_object = csv.DictReader(csvfile, delimiter=',')
        for row in csv_reader_object:
            print(row)
            mcu = GD32MCUInfo(row["Part No."], row["Series"], row["Line"], int(row["Speed"]), int(row["Flash"][:-1]), int(row["SRAM"][:-1]), core_type)
            mcus.append(mcu)
    return mcus

def get_info_for_mcu_name(mcu_name, mcu_data):
    for mcu in mcu_data:
        if mcu.name.lower().startswith(mcu_name.lower()):
            return mcu

def read_all_known_mcus() -> List[GD32MCUInfo]:
    this_script_path = os.path.dirname(os.path.realpath(__file__))
    mcus = []
    mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m4_devs.csv"), "cortex-m4")
    mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m3_devs.csv"), "cortex-m3")
    mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m23_devs.csv"), "cortex-m23")
    mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m33_devs.csv"), "cortex-m33")
    return mcus

def main():
    mcus = read_all_known_mcus()

    #print(mcus)
    for x in mcus:
        print(repr(x))

    # special case: GD32E232 MCUs are listed in the CSV file but have no released datasheet or SPL support yet
    # (the GD32E23x.h only accepts E230 or E231, not E232).
    # these are probabl "upcoming" MCUs. 
    # filter them from the list for now.
    mcus = list(filter(lambda x: x.series != "GD32E232", mcus))

    print(get_info_for_mcu_name("GD32F303CC", mcus))
    print(get_info_for_mcu_name("GD32F350CB", mcus))
    print(get_info_for_mcu_name("GD32F103C8", mcus))
    print(get_info_for_mcu_name("GD32F205RE", mcus))
    print(get_info_for_mcu_name("GD32E230C4", mcus))

    #return
    #print_board_files_mcus = ["GD32F303CC", "GD32F350CB", "GD32F450IG", "GD32E103C8"]
    #print(get_info_for_mcu_name("GD32F450IG", mcus))
    #print_board_files_mcus = ["GD32F450IG", "GD32F405RG"]
    #print_board_files_mcus = ["GD32F103C8", "GD32F205RE"]
    #print_board_files_mcus = ["GD32E231C8T6"]
    print_board_files_mcus = ["GD32E507ZE"]

    for mcu in print_board_files_mcus:
        output_filename, board_def = get_info_for_mcu_name(mcu, mcus).generate_board_def()
        print(output_filename + ":")
        print(board_def)
    #return
    if os.path.exists("generated_output"):
        shutil.rmtree("generated_output")
    os.mkdir("generated_output")
    for x in mcus:  
        output_filename, board_def = x.generate_board_def()
        with open(os.path.join("generated_output", output_filename), "w") as fp:
            fp.write(board_def)

    print("Done writing %d board defs." % len(mcus))

if __name__ == '__main__':
    main()
