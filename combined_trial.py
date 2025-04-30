import pandas as pd
import numpy as np
from RF_track_4quad import *
# from sabrina_rf_topas_conversion import *
from partrec_gaussian_optimiser_utils import partrec_gaussian_optimiser_utils
from topasToDose import getDosemap
from uniformity_fit import *
from partrec_foil_plotting import partrec_foil_plotting

quad_length = 0.3
k1 = 0
drift_l = 0.2
dir = '/Users/sabrinawang/Desktop/Cameron_Project/'
name = '4quad'
n_particles = 1e6
R = four_quads(quad_length, k1, drift_l, n_particles, 200)
dose_depth = 100
output_filename = "RFT_"

for s2_depth in [3]:
    for s2_radius in [5,10,15]:

        setup = partrec_gaussian_optimiser_utils()

        setup.export_phsp(R, dir + name + '.phsp')

        setup.write_header(R, dir + name + '.header')

        setup.import_beam_topas(dir+ name, position=0)

        # add pre-scatterer to magnify beam, thickness in mm to make beam 7.5mm radius
        setup.add_flat_scatterer(0.1, 'Tantalum')
        # define gaussian scatterer (here with 22mm depth, 10mm radius, composed of 100 slices, situated 100mm downstream (standard convention) of first scatterer, )
        setup.add_gaussian_scatterer(
            s2_depth, s2_radius, 1, 100, 'Aluminum', 100, show_shape=False)
        #add water phantom 2500mm away, depth in mm, 50 bins in x, y, 1 bin in z
        # setup.add_tank_bins(2500,dose_depth,50,50,1)

        #add vacuum patient 2500mm away
        setup.add_patient(2500)
        # initialise plotting class
        
        setup.run_topas(view_setup=False)
        plotter = partrec_foil_plotting('patient_beam.phsp' )
        # plot transverse distributions and energy spectrum at patient
        plotter.show_transverse_beam("4quadOff", s2_depth, s2_radius,fov=50, col=50)



        # initialise plotting class
        # doseMap = getDosemap("DoseAtTank"+str(dose_depth)+".csv",n_particles, dose_depth, output_filename, plot = True)
        # fitDoseMap(n_particles, dose_depth, output_filename)



