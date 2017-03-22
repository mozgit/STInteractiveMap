import pickle
from Add_Histograms import *

def Add_Pkl(detector, pickle_file, hist_name,hist_coll, username="anonimuos", opt_stats_mode = "emr"):
    f = open(pickle_file)
    TT_hists = pickle.load(f)
    hname = hist_name
    Add_Histograms(detector, TT_hists, hname, hist_coll, username, opt_stats_mode)
    return