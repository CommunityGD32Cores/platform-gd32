from os import path
from typing import Dict
from parsing_info import DatasheetAFPageParsingInfo, DatasheetPinDefPageParsingInfo, DatasheetParsingInfo, FootnoteAvailabilityInfo
from parsing_quirks import ParseUsingAreaQuirk, OverwritePinDescriptionQuirk, OverwritePinAlternateInfoQuirk, OverwriteAdditionFunctionsList, CondenseColumnsQuirk
import gd32f10x_remap

# Use this info to recognize the PDF and its parsing quirks.
# Every PDF will probably need different parsing quirks, like only
# scanning a range of pages at a time, different footnotes for device
# availability, the type of SPL family it belongs to (GD32F30x vs GD32F3x0 etc)

known_datasheets_infos: Dict[str, DatasheetAFPageParsingInfo] = {
    "GD32F190xx_Datasheet_Rev2.1.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([28,29], { "1": FootnoteAvailabilityInfo(["GD32F190x4"]), "2": FootnoteAvailabilityInfo(["GD32F190x8", "GD32F190x6"]), "3": FootnoteAvailabilityInfo(["GD32F190x8"])}),
            DatasheetAFPageParsingInfo([30,31], { "1": FootnoteAvailabilityInfo(["GD32F190x4"]), "2": FootnoteAvailabilityInfo(["GD32F190x8", "GD32F190x6"]), "3": FootnoteAvailabilityInfo(["GD32F190x8"])}),
            DatasheetAFPageParsingInfo([32],    { "1": FootnoteAvailabilityInfo(["GD32F190x4"]), "2": FootnoteAvailabilityInfo(["GD32F190x8"])}, quirks=[
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
                OverwritePinDescriptionQuirk("PA5", "Additional: ADC_IN5, CMP0_IM5, CMP1_IM5, DAC1_OUT, CANH")
            ]),
            # PB15 cut off on page 23 too but no *additional* functions are cut-off, so no need to correct it 
            DatasheetPinDefPageParsingInfo([22,23], "GD32F190Cx", "LQFP48", [
                ParseUsingAreaQuirk((79.996,124.645,766.847,533.183)),
                OverwritePinDescriptionQuirk("PB15", "Additional: RTC_REFIN")
            ]),
            DatasheetPinDefPageParsingInfo([24], "GD32F190Cx", "LQFP48", [ParseUsingAreaQuirk((81.484,125.389,385.098,531.695))]),
            # GD32F190Tx
            DatasheetPinDefPageParsingInfo([25], "GD32F190Tx", "QFN36", [
                ParseUsingAreaQuirk((176.736,125.389,767.591,531.695)),
                OverwritePinDescriptionQuirk("PA6", "Additional: ADC_IN6, OPA1_VINP, CANL")
            ]),
            DatasheetPinDefPageParsingInfo([26], "GD32F190Tx", "QFN36", [ParseUsingAreaQuirk((79.996,124.645,766.847,533.183))]),
            DatasheetPinDefPageParsingInfo([27], "GD32F190Tx", "QFN36", [ParseUsingAreaQuirk((81.484,124.645,514.58,533.183))]),
        ],
        series = "GD32F190", # series
        family_type = "B" # family type
    ), 
    "GD32F170xx_Datasheet_Rev2.1.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([26], { "1": FootnoteAvailabilityInfo(["GD32F170x4"]), "2": FootnoteAvailabilityInfo(["GD32F170x8", "GD32F170x6"]), "3": FootnoteAvailabilityInfo(["GD32F170x8"])}),
            DatasheetAFPageParsingInfo([27], { "1": FootnoteAvailabilityInfo(["GD32F170x4"]), "2": FootnoteAvailabilityInfo(["GD32F170x8", "GD32F170x6"]), "3": FootnoteAvailabilityInfo(["GD32F170x8"])}),
            DatasheetAFPageParsingInfo([28], { "1": FootnoteAvailabilityInfo(["GD32F170x4"]), "2": FootnoteAvailabilityInfo(["GD32F170x8"])}, quirks=[
                OverwriteAdditionFunctionsList(["AF%d" % x for x in range(10)])
            ])
        ],
        pin_defs = [
            # GD32F170R8
            DatasheetPinDefPageParsingInfo([14], "GD32F170R8", "LQFP64", [
                ParseUsingAreaQuirk((176.736,125.389,767.591,531.695)),
                OverwritePinDescriptionQuirk("PA2", "Additional: ADC_IN2")
            ]),
            DatasheetPinDefPageParsingInfo([15], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([16], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([17], "GD32F170R8", "LQFP64", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            # GD32F170Cx
            DatasheetPinDefPageParsingInfo([19], "GD32F170Cx", "LQFP48", [
                ParseUsingAreaQuirk((127.622,124.645,760.893,533.183)),
                OverwritePinDescriptionQuirk("PA6", "Additional: ADC_IN6, CANL")
                ]),
            DatasheetPinDefPageParsingInfo([20], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([21], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([22], "GD32F170Cx", "LQFP48", [ParseUsingAreaQuirk((82.229,124.645,270.499,532.439))]),
            # GD32F170Tx
            DatasheetPinDefPageParsingInfo([23], "GD32F170Tx", "QFN36", [
                ParseUsingAreaQuirk((128.366,125.389,770.567,533.183)),
                OverwritePinDescriptionQuirk("PA7", "Additional: ADC_IN7")
            ]),
            DatasheetPinDefPageParsingInfo([24], "GD32F170Tx", "QFN36", [ParseUsingAreaQuirk((82.973,125.389,771.311,539.881))]),
            DatasheetPinDefPageParsingInfo([25], "GD32F170Tx", "QFN36", [ParseUsingAreaQuirk((82.229,124.645,401.469,531.695))]),
        ],
        series = "GD32F170", # series
        family_type = "B" # family type
    ),
    "GD32F150xx_Datasheet_Rev3.2.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([30], { "1": FootnoteAvailabilityInfo(["GD32F150x4"]), "2": FootnoteAvailabilityInfo(["GD32F150x8", "GD32F150x6"]), "3": FootnoteAvailabilityInfo(["GD32F150x8"])}, quirks=[
                ParseUsingAreaQuirk((132.804,123.132,765.204,532.332)),
                CondenseColumnsQuirk(),
                OverwritePinAlternateInfoQuirk("PA11", ["EVENTOUT", "USART0_CTS", "TIMER0_CH3", "TSI_G3_CH3", None, None, None, "CMP0_OUT"])
            ]),
            DatasheetAFPageParsingInfo([31], { "1": FootnoteAvailabilityInfo(["GD32F150x4"]), "2": FootnoteAvailabilityInfo(["GD32F150x8", "GD32F150x6"]), "3": FootnoteAvailabilityInfo(["GD32F150x8"])}, quirks=[
                ParseUsingAreaQuirk((80.724,123.132,321.036,532.332)),
                CondenseColumnsQuirk()
            ]),
            DatasheetAFPageParsingInfo([32], { "1": FootnoteAvailabilityInfo(["GD32F150x4"]), "2": FootnoteAvailabilityInfo(["GD32F150x8", "GD32F150x6"]), "3": FootnoteAvailabilityInfo(["GD32F150x8"])}, quirks=[
                ParseUsingAreaQuirk((97.836,122.388,656.58,532.332)),
                CondenseColumnsQuirk()
            ]),
            DatasheetAFPageParsingInfo([33], { "1": FootnoteAvailabilityInfo(["GD32F150x4"]), "2": FootnoteAvailabilityInfo(["GD32F150x8", "GD32F150x6"]), "3": FootnoteAvailabilityInfo(["GD32F150x8"])}, quirks=[
                ParseUsingAreaQuirk((97.092,123.132,389.484,530.844)),
                CondenseColumnsQuirk()
            ])
        ],
        pin_defs = [
            # GD32F150Rx
            DatasheetPinDefPageParsingInfo([15], "GD32F150Rx", "LQFP64", [
                ParseUsingAreaQuirk((175.956,121.644,759.252,533.076)),
                OverwritePinDescriptionQuirk("PA1", "Additional: ADC_IN1, CMP0_IP"),
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
                OverwritePinDescriptionQuirk("PA5", "Additional: ADC_IN5, CMP0_IM5, CMP1_IM5"),
                CondenseColumnsQuirk(0),
                CondenseColumnsQuirk(2)
            ]),
            DatasheetPinDefPageParsingInfo([21], "GD32F150Cx", "LQFP48", [
                ParseUsingAreaQuirk((80.724,122.388,766.692,532.332)),
                OverwritePinDescriptionQuirk("PB15", "Additional: RTC_REFIN"),
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
                OverwritePinDescriptionQuirk("PA7", "Additional: ADC_IN7"),
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
                OverwritePinDescriptionQuirk("PA7", "Additional: ADC_IN7"),
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
            DatasheetAFPageParsingInfo([31], { "1": FootnoteAvailabilityInfo(["GD32F130x4"]), "2": FootnoteAvailabilityInfo(["GD32F130x8", "GD32F130x6"]), "3": FootnoteAvailabilityInfo(["GD32F130x8"])}, quirks=[
                ParseUsingAreaQuirk((130.572,123.132,704.94,533.076)),
                CondenseColumnsQuirk(),
            ]),
            DatasheetAFPageParsingInfo([32], { "1": FootnoteAvailabilityInfo(["GD32F130x4"]), "2": FootnoteAvailabilityInfo(["GD32F130x8", "GD32F130x6"]), "3": FootnoteAvailabilityInfo(["GD32F130x8"])}, quirks=[
                ParseUsingAreaQuirk((97.836,124.62,687.084,533.82)),
                CondenseColumnsQuirk(),
            ]),
            DatasheetAFPageParsingInfo([33], { "1": FootnoteAvailabilityInfo(["GD32F130x4", "GD32F130x6"]), "2": FootnoteAvailabilityInfo(["GD32F130x8"])}, quirks=[
                ParseUsingAreaQuirk((96.348,124.62,405.852,533.82)),
                CondenseColumnsQuirk(),
            ]),
        ], 
        pin_defs = [
            # GD32F130R8
            DatasheetPinDefPageParsingInfo([15], "GD32F130R8", "LQFP64", [
                ParseUsingAreaQuirk((175.956,123.876,762.228,533.076)),
                OverwritePinDescriptionQuirk("PA1", "Additional: ADC_IN1"),
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
                OverwritePinDescriptionQuirk("PA3", "Additional: ADC_IN3"),
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
                OverwritePinDescriptionQuirk("PB0", "Additional: ADC_IN8"),
                CondenseColumnsQuirk(),
            ]),
            DatasheetPinDefPageParsingInfo([28], "GD32F130Gx", "QFN28", [
                ParseUsingAreaQuirk((81.468,124.62,690.804,533.076)),
                CondenseColumnsQuirk(),
            ]),
            # GD32F130Fx
            DatasheetPinDefPageParsingInfo([29], "GD32F130Fx", "TSSOP20", [
                ParseUsingAreaQuirk((174.468,124.62,771.156,532.332)),
                OverwritePinDescriptionQuirk("PA7", "Additional: ADC_IN7"),
            ]),
            DatasheetPinDefPageParsingInfo([30], "GD32F130Fx", "TSSOP20", [
                ParseUsingAreaQuirk((82.212,124.62,434.124,533.076)),
            ]),
        ],
        series = "GD32F130", # series
        family_type = "B" # family type
    ),
    "GD32E230xx_Datasheet_Rev1.4.pdf" : DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([32], { "1": FootnoteAvailabilityInfo(["GD32E230x4"]), "2": FootnoteAvailabilityInfo(["GD32E230x8", "GD32E230x6"]), "3": FootnoteAvailabilityInfo(["GD32E230x8"])}, quirks=[
                ParseUsingAreaQuirk((132.831,124.645,708.059,533.928)),
            ]),
            DatasheetAFPageParsingInfo([33], { "1": FootnoteAvailabilityInfo(["GD32E230x4"]), "2": FootnoteAvailabilityInfo(["GD32E230x8", "GD32E230x6"]), "3": FootnoteAvailabilityInfo(["GD32E230x8"])}, quirks=[
                ParseUsingAreaQuirk((94.879,124.645,637.364,535.416)),
            ]),
            DatasheetAFPageParsingInfo([33], { "1": FootnoteAvailabilityInfo(["GD32E230x4"]), "2": FootnoteAvailabilityInfo(["GD32E230x8", "GD32E230x6"]), "3": FootnoteAvailabilityInfo(["GD32E230x8"])}, quirks=[
                ParseUsingAreaQuirk((658.201,125.389,757.917,533.928 )),
                OverwritePinAlternateInfoQuirk("PF6", ["I2C0_SCL(1)/I2C1_SCL(3)", None, None, None, None, None, None])
            ]),
            DatasheetAFPageParsingInfo([34], { "1": FootnoteAvailabilityInfo(["GD32E230x4"]), "2": FootnoteAvailabilityInfo(["GD32E230x8", "GD32E230x6"]), "3": FootnoteAvailabilityInfo(["GD32E230x8"])}, quirks=[
                ParseUsingAreaQuirk((79.996,124.645,178.968,533.183 ))
            ]),
        ],
        pin_defs = [
            # GD32E230Cx
            DatasheetPinDefPageParsingInfo([18], "GD32E230Cx", "LQFP48", [ParseUsingAreaQuirk((179.712,125.389,757.173,536.904))]),
            DatasheetPinDefPageParsingInfo([19], "GD32E230Cx", "LQFP48", [ParseUsingAreaQuirk((79.996,124.645,766.102,535.416))]),
            DatasheetPinDefPageParsingInfo([20], "GD32E230Cx", "LQFP48", [ParseUsingAreaQuirk((79.252,124.645,758.661,534.672))]),
            # page 21 only has VSS and VDD, non important for Cx.
            # GD32E230Kx, LQFP32 and QFN32 definitions are the same.
            DatasheetPinDefPageParsingInfo([21], "GD32E230Kx", "LQFP32", [
                ParseUsingAreaQuirk((325.566,125.389,759.405,536.904)),
                OverwritePinDescriptionQuirk("PA4", "Additional: ADC_IN4, CMP_IM4"),
            ]),
            DatasheetPinDefPageParsingInfo([22], "GD32E230Kx", "LQFP32", [ParseUsingAreaQuirk((79.252,124.645,772.8,535.416))]),
            DatasheetPinDefPageParsingInfo([23], "GD32E230Kx", "LQFP32", [ParseUsingAreaQuirk((79.252,123.157,343.425,536.16))]),
            # GD32E230Gx
            DatasheetPinDefPageParsingInfo([25], "GD32E230Gx", "QFN28", [ParseUsingAreaQuirk((697.641,123.901,763.87,536.904))]),
            DatasheetPinDefPageParsingInfo([26], "GD32E230Gx", "QFN28", [
                ParseUsingAreaQuirk((79.252,124.645,768.335,536.904)),
                OverwritePinDescriptionQuirk("PB1", "Additional: ADC_IN9"),
            ]),
            DatasheetPinDefPageParsingInfo([27], "GD32E230Gx", "QFN28", [ParseUsingAreaQuirk((80.74,124.645,602.389,535.416))]),
            # GD32E230Fx TSSOP20 + LGA20.
            DatasheetPinDefPageParsingInfo([28], "GD32E230Fx", "TSSOP20", [
                ParseUsingAreaQuirk((135.063,123.157,763.87,535.416)),
                OverwritePinDescriptionQuirk("PB1", "Additional: ADC_IN9"),
            ]),
            DatasheetPinDefPageParsingInfo([29], "GD32E230Fx", "TSSOP20", [ParseUsingAreaQuirk((79.996,123.901,333.751,535.416))])
        ],
        series = "GD32E230", # series
        family_type = "B" # family type
    ),
    "GD32F303xx_Datasheet_Rev1.9.pdf" : DatasheetParsingInfo(
        alternate_funcs = [],
        pin_defs = [
            # GD32F303Cx
            DatasheetPinDefPageParsingInfo([39], "GD32F303Cx", "LQFP48", [ParseUsingAreaQuirk((130.572,123.132,759.252,531.588))], {"3":["GD32F303CG"]}),
        ],
        series = "GD32F303", # series
        family_type = "A", # family type
        family_name= "GD32F30x"
    ),
    "GD32F350xx_Datasheet_Rev2.3.pdf": DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([30], { "1": FootnoteAvailabilityInfo(["GD32F350x4"]), "2": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8", "GD32F350x6"]), "3": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8"])}, quirks=[
                ParseUsingAreaQuirk((127.622,122.413,748.243,535.416)),
            ]),
            DatasheetAFPageParsingInfo([31], { "1": FootnoteAvailabilityInfo(["GD32F350x4"]), "2": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8", "GD32F350x6"]), "3": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8"])}, quirks=[
                ParseUsingAreaQuirk((97.112,117.204,687.223,539.137)),
            ]),
            DatasheetAFPageParsingInfo([32], { "1": FootnoteAvailabilityInfo(["GD32F350x4"]), "2": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8", "GD32F350x6"]), "3": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8"])}, quirks=[
                ParseUsingAreaQuirk((97.112,124.645,394.027,534.672)),
            ]),
            DatasheetAFPageParsingInfo([32], { "1": FootnoteAvailabilityInfo(["GD32F350x4"]), "2": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8", "GD32F350x6"]), "3": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8"])}, quirks=[
                ParseUsingAreaQuirk((431.979,116.459,728.151,555.508)),
            ]),
            DatasheetAFPageParsingInfo([33], { "1": FootnoteAvailabilityInfo(["GD32F350x4"]), "2": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8", "GD32F350x6"]), "3": FootnoteAvailabilityInfo(["GD32F350xB", "GD32F350x8"])}, quirks=[
                ParseUsingAreaQuirk((97.112,123.901,422.305,534.672)),
            ]),
        ],
        pin_defs = [
            # GD32F350Rx
            DatasheetPinDefPageParsingInfo([17], "GD32F350Rx", "LQFP64", [ParseUsingAreaQuirk((233.291,125.389,771.311,533.183))]),
            DatasheetPinDefPageParsingInfo([18], "GD32F350Rx", "LQFP64", [
                ParseUsingAreaQuirk((82.973,124.645,766.102,533.928)),
                OverwritePinDescriptionQuirk("PB0", "Default: PB0\rAlternate: TIMER2_CH2, TIMER0_CH1_ON, TSI_G2_IO1, USART1_RX(4), EVENTOUT\rAdditional: ADC_IN8"),
            ]),
            DatasheetPinDefPageParsingInfo([19], "GD32F350Rx", "LQFP64", [ParseUsingAreaQuirk((81.484,123.157,773.544,535.416))]),
            DatasheetPinDefPageParsingInfo([20], "GD32F350Rx", "LQFP64", [ParseUsingAreaQuirk((83.717,123.157,760.893,535.416))]),
            DatasheetPinDefPageParsingInfo([21], "GD32F350Rx", "LQFP64", [ParseUsingAreaQuirk((81.484,123.901,201.293,534.672))]),
            # GD32F350Cx
            DatasheetPinDefPageParsingInfo([21], "GD32F350Cx", "LQFP48", [ParseUsingAreaQuirk((347.89,123.901,760.149,537.648))]),
            DatasheetPinDefPageParsingInfo([22], "GD32F350Cx", "LQFP48", [ParseUsingAreaQuirk((82.973,124.645,767.591,537.648))]),
            DatasheetPinDefPageParsingInfo([23], "GD32F350Cx", "LQFP48", [ParseUsingAreaQuirk((83.717,123.901,771.311,537.648))]),
            DatasheetPinDefPageParsingInfo([24], "GD32F350Cx", "LQFP48", [ParseUsingAreaQuirk((82.229,123.157,446.118,538.393))]),
            # GD32F350Kx
            DatasheetPinDefPageParsingInfo([24], "GD32F350Kx", "QFN32", [
                ParseUsingAreaQuirk((588.995,123.901,762.382,539.881)),
                OverwritePinDescriptionQuirk("PA0", "Default: PA0\rAlternate: USART0_CTS(3), USART1_CTS(4), TIMER1_CH0, TIMER1_ETI, CMP0_OUT, TSI_G0_IO0, I2C1_SCL(5)\rAdditional: ADC_IN0, CMP0_IM6, RTC_TAMP1, WKUP0"),
            ]),
            DatasheetPinDefPageParsingInfo([25], "GD32F350Kx", "QFN32", [ParseUsingAreaQuirk((84.461,122.413,769.079,537.648))]),
            DatasheetPinDefPageParsingInfo([26], "GD32F350Kx", "QFN32", [ParseUsingAreaQuirk((82.229,123.901,760.893,536.16))]),
            # GD32F350Gx
            DatasheetPinDefPageParsingInfo([27], "GD32F350Gx", "QFN28", [
                ParseUsingAreaQuirk((288.358,123.157,769.079,536.904)),
                OverwritePinDescriptionQuirk("PA5", "Default: PA5\rAlternate: SPI0_SCK, I2S0_CK, CEC, TIMER1_CH0, TIMER1_ETI, TSI_G1_IO1\rAdditional: ADC_IN5, CMP0_IM5, CMP1_IM5"),
            ]),
            DatasheetPinDefPageParsingInfo([28], "GD32F350Gx", "QFN28", [ParseUsingAreaQuirk((81.484,125.389,758.661,534.672))]),
            DatasheetPinDefPageParsingInfo([29], "GD32F350Gx", "QFN28", [ParseUsingAreaQuirk((83.717,124.645,359.052,534.672))]),
        ],
        series = "GD32F350", # series
        family_type = "B" # family type
    ),
    "GD32F330xx_Datasheet_Rev2.6.pdf": DatasheetParsingInfo(
        alternate_funcs = [ 
            DatasheetAFPageParsingInfo([34], { "1": FootnoteAvailabilityInfo(["GD32F330x4"]), "2": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8", "GD32F330x6"]), "3": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8"])}, quirks=[
                ParseUsingAreaQuirk((125.389,124.645,643.318,536.16)),
            ]),
            DatasheetAFPageParsingInfo([35], { "1": FootnoteAvailabilityInfo(["GD32F330x4"]), "2": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8", "GD32F330x6"]), "3": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8"])}, quirks=[
                ParseUsingAreaQuirk((94.879,125.389,562.205,534.672)),
            ]),
            DatasheetAFPageParsingInfo([36], { "1": FootnoteAvailabilityInfo(["GD32F330x4"]), "2": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8", "GD32F330x6"]), "3": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8"])}, quirks=[
                ParseUsingAreaQuirk((110.506,123.157,405.934,533.928)),
            ]),
            DatasheetAFPageParsingInfo([36], { "1": FootnoteAvailabilityInfo(["GD32F330x4"]), "2": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8", "GD32F330x6"]), "3": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8"])}, quirks=[
                ParseUsingAreaQuirk((442.397,118.692,729.639,539.137)),
            ]),
            DatasheetAFPageParsingInfo([37], { "1": FootnoteAvailabilityInfo(["GD32F330x4"]), "2": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8", "GD32F330x6"]), "3": FootnoteAvailabilityInfo(["GD32F330xB", "GD32F330x8"])}, quirks=[
                ParseUsingAreaQuirk((111.25,123.901,436.444,535.416)),
            ]),
        ],
        pin_defs = [
            # GD32F330Rx
            DatasheetPinDefPageParsingInfo([19], "GD32F330Rx", "LQFP64", [
                ParseUsingAreaQuirk((169.294,123.901,769.079,535.416)),
                OverwritePinDescriptionQuirk("PA2", "Default: PA2\rAlternate: USART1_TX, TIMER1_CH2, TIMER14_CH0\rAdditional: ADC_IN2"),
            ]),
            DatasheetPinDefPageParsingInfo([20], "GD32F330Rx", "LQFP64", [
                ParseUsingAreaQuirk((79.996,122.413,768.335,533.928)),
                OverwritePinDescriptionQuirk("PB12", "Default: PB12\rAlternate: SPI1_NSS, TIMER0_BKIN, I2C1_SMBA, EVENTOUT"),
            ]),
            DatasheetPinDefPageParsingInfo([21], "GD32F330Rx", "LQFP64", [ParseUsingAreaQuirk((80.74,124.645,768.335,533.183))]),
            DatasheetPinDefPageParsingInfo([22], "GD32F330Rx", "LQFP64", [ParseUsingAreaQuirk((81.484,124.645,491.511,533.928))]),
            # GD32F330Cx
            DatasheetPinDefPageParsingInfo([22], "GD32F330Cx", "LQFP48", [ParseUsingAreaQuirk((636.62,123.157,767.591,534.672))]),
            DatasheetPinDefPageParsingInfo([23], "GD32F330Cx", "LQFP48", [ParseUsingAreaQuirk((79.996,117.948,770.567,535.416))]),
            DatasheetPinDefPageParsingInfo([24], "GD32F330Cx", "LQFP48", [
                ParseUsingAreaQuirk((79.996,123.901,759.405,535.416)),
                OverwritePinDescriptionQuirk("PF6", "Default: PF6\rAlternate: I2C0_SCL(3), I2C1_SCL(5)"),
            ]),
            DatasheetPinDefPageParsingInfo([25], "GD32F330Cx", "LQFP48", [ParseUsingAreaQuirk((79.252,123.901,543.602,533.928))]),
            # GD32F330Kx (LQFP32)
            DatasheetPinDefPageParsingInfo([25], "GD32F330Kx", "LQFP32", [ParseUsingAreaQuirk((688.711,123.157,773.544,535.416))]),
            DatasheetPinDefPageParsingInfo([26], "GD32F330Kx", "LQFP32", [ParseUsingAreaQuirk((79.996,123.157,760.893,537.648))]),
            DatasheetPinDefPageParsingInfo([27], "GD32F330Kx", "LQFP32", [ParseUsingAreaQuirk((79.252,121.669,670.851,536.16))]),
            # GD32F330Kx (QFN32) is ommited here, same info as for LQFP32!
            # GD32F330Gx (QFN28)
            DatasheetPinDefPageParsingInfo([30], "GD32F330Gx", "QFN28", [ParseUsingAreaQuirk((230.314,120.18,770.567,534))]),
            DatasheetPinDefPageParsingInfo([31], "GD32F330Gx", "QFN28", [ParseUsingAreaQuirk((77.764,122.413,735.592,536.16))]),
            # GD32F330Fx (TSSOP20)
            DatasheetPinDefPageParsingInfo([32], "GD32F330Fx", "TSSOP20", [ParseUsingAreaQuirk((199.06,123.157,766.847,537.648))]),
            DatasheetPinDefPageParsingInfo([33], "GD32F330Fx", "TSSOP20", [ParseUsingAreaQuirk((79.252,120.924,352.355,536.904))]),
        ],
        series = "GD32F330", # series
        family_type = "B" # family type
    ),
    "GD32F103xx-Datasheet-Rev-2.7.pdf": DatasheetParsingInfo(
        alternate_funcs = [],
        pin_defs = [
            # GD32F103Zx
            DatasheetPinDefPageParsingInfo([21], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((180,123,769,527)),
                OverwritePinDescriptionQuirk("PF6", "Default: PF6\rAlternate: ADC2_IN4, EXMC_NIORD\nRemap: TIMER9_CH0(3)"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([22], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([23], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PG1", "Default: PG1\rAlternate: EXMC_A11"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([24], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PB13", "Default: PB13\rAlternate: SPI1_SCK, USART2_CTS, TIMER0_CH0_ON, I2S1_CK"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([25], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([26], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PC10", "Default: PC10\nAlternate: UART3_TX, SDIO_D2\nRemap: USART2_TX, SPI2_SCK, I2S2_CK"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([27], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            DatasheetPinDefPageParsingInfo([28], "GD32F103Zx", "LQFP144", [
                ParseUsingAreaQuirk((88,123,650,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103Z[FGIK]"]) }),
            # GD32F103Vx
            DatasheetPinDefPageParsingInfo([29], "GD32F103Vx", "LQFP100", [
                ParseUsingAreaQuirk((133,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103V[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"], "ADC2") }),
            DatasheetPinDefPageParsingInfo([30], "GD32F103Vx", "LQFP100", [
                ParseUsingAreaQuirk((88,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103V[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"], "ADC2") }),
            DatasheetPinDefPageParsingInfo([31], "GD32F103Vx", "LQFP100", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PB13", "Default: PB13\nAlternate: SPI1_SCK, USART2_CTS, TIMER0_CH0_ON, I2S1_CK(4)"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103V[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"], "ADC2") }),
            DatasheetPinDefPageParsingInfo([32], "GD32F103Vx", "LQFP100", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PC9", "Default: PB13\nAlternate: TIMER7_CH3(4), SDIO_D1(4)\nRemap: TIMER2_CH3"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103V[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"], "ADC2") }),
            DatasheetPinDefPageParsingInfo([33], "GD32F103Vx", "LQFP100", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PD3", "Default: PD3\nAlternate: EXMC_CLK\nRemap: USART1_CTS"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103V[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103V[CDEFGIK]"], "ADC2") }),            
            # GD32F103Rx
            DatasheetPinDefPageParsingInfo([36], "GD32F103Rx", "LQFP64", [
                ParseUsingAreaQuirk((135,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103R[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"], "ADC2"), "6": FootnoteAvailabilityInfo(["GD32F103R[8BCDEFGIK]"]) }),
            DatasheetPinDefPageParsingInfo([37], "GD32F103Rx", "LQFP64", [
                ParseUsingAreaQuirk((88,123,769,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103R[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"], "ADC2"), "6": FootnoteAvailabilityInfo(["GD32F103R[8BCDEFGIK]"]) }),
            DatasheetPinDefPageParsingInfo([38], "GD32F103Rx", "LQFP64", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PC12", "Default: PC12\rAlternate: UART4_TX(4), SDIO_CK(4)\nRemap: USART2_CK (6), SPI2_MOSI(4), I2S2_SD(4)"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103R[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"], "ADC2"), "6": FootnoteAvailabilityInfo(["GD32F103R[8BCDEFGIK]"]) }),
            DatasheetPinDefPageParsingInfo([39], "GD32F103Rx", "LQFP64", [
                ParseUsingAreaQuirk((135,123,576,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103R[FGIK]"]), "4": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"]), "5": FootnoteAvailabilityInfo(["GD32F103R[CDEFGIK]"], "ADC2"), "6": FootnoteAvailabilityInfo(["GD32F103R[8BCDEFGIK]"]) }),
            # GD32F103Cx
            DatasheetPinDefPageParsingInfo([40], "GD32F103Cx", "LQFP48", [
                ParseUsingAreaQuirk((135,123,769,527)),
                OverwritePinDescriptionQuirk("PB1", "Default: PB1\rAlternate: ADC01_IN9, TIMER2_CH3\nRemap: TIMER0_CH2_ON"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103C[468B]"], "ADC2"), "4": FootnoteAvailabilityInfo(["GD32F103C[8B]"]) }),
            DatasheetPinDefPageParsingInfo([41], "GD32F103Cx", "LQFP48", [
                ParseUsingAreaQuirk((88,123,769,527)),
                OverwritePinDescriptionQuirk("PB3", "Default: JTDO\rRemap: PB3, TRACESWO, TIMER1_CH1, SPI0_SCK"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103C[468B]"], "ADC2"), "4": FootnoteAvailabilityInfo(["GD32F103C[8B]"]) }),
            DatasheetPinDefPageParsingInfo([42], "GD32F103Cx", "LQFP48", [
                ParseUsingAreaQuirk((88,123,476,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103C[468B]"], "ADC2"), "4": FootnoteAvailabilityInfo(["GD32F103C[8B]"]) }),
            # GD32F103Tx
            DatasheetPinDefPageParsingInfo([43], "GD32F103Tx", "LQFP36", [
                ParseUsingAreaQuirk((135,123,769,527)),
                OverwritePinDescriptionQuirk("PA9", "Default: PA9\rAlternate: USART0_TX, TIMER0_CH1"),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103T[468B]"], "ADC2", False), "4": FootnoteAvailabilityInfo(["GD32F103T[8B]"]) }),
            DatasheetPinDefPageParsingInfo([44], "GD32F103Tx", "LQFP36", [
                ParseUsingAreaQuirk((88,123,621,527)),
            ], { "3": FootnoteAvailabilityInfo(["GD32F103T[468B]"], "ADC2", False), "4": FootnoteAvailabilityInfo(["GD32F103T[8B]"]) }),            
        ],
        series = "GD32F10x",
        family_name = "GD32F103xx",
        family_type = "A",
        internal_adc = {
            "ADC_TEMP": ("0", "16"), # (adc, channel)
            "ADC_VREF": ("0", "17"), 
        }
    ),
}

#remapping_infos = [
#    ("PA4", "SPI2_NSS", "GPIO_SPI2_REMAP")
#]

remapping_infos_2 = {
    "GPIO_SPI2_REMAP": {
        "mapping": [
            ("PA4", "SPI2_NSS"),
            ("PA4", "I2S2_WS")
        ]
    }
}

remapping_infos_3 = {
    # when this macro is active, the following pins have these functions.
    # note: we don't say what the "off" (no remap) info is since we don't need it.
    "GPIO_SPI2_REMAP": {
        "PA4": "SPI2_NSS/I2S2_WS",
        "PC10": "SPI2_SCK/I2S2_CK",
        "PC11": "SPI2_MOSI",
        "PC12": "SPI2_MISO/I2S_SD",
    }
}

remapper_infos = {
    "GD32F30x": {
        "GPIO_SPI2_REMAP": {
            "PA4": "SPI2_NSS/I2S2_WS",
            "PC10": "SPI2_SCK/I2S2_CK",
            "PC11": "SPI2_MOSI",
            "PC12": "SPI2_MISO/I2S_SD",
        }
    },
    "GD32F103xx": {
        "NAME_TIMER3_REMAP": {
            "PD12": "TIMER3_CH0"
        },
        "NAME_USART2_FULL_REMAP": {
            "PD12": "USART2_RTS"
        }
    }
}

# This structure will permit remapping of individual pins, but
# what it doesn't describe accurately is the effect remapping
# one pin will have on other pins. For instance, on GD32F103,
# remapping TIMER1_CH2 to PB10 can map TIMER1_CH1 to PA1 or PB3
# depending on the remap. Thus, this structure is also used to 
# provide alternative mappings in the platform, ie PA0_ALT1.
remapper_info = {
    **gd32f10x_remap.remapping_info
}

def identify_datasheet(datasheet_pdf_path: str) -> DatasheetParsingInfo:
    global known_datasheets_infos
    if path.basename(datasheet_pdf_path) in known_datasheets_infos:
        return known_datasheets_infos[path.basename(datasheet_pdf_path)]
    else:
        return None