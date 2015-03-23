from engine.adding_data.Name_Parser import *

def mask_sector(coll_it_d, coll_tt_d, sector):
    ps = Parse_Name(sector)
    if ps['station']:
        for h in coll_it_d:
            coll_it_d[h][ps['station']][ps['side']][ps['layer']][ps['sector']]['is_masked'] = True
    else:
        for h in coll_tt_d:
            coll_tt_d[h][ps['side']][ps['layer']][ps['sector']]['is_masked'] = True
    return
