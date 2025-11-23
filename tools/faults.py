import pandas as pd
import numpy as np
from pathlib import Path
import pyvista as pv
import pyproj
from tools.intersection import circle_intersect_horizontal_plane, circle_vertical_x_plane


class Faults:
    def __init__(self, df, crs):
        self.df: pd.DataFrame = df
        self.crs: str = crs

    def to_cartesian(self, lon0 = 0, lat0 = 0, strike = 0):
        transformer = pyproj.Transformer.from_crs(self.crs, "EPSG:3857", always_xy=True)
        lat = self.df["latitude"].to_numpy()
        lon = self.df["longitude"].to_numpy()
        depth = self.df["depth"].to_numpy()
        x, y = transformer.transform(lon, lat)
        x0, y0 = transformer.transform(lon0, lat0)
        cloud = pv.PolyData(np.column_stack((x, y, depth)))
        transformer = pv.Transform()
        transformer.translate([-x0, -y0, 0])
        transformer.rotate_z(strike)
        cloud.transform(transformer, inplace=True)
        # Корректировка strike (в градусах)
        self.df["strike"] = (self.df["strike"] - strike) % 360
        # Нормализация strike в диапазон [0, 360) для consistency
        self.df["x"] = cloud.points[:, 0]
        self.df["y"] = cloud.points[:, 1]
    
    def compute_radius(self):
        d_sgm = 6.75  # MPa
        self.df["r"] = self._get_disk_radius(self.df["magnitude"].to_numpy(), d_sgm)
    
    def get_circles(self):
        df = self.df[self.df["r"] > 0]
        x = df["x"].to_numpy()
        y = df["y"].to_numpy()
        h = df["depth"].to_numpy() * 1000
        radii = df["r"].to_numpy()
        dip = np.radians(df["dip"].to_numpy())
        strike = np.radians(df["strike"].to_numpy())
        normals = np.column_stack(self._get_normal(dip, strike))
        centers = np.column_stack((x, y, h))
        return centers, normals, radii
    
    def compute_horizontal_cut(self, h1):
        centers, normals, radii = self.get_circles()
        points1, points2 = circle_intersect_horizontal_plane(h1, centers, normals, 3 * radii)
        point_matrix = np.column_stack((points1, points2))
        np.save('../temp/point_matrix.npy', point_matrix)
        
    def compute_vertical_cut(self, pos_x):
        centers, normals, radii = self.get_circles()
        points1, points2 = circle_vertical_x_plane(pos_x, centers, normals, 3 * radii)
        point_matrix = np.column_stack((points1, points2))
        np.save('../temp/point_matrix.npy', point_matrix)
    
    @classmethod
    def load_data(cls):
        headers = load_headers()
        data_path = Path("..") / "data/CSAF_M1.focmec_pub"
        df = pd.read_csv(data_path, sep=" ", names=headers)
        obj = cls(df, "EPSG:4326")
        return obj

    @staticmethod
    def _get_disk_radius(m, d_sgm=1.0):
        return np.cbrt(7 / (16 * 6.75)) * 10 ** (0.5 * (m + 6)) * 10 ** (-2)
    
    @staticmethod
    def _get_normal(dip, strike):
        nx = np.sin(dip) * np.sin(strike)
        ny = -np.sin(dip) * np.cos(strike)
        nz = np.cos(dip)
        return nx, ny, nz


def load_headers():
    with open("../data/headers.txt", 'r', encoding='utf-8') as f:
        headers = [line.strip().split(' ', 1)[1] for line in f]
    return headers

