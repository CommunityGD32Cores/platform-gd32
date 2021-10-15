from typing import Dict, Tuple, List
from pin_definitions import GD32AdditionalFunc, GD32AdditionalFuncFamiliy, GD32AlternateFunc, GD32Pin
from pin_map import GD32PinMap
from datasheet_parser import GD32DatasheetParser
        
class GD32PinMapGenerator:
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
