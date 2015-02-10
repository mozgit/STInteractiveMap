import matplotlib as mpl
import matplotlib.cm as cm

"""
These functions provide color mapping of a IT/TT according to functions from histograms.
You can define your own functions at histo_drawing/DefineHistogram.py
"""

def convert_to_hex(rgba_color) :
    red = int(rgba_color[0]*255)
    green = int(rgba_color[1]*255)
    blue = int(rgba_color[2]*255)
    return '#{r:02x}{g:02x}{b:02x}'.format(r=red,g=green,b=blue)

def Normalize_Colours(tt_d, it_d):
    collection = {}
    cmap = cm.PiYG
    #Create collection of properties:
    #collection = {'tt+hist+property':{
    #                                'vals':[]
    #                                'min':
    #                                'max':
    #                                'bin_number':{colour_code, value}
    #                               }}
    #print json.dumps(tt_d,sort_keys=True, indent=4)
    for layer in tt_d:
        for side in tt_d[layer]:
            if side not in ["layer_info"]:
                for sector in tt_d[layer][side]:
                    if sector not in ["side_info"]:
                        if tt_d[layer][side][sector]['is_masked'] == False:
                            for hist in tt_d[layer][side][sector]['Histograms']:
                                for prop in tt_d[layer][side][sector]['Histograms'][hist]['properties']:
                                    if 'tt_d'+hist+prop not in collection:
                                        collection['tt_d'+hist+prop]={'vals':[], 'min':'', 'max':''}
                                    collection['tt_d'+hist+prop]['vals'].append(tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop])
    for station in it_d:
        for side in it_d[station]:
            if side not in ["station_info"]:
                for layer in it_d[station][side]:
                    if layer not in ["side_info"]:
                        for sector in it_d[station][side][layer]:
                            if sector not in ["layer_info"]:
                                if it_d[station][side][layer][sector]['is_masked'] == False:
                                    for hist in it_d[station][side][layer][sector]['Histograms']:
                                        for prop in it_d[station][side][layer][sector]['Histograms'][hist]['properties']:
                                            if 'it_d'+hist+prop not in collection:
                                                collection['it_d'+hist+prop]={'vals':[], 'min':'', 'max':''}
                                            collection['it_d'+hist+prop]['vals'].append(it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop])
    for coll in collection:
        collection[coll]['min']=min(collection[coll]['vals'])
        collection[coll]['max']=max(collection[coll]['vals'])
        norm = mpl.colors.Normalize(vmin=collection[coll]['min'], vmax=collection[coll]['max'])
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        for i in range(0,100):
            collection[coll][str(i)] = {}
            collection[coll][str(i)]['colour'] = convert_to_hex(m.to_rgba(collection[coll]['min'] + float(i)/100.*(collection[coll]['max']-collection[coll]['min'])))
            collection[coll][str(i)]['value'] = str(collection[coll]['min'] + float(i)/100.*(collection[coll]['max']-collection[coll]['min']))
    #print json.dumps(collection,sort_keys=True, indent=4)
    for layer in tt_d:
        for side in tt_d[layer]:
            if side not in ["layer_info"]:
                for sector in tt_d[layer][side]:
                    if sector not in ["side_info"]:
                        for hist in tt_d[layer][side][sector]['Histograms']:
                            for prop in tt_d[layer][side][sector]['Histograms'][hist]['properties']:
                                if tt_d[layer][side][sector]['is_masked'] == False:
                                    norm = mpl.colors.Normalize(vmin=collection['tt_d'+hist+prop]['min'], vmax=collection['tt_d'+hist+prop]['max'])
                                    m = cm.ScalarMappable(norm=norm, cmap=cmap)
                                    tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop] = convert_to_hex(m.to_rgba(tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop]))
                                else:
                                    tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop] = "#000000"
                                #print m.to_rgba(tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop],bytes=True)
    for station in it_d:
        for side in it_d[station]:
            if side not in ["station_info"]:
                for layer in it_d[station][side]:
                    if layer not in ["side_info"]:
                        for sector in it_d[station][side][layer]:
                            if sector not in ["layer_info"]:
                                for hist in it_d[station][side][layer][sector]['Histograms']:
                                    for prop in it_d[station][side][layer][sector]['Histograms'][hist]['properties']:
                                        if it_d[station][side][layer][sector]['is_masked'] == False:
                                            norm = mpl.colors.Normalize(vmin=collection['it_d'+hist+prop]['min'], vmax=collection['it_d'+hist+prop]['max'])
                                            m = cm.ScalarMappable(norm=norm, cmap=cmap)
                                            it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop] = convert_to_hex(m.to_rgba(it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop]))
                                        else:
                                            it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop] = "#000000"
    return collection

