import os
from flask import Flask, request, redirect, url_for, Response
from flask.ext.mongoengine import MongoEngine
from engine.detectors.CreateDetectors import *
#from flask.ext.login import LoginManager


tt_d = create_TT()
it_d = create_IT()
histos = {'it':{},'tt':{}}
collection = {}
coll_tt_d = {}
coll_it_d = {}
Drawing_mode = {'TT_hist':'', 'IT_hist':'','TT_prop':'', 'IT_prop':''}

dead_sector = ['IT1BottomX2Sector7', 'IT3TopX1Sector7']


UPLOAD_FOLDER = 'app/temp/'
ALLOWED_EXTENSIONS = set(['pkl', 'root', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
db = MongoEngine(app)
#app.config.from_object('config')
#db = SQLAlchemy(app)
#login_manager = LoginManager()
#login_manager.init_app(app)

from app import views, models
