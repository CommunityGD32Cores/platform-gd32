from typing import Dict, Tuple, List
from func_utils import get_trailing_number
from pin_definitions import GD32AdditionalFunc, GD32AdditionalFuncFamiliy, GD32AlternateFunc, GD32Pin
from pin_map import GD32PinMap
from datasheet_parser import GD32DatasheetParser
from static_data import *
        
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
        return pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHERAL_STARTS_WITH, "TIMER", filter_device_name=device_name)

    @staticmethod
    def get_uart_tx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
        res = pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("USART", "TX"), filter_device_name=device_name)
        return res + pinmap.search_pins_for_af(GD32PinMap.CRITERIA_PERIPHAL_AND_PIN_SUB_FUNCTION, ("UART", "TX"), filter_device_name=device_name)

    @staticmethod
    def get_uart_tx_pins(pinmap: GD32PinMap, device_name:str) -> List[Tuple[GD32Pin, GD32AlternateFunc]]:
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
        return "    {NC,   NC,    0}\n};\n"

    @staticmethod
    def format_pin_to_port_pin(pin_name:str) -> str:
        port_ident = pin_name[1]
        pin_num = pin_name[2:]
        return "PORT%s_%s" % (port_ident, pin_num)

    @staticmethod
    def add_ad_pin(pin: GD32Pin, func: GD32AdditionalFunc, function_bits:str, commented_out:bool = False):
        temp = "%s    {%s, %s, %s}," % (
            "" if commented_out is False else "//",
            GD32PinMapGenerator.format_pin_to_port_pin(pin.pin_name),
            func.peripheral,
            function_bits
        )
        temp = temp.ljust(50) # padding with spaces
        temp += "/* %s */\n" % func.signal_name
        return temp 

    @staticmethod
    def add_adc_pin(pin: GD32Pin, func: GD32AdditionalFunc) -> str: 
        chan_num = get_trailing_number(func.signal_name)
        return GD32PinMapGenerator.add_ad_pin(
            pin, func, "GD_PIN_FUNC_ANALOG_CH(%d)" % chan_num, False)

    # generation methods
    @staticmethod
    def generate_arduino_peripheralpins_c(pinmap:GD32PinMap, device_name:str) -> str:
        output = gigadevice_header
        output += spl_family_b_peripheral_pins_c_header
        # ADC
        output += GD32PinMapGenerator.begin_pinmap("ADC")
        for p, f in GD32PinMapGenerator.get_adc_pins(pinmap, device_name):
            output += GD32PinMapGenerator.add_adc_pin(p, f)
        # .. all other peripherals..
        output += GD32PinMapGenerator.end_pinmap()
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
        print("PeripheralsPin.c for GD32F190T6:")
        print(output)

        output = GD32PinMapGenerator.generate_arduino_peripheralpins_c(pinmap, "GD32F190R8")
        print("PeripheralsPin.c for GD32F190R8:")
        print(output)

        #print(pinmap.pin_map["PB7"])
        pass

def main_func():
    print("Pinmap generator started.")
    # temporary static path
    datasheet_pdf_path = "C:\\Users\\Max\\Desktop\\gd32_dev\\gigadevice-firmware-and-docs\\GD32F1x0\\GD32F190xx_Datasheet_Rev2.1.pdf"
    device_pinmap = GD32DatasheetParser.get_pinmap_for_pdf(datasheet_pdf_path)
    GD32PinMapGenerator.generate_from_pinmap(device_pinmap)
if __name__ == "__main__":
    main_func()
