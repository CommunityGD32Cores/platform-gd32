from os import path
from typing import Dict
from parsing_info import DatasheetAFPageParsingInfo, DatasheetPinDefPageParsingInfo, DatasheetParsingInfo
from parsing_quirks import ParseUsingAreaQuirk, OverwritePinAdditionalInfoQuirk, OverwritePinAlternateInfoQuirk, OverwriteAdditionFunctionsList, CondenseColumnsQuirk

# Use this info to recognize the PDF and its parsing quirks.
# Every PDF will probably need different parsing quirks, like only
# scanning a range of pages at a time, different footnotes for device
# availability, the type of SPL family it belongs to (GD32F30x vs GD32F3x0 etc)

known_datasheets_infos: Dict[str, DatasheetAFPageParsingInfo] = {
    "GD32F190xx_Datasheet_Rev2.1.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([28,29], { "1": ["GD32F190x4"], "2": ["GD32F190x8", "GD32F190x6"], "3": ["GD32F190x8"]}),
            DatasheetAFPageParsingInfo([30,31], { "1": ["GD32F190x4"], "2": ["GD32F190x8", "GD32F190x6"], "3": ["GD32F190x8"]}),
            DatasheetAFPageParsingInfo([32],    { "1": ["GD32F190x4"], "2": ["GD32F190x8"]}, quirks=[
                ParseUsingAreaQuirk((95.623,123.157,766.102,533.928)),
                OverwritePinAlternateInfoQuirk("PF7", ["I2C0_SDA(1)/I2C1_SDA(2)", None, None, None, None, None, None, None, None, "SEG31"])
            ])
            #33rd page only has half of the PF7 line  -- parsed by using a quirk on the page before.
        ],
        pin_defs = [
            # GD32F190Rx
            DatasheetPinDefPageParsingInfo([16], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((176.736,125.389,767.591,531.695))]),
            DatasheetPinDefPageParsingInfo([17,18,19], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((79.996,124.645,766.847,533.183))]),
            DatasheetPinDefPageParsingInfo([20], "GD32F190Rx", "LQFP64", [ParseUsingAreaQuirk((79.996,124.645,458.024,533.183))]),
            # GD32F190Cx
            DatasheetPinDefPageParsingInfo([21], "GD32F190Cx", "LQFP48", [
                ParseUsingAreaQuirk((176.736,125.389,767.591,531.695)),
                OverwritePinAdditionalInfoQuirk("PA5", "Additional: ADC_IN5, CMP0_IM5, CMP1_IM5, DAC1_OUT, CANH")
            ]),
            # PB15 cut off on page 23 too but no *additional* functions are cut-off, so no need to correct it 
            DatasheetPinDefPageParsingInfo([22,23], "GD32F190Cx", "LQFP48", [
                ParseUsingAreaQuirk((79.996,124.645,766.847,533.183)),
                OverwritePinAdditionalInfoQuirk("PB15", "Additional: RTC_REFIN")
            ]),
            DatasheetPinDefPageParsingInfo([24], "GD32F190Cx", "LQFP48", [ParseUsingAreaQuirk((81.484,125.389,385.098,531.695))]),
            # GD32F190Tx
            DatasheetPinDefPageParsingInfo([25], "GD32F190Tx", "QFN36", [
                ParseUsingAreaQuirk((176.736,125.389,767.591,531.695)),
                OverwritePinAdditionalInfoQuirk("PA6", "Additional: ADC_IN6, OPA1_VINP, CANL")
            ]),
            DatasheetPinDefPageParsingInfo([26], "GD32F190Tx", "QFN36", [ParseUsingAreaQuirk((79.996,124.645,766.847,533.183))]),
            DatasheetPinDefPageParsingInfo([27], "GD32F190Tx", "QFN36", [ParseUsingAreaQuirk((81.484,124.645,514.58,533.183))]),
        ],
        series = "GD32F190", # series
        family_type = "B" # family type
    ), 
    "GD32F170xx_Datasheet_Rev2.1.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([26], { "1": ["GD32F170x4"], "2": ["GD32F170x8", "GD32F170x6"], "3": ["GD32F170x8"]}),
            DatasheetAFPageParsingInfo([27], { "1": ["GD32F170x4"], "2": ["GD32F170x8", "GD32F170x6"], "3": ["GD32F170x8"]}),
            DatasheetAFPageParsingInfo([28], { "1": ["GD32F170x4"], "2": ["GD32F170x8"]}, quirks=[
                OverwriteAdditionFunctionsList(["AF%d" % x for x in range(10)])
            ])
        ],
        pin_defs = [
            # GD32F170R8
            DatasheetPinDefPageParsingInfo([14], "GD32F170R8", "LQFP64", [
                ParseUsingAreaQuirk((176.736,125.389,767.591,531.695)),
                OverwritePinAdditionalInfoQuirk("PA2", "Additional: ADC_IN2")
            ]),
            DatasheetPinDefPageParsingInfo([15], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([16], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([17], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            # GD32F170Cx
            DatasheetPinDefPageParsingInfo([19], "GD32F170Cx", "LQFP48", [
                ParseUsingAreaQuirk((127.622,124.645,760.893,533.183)),
                OverwritePinAdditionalInfoQuirk("PA6", "Additional: ADC_IN6, CANL")
                ]),
            DatasheetPinDefPageParsingInfo([20], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([21], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([22], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.229,124.645,270.499,532.439))]),
            # GD32F170Tx
            DatasheetPinDefPageParsingInfo([23], "GD32F170Tx", "QFN36", [
                ParseUsingAreaQuirk((128.366,125.389,770.567,533.183)),
                OverwritePinAdditionalInfoQuirk("PA7", "Additional: ADC_IN7")
            ]),
            DatasheetPinDefPageParsingInfo([24], "GD32F170Tx", "QFN36", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([25], "GD32F170Tx", "QFN36", [ParseUsingAreaQuirk((82.229,124.645,401.469,531.695))]),
        ],
        series = "GD32F170", # series
        family_type = "B" # family type
    ),
    "GD32F150xx_Datasheet_Rev3.2.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([30], { "1": ["GD32F150x4"], "2": ["GD32F150x8", "GD32F150x6"], "3": ["GD32F150x8"]}, quirks=[
                ParseUsingAreaQuirk((132.804,123.132,765.204,532.332)),
                CondenseColumnsQuirk(),
                OverwritePinAlternateInfoQuirk("PA11", ["EVENTOUT", "USART0_CTS", "TIMER0_CH3", "TSI_G3_CH3", None, None, None, "CMP0_OUT"])
            ]),
            DatasheetAFPageParsingInfo([31], { "1": ["GD32F150x4"], "2": ["GD32F150x8", "GD32F150x6"], "3": ["GD32F150x8"]}, quirks=[
                ParseUsingAreaQuirk((80.724,123.132,321.036,532.332)),
                CondenseColumnsQuirk()
            ]),
            DatasheetAFPageParsingInfo([32], { "1": ["GD32F150x4"], "2": ["GD32F150x8", "GD32F150x6"], "3": ["GD32F150x8"]}, quirks=[
                ParseUsingAreaQuirk((97.836,122.388,656.58,532.332)),
                CondenseColumnsQuirk()
            ]),
            DatasheetAFPageParsingInfo([33], { "1": ["GD32F150x4"], "2": ["GD32F150x8", "GD32F150x6"], "3": ["GD32F150x8"]}, quirks=[
                ParseUsingAreaQuirk((97.092,123.132,389.484,530.844)),
                CondenseColumnsQuirk()
            ])
        ],
        pin_defs = [
            # GD32F150Rx
            DatasheetPinDefPageParsingInfo([15], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((175.956,121.644,759.252,533.076)),
                OverwritePinAdditionalInfoQuirk("PA1", "Additional: ADC_IN1, CMP0_IP"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([16], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((82.212,123.132,769.668,532.332)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([17], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((82.212,123.132,769.668,532.332)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([18], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((82.212,123.132,769.668,532.332)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([19], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((82.212,122.388,301.692,531.588)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            # GD32F150Cx
            DatasheetPinDefPageParsingInfo([20], "GD32F150Cx", "LQFP48", [
                ParseUsingAreaQuirk((131.316,121.644,771.156,531.588)),
                OverwritePinAdditionalInfoQuirk("PA5", "Additional: ADC_IN5, CMP0_IM5, CMP1_IM5"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([21], "GD32F150Cx", "LQFP48", [
                ParseUsingAreaQuirk((80.724,122.388,766.692,532.332)),
                OverwritePinAdditionalInfoQuirk("PB15", "Additional: RTC_REFIN"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([22], "GD32F150Cx", "LQFP48", [
                ParseUsingAreaQuirk((80.724,122.388,766.692,532.332)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([23], "GD32F150Cx", "LQFP48", [
                ParseUsingAreaQuirk((80.724,123.132,344.844,531.588)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            # GD32F150Kx
            DatasheetPinDefPageParsingInfo([24], "GD32F150Kx", "QFN32", [
                ParseUsingAreaQuirk((131.316,121.644,771.9,532.332)),
                OverwritePinAdditionalInfoQuirk("PA7", "Additional: ADC_IN7"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([25], "GD32F150Kx", "QFN32", [
                ParseUsingAreaQuirk((81.468,120.9,758.508,531.588)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([26], "GD32F150Kx", "QFN32", [
                ParseUsingAreaQuirk((80.724,121.644,431.892,533.076)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            # GD32F150Gx
            DatasheetPinDefPageParsingInfo([27], "GD32F150Gx", "QFN28", [
                ParseUsingAreaQuirk((132.06,122.388,771.9,532.332)),
                OverwritePinAdditionalInfoQuirk("PA7", "Additional: ADC_IN7"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([28], "GD32F150Gx", "QFN28", [
                ParseUsingAreaQuirk((81.468,123.132,759.252,530.1)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
            DatasheetPinDefPageParsingInfo([29], "GD32F150Gx", "QFN28", [
                ParseUsingAreaQuirk((82.212,121.644,315.084,531.588)),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(1)
            ]),
        ],
        series = "GD32F150", # series
        family_type = "B" # family type
    ),
    "GD32F130xx_Datasheet_Rev3.4.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([31], { "1": ["GD32F130x4"], "2": ["GD32F130x8", "GD32F130x6"], "3": ["GD32F130x8"]}, quirks=[
                ParseUsingAreaQuirk((130.572,123.132,704.94,533.076)),
                CondenseColumnsQuirk(),
            ]),
            DatasheetAFPageParsingInfo([32], { "1": ["GD32F130x4"], "2": ["GD32F130x8", "GD32F130x6"], "3": ["GD32F130x8"]}, quirks=[
                ParseUsingAreaQuirk((97.836,124.62,687.084,533.82)),
                CondenseColumnsQuirk(),
            ]),
            DatasheetAFPageParsingInfo([33], { "1": ["GD32F130x4", "GD32F130x6"], "2": ["GD32F130x8"]}, quirks=[
                ParseUsingAreaQuirk((96.348,124.62,405.852,533.82)),
                CondenseColumnsQuirk(),
            ]),
        ], 
        pin_defs = [
            # GD32F130R8
            DatasheetPinDefPageParsingInfo([15], "GD32F130R8", "LQFP64", [
                ParseUsingAreaQuirk((175.956,123.876,762.228,533.076)),
                OverwritePinAdditionalInfoQuirk("PA1", "Additional: ADC_IN1"),
            ]),
            DatasheetPinDefPageParsingInfo([16], "GD32F130R8", "LQFP64", [
                ParseUsingAreaQuirk((80.724,124.62,769.668,531.588)),
            ]),
            DatasheetPinDefPageParsingInfo([17], "GD32F130R8", "LQFP64", [
                ParseUsingAreaQuirk((80.724,124.62,769.668,531.588)),
            ]),
            DatasheetPinDefPageParsingInfo([18], "GD32F130R8", "LQFP64", [
                ParseUsingAreaQuirk((81.468,124.62,588.876,533.076)),
            ]),
            # GD32F130Cx
            DatasheetPinDefPageParsingInfo([19], "GD32F130Cx", "LQFP48", [
                ParseUsingAreaQuirk((132.804,125.364,768.924,532.332)),
            ]),
            DatasheetPinDefPageParsingInfo([20], "GD32F130Cx", "LQFP48", [
                ParseUsingAreaQuirk((81.468,123.876,769.668,533.076)),
            ]),
            DatasheetPinDefPageParsingInfo([21], "GD32F130Cx", "LQFP48", [
                ParseUsingAreaQuirk((82.212,124.62,703.452,531.588)),
            ]),
            # GD32F130Kx LQFP32, meaning actually GD32F130KxTx
            # HOWEVER, looking at https://www.gigadevice.com/?s=GD32F130K8
            # There are only U variants listed (QFN32)
            # and no T variants (LQFP32)
            # so we actually ignore the LQFP32 variants..
            # besides, we don't get the package name anyways and
            # the board definitions also ommit the package.
            # we might have to rethink that. 
            #DatasheetPinDefPageParsingInfo([22], "GD32F130Kx", "LQFP32", [
            #    ParseUsingAreaQuirk((191.58,124.62,772.644,531.588)),
            #    OverwritePinAdditionalInfoQuirk("PA7", "Additional: ADC_IN7"),
            #    CondenseColumnsQuirk(),
            #]),
            #DatasheetPinDefPageParsingInfo([23], "GD32F130Kx", "LQFP32", [
            #    ParseUsingAreaQuirk((82.212,123.876,760.74,531.588)),
            #    CondenseColumnsQuirk(),
            #]),
            #DatasheetPinDefPageParsingInfo([24], "GD32F130Kx", "LQFP32", [
            #    ParseUsingAreaQuirk((81.468,124.62,232.5,532.332)),
            #    CondenseColumnsQuirk(),
            #]),
            # technically this is for GD32F130KxUx but we don't get the package
            # name.
            DatasheetPinDefPageParsingInfo([24], "GD32F130Kx", "QFN32", [
                ParseUsingAreaQuirk((385.02,124.62,768.924,533.076)),
                OverwritePinAdditionalInfoQuirk("PA3", "Additional: ADC_IN3"),
                CondenseColumnsQuirk(),
            ]),
            DatasheetPinDefPageParsingInfo([25], "GD32F130Kx", "QFN32", [
                ParseUsingAreaQuirk((82.212,124.62,760.74,533.82)),
                CondenseColumnsQuirk(),
            ]),
            DatasheetPinDefPageParsingInfo([26], "GD32F130Kx", "QFN32", [
                ParseUsingAreaQuirk((81.468,124.62,444.54,533.076)),
                CondenseColumnsQuirk(),
            ]),
            # GD32F130Gx
            DatasheetPinDefPageParsingInfo([27], "GD32F130Gx", "QFN28", [
                ParseUsingAreaQuirk((131.316,124.62,769.668,533.076)),
                OverwritePinAdditionalInfoQuirk("PB0", "Additional: ADC_IN8"),
                CondenseColumnsQuirk(),
            ]),
            DatasheetPinDefPageParsingInfo([28], "GD32F130Gx", "QFN28", [
                ParseUsingAreaQuirk((81.468,124.62,690.804,533.076)),
                CondenseColumnsQuirk(),
            ]),
            # GD32F130Fx
            DatasheetPinDefPageParsingInfo([29], "GD32F130Fx", "TSSOP20", [
                ParseUsingAreaQuirk((174.468,124.62,771.156,532.332)),
                OverwritePinAdditionalInfoQuirk("PA7", "Additional: ADC_IN7"),
            ]),
            DatasheetPinDefPageParsingInfo([30], "GD32F130Fx", "TSSOP20", [
                ParseUsingAreaQuirk((82.212,124.62,434.124,533.076)),
            ]),
        ],
        series = "GD32F130", # series
        family_type = "B" # family type
    )
}

def identify_datasheet(datasheet_pdf_path: str) -> DatasheetParsingInfo:
    global known_datasheets_infos
    if path.basename(datasheet_pdf_path) in known_datasheets_infos:
        return known_datasheets_infos[path.basename(datasheet_pdf_path)]
    else:
        return None