import pandas as pd
import numpy as np
from pathlib import Path
import pyvista as pv
import pyproj

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
        self.df["x"] = cloud.points[:, 0]
        self.df["y"] = cloud.points[:, 1]

    @classmethod
    def load_data(cls):
        headers = load_headers()
        data_path = Path(".") / "data/CSAF_M1.focmec_pub"
        df = pd.read_csv(data_path, sep=" ", names=headers)
        obj = cls(df, "EPSG:4326")
        return obj

def load_headers():
    with open("data/headers.txt", 'r', encoding='utf-8') as f:
        headers = [line.strip().split(' ', 1)[1] for line in f]
    return headers