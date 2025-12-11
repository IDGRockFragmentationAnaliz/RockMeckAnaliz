import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pathlib import Path
from tools.reproject_mosaic import reproject_mosaic
import matplotlib.ticker as mticker
from tools.oblique_mercator import ObliqueMercator

import cartopy.crs as ccrs
import numpy as np

def main():
    #file_paths = get_geotiff_paths()
    file_path_1 = Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N35W121_FABDEM_V1-2.tif")
    file_path_2 = Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N35W122_FABDEM_V1-2.tif")
    file_path_3 = Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N36W122_FABDEM_V1-2.tif")
    file_path_4 = Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N36W121_FABDEM_V1-2.tif")
    file_paths = [str(file_path_1)]
    mosaic, transform = get_mosaic(file_paths)
    
    projection = ObliqueMercator(
        central_longitude=-120.447,
        central_latitude=35.867,
        gamma=(42+180),
        azimuth=90.0
    )
    
    #x, y = projection.transform_point(-120, 35.867, ccrs.PlateCarree())
    
    
    #projection = ccrs.PlateCarree()
    
    mosaic, transform = reproject_mosaic(mosaic, transform, projection)
    
    # Создание фигуры с проекцией
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    
    # # Отображение растра (первый канал)
    extent = (
        transform[2],
        transform[2] + transform[0] * mosaic.shape[2],  # width
        transform[5] + transform[4] * mosaic.shape[1],  # height
        transform[5]
    )
    ax.imshow(mosaic[0], cmap='terrain', extent=extent, transform=projection)
    
    # Добавление элементов карты
    ax.coastlines(resolution='10m', color='black')
    ax.set_extent([-122, -120, 35, 37], crs=ccrs.PlateCarree())
    ax.set_extent([-50000, 200000, -40000, 100000], crs=projection)
    
    ggg(ax, projection)
    #ax.gridlines(draw_labels=True)
    
    plt.title('1')
    plt.show()


import matplotlib.ticker as mticker
import numpy as np


def ggg(ax, projection):
    gl = ax.gridlines(crs=projection, draw_labels=False, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    
    # Заполнение переменных на основе текущих лимитов оси
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    
    # Проверка на валидные лимиты (избегание глобального диапазона)
    if x_min == x_max or y_min == y_max:
        x_min, x_max = projection.x_limits
        y_min, y_max = projection.y_limits
    
    # Шаг в метрах; уменьшен для ускорения
    step_y = 20000  # Корректируйте по масштабу (например, 10000 для большего экстента)
    step_x = 50000
    # Генерация тиков с ограничением количества (максимум 10 по оси)
    x_ticks = np.arange(np.ceil(x_min / step_x) * step_x, np.floor(x_max / step_x) * step_x + step_x, step_x)
    y_ticks = np.arange(np.ceil(y_min / step_y) * step_y, np.floor(y_max / step_y) * step_y + step_y, step_y)
    x_ticks = x_ticks[:]  # Ограничение для производительности
    y_ticks = y_ticks[:]  # Ограничение для производительности
    
    gl.xlocator = mticker.FixedLocator(x_ticks)
    gl.ylocator = mticker.FixedLocator(y_ticks)
    
    # Настройка тиков и меток для оси X
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f'{x / 1000:.0f} km' for x in x_ticks], fontsize=8)
    
    # Настройка тиков и меток для оси Y
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f'{y / 1000:.0f} km' for y in y_ticks], fontsize=8)
    
    # Настройка параметров тиков
    ax.tick_params(axis='both', which='major', labelsize=8, direction='out', pad=5)
    

def get_geotiff_paths():
    directory = Path("D:/1.ToSaver/DEM/N30W130-N40W120_FABDEM_V1-2")
    # Перечисление всех .tif файлов в директории
    file_paths = [str(file) for file in directory.glob("*.tif")]
    return file_paths[0:1]


def get_mosaic(file_paths):
    src_files_to_mosaic = []
    for fp in file_paths:
        _src = rasterio.open(fp)
        src_files_to_mosaic.append(_src)
    mosaic, out_trans = merge(src_files_to_mosaic)
    
    # Закрытие исходных файлов
    for src in src_files_to_mosaic:
        src.close()
    
    return mosaic, out_trans


if __name__ == '__main__':
    main()