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
        self.name = name
        self.series = series
        self.line = line
        self.speed_mhz = speed_mhz
        self.flash_kb = flash_kb
        self.sram_kb = sram_kb
        self.core_type = core_type
    
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
        "GD32F450": "GD32F4xx"
    }

    def inferr_missing_info(self):
        mcu_url = f"https://www.gigadevice.com/microcontroller/{self.name.lower()}/"
        pass
    
    def generate_board_def() -> Tuple[str,str]:
        pass

def read_csv(filename, core_type) -> List[GD32MCUInfo]:
    mcus = []
    with open(filename) as csvfile:
        csv_reader_object = csv.DictReader(csvfile, delimiter=',')
        for row in csv_reader_object:
            print(row)
            mcu = GD32MCUInfo(row["Part No."], row["Series"], row["Line"], int(row["Speed"]), int(row["Flash"][:-1]), int(row["SRAM"][:-1]), core_type)
            mcus.append(mcu)
    return mcus

def main():
    this_script_path = os.path.dirname(os.path.realpath(__file__))
    mcus = read_csv(os.path.join(this_script_path, "gd32_cortex_m4_devs.csv"), "cortex-m4")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m3_devs.csv"), "cortex-m3")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m23_devs.csv"), "cortex-m23")
    #mcus += read_csv(os.path.join(this_script_path, "gd32_cortex_m33_devs.csv"), "cortex-m33")

    #print(mcus)
    for x in mcus:
        print(repr(x))
    pass

if __name__ == '__main__':
    main()