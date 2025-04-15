#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 07:45:10 2025

@author: robertsoncl
"""
import pandas as pd
import numpy as np
# Astropy is a great library from my undergrad days! Really useful for formatting tables
# and the like
from astropy.table import Table
from astropy.io import ascii
# excerpt from the end of an arbitrary RF Track script
# R is a matrix with the relevant information needed for TOPAS input
# in our case, px=x'
# we don't use pt but I've kept it in there.. for reasons??
# L is the lattice, bunchd is the initial bunch

# bunch = L.track(bunchd)
# retrieve transverse distribution results
#R = bunch.get_phase_space("%x %px %y %py %pt %E")

# R is the RF track phase space output as formatted above
# path_to_phsp_file is just where the new file will go and its name
# this must end with .phsp


def export_phsp(R, path_to_phsp_file):

    X = R[:, 0]
    PX = R[:, 1]
    Y = R[:, 2]
    PY = R[:, 3]
    E = R[:, 4] #changed from 5 to 4 here
    # assume constant position in Z at this stage - not physical bu
    # as we use TOPAS we through away our knowledge of accelerator physics
    Z = np.zeros(len(X))
    # we equally weight the beam
    weight = np.full(len(X), 1)
    ptype = np.full(len(X), 11)
    # topas uses rad rather than mrad
    PX = PX / 1000
    PY = PY / 1000
    # topas header uses cm
    X = X / 10
    Y = Y / 10
    # all particles are travelling forwards
    neg_cos = np.full(len(X), 1)
    # all primary particles, so first score is always 1, like weight
    first_score = weight
    # initialise dataframe with all relevant data required by TOPAS
    phase_space_data = pd.DataFrame(
        {
            "X": X,
            "Y": Y,
            "Z": Z,
            "PX": PX,
            "PY": PY,
            "E": E,
            "Weight": weight,
            "ptype": ptype,
            "neg_cos": neg_cos,
            "first_score": first_score,
        }
    )
    # convert DataFrame into astropy table for manipulation
    phase_space_table = Table.from_pandas(phase_space_data)
    # format for topas input
    ascii.write(
        phase_space_table,
        path_to_phsp_file,
        format="fixed_width_no_header",
        delimiter="\t",
        overwrite=True,
    )
# TOPAS beam inputs need a header alongside the .phsp file so that it knows
# how to process the beam data
# path_to_headerfile is just where the new file will go and its name
# this must be the same filename as the phsp file, but ending with .header
# rather than .phsp


def write_header(R, path_to_header_file):
    E = R[:, 4] #changed from 5 to 4
    N_particles_str = str(len(E))
    file = open(path_to_header_file, "w")
    file.write("TOPAS ASCII Phase Space\n")
    file.write("\n")
    file.write("Number of Original Histories: " + N_particles_str + "\n")
    file.write(
        "Number of Original Histories that Reached Phase Space: "
        + N_particles_str
        + "\n"
    )
    file.write("Number of Scored Particles: " + N_particles_str + "\n")
    file.write("\n")
    file.write("Columns of data are as follows:\n")
    file.write(" 1: Position X [cm]\n")
    file.write(" 2: Position Y [cm]\n")
    file.write(" 3: Position Z [cm]\n")
    file.write(" 4: Direction Cosine X\n")
    file.write(" 5: Direction Cosine Y\n")
    file.write(" 6: Energy [MeV]\n")
    file.write(" 7: Weight\n")
    file.write(" 8: Particle Type (in PDG Format)\n")
    file.write(
        " 9: Flag to tell if Third Direction Cosine is Negative (1 means true)\n"
    )
    file.write(
        "10: Flag to tell if this is the First Scored Particle from this History (1 means true)\n"
    )
    file.write("\n")
    file.write("Number of e-: " + N_particles_str + "\n")
    file.write("\n")
    file.write("Minimum Kinetic Energy of e-: " + str(min(E)) + " MeV\n")
    file.write("\n")
    file.write("Maximum Kinetic Energy of e-: " + str(max(E)) + " MeV\n")

# function adds
# relevant lines in TOPAS to import beam from phsp and header files
# acc_source is the name of the beam I've given here, this is arbitrary
# position allows you to modify the position in Z in the world that the imported
# beam starts from
# infile is the path to the phase space file you want to import
# give this without the .phsp and it will automatically find the
# header as well - make sure those are in the same directory


def import_beam_topas(infile, position=0):
    file = open('topas_script.txt', 'a')
    file.write('s:So/acc_source/Type = "PhaseSpace"\n')
    file.write('s:So/acc_source/Component = "World"\n')
    file.write('s:So/acc_source/PhaseSpaceFileName = "'+infile+'"\n')
    file.write('d:So/acc_source/TransZ = -'+str(position)+' mm\n')
