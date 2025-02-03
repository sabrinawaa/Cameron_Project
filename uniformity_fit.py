import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from topasToDose import getDosemap


#characterise uniformity
def supergaussian(x, y, A, x0, y0, sigma_x, sigma_y, P):
    return A * np.exp(-( (x-x0)**2 /(2*sigma_x**2) + (y-y0)**2 /(2*sigma_y**2))**P)

def supergaussian1(xy, A, x0, y0, sigma_x, sigma_y, P): #different version of supergaussian for curvefit
    x,y = xy
    return A * np.exp(-((x-x0)**2/(2*sigma_x**2) + (y-y0)**2/(2*sigma_y**2))**P)

def MSE(params, x, y, dose_map):
    model = supergaussian(x, y, *params)
    return np.sum((model - dose_map)**2)  # Mean squared error

def r90(sig,P):
    return sig * np.sqrt(2) * (-np.log(0.9))**(0.5*P)

def main():
    n_particles = 100000
    dose_depth = 500
    doseMap = getDosemap("DoseAtTank"+str(dose_depth)+".csv",n_particles, dose_depth, plot = False)
    doseMap = doseMap[10:40, 10:40]  #only the central 60% of the beam
  
    x_length, y_length = doseMap.shape
    x = np.arange(0, x_length, 1)
    y = np.arange(0, y_length, 1)
    x, y = np.meshgrid(x, y)
    gaussian_test = supergaussian(x, y, 1, x_length//2, y_length//2, 8, 8, 2)
    
    p0=[0.2, x_length//2, y_length//2, 8, 8, 6]
    #curvefit 2d histogram to supergaussian
    # fit_params, cov = curve_fit(supergaussian1, (x.flatten(), y.flatten()), doseMap.flatten(), p0)
    # Perform the optimization
    bounds = [(None, None),(None, None), (None, None), (1e-5, None), (1e-5, None), (1, None)] 
    result = minimize(MSE, p0, args=(x, y, doseMap), method='L-BFGS-B', bounds=bounds)
    fit_params = result.x
    print(fit_params)

    # Calculate the fitted super-Gaussian
    fitted_map = supergaussian(x, y, *fit_params)
    sig, P = fit_params[3], fit_params[5]
    r_90 = r90(sig,P)
    print("r90 = " + str(r_90))
    
    dose_y = fitted_map[fitted_map.shape[0] // 2, :]  # Middle row (horizontal slice)
    dose_x = fitted_map[:, fitted_map.shape[1] // 2]  # Middle column (vertical slice)

    orig_dose_y = doseMap[doseMap.shape[0] // 2, :]  # Middle row (horizontal slice)
    orig_dose_x = doseMap[:, doseMap.shape[1] // 2]  # Middle column (vertical slice)

    # Create the figure with subplots
    # Create the figure with subplots
    fig = plt.figure(figsize=(10, 8))
    grid = plt.GridSpec(4, 4, hspace=0.4, wspace=0.4)  # Create a grid for subplots
    gs = fig.add_gridspec(4, 4)

    # Plot the 2D dose map
    # ax_main = fig.add_subplot(grid[1:, :-1])
    ax_main = fig.add_subplot(gs[1:3, 0:2])
    im = ax_main.imshow(doseMap, extent=[x.min(), x.max(), y.min(), y.max()],
                        origin='lower', cmap='viridis')
    ax_main.set_title(f"Super-Gaussian  P = {P:.2f}, sigma = {sig:.2f}, r90 = {r_90:.2f}")
    ax_main.set_xlabel("X Bins")
    ax_main.set_ylabel("Y Bins")
    cbar = plt.colorbar(im, ax=ax_main, orientation='vertical', fraction=0.046, pad=0.04)
    cbar.set_label("Supergaussian Dose (Gy)")

    # Plot the histogram along the X-axis
    # ax_x = fig.add_subplot(grid[0, :-1], sharex=ax_main)
    ax_x = fig.add_subplot(gs[0, 0:2])
    ax_x.bar(range(dose_x.shape[0]), dose_x, alpha=0.4, label="fitted", color="blue", edgecolor="black")
    ax_x.bar(range(orig_dose_x.shape[0]), orig_dose_x, alpha=0.4, label="orig", color="green", edgecolor="black")
    ax_x.set_ylabel("Sum Dose (Gy)")
    ax_x.set_title("X Histogram")
    ax_x.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  # Hide x-ticks
    ax_x.legend()

    # Plot the histogram along the Y-axis
    # ax_y = fig.add_subplot(grid[1:, -1], sharey=ax_main)
    ax_y = fig.add_subplot(gs[1:3, 3])
    ax_y.barh(range(dose_y.shape[0]), dose_y, alpha=0.4, label="fitted", color="blue", edgecolor="black")
    ax_y.barh(range(orig_dose_y.shape[0]), orig_dose_y, alpha=0.4, label="orig", color="green", edgecolor="black")
    ax_y.set_xlabel("Sum Dose (Gy)")
    ax_y.set_title("Y Histogram")
    ax_y.tick_params(axis='y', which='both', left=False, labelleft=False)  # Hide y-ticks
    ax_y.legend()

    plt.tight_layout()
    plt.show()

main()
        


        