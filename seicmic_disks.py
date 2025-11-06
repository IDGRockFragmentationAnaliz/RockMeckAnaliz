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
    faults.compute_radius()
    df = faults.df

    x = df["x"]
    y = df["y"]
    d = df["depth"]
    r = df["r"]

    # print(r)
    # return
    # mask = r > 10
    # r = r[mask]
    # x = x[mask]
    # y = y[mask]
    # d = d[mask]

    # print(r)
    # bins = np.logspace(np.log10(r.min()), np.log10(r.max()), 50)
    #
    # plt.hist(r, bins=bins, alpha=0.7, edgecolor='black')
    # plt.xscale('log')
    # plt.yscale('log')
    # plt.xlabel('Значения (лог масштаб)')
    # plt.ylabel('Частота (лог масштаб)')
    # plt.title('Гистограмма в лог-лог масштабе')
    # plt.grid(True, alpha=0.3)
    # plt.show()
    # return

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, d, c=d, cmap='viridis', s=20, alpha=0.7)

    plt.show()
    return
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


def get_disk_radius(m, d_sgm = 1.0):
    return np.cbrt(7/(16 * d_sgm)) * 10 ** (0.5 * (m + 6))



if __name__ == '__main__':
    main()