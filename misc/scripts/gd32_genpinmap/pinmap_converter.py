from collections import defaultdict
from typing import Callable, Dict, Tuple, List, TypeVar, Iterable
from func_utils import get_trailing_number, print_big_str, natural_keys, remove_last_comma, write_to_file, natural_key_for_pin_func
from pin_definitions import GD32Pin, GD32PinFunction
from pin_map import GD32PinCriteria, GD32PinCriteriaType, GD32PinMap
from static_data import *
from os import mkdir, path
import string, re
import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
# now we can use absolute imports
from board_generator import GD32MCUInfo

class GD32PinMapGenerator:
    @staticmethod
    def get_adc_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["ADC"])], filter_device_name=device_name)

    @staticmethod
    def get_adc_pinnames(pinmap: GD32PinMap, device_name:str) -> List[str]:
        adc_pins = GD32PinMapGenerator.get_adc_pins(pinmap, device_name)
        return list(set([x[0].pin_name for x in adc_pins]))

    @staticmethod
    def get_non_adc_pinnames(pinmap: GD32PinMap, device_name:str) -> List[str]:
        adc_pins = GD32PinMapGenerator.get_adc_pinnames(pinmap, device_name)
        subfam = pinmap.get_subfamily_for_device_name(device_name)
        if subfam is None:
            return list()
        subfam = pinmap.subseries_pinmaps[subfam]
        non_adc_pins = list(filter(lambda p: p not in adc_pins, subfam.pin_map.keys()))
        return non_adc_pins

    @staticmethod
    def get_alt_pinnames(pinmap: GD32PinMap, mcu:GD32MCUInfo) -> List[str]:
        subfam = pinmap.get_subfamily_for_device_name(mcu.name_no_package)
        if subfam is None:
            return list()
        subfam = pinmap.subseries_pinmaps[subfam]
        alt_pinnames = []
        for pin_info in subfam.pin_map.values():
            if len(pin_info.pin_functions):
                nalts = max([len(func.remapping_macros(mcu) or []) for func in pin_info.pin_functions])
                if nalts:
                    alt_pinnames += [f"{pin_info.pin_name}_ALT{alt} ({pin_info.pin_name} | ALT{alt})" for alt in range(1, nalts)]        
        return alt_pinnames
    
    @staticmethod
    def get_dac_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["DAC"])], filter_device_name=device_name)

    @staticmethod
    def get_i2c_sda_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("I2C", "SDA")])], filter_device_name=device_name)

    @staticmethod
    def get_i2c_scl_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("I2C", "SCL")])], filter_device_name=device_name)

    @staticmethod
    def get_pwm_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([
                GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["TIMER"]),
                GD32PinCriteria(GD32PinCriteriaType.SIGNAL_CONTAINS, ["_CH"])
            ], 
            filter_device_name=device_name)

    @staticmethod
    def get_uart_tx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("USART", "TX"), ("UART", "TX")])], filter_device_name=device_name)

    @staticmethod
    def get_uart_rx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("USART", "RX"), ("UART", "RX")])], filter_device_name=device_name)

    @staticmethod
    def get_uart_rts_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("USART", "RTS"), ("UART", "RTS")])], filter_device_name=device_name)

    @staticmethod
    def get_uart_cts_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("USART", "CTS"), ("UART", "CTS")])], filter_device_name=device_name)
   
    @staticmethod
    def get_spi_mosi_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("SPI", "MOSI")])], filter_device_name=device_name)

    @staticmethod
    def get_spi_miso_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("SPI", "MISO")])], filter_device_name=device_name)

    @staticmethod
    def get_spi_sclk_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("SPI", "SCK")])], filter_device_name=device_name)

    @staticmethod
    def get_spi_nss_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("SPI", "NSS")])], filter_device_name=device_name)

    @staticmethod
    def get_can_rd_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("CAN", "RX")])], filter_device_name=device_name)

    @staticmethod
    def get_can_td_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("CAN", "TX")])], filter_device_name=device_name)

    # ToDo: check if it makes sense to declare these. (CAN builtin PHY pins)
    @staticmethod
    def get_can_h_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("", "CANH")])], filter_device_name=device_name)

    @staticmethod
    def get_can_l_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32PinFunction]]:
        return pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("", "CANL")])], filter_device_name=device_name)

    @staticmethod
    def begin_pinmap(name:str):
        return "/* %s PinMap */\nconst PinMap PinMap_%s[] = {\n" % (name, name)

    @staticmethod
    def end_pinmap():
        return "    {NC,   NC,    0}\n};\n\n"

    @staticmethod
    def format_pin_to_port_pin(pin_name:str) -> str:
        port_ident = pin_name[1]
        pin_num = pin_name[2:]
        return "PORT%s_%s" % (port_ident, pin_num)
    
    @staticmethod
    def get_chan_num(func: GD32PinFunction):
        chan_num = 0
        sig_split = func.signal_name.split("TIMER")
        sig_split = [x.replace(",","") for x in sig_split]
        
        # we probably want to remember that "_ON" thing and 
        # give it in the pinmap? don't fully understand PWM yet, but 
        # there is the GD_PIN_CHON_GET() macro. 
        sig_split = [x.replace("_ON","") for x in sig_split]
        if len(sig_split) >= 2:
            chan_num = get_trailing_number(sig_split[1])
        
        #print(pin.pin_name)
        #print(func.signal_name)
        #print(sig_split)
        #print(chan_num)

        return chan_num
    
    @staticmethod
    def add_pin_text(pin_and_port:str, periph:str, function_bits:str, signal_name:str, commented_out:bool = False, width:int = 50):
        temp = "%s    {%s,%s %s,%s%s}," % (
            "" if commented_out is False else "//",
            pin_and_port,
            " " * (len("PORTA_15_ALT1") - len(pin_and_port)),
            periph,
            " " if "TIMER" not in periph else " " * (len("TIMER_15") - len(periph)), 
            function_bits
        )
        temp = temp.ljust(width) + " " # padding with spaces
        temp += "/* %s */\n" % signal_name
        return temp 

    @staticmethod
    def add_pin(pin: GD32Pin, func: GD32PinFunction, function_bits:str, commented_out:bool = False, width:int = 50, alt:int = 0):
        return GD32PinMapGenerator.add_pin_text(
            GD32PinMapGenerator.format_pin_to_port_pin(pin.pin_name) + ("_ALT" + str(alt) if alt > 0 else ""),
            func.peripheral,
            function_bits,
            func.signal_name,
            commented_out,
            width
        )
    
    @staticmethod
    def add_alt_pins(pin:GD32Pin, func:GD32PinFunction, function_bits, remapping_macros: any, commented_out:bool, alt: int = 0):
        retStr = ""
        for remapping_macro in remapping_macros:
            retStr += GD32PinMapGenerator.add_pin(
                pin, func, function_bits % remapping_macro, commented_out, alt=alt)
            alt += 1
        return retStr

    @staticmethod
    def add_adc_pin(pin: GD32Pin, func: GD32PinFunction, mcu:GD32MCUInfo, context: any) -> str: 
        chan_num = get_trailing_number(func.signal_name)
        alt = context["alt"]
        if func.family_type == "A":
            remapping_macros = func.remapping_macros(mcu)
            context["alt"] += len(remapping_macros) or 1
            if len(remapping_macros):
                return GD32PinMapGenerator.add_alt_pins(
                    pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)", [chan_num] * len(remapping_macros), False, alt)
            else:
                return GD32PinMapGenerator.add_pin(
                    pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False, alt=alt)
        elif func.family_type == "B":
            context["alt"] += 1
            return GD32PinMapGenerator.add_pin(
                pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False, alt=alt)
        else:
            raise Exception("Unknown family_type: %s" % func.family_type)

    @staticmethod
    def add_dac_pin(pin: GD32Pin, func: GD32PinFunction) -> str: 
        # expecting signal name "DACn_OUT"
        sig = get_trailing_number(func.signal_name)
        chan_num = 0 if sig is None else sig
        return GD32PinMapGenerator.add_pin(
            pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False)

    @staticmethod
    def add_i2c_pin(pin: GD32Pin, func: GD32PinFunction, mcu: GD32MCUInfo, context) -> str: 
        if func.family_type == "A":
            alt = context["alt"]
            remapping_macros = func.remapping_macros(mcu)
            context["alt"] += len(remapping_macros) or 1
            if remapping_macros and len(remapping_macros):
                return GD32PinMapGenerator.add_alt_pins(pin, func, "GD_PIN_FUNCTION5(PIN_MODE_AF, PIN_OTYPE_PP, PIN_PUPD_PULLUP, %s)", remapping_macros, False, alt)
            else:
                return GD32PinMapGenerator.add_pin(pin, func, "7", False)
        elif func.family_type is "B":
            if func.has_af_number():
                return GD32PinMapGenerator.add_pin(
                    pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, PIN_OTYPE_OD, PIN_PUPD_PULLUP, IND_GPIO_AF_%d)" % func.af_number, False)
            else:
                raise Exception("Alternate function number must be provided to enable i2c AF on B family devices")
        else:
            raise Exception("Unknown family_type: %s" % func.family_type)

    @staticmethod
    def add_uart_pin(pin: GD32Pin, func: GD32PinFunction, mcu: GD32MCUInfo, context) -> str: 
        alt = 0
        if func.family_type == "A":
            alt = context["alt"]
            remapping_macros = func.remapping_macros(mcu)
            context["alt"] += len(remapping_macros) or 1
            if remapping_macros and len(remapping_macros):
                return GD32PinMapGenerator.add_alt_pins(pin, func, "GD_PIN_FUNCTION5(PIN_MODE_AF, PIN_OTYPE_PP, PIN_PUPD_PULLUP, %s)", remapping_macros, False, alt)
        elif func.family_type == "B":
            if func.has_af_number():
                return GD32PinMapGenerator.add_pin(
                    pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, PIN_OTYPE_PP, PIN_PUPD_PULLUP, IND_GPIO_AF_%d)" % func.af_number, False)
        else:
            raise Exception("Unknown family_type: %s" % func.family_type)
        
        # output driving
        if any([x in func.signal_name for x in ("TX", "CTS", "RTS")]):
            return GD32PinMapGenerator.add_pin(
                pin, func, "7", False, alt=alt)
        # input
        else:
            return GD32PinMapGenerator.add_pin(
                pin, func, "1", False, alt=alt)

    @staticmethod
    def add_standard_af_pin(pin: GD32Pin, func: GD32PinFunction, mcu: GD32MCUInfo, context) -> str: 
        alt = 0
        if func.family_type == "A":
            alt = context["alt"]
            remapping_macros = func.remapping_macros(mcu)
            context["alt"] += len(remapping_macros) or 1
            if remapping_macros and len(remapping_macros):
                return GD32PinMapGenerator.add_alt_pins(pin, func, "GD_PIN_FUNCTION5(PIN_MODE_AF, PIN_OTYPE_PP, PIN_PUPD_PULLUP, %s)", remapping_macros, False, alt)
        elif func.family_type == "B":
            af_num = func.af_number
            if func.has_af_number():
                return GD32PinMapGenerator.add_pin(
                    pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, PIN_OTYPE_PP, PIN_PUPD_NONE, IND_GPIO_AF_%d)" % af_num, False)
        else:
            raise Exception("Unknown family_type: %s" % func.family_type)

        # not correct for all cases like CAN_RD, FIXME
        return GD32PinMapGenerator.add_pin(
            pin, func, "7", False, alt=alt)

    @staticmethod
    def add_pwm_pin(pin: GD32Pin, func: GD32PinFunction, mcu:GD32MCUInfo, context) -> str: 
        if func.family_type == "A":
            alt = context["alt"]
            chan_num = GD32PinMapGenerator.get_chan_num(func)
            remapping_macros = [(chan_num, m) for m in func.remapping_macros(mcu)]
            context["alt"] += len(remapping_macros) or 1
            return GD32PinMapGenerator.add_alt_pins(
                pin, func, "GD_PIN_FUNC_PWM(%d, %s)", remapping_macros if len(remapping_macros) else [(chan_num, "0")], False, alt)
        elif func.family_type == "B":
            ret = ""
            chan_num = GD32PinMapGenerator.get_chan_num(func)
            af_num = func.af_number
            if func.has_af_number():
                #print(af_num)
                ret += GD32PinMapGenerator.add_pin(
                    pin, func, "GD_PIN_FUNC_PWM(%d, IND_GPIO_AF_%d)" % (chan_num, af_num), False)
            else: 
                raise Exception("Alternate function number must be provided to enable PWM AF on B family devices")
        else:
            raise Exception("Unknown family_type: %s" % func.family_type)
        
    @staticmethod
    def add_gpio_ports(pinmap:GD32PinMap, device_name:str) -> str:
        temp = "const uint32_t gpio_port[] = {\n"
        # correct for all GD32F1x0.
        # the digitalWrite() logic expects this array to be this
        # way, even if the package does not provide access
        # to these pins -- might be worth refactoring.
        all_ports = ["A","B","C","D","E","F","G","H","I"]
        for idx, p in enumerate(all_ports):
            maybe_comma = ""
            if idx != len(all_ports) - 1:
                maybe_comma = ","
            temp += "#ifdef GPIO" + p + "\n"
            temp += "    GPIO" + p  + maybe_comma + "\n"
            temp += "#else" + "\n"
            temp += "    0" + maybe_comma  +  "\n"
            temp += "#endif\n"
        temp += "};\n\n"
        return temp

    @staticmethod
    def add_all_gpio_pins() -> str:
        temp = "const uint32_t gpio_pin[] = {\n"
        all_pins = ["    GPIO_PIN_%d" % p for p in range(16)]
        temp += ",\n".join(all_pins)
        temp += "\n};\n\n"
        return temp
    
    T = TypeVar("T")
    R = TypeVar("R")
    
    # itertools.groupby would need a sorted list
    @staticmethod
    def groupby(l: Iterable[T], key: Callable[[T],R]) -> Dict[R, T]:
        d = defaultdict(list)
        for item in l:
            d[key(item)].append(item)
        return d.items()
        
    @staticmethod
    def exec_by_pin_group(pins: List[Tuple[GD32Pin, GD32PinFunction]], function:Callable[[GD32Pin, GD32PinFunction, any], str], context: Callable[[], any] = lambda: {"alt": 0}) -> str:
        output = ""
        # group all functions together by pin name
        for p, fs in ((i, [j[1] for j in j]) for i, j in GD32PinMapGenerator.groupby(pins, lambda x: x[0])):
            func_context = context()
            for f in fs:
                output += function(p, f, func_context)
        return output

    # generation methods
    @staticmethod
    def generate_arduino_peripheralpins_c(pinmap:GD32PinMap, mcu:GD32MCUInfo) -> str:
        device_name = mcu.name_no_package
        output = gigadevice_header
        if pinmap.datasheet_info.family_type == "B":
            output += spl_family_b_peripheral_pins_c_header
        elif pinmap.datasheet_info.family_type == "A":
            output += spl_family_a_peripheral_pins_c_header.replace("GD32_FAMILY_REMAP_HEADER", f"{mcu.spl_series.lower()}_remap.h")
        # small correction for header: remove AF above 6
        if device_name.lower().startswith("gd32e23"):
            output = output.replace("    GPIO_AF_7,             /* 7 */\n", "")
            output = output.replace("    GPIO_AF_9,             /* 8 */\n", "")
            output = output.replace("    GPIO_AF_11             /* 9 */\n", "")
        if pinmap.devicename_matches_constraint(device_name, "GD32F3x0"):
            output = output.replace("    GPIO_AF_9,             /* 8 */\n", "")
            output = output.replace("    GPIO_AF_11             /* 9 */\n", "")
        # ADC
        output += GD32PinMapGenerator.begin_pinmap("ADC")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_adc_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_adc_pin(p, f, mcu, context))
        # ToDo: The "ADC" might actaully be "ADC0" ("ADC1"?) for some chips.
        # Channel 16 and 17 should be correct.
        if pinmap.datasheet_info.internal_adc != None:
            for (adc_name, (adc, channel)) in pinmap.datasheet_info.internal_adc.items():
                output += GD32PinMapGenerator.add_pin_text(
                    adc_name, "ADC%s" %(adc or ""), "GD_PIN_FUNC_ANALOG_CH(%s)" % channel, "ADC%s_IN%s" %(adc or "", channel))
        else:
            output += GD32PinMapGenerator.add_pin_text(
                "ADC_TEMP", "ADC", "GD_PIN_FUNC_ANALOG_CH(16)", "ADC_IN16")
            output += GD32PinMapGenerator.add_pin_text(
                "ADC_VREF", "ADC", "GD_PIN_FUNC_ANALOG_CH(17)", "ADC_IN17")
        output += GD32PinMapGenerator.end_pinmap()
        # DAC
        output += GD32PinMapGenerator.begin_pinmap("DAC")
        for p, f in GD32PinMapGenerator.get_dac_pins(pinmap, device_name):
            # hotfix for differently named DAC peripheral (DAC0 -> DAC)
            if device_name.lower().startswith("gd32f35"):
                f.peripheral = "DAC"
            output += GD32PinMapGenerator.add_dac_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # I2C SDA
        output += GD32PinMapGenerator.begin_pinmap("I2C_SDA")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_i2c_sda_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_i2c_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # I2C SCL
        output += GD32PinMapGenerator.begin_pinmap("I2C_SCL")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_i2c_scl_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_i2c_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # PWM
        output += GD32PinMapGenerator.begin_pinmap("PWM")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_pwm_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_pwm_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # UART TX
        output += GD32PinMapGenerator.begin_pinmap("UART_TX")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_uart_tx_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_uart_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # UART RX
        output += GD32PinMapGenerator.begin_pinmap("UART_RX")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_uart_rx_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_uart_pin(p, f, mcu, context))        
        output += GD32PinMapGenerator.end_pinmap()
        # UART RTS
        output += GD32PinMapGenerator.begin_pinmap("UART_RTS")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_uart_rts_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))          
        output += GD32PinMapGenerator.end_pinmap()
        # UART CTS
        output += GD32PinMapGenerator.begin_pinmap("UART_CTS")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_uart_cts_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))          
        output += GD32PinMapGenerator.end_pinmap()
        # SPI MOSI
        output += GD32PinMapGenerator.begin_pinmap("SPI_MOSI")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_spi_mosi_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))         
        output += GD32PinMapGenerator.end_pinmap()
        # SPI MISO
        output += GD32PinMapGenerator.begin_pinmap("SPI_MISO")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_spi_miso_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))          
        output += GD32PinMapGenerator.end_pinmap()
        # SPI SCLK
        output += GD32PinMapGenerator.begin_pinmap("SPI_SCLK")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_spi_sclk_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))           
        output += GD32PinMapGenerator.end_pinmap()
        # SPI SSEL
        output += GD32PinMapGenerator.begin_pinmap("SPI_SSEL")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_spi_nss_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # CAN RD
        output += GD32PinMapGenerator.begin_pinmap("CAN_RD")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_can_rd_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))
        output += GD32PinMapGenerator.end_pinmap()
        # CAN TD
        output += GD32PinMapGenerator.begin_pinmap("CAN_TD")
        output += GD32PinMapGenerator.exec_by_pin_group(
            GD32PinMapGenerator.get_can_td_pins(pinmap, device_name), 
            lambda p, f, context: GD32PinMapGenerator.add_standard_af_pin(p, f, mcu, context))        
        output += GD32PinMapGenerator.end_pinmap()
        # was refactored to be in core since it's constant data.
        # ports
        #output += GD32PinMapGenerator.add_gpio_ports(pinmap, device_name)
        # pins
        #output += GD32PinMapGenerator.add_all_gpio_pins()
        return output

    @staticmethod
    # e.g. "ADC" -> "ADC_0"
    #      "USART0" -> "UART_0"
    #      "USART1" -> "UART_1"
    #      "UART3" -> "UART_3"
    def convert_periph_name_into_enum_name(periph: str) -> str:
        orig_periph = periph
        periph_num_orig = get_trailing_number(periph)
        periph_num = periph_num_orig
        if periph_num_orig is None:
            periph_num = 0
        if periph.startswith("USART") or periph.startswith("UART"):
            periph = "UART" + str(periph_num)
        if periph.startswith("TIMER"):
            periph = "PWM" + str(periph_num)
        periph_no_num = periph
        if periph_num_orig is not None:
            periph_no_num = periph[0: len(periph) - len(str(periph_num))]
        left_side = periph_no_num + "_" + str(periph_num)
        return f"    {left_side} = (int){orig_periph},\n"

    @staticmethod
    def begin_periphalnames_enum():
        return "typedef enum {\n" 

    @staticmethod
    def end_periphalnames_enum(periph: str):
        return "} %sName;\n\n" % periph

    @staticmethod
    def add_periphalnames_enum(periph: str, pins: List[Tuple[GD32Pin, object]]) -> str:
        if len(pins) == 0:
            return "/* no %s pins */\n\n" % periph
        output = GD32PinMapGenerator.begin_periphalnames_enum()
        all_periphs = list(set([x[1].peripheral for x in pins]))
        all_periphs.sort(key=natural_keys)
        for p in all_periphs:
            output += GD32PinMapGenerator.convert_periph_name_into_enum_name(p)
        output += GD32PinMapGenerator.end_periphalnames_enum(periph)
        output = remove_last_comma(output)
        return output

    @staticmethod
    def generate_arduino_peripheralnames_h(pinmap:GD32PinMap, device_name:str) -> str:
        output = community_copyright_header
        output += peripheralnames_h_header_start
        periphs_and_pins = [
         ("ADC", GD32PinMapGenerator.get_adc_pins(pinmap, device_name)),
         ("DAC", GD32PinMapGenerator.get_dac_pins(pinmap, device_name)),
         ("UART", GD32PinMapGenerator.get_uart_tx_pins(pinmap, device_name)),
         ("SPI", GD32PinMapGenerator.get_spi_miso_pins(pinmap, device_name)),
         ("I2C", GD32PinMapGenerator.get_i2c_sda_pins(pinmap, device_name)),
         ("PWM", GD32PinMapGenerator.get_pwm_pins(pinmap, device_name)),
        ]
        for periph, pins in periphs_and_pins:
            output += GD32PinMapGenerator.add_periphalnames_enum(periph, pins)
        output += peripheralnames_h_header_end
        return output

    @staticmethod
    def generate_arduino_pinnamesvar_h(peripheral_pins_output: str) -> str:
        alt_match = re.findall("PORT[A-Z]_[0-9]+_ALT[0-9]", peripheral_pins_output) or []
        output = "".join(m + ",\n" for m in sorted(set(alt_match), key=GD32Pin.natural_sort_key))
        return output

    @staticmethod
    def add_macro_def(macro_name:str, macro_value="", overridable:bool = False, width:int = 35):
        output = f"#define {macro_name}"
        if len(str(macro_value)) != 0:
            output = output.ljust(width) + " "
            output += str(macro_value)
        output += "\n"
        if overridable:       
            output = f"#ifndef {macro_name}\n" + output + "#endif\n"
        return output

    @staticmethod
    def filter_for_periph(pins: List[Tuple[GD32Pin, GD32PinFunction]], periph:str) -> List[str]:
        return [p.pin_name for p,f in pins if f.peripheral == periph] 

    @staticmethod
    def get_second_or_fallback_first_pin(pins, already_assigned_pins:List[str] = None) -> str:
        if len(pins) == 0:
            return "UNKNOWN_PIN"
            # think about doing this
            raise RuntimeError("No pins to chose from.")
        pin_candidate = pins[1] if len(pins) >= 2 else pins[0]
        if already_assigned_pins is None:
            return pin_candidate
        else:
            if pin_candidate in already_assigned_pins:
                # pick first non assigned pin
                pin_candidates = list(filter(lambda p: p not in already_assigned_pins, pins))
                if len(pin_candidates) >= 1:
                    pin_candidates[0]
                else:
                    raise RuntimeError("Cannot find pin that is still unassigned!")
            else:
                return pin_candidate

    @staticmethod
    def generate_arduino_variant_h(pinmap:GD32PinMap, mcu:GD32MCUInfo) -> str:
        device_name = mcu.name_no_package
        output = community_copyright_header
        output += variant_h_header_start
        # generate all "#define <pin name> <index>" macros
        # due to pin numbering with ADC pins, we want that the ADC pins
        # form one *uniform*, uninterrupted block.
        # so, we place all ADC pins at the end
        counter = 0
        for p in GD32PinMapGenerator.get_non_adc_pinnames(pinmap, device_name):
            output += f"#define {p} {counter}\n"
            counter += 1
        num_gpio_pins = counter
        num_analog_pins = 0
        all_adc_pins = GD32PinMapGenerator.get_adc_pinnames(pinmap, device_name)
        output += "/* analog pins */\n"
        for p in all_adc_pins:
            output += f"#define {p} {counter}\n"
            counter += 1
            num_analog_pins += 1
        output += "\n/* digital pins and analog pins number definitions */\n"
        # analog pins can be used as digital pins too
        output += GD32PinMapGenerator.add_macro_def("DIGITAL_PINS_NUM", counter)
        output += GD32PinMapGenerator.add_macro_def("ANALOG_PINS_NUM", num_analog_pins)
        if len(all_adc_pins) != 0:
            output += GD32PinMapGenerator.add_macro_def("ANALOG_PINS_START", all_adc_pins[0])
            output += GD32PinMapGenerator.add_macro_def("ANALOG_PINS_LAST", all_adc_pins[-1])
        else:
            output += "/* warning: no ADC pins detected.. */\n"

        all_alt_pins = GD32PinMapGenerator.get_alt_pinnames(pinmap, mcu)
        output += "\n/* alternative pin remappings */\n"
        for p in all_alt_pins:
            output += f"#define {p}\n"

        output += "\n/* LED definitions */\n"
        if pinmap.pin_is_available_for_device("PC13", device_name):
            output += GD32PinMapGenerator.add_macro_def("LED_BUILTIN", "PC13") # default for now
        elif pinmap.pin_is_available_for_device("PB2", device_name):
            output += GD32PinMapGenerator.add_macro_def("LED_BUILTIN", "PB2") # default for now
        elif pinmap.pin_is_available_for_device("PA4", device_name):
            output += GD32PinMapGenerator.add_macro_def("LED_BUILTIN", "PA4") # default for now
        output += "\n/* user keys definitions */\n"
        output += GD32PinMapGenerator.add_macro_def("KEY0", "PA0") # default for now
        output += "\n/* SPI definitions */\n"
        # default to the first available SPI (SPI0) but the second available pin for each function
        # ensures we get the standard MOSI = PB5, MISO = PB4, etc. as known on the standard 
        # bluepill
        # first, get all pins for "SPI0"
        default_spi = "SPI0"
        spi_mosi = GD32PinMapGenerator.get_second_or_fallback_first_pin(
            GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_spi_mosi_pins(pinmap, device_name),
                default_spi
            )
        )
        spi_miso = GD32PinMapGenerator.get_second_or_fallback_first_pin(
            GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_spi_miso_pins(pinmap, device_name),
                default_spi
            )
        )
        spi_sclk = GD32PinMapGenerator.get_second_or_fallback_first_pin(
            GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_spi_sclk_pins(pinmap, device_name),
                default_spi
            )
        )
        spi_nss = GD32PinMapGenerator.get_second_or_fallback_first_pin(
            GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_spi_nss_pins(pinmap, device_name),
                default_spi
            )
        )
        # write back
        output += GD32PinMapGenerator.add_macro_def("PIN_SPI_SS", spi_nss)
        output += GD32PinMapGenerator.add_macro_def("PIN_SPI_MOSI", spi_mosi)
        output += GD32PinMapGenerator.add_macro_def("PIN_SPI_MISO", spi_miso)
        output += GD32PinMapGenerator.add_macro_def("PIN_SPI_SCK", spi_sclk)
        # same logic for I2C pin
        all_i2c_sda_pins = GD32PinMapGenerator.get_i2c_sda_pins(pinmap, device_name)
        i2c_periphs = list(sorted(set([af.peripheral for _, af in all_i2c_sda_pins])))
        output += "\n/* I2C definitions */\n"
        assigned_i2c_pins: list[str] = list()
        for i2c_periph in i2c_periphs:
            i2c_scl = GD32PinMapGenerator.get_second_or_fallback_first_pin(
                GD32PinMapGenerator.filter_for_periph(
                    GD32PinMapGenerator.get_i2c_scl_pins(pinmap, device_name),
                    i2c_periph
                )
            )
            i2c_sda = GD32PinMapGenerator.get_second_or_fallback_first_pin(
                GD32PinMapGenerator.filter_for_periph(
                    GD32PinMapGenerator.get_i2c_sda_pins(pinmap, device_name),
                    i2c_periph
                )
            )
            # update already used pins
            assigned_i2c_pins.extend([i2c_scl, i2c_sda])
            i2c_periph_num = int(i2c_periph[-1])
            have_i2c_macro_name = "HAVE_I2C" if i2c_periph_num == 0 else "HAVE_%s" % i2c_periph
            pin_wire = "PIN_WIRE" if i2c_periph_num == 0 else "PIN_WIRE%d" % i2c_periph_num

            output += f"/* {i2c_periph} */\n"
            if i2c_periph_num == 2:
                output += "/* Pins overlap with I2C0. Change I2C0 pins as neeeded. */\n"
            output += GD32PinMapGenerator.add_macro_def(have_i2c_macro_name)
            output += GD32PinMapGenerator.add_macro_def(f"{pin_wire}_SDA", i2c_sda, overridable=True)
            output += GD32PinMapGenerator.add_macro_def(f"{pin_wire}_SCL", i2c_scl, overridable=True)
            output += "\n"

        output += "/* TIMER or PWM definitions */\n"
        timer_tone = "TIMER5" # defaults
        timer_servo = "TIMER6" # defaults
        # some timers are not available on all devices, use other ones.
        if device_name.upper().startswith("GD32F330"):
            timer_tone = "TIMER13"
            timer_servo = "TIMER14"
        output += GD32PinMapGenerator.add_macro_def("TIMER_TONE", timer_tone) 
        output += GD32PinMapGenerator.add_macro_def("TIMER_SERVO", timer_servo)
        output += "\n"

        # generate list of first 5 PWM pins
        pwm_pins = GD32PinMapGenerator.get_pwm_pins(pinmap, device_name)
        pwm_pins = list(dict.fromkeys([p_f[0].pin_name for p_f in pwm_pins]))
        pwm_pins = pwm_pins[:5]
        for idx, p in enumerate(pwm_pins):
            output += GD32PinMapGenerator.add_macro_def("PWM%d" % idx, p)

        output += "\n/* Serial definitions */\n"
        output += "/* \"Serial\" is by default Serial1 / USART0 */\n"
        output += GD32PinMapGenerator.add_macro_def("DEFAULT_HWSERIAL_INSTANCE", "1", True) # defaults
        all_usart_tx_pins = GD32PinMapGenerator.get_uart_tx_pins(pinmap, device_name)
        usart_periphs = list(sorted(set([af.peripheral for _, af in all_usart_tx_pins])))
        for (i, usart) in enumerate(usart_periphs):
            output += f"\n/* {usart} */\n"
            uart_tx = GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_uart_tx_pins(pinmap, device_name),
                usart
            )[0]
            uart_rx = GD32PinMapGenerator.filter_for_periph(
                GD32PinMapGenerator.get_uart_rx_pins(pinmap, device_name),
                usart
            )[0]
            output += GD32PinMapGenerator.add_macro_def("HAVE_HWSERIAL%d" % (i+1))
            output += GD32PinMapGenerator.add_macro_def("SERIAL%d_RX" % i, uart_rx, overridable=True)
            output += GD32PinMapGenerator.add_macro_def("SERIAL%d_TX" % i, uart_tx, overridable=True)

        output += "\n/* ADC definitions */\n"
        output += GD32PinMapGenerator.add_macro_def("ADC_RESOLUTION", 10)
        if len(GD32PinMapGenerator.get_dac_pins(pinmap, device_name)) != 0:
            output += GD32PinMapGenerator.add_macro_def("DAC_RESOLUTION", 12)
        output += "\n"

        output += variant_h_header_end
        return output

    @staticmethod
    def generate_arduino_variant_cpp(pinmap:GD32PinMap, device_name:str) -> str:
        output = community_copyright_header
        output += variant_cpp_start
        for p in GD32PinMapGenerator.get_non_adc_pinnames(pinmap, device_name):
            output += f"    {GD32PinMapGenerator.format_pin_to_port_pin(p)},\n"
        # analog pins can be used as digital pins too..
        # todo check the whole pin remapping logic with ADC pins etc.
        for p in GD32PinMapGenerator.get_adc_pinnames(pinmap, device_name):
            output += f"    {GD32PinMapGenerator.format_pin_to_port_pin(p)},\n"
        output = remove_last_comma(output)
        output += "};\n"
        output += "\n/* analog pins for pinmap list */\n"
        output += "const uint32_t analog_pins[] = {\n"
        for idx, p in enumerate(GD32PinMapGenerator.get_adc_pinnames(pinmap, device_name)):
            output += f"    {p}, //A{idx}\n"
        output = remove_last_comma(output)
        output += "};\n\n"
        output += variant_cpp_end
        return output

    @staticmethod
    def generate_arduino_ldscript(mcu: GD32MCUInfo) -> str:
        ram = mcu.sram_kb
        flash = mcu.flash_kb
        template_file = path.join(path.dirname(path.realpath(__file__)), "ldscript.tpl")
        content = ""
        # 2K stack for all with over 4K RAM, below that (<=4K RAM) we only set 512 bytes of RAM (1/8th of RAM at worst)
        # this may still be too much for lower-RAM chips.. 
        stack_size = "2048" if mcu.sram_kb > 4 else "512"
        with open(template_file) as fp:
            data = string.Template(fp.read())
            print(data)
            content = data.substitute(
                ram=str(ram) + "K",
                flash=str(flash) + "K",
                stack=stack_size)
        return content

    @staticmethod
    def print_pinmap_info(pinmap: GD32PinMap):
        all_i2c_sda_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PIN_SUB_FUNCTION, ["SDA"])])
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        all_uart_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["UART", "USART"])])
        for pin, func in all_uart_pins:
            print("Found UART pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_rx_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHAL_AND_PIN_SUB_FUNCTION, [("CAN", "RX")])])
        for pin, func in all_can_rx_pins:
            print("Found CAN RX pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["CAN"])])
        for pin, func in all_can_pins:
            if func.has_af_number():
                print("Found CAN pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  
            else:
                print("Found CAN pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        all_adc_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["ADC"])])
        for pin, func in all_adc_pins:
            print("Found ADC pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        print("Testing search for only a device name.")
        all_adc_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PERIPHERAL_STARTS_WITH, ["ADC"])], filter_device_name="GD32F190T6")
        for pin, func in all_adc_pins:
            print("Found ADC pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        all_i2c_sda_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PIN_SUB_FUNCTION, ["SDA"])], filter_device_name="GD32F190T6")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        all_i2c_sda_pins = pinmap.search_pins_for_function([GD32PinCriteria(GD32PinCriteriaType.PIN_SUB_FUNCTION, ["SDA"])], filter_device_name="GD32F190T4")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

    @staticmethod
    def generate_from_pinmap(pinmap: GD32PinMap, mcus:List[GD32MCUInfo]):
        variant_base_folder = path.join(path.dirname(path.realpath(__file__)), "variants")
        if not path.isdir(variant_base_folder):
            mkdir(variant_base_folder)
        for mcu in mcus:
            mcu_name = mcu.name_no_package
            print(f"Generating Arduino variant folder for {mcu_name}.")
            target_base_folder = path.join(variant_base_folder, mcu_name.upper() + "_GENERIC")
            if not path.isdir(target_base_folder):
                mkdir(target_base_folder)
            # PeripheralName.h
            output = GD32PinMapGenerator.generate_arduino_peripheralnames_h(pinmap, mcu_name)
            print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "PeripheralNames.h"))
            # PeripheralPins.c
            output = GD32PinMapGenerator.generate_arduino_peripheralpins_c(pinmap, mcu)
            print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "PeripheralPins.c"))
            # PinNamesVar.h; Use PeripheralPins.c output to generate a list of alt names 
            output = GD32PinMapGenerator.generate_arduino_pinnamesvar_h(output) 
            print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "PinNamesVar.h"))
            # variant.cpp
            output = GD32PinMapGenerator.generate_arduino_variant_cpp(pinmap, mcu_name)
            print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "variant.cpp"))
            # variant.h
            output = GD32PinMapGenerator.generate_arduino_variant_h(pinmap, mcu)
            print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "variant.h"))
            # ldscript.ld
            output = GD32PinMapGenerator.generate_arduino_ldscript(mcu)
            #print_big_str(output)
            write_to_file(output, path.join(target_base_folder, "ldscript.ld"))
        print("Done writing %d variant definitions to %s." % (len(mcus), variant_base_folder))
