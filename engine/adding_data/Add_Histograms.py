import pickle
import sys
from Name_Parser import *
from engine.histo_drawing.DefineHistogram import GetAPlot
from engine.detectors.CreateDetectors import *
"""
This function add histograms to detector.
"""

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
            det[hist_name]=create_TT()
            break
        if k in NameList['ITNames']:
            det[hist_name]=create_IT()
            break

    for i, k in enumerate(hist_set):
        p_name = Parse_Name(k)
        if k in NameList['TTNames']:
            det[hist_name][p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]=GetAPlot(hist_set[k], histname = hist_name+"_"+k)
            if hist_name not in hist_coll['tt']:
                hist_coll['tt'][hist_name]=[]
            for pr in det[hist_name][p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]["properties"]:
                if pr not in hist_coll['tt'][hist_name]:
                    hist_coll['tt'][hist_name].append(pr)
        if k in NameList['ITNames']:
            det[hist_name][p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]=GetAPlot(hist_set[k], histname = hist_name+"_"+k)
            if hist_name not in hist_coll['it']:
                hist_coll['it'][hist_name]=[]
            for pr in det[hist_name][p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]["properties"]:
                if pr not in hist_coll['it'][hist_name]:
                    hist_coll['it'][hist_name].append(pr)
        sys.stdout.flush()
        sys.stdout.write("Getting histograms for "+hist_name+":  "+str(i+1)+'/'+ str(len(hist_set))+' ('+ str(int(100*float(i+1)/float(len(hist_set))))+'%)\r')
    print ''
    print hist_name+': all done.'
    return 


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
            det[hist_name][p_name['layer']][p_name['side']][p_name['sector']]['Histograms'][hist_name]={'plot':hist_set[k], "init_properties":{},'properties':{}}
            if hist_name not in hist_coll['tt']:
                hist_coll['tt'][hist_name]=[]
        if k in NameList['ITNames']:
            det[hist_name][p_name['station']][p_name['side']][p_name['layer']][p_name['sector']]['Histograms'][hist_name]={'plot':hist_set[k], "init_properties":{} ,'properties':{}}
            if hist_name not in hist_coll['it']:
                hist_coll['it'][hist_name]=[]
        sys.stdout.flush()
        sys.stdout.write("Getting histograms for "+hist_name+":  "+str(i+1)+'/'+ str(len(hist_set))+' ('+ str(int(100*float(i+1)/float(len(hist_set))))+'%)\r')
    print ''
    print hist_name+': all done.'
    return 
