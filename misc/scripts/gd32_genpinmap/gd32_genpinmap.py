from typing import Dict, Tuple, List
from func_utils import get_trailing_number, print_big_str, natural_keys, remove_last_comma
from known_datasheets import identify_datasheet
from pin_definitions import GD32AdditionalFunc, GD32AdditionalFuncFamiliy, GD32AlternateFunc, GD32Pin
from pin_map import GD32PinMap
from datasheet_parser import GD32DatasheetParser
from static_data import *
import pickle
from os import mkdir, path
import sys

class GD32PinMapGenerator:
    @staticmethod
    def get_adc_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AdditionalFunc]]:
        return pinmap.search_pins_for_add_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "ADC", filter_device_name=device_name)

    @staticmethod
    def get_dac_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AdditionalFunc]]:
        return pinmap.search_pins_for_add_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "DAC", filter_device_name=device_name)

    @staticmethod
    def get_i2c_sda_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("I2C", "SDA"), filter_device_name=device_name)

    @staticmethod
    def get_i2c_scl_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("I2C", "SCL"), filter_device_name=device_name)

    @staticmethod
    def get_pwm_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        all_timers = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "TIMER", filter_device_name=device_name)
        all_timers = list(filter(lambda p_func: "_CH" in p_func[1].signal_name, all_timers))
        return all_timers

    @staticmethod
    def get_uart_tx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        res = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("USART", "TX"), filter_device_name=device_name)
        return res + pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("UART", "TX"), filter_device_name=device_name)

    @staticmethod
    def get_uart_rx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        res = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("USART", "RX"), filter_device_name=device_name)
        return res + pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("UART", "RX"), filter_device_name=device_name)

    @staticmethod
    def get_uart_rts_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        res = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("USART", "RTS"), filter_device_name=device_name)
        return res + pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("UART", "RTS"), filter_device_name=device_name)

    @staticmethod
    def get_uart_cts_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        res = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("USART", "CTS"), filter_device_name=device_name)
        return res + pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("UART", "CTS"), filter_device_name=device_name)
   
    @staticmethod
    def get_spi_mosi_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("SPI", "MOSI"), filter_device_name=device_name)

    @staticmethod
    def get_spi_miso_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("SPI", "MISO"), filter_device_name=device_name)

    @staticmethod
    def get_spi_sclk_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("SPI", "SCK"), filter_device_name=device_name)

    @staticmethod
    def get_spi_nss_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("SPI", "NSS"), filter_device_name=device_name)

    @staticmethod
    def get_can_rd_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("CAN", "RX"), filter_device_name=device_name)

    @staticmethod
    def get_can_td_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("CAN", "TX"), filter_device_name=device_name)

    # ToDo: check if it makes sense to declare these. (CAN builtin PHY pins)
    @staticmethod
    def get_can_h_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("", "CANH"), filter_device_name=device_name)

    @staticmethod
    def get_can_l_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("", "CANL"), filter_device_name=device_name)

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
    def add_pin(pin_and_port:str, periph:str, function_bits:str, signal_name:str, commented_out:bool = False, width:int = 50):
        temp = "%s    {%s,%s %s,%s%s}," % (
            "" if commented_out is False else "//",
            pin_and_port,
            " " * (len("PORTA_15") - len(pin_and_port)),
            periph,
            " " if "TIMER" not in periph else " " * (len("TIMER_15") - len(periph)), 
            function_bits
        )
        temp = temp.ljust(width) + " " # padding with spaces
        temp += "/* %s */\n" % signal_name
        return temp 

    @staticmethod
    def add_ad_pin(pin: GD32Pin, func: GD32AdditionalFunc, function_bits:str, commented_out:bool = False, width:int = 50):
        return GD32PinMapGenerator.add_pin(
            GD32PinMapGenerator.format_pin_to_port_pin(pin.pin_name),
            func.peripheral,
            function_bits,
            func.signal_name,
            commented_out,
            width
        )

    @staticmethod
    def add_af_pin(pin: GD32Pin, func: GD32AlternateFunc, function_bits:str, commented_out:bool = False, width:int = 50):
        return GD32PinMapGenerator.add_pin(
            GD32PinMapGenerator.format_pin_to_port_pin(pin.pin_name),
            func.peripheral,
            function_bits,
            func.signal_name,
            commented_out,
            width
        )

    @staticmethod
    def add_adc_pin(pin: GD32Pin, func: GD32AdditionalFunc) -> str: 
        chan_num = get_trailing_number(func.signal_name)
        return GD32PinMapGenerator.add_ad_pin(
            pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False)

    @staticmethod
    def add_dac_pin(pin: GD32Pin, func: GD32AdditionalFunc) -> str: 
        # expecting signal name "DACn_OUT"
        sig = get_trailing_number(func.signal_name)
        chan_num = 0 if sig is None else sig
        return GD32PinMapGenerator.add_ad_pin(
            pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False)

    @staticmethod
    def add_i2c_pin(pin: GD32Pin, func: GD32AlternateFunc) -> str: 
        af_num = func.af_number
        return GD32PinMapGenerator.add_af_pin(
            pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, PIN_OTYPE_OD, PIN_PUPD_PULLUP, IND_GPIO_AF_%d)" % af_num, False)

    @staticmethod
    def add_uart_pin(pin: GD32Pin, func: GD32AlternateFunc) -> str: 
        af_num = func.af_number
        return GD32PinMapGenerator.add_af_pin(
            pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, GPIO_OTYPE_PP, PIN_PUPD_PULLUP, IND_GPIO_AF_%d)" % af_num, False)

    @staticmethod
    def add_standard_af_pin(pin: GD32Pin, func: GD32AlternateFunc) -> str: 
        af_num = func.af_number
        return GD32PinMapGenerator.add_af_pin(
            pin, func, "GD_PIN_FUNCTION4(PIN_MODE_AF, GPIO_OTYPE_PP, PIN_PUPD_NONE, IND_GPIO_AF_%d)" % af_num, False)


    @staticmethod
    def add_pwm_pin(pin: GD32Pin, func: GD32AlternateFunc) -> str: 
        chan_num = 0
        sig_split = func.signal_name.split("TIMER")
        sig_split = [x.replace(",","") for x in sig_split]
        # we probably want to remember that "_ON" thing and 
        # give it in the pinmap? don't fully understand PWM yet, but 
        # there is the GD_PIN_CHON_GET() macro. 
        sig_split = [x.replace("_ON","") for x in sig_split]
        if len(sig_split) >= 2:
            chan_num = get_trailing_number(sig_split[1])
        af_num = func.af_number
        #print(pin.pin_name)
        #print(func.signal_name)
        #print(sig_split)
        #print(chan_num)
        #print(af_num)
        return GD32PinMapGenerator.add_af_pin(
            pin, func, "GD_PIN_FUNC_PWM(%d, IND_GPIO_AF_%d)" % (chan_num, af_num), False)

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

    # generation methods
    @staticmethod
    def generate_arduino_peripheralpins_c(pinmap:GD32PinMap, device_name:str) -> str:
        output = gigadevice_header
        output += spl_family_b_peripheral_pins_c_header
        # ADC
        output += GD32PinMapGenerator.begin_pinmap("ADC")
        for p, f in GD32PinMapGenerator.get_adc_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_adc_pin(p, f)
        # ToDo: The "ADC" might actaully be "ADC0" ("ADC1"?) for some chips.
        # Channel 16 and 17 should be correct.
        output += GD32PinMapGenerator.add_pin(
            "ADC_TEMP", "ADC", "GD_PIN_FUNC_ANALOG_CH(16)", "ADC_IN16")
        output += GD32PinMapGenerator.add_pin(
            "ADC_VREF", "ADC", "GD_PIN_FUNC_ANALOG_CH(17)", "ADC_IN17")
        output += GD32PinMapGenerator.end_pinmap()
        # DAC
        output += GD32PinMapGenerator.begin_pinmap("DAC")
        for p, f in GD32PinMapGenerator.get_dac_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_dac_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # I2C SDA
        output += GD32PinMapGenerator.begin_pinmap("I2C_SDA")
        for p, f in GD32PinMapGenerator.get_i2c_sda_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_i2c_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # I2C SCL
        output += GD32PinMapGenerator.begin_pinmap("I2C_SCL")
        for p, f in GD32PinMapGenerator.get_i2c_scl_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_i2c_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # PWM
        output += GD32PinMapGenerator.begin_pinmap("PWM")
        for p, f in GD32PinMapGenerator.get_pwm_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_pwm_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # UART TX
        output += GD32PinMapGenerator.begin_pinmap("UART_TX")
        for p, f in GD32PinMapGenerator.get_uart_tx_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_uart_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # UART RX
        output += GD32PinMapGenerator.begin_pinmap("UART_RX")
        for p, f in GD32PinMapGenerator.get_uart_rx_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_uart_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # UART RTS
        output += GD32PinMapGenerator.begin_pinmap("UART_RTS")
        for p, f in GD32PinMapGenerator.get_uart_rts_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # UART CTS
        output += GD32PinMapGenerator.begin_pinmap("UART_CTS")
        for p, f in GD32PinMapGenerator.get_uart_cts_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # SPI MOSI
        output += GD32PinMapGenerator.begin_pinmap("SPI_MOSI")
        for p, f in GD32PinMapGenerator.get_spi_mosi_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # SPI MISO
        output += GD32PinMapGenerator.begin_pinmap("SPI_MISO")
        for p, f in GD32PinMapGenerator.get_spi_miso_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # SPI SCLK
        output += GD32PinMapGenerator.begin_pinmap("SPI_SCLK")
        for p, f in GD32PinMapGenerator.get_spi_sclk_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # SPI SSEL
        output += GD32PinMapGenerator.begin_pinmap("SPI_SSEL")
        for p, f in GD32PinMapGenerator.get_spi_nss_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # CAN RD
        output += GD32PinMapGenerator.begin_pinmap("CAN_RD")
        for p, f in GD32PinMapGenerator.get_can_rd_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
        output += GD32PinMapGenerator.end_pinmap()
        # CAN TD
        output += GD32PinMapGenerator.begin_pinmap("CAN_TD")
        for p, f in GD32PinMapGenerator.get_can_td_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_standard_af_pin(p, f)
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
    def generate_from_pinmap(pinmap: GD32PinMap):
        all_i2c_sda_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PIN_SUB_FUNCTION, "SDA")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        all_uart_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "UART")
        all_uart_pins.extend(pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "USART"))
        for pin, func in all_uart_pins:
            print("Found UART pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_rx_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("CAN", "RX"))
        for pin, func in all_can_rx_pins:
            print("Found CAN RX pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  

        all_can_pins = pinmap.search_pins_for_any_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "CAN")
        for pin, func in all_can_pins:
            if isinstance(func, GD32AlternateFunc):
                print("Found CAN pin %s (AF%d, func %s, periph %s, footnote %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote))  
            elif isinstance(func, GD32AdditionalFunc):
                print("Found CAN pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        all_adc_pins = pinmap.search_pins_for_add_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "ADC")
        for pin, func in all_adc_pins:
            print("Found ADC pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        print("Testing search for only a device name.")
        all_adc_pins = pinmap.search_pins_for_add_func(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "ADC", filter_device_name="GD32F190T6")
        for pin, func in all_adc_pins:
            print("Found ADC pin %s (func %s, periph %s, subseries %s)" % (pin.pin_name, func.signal_name, func.peripheral, func.subseries))  

        all_i2c_sda_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PIN_SUB_FUNCTION, "SDA", filter_device_name="GD32F190T6")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        all_i2c_sda_pins = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PIN_SUB_FUNCTION, "SDA", filter_device_name="GD32F190T4")
        for pin, func in all_i2c_sda_pins:
            print("Found I2C SDA pin %s (AF%d, func %s, periph %s, footnote %s %s)" % (pin.pin_name, func.af_number, func.signal_name, func.peripheral, func.footnote, func.footnote_resolved))  

        output = GD32PinMapGenerator.generate_arduino_peripheralpins_c(pinmap, "GD32F190T6")
        print("PeripheralPin.c for GD32F190T6:")
        print_big_str(output)

        output = GD32PinMapGenerator.generate_arduino_peripheralpins_c(pinmap, "GD32F190R8")
        print("PeripheralPin.c for GD32F190R8:")
        print_big_str(output)

        output = GD32PinMapGenerator.generate_arduino_peripheralpins_c(pinmap, "GD32F190C8")
        print("PeripheralPin.c for GD32F190C8:")
        print_big_str(output)

        output = GD32PinMapGenerator.generate_arduino_peripheralnames_h(pinmap, "GD32F190C8")
        print("PeripheralNames.h for GD32F190C8:")
        print_big_str(output)

        #print(pinmap.pin_map["PB7"])
        pass

# cache previously parsed datasheet for speed reaonss
def save_pinmap(pinmap: GD32PinMap):
    this_script = path.dirname(path.realpath(__file__))
    if not path.isdir(path.join(this_script, "preparsed_datasheets")):
        mkdir(path.join(this_script, "preparsed_datasheets"))
    try:
        pickle.dump( pinmap, open( path.join(this_script, "preparsed_datasheets", pinmap.series + ".p"), "wb" ) )
    except Exception as exc:
        print("Saving pinmap failed with error: %s" % str(exc)) 

# return previously loaded instance or None if it doesn't exist
def load_pinmap(datasheet_pdf_path:str) -> GD32PinMap:
    datasheet = identify_datasheet(datasheet_pdf_path)
    if datasheet is None: 
        return None
    this_script = path.dirname(path.realpath(__file__))
    expected_filepath = path.join(this_script, "preparsed_datasheets", datasheet.series + ".p")
    print("Checking if pre-saved pickle file \"%s\" exists.." % expected_filepath)
    if path.isfile(expected_filepath):
        try:
            pinmap = pickle.load(open(expected_filepath, "rb"))
            return pinmap
        except Exception as exc:
            print("Loading pinmap failed with error: %s" % str(exc))         
    print("Nope, parsing from PDF.")
    return None

def main_func():
    print("Pinmap generator started.")
    # temporary static path
    datasheet_pdf_path = "C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F190xx_Datasheet_Rev2.1.pdf"
    device_pinmap = load_pinmap(datasheet_pdf_path)
    if device_pinmap is None or "--no-load-preparsed" in sys.argv:
        device_pinmap = GD32DatasheetParser.get_pinmap_for_pdf(datasheet_pdf_path)
        save_pinmap(device_pinmap)
    GD32PinMapGenerator.generate_from_pinmap(device_pinmap)
if __name__ == "__main__":
    main_func()
