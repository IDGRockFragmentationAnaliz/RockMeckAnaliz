import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv


def main():
    strike = 30
    dip = 40

    strike = np.radians(strike)
    dip = np.radians(dip)
    shape = (100, 100, 100)

    strike = 30
    dip = 30
    i_0 = 30
    j_0 = 40
    k_0 = 60
    disk1 = pv.Cylinder(center=(i_0, j_0, k_0), direction=(0, 1, 0), radius=10, height = 1, resolution = 100, capping=True)
    geometry = disk1.extract_surface().extract_surface().clean()

    # Создаем регулярную 3D сетку
    grid_shape = (100, 100, 100)  # ваша desired shape
    x = np.arange(0, 100, 1.0)
    y = np.arange(0, 100, 1.0)
    z = np.arange(0, 100, 1.0)

    grid = pv.RectilinearGrid(x, y, z)

    # Определяем какие точки внутри геометрии
    binary_grid = grid.select_enclosed_points(geometry)


    # Получаем массив: 1 - внутри, 0 - снаружи
    binary_array = np.array(binary_grid['SelectedPoints'].reshape(grid_shape))

    # Создаем plotter для отображения
    print(binary_array)
    print(np.sum(binary_array))


    # plotter = pv.Plotter()
    #
    # # Добавляем исходные поверхности
    # plotter.add_mesh(geometry, color='red', opacity=0.4)
    #
    # # Показываем
    # plotter.show()


    plot_3d_voxels(binary_array, threshold=0.5)


def plot_3d_voxels(voxel_matrix, threshold=0.5):
    """Отображение 3D воксельной сетки в matplotlib"""

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    ax.voxels(voxel_matrix)

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('3D Voxel Grid with Two Discs')

    plt.tight_layout()
    plt.show()


def vectors():
    headers = load_headers()

    data_path = Path(".") / "data/CSAF_M1.focmec_pub"
    df = pd.read_csv(data_path, sep=" ", names=headers)
    lat = df["latitude"].to_numpy()
    lon = df["longitude"].to_numpy()
    depth = df["depth"].to_numpy()
    #
    strike = df["strike"].to_numpy()
    dip = df["dip"].to_numpy()
    rake = df["rake"].to_numpy()

    # Выбираем 5 случайных индексов
    random_indices = np.random.choice(len(df), size=5, replace=False)
    # Рисуем все три вектора
    # ax.quiver(lon[i], lat[i], depth[i], dx_strike, dy_strike, dz_strike,
    #           color='blue', label='Strike' if i == 0 else "", length=vector_length)

    # print(strike)
    # exit()
    lat = lat[random_indices]
    lon = lon[random_indices]
    depth = depth[random_indices]
    #
    strike = strike[random_indices]
    dip = dip[random_indices]
    rake = rake[random_indices]



    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(lon, lat, depth,
                         c=depth, cmap='viridis', s=20, alpha=0.7)

    plt.show()


def load_headers():
    with open("data/headers.txt", 'r', encoding='utf-8') as f:
        headers = [line.strip().split(' ', 1)[1] for line in f]
    return headers

if __name__ == '__main__':
    main()

