import pandas as pd
import numpy as np
from RF_track_4quad import *
# from sabrina_rf_topas_conversion import *
from partrec_gaussian_optimiser_utils import partrec_gaussian_optimiser_utils
from topasToDose import getDosemap
from uniformity_fit import *
from partrec_foil_plotting import partrec_foil_plotting

quad_length = 0.3
k1_1, k1_2, k1_3, k1_4 = -10,9,0,0 #<75
drift_l = 0.2
dir = '/Users/sabrinawang/Desktop/Cameron_Project/'
name = '4qua_s1off'
output_filename = "4quad"
n_particles = 1e5 #1e5
dose_depth = 100

R = four_quads(quad_length, k1_1, k1_2, k1_3, k1_4, drift_l, n_particles, 200,saveparams=True, plot=True)


# R = np.loadtxt(f"RFT_k1s={k1_1}_{k1_2}_{k1_3}_{k1_4}_N={int(n_particles)}.txt") 

for s1_depth in [0.8]:
    for s2_depth in [3]:
        for s2_radius in [3]:

            setup = partrec_gaussian_optimiser_utils()

            setup.export_phsp(R, dir + name + '.phsp')

            setup.write_header(R, dir + name + '.header')

            setup.import_beam_topas(dir+ name, position=0)

            # add pre-scatterer to magnify beam, thickness in mm to make beam 7.5mm radius
            # setup.add_flat_scatterer(s1_depth, 'Tantalum')
            # define gaussian scatterer (here with 22mm depth, 10mm radius, composed of 100 slices, situated 100mm downstream (standard convention) of first scatterer, )
            # #setup.add_patient(100)
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
            plotter.show_transverse_beam(output_filename, s1_depth, s2_depth, s2_radius,particle= 'e',fov= 150, col=75)
            # plotter.show_transverse_beam(output_filename, s1_depth, s2_depth, s2_radius,particle= 'y',fov= 150, col=75)



#             # initialise plotting class
#             # doseMap = getDosemap("DoseAtTank"+str(dose_depth)+".csv",n_particles, dose_depth, output_filename, plot = True)
#             # fitDoseMap(n_particles, dose_depth, output_filename)



