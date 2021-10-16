from os import device_encoding
from typing import Dict, List, Tuple
import re
from pin_definitions import GD32AdditionalFunc, GD32AlternateFunc, GD32Pin, GD32AdditionalFuncFamiliy

class GD32PinMap:
    def __init__(self, series: str, datasheet_info, pin_map: Dict[str, GD32Pin], pins_per_subdevice_family=None) -> None:
        self.series = series
        self.datasheet_info = datasheet_info
        self.pin_map: Dict[str, GD32Pin] = pin_map
        # maps from e.g. "GD32F190Cx" to all total pins available
        # usually parsed from the section that also additional functions 
        # are parsed from.
        if pins_per_subdevice_family is None: 
            pins_per_subdevice_family = dict()
        self.pins_per_subdevice_family: Dict[str, GD32AdditionalFuncFamiliy] = pins_per_subdevice_family

    CRITERIA_PERIPHERAL_STARTS_WITH = 0
    CRITERIA_PIN_SUB_FUNCTION = 1
    CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION = 2

    def search_pins_for_any_func(self, criteria_type, criteria_value) -> List[Tuple[GD32Pin, object]]:
        results_af = self.search_pins_for_af(criteria_type, criteria_value)
        results_ad = self.search_pins_for_add_func(criteria_type, criteria_value)
        return results_af + results_ad

    def get_subfamily_for_device_name(self, device_name: str) -> str:
        # try to identify the family name
        matching_subfamilies = list(filter(
            lambda fam_name: GD32PinMap.devicename_matches_constraint(device_name, fam_name),
            self.pins_per_subdevice_family.keys()
        ))
        if len(matching_subfamilies) == 0:
            print("Failed to identify device \"%s\" to be in %s" % (device_name, str(self.pins_per_subdevice_family.keys())))
            return None
        return matching_subfamilies[0]

    def pin_is_available_for_device(self, pin_name:str, device_name:str):
        if device_name == None:
            # do not apply any filter
            return True
        # try to identify the family name
        matching_subfamiliy_name = self.get_subfamily_for_device_name(device_name)
        if matching_subfamiliy_name == None: 
            return False
        matching_subfamiliy = self.pins_per_subdevice_family[matching_subfamiliy_name]
        ret = pin_name in matching_subfamiliy.additional_funcs.keys()
        print("Pin %s in family %s (%s) --> %s" % (pin_name, matching_subfamiliy.subseries, matching_subfamiliy.package, ret))
        return ret

    # Examples: devicename = GD32F190T6, constraint = GD32F190T8 => false
    #           devicename = GD32F190T6, constraint = GD32F190T6 => true
    #           devicename = GD32F190T6, constraint = GD32F190Rx => false
    #           devicename = GD32F190T6, constraint = GD32F190Tx => true
    @staticmethod
    def devicename_matches_constraint(device_name:str, constraint:str) -> bool:
        if "x" not in constraint:
            ret = device_name == constraint
        else: 
            # replace x with "can be any character" regex
            regex_str = constraint.replace("x", ".")
            ret = re.match(regex_str, device_name) != None
        print("Checked constraint \"%s\" against devicename \"%s\" -> %s" % (constraint, device_name, str(ret)))
        return ret

    @staticmethod
    def does_af_pass_filter(af: GD32AlternateFunc, device_name:str) -> bool:
        # we can't decide without a devicename, so we'll let anyhting pass
        if device_name is None: 
            return True
        # no device constraint per footnote? Then this passes.
        if af.footnote_resolved == None:
            return True
        else:
            return any([GD32PinMap.devicename_matches_constraint(device_name, dev_constraint) for dev_constraint in af.footnote_resolved])

    @staticmethod
    def does_ad_pass_filter(ad: GD32AdditionalFunc, device_name:str) -> bool:
        # we can't decide without a devicename, so we'll let anyhting pass
        if device_name is None: 
            return True
        # all additional functions were saved with their sub-series.
        else:
            return GD32PinMap.devicename_matches_constraint(device_name, ad.subseries)

    def search_pins_for_add_func(self, criteria_type, criteria_value, filter_device_name:str=None) -> List[Tuple[GD32Pin, GD32AdditionalFunc]]:
        results = list()
        for p in self.pin_map.values():
            # search through all additional functions
            for additional_func in p.additional_functions:
                if criteria_type == GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH:
                    if (additional_func.peripheral == "" and additional_func.signal_name.startswith(criteria_value)) or additional_func.peripheral.startswith(criteria_value):
                        results.append((p, additional_func))
                elif criteria_type == GD32PinMap.CRITERIA_PIN_SUB_FUNCTION:
                    if additional_func.subfunction is not None and criteria_value in additional_func.subfunction:
                        results.append((p, additional_func))
                elif criteria_type == GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION:
                    if additional_func.peripheral.startswith(criteria_value[0]) and (additional_func.subfunction is not None and criteria_value[1] in additional_func.subfunction):
                        results.append((p, additional_func))
        results = list(filter(lambda p_func_tuple: GD32PinMap.does_ad_pass_filter(p_func_tuple[1], filter_device_name), results))
        results = list(filter(lambda p_func_tuple: self.pin_is_available_for_device(p_func_tuple[0].pin_name, filter_device_name), results))
        return results

    def search_pins_for_af(self, criteria_type, criteria_value,filter_device_name:str=None) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        results = list()
        for p in self.pin_map.values():
            # search through all alternate functions pins
            for alternate_funcs in p.af_functions_map.values():
                for alternate_func in alternate_funcs:
                    if criteria_type == GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH:
                        if alternate_func.peripheral.startswith(criteria_value):
                            results.append((p, alternate_func))
                    elif criteria_type == GD32PinMap.CRITERIA_PIN_SUB_FUNCTION:
                        if alternate_func.subfunction is not None and criteria_value in alternate_func.subfunction:
                            results.append((p, alternate_func))
                    elif criteria_type == GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION:
                        if alternate_func.peripheral.startswith(criteria_value[0]) and (alternate_func.subfunction is not None and criteria_value[1] in alternate_func.subfunction):
                            results.append((p, alternate_func))
        results = list(filter(lambda p_func_tuple: GD32PinMap.does_af_pass_filter(p_func_tuple[1], filter_device_name), results))
        results = list(filter(lambda p_func_tuple: self.pin_is_available_for_device(p_func_tuple[0].pin_name, filter_device_name), results))
        return results
