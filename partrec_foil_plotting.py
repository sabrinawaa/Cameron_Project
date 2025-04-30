import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class partrec_foil_plotting:
    # import phase space from defined file
    def __init__(self, path_to_phsp_file):
        plt.rc("axes", labelsize=10)
        plt.rc("xtick", labelsize=8)
        plt.rc("ytick", labelsize=8)

        # read Topas ASCII output file
        phase_space = pd.read_csv(
            path_to_phsp_file,
            names=["X", "Y", "Z", "PX", "PY", "E", "Weight", "PDG", "9", "10"],
            delim_whitespace=True,
        )
        phase_space["X"] = phase_space["X"] * 10
        phase_space["Y"] = phase_space["Y"] * 10
        # add "R" column for radial distance from origin in cm
        phase_space["R"] = np.sqrt(
            np.square(phase_space["X"]) + np.square(phase_space["Y"])
        )

        gamma_phase_space = phase_space.copy()
        # create DataFrame containing only electron data at patient
        electron_phase_space = phase_space.drop(
            phase_space[phase_space["PDG"] != 11].index
        )
        # create DataFrame containing only gamma data at patient
        gamma_phase_space = gamma_phase_space.drop(
            phase_space[phase_space["PDG"] != 22].index
        )
        phsp_dict = {
            "all": phase_space,
            "e": electron_phase_space,
            "y": gamma_phase_space,
        }

        self.phsp_dict = phsp_dict
    # show transverse beam profile and energy spectrum
    # fov is field of view of profile graphs
    # col is the virtual collimator radius for calculation of transmission
    # both in millimetres
    # mean energy is calculated within collimator radius only

    def show_transverse_beam(self, out_filename, s2_depth, s2_r, particle='e', fov=50, col=50):
        def get_slices(phsp, slice_width=1):
            phsp_xslice = phsp[(phsp["Y"] < slice_width)]
            phsp_xslice = phsp_xslice[(phsp_xslice["Y"] > -slice_width)]
            phsp_yslice = phsp[(phsp["X"] < slice_width)]
            phsp_yslice = phsp_yslice[(phsp_yslice["X"] > -slice_width)]
            return phsp_xslice, phsp_yslice

        try:
            phsp = self.phsp_dict[particle]
        except KeyError:
            print('Beam type not found - should be one of "all", "e", "y"')
        phsp_xslice, phsp_yslice = get_slices(phsp)
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].hist(phsp_xslice["X"], bins=50, range=[-fov, fov], color="b")
        ax[0].set_xlabel("X [cm]")
        ax[0].set_ylabel("N")
        ax[0].set_title("X Distribution")
        ax[1].hist(phsp_yslice["Y"], bins=50, range=[-fov, fov], color="b")
        ax[1].set_xlabel("Y [cm]")
        ax[1].set_ylabel("N")
        ax[1].set_title("Y Distribution")
        # fig1, ax1 = plt.subplots(1, 2, figsize=(10,5))
        # ax1[0].hist2d(
        #     phsp["X"], phsp["Y"], bins=100, range=[[-fov, fov], [-fov, fov]], cmap="jet"
        # )
        # ax1[0].set_xlabel("X [mm]")
        # ax1[0].set_ylabel("Y [mm]")
        # ax1[0].set_title("XY Distribution")
        # ax1[1].hist(phsp["E"], bins=100, color="k")
        # ax1[1].set_xlabel("E [MeV]")
        # ax1[1].set_ylabel("N")
        # ax1[1].set_yscale('log')
        # ax1[1].set_title("Energy Spectrum")

        col_phsp = phsp[(phsp.R < col)]
        col_phsp = col_phsp.dropna()
        fig.savefig("Output_figs/"+out_filename+"_s2depth=" + str(s2_depth) + "s2r=" + str(s2_r) +"Intensity.png")
        #fig1.savefig("Output_figs/s2depth=" + str(s2_depth) + "s2r=" + str(s2_r) +"XY_Energy.png")
        #plt.show()
        print(
            "Electron Transmission = " +
            str(len(col_phsp["X"]) / len(phsp["X"]) * 100)
        )
        print("Mean Energy at Dump:" + str(np.mean(col_phsp["E"])))
#
