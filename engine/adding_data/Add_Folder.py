import os
from engine.module_based_naming.Alternative_Naming_Triggers import *
from Add_NTuple import *
from Add_Histograms import *

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
