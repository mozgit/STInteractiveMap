import os

import ROOT
from root_numpy import root2array, root2rec, tree2rec
from root_numpy.testdata import get_filepath

from pandas import DataFrame
from root_pandas import read_root

address = "/afs/cern.ch/user/i/ikomarov/ccbar/potential-spice/Applying_Tesla/Simplified/New_MakeLineForTurboSimplified/DaVinci/"
ROOT_PATH = address+"TutorialTuple_PVREFIT.root"
ROOT_TREE = "TeslaTuple/DecayTree"


df = read_root(ROOT_PATH, ROOT_TREE)
print df.branch_name.min(), df.branch_name.min()