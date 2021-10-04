import math
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import pandas as pd
try:
    import tabula as tb
except ImportError:
    print("Could not import pdfminer. Please 'pip install pdfminer.six' first!")
    exit(-1)

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
        "family_type": "B"
    }
}

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
            input_str_or_float = input_str_or_float.replace("I2S", "/I2S")
            # cleanup for double forward slash
            input_str_or_float = input_str_or_float.replace("//", "/")
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
    combine_duplicate_columns = False
    if len(dfs.columns) > 11:
        print("Need cleanup") 
        combine_duplicate_columns = True
        # source_col_loc = dfs.columns.get_loc('Unnamed: 1') # column position starts from 0
        #dfs['Unnamed: 1'] = dfs.iloc[:,source_col_loc+1:source_col_loc+2].apply(
        #    lambda x: " BLAH ".join(x.astype(str)), axis=1)

    #print(dfs["Unnamed: 1"])
    # for special pages where the parser fails: combine columns
    print(dfs)
    print(type(dfs))

    parser_result = {
        "alternate_functions": [],
        "pins": []
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
            if is_nan(pin_name):
                print("Skipping empty line because pin is not there.")
                continue
            if combine_duplicate_columns:
                pin_alternate_funcs = pin_row[2::]
            else:
                pin_alternate_funcs = pin_row[1::]
            pin_alternate_funcs = [filter_string(x) for x in pin_alternate_funcs]
            #print("[Before adjustment] Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
            if combine_duplicate_columns:
                new_list = []
                # delete every even element - they are all "None" and were duplicated / stretched by the parser
                for i in range(0, len(pin_alternate_funcs), 2):
                    left_elem = pin_alternate_funcs[i]
                    if i + 1 < len(pin_alternate_funcs):
                        right_elem = pin_alternate_funcs[i + 1]
                        new_list.append(left_elem if left_elem != None else right_elem)
                pin_alternate_funcs = new_list
            print("Got pin: %s funcs %s" % (str(pin_name), str(pin_alternate_funcs)))
            #for pin_func in pin_alternate_funcs:
            #    print(pin_func)
            #if i == 3:
            #    exit(0)
            #for x in j:
            #    print(x)
if __name__ == "__main__":
    main_func()
