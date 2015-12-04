from app import app
from ROOT import *
from flask import render_template
from flask import abort, redirect, url_for, request, flash
from engine.colors.Color_Mapping import *
from app.supplimentaryfunctions import *
from werkzeug import secure_filename
import pickle
import sys
import json
from app.models import *
#from app.auth import requires_auth
from app.auth import *
from app import it_d as g_it_d
from app import tt_d as g_tt_d
from app import histos, collection, coll_it_d, coll_tt_d, Drawing_mode
from flask import make_response
from flask.ext.login import login_required
import flask.ext.login as flask_login
# Avoid spawning canvases
gROOT.SetBatch(kTRUE)

# Make stylish plots
gROOT.ProcessLine(".x engine/histo_drawing/lhcbStyle.C")

# Load the list of unique sector names

f = open('engine/NameList.pkl')
NameList = pickle.load(f)


@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['email']
    users = get_users()
    if email in users:
        if request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            if request.form['wantsurl']:
                #print "*"*100
                #request.form['wantsurl']
                #print "*"*100
                return redirect(request.form['wantsurl'])
                
            else:
                #print "F"*100
                return redirect(url_for('.hello'))
    return render_template('Login.html', wantsurl=url_for('hello'))

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route("/configure",methods = ('GET', 'POST'))
def configure():
    global histos
    global coll_tt_d
    global coll_it_d
    global collection
    if request.method == 'POST':
        if request.form['btn'] == 'Edit histograms list':
            existing_plots_IT = {}
            existing_plots_TT = {}
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    if mp.owner not in existing_plots_TT:
                        existing_plots_TT[mp.owner]=[]
                    existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
                if mp.dtype == 'IT':
                    if mp.owner not in existing_plots_IT:
                        existing_plots_IT[mp.owner]=[]
                    existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos))
        if request.form['btn'] == 'Configure':
            for mp in MappedPlot.objects.all():
                mp.remove_from_detector()
                if mp.__unicode__() in request.form:
                    if request.form[mp.__unicode__()] == 'on':
                        if not mp.is_loaded():
                            mp.add_to_detector()
            #collection = Normalize_Colours(coll_tt_d, coll_it_d)
            return redirect(url_for('hello'))
    existing_plots_IT = {}
    existing_plots_TT = {}
    for mp in MappedPlot.objects.all():
        if mp.dtype == 'TT':
            if mp.owner not in existing_plots_TT:
                existing_plots_TT[mp.owner]=[]
            existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
        if mp.dtype == 'IT':
            if mp.owner not in existing_plots_IT:
                existing_plots_IT[mp.owner]=[]
            existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
    #print existing_plots_IT
    return render_template('Configure.html', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT, hist_coll = histos)






@app.route("/edit",methods = ('GET', 'POST'))
@login_required
def edit():
    global coll_tt_d
    global coll_it_d
    global collection
    if request.method == 'POST':

        if request.form['btn'] == 'Upload':
            files = request.files.getlist("file[]")
            prefix = "".join(c for c in request.form['text'] if c.isalnum())+"::"+flask_login.current_user.id
            comment = request.form['comment']
            #print comment
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_address = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_address)
                    #print "*"*100
                    #print "Adding file with owner "+flask_login.current_user.id
                    add_file(filename, prefix, flask_login.current_user.id, comment)
                    #print "*"*100
                    #print "Added file with owner "+flask_login.current_user.id                    
                    os.system("rm "+file_address)
            existing_plots_IT = {}
            existing_plots_TT = {}
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    if mp.owner not in existing_plots_TT:
                        existing_plots_TT[mp.owner]=[]
                    existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
                if mp.dtype == 'IT':
                    if mp.owner not in existing_plots_IT:
                        existing_plots_IT[mp.owner]=[]
                    existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT))

        if request.form['btn'] == 'Remove':
            for mp in MappedPlot.objects.all():
                if mp.__unicode__() in request.form:
                    if (flask_login.current_user.id == 'admin') or (flask_login.current_user.id == mp.owner):
                        mp.remove_plots()
                        mp.remove_from_detector()
                        mp.remove_color_map()
                        MappedPlot.objects.get(name=mp.__unicode__()).delete()
            existing_plots_IT = {}
            existing_plots_TT = {}
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    if mp.owner not in existing_plots_TT:
                        existing_plots_TT[mp.owner]=[]
                    existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
                if mp.dtype == 'IT':
                    if mp.owner not in existing_plots_IT:
                        existing_plots_IT[mp.owner]=[]
                    existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT))

        if request.form['btn'] == 'Remove all':
            for mp in MappedPlot.objects.all():
                if (flask_login.current_user.id == 'admin') or (flask_login.current_user.id == mp.owner):
                    mp.remove_plots()
                    mp.remove_from_detector()
                    mp.remove_color_map()
                    MappedPlot.objects.get(name=mp.__unicode__()).delete()
            existing_plots_IT = {}
            existing_plots_TT = {}
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    if mp.owner not in existing_plots_TT:
                        existing_plots_TT[mp.owner]=[]
                    existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
                if mp.dtype == 'IT':
                    if mp.owner not in existing_plots_IT:
                        existing_plots_IT[mp.owner]=[]
                    existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
            return redirect(url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT))

        if request.form['btn'] == 'Change user':
            existing_plots_IT = {}
            existing_plots_TT = {}
            for mp in MappedPlot.objects.all():
                if mp.dtype == 'TT':
                    if mp.owner not in existing_plots_TT:
                        existing_plots_TT[mp.owner]=[]
                    existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
                if mp.dtype == 'IT':
                    if mp.owner not in existing_plots_IT:
                        existing_plots_IT[mp.owner]=[]
                    existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
            flask_login.logout_user()
            return render_template('Login.html', wantsurl=url_for('.edit', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT))

    existing_plots_IT = {}
    existing_plots_TT = {}
    for mp in MappedPlot.objects.all():
        if mp.dtype == 'TT':
            if mp.owner not in existing_plots_TT:
                existing_plots_TT[mp.owner]=[]
            existing_plots_TT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
        if mp.dtype == 'IT':
            if mp.owner not in existing_plots_IT:
                existing_plots_IT[mp.owner]=[]
            existing_plots_IT[mp.owner].append({'name':mp.__unicode__(),'comment':mp.comment})
    return render_template('Edit.html', existing_plots_TT = existing_plots_TT, existing_plots_IT = existing_plots_IT)




# Here is some flask magic
@app.route("/",methods = ('GET', 'POST'))
@app.route("/index",methods = ('GET', 'POST'))
def hello():
    global Drawing_mode
    global coll_tt_d
    global coll_it_d
    global g_tt_d
    global g_it_d
    global collection
    global histos
    if request.method == 'POST':
        for m in ['IT_hist', 'TT_hist','IT_prop', 'TT_prop']:
            try:
                Drawing_mode[m]=request.form[m]
            except:
                pass
        return render_template('index.html', coll_tt = coll_tt_d, coll_it=coll_it_d, dm = Drawing_mode, collections = collection, hist_coll = histos, tt = g_tt_d, it = g_it_d)
    #collection = Retrieve_Collection(histos)
    collection = Normalize_Colours(coll_tt_d, coll_it_d)
    Drawing_mode = {'TT_hist':'', 'IT_hist':'','TT_prop':'', 'IT_prop':''}
    #print json.dumps(collection,sort_keys=True, indent=4)
    #print json.dumps(histos,sort_keys=True, indent=4)
    return render_template('index.html', coll_tt = coll_tt_d, coll_it=coll_it_d, dm = Drawing_mode, collections = collection, hist_coll = histos, tt = g_tt_d, it = g_it_d)

@app.route("/<d>",methods = ('GET', 'POST'))
def Detector(d):
    if d in NameList['TTNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "TT", name = d, sec=p_name, det = coll_tt_d)
    if d in NameList['ITNames']: 
        p_name = Parse_Name(d)
        return render_template('Sector.html', dtype = "IT", name = d, sec=p_name, det = coll_it_d)
    return redirect(url_for('hello'))



    """
    #collection = {'tt+hist+property':{
    #                                'owner':
    #                                'vals':[]
    #                                'min':
    #                                'max':
    #                                'bin_number':{colour_code, value}
    #                               }}
    #I.E. Collection is just color schema of given histogram
    #histos ={
    #"it": {
    #    "IT_::Ilya_Residual": [
    #        "slope", 
    #        "Y_mean", 
    #        "max_variation", 
    #        "min_y", 
    #        "max_y", 
    #        "sigma", 
    #        "smoothness", 
    #        "mean"
    #    ],
    #   ...
    #}, 
    #"tt":{ 
    #...
    #}
    #I.e. Histos just conutain all properties of shown histograms.
    #So having histos, one can create collection from db.
    """
