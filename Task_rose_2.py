import numpy as np
import rasterio
from rasterio.merge import merge
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pathlib import Path
from tools.reproject_mosaic import reproject_mosaic, get_mosaic, save_to_geotiff, load_geotiff, crop_mosaic
import matplotlib.ticker as mticker
from tools.oblique_mercator import ObliqueMercator
from tools.grid_projection import grid_projection

def main():
    file_paths = get_geotiff_paths()
    file_path_s = [Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N35W121_FABDEM_V1-2.tif"),
                   Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N35W122_FABDEM_V1-2.tif"),
                   Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N36W122_FABDEM_V1-2.tif"),
                   Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N36W121_FABDEM_V1-2.tif"),
                   Path("D://1.ToSaver//DEM//N30W130-N40W120_FABDEM_V1-2//N37W122_FABDEM_V1-2.tif"),
                   Path("D://1.ToSaver//DEM//N30W120-N40W110_FABDEM_V1-2//N35W120_FABDEM_V1-2.tif")]
    file_paths = file_path_s
    mosaic, transform = get_mosaic(file_paths)
    
    projection = ObliqueMercator(
        central_longitude=-120.447,
        central_latitude=35.867,
        gamma=(42+180),
        azimuth=90.0
    )
    
    mosaic, transform = reproject_mosaic(mosaic, transform, projection)
    
    #mosaic, transform = load_geotiff(".//temp//mosaic_reproj.tif")
    mosaic, transform = crop_mosaic(mosaic, transform, (-30000, -20000, 170000, 20000))
    save_to_geotiff(mosaic, transform, projection, ".//temp//mosaic_reproj.tif")
    
    # Создание фигуры с проекцией
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    
    # Отображение растра (первый канал)
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
    
    grid_projection(ax, projection)
    ax.gridlines(draw_labels=True)
    
    plt.title('1')
    plt.show()
    

def get_geotiff_paths():
    directory = Path("D:/1.ToSaver/DEM/N30W130-N40W120_FABDEM_V1-2")
    # Перечисление всех .tif файлов в директории
    file_paths = [str(file) for file in directory.glob("*.tif")]
    return file_paths


if __name__ == '__main__':
    main()