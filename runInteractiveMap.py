from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for, request, flash
from ROOT import *
from engine.detectors.CreateDetectors import *
from engine.adding_data.Add_Folder import *
from engine.adding_data.Add_Pkl import *
from engine.adding_data.Add_NTuple import *
from engine.colors.Color_Mapping import *
import pickle
import sys
import os
import json


# Avoid spawning canvases
gROOT.SetBatch(kTRUE)

# Prepare a Flask application
app = Flask(__name__)

# Load the list of unique sector names
f = open('engine/NameList.pkl')
NameList = pickle.load(f)

# Create detectors
tt_d = create_TT()
it_d = create_IT()
histos = {'it':{},'tt':{}}

# Add data in .pkl format
pickle_file = 'data/TT_Efficiency_Per_Run.pkl'
hist_name = 'Efficiency_time_dependence'
Add_Pkl(tt_d, pickle_file, hist_name,histos)

# Add data as ntuple
"""
ntuple = 'data/STTrackMonitor-2012.root'
Add_NTuple(ntuple, it_d, tt_d,histos)
"""

#Add preloaded pctures
#Pay attention, that this folder should be in static folder. (static/<your_folder>)
#Names should be given as <Name_of_Histogram>_<SectorName>.<extension> and they shouldn't contain "-"
"""
folder_with_plots = 'preloaded_pictures'
Add_Folder(folder_with_plots, it_d, tt_d,histos)
"""

#This is needed to make color map
collection = Normalize_Colours(tt_d, it_d)

# Here is some flask magic
@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    global Drawing_mode
    if request.method == 'POST':
        for m in ['IT_hist', 'TT_hist','IT_prop', 'TT_prop']:
            try:
                Drawing_mode[m]=request.form[m]
            except:
                pass
        return render_template('index.html', tt = tt_d, it=it_d, dm = Drawing_mode, collections = collection, hist_coll = histos)
    Drawing_mode = {'TT_hist':'', 'IT_hist':'','TT_prop':'', 'IT_prop':''}
    return render_template('index.html', tt = tt_d, it=it_d, dm = Drawing_mode, collections = collection, hist_coll = histos)
@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', sec=tt_d[p_name['layer']][p_name['side']][p_name['sector']])
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', sec=it_d[p_name['station']][p_name['side']][p_name['layer']][p_name['sector']])
    return redirect(url_for('hello'))


# Execute the program
if __name__ == "__main__":
    Drawing_mode = {'TT_hist':'', 'IT_hist':'','TT_prop':'', 'IT_prop':''}
    app.debug = False # You can make it true if you have an error and want to debug it by yourself
    app.run(port=5000)
