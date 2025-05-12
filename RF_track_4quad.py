import RF_Track as RFT
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

RFT.cvar.number_of_threads = 8
quad_length = 0.3
k1 = 30
drift_l = 0.2

def gaussian(x,A,mu,sig):
    return A * np.exp(- (x-mu)**2 /(2*sig**2))

def four_quads(Lquad, k11, k12, k13, k14, Ldrift, N_particles, Energy ,plot=True):
    Q1 =RFT.Quadrupole(Lquad, k11) 
    Q2 = RFT.Quadrupole(Lquad, k12)
    Q3 = RFT.Quadrupole(Lquad, k13)
    Q4 = RFT.Quadrupole(Lquad, k14)
    Drift = RFT.Drift(Ldrift)
    Drift.set_tt_nsteps(50)  

    #lattice
    lattice = RFT.Lattice()
    lattice.append(Q1)
    lattice.append(Drift)
    lattice.append(Q2)
    lattice.append(Drift)
    lattice.append(Q3)
    lattice.append(Drift)
    lattice.append(Q4)
    lattice.append(Drift)

    # ttable = lattice.get_transport_table("%beta_x %beta_y")
    # beta_x, beta_y = ttable[:, 0], ttable[:, 1]


    E = 200 # MeV
    N_particles = int(N_particles)
    charge = -1
    Q = np.full(N_particles,charge)
    mass = RFT.electronmass
    rel_gamma = E/mass
    rel_beta = np.sqrt(1-1/(rel_gamma**2))

    MASS = np.full(N_particles,mass)
    sigma_x, sigma_y = 1,1
    sigma_xp, sigma_yp = 1,1
    Pref = Energy
    x = np.random.normal(0, sigma_x, N_particles)
    xp = np.random.normal(0, sigma_xp, N_particles)
    y = np.random.normal(0, sigma_y, N_particles)
    yp = np.random.normal(0, sigma_yp, N_particles)
    P = E * (1 + np.random.normal(0, 0.005, N_particles))  # 200 MeV ± 0.5%
    T = np.zeros(N_particles)

    Twiss = RFT.Bunch6d_twiss() #maybe need to set emittance?
    Twiss.emitt_x = 10 #mm mrad normalised
    Twiss.emitt_y = 10
    geo_emm = Twiss.emitt_x / (rel_beta * rel_gamma)

    Twiss.beta_x = 1/geo_emm #m to get 1 mm sigma x
    Twiss.beta_y = 1/geo_emm
    # Twiss.beta_x = 1 * (1 + np.sin(np.radians(mu/2))) / np.sin(np.radians(mu))  # m
    # Twiss.beta_y = 1 * (1 - np.sin(np.radians(mu/2))) / np.sin(np.radians(mu))
    Twiss.alpha_x = 0.0
    Twiss.alpha_y = 0.0 #at symmetry points (inside quads)

    # bunch = RFT.Bunch6d(mass, N_particles, charge, np.array([ x, xp, y, yp, T, P ]) )
    # bunch= RFT.Bunch6d( np.array([ x, xp, y, yp, T, P,  MASS, Q, np.ones(N_particles) ]) )
    bunch = RFT.Bunch6d(mass, N_particles, charge, Pref, Twiss, N_particles)
    B1 = lattice.track(bunch)
    T = lattice.get_transport_table('%S %beta_x %beta_y %alpha_x %alpha_y')
    # print(B1.get_info().beta_x)
    M = B1.get_phase_space('%x %xp %y %yp %E %z')

    if plot:
        # Make plots
        plt.figure(1)
        plt.plot(T[:,0], T[:,1], 'b-', label=r'$\beta_x$')
        plt.plot(T[:,0], T[:,2], 'r-', label=r'$\beta_y$')
        plt.plot(T[:,0], T[:,3], 'g-', label=r'$\alpha_x$')
        plt.plot(T[:,0], T[:,4], 'b-', label=r'$\alpha_y$')
        plt.legend()
        plt.xlabel('S [m]')
        plt.ylabel(r'$\beta$ [m]')

        def scatter_hist(x, y, ax, ax_histx, ax_histy):

            ax_histx.tick_params(axis="x", labelbottom=True)
            ax_histy.tick_params(axis="y", labelleft=True)

            # the scatter plot:
            ax.scatter(x, y,s=5)

            ax.set_xlabel('X (mm)')  # Set x-axis label for scatter plot
            ax.set_ylabel('Y (mm)')

            # now determine nice limits by hand:
            binwidth = 0.25
            xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
            lim = (int(xymax/binwidth) + 1) * binwidth

            bins = np.arange(-lim, lim + binwidth, binwidth)
            # ax_histx.hist(x, bins=bins)
            # ax_histy.hist(y, bins=bins, orientation='horizontal')
            n_x, bins_x, _ = ax_histx.hist(x, bins=bins, alpha=0.6)
            n_y, bins_y, _ = ax_histy.hist(y, bins=bins, orientation='horizontal', alpha=0.6)

            mu_x, sigma_x = np.mean(x), np.std(x)
            mu_y, sigma_y = np.mean(y), np.std(y)
            
            # Scale factor to match histogram counts
            scale_x = len(x) * binwidth
            scale_y = len(y) * binwidth
            
            # Plot Gaussian fits
            pdf_x = norm.pdf(bins_x, mu_x, sigma_x) * scale_x
            ax_histx.plot(bins_x, pdf_x, 'k-', linewidth=2, label= f"sig_x = {sigma_x:.2f}")
            ax_histx.legend()
            
            pdf_y = norm.pdf(bins_y, mu_y, sigma_y) * scale_y
            ax_histy.plot(pdf_y, bins_y, 'k-', linewidth=2, label= f"sig_y = {sigma_y:.2f}")
            ax_histy.legend()

        fig, axs = plt.subplot_mosaic([['histx', '.'],
                                    ['scatter', 'histy']],
                                    figsize=(6, 6),
                                    width_ratios=(4, 1), height_ratios=(1, 4),
                                    layout='constrained')
        scatter_hist(M[:,0], M[:,2], axs['scatter'], axs['histx'], axs['histy'])

        fig.savefig(f"Output_figs/RFT_k1s={k11}_{k12}_{k13}_{k14}.png")
        np.savetxt(f"RFT_k1s={k11}_{k12}_{k13}_{k14}_N={N_particles}.txt",M) 
    
    return M






