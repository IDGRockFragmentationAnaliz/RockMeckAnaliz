import numpy as np
from rasterio.warp import reproject, Resampling, calculate_default_transform


def reproject_mosaic(mosaic, transform, to_projection):
    src_crs = 'EPSG:4326'
    dst_crs = to_projection.proj4_init
    extent_bounds = (transform[2], transform[5] + transform[4] * mosaic.shape[1], transform[2] + transform[0] * mosaic.shape[2], transform[5])
    dst_transform, dst_width, dst_height = calculate_default_transform(
        src_crs, dst_crs, mosaic.shape[2], mosaic.shape[1], *extent_bounds
    )
    reprojected_mosaic = np.empty((1, dst_height, dst_width), dtype=mosaic.dtype)
    reproject(
        mosaic[0],
        reprojected_mosaic[0],
        src_transform=transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )
    return reprojected_mosaic, dst_transform