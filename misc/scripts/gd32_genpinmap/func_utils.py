import re
import math
from pandas import Series

def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

def is_nan(number_or_obj):
    return type(number_or_obj) == float and math.isnan(number_or_obj)

def filter_nans(list_input: Series) -> list:
    return [x for x in list_input if not is_nan(x) and x != ""]
