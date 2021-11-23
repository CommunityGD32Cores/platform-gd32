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

from parsing_quirks import OverwritePinAlternateInfoQuirk, OverwritePinAdditionalInfoQuirk, ParseUsingAreaQuirk, OverwriteAdditionFunctionsList, CondenseColumnsQuirk
from func_utils import get_trailing_number, filter_nans, is_nan, print_big_str
from parsing_info import DatasheetAFPageParsingInfo, DatasheetPageParsingInfo, DatasheetParsingInfo, DatasheetPinDefPageParsingInfo
from pin_definitions import GD32AdditionalFunc, GD32AdditionalFuncFamiliy, GD32AlternateFunc, GD32Pin
from pin_map import GD32PinMap
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
        pinmaps: List[GD32PinMap] = list()
        for af_page in datasheet_info.alternate_funcs:
            dataframe = GD32DatasheetParser.get_dataframe_for_pdf_pages(datasheet_pdf_path, af_page)
            pin_map = GD32DatasheetParser.process_af_dataframe(dataframe, datasheet_info, af_page)
            pinmaps.append(pin_map)
        additional_functions: List[GD32AdditionalFuncFamiliy] = list()
        for pindef_page in datasheet_info.pin_defs:
            dataframe = GD32DatasheetParser.get_dataframe_for_pdf_pages(datasheet_pdf_path, pindef_page)
            add_func_family = GD32DatasheetParser.process_add_funcs_dataframe(dataframe, datasheet_info, pindef_page)
            additional_functions.append(add_func_family)
        # merge all pinmap dictionary into the first object
        first_pinmap = pinmaps[0]
        for i in range(1, len(pinmaps)):
            first_pinmap.pin_map.update(pinmaps[i].pin_map)
        # merge all additional funcs families into first pinmap
        for add_func in additional_functions:
            GD32DatasheetParser.merge_additional_funcs_into_pinmap(add_func, first_pinmap)
        # merge all additional funcs families into a full one for the subfamiliy
        pins_per_subdev_family_dict: Dict[str, GD32AdditionalFuncFamiliy] = dict()
        for add_func in additional_functions:
            subfam = add_func.subseries
            if subfam not in pins_per_subdev_family_dict:
                pins_per_subdev_family_dict[subfam] = add_func
            else:
                pins_per_subdev_family_dict[subfam].additional_funcs.update(add_func.additional_funcs)
        first_pinmap.pins_per_subdevice_family = pins_per_subdev_family_dict
        for k in pins_per_subdev_family_dict:
            fam = pins_per_subdev_family_dict[k]
            print("Subfamiliy \"%s\" (%s) has %s GPIO pins" %(fam.subseries, fam.package, len(fam.additional_funcs)))
            print(",".join(fam.additional_funcs.keys()))
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

    def print_parsing_result_json(res:dict):
        as_json = json.dumps(res, indent=2, default=lambda o: o.__dict__)
        print_big_str(as_json)

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
            overwrite_quirk = pages_info.get_quirks_of_type(OverwritePinAdditionalInfoQuirk)
            if len(overwrite_quirk) == 1:
                overwrite_quirk: OverwritePinAdditionalInfoQuirk = overwrite_quirk[0]
                if overwrite_quirk.pin_name == pin_name:
                    last_column = overwrite_quirk.additional_funcs_str
            add_funcs_arr = GD32DatasheetParser.analyze_additional_funcs_string(last_column)
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
                af_list_quirks: List[OverwriteAdditionFunctionsList] = pages_info.get_quirks_of_type(OverwriteAdditionFunctionsList)
                if len(af_list_quirks) == 1:
                    parser_result["alternate_functions"] = af_list_quirks[0].af_list
                else:
                    alternate_funcs = filter_nans(j)
                    print(alternate_funcs)
                    if any([not x.startswith("AF") for x in alternate_funcs]):
                        print("Fail: These are not the alternate function descriptions: " + str(alternate_funcs))
                    else:
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
                pin_alternate_funcs = [GD32DatasheetParser.filter_string(x) for x in pin_alternate_funcs]
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
                    for f in funcs:
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
