from typing import List

class DatasheetPageParsingQuirk:
    pass

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

class OverwriteAdditionFunctionsList(DatasheetPageParsingQuirk):
    def __init__(self, af_list: List[str]) -> None:
        super().__init__()
        self.af_list = af_list

class CondenseColumnsQuirk(DatasheetPageParsingQuirk):
    def __init__(self, row=0) -> None:
        super().__init__()
        self.row = row