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

class DatasheetPageParsingQuirk:
    def apply_to_pinmap(self, pinmap):
        raise NotImplementedError("Subclass did not implement function")

class OverwritePinAlternateInfoQuirk(DatasheetPageParsingQuirk):
    def __init__(self, pin_name:str, alternate_funcs: List[str]) -> None:
        super().__init__()
        self.pin_name = pin_name
        self.alternate_funcs = alternate_funcs

class OverwritePinAdditionalInfoQuirk(DatasheetPageParsingQuirk):
    def __init__(self, pin_name:str, additional_funcs_str: str) -> None:
        super().__init__()
        self.pin_name = pin_name
        self.additional_funcs_str = additional_funcs_str

class ParseUsingAreaQuirk(DatasheetPageParsingQuirk):
    def __init__(self, area) -> None:
        super().__init__()
        self.area = area

class DatasheetPageParsingInfo:
    def __init__(self, page_range: List[int], quirks:List[DatasheetPageParsingQuirk]=None):
        self.page_range = page_range
        if quirks is None:
            quirks = list()
        self.quirks = quirks

    def get_quirks_of_type(self, wanted_type) -> List[DatasheetPageParsingQuirk]:
        return list(filter(lambda q: isinstance(q, wanted_type), self.quirks))

class DatasheetAFPageParsingInfo(DatasheetPageParsingInfo):
    def __init__(self, page_range: List[int], footnotes_device_availablity: Dict[str, str], quirks:List[DatasheetPageParsingQuirk]=None) -> None:
        super().__init__(page_range, quirks)
        self.footnotes_device_availability = footnotes_device_availablity

class DatasheetPinDefPageParsingInfo(DatasheetPageParsingInfo):
    def __init__(self, page_range: List[int], subseries:str, package:str, quirks:List[DatasheetPageParsingQuirk]=None) -> None:
        super().__init__(page_range, quirks)
        self.subseries = subseries
        self.package = package

class DatasheetParsingInfo:
    def __init__(self, alternate_funcs: List[DatasheetAFPageParsingInfo], pin_defs: List[DatasheetPinDefPageParsingInfo], series:str, family_type:str) -> None:
        self.alternate_funcs = alternate_funcs
        self.pin_defs = pin_defs
        self.series = series 
        self.family_type = family_type

# Use this info to recognize the PDF and its parsing quirks.
# Every PDF will probably need different parsing quirks, like only
# scanning a range of pages at a time, different footnotes for device
# availability, the type of SPL family it belongs to (GD32F30x vs GD32F3x0 etc)
known_datasheets_infos: Dict[str, DatasheetAFPageParsingInfo] = {
    "GD32F190xx_Datasheet_Rev2.1.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([28,29], { "1": ["GD32F190x4"], "2": ["GD32F190x8", "GD32F190x6"], "3": ["GD32F190x8"]}),
            DatasheetAFPageParsingInfo([30,31], { "1": ["GD32F190x4"], "2": ["GD32F190x8", "GD32F190x6"], "3": ["GD32F190x8"]}),
            DatasheetAFPageParsingInfo([32],    { "1": ["GD32F190x4"], "2": ["GD32F190x8"]}, quirks=[
                ParseUsingAreaQuirk((95.623,123.157,766.102,533.928)),
                OverwritePinAlternateInfoQuirk("PF7", ["I2C0_SDA(1)/I2C1_SDA(2)", None, None, None, None, None, None, None, None, "SEG31"])
            ])
            #33rd page only has half of the PF7 line  -- parsed by using a quirk on the page before.
        ],
        pin_defs = [
            DatasheetPinDefPageParsingInfo([16], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((176.736,125.389,767.591,531.695))]),
            DatasheetPinDefPageParsingInfo([17,19], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((79.996,124.645,766.847,533.183))]),
            DatasheetPinDefPageParsingInfo([18,19], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((79.996,124.645,458.024,533.183))]),
            #DatasheetPinDefPageParsingInfo([21,24], "GD32F190Cx", "LQFP48", []),
            #DatasheetPinDefPageParsingInfo([25,27], "GD32F190Tx", "QFN36", [])
        ],
        series = "GD32F190", # series
        family_type = "B" # family type
    )
}

class GD32AdditionalFunc:
    def __init__(self, signal_name:str, subseries:str, package:str,) -> None:
        self.subseries = subseries
        self.package = package
        self.signal_name = signal_name
        self.peripheral:str = ""
        self.subfunction:str = None
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
        return "AdditionalFunc(" + ret + ")"

class GD32AdditionalFuncFamiliy:
    def __init__(self, subseries:str, package:str, additional_funcs: Dict[str, List[GD32AdditionalFunc]]) -> None:
        self.subseries = subseries
        self.package = package
        self.additional_funcs = additional_funcs

class GD32AlternateFunc:
    def __init__(self, signal_name:str, af_number:int, footnote:str, footnote_device_availability:Dict[str,str]) -> None:
        self.signal_name = signal_name
        self.footnote = footnote
        self.footnote_device_availability = footnote_device_availability
        self.footnote_resolved = None
        if self.footnote in self.footnote_device_availability:
            self.footnote_resolved = self.footnote_device_availability[self.footnote]
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
    def __init__(self, pin_name: str, af_functions_map: Dict[str, List[GD32AlternateFunc]], additional_functions: List[GD32AdditionalFunc]=None) -> None:
        self.pin_name = pin_name
        self.af_functions_map: Dict[str, List[GD32AlternateFunc]] = af_functions_map
        if additional_functions is None:
            additional_functions = list()
        self.additional_functions: List[GD32AdditionalFunc] = additional_functions
    def __repr__(self) -> str:
        return f"GD32Pin(pin={self.pin_name}, funcs={str(self.af_functions_map)}, add_funcs={str(self.additional_functions)}"

class GD32PinMap:
    def __init__(self, series: str, datasheet_info, pin_map: Dict[str, GD32Pin]) -> None:
        self.series = series
        self.datasheet_info = datasheet_info
        self.pin_map: Dict[str, GD32Pin] = pin_map

    CRITERIA_PERIPHERAL_STARTS_WITH = 0
    CRITERIA_PIN_SUB_FUNCTION = 1
    CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION = 2

    def search_pins_for_any_func(self, criteria_type, criteria_value) -> List[Tuple[GD32Pin, object]]:
        results_af = self.search_pins_for_af(criteria_type, criteria_value)
        results_ad = self.search_pins_for_add_func(criteria_type, criteria_value)
        return results_af + results_ad

    def search_pins_for_add_func(self, criteria_type, criteria_value) -> List[Tuple[GD32Pin, GD32AdditionalFunc]]:
        results = list()
        for p in self.pin_map.values():
            # search through all additional functions
            for additional_func in p.additional_functions:
                if criteria_type == GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH:
                    if (additional_func.peripheral == "" and additional_func.signal_name.startswith(criteria_value)) or additional_func.peripheral.startswith(criteria_value):
                        results.append((p, additional_func))
                elif criteria_type == GD32PinMap.CRITERIA_PIN_SUB_FUNCTION:
                    if additional_func.subfunction is not None and criteria_value in additional_func.subfunction:
                        results.append((p, additional_func))
                elif criteria_type == GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION:
                    if additional_func.peripheral.startswith(criteria_value[0]) and (additional_func.subfunction is not None and criteria_value[1] in additional_func.subfunction):
                        results.append((p, additional_func))
        return results

    def search_pins_for_af(self, criteria_type, criteria_value) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
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
        all_i2c_sda_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PIN_SUB_FUNCTION, "SDA")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        all_uart_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "UART")
        all_uart_pins.extend(pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "USART"))
        for pin, func in all_uart_pins:
            print("Found UART pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_rx_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("CAN", "RX"))
        for pin, func in all_can_rx_pins:
            print("Found CAN RX pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_pins = pinmap.search_pins_for_any_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "CAN")
        for pin, func in all_can_pins:
            if isinstance(func, GD32AlternateFunc):
                print("Found CAN pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  
            elif isinstance(func, GD32AdditionalFunc):
                print("Found CAN pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        all_adc_pins = pinmap.search_pins_for_add_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "ADC")
        for pin, func in all_adc_pins:
            print("Found ADC pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        #print(pinmap.pin_map["PB7"])
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

def get_pinmap_for_pdf(datasheet_pdf_path: str) -> GD32PinMap:
    # go through all alternate function pages as descriped
    datasheet_info = identify_datasheet(datasheet_pdf_path)
    if datasheet_info is None: 
        print(f"Failed to find datasheet info for filename {path.basename(datasheet_pdf_path)}.")
        print("Known datasheets: " + ",".join(known_datasheets_infos.keys()))
    pinmaps: List[GD32PinMap] = list()
    for af_page in datasheet_info.alternate_funcs:
        dataframe = get_dataframe_for_pdf_pages(datasheet_pdf_path, af_page)
        pin_map = process_af_dataframe(dataframe, datasheet_info, af_page)
        pinmaps.append(pin_map)
    additional_functions: List[GD32AdditionalFuncFamiliy] = list()
    for pindef_page in datasheet_info.pin_defs:
        dataframe = get_dataframe_for_pdf_pages(datasheet_pdf_path, pindef_page)
        add_func_family = process_add_funcs_dataframe(dataframe, datasheet_info, pindef_page)
        additional_functions.append(add_func_family)
    # merge all pinmap dictionary into the first object
    first_pinmap = pinmaps[0]
    for i in range(1, len(pinmaps)):
        first_pinmap.pin_map.update(pinmaps[i].pin_map)
    # merge all additional funcs families into first pinmap
    for add_func in additional_functions:
        merge_additional_funcs_into_pinmap(add_func, first_pinmap)
    print(pinmaps)
    #print_parsing_result_json(first_pinmap.pin_map)
    print("Parsed PDF \"%s\" and extracted %d pin infos." % (path.basename(datasheet_pdf_path), len(first_pinmap.pin_map)))
    return first_pinmap

def get_dataframe_for_pdf_pages(datasheet_pdf_path: str, pages_info: DatasheetPageParsingInfo) -> DataFrame:
    # lattice is important, can't correctly parse data otherwise
    area_quirk = pages_info.get_quirks_of_type(ParseUsingAreaQuirk)
    area = None
    if len(area_quirk) == 1:
        area = area_quirk[0].area
    dfs : DataFrame = tb.read_pdf(datasheet_pdf_path, pages=pages_info.page_range, lattice=True, stream=False, area=area) 
    if len(dfs) >= 1:
        dfs = pd.concat(dfs)
    else:
        print("Failed to extract one datatable from PDF")
        return False
    dfs = cleanup_dataframe(dfs)

    print(dfs)
    print(type(dfs))
    return dfs

def cleanup_dataframe(dfs: DataFrame) -> DataFrame:
    if len(dfs.columns) > 11:
        print("Before cleanup:")
        pd.set_option('display.expand_frame_repr', False)
        print(dfs)
        pd.set_option('display.expand_frame_repr', True)
        print("Need cleanup") 
        # the data for one AF is spread over two columsn. 
        # the left columns has the pin function, the right column has only "AFx" at the first row
        # and then only NaNs. 
        # We combine the two columns and drop the unneeded one.
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
    return dfs

def print_parsing_result_json(res:dict):
    as_json = json.dumps(res, indent=2, default=lambda o: o.__dict__)
    # string is large, breaks console. print block-wise
    n = 5*1024
    for x in [as_json[i:i+n] for i in range(0, len(as_json), n)]:
        print(x, end="", flush=True)
        sys.stdout.flush()

def remove_newlines(inp):
    if isinstance(inp, str):
        return inp.replace("\r", "")
    else:
        return inp

def analyze_additional_funcs_string(inp:str) -> List[str]: 
    # find where it says "additional"
    add_start = inp.find("Additional: ")
    # check if anyhting was found
    if add_start == -1:
        return list()
    # get the rest of the string after that
    inp = inp[add_start + len("Additional: "):]
    arr = inp.split(",")
    arr = [x.strip() for x in arr]
    return arr

def strip_pinname(pin_name:str):
    if "-" in pin_name:
        return pin_name[0 : pin_name.index("-")]
    return pin_name

def merge_additional_funcs_into_pinmap(add_funcs_fam:GD32AdditionalFuncFamiliy, gd32_pin_map:GD32PinMap):
    for pin in add_funcs_fam.additional_funcs.keys():
        add_funcs = add_funcs_fam.additional_funcs[pin]
        if pin not in gd32_pin_map.pin_map:
            print("Setting new pin %s with add funcs %s" % (pin, str(add_funcs)))
            gd32_pin_map.pin_map[pin] = GD32Pin(pin, dict(), add_funcs)
        else:
            print("Extending pin %s by funcs %s" % (pin, str(add_funcs)))
            gd32_pin_map.pin_map[pin].additional_functions.extend(add_funcs)

def process_add_funcs_dataframe(dfs: DataFrame, datasheet_info: DatasheetParsingInfo, pages_info: DatasheetPinDefPageParsingInfo) -> GD32AdditionalFuncFamiliy:
    additional_funcs: Dict[str, List[GD32AdditionalFunc]] = dict()
    for i, j in dfs.iterrows():
        if i == 0:
            # ignore row 
            continue 
        else: 
            # data row
            pin_row = list(j)
            pin_name = remove_newlines(pin_row[0])
            if is_nan(pin_name) or pin_name == "Pin Name" or not pin_name.startswith("P"):
                print("Skipping empty line because pin is not there.")
                continue
            pin_name = strip_pinname(pin_name)
            last_column: str = j[len(j) - 1]
            last_column = last_column.replace("\r", " ")
            add_funcs_arr = analyze_additional_funcs_string(last_column)
            print("Pin %s Add. Funcs: %s" % (pin_name, str(add_funcs_arr)))
            additional_funcs[pin_name] = [GD32AdditionalFunc(sig, pages_info.subseries, pages_info.package) for sig in add_funcs_arr]
    #print(additional_funcs)
    return GD32AdditionalFuncFamiliy(pages_info.subseries, pages_info.package, additional_funcs)

def process_af_dataframe(dfs: DataFrame, datasheet_info: DatasheetParsingInfo, pages_info: DatasheetAFPageParsingInfo) -> GD32PinMap:
    parser_result = {
        "alternate_functions": [],
        "pins": dict()
    }
    for i, j in dfs.iterrows():
        # debug info
        if False:
            print("i")
            print(i)
            print("j")
            print(j)
        # first row gives us list of alternate functions (AF0..AF11) in the table!
        if i == 0:
            alternate_funcs = filter_nans(j)
            print(alternate_funcs)
            parser_result["alternate_functions"] = alternate_funcs
        else: 
            # data row
            pin_row = list(j)
            pin_name = pin_row[0]
            if is_nan(pin_name) or pin_name == "Name":
                print("Skipping empty line because pin is not there.")
                continue
            pin_alternate_funcs = pin_row[1::]
            # apply possibly Overwrite pin alternate info quirk
            pin_override_quirks: List[OverwritePinAlternateInfoQuirk] = pages_info.get_quirks_of_type(OverwritePinAlternateInfoQuirk)
            for pin_override_quirk in pin_override_quirks:
                if pin_override_quirk.pin_name == pin_name:
                    pin_alternate_funcs = pin_override_quirk.alternate_funcs
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
                    af_list.append(GD32AlternateFunc(sig_name, get_trailing_number(af_name), footnote, pages_info.footnotes_device_availability))
                if af_name not in af_map:
                    af_map[af_name] = list()
                af_map[af_name].extend(af_list)
            #print(af_map)
            parser_result["pins"][pin_name] = GD32Pin(pin_name, af_map)
    print("Parsed all %d pins." % len(parser_result["pins"]))
    #print_parsing_result_json(parser_result["pins"])
    device_pinmap = GD32PinMap(datasheet_info.series, datasheet_info, parser_result["pins"])
    return device_pinmap

def identify_datasheet(datasheet_pdf_path: str) -> DatasheetParsingInfo:
    global known_datasheets_infos
    if path.basename(datasheet_pdf_path) in known_datasheets_infos:
        return known_datasheets_infos[path.basename(datasheet_pdf_path)]
    else:
        return None

def main_func():
    print("Pinmap generator started.")
    # temporary static path
    datasheet_pdf_path = "C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F190xx_Datasheet_Rev2.1.pdf"
    device_pinmap = get_pinmap_for_pdf(datasheet_pdf_path)
    GD32PinMapGenerator.generate_from_pinmap(device_pinmap)
if __name__ == "__main__":
    main_func()
