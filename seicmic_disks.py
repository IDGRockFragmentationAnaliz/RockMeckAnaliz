import numpy as np
from matplotlib import pyplot as plt
from tools.faults import Faults


def main():
    vectors()


def vectors():

    faults = Faults.load_data()
    
    lat_0 = 35.867
    lon_0 = -120.447
    strike_0 = 319
    
    faults.to_cartesian(lon_0, lat_0, strike_0)
    faults.compute_radius()
    
    faults.compute_horizontal_cut(6000)
    
    
if __name__ == '__main__':
    main()