import pickle
from engine.module_based_naming.TTModules import *
from TT_info import *
from IT_info import *

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













