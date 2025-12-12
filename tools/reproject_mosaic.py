import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.windows import from_bounds
from affine import Affine
import math


def get_mosaic(file_paths):
    src_files_to_mosaic = []
    for fp in file_paths:
        _src = rasterio.open(fp)
        src_files_to_mosaic.append(_src)
    mosaic, transform = merge(src_files_to_mosaic, nodata=np.nan)
    
    # Закрытие исходных файлов
    for src in src_files_to_mosaic:
        src.close()
    return mosaic, transform


def reproject_mosaic(mosaic, transform, to_projection):
    src_crs = 'EPSG:4326'
    dst_crs = to_projection.proj4_init
    extent_bounds = (transform[2], transform[5] + transform[4] * mosaic.shape[1], transform[2] + transform[0] * mosaic.shape[2], transform[5])
    dst_transform, dst_width, dst_height = calculate_default_transform(
        src_crs, dst_crs, mosaic.shape[2], mosaic.shape[1], *extent_bounds
    )
    
    nodata_value = np.nan
    reprojected_mosaic = np.full((1, dst_height, dst_width), nodata_value, dtype=mosaic.dtype)
    
    reproject(
        mosaic[0],
        reprojected_mosaic[0],
        src_transform=transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest,
        src_nodata=None,
        dst_nodata=nodata_value
    )
    return reprojected_mosaic, dst_transform



def crop_mosaic(mosaic, transform, bounds):
    """
    Обрезает мозаику по заданным географическим границам.

    :param mosaic: NumPy-массив растра (форма: (bands, height, width)).
    :param transform: Аффина-трансформация исходной мозаики (rasterio.Affine).
    :param bounds: Кортеж границ (min_x, min_y, max_x, max_y).
    :return: cropped_mosaic (обрезанный NumPy-массив), new_transform (обновлённая аффина-трансформация).
    """
    # Вычисление окна обрезки
    window = from_bounds(*bounds, transform=transform)
    
    # Округление значений для точного слайсинга
    row_off = math.floor(window.row_off)
    col_off = math.floor(window.col_off)
    height = math.ceil(window.height)
    width = math.ceil(window.width)
    
    # Проверка на валидность окна (избежать пустой обрезки)
    if height <= 0 or width <= 0:
        raise ValueError("Границы обрезки выходят за пределы мозаики или некорректны.")
    
    # Обрезка массива
    cropped_mosaic = mosaic[:, row_off:row_off + height, col_off:col_off + width]
    
    # Обновление трансформации
    new_transform = transform * Affine.translation(col_off, row_off)
    
    return cropped_mosaic, new_transform


def save_to_geotiff(reprojected_mosaic, dst_transform, dst_crs, output_path):
    """
    Сохраняет репроектированную мозаику в GeoTIFF.

    :param reprojected_mosaic: Массив NumPy с данными мозаики (форма: (bands, height, width)).
    :param dst_transform: Аффина-трансформация для выходных данных.
    :param dst_crs: Целевая проекция (строка в формате PROJ4 или WKT).
    :param output_path: Путь к выходному файлу GeoTIFF.
    """
    dst_height = reprojected_mosaic.shape[1]
    dst_width = reprojected_mosaic.shape[2]
    
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=dst_height,
        width=dst_width,
        count=reprojected_mosaic.shape[0],  # Количество каналов
        dtype=reprojected_mosaic.dtype,
        crs=dst_crs,
        transform=dst_transform,
        compress='lzw'  # Опционально: сжатие
    ) as dst:
        dst.write(reprojected_mosaic)


def load_geotiff(file_path):
    """
    Загружает GeoTIFF-файл и возвращает растровые данные и трансформацию.

    :param file_path: Путь к GeoTIFF-файлу.
    :return: mosaic (NumPy-массив растра), transform (аффина-трансформация).
    """
    with rasterio.open(file_path) as src:
        # Чтение растра (для одноканального; для многоканального используйте src.read())
        mosaic = src.read(1)  # Возвращает 2D-массив; для 3D добавьте reshape если нужно
        mosaic = np.expand_dims(mosaic, axis=0)  # Добавление размерности для совместимости (bands, height, width)
        transform = src.transform
    return mosaic, transform
