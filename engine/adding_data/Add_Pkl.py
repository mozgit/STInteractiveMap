import pickle
from Add_Histograms import *

def Add_Pkl(detector, pickle_file, hist_name,hist_coll):
    f = open(pickle_file)
    TT_hists = pickle.load(f)
    hname = hist_name
    Add_Histograms(detector, TT_hists, hname, hist_coll)
    return