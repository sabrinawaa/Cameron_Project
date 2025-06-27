#!/Users/sabrinawang/Desktop/Cameron_Project/venv/bin/python

import numpy as np
import matplotlib.pyplot as plt
from RF_track_4quad import *
import sys


def main(args):
    n_particles = 1e5
    L_drift = 0.2
    L_quad = 0.3
    L_after = 10 #m 
    ks = np.arange(-75,75,5)
    k1_1 = args[0]
    k1_2 = args[1]
    name = "s1_off"
    i=0

    for k1_3 in ks:
        for k1_4 in ks:

            R = four_quads(L_quad, float(k1_1), float(k1_2), float(k1_3), float(k1_4),
                            L_drift, n_particles, 200, L_drift_after=L_after, plot=False,saveparams=False)


            sig_x = np.std(R[:,0])
            sig_y = np.std(R[:,2])
            sig_xp = np.std(R[:,1])
            sig_yp = np.std(R[:,3])
            

            print(f"f1: {k1_1}, f2: {k1_2}, f3: {k1_3}, f4: {k1_4}--- sig_x: {sig_x}, sig_y: {sig_y}, sig_xp: {sig_xp}, sig_yp: {sig_yp}")

if __name__ == "__main__":
    main(sys.argv[1:])
#