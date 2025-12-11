import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
from tools.faults import Faults


def main():
    faults = Faults.load_data()
    strike = faults.df["strike"].to_numpy()
    mag = faults.df["magnitude"].to_numpy()
    #print(strike)
    
    

def plot_rose():
    n_bins = 32
    hist, bins = np.histogram(strike, bins=n_bins, range=(0, 360))
    width = 2 * np.pi / n_bins
    angles = (bins[:-1] + bins[1:]) / 2
    angles_rad = np.deg2rad(angles)
    
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="polar")
    bars = ax.bar(angles_rad, hist, width=width, alpha=0.7,
                  color=plt.cm.plasma(hist / hist.max()))
    plt.show()

if __name__ == '__main__':
    main()
    