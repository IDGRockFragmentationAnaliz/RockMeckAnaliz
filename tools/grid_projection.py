import numpy as np
import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pathlib import Path
from tools.reproject_mosaic import reproject_mosaic, get_mosaic, save_to_geotiff, load_geotiff, crop_mosaic
import matplotlib.ticker as mticker
from tools.oblique_mercator import ObliqueMercator


def grid_projection(ax, projection):
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
