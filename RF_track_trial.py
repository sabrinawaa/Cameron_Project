import RF_Track as RFT
import numpy as np
import matplotlib.pyplot as plt
# plt.rcParams['text.usetex'] = True
print(RFT.max_number_of_threads)

RFT.cvar.number_of_threads = 8
Lquad = 0.3
strength = 3


Qf =RFT.Quadrupole(Lquad/2, strength/2) # half focusing quadrupole
Qd = RFT.Quadrupole(Lquad, -strength)
Drift = RFT.Drift(0.2)
Drift.set_tt_nsteps(50)  

#lattice
FODO = RFT.Lattice()
FODO.append(Qf)
FODO.append(Drift)
FODO.append(Qd)
FODO.append(Drift)
FODO.append(Qf)

# ttable = FODO.get_transport_table("%beta_x %beta_y")
# beta_x, beta_y = ttable[:, 0], ttable[:, 1]


E = 200 # MeV
N_particles = int(1e6)
charge = -1
Q = np.full(N_particles,charge)
mass = RFT.electronmass
MASS = np.full(N_particles,mass)
sigma_x, sigma_y = 1,1
sigma_xp, sigma_yp = 1,1
Pref = 200
x = np.random.normal(0, sigma_x, N_particles)
xp = np.random.normal(0, sigma_xp, N_particles)
y = np.random.normal(0, sigma_y, N_particles)
yp = np.random.normal(0, sigma_yp, N_particles)
P = E * (1 + np.random.normal(0, 0.005, N_particles))  # 200 MeV ± 0.5%
T = np.zeros(N_particles)

Twiss = RFT.Bunch6d_twiss() #maybe need to set emittance?

# bunch = RFT.Bunch6d(mass, N_particles, charge, np.array([ x, xp, y, yp, T, P ]) )
# bunch= RFT.Bunch6d( np.array([ x, xp, y, yp, T, P,  MASS, Q, np.ones(N_particles) ]) )
bunch = RFT.Bunch6d(mass, N_particles, charge, Pref, Twiss, 1000 )
B1 = FODO.track(bunch)
T = FODO.get_transport_table('%S %beta_x %beta_y')
# print(B1.get_info().beta_x)
M = B1.get_phase_space('%x %xp %y %yp')
print(T)
print(M)
# Make plots
plt.figure(1)
plt.plot(T[:,0], T[:,1], 'b-', label=r'$\beta_x$')
plt.plot(T[:,0], T[:,2], 'r-', label=r'$\beta_y$')
plt.legend()
plt.xlabel('S [m]')
plt.ylabel(r'$\beta$ [m]')

plt.figure(2)
plt.scatter(M[:,0], M[:,1], marker='*')
plt.xlabel('x [mm]')
plt.ylabel("x' [mrad]")

plt.show()