import rasterio
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
from tools.faults import Faults
from tools.oblique_mercator import ObliqueMercator
import cartopy.crs as ccrs
from tools.grid_projection import grid_projection
from tools.reproject_mosaic import reproject_mosaic, get_mosaic, save_to_geotiff, load_geotiff, crop_mosaic


def main():
    faults = Faults.load_data()
    projection = ObliqueMercator(
        central_longitude=-120.447,
        central_latitude=35.867,
        gamma=(42 + 180),
        azimuth=90.0
    )
    
    faults.to_projection(projection)
    
    x = faults.df["x"].to_numpy()
    y = faults.df["y"].to_numpy()
    strikes = (faults.df["strike"].to_numpy() - 42)
    
    nbins = 10
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)
    len_x = (xmax - xmin)
    len_y = (ymax - ymin)
    dl = len_x/nbins
    xbins = np.linspace(xmin, xmax, nbins+1)
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(3, 1, 3, projection=projection)
    plot_background(ax, projection)
    #ax.scatter(x, y, transform=projection)
    #ax.scatter(0, 0, color="black", transform=projection)
    ax.gridlines(draw_labels=True)
    #ax.coastlines(resolution='10m', color='black')
    ax.plot(xbins, ymin + np.zeros(nbins+1), color="black")
    ax.plot(xbins, ymax + np.zeros(nbins + 1), color="black")
    ax.set_xlim([-20000, 170000])
    ax.set_extent([-30000, 150000, -20000, 20000], crs=projection)
    for _x in xbins:
        ax.plot([_x, _x], [ymin, ymax], color="black")
    #grid_projection(ax, projection)
    #
    entropies = []
    for i in range(nbins):
        ax2 = fig.add_subplot(3, nbins, i+1, projection="polar")
        ax2.set_xticks([])
        ax2.set_yticks([])
        mask = (x < xmin + dl*(i+1)) & (x > xmin + dl*i)
        entropy = plot_rose(ax2, strikes[mask])
        entropies.append(entropy)
    
    ax3 = fig.add_subplot(3, 1, 2)
    ax3.plot((xbins[0:-1]+xbins[1:])/2000, entropies,"-o")
    ax3.set_xlim([xmin/1000, xmax/1000])
    plt.savefig('pictures/1.eps', format='eps', dpi=300)
    plt.show()


def plot_background(ax, projection):
    mosaic, transform = load_geotiff(".//temp//mosaic_reproj.tif")
    extent = (
        transform[2],
        transform[2] + transform[0] * mosaic.shape[2],  # width
        transform[5] + transform[4] * mosaic.shape[1],  # height
        transform[5]
    )
    ax.imshow(mosaic[0], cmap='terrain', extent=extent, transform=projection)


def plot_rose(ax, strike):
    strike = strike % 180
    n_bins = 32
    hist, bins = np.histogram(strike, bins=n_bins, range=(0, 180))
    width = np.pi / n_bins
    
    # Дублируем данные для полного круга
    angles = (bins[:-1] + bins[1:]) / 2
    angles_rad = np.deg2rad(angles)
    hist_double = np.concatenate([hist, hist])  # Дублируем гистограмму
    angles_double_rad = np.concatenate([angles_rad, angles_rad + np.pi])  # Сдвигаем на 180°
    
    bars = ax.bar(angles_double_rad, hist_double, width=width, alpha=0.7,
                  color=plt.cm.plasma(hist_double / hist_double.max()))
    
    probs = hist / hist.sum()
    probs = probs[probs > 0]
    entropy = -np.sum(probs * np.log2(probs))
    return entropy



if __name__ == '__main__':
    main()
    