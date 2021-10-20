from os import path
from typing import Dict
from parsing_info import DatasheetAFPageParsingInfo, DatasheetPinDefPageParsingInfo, DatasheetParsingInfo
from parsing_quirks import ParseUsingAreaQuirk, OverwritePinAdditionalInfoQuirk, OverwritePinAlternateInfoQuirk

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
    )
}

def identify_datasheet(datasheet_pdf_path: str) -> DatasheetParsingInfo:
    global known_datasheets_infos
    if path.basename(datasheet_pdf_path) in known_datasheets_infos:
        return known_datasheets_infos[path.basename(datasheet_pdf_path)]
    else:
        return None