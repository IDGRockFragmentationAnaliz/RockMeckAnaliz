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


if __name__ == '__main__':
    main()

