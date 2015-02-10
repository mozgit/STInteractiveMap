from engine.adding_data.Name_Parser import *

def mask_sector(it_d, tt_d, sector):
    ps = Parse_Name(sector)
    if ps['station']:
        it_d[ps['station']][ps['side']][ps['layer']][ps['sector']]['is_masked'] = True
    else:
        tt_d[ps['side']][ps['layer']][ps['sector']]['is_masked'] = True
    return
