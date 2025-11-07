from skspatial.objects import Sphere, Line, Plane
from skspatial.plotting import plot_2d
from skspatial.plotting import plot_3d


def main():
    plane_cut = Plane([0, 0, 1], [0, 0, 1])
    plane = Plane([0, 0, 0], [1, 0, 1])
    
    line = plane_cut.intersect_plane(plane)
    sphere = Sphere([0, 0, 0], 1)
    point_a, point_b = sphere.intersect_line(line)
    print(point_a, point_b)


def circle_intersect(h1, x, y, h, n, r):
    plane_cut = Plane([0, 0, h1], [0, 0, 1])
    plane = Plane([x, y, h], n)
    # Линия пересечения сечения h1 и плоскости скольжения
    line = plane_cut.intersect_plane(plane)
    # Сфера радиуса окружности плоскости скложения
    sphere = Sphere([x, y, h], r)
    
    # Предварительная проверка расстояния
    dist = line.distance_point(sphere.point)
    if dist > sphere.radius:
        return None
    
    # точки пересечения c диском
    point_a, point_b = sphere.intersect_line(line)
    return point_a, point_b
    
    
if __name__ == '__main__':
    main()

#
# circle = Circle([0, 0], 5)
# line = Line([0, 0], [1, 1])
#
# point_a, point_b = circle.intersect_line(line)
