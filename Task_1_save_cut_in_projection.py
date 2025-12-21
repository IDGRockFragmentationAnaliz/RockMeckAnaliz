import numpy as np
import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pathlib import Path
from tools.oblique_mercator import ObliqueMercator
from tools.faults import Faults


def main():
    vectors()


def vectors():

    faults = Faults.load_data()

    projection = ObliqueMercator(
        central_longitude=-120.447,
        central_latitude=35.867,
        gamma=(42 + 180),
        azimuth=90.0
    )
    faults.to_projection(projection)
    faults.compute_radius()
    #print(faults.df["r"].to_numpy())
    faults.compute_horizontal_cut(5000, threshold=100)


    
if __name__ == '__main__':
    main()