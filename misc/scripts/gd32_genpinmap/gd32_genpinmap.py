from typing import List
from known_datasheets import identify_datasheet
from pin_map import GD32PinMap
from datasheet_parser import GD32DatasheetParser
from static_data import *
import pickle
from os import mkdir, path
import sys
from pinmap_converter import GD32PinMapGenerator

# add directory above us to the python path.
# needed so that we can sipphon info from the board generator
import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
# now we can use absolute imports
from board_generator import GD32MCUInfo, read_all_known_mcus

def get_all_mcus_matching_pinmap(all_mcus:List[GD32MCUInfo], pinmap:GD32PinMap) -> List[GD32MCUInfo]:
    # check whether device name is matches by any of the sub-families names
    subfams_name = pinmap.subseries_pinmaps.keys()
    return list(filter(lambda m: any([GD32PinMap.devicename_matches_constraint(m.name_no_package, fam) for fam in subfams_name]), all_mcus))

# cache previously parsed datasheet for speed reaonss
def save_pinmap(pinmap: GD32PinMap):
    this_script = path.dirname(path.realpath(__file__))
    if not path.isdir(path.join(this_script, "preparsed_datasheets")):
        mkdir(path.join(this_script, "preparsed_datasheets"))
    try:
        pickle.dump( pinmap, open( path.join(this_script, "preparsed_datasheets", pinmap.series + ".p"), "wb" ) )
    except Exception as exc:
        print("Saving pinmap failed with error: %s" % str(exc)) 

# return previously loaded instance or None if it doesn't exist
def load_pinmap(datasheet_pdf_path:str) -> GD32PinMap:
    datasheet = identify_datasheet(datasheet_pdf_path)
    if datasheet is None: 
        return None
    this_script = path.dirname(path.realpath(__file__))
    expected_filepath = path.join(this_script, "preparsed_datasheets", datasheet.series + ".p")
    print("Checking if pre-saved pickle file \"%s\" exists.." % expected_filepath)
    if path.isfile(expected_filepath):
        try:
            pinmap = pickle.load(open(expected_filepath, "rb"))
            return pinmap
        except Exception as exc:
            print("Loading pinmap failed with error: %s" % str(exc))         
    print("Nope, parsing from PDF.")
    return None

def main_func():
    print("Pinmap generator started.")
    all_mcus = read_all_known_mcus()
    # temporary static path
    datasheet_pdf_paths = [
        "C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F3x0\\GD32F350xx_Datasheet_Rev2.3.pdf"
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F30x\\GD32F303xx_Datasheet_Rev1.9.pdf"
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32E23x\\GD32E230xx_Datasheet_Rev1.4.pdf",
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F190xx_Datasheet_Rev2.1.pdf",
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F170xx_Datasheet_Rev2.1.pdf",
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F150xx_Datasheet_Rev3.2.pdf",
        #"C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F130xx_Datasheet_Rev3.4.pdf",
    ]
    for datasheet_pdf_path in datasheet_pdf_paths:
        device_pinmap = load_pinmap(datasheet_pdf_path)
        if device_pinmap is None or "--no-load-preparsed" in sys.argv or True:
            device_pinmap = GD32DatasheetParser.get_pinmap_for_pdf(datasheet_pdf_path)
            save_pinmap(device_pinmap)
            device_pinmap.solve_remapper_pins()
            #return
        all_matching_mcus = get_all_mcus_matching_pinmap(all_mcus, device_pinmap)
        GD32PinMapGenerator.generate_from_pinmap(device_pinmap, all_matching_mcus)
if __name__ == "__main__":
    main_func()
