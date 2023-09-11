import sys, os, re
from typing import Dict, List, Optional

from known_datasheets import remapper_info
from parsing_info import FootnoteAvailabilityInfo, RemappingMacro

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from board_generator import GD32MCUInfo

class GD32PinFunction:
    def __init__(self, pin_name: str, signal_name: str, af_number: int, footnote: str, footnote_device_availability: Dict[str, FootnoteAvailabilityInfo], family_type: str, subseries: str = None, package: str = None, needs_remap: bool = False) -> None:
        self.pin_name = pin_name
        self.signal_name = signal_name
        self.family_type = family_type
        self.footnote = footnote
        self.footnote_device_availability = footnote_device_availability
        self.footnote_resolved = None
        if self.footnote_device_availability is not None:
            if self.footnote in self.footnote_device_availability:
                self.footnote_resolved = self.footnote_device_availability[self.footnote]
        self.peripheral:str = ""
        self.subfunction:str = None
        # can be "None" if it's a regular "additional function" or an alternate function on with SPL family A
        self.af_number:Optional[int] = af_number
        self.subseries = subseries
        self.package = package
        self.needs_remap = needs_remap
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

    def has_af_number(self):
        return self.af_number is not None
    
    def remapping_macros(self, mcu: GD32MCUInfo) -> List[str]:
        try:
            scopes = remapper_info[mcu.spl_series.lower()][self.pin_name][self.signal_name]
            validScopes: List[RemappingMacro] = []
            for scope in scopes:
                if scope.include_packages and not any(re.search(s, self.package, re.RegexFlag.IGNORECASE) for s in scope.include_packages):
                    continue 
                if scope.include_subseries and not any(re.search(s, mcu.sub_series, re.RegexFlag.IGNORECASE) for s in scope.include_subseries):
                    continue
                if scope.include_mcus and not any(re.search(s, mcu.name, re.RegexFlag.IGNORECASE) for s in scope.include_mcus):
                    continue
                validScopes.append(scope)

            if not len(validScopes): raise
            
            print(f"MATCH for {self.pin_name} ({self.signal_name}) -> {[s.replacement_macro for s in validScopes]}")
            return [("DISABLE_" if s.disable else "") + s.replacement_macro for s in validScopes]
        except:
            print(f"No remapping match found for {self.pin_name} ({self.signal_name})")
        
        return []

class GD32Pin:
    def __init__(self, pin_name: str, pin_functions: List[GD32PinFunction]=None) -> None:
        self.pin_name = pin_name
        self.pin_functions = pin_functions
    def __repr__(self) -> str:
        return f"GD32Pin(pin={self.pin_name}, funcs={str(self.pin_functions)}"

    def add_func(self, pin_func:GD32PinFunction):
        self.pin_functions.append(pin_func)

    @staticmethod
    def natural_sort_key(pin_name):
        key = 0
        # Matches PA1, PA1_ALT1, PORTA_1, PORTA_1_ALT1
        m = re.match("P(ORT)?([A-Z])_?([0-9]+)_?(ALT([0-9]))?", pin_name)
        mg = m.groups()
        key = "%s%02d%s" % (mg[1], int(mg[2]), mg[4] or "0")
        return key 