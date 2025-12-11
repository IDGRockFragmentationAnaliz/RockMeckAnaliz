import cartopy.crs as ccrs
import numpy as np
import shapely.geometry as sgeom
from cartopy.crs import Mercator


class ObliqueMercator(ccrs.Projection):
    def __init__(self, central_longitude=0.0, central_latitude=0.0,
                 false_easting=0.0, false_northing=0.0,
                 scale_factor=1.0, azimuth=0.0, gamma=0.0,
                 globe=ccrs.Globe(datum='WGS84')):
        if np.isclose(azimuth, 90):
            azimuth -= 1e-3  # Избежать артефактов при точно 90°
        proj4_params = [
            ('proj', 'omerc'),
            ('lonc', central_longitude),
            ('lat_0', central_latitude),
            ('k', scale_factor),
            ('x_0', false_easting),
            ('y_0', false_northing),
            ('alpha', azimuth),
            ('gamma', gamma),
            ('units', 'm')
        ]
        super().__init__(proj4_params, globe=globe)
        
        # Установка пределов на основе Mercator для consistency
        mercator = Mercator(
            central_longitude=central_longitude,
            globe=globe,
            false_easting=false_easting,
            false_northing=false_northing,
            scale_factor=scale_factor,
        )
        self._x_limits = mercator.x_limits
        self._y_limits = mercator.y_limits
        self.threshold = mercator.threshold
    
    @property
    def boundary(self):
        x0, x1 = self.x_limits
        y0, y1 = self.y_limits
        return sgeom.LinearRing([(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)])
    
    @property
    def x_limits(self):
        return self._x_limits
    
    @property
    def y_limits(self):
        return self._y_limits