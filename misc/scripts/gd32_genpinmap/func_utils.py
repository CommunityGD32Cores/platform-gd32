import re
import math
from pandas import Series
import sys

def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

def is_nan(number_or_obj):
    return type(number_or_obj) == float and math.isnan(number_or_obj)

def filter_nans(list_input: Series) -> list:
    return [x for x in list_input if not is_nan(x) and x != ""]

def print_big_str(res:str):
    # string is large, breaks console. print block-wise
    n = 5*1024
    for x in [res[i:i+n] for i in range(0, len(res), n)]:
        print(x, end="", flush=True)
        sys.stdout.flush()

def atoi(text:str):
    return int(text) if text.isdigit() else text

def natural_keys(text:str):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def remove_last_comma(text:str) -> str: 
    return "".join(text.rsplit(",", 1))