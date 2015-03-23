from app import db
from app import coll_it_d, coll_tt_d
from app import histos as hist_coll
import sys
from copy import deepcopy

class MappedPlot(db.Document):
    name = db.StringField(max_length=255, required=True, unique=True)
    dtype = db.StringField(max_length=2, required=True)
    body = db.DictField(required=True)
    h_props = db.ListField(required=True)

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
