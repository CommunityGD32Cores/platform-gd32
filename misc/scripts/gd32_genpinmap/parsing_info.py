from typing import List, Dict
from parsing_quirks import DatasheetPageParsingQuirk

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
    def __init__(self, page_range: List[int], subseries:str, package:str, quirks:List[DatasheetPageParsingQuirk]=None, footnotes_device_availablity: Dict[str, str]=None) -> None:
        super().__init__(page_range, quirks)
        self.subseries = subseries
        self.package = package
        self.footnotes_device_availability = footnotes_device_availablity

class DatasheetParsingInfo:
    def __init__(self, alternate_funcs: List[DatasheetAFPageParsingInfo], pin_defs: List[DatasheetPinDefPageParsingInfo], series:str, family_type:str, family_name:str=None) -> None:
        self.alternate_funcs = alternate_funcs
        self.pin_defs = pin_defs
        self.series = series 
        self.family_type = family_type
        self.family_name = family_name