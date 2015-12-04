from app import db
from app import coll_it_d, coll_tt_d
from app import histos as hist_coll
import sys
import os
from copy import deepcopy


    #collection = {'tt+hist+property':{
    #                                'owner':
    #                                'vals':[]
    #                                'min':
    #                                'max':
    #                                'bin_number':{colour_code, value}
    #                               }}
class ColorMap(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    histo_name = db.StringField(max_length=255, required=True)
    owner = db.StringField(max_length=255, required=True)
    det_type = db.StringField(max_length=255, required=True)
    values = db.ListField(required=True)
    minv = db.FloatField(required=True)
    maxv = db.FloatField(required=True)
    bins = db.DictField(required=True)

    def return_collection(self):
        collection = {'owner':self.owner,
                      'vals':self.values,
                      'min':self.minv,
                      'max':self.maxv,
                      'bins':self.bins,
                      'histo_name':self.histo_name,
                      'det_type':self.det_type
        }
        return collection


class MappedPlot(db.Document):
    #Name of a histogram
    name = db.StringField(max_length=255, required=True, unique=True)
    #Owner
    owner = db.StringField(max_length=255)
    #TT or IT
    dtype = db.StringField(max_length=2, required=True)
    #The huge dictionary containing all sectors, plots and numbers
    body = db.DictField(required=True)
    #Calculated properties (mean, sigma etc)
    h_props = db.ListField(required=True)
    #Comment to keep run conditions etx
    comment = db.StringField(max_length=2000)

    def remove_color_map(self):
        for p in self.h_props:
            name = self.dtype.lower()+"_d"+self.name+p
            try:
                ColorMap.objects.get(name=name).delete()
                print name + " map deleted"
            except:
                print "Failed to delete "+name
        return True
    def __unicode__(self):
        return self.name

    def add_to_detector(self):
        global coll_it_d
        global coll_tt_d
        global hist_coll
        if self.dtype == "TT":
            coll_tt_d[self.name] = deepcopy(self.body)
            hist_coll['tt'][self.name] = deepcopy(self.h_props)
            return self.name+" added"
        if self.dtype == "IT":
            coll_it_d[self.name] = deepcopy(self.body)
            hist_coll['it'][self.name] = deepcopy(self.h_props)
            return self.name+" added"

        return self.name+" not added. Check self.dtype"

    def remove_from_detector(self):
        global coll_it_d
        global coll_tt_d
        global hist_coll
        if self.dtype == "TT":
            if self.name in coll_tt_d:
                del coll_tt_d[self.name]
                del hist_coll['tt'][self.name]
                return self.name+" removed from detector"
            else:
                return self.name+" not in detector"
        if self.dtype == "IT":
            if self.name in coll_it_d:
                del coll_it_d[self.name]
                del hist_coll['it'][self.name]
                return self.name+" removed from detector"
            else:
                return self.name+" not in detector"

        return self.name+" not removed. Check self.type"

    def is_loaded(self):
        global coll_it_d
        global coll_tt_d
        if self.dtype == "TT":
            if self.name in coll_tt_d:
                return True
        if self.dtype == "IT":
            if self.name in coll_it_d:
                return True
        return False

    def remove_plots(self):
        global coll_it_d
        global coll_tt_d
        global hist_coll
        print "Trying to remove plots for "+self.name
        if self.dtype == "TT":
            if self.name in coll_tt_d:
                for layer in coll_tt_d[self.name]:
                    if layer not in ["dtype"]:
                        for side in coll_tt_d[self.name][layer]:
                            if side not in ["layer_info"]:
                                for sector in coll_tt_d[self.name][layer][side]:
                                    if sector not in ["side_info"]:
                                        try:
                                            plot_address = coll_tt_d[self.name][layer][side][sector]['Histograms'][self.name]['plot']
                                            os.system("rm app/static/" + plot_address)
                                            print "app/static/"+plot_address+" removed"
                                        except:
                                            pass
            return
        if self.dtype == "IT":
            if self.name in coll_it_d: 
                for station in coll_it_d[self.name]:
                    if station not in ["dtype"]:
                        for side in coll_it_d[self.name][station]:
                            if side not in ["station_info"]:
                                for layer in coll_it_d[self.name][station][side]:
                                    if layer not in ["side_info"]:
                                        for sector in coll_it_d[self.name][station][side][layer]:
                                            if sector not in ["layer_info"]:
                                                try:
                                                    plot_address = coll_it_d[self.name][station][side][layer][sector]['Histograms'][self.name]['plot']
                                                    os.system("rm app/static/" + plot_address)
                                                    print "app/static/"+plot_address+" removed"
                                                except:
                                                    pass
            return
        return "Plots for "+self.name+" not removed."
