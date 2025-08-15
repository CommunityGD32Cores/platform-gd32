from enum import Enum
from typing import Dict, List, Tuple
import re
from pin_definitions import GD32Pin, GD32PinFunction
from parsing_info import DatasheetParsingInfo

class GD32PinCriteriaType(Enum):
    PERIPHERAL_STARTS_WITH = 0 
    PIN_SUB_FUNCTION = 1 
    PERIPHAL_AND_PIN_SUB_FUNCTION = 2
    SIGNAL_CONTAINS = 3

class GD32PinCriteria:
    def __init__(self, criteria_type: GD32PinCriteriaType, criteria_values: List[any]) -> None:
        self.type = criteria_type
        self.values = criteria_values

class GD32SubseriesPinMap:
    def __init__(self, series: str, subseries:str, package:str, datasheet_info:DatasheetParsingInfo, pin_map: Dict[str, GD32Pin]) -> None:
        self.series = series
        self.subseries = subseries
        self.package = package
        self.datasheet_info = datasheet_info
        self.pin_map = pin_map

    # to be called after all pin defs were parsed
    # on SPL family type B, there is "pin alternate functions" map available.
    def add_alternate_func_to_pin(self, pin_name:str, func: GD32PinFunction):
        # we assume that at this point, all the pin definitions were already loaded
        # so we get an AF for a pin that doesn't exist for this series, we reject it
        if pin_name not in self.pin_map:
            return
            #self.pin_map[pin_name] = GD32Pin(pin_name, [func])
        else:
            self.pin_map[pin_name].pin_functions.append(func)

class GD32PinMap:
    def __init__(self, series: str, datasheet_info:DatasheetParsingInfo, subseries_pinmaps: Dict[str, GD32SubseriesPinMap]) -> None:
        self.series = series
        self.datasheet_info = datasheet_info
        # maps from e.g. "GD32F190Cx" to all total pins available
        # usually parsed from the section that also additional functions 
        # are parsed from.
        if subseries_pinmaps is None: 
            subseries_pinmaps = dict()
        self.subseries_pinmaps = subseries_pinmaps

    def get_subfamily_for_device_name(self, device_name: str) -> str:
        # try to identify the family name
        matching_subfamilies = list(filter(
            lambda fam_name: GD32PinMap.devicename_matches_constraint(device_name, fam_name),
            self.subseries_pinmaps.keys()
        ))
        if len(matching_subfamilies) == 0:
            print("Failed to identify device \"%s\" to be in %s" % (device_name, str(self.subseries_pinmaps.keys())))
            return None
        return matching_subfamilies[0]

    def get_pinmap_for_device_name(self, device_name: str) -> GD32SubseriesPinMap:
        # try to identify the family name
        matching_subfamiliy_name = self.get_subfamily_for_device_name(device_name)
        # no matches?
        if matching_subfamiliy_name == None: 
            return None
        matching_subfamiliy = self.subseries_pinmaps[matching_subfamiliy_name]
        return matching_subfamiliy

    def pin_is_available_for_device(self, pin_name:str, device_name:str):
        if device_name == None:
            # do not apply any filter
            return True
        matching_subfamiliy: GD32SubseriesPinMap = self.get_pinmap_for_device_name(device_name)
        if matching_subfamiliy is None:
            # couldn't identify
            return False
        ret = pin_name in matching_subfamiliy.pin_map.keys()
        print("Pin %s in family %s (%s) --> %s" % (pin_name, matching_subfamiliy.subseries, matching_subfamiliy.package, ret))
        return ret

    # Examples: devicename = GD32F190T6, constraint = GD32F190T8 => false
    #           devicename = GD32F190T6, constraint = GD32F190T6 => true
    #           devicename = GD32F190T6, constraint = GD32F190Rx => false
    #           devicename = GD32F190T6, constraint = GD32F190Tx => true
    @staticmethod
    def devicename_matches_constraint(device_name:str, constraint:str) -> bool:
        if "x" not in constraint and constraint.isalnum(): # may be regex
            ret = device_name == constraint
        else: 
            # replace x with "can be any character" regex
            regex_str = constraint.replace("x", ".")
            ret = re.match(regex_str, device_name) != None
        #print("Checked constraint \"%s\" against devicename \"%s\" -> %s" % (constraint, device_name, str(ret)))
        return ret

    @staticmethod
    def does_pinfunction_pass_filter(func: GD32PinFunction, device_name:str) -> bool:
        # we can't decide without a devicename, so we'll let anyhting pass
        if device_name is None: 
            return True
        # no device constraint per footnote? Then this passes.
        if func.footnote_resolved == None:
            return True
        # subseries present? check against that.
        if func.subseries is not None:
            if not GD32PinMap.devicename_matches_constraint(device_name, func.subseries):
                return False
        if func.footnote_resolved.signal_filter:
            if func.signal_name.startswith(func.footnote_resolved.signal_filter):
                return func.footnote_resolved.signal_inclusive == any([GD32PinMap.devicename_matches_constraint(device_name, dev_constraint) for dev_constraint in func.footnote_resolved.device_filter])
            else:
                return True
        else:
            return any([GD32PinMap.devicename_matches_constraint(device_name, dev_constraint) for dev_constraint in func.footnote_resolved.device_filter])

    def search_pins_for_function(self, pin_criteria:List[GD32PinCriteria], filter_device_name:str=None) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        results: List[Tuple[GD32Pin, GD32PinFunction]] = list()
        pin_maps_to_search: List[GD32SubseriesPinMap]
        if filter_device_name is None:
            pin_maps_to_search = self.subseries_pinmaps
        else:
            pin_maps_to_search = [self.get_pinmap_for_device_name(filter_device_name)]
        for pin_map in pin_maps_to_search:
            for pin in pin_map.pin_map.values():
                # search through all functions
                for function in pin.pin_functions:
                    # all pin_criteria are AND, but values are OR:
                    # PERIPHERAL_STARTS_WITH("A" OR "B") AND SIGNAL_CONTAINS("C")
                    all_criteria_passed = True
                    for criteria in pin_criteria:
                        criteria_passed = False
                        if criteria.type == GD32PinCriteriaType.PERIPHERAL_STARTS_WITH:
                            if any(function.peripheral.startswith(value) for value in criteria.values):
                                criteria_passed = True
                        elif criteria.type == GD32PinCriteriaType.PIN_SUB_FUNCTION:
                            if any((function.subfunction is not None and value in function.subfunction) for value in criteria.values):
                                criteria_passed = True
                        elif criteria.type == GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION:
                            if any((function.peripheral.startswith(value[0]) and (function.subfunction is not None and value[1] in function.subfunction)) for value in criteria.values):
                                criteria_passed = True
                        elif criteria.type == GD32PinCriteriaType.SIGNAL_CONTAINS:
                            if any((value in function.signal_name) for value in criteria.values):
                                criteria_passed = True
                        all_criteria_passed &= criteria_passed
                    if all_criteria_passed: 
                        results.append((pin, function))
        results = list(filter(lambda p_func_tuple: GD32PinMap.does_pinfunction_pass_filter(p_func_tuple[1], filter_device_name), results))
        results = list(filter(lambda p_func_tuple: self.pin_is_available_for_device(p_func_tuple[0].pin_name, filter_device_name), results))
        results.sort(key=lambda x: GD32Pin.natural_sort_key(x[0].pin_name) + x[1].signal_name)
        return results
    