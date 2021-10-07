import math
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import pandas as pd
from typing import Dict, Tuple, List
import json
import sys
from os import path
import re
try:
    import tabula as tb
except ImportError:
    print("Could not import pdfminer. Please 'pip install pdfminer.six' first!")
    exit(-1)

def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

# ToDo: Use this info to recognize the PDF and its parsing quirks.
# Every PDF will probably need different parsing quirks, like only
# scanning a range of pages at a time, different footnotes for device
# availability, the type of SPL family it belongs to (GD32F30x vs GD32F3x0 etc)
known_datasheets_infos = {
    "GD32F190xx_Datasheet_Rev2.1.pdf" : {
        "alternate_funcs": { 
            "pages": [[28,29],[30,31],[32],[33]], #33rd page only has half of the PF7 line 
            "footnotes_device_availability": {
                "1": ["GD32F190x4"],
                "2": ["GD32F190x8", "GD32F190x6"],
                "3": ["GD32F190x8"],
            }
        },
        "series": "GD32F190",
        "family_type": "B"
    }
}

class GD32AlternateFunc:
    def __init__(self, signal_name:str, af_number:int, footnote:str) -> None:
        self.signal_name = signal_name
        self.footnote = footnote
        self.peripheral:str = ""
        self.subfunction:str = None
        self.af_number:int = af_number
        try:
            if "_" in self.signal_name:
                self.peripheral = self.signal_name.split("_")[0]
                self.subfunction = "_".join(self.signal_name.split("_")[1:])
        except Exception as exc:
            print("Failed to decode peripheral name: " + str(exc))
    def __repr__(self) -> str:
        ret = ""
        if self.peripheral is not None:
            ret += f"({self.peripheral}) "
        ret += f"{self.signal_name}"
        if self.footnote is not None:
            ret += f" ({self.footnote})"
        return "Func(" + ret + ")"

class GD32Pin:
    def __init__(self, pin_name: str, af_functions_map: Dict[str, GD32AlternateFunc]) -> None:
        self.pin_name = pin_name
        self.af_functions_map = af_functions_map
    def __repr__(self) -> str:
        return f"GD32Pin(pin={self.pin_name}, funcs={str(self.af_functions_map)}"

class GD32PinMap:
    def __init__(self, series: str, datasheet_info, pin_map: Dict[str, GD32Pin]) -> None:
        self.series = series
        self.datasheet_info = datasheet_info
        self.pin_map = pin_map

    CRITERIA_PERIPHERAL_STARTS_WITH = 0
    CRITERIA_PIN_SUB_FUNCTION = 1
    CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION = 2

    def search_pins(self, criteria_type, criteria_value) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        results = list()
        for p in self.pin_map.values():
            # search through all alternate functions pins
            for alternate_funcs in p.af_functions_map.values():
                for alternate_func in alternate_funcs:
                    if criteria_type == GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH:
                        if alternate_func.peripheral.startswith(criteria_value):
                            results.append((p, alternate_func))
                    elif criteria_type == GD32PinMap.CRITERIA_PIN_SUB_FUNCTION:
                        if alternate_func.subfunction is not None and criteria_value in alternate_func.subfunction:
                            results.append((p, alternate_func))
                    elif criteria_type == GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION:
                        if alternate_func.peripheral.startswith(criteria_value[0]) and (alternate_func.subfunction is not None and criteria_value[1] in alternate_func.subfunction):
                            results.append((p, alternate_func))
        return results
        
class GD32PinMapGenerator:
    @staticmethod
    def generate_from_pinmap(pinmap: GD32PinMap):
        all_i2c_sda_pins = pinmap.search_pins(GD32PinMap.CRITERIA_PIN_SUB_FUNCTION, "SDA")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_uart_pins = pinmap.search_pins(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "UART")
        all_uart_pins.extend(pinmap.search_pins(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "USART"))
        for pin, func in all_uart_pins:
            print("Found UART pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_rx_pins = pinmap.search_pins(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, ("CAN", "RX"))
        for pin, func in all_can_rx_pins:
            print("Found CAN RX pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  


        pass

def is_nan(number_or_obj):
    return type(number_or_obj) == float and math.isnan(number_or_obj)

def filter_nans(list_input: Series) -> list:
    return [x for x in list_input if not is_nan(x) and x != ""]

def filter_string(input_str_or_float: str):
    if type(input_str_or_float) == str:
        input_str_or_float = input_str_or_float.replace("\r", "\n")
        #print("%s (%d newlines)" % (input_str_or_float.encode('utf-8'), input_str_or_float.count("\n")))
        # the pin alternate functions decsription is complicated.
        # e.g, some fileds are simple. 
        # "I2C0_SDA" --> Pin alternate function is always I2C0_SDA, for all devices
        # "TIMER1_CH0,TIMER1_ETI" means the pin has two functions at the same time (??)
        #    in this case Timer 1 channel 0, but also timer 1 "ETI" ("External Trigger Input"), 
        #    I guess depending on timer settings.
        #    in the case of the Arduino pinmap, we do not care about that "ETI" in this case, just
        #    the pins where PWM output is possible, and for that, only the TIMER1_CH0 is the important
        #    info -- the info that the pin is capable of being TIMER1_ETI will not be in th Arduino pinmap.
        #    But let's filter that at a later time, and include all info at this stage. 
        #  "USART0_CTS(1)/USART1_CTS(2)" 
        #     -> there are footnotes which say that a function is only available for specific devices 
        #     -> e.g. "(1)" means "on GD32F190x4 devices only", "(2)" means "on GD32F190x8/6 devices"
        #     -> this a constraint: for x4 devices, this is equivalent to the simple "USART0_CTS", for x8/x6 
        #        this is "USART1_CTS", for all other device classes, the pin function is not available.
        #     -> when generating the final pinmap, the script needs to take into account for which exact 
        #        device were a generating it and filter it in the last stage.
        # "SPI1_MOSI(3)" 
        #     -> again refering to a footnote, "available on GD32F190x8 devices"
        #     -> for all x8 devices, this is equal to a simple "SPI1_MOSI", for all other devices it is not available.
        # there are weird newlines in thie output which break the text in the middle or accross two 
        # separate pin functions -- stith them together as appropriately as possible.
        if input_str_or_float.count("\n") >= 3:
            # remove first newline, convert second to "/" if it's not a list but an either-or, remove third newline
            input_str_or_float = input_str_or_float.replace("\n", "", 1)
            # indicates pin has multiple functions at once, keep existing comma as a separator
            # some pin names also have a built-in "/", e..g, SPI2_NSS / I2S2_WS, there we keep the "/"
            if "," in input_str_or_float or "/" in input_str_or_float: 
                input_str_or_float = input_str_or_float.replace("\n", "", 1)
            else:
                input_str_or_float = input_str_or_float.replace("\n", "/", 1) # use / to indicate an "either/or" relationship
            input_str_or_float = input_str_or_float.replace("\n", "", 1)
        elif input_str_or_float.count("\n") >= 1:
            input_str_or_float = input_str_or_float.replace("\n", "", 1)
        # remove all still contained newlines.
        input_str_or_float = input_str_or_float.replace("\n", "")

        # domain specific cleanup
        if "SPI" in input_str_or_float and "I2S" in input_str_or_float:
            input_str_or_float = input_str_or_float.replace("I2S", "_I2S")
            input_str_or_float = input_str_or_float.replace("/I2S", "_I2S")
            # cleanup for double forward slash
            input_str_or_float = input_str_or_float.replace("//", "/")
            input_str_or_float = input_str_or_float.replace("/_", "_")
            #input_str_or_float = input_str_or_float.replace("/,", ",")

        return input_str_or_float
    else: 
        # convert float NaN to more easily handable python None value
        return None if is_nan(input_str_or_float) else input_str_or_float


def main_func():
    print("Pinmap generator started.")
    # temporary static path
    datasheet_pdf_path = "C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F190xx_Datasheet_Rev2.1.pdf"
    #datasheet_af_pages = [28, 29, 30, 31, 32, 33]
    #datasheet_af_pages = [28, 29]
    datasheet_af_pages = [30, 31]
    #datasheet_af_pages = [32, 33]
    dfs : DataFrame = tb.read_pdf(datasheet_pdf_path, pages=datasheet_af_pages, stream=True, lattice=True) # lattice is important, can't correctly parse data otherwise
    print("Extract %d tables." % len(dfs))
    # if we just extract multiple tables from multiple pages, merge them together to one.
    if len(dfs) >= 1:
        dfs = pd.concat(dfs)
    else:
        print("Failed to extract one datatable from PDF")
        exit(0)
    # cleanup garbage columns (parser is not perfect...)
    #dfs = dfs.dropna(axis=1, how='all')
    if len(dfs.columns) > 11:
        print("Need cleanup") 
        # the data for one AF is spread over two columsn. 
        # the left columns has the pin function, the right column has only "AFx" at the first row
        # and then only NaNs. 
        # We combine the two columns and drop the unneeded one.
        orig_len = len(dfs.columns)
        for i in range(1, len(dfs.columns), 2):
            left_col_name = "Unnamed: %d" % (i)
            right_col_name = "Unnamed: %d" % (i+1)
            if right_col_name not in dfs.columns:
                continue
            dfs[left_col_name] = dfs.apply(lambda row: row[left_col_name] if not pd.isna(row[left_col_name]) else row[right_col_name], axis=1)
            dfs = dfs.drop([right_col_name], axis=1)
        # combine the pin column too
        dfs["Pin"] = dfs.apply(lambda row: row["Unnamed: 0"] if not pd.isna(row["Unnamed: 0"]) else row["Pin"], axis=1)
        dfs = dfs.drop(["Unnamed: 0"], axis=1)
        # last column is all NaNs
        dfs = dfs.drop([dfs.columns[-1]], axis=1)

        # source_col_loc = dfs.columns.get_loc('Unnamed: 1') # column position starts from 0
        #dfs['Unnamed: 1'] = dfs.iloc[:,source_col_loc+1:source_col_loc+2].apply(
        #    lambda x: " BLAH ".join(x.astype(str)), axis=1)

    #print(dfs["Unnamed: 1"])
    # for special pages where the parser fails: combine columns
    print(dfs)
    print(type(dfs))
    #return

    parser_result = {
        "alternate_functions": [],
        "pins": dict()
    }

    # iterating over rows using iterrows() function
    for i, j in dfs.iterrows():
        # debug info
        if False:
            print("i")
            print(i)
            print("j")
            print(j)
        # first row gives us list of alternate functions (AF0..AF11) in the table!
        if i == 0:
            #print("Detected first row")
            alternate_funcs = filter_nans(j)
            print(alternate_funcs)
            #print(type(alternate_funcs))
            parser_result["alternate_functions"] = alternate_funcs
        else: 
            #print("got data row")
            pin_row = list(j)
            pin_name = pin_row[0]
            if is_nan(pin_name) or pin_name == "Name":
                print("Skipping empty line because pin is not there.")
                continue
            pin_alternate_funcs = pin_row[1::]
            pin_alternate_funcs = [filter_string(x) for x in pin_alternate_funcs]
            #print("[Before adjustment] Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
            print("Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
            af_map = dict()
            for ind, func in enumerate(pin_alternate_funcs):
                af_name = parser_result["alternate_functions"][ind]
                # check if individual breakup is needed
                funcs = None
                if func is None: 
                    continue
                if "/" in func:
                    funcs = func.split("/")
                else:
                    funcs = [func]
                af_list = list()
                for f_idx, f in enumerate(funcs):
                    # check if we need to extra footnotes
                    sig_name = f 
                    footnote = None
                    if "(" in f and ")" in f:
                        sig_name = f[0:f.index("(")]
                        func_footnode_part = f[f.index("("):]
                        # strip first and last char
                        footnote = func_footnode_part[1:-1]
                        #print("Got func with footnote. name = %s footnote = %s"  % (str(sig_name), str(func_footnode_part)))
                    af_list.append(GD32AlternateFunc(sig_name, get_trailing_number(af_name), footnote))
                if af_name not in af_map:
                    af_map[af_name] = list()
                af_map[af_name].extend(af_list)
            #print(af_map)
            parser_result["pins"][pin_name] = GD32Pin(pin_name, af_map)
            #for pin_func in pin_alternate_funcs:
            #    print(pin_func)
            #if i == 3:
            #    exit(0)
            #for x in j:
            #    print(x)
    print("Parsed all %d pins." % len(parser_result["pins"]))
    as_json = json.dumps(parser_result["pins"], indent=2, default=lambda o: o.__dict__)
    # string is large, breaks console. print block-wise
    n = 5*1024
    for x in [as_json[i:i+n] for i in range(0, len(as_json), n)]:
        print(x, end="", flush=True)
    print("")
    print("Done.")

    datasheet_info = known_datasheets_infos[path.basename(datasheet_pdf_path)]
    device_pinmap = GD32PinMap(datasheet_info["series"], datasheet_info, parser_result["pins"])
    print(device_pinmap)

    GD32PinMapGenerator.generate_from_pinmap(device_pinmap)
if __name__ == "__main__":
    main_func()
