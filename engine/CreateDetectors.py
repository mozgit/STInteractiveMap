"""
This script creates dictionaries with the names of IT and TT sectors
Sectors can be accessed through:
for i in IT.values():
    for j in i.values():
        for k in j.values():
            print k.values()
or
for i in TT.values():
    for j in i.values():
        print j.values():

"""
import pickle
from DefineHistogram import GetAPlot
from ROOT import *
import re
import sys
import os
import matplotlib as mpl
import matplotlib.cm as cm
import json
from TTModules import *

def TT_reg_len(det,region):
    top = 25
    if ((det[2]=='a') and (region == 'RegionB')):
        top = 19
    if ((det[2]=='b') and (region == 'RegionB')):
        top = 27
    return range(1, top)


def TT_div_info(det, region, sector):
    nX = 6
    nY = 4
    sector_iy = sector-1
    sector_ix = sector-1
    if ((det[2]=='a') and (region == 'RegionB')):
        nX = 3
        nY = 6
    if ((det[2]=='b') and (region == 'RegionB')):
        nX = 5
        if ((sector>4) and (sector<23)):
            sector_iy = sector+1
            sector_ix = sector+1
            nY = 6
        if (sector>22):
            sector_iy = sector-7
            sector_ix = sector-7

    width = str(float(100*1./nX))+"%"
    height = str(float(100*1./nY))+"%"
    top = str(float(100*1./nY)*(nY-sector_iy%nY-1))+"%"
    left = str(float(100*1./nX)*(nX-int((sector_ix-sector_ix%nY)/nY)-1))+"%"
    return {'width':width, 
            'height':height, 
            'top':top, 
            'left':left,
            'position':'absolute',
            'border':' 1px solid #000000',
            'text-align':'center'}


def TT_layer_info(a):
    if a == 'TTaU':
        return {'position':'absolute',
                'top': '0%',
                'left': '0%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTaX':
        return {'position':'absolute',
                'top': '0%',
                'left': '50%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTbV':
        return {'position':'absolute',
                'top': '50%',
                'left': '0%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    if a == 'TTbX':
        return {'position':'absolute',
                'top': '50%',
                'left': '50%',
                'width':'50%',
                'height':'50%',
                'border':'1px dashed'}
    return {}


def TT_side_info(a,r):
    if (r == 'RegionA'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 0%',
                                'width':'32%',
                                'height':'99%'}

    if (r == 'RegionB'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 33.3%',
                                'width':'32%',
                                'height':'99%'}

    if (r == 'RegionC'): return {'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 66.6%',
                                'width':'32%',
                                'height':'99%'}
    return {}


def IT_station_info(st):
    if st == 'IT1': return{'position':'absolute',
                            'top': '0%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    if st == 'IT2': return{'position':'absolute',
                            'top': '33.3%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    if st == 'IT3': return{'position':'absolute',
                            'top': '66.6%',
                            'left': '0%',
                            'width':'100%',
                            'height':'33.3%',
                            'border':'1px dashed',
                            'text-align':'left'}
    return {}


def IT_side_info(st,s):
    
    if s == 'ASide': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 30%',
                                'left':' 0%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'CSide': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 30%',
                                'left':' 66.6%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'Bottom': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 60%',
                                'left':' 33.3%',
                                'width':'33.3%',
                                'height':'40%'}
    if s == 'Top': return{'position':'absolute',
                                'border':' 1px solid ',
                                'top':' 0%',
                                'left':' 33.3%',
                                'width':'33.3%',
                                'height':'40%'}
    return {}


def IT_layer_info(st,s,l):
    if l == 'X1': return {'position':'absolute',
                        'top':' 0%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'U': return {'position':'absolute',
                        'top':' 25%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'V': return {'position':'absolute',
                        'top':' 50%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    if l == 'X2': return {'position':'absolute',
                        'top':' 75%',
                        'left':' 0%',
                        'width':'100%',
                        'height':'25%'}
    return {}


def Parse_Name(d):
    """ Parses station, side, layer and sector
    from a unique sector name """
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f)
    if d in NameList['TTNames']:
        return {'side':d[4:11],'layer':d[0:4],'sector':d[17:],'station':''}
    if d in NameList['ITNames']:
        station = d[0:3]
        sides = {'A':'ASide', 'B':'Bottom', 'C':'CSide', 'T':'Top'}
        side = sides[d[3]]
        layer = d[3+len(side):3+len(side)+1]
        if layer=='X':
            layer = d[3+len(side):3+len(side)+2]
        sector = str(d[len(d)-1])
        return {'station':station,'side':side,'layer':layer,'sector':sector}
    return d


def IT_div_info(st,s,l,n):
    nX = 7
    width = str(float(1./nX)*100)+"%"
    height = "100%"
    top = "0%"
    left = str(float(nX-n)/nX*100)+"%"
    return {'width':width, 
            'height':height, 
            'top':top, 
            'left':left,
            'position':'absolute',
            'border':'1px solid #000000',
            'text-align':'center'}


def create_TT():
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    TT = {}
    layer = ['TTaU','TTaX','TTbV','TTbX']
    side = ['RegionA','RegionB','RegionC']
    for l in layer:
        TT[l]={'layer_info':TT_layer_info(l)}
        for si in side:
            TT[l][si]={'side_info': TT_side_info(l,si)}
            for s in TT_reg_len(l,si):
                Info = {'Name':l+si+'Sector'+str(s), 'div_info':TT_div_info(l,si,s),'Histograms':{}}
                #if a+r+'Sector'+str(s) in NameList['TTNames']:
                TT[l][si][str(s)] = Info
                    #print a+r+'Sector'+str(s)
    return TT


def create_IT():
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    IT = {}
    station = ['IT1','IT2','IT3']
    side = ['ASide','CSide','Bottom','Top']
    layer = ['X1','X2','U','V']
    for st in station:
        IT[st]={'station_info':IT_station_info(st)}
        for s in side:
            IT[st][s]= {'side_info':IT_side_info(st,s)}
            for l in layer:
                IT[st][s][l]={'layer_info':IT_layer_info(st,s,l)}
                for n in range(1,8):
                    Info = {'Name':st+s+l+'Sector'+str(n), 'div_info':IT_div_info(st,s,l,n),'Histograms':{}}
                    IT[st][s][l][str(n)]=Info
    return IT


def Add_Histograms(det, hist_set, hist_name='hist',hist_coll={'it':{}, 'tt':{}}):
    """ Adds a plot for every sector to the detector dictionary

    Inputs:
    - det is an instance of create_TT or create_IT
    - hist_set is a set of histograms loaded from a pickle file
    - hist_name is the name of the set of histograms (e.g. TT_UnbiasedResidual_)
    """
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    print "Creating histograms for "+hist_name
    print ""
    for i, k in enumerate(hist_set):
        p_name = Parse_Name(k)
        if k in NameList['TTNames']:
            det[p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]=GetAPlot(hist_set[k], histname = hist_name+"_"+k)
            if hist_name not in hist_coll['tt']:
                hist_coll['tt'][hist_name]=[]
            for pr in det[p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]["properties"]:
                if pr not in hist_coll['tt'][hist_name]:
                    hist_coll['tt'][hist_name].append(pr)
        if k in NameList['ITNames']:
            det[p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]=GetAPlot(hist_set[k], histname = hist_name+"_"+k)
            if hist_name not in hist_coll['it']:
                hist_coll['it'][hist_name]=[]
            for pr in det[p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]["properties"]:
                if pr not in hist_coll['it'][hist_name]:
                    hist_coll['it'][hist_name].append(pr)
        sys.stdout.flush()
        sys.stdout.write("Getting histograms for "+hist_name+":  "+str(i+1)+'/'+ str(len(hist_set))+' ('+ str(int(100*float(i+1)/float(len(hist_set))))+'%)\r')
    print ''
    print hist_name+': all done.'
    return 


def CheckIfModule(name):
    try: 
        a = sectorsInModule(name)
        return True
    except:
        return False

def CheckIfHalfModule(name):
    try: 
        a = sectorsInHalfModule(name)
        return True
    except:
        return False


def SniffInfo(f, dictionary, names):
    """ Populates a dictionary of the content of the ROOT file
    (in this case, TH1D histograms) """
    for k in f.GetListOfKeys():
        t = k.GetClassName()
        element_name = k.GetName()
        if t == 'TH1D' or t == 'TH1F' or t == 'TH1I':
            #Here we deal with module-based binning.
            orig_histo_name = element_name
            try:
                element_name = orig_histo_name.split('_')[1] # parse histogram name for ST element name
            except:
                pass
            extracted_sector_names = [element_name]
            if CheckIfHalfModule(element_name):
                extracted_sector_names = sectorsInHalfModule(element_name)[0]
            if CheckIfModule(element_name):
                extracted_sector_names = sectorsInModule(element_name)[0]
            for name in extracted_sector_names:
                for sector_name in names['ITNames']:
                    if sector_name == name[len(name) - len(sector_name):]:
                        #naming_schema = 'IT_'+re.sub(sector_name,'',name)
                        naming_schema = 'IT_'+orig_histo_name.split('_')[0]
                        if naming_schema not in dictionary.keys():
                            dictionary[naming_schema] = {}
                        dictionary[naming_schema][sector_name] = f.Get(orig_histo_name)
                        #print dictionary[naming_schema][name]
                for sector_name in names['TTNames']:
                    if sector_name == name[len(name) - len(sector_name):]:
                        #naming_schema = 'TT_'+re.sub(sector_name,'',name)
                        naming_schema = 'TT_'+orig_histo_name.split('_')[0]
                        if naming_schema not in dictionary.keys():
                            dictionary[naming_schema] = {}
                        dictionary[naming_schema][sector_name] = f.Get(orig_histo_name)
                        #print dictionary[naming_schema][name]
        if t == 'TDirectoryFile':
            SniffInfo(f.Get(element_name), dictionary, names)
    return dictionary


def GetHistosFromNT(f_n):
    """ Dumps the histograms of a ROOT file into pikle files
    according to the histogram name """
    nf = open('engine/NameList.pkl')
    names = pickle.load(nf)
    print 'Opening file %s ...'%f_n
    f = TFile(f_n)
    dictionary = {}
    dictionary = SniffInfo(f, dictionary, names)
    for d in dictionary:
        output = open('pickle/'+d+'.pkl', 'wb')
        pickle.dump(dictionary[d], output)
        output.close()
    return dictionary.keys()

def CreateHistSetFromFilesInFolder(folder):
    hist_set = {}
    return hist_set


def Add_Existing_Histograms(det, hist_set, hist_name='hist',hist_coll={'it':{}, 'tt':{}}):
    """ Adds already existing plot for every sector to the detector dictionary - needed for plots compiled elsewhere

    Inputs:
    - det is an instance of create_TT or create_IT (det -  from detector)
    - hist_set is a dictionary {sector_name, histogram_address}
    - hist_name is the name of the set of histograms (e.g. TT_UnbiasedResidual_)
    """
    f = open('engine/NameList.pkl')
    NameList = pickle.load(f) 
    print "Creating histograms for "+hist_name
    print ""
    for i, k in enumerate(hist_set):
        p_name = Parse_Name(k)
        if k in NameList['TTNames']:
            det[p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]={'plot':hist_set[k], "init_properties":{},'properties':{}}
            if hist_name not in hist_coll['tt']:
                hist_coll['tt'][hist_name]=[]
        if k in NameList['ITNames']:
            det[p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]={'plot':hist_set[k], "init_properties":{} ,'properties':{}}
            if hist_name not in hist_coll['it']:
                hist_coll['it'][hist_name]=[]
        sys.stdout.flush()
        sys.stdout.write("Getting histograms for "+hist_name+":  "+str(i+1)+'/'+ str(len(hist_set))+' ('+ str(int(100*float(i+1)/float(len(hist_set))))+'%)\r')
    print ''
    print hist_name+': all done.'
    return 

def Add_Folder(folder_with_plots, it_d, tt_d,hist_coll):
    files = os.listdir('static/'+folder_with_plots)
    it_pictures = {}
    tt_pictures = {}
    for pic in files:
        if pic[len(pic)-5:] == '.root':
            Add_NTuple('static/'+folder_with_plots+'/'+pic, it_d, tt_d)
            continue
        if pic[len(pic)-4:] == '.pdf':
            if pic[:-4]+'.png' in files:
                continue
            os.system('convert static/'+folder_with_plots+'/'+pic+' static/'+folder_with_plots+'/'+pic[:-4]+'.png')
            pic = pic[:-4]+'.png'
        if pic.split('.')[0]=='':
            continue

        if '-' in pic.split('.')[0]:
            #This is for <HistType>-<SectorName>.<extension>
            #naming schema
            pic_name = pic.split('.')[0].split('-')[0]
            hist_name = pic.split('.')[0].split('-')[1]
            pic_ext = '.'+pic.split('.')[1]
        elif "_" in pic.split('.')[0]:
            #This is for <HistType>_<SectorName>.<extension> 
            #naming schema
            pic_name = pic.split('.')[0].split("_")[len(pic.split('.')[0].split("_"))-1]
            hist_name = pic.split('.')[0].replace(pic_name,"")
            pic_ext = '.'+pic.split('.')[1]
        else:
            pic_name = pic.split('.')[0]
            pic_ext = '.'+pic.split('.')[1]
            hist_name = folder_with_plots

        sectorNames = [pic_name]
        if CheckIfHalfModule(pic_name):
            sectorNames = sectorsInHalfModule(pic_name)[0]
        if CheckIfModule(pic_name):
            sectorNames = sectorsInModule(pic_name)[0]
        for sector in sectorNames:
            if sector[0] == 'T':
                if hist_name not in tt_pictures:
                    tt_pictures[hist_name] = {}
                tt_pictures[hist_name][sector]=folder_with_plots+'/'+pic
            if sector[0] == 'I':
                if hist_name not in it_pictures:
                    it_pictures[hist_name] = {}
                it_pictures[hist_name][sector]=folder_with_plots+'/'+pic
    for histos in it_pictures:
        if histos not in hist_coll['it']:
            hist_coll['it'][histos]=[]
        Add_Existing_Histograms(it_d, it_pictures[histos], histos,hist_coll)
    for histos in tt_pictures:
        if histos not in hist_coll['tt']:
            hist_coll['tt'][histos]=[]
        Add_Existing_Histograms(tt_d, tt_pictures[histos], histos,hist_coll)
    return

def Add_NTuple(ntuple, it_d, tt_d,hist_coll):
    for h in GetHistosFromNT(ntuple):
        if h[0] == 'T':
            f = open('pickle/'+h+".pkl")
            TT_hists = pickle.load(f)
            #if h not in hist_coll['tt']:
            #    hist_coll['tt'].append(h)
            Add_Histograms(tt_d, TT_hists, h, hist_coll)
        if h[0] == 'I':
            f = open('pickle/'+h+".pkl")
            IT_hists = pickle.load(f)
            #if h not in hist_coll['it']:
            #    hist_coll['it'].append(h)
            Add_Histograms(it_d, IT_hists, h, hist_coll)
    return

def Add_Pkl(detector, pickle_file, hist_name,hist_coll):
    f = open(pickle_file)
    TT_hists = pickle.load(f)
    hname = hist_name
    #try: 
    #    if detector['layer_info']:
    #        if hist_name not in hist_coll['tt']:
    #            hist_coll['tt'].append(hist_name)
    #except:
    #    if hist_name not in hist_coll['it']:
    #        hist_coll['it'].append(hist_name)
    Add_Histograms(detector, TT_hists, hname, hist_coll)
    return

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
                                norm = mpl.colors.Normalize(vmin=collection['tt_d'+hist+prop]['min'], vmax=collection['tt_d'+hist+prop]['max'])
                                m = cm.ScalarMappable(norm=norm, cmap=cmap)
                                tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop] = convert_to_hex(m.to_rgba(tt_d[layer][side][sector]['Histograms'][hist]['properties'][prop]))
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
                                        norm = mpl.colors.Normalize(vmin=collection['it_d'+hist+prop]['min'], vmax=collection['it_d'+hist+prop]['max'])
                                        m = cm.ScalarMappable(norm=norm, cmap=cmap)
                                        it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop] = convert_to_hex(m.to_rgba(it_d[station][side][layer][sector]['Histograms'][hist]['properties'][prop]))
    return collection
