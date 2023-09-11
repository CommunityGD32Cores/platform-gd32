from parsing_info import RemappingMacro

remapping_info = {
    "gd32f10x": {
        "PA0": { 
            "TIMER1_CH0": [
                RemappingMacro("TIMER1_FULL_REMAP", disable=True),
                RemappingMacro("TIMER1_PARTIAL_REMAP1")
            ],
            "TIMER1_ETI": [
                RemappingMacro("TIMER1_FULL_REMAP", disable=True),
                RemappingMacro("TIMER1_PARTIAL_REMAP1")
            ],
            "USART1_CTS": [RemappingMacro("USART1_REMAP", disable=True, include_packages=["144", "100"])]
        },
        "PA1": { 
            "TIMER1_CH1": [
                RemappingMacro("TIMER1_FULL_REMAP", disable=True),
                RemappingMacro("TIMER1_PARTIAL_REMAP1")
            ],
            "USART1_RTS": [RemappingMacro("USART1_REMAP", disable=True, include_packages=["144", "100"])]
        },
        "PA2": { 
            "TIMER1_CH2": [
                RemappingMacro("TIMER1_FULL_REMAP", disable=True),
                RemappingMacro("TIMER1_PARTIAL_REMAP0")
            ],
            "TIMER8_CH0": [RemappingMacro("TIMER8_REMAP", disable=True, include_packages=["144", "100"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "USART1_TX": [RemappingMacro("USART1_REMAP", disable=True, include_packages=["144", "100"])]
        },
        "PA3": { 
            "TIMER1_CH3": [
                RemappingMacro("TIMER1_FULL_REMAP", disable=True),
                RemappingMacro("TIMER1_PARTIAL_REMAP0")
            ],
            "TIMER8_CH1": [RemappingMacro("TIMER8_REMAP", disable=True, include_packages=["144", "100"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "USART1_RX": [RemappingMacro("USART1_REMAP", disable=True, include_packages=["144", "100"])]
        },
        "PA4": { 
            "USART1_CK": [RemappingMacro("USART1_REMAP", disable=True, include_packages=["144", "100"])],
            "SPI0_NSS": [RemappingMacro("SPI0_REMAP", disable=True)],
            "SPI2_NSS": [RemappingMacro("SPI0_REMAP")],
            "I2S2_WS": [RemappingMacro("SPI0_REMAP")],
        },
        "PA5": {
            "SPI0_SCK": [RemappingMacro("SPI0_REMAP", disable=True)]
        },
        "PA6": { 
            "TIMER0_BKIN": [RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"])],
            "TIMER2_CH0": [RemappingMacro("TIMER2_FULL_REMAP", disable=True)],
            "TIMER12_CH0": [RemappingMacro("TIMER12_REMAP", disable=True, include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "SPI0_MISO": [RemappingMacro("SPI0_REMAP", disable=True)]
        },
        "PA7": { 
            "TIMER0_CH0_ON": [RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"])],
            "TIMER2_CH1": [RemappingMacro("TIMER2_FULL_REMAP", disable=True)],
            "TIMER13_CH0": [RemappingMacro("TIMER13_REMAP", disable=True, include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "SPI0_MOSI": [RemappingMacro("SPI0_REMAP", disable=True)]
        },
        "PA8": { 
            "TIMER0_CH0": [
                RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"]),
                RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"]) 
            ]
        },
        "PA9": { 
            "TIMER0_CH1": [
                RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"]),
                RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"]) 
            ],
            "USART0_TX": [RemappingMacro("USART0_REMAP", disable=True)]
        },
        "PA10": { 
            "TIMER0_CH2": [
                RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"]),
                RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"]) 
            ],
            "USART0_RX": [RemappingMacro("USART0_REMAP", disable=True)]
        },
        "PA11": { 
            "TIMER0_CH3": [
                RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"]),
                RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"]) 
            ],
            "CAN0_RX": [RemappingMacro("CAN0_FULL_REMAP", disable=True, include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_RX": [RemappingMacro("CAN_FULL_REMAP", disable=True, include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],
        },
        "PA12": { 
            "TIMER0_ETI": [ 
                RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"]),
                RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "CAN0_TX": [RemappingMacro("CAN0_FULL_REMAP", disable=True, include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_TX": [RemappingMacro("CAN_FULL_REMAP", disable=True, include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],
        },
        "PA15": { 
            "TIMER1_CH0": [
                RemappingMacro("TIMER1_PARTIAL_REMAP0"),
                RemappingMacro("TIMER1_FULL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "TIMER1_ETI": [
                RemappingMacro("TIMER1_PARTIAL_REMAP0"),
                RemappingMacro("TIMER1_FULL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "SPI0_NSS": [RemappingMacro("SPI0_REMAP")],
            "SPI2_NSS": [RemappingMacro("SPI0_REMAP", disable=True)],
            "I2S2_WS": [RemappingMacro("SPI0_REMAP", disable=True)],
        },

        "PB0": { 
            "TIMER0_CH1_ON": [RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"])],
            "TIMER2_CH2": [
                RemappingMacro("TIMER2_FULL_REMAP", disable=True),
                RemappingMacro("TIMER2_PARTIAL_REMAP")
            ] 
        },
        "PB1": { 
            "TIMER0_CH2_ON": [RemappingMacro("TIMER0_PARTIAL_REMAP", include_packages=["144", "100", "64", "48"])],
            "TIMER2_CH3": [
                RemappingMacro("TIMER2_FULL_REMAP", disable=True),
                RemappingMacro("TIMER2_PARTIAL_REMAP")
            ]
        },
        "PB3": { 
            "TIMER1_CH1": [
                RemappingMacro("TIMER1_PARTIAL_REMAP0"),
                RemappingMacro("TIMER1_FULL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "SPI0_SCK": [RemappingMacro("SPI0_REMAP")],
            "SPI2_SCK": [RemappingMacro("SPI0_REMAP", disable=True)],
            "I2S2_CK": [RemappingMacro("SPI0_REMAP", disable=True)],
        },
        "PB4": { 
            "TIMER2_CH0": [RemappingMacro("TIMER2_PARTIAL_REMAP")],
            "SPI0_MISO": [RemappingMacro("SPI0_REMAP")],
            "SPI2_MISO": [RemappingMacro("SPI0_REMAP", disable=True)],
        },
        "PB5": { 
            "TIMER2_CH1": [RemappingMacro("TIMER2_PARTIAL_REMAP")],
            "SPI0_MOSI": [RemappingMacro("SPI0_REMAP")], 
            "SPI2_MOSI": [RemappingMacro("SPI0_REMAP", disable=True)],
            "I2S2_SD": [RemappingMacro("SPI0_REMAP", disable=True)],
            "CAN1_RX": [RemappingMacro("CAN1_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])]
        },
        "PB6": { 
            "TIMER3_CH0": [RemappingMacro("TIMER3_REMAP", disable=True, include_packages=["144", "100"])],
            "USART0_TX": [RemappingMacro("USART0_REMAP")],
            "I2C0_SCL": [RemappingMacro("I2C0_REMAP", disable=True)],
            "CAN1_TX": [RemappingMacro("CAN1_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])]
        },
        "PB7": { 
            "TIMER3_CH1": [RemappingMacro("TIMER3_REMAP", disable=True, include_packages=["144", "100"])],
            "USART0_RX": [RemappingMacro("USART0_REMAP")],
            "I2C0_SDA": [RemappingMacro("I2C0_REMAP", disable=True)]
        },
        "PB8": { 
            "TIMER3_CH2": [RemappingMacro("TIMER3_REMAP", disable=True, include_packages=["144", "100"])],
            "TIMER9_CH0": [RemappingMacro("TIMER9_REMAP", disable=True, include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "I2C0_SDA": [RemappingMacro("I2C0_REMAP")],
            "CAN0_RX": [RemappingMacro("CAN0_PARTIAL_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_RX": [RemappingMacro("CAN_PARTIAL_REMAP", include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],

        },
        "PB9": { 
            "TIMER3_CH3": [RemappingMacro("TIMER3_REMAP", disable=True, include_packages=["144", "100"])],
            "TIMER10_CH0": [RemappingMacro("TIMER10_REMAP", disable=True, include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])],
            "I2C0_SCL": [RemappingMacro("I2C0_REMAP")],
            "CAN0_TX": [RemappingMacro("CAN0_PARTIAL_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_TX": [RemappingMacro("CAN_PARTIAL_REMAP", include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],
        },
        "PB10": { 
            "TIMER1_CH2": [
                RemappingMacro("TIMER1_PARTIAL_REMAP1"),
                RemappingMacro("TIMER1_FULL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "USART2_TX": [RemappingMacro("USART2_FULL_REMAP", disable=True, include_packages=["144", "100", "64"])]
        },
        "PB11": { 
            "TIMER1_CH3": [
                RemappingMacro("TIMER1_PARTIAL_REMAP1"),
                RemappingMacro("TIMER1_FULL_REMAP", include_packages=["144", "100", "64", "48"])
            ],
            "USART2_RX": [RemappingMacro("USART2_FULL_REMAP", disable=True, include_packages=["144", "100", "64"])]
        },
        "PB12": { 
            "TIMER0_BKIN": [RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"])],
            "USART2_CK": [RemappingMacro("USART2_FULL_REMAP", disable=True, include_packages=["144", "100", "64"])],
            "CAN1_RX": [RemappingMacro("CAN1_REMAP", disable=True, include_subseries=["CL"], include_packages=["144", "100", "64", "48"])]
        },
        "PB13": { 
            "TIMER0_CH0_ON": [RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"])],
            "USART2_CTS": [
                RemappingMacro("USART2_FULL_REMAP", disable=True, include_packages=["144", "100", "64"]),
                RemappingMacro("USART2_PARTIAL_REMAP", include_packages=["144", "100", "64"]),
            ],
            "CAN1_TX": [RemappingMacro("CAN1_REMAP", disable=True, include_subseries=["CL"])]
        },
        "PB14": { 
            "TIMER0_CH0_ON": [RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"])],
            "USART2_RTS": [
                RemappingMacro("USART2_FULL_REMAP", disable=True, include_packages=["144", "100", "64"]),
                RemappingMacro("USART2_PARTIAL_REMAP", include_packages=["144", "100", "64"]),
            ]
        },
        "PB15": { "TIMER0_CH0_ON": [RemappingMacro("TIMER0_FULL_REMAP", disable=True, include_packages=["144", "100", "64", "48"])] },

        "PC6": { "TIMER2_CH0": [RemappingMacro("TIMER2_FULL_REMAP", include_packages=["144", "100", "64"])] },
        "PC7": { "TIMER2_CH1": [RemappingMacro("TIMER2_FULL_REMAP", include_packages=["144", "100", "64"])] },
        "PC8": { "TIMER2_CH2": [RemappingMacro("TIMER2_FULL_REMAP", include_packages=["144", "100", "64"])] },
        "PC9": { "TIMER2_CH3": [RemappingMacro("TIMER2_FULL_REMAP", include_packages=["144", "100", "64"])] },
        "PC10": { 
            "USART2_TX": [RemappingMacro("USART2_PARTIAL_REMAP", include_packages=["144", "100", "64"])],
            "SPI2_SCK": [RemappingMacro("SPI0_REMAP")],
            "I2S2_CK": [RemappingMacro("SPI0_REMAP")],
        },
        "PC11": { 
            "USART2_RX": [RemappingMacro("USART2_PARTIAL_REMAP", include_packages=["144", "100", "64"])],
            "SPI2_MISO": [RemappingMacro("SPI0_REMAP")],
        },
        "PC12": { 
            "USART2_CK": [RemappingMacro("USART2_PARTIAL_REMAP", include_packages=["144", "100", "64"])],
            "SPI2_MOSI": [RemappingMacro("SPI0_REMAP")],
            "I2S2_SD": [RemappingMacro("SPI0_REMAP")],
        },

        "PD0": {
            "CAN0_RX": [RemappingMacro("CAN0_FULL_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_RX": [RemappingMacro("CAN_FULL_REMAP", include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],
        },
        "PD1": {
            "CAN0_RX": [RemappingMacro("CAN0_FULL_REMAP", include_subseries=["CL"], include_packages=["144", "100", "64", "48"])],
            "CAN_RX": [RemappingMacro("CAN_FULL_REMAP", include_subseries=["MD", "HD", "XD"], include_packages=["144", "100", "64", "48"])],
        },        
        "PD3": { "USART1_CTS": [RemappingMacro("USART1_REMAP", include_packages=["144", "100"])] },
        "PD4": { "USART1_RTS": [RemappingMacro("USART1_REMAP", include_packages=["144", "100"])] },
        "PD5": { "USART1_TX": [RemappingMacro("USART1_REMAP", include_packages=["144", "100"])] },
        "PD6": { "USART1_RX": [RemappingMacro("USART1_REMAP", include_packages=["144", "100"])] },
        "PD7": { "USART1_CK": [RemappingMacro("USART1_REMAP", include_packages=["144", "100"])] },
        "PD8": { "USART2_TX": [RemappingMacro("USART2_FULL_REMAP", include_packages=["144", "100"])] },
        "PD9": { "USART2_RX": [RemappingMacro("USART2_FULL_REMAP", include_packages=["144", "100"])] },
        "PD10": { "USART2_CK": [RemappingMacro("USART2_FULL_REMAP", include_packages=["144", "100"])] },
        "PD11": { "USART2_CTS": [RemappingMacro("USART2_FULL_REMAP", include_packages=["144", "100"])] },
        "PD12": {
            "TIMER3_CH0": [RemappingMacro("TIMER3_REMAP", include_packages=["144", "100"])],
            "USART2_RTS": [RemappingMacro("USART2_FULL_REMAP", include_packages=["144", "100"])]
        },
        "PD13": { "TIMER3_CH1": [RemappingMacro("TIMER3_REMAP", include_packages=["144", "100"])] },
        "PD14": { "TIMER3_CH2": [RemappingMacro("TIMER3_REMAP", include_packages=["144", "100"])] },
        "PD15": { "TIMER3_CH3": [RemappingMacro("TIMER3_REMAP", include_packages=["144", "100"])] },

        "PE5": { "TIMER8_CH0": [RemappingMacro("TIMER8_REMAP", include_packages=["144", "100"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
        "PE6": { "TIMER8_CH1": [RemappingMacro("TIMER8_REMAP", include_packages=["144", "100"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
        "PE7": { "TIMER0_ETI": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE8": { "TIMER0_CH0_ON": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE9": { "TIMER0_CH0": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE10": { "TIMER0_CH1_ON": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE11": { "TIMER0_CH1": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE12": { "TIMER0_CH2_ON": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE13": { "TIMER0_CH2": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE14": { "TIMER0_CH3": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },
        "PE15": { "TIMER0_BKIN": [RemappingMacro("TIMER0_FULL_REMAP", include_packages=["144", "100"])] },

        "PF6": { "TIMER9_CH0": [RemappingMacro("TIMER9_REMAP", include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
        "PF7": { "TIMER10_CH0": [RemappingMacro("TIMER10_REMAP", include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
        "PF8": { "TIMER12_CH0": [RemappingMacro("TIMER12_REMAP", include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
        "PF9": { "TIMER13_CH0": [RemappingMacro("TIMER13_REMAP", include_packages=["144"], include_mcus=["GD32F103Z(F|G|I|K)"])] },
    }
}