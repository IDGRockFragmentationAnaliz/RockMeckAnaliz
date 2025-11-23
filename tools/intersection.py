import numpy as np
from skspatial.objects import Sphere, Line, Plane
from skspatial.plotting import plot_2d
from skspatial.plotting import plot_3d
from tqdm import tqdm


def circle_intersect_horizontal_plane(h1, point, n, r):
    points_1, points_2 = circle_intersect_plane(
        [0, 0, h1],
        [0, 0, 1], point, n, r
    )
    return points_1, points_2


def circle_vertical_x_plane(pos_x, point, n, r):
    points_1, points_2 = circle_intersect_plane(
        [pos_x, 0, 0],
        [1, 0, 0], point, n, r
    )
    return points_1, points_2


def circle_intersect_plane(plane_center, plane_normal, point, n, r):
    points_1 = []
    points_2 = []
    plane_cut = Plane(plane_center, plane_normal)
    for _point, _n, _r in tqdm(zip(point, n, r), total=len(point)):
        p1, p2 = one_circle_intersect_plane(plane_cut, _point, _n, _r)
        if p1 is not None:
            points_1.append(p1)
            points_2.append(p2)
    points_1 = np.array(points_1)
    points_2 = np.array(points_2)
    return points_1, points_2

    
def one_circle_intersect_plane(plane_cut: Plane, point: np.ndarray, normal: np.ndarray, radius):
    dist = plane_cut.distance_point(point)
    if dist > radius:
        return None, None
    plane = Plane(point, normal)
    # Линия пересечения сечения h1 и плоскости скольжения
    line = plane_cut.intersect_plane(plane)
    # Сфера радиуса окружности плоскости скложения
    sphere = Sphere(point, radius)
    # Предварительная проверка расстояния
    dist = line.distance_point(sphere.point)
    if dist > sphere.radius:
        return None, None
    # Точки пересечения c диском
    point_a, point_b = sphere.intersect_line(line)
    return point_a, point_b
