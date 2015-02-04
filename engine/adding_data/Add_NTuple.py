import pickle
import os
from ROOT import *
from engine.module_based_naming.Alternative_Naming_Triggers import *
from Add_Histograms import *
"""
These functions are used to add histograms from NTuple
"""
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
        output = open('engine/adding_data/pickle/'+d+'.pkl', 'wb')
        pickle.dump(dictionary[d], output)
        output.close()
    return dictionary.keys()

def Add_NTuple(ntuple, it_d, tt_d,hist_coll):
    if not os.path.exists("engine/adding_data/pickle"):
        os.system("mkdir engine/adding_data/pickle")
    for h in GetHistosFromNT(ntuple):
        if h[0] == 'T':
            f = open('engine/adding_data/pickle/'+h+".pkl")
            TT_hists = pickle.load(f)
            #if h not in hist_coll['tt']:
            #    hist_coll['tt'].append(h)
            Add_Histograms(tt_d, TT_hists, h, hist_coll)
        if h[0] == 'I':
            f = open('engine/adding_data/pickle/'+h+".pkl")
            IT_hists = pickle.load(f)
            #if h not in hist_coll['it']:
            #    hist_coll['it'].append(h)
            Add_Histograms(it_d, IT_hists, h, hist_coll)
    return
