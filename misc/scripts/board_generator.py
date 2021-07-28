#!/usr/bin/env python3
import csv
import os
import json
from typing import Tuple, List

# This script converts CSV files, obtainable from the "Export to CSV" 
# button at e.g. https://www.gigadevice.com/products/microcontrollers/gd32/arm-cortex-m3/ 
# to PlatformIO board JSON definition.

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
        self.spl_series = None 
        self.sub_series = None
        self.mcu_url = None
        self.svd_path = None
        self.compile_flags = None
        self.arduino_variant = None
        self.usb_dfu_supported = False
        self.infer_missing_info()
    
    def __str__(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return "GD32MCUInfo(%s)" % ",".join(["%s=\"%s\"" % (key,val) for key,val in list(self.__dict__.items())])

    series_to_spl_series = {
        "GD32F303": "GD32F30x",
        "GD32F305": "GD32F30x",
        "GD32F307": "GD32F30x",
        "GD32F330": "GD32F3x0",
        "GD32F350": "GD32F3x0",
        "GD32F403": "GD32F403", #yes, this is correct. special SPL package for only that chip.
        "GD32F405": "GD32F4xx",
        "GD32F407": "GD32F4xx",
        "GD32F450": "GD32F4xx",
        "GD32E103": "GD32E10x"
    }

    known_arduino_variants = {
        "GD32F303CCT6": "GD32F303CC_GENERIC"
    }

    def infer_sub_series(self):
        sub_series = None
        if self.spl_series == "GD32F30x":
            # per GD32F30x user manual page 114. 
            # all 305xx are conenctivity line (CL)
            # other devs strictly over 512 kByte flash are XD (extra-density)
            # else HD (high-density)
            sub_series = "CL" if self.name.startswith("GD32F305") else "HD" if self.flash_kb <= 512 else "XD"
        # todo: GD32F10x logic
        self.sub_series = sub_series

    def infer_spl_series(self):
        if self.series in GD32MCUInfo.series_to_spl_series:
            self.spl_series = GD32MCUInfo.series_to_spl_series[self.series]

    def infer_svd_path(self):
        svd = None
        if self.sub_series is None:
            svd = f"{self.series}.svd"
        else:
            svd = f"{self.series}_{self.sub_series}.svd"
        self.svd_path = svd

    def infer_compile_flags(self):
        compile_flags = [] 
        compile_flags += ["-D" + self.series]
        compile_flags += ["-D" + self.spl_series]
        if self.sub_series is not None:
            compile_flags += ["-D" + self.spl_series.upper() + "_" + self.sub_series]
        # todo add series specific compile flags
        # fpr genericGD32F190C8 -DGD32F130_150 -D__GD32F130_SUBFAMILY -D__GD32F1x0_FAMILY
        # for genericGD32F130C8 -DGD32F130_150 -D__GD32F130_SUBFAMILY -D__GD32F1x0_FAMILY
        # double check if these are used in SPL
        self.compile_flags = compile_flags

    def infer_arduino_variant(self):
        if self.name in GD32MCUInfo.known_arduino_variants:
            self.arduino_variant =  GD32MCUInfo.known_arduino_variants[self.name]

    def infer_openocd_target(self):
        # TODO
        pass

    def infer_usb_dfu_supported(self):
        # TODO better logic. 
        # should return whether the device supports
        # native USB upload *or* supported by e.g.
        # STM32Duino bootloader.
        # USB bootloader created at later stage
        self.usb_dfu_supported = any( [
            self.name.startswith("GD32F103"),
            self.name.startswith("GD32F303"),
        ]) 
        pass

    def infer_missing_info(self):
        self.infer_spl_series()
        self.infer_sub_series()
        self.infer_svd_path()
        self.infer_compile_flags()
        self.infer_arduino_variant()
        self.infer_openocd_target()
        self.infer_usb_dfu_supported()
        self.mcu_url = f"https://www.gigadevice.com/microcontroller/{self.name.lower()}/"
        pass

    def set_val_if_exists(self, d, key, val):
        if val is not None:
            d[key] = val
    
    def add_val_if_true(self, d, key, check_value, add_value):
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
                "spl_series": self.spl_series
            },
            "debug": {
                "jlink_device": self.name_no_package.upper(),
                "openocd_target": "unknown",
                "svd_path": self.svd_path,
                "default_tools": [
                    "stlink"
                ]
                # todo: think about how to handle set CPUTAPID better.. just set to 0
                # openocd_extra_pre_target_args
            },
            "frameworks": [
                "spl"
            ],
            "name": self.name,
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
        self.set_val_if_exists(board["build"], "variant", self.arduino_variant)
        self.add_val_if_true(board, "frameworks", self.arduino_variant != None, "arduino")
        self.add_val_if_true(board["upload"], "protocols", self.usb_dfu_supported, "dfu")

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

def main():
    this_script_path = os.path.dirname(os.path.realpath(__file__))
    mcus = read_csv(os.path.join(this_script_path, "gd32_cortex_m4_devs.csv"), "cortex-m4")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m3_devs.csv"), "cortex-m3")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m23_devs.csv"), "cortex-m23")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m33_devs.csv"), "cortex-m33")

    #print(mcus)
    for x in mcus:
        print(repr(x))

    print(get_info_for_mcu_name("GD32F303CC", mcus))
    print(get_info_for_mcu_name("GD32F350CB", mcus))

    output_filename, board_def = get_info_for_mcu_name("GD32F303CC", mcus).generate_board_def()
    print(output_filename + ":")
    print(board_def)

    output_filename, board_def = get_info_for_mcu_name("GD32F350CB", mcus).generate_board_def()
    print(output_filename + ":")
    print(board_def)

    pass

if __name__ == '__main__':
    main()