#!/Users/sabrinawang/Desktop/Cameron_Project/venv/bin/python

import numpy as np
import matplotlib.pyplot as plt
from RF_track_4quad import *
import sys


def main(args):
    n_particles = 1e5
    L_drift = 0.2
    L_quad = 0.3
    ks = np.arange(-75,75,5)
    k1_1 = args[0]
    k1_2 = args[1]
    i=0

    for k1_3 in ks:
        for k1_4 in ks:

            R = four_quads(L_quad, float(k1_1), float(k1_2), float(k1_3), float(k1_4), L_drift, n_particles, 200, plot=False)
            sig_x = np.std(R[:,0])
            sig_y = np.std(R[:,2])
            
            if sig_x > 1 and sig_y > 1:
                print(f"f1: {k1_1}, f2: {k1_2}, f3: {k1_3}, f4: {k1_4}")

if __name__ == "__main__":
    main(sys.argv[1:])
# result = np.zeros((150,150,150,150))
