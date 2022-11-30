import math
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import pandas as pd
from typing import Dict, Tuple, List
import json
from os import path
import sys
try:
    import tabula as tb
except ImportError:
    print("Could not import tabula. Please 'pip install tabula-py' first!")
    exit(-1)

from parsing_quirks import OverwritePinAlternateInfoQuirk, OverwritePinDescriptionQuirk, ParseUsingAreaQuirk, OverwriteAdditionFunctionsList, CondenseColumnsQuirk
from func_utils import get_trailing_number, filter_nans, is_nan, print_big_str
from parsing_info import DatasheetAFPageParsingInfo, DatasheetPageParsingInfo, DatasheetParsingInfo, DatasheetPinDefPageParsingInfo
from pin_definitions import GD32Pin, GD32PinFunction
from pin_map import GD32PinMap, GD32SubseriesPinMap
from known_datasheets import known_datasheets_infos, identify_datasheet

class GD32DatasheetParser:
    @staticmethod
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
                if input_str_or_float.count("(") >= 2 and input_str_or_float.count(")") >= 2:
                    input_str_or_float = input_str_or_float.replace("\n", "/", 1)
                else:
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
            # cleanup data error from datasheet ("SPI1_ MOSI(3)")
            if "_ " in input_str_or_float:
                input_str_or_float = input_str_or_float.replace("_ ", "_", 1)
            
            # cleanup double "/"
            if input_str_or_float.count("//") >= 1:
                input_str_or_float = input_str_or_float.replace("//", "/")

            # slight timer fixup.. if we detected "_CH%d_TIMER" we put a 
            # , after the %d. 
            # e.g., TIMER1_CH0TIMER1_ETI -> TIMER1_CH0,TIMER1_ETI
            for c in range(15):
                if "_CH%dTIMER" % c in input_str_or_float:
                    input_str_or_float = input_str_or_float.replace("_CH%dTIMER" % c, "_CH%d,TIMER" % c, 1)
            # general fixups where we're too lazy to do complicated parsing / reconstructing
            # if key is found, it will be replaced with the value in the dict.
            general_replacements = {
                "USART1_T(2)X": "USART1_TX(2)",
                "SPI1_NSS,EVENTOUT": "SPI1_NSS/EVENTOUT"
            }
            for k in general_replacements.keys():
                if k in input_str_or_float:
                    input_str_or_float = input_str_or_float.replace(k, general_replacements[k], 1)

            return input_str_or_float
        else: 
            # convert float NaN to more easily handable python None value
            return None if is_nan(input_str_or_float) else input_str_or_float

    @staticmethod
    def get_pinmap_for_pdf(datasheet_pdf_path: str) -> GD32PinMap:
        # go through all alternate function pages as descriped
        datasheet_info = identify_datasheet(datasheet_pdf_path)
        if datasheet_info is None: 
            print(f"Failed to find datasheet info for filename {path.basename(datasheet_pdf_path)}.")
            print("Known datasheets: " + ",".join(known_datasheets_infos.keys()))
            exit(0)
        # maps from subseries to list of dictionaries
        pinmaps: Dict[str, Dict[str, GD32Pin]] = dict()
        # alternate function mapping exists *ONCE* per datasheet for a SPL family type B datasheet.
        # can be accumulated all into one object
        all_alternate_func_infos: Dict[str, GD32Pin] = dict()
        # maps from subseries to package type
        package_info: Dict[str, str] = dict()
        for af_page in datasheet_info.alternate_funcs:
            dataframe = GD32DatasheetParser.get_dataframe_for_pdf_pages(datasheet_pdf_path, af_page)
            alternate_func_infos = GD32DatasheetParser.process_af_dataframe(dataframe, datasheet_info, af_page)
            all_alternate_func_infos.update(alternate_func_infos)
        for pindef_page in datasheet_info.pin_defs:
            dataframe = GD32DatasheetParser.get_dataframe_for_pdf_pages(datasheet_pdf_path, pindef_page)
            add_funcs = GD32DatasheetParser.process_add_funcs_dataframe(dataframe, datasheet_info, pindef_page)
            # we don't have a "pin alternative functions" page, we have to extract it from the last column text
            alt_and_remaps: Dict[str, GD32Pin] = dict()
            if datasheet_info.family_type == "A":
                alt_and_remaps = GD32DatasheetParser.process_alts_and_remaps(dataframe, datasheet_info, pindef_page)
            if pindef_page.subseries not in pinmaps:
                pinmaps[pindef_page.subseries] = dict()
            # merge into one dictionary (alt_and_remaps)
            for pin_name, gd32pin in add_funcs.items():
                if pin_name in alt_and_remaps:
                    for f in gd32pin.pin_functions:
                        alt_and_remaps[pin_name].add_func(f)
                else:
                    alt_and_remaps[pin_name] = gd32pin
            pinmaps[pindef_page.subseries].update(alt_and_remaps)
            package_info[pindef_page.subseries] = pindef_page.package

        # All subseries and the AF mapping has been parsed.
        # Propagate AF pin info to subseries pin info.
        for pin_name, gd32pin in all_alternate_func_infos.items():
            for subseries in pinmaps.keys():
                # only add function to it if this pin exists in this subseries
                # otherwise do not create it.
                if pin_name in pinmaps[subseries]:
                    for f in gd32pin.pin_functions:
                        pinmaps[subseries][pin_name].add_func(f)

        # generate all sub series maps
        subseries_pin_maps: Dict[str, GD32SubseriesPinMap] = dict()
        for subseries in pinmaps.keys():
            subseries_pin_maps[subseries] = GD32SubseriesPinMap(
                datasheet_info.series,
                subseries,
                package_info[subseries],
                datasheet_info,
                pinmaps[subseries]
            )

        for k in subseries_pin_maps:
            fam = subseries_pin_maps[k]
            print("Subfamiliy \"%s\" (%s) has %s GPIO pins" %(fam.subseries, fam.package, len(fam.pin_map)))
            print(",".join(fam.pin_map.keys()))

        total_pinmap = GD32PinMap(
            datasheet_info.series,
            datasheet_info,
            subseries_pin_maps
        )
        print("Parsed PDF \"%s\" and extracted %d pin infos." % (
            path.basename(datasheet_pdf_path), 
            sum([len(pmap.pin_map.keys()) for pmap in total_pinmap.subseries_pinmaps.values()])))
        return total_pinmap

    def get_dataframe_for_pdf_pages(datasheet_pdf_path: str, pages_info: DatasheetPageParsingInfo) -> DataFrame:
        # lattice is important, can't correctly parse data otherwise
        area_quirk = pages_info.get_quirks_of_type(ParseUsingAreaQuirk)
        area = None
        if len(area_quirk) == 1:
            the_quirk: ParseUsingAreaQuirk = area_quirk[0]
            area = the_quirk.area
        print("Parsing PDF \"%s\" pages %s.." % (datasheet_pdf_path, str(pages_info.page_range)))
        dfs : DataFrame = tb.read_pdf(datasheet_pdf_path, pages=pages_info.page_range, lattice=True, stream=False, area=area) 
        if len(dfs) >= 1:
            dfs = pd.concat(dfs)
        else:
            print("Failed to extract one datatable from PDF")
            return False
        # check if we need to condense columns
        for q in pages_info.get_quirks_of_type(CondenseColumnsQuirk):
            dfs = GD32DatasheetParser.dataframe_condense_columns(dfs, q)
        else:
            # if no elements in for loop, do generic cleanup
            dfs = GD32DatasheetParser.cleanup_dataframe(dfs)

        print(dfs)
        print(type(dfs))
        return dfs

    def dataframe_condense_columns(dfs: DataFrame, quirk: CondenseColumnsQuirk) -> DataFrame:
        # fix for parsing quirk where colums have NaNs in between 
        # and are thus shifted 
        # 0 NaN AF0 AF1 AF2 AF3 NaN AF4 AF5 AF6 AF7
        # we just move over the column names and drop all NaN columns
        row = quirk.row
        print("Condensing columns on row %d" % row)
        print("Before:")
        print(dfs)
        # get first row, but skip first element (always NaN)
        first_row = list(dfs.iloc[row,])[1:]
        print(first_row)
        first_row_no_nans = [x for x in first_row if not is_nan(x)]
        # expand with NaNs at the end
        first_row_no_nans.extend([math.nan] * (len(first_row) - len(first_row_no_nans)))
        # add back first element
        first_row_no_nans.insert(0, math.nan)
        print(first_row_no_nans)
        dfs.iloc[row] = first_row_no_nans
        #print(dfs)
        dfs = dfs.dropna(axis=1, how='all')
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
            # drop last column if it's all NaNs
            if all([is_nan(x) for x in dfs.iloc[:, -1]]):
                dfs = dfs.drop([dfs.columns[-1]], axis=1)
        return dfs

    def remove_newlines(inp):
        if isinstance(inp, str):
            return inp.replace("\r", "")
        else:
            return inp

    def analyze_additional_funcs_string(inp:str) -> List[str]: 
        # find where it says "additional".
        # due to bad parsing when the boundary is close to the letters,
        # the parser swallows the first letter. of the line. 
        # however, since all additional functions fit in one line (observed for now)
        # meaning no letter are swallowed of additional function signal names,
        # it's acceptabale to also only look for "dditional". 
        # Stream-based parsing instead of lattice-based parsing does not have this
        # problem, however, the data is weirdly formatted so that other cleanup
        # techniques are needed again...
        add_start = inp.find("dditional: ")
        # check if anyhting was found
        if add_start == -1:
            return list()
        # get the rest of the string after that
        inp = inp[add_start + len("dditional: "):]
        arr = inp.split(",")
        arr = [x.strip() for x in arr]
        return arr

    # Input: Last column description text
    # Output: List of "alternate" functions, List of "remap" functions
    def analyze_alternate_and_remap_funcs_string(inp:str) -> Tuple[List[str], List[str]]: 
        alt_start = inp.find("lternate: ")
        remap_start = inp.find("Remap:")
        # check if anyhting was found
        if alt_start == -1 and remap_start == -1:
            return (list(), list())
        # get the rest of the string after that
        if remap_start == -1:
            alt_inp = inp[alt_start + len("lternate: "):]
        else:
            alt_inp = inp[alt_start + len("lternate: "):remap_start]
        alt_arr = alt_inp.split(",")
        alt_arr = [x.strip() for x in alt_arr]
        remap_arr = []
        if remap_start != -1:
            remap_inp = inp[remap_start + len("Remap:"):]
            remap_arr = remap_inp.split(",")
            remap_arr = [x.strip() for x in remap_arr]
        return alt_arr, remap_arr

    # Applies corrections regarding shorthand name for
    # signals names like "ADC0123_IN1" that are actually
    # multiple signals. 
    def cleanup_funcs_array(inp: List[str]) -> List[str]:
        l = list()
        for f in inp:
            if f.startswith("ADC") and f.count("_")  == 1:
                # could be "ADC012_IN1", "ADC01_IN5" etc
                # we have to add individually "ADC0", "ADC1", "ADC2".
                periph_part, signal_part = f.split("_")
                periph_part = periph_part.replace("ADC", "", 1)
                # iterate through each char
                for c in periph_part:
                    l.append("ADC" + str(c) + "_" + signal_part)
            else:
                l.append(f)
        return l

    # removes - and () parts (footnotes)
    def strip_pinname(pin_name:str):
        if "-" in pin_name:
            pin_name = pin_name[0 : pin_name.index("-")]
        # to get rid of "PA9(6)" style pin names with footnotes
        if "(" in pin_name:
            pin_name = pin_name[0 : pin_name.index("(")]
        return pin_name

    def process_add_funcs_dataframe(dfs: DataFrame, datasheet_info: DatasheetParsingInfo, pages_info: DatasheetPinDefPageParsingInfo) -> Dict[str, GD32Pin]:
        additional_funcs: Dict[str, GD32Pin] = dict()
        for i, j in dfs.iterrows():
            # data row
            pin_row = list(j)
            pin_name = GD32DatasheetParser.remove_newlines(pin_row[0])
            if is_nan(pin_name) or pin_name == "Pin Name" or not pin_name.startswith("P"):
                print("Skipping empty line because pin is not there.")
                continue
            pin_name = GD32DatasheetParser.strip_pinname(pin_name)
            last_column: str = j[len(j) - 1]
            last_column = last_column.replace("\r", " ")
            # apply overwrite quirk
            overwrite_quirk = pages_info.get_quirks_of_type(OverwritePinDescriptionQuirk)
            if len(overwrite_quirk) == 1:
                overwrite_quirk: OverwritePinDescriptionQuirk = overwrite_quirk[0]
                if overwrite_quirk.pin_name == pin_name:
                    last_column = overwrite_quirk.pin_description
            add_funcs_arr = GD32DatasheetParser.analyze_additional_funcs_string(last_column)
            print("Pin %s Add. Funcs: %s" % (pin_name, str(add_funcs_arr)))
            additional_funcs[pin_name] = GD32Pin(pin_name, [GD32PinFunction(sig, None, None, None, pages_info.subseries, pages_info.package) for sig in add_funcs_arr])
        print(additional_funcs)
        return additional_funcs

    # input: signal name with possible footnote
    # output: cleaned signal name, footnote
    def analyze_footnote(inp:str) -> Tuple[str, str]:
        if "(" in inp and ")" in inp:
            sig_name = inp[0:inp.index("(")]
            func_footnode_part = inp[inp.index("("):]
            # strip first and last char
            footnote = func_footnode_part[1:-1]
            #print("Got func with footnote. name = %s footnote = %s"  % (str(sig_name), str(func_footnode_part)))
            return sig_name, footnote
        else:
            return inp, None

    def process_alts_and_remaps(dfs: DataFrame, datasheet_info: DatasheetParsingInfo, pages_info: DatasheetPinDefPageParsingInfo) -> Dict[str, GD32Pin]:
        parsed_pins: Dict[str, GD32Pin] = dict()
        for i, j in dfs.iterrows():
            # data row
            pin_row = list(j)
            pin_name = GD32DatasheetParser.remove_newlines(pin_row[0])
            if is_nan(pin_name) or pin_name == "Pin Name" or not pin_name.startswith("P"):
                print("Skipping empty line because pin is not there.")
                continue
            pin_name = GD32DatasheetParser.strip_pinname(pin_name)
            last_column: str = j[len(j) - 1]
            last_column = last_column.replace("\r", " ")
            # apply overwrite quirk
            overwrite_quirk = pages_info.get_quirks_of_type(OverwritePinDescriptionQuirk)
            if len(overwrite_quirk) == 1:
                overwrite_quirk: OverwritePinDescriptionQuirk = overwrite_quirk[0]
                if overwrite_quirk.pin_name == pin_name:
                    last_column = overwrite_quirk.pin_description
            alternate_arr, remap_arr = GD32DatasheetParser.analyze_alternate_and_remap_funcs_string(last_column)
            alternate_arr = GD32DatasheetParser.cleanup_funcs_array(alternate_arr)
            remap_arr = GD32DatasheetParser.cleanup_funcs_array(remap_arr)
            print("Pin %s Alt. Funcs: %s Remap funcs: %s" % (pin_name, str(alternate_arr), str(remap_arr)))
            parsed_pins[pin_name] = GD32Pin(pin_name, [
                GD32PinFunction(GD32DatasheetParser.analyze_footnote(sig)[0], 
                None, 
                GD32DatasheetParser.analyze_footnote(sig)[1], 
                pages_info.footnotes_device_availability, 
                pages_info.subseries, pages_info.package, False) for sig in alternate_arr
            ] + [
                GD32PinFunction(GD32DatasheetParser.analyze_footnote(sig)[0], 
                None, 
                GD32DatasheetParser.analyze_footnote(sig)[1], 
                pages_info.footnotes_device_availability,
                pages_info.subseries, pages_info.package, True) for sig in remap_arr
            ])
        print(parsed_pins)
        return parsed_pins

    def process_af_dataframe(dfs: DataFrame, datasheet_info: DatasheetParsingInfo, pages_info: DatasheetAFPageParsingInfo) -> Dict[str, GD32Pin]:
        parser_result_alternate_functions = []
        parser_result_pins: Dict[str, GD32Pin] = dict()
        for i, j in dfs.iterrows():
            # debug info
            if False:
                print("i")
                print(i)
                print("j")
                print(j)
            # first row gives us list of alternate functions (AF0..AF11) in the table!
            if i == 0:
                af_list_quirks: List[OverwriteAdditionFunctionsList] = pages_info.get_quirks_of_type(OverwriteAdditionFunctionsList)
                if len(af_list_quirks) == 1:
                    parser_result_alternate_functions = af_list_quirks[0].af_list
                else:
                    alternate_funcs = filter_nans(j)
                    print(alternate_funcs)
                    if any([not x.startswith("AF") for x in alternate_funcs]):
                        print("Fail: These are not the alternate function descriptions: " + str(alternate_funcs))
                    else:
                        parser_result_alternate_functions = alternate_funcs
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
                pin_alternate_funcs = [GD32DatasheetParser.filter_string(x) for x in pin_alternate_funcs]
                #print("[Before adjustment] Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
                print("Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
                af_list: List[GD32PinFunction] = list()
                for ind, func in enumerate(pin_alternate_funcs):
                    af_name = parser_result_alternate_functions[ind]
                    # check if individual breakup is needed
                    funcs = None
                    if func is None: 
                        continue
                    if "/" in func:
                        funcs = func.split("/")
                    else:
                        funcs = [func]
                    for f in funcs:
                        # check if we need to extra footnotes
                        sig_name, footnote = GD32DatasheetParser.analyze_footnote(f)
                        af_list.append(GD32PinFunction(sig_name, get_trailing_number(af_name), footnote, pages_info.footnotes_device_availability))
                print(af_list)
                parser_result_pins[pin_name] = GD32Pin(pin_name, af_list)
        print("Parsed all %d pins." % len(parser_result_pins))
        return parser_result_pins
