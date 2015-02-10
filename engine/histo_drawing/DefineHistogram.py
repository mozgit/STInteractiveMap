from ROOT import *
import os

if not os.path.exists("static/plots"):
    os.system("mkdir static/plots")

def GetAPlot(hist,histname):
    """ Looks for a png files. If it is not there,
    it produces it by saving a ROOT histogram  as .png """
    if not os.path.isfile("static/plots/"+histname+".png"):
        gROOT.ProcessLine(".x lhcbStyle.C")
        gStyle.SetOptStat("emr")
        gStyle.SetPadTopMargin(0.06) 
        c = TCanvas("c","c", 900, 900)
        hist.Draw()
        c.SaveAs("static/plots/"+histname+".png")
    dic = {"plot":"plots/"+histname+".png", "init_properties":{}, "properties":{'mean':hist_mean(hist)
                                                            , 'sigma':hist_sigma(hist)
                                                            , 'Y_mean':Y_mean(hist)
                                                            , 'slope':slope(hist)
                                                            , 'smoothness':chi2_lin(hist)
                                                            }}
    for p in dic['properties']:
        dic['init_properties'][p]=dic['properties'][p]

    return dic

def hist_mean(hist):
    return hist.GetMean()

def hist_sigma(hist):
    return hist.GetRMS()

def Y_mean(hist):
    hist.Fit("pol0")
    f = hist.GetFunction("pol0","q") #q - to make fit silent
    try:
        return f.GetParameter(0)
    except:
        return 0

def slope(hist):
    hist.Fit("pol1")
    f = hist.GetFunction("pol1","q") #q - to make fit silent
    try:
        return f.GetParameter(1)
    except:
        return 0

def chi2_lin(hist):
    hist.Fit("pol1")
    f = hist.GetFunction("pol1","q") #q - to make fit silent
    try:
        return f.GetChisquare()
    except:
        return 0