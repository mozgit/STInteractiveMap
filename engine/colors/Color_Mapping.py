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

def split_number(number):
    if number == 0:
        return{'sing':1,'power':0,'digits':'0'}
    sign = 1
    integers = ""
    decimals = ""
    power = 0
    if number<0:
        sign = -1
    integers = str(abs(number)).split(".")[0]
    try:
        decimals = str(abs(number)).split(".")[1]
    except:
        decimals = ""
    power = len(integers)-1
    if abs(number)<1:
        while (int(number)==0):
            number *=10
            power -=1
    simplified = integers+decimals
    while simplified[len(simplified)-1]=='0':
        simplified = simplified[:-1]
    while simplified[0]=='0':
        simplified=simplified[1:]
    return {'sing':sign,'power':power,'digits':simplified}


def round_up(number, ndigit):
    if number<0:
        return -round_down(-number,ndigit)
    if ndigit < 1:
        print "Warning in smart schema rounding! (Round Up) ndigit = "+str(ndigit)+", returning original number"
        return number
    simplified = split_number(number)['digits']
    power = split_number(number)['power']
    temp = ""
    if len(simplified)<ndigit:
        #simplified=str(int(simplified)+1)
        while len(simplified)<ndigit:
            simplified+='0'
        for i in range(0, ndigit):
            temp+=simplified[i]
        rn = int(temp)+1
        return float(rn)/10**(len(str(temp))-1)*10**(power)
    for i in range(0, ndigit):
        temp+=simplified[i]
    rn = int(temp)+1
    return float(rn)/10**(len(str(temp))-1)*10**(power)

def round_down(number, ndigit):
    if number<0:
        return -round_down(-number,ndigit)
    if ndigit < 1:
        print "Warning in smart schema rounding! (Round Down) ndigit = "+str(ndigit)+", returning 0"
        return 0
    simplified = split_number(number)['digits']
    power = split_number(number)['power']
    temp = ""
    if len(simplified)<ndigit:
        simplified=str(int(simplified)+1)
        while len(simplified)<ndigit:
            simplified+='0'
        for i in range(0, ndigit):
            temp+=simplified[i]
        rn = int(temp)-1
        return float(rn)/10**(len(str(temp))-1)*10**(power)
    for i in range(0, ndigit):
        temp+=simplified[i]
    rn = int(temp)-1
    return float(rn)/10**(len(str(temp))-1)*10**(power)



def smart_interval(min_l, max_l, ndigit):
    if (min_l<0) and (max_l<0):
        return [-smart_interval(-max_l,-min_l,ndigit)[1],-smart_interval(-max_l,-min_l,ndigit)[0]]
    d_min = split_number(min_l)['digits']
    d_max = split_number(max_l)['digits']
    p_min = split_number(min_l)['power']
    p_max = split_number(max_l)['power']
    if (min_l<0) and (max_l>0):
        return [-round_up(max(max_l,-min_l),2),round_up(max(max_l,-min_l),2)]

    d_pow = p_max-p_min
    if d_pow!=0:
        for i in range(0, d_pow):
            d_min = '0'+d_min


    if len(d_max)<ndigit:
        if len(d_min)<ndigit:
            return [min_l,max_l]
        return [round_down(min_l,ndigit),max_l]
    if len(d_min)<ndigit:
        return [min_l,round_up(max_l,ndigit)]

    counter = 0
    i = 0
    while counter<ndigit:
        if d_max[i]!=d_min[i]:
            counter+=1
        i+=1
    print "("+str(min_l)+", "+str(max_l)+") ="+str(i)+"=> ("+str(round_down(min_l,i-d_pow))+", "+str(round_up(max_l,i))+")"
    return [round_down(min_l,i-d_pow),round_up(max_l,i)]


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
        collection[coll]['min']=smart_interval(min(collection[coll]['vals']),max(collection[coll]['vals']),2)[0]
        collection[coll]['max']=smart_interval(min(collection[coll]['vals']),max(collection[coll]['vals']),2)[1]
        norm = mpl.colors.Normalize(vmin=collection[coll]['min'], vmax=collection[coll]['max'])
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        for i in range(0,100):
            collection[coll][str(i)] = {}
            collection[coll][str(i)]['colour'] = convert_to_hex(m.to_rgba(collection[coll]['min'] + float(i)/100.*(collection[coll]['max']-collection[coll]['min'])))
            collection[coll][str(i)]['value'] = str(collection[coll]['min'] + float(i)/100.*(collection[coll]['max']-collection[coll]['min']))
        collection[coll]['99']['value'] = str(collection[coll]['max']) 
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

