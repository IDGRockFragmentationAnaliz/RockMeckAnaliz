import pandas
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from faults import Faults
import shapely
import pyproj

def main():
    vectors()


def vectors():


    faults = Faults.load_data()

    lat_0 = 35.867
    lon_0 = -120.447
    strike_0 = 319

    faults.to_cartesian(lon_0, lat_0, strike_0)
    df = faults.df

    x = df["x"]
    y = df["y"]
    depth = df["depth"]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, depth,
                         c=depth, cmap='viridis', s=20, alpha=0.7)

    plt.show()

    # # Выбираем 5 случайных индексов
    # random_indices = np.random.choice(len(df), size=10, replace=False)
    # # Рисуем все три вектора
    # # ax.quiver(lon[i], lat[i], depth[i], dx_strike, dy_strike, dz_strike,
    # #           color='blue', label='Strike' if i == 0 else "", length=vector_length)
    #
    #
    # lat = lat[random_indices]
    # lon = lon[random_indices]
    # depth = depth[random_indices]
    # #
    # strike = strike[random_indices]
    # dip = dip[random_indices]
    # rake = rake[random_indices]


    # x_0, y_0 = transformer.transform(lon_0, lat_0)
    # x = x - x_0
    # y = y - y_0
    #
    #






if __name__ == '__main__':
    main()