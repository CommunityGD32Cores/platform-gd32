from typing import Dict, List

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
    def __init__(self, signal_name:str, af_number:int, footnote:str, footnote_device_availability:Dict[str,List[str]]) -> None:
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
