import pandas as pd
import numpy as np
from RF_track_4quad import *
from sabrina_rf_topas_conversion import *
from partrec_gaussian_optimiser_utils import partrec_gaussian_optimiser_utils
from topasToDose import getDosemap
from uniformity_fit import *

quad_length = 0.3
k1 = 0
drift_l = 0.2
dir = '/Users/sabrinawang/Desktop/Cameron_Project/'
name = '4quad'
n_particles = 1e4
R = four_quads(quad_length, k1, drift_l, n_particles, 200)
dose_depth = 100
output_filename = "RFT_"

export_phsp(R, dir + name + '.phsp')

write_header(R, dir + name + '.header')

import_beam_topas(dir+ name, position=0)

setup = partrec_gaussian_optimiser_utils()
# add pre-scatterer to magnify beam, thickness in mm
setup.add_flat_scatterer(0.8, 'Tungsten')
# define gaussian scatterer (here with 22mm depth, 10mm radius, composed of 250 slices, situated 100mm downstream of first scatterer, )
setup.add_gaussian_scatterer(
    3, 1.5, 1, 250, 'Aluminum', 100, show_shape=False)
#add water phantom 2500mm away, depth 500 mm, 50 bins in x, y, 1 bin in z
setup.add_tank_bins(2500,dose_depth,50,50,1)
# run script
setup.run_topas(view_setup=False)
# initialise plotting class
doseMap = getDosemap("DoseAtTank"+str(dose_depth)+".csv",n_particles, dose_depth, output_filename, plot = True)
fitDoseMap(n_particles, dose_depth, output_filename)


#why no initial beam still gives a dose profile? even the same as the one before
#beam imported into topas_script, other setup in partrec_test

