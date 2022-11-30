from typing import Dict, List, Optional

class GD32PinFunction:
    def __init__(self, signal_name: str, af_number: int, footnote: str, footnote_device_availability: Dict[str, List[str]], subseries: str = None, package: str = None, needs_remap: bool = False) -> None:
        self.signal_name = signal_name
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

class GD32Pin:
    def __init__(self, pin_name: str, pin_functions: List[GD32PinFunction]=None) -> None:
        self.pin_name = pin_name
        self.pin_functions = pin_functions
    def __repr__(self) -> str:
        return f"GD32Pin(pin={self.pin_name}, funcs={str(self.pin_functions)}"

    def add_func(self, pin_func:GD32PinFunction):
        self.pin_functions.append(pin_func)