from math import cos, sin, pi
from Vector import Point
from sys import maxsize
from AccessPoint import AccessPoint


class Circle:
    def __init__(self, _center_point, _radius):
        self.center_point = _center_point
        self.radius = _radius
        self.first_angle_to_create = 0
        self.closest_angle_point = 0


def get_distance_between_2_points(point1, point2):
    """
    :return: distance between 2 points
    """
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


def get_distances_sum_of_3_points(point1, point2, point3):
    """
    :return: sum of distances between the 3 points and themself
    """
    return get_distance_between_2_points(point1, point2) + get_distance_between_2_points(point1, point3) + \
           get_distance_between_2_points(point2, point3)


def make_point_on_circle(center_point, radius, angle):
    """
    :return: point on a circle, created by its angle, radius, and center point
    """
    # new_point_x = int(round(center_point.x + radius * cos(angle), 1))
    # new_point_y = int(round(center_point.y + radius * sin(angle), 1))
    new_point_x = center_point.x + (radius * cos(angle))
    new_point_y = center_point.y + (radius * sin(angle))
    return Point(new_point_x, new_point_y)


def get_triangle_center(point1, point2, point3):
    """
    :return: return the center of a triangle represented by 3 points
    """
    return (point1.x + point2.x + point3.x) / 3, (point1.y + point2.y + point3.x) / 3


def get_first_angle_to_create(last_round_closest_point_angle, n_points_to_create: int, angle_change: float):
    """
    :return: the first angle to create
    """
    return last_round_closest_point_angle - angle_change * n_points_to_create / 2


def get_3_closest_points_on_circles(c1, c2, c3):
    """
    :return: The 3 closest points on circles c1, c2, c3, with the lowest total sum of distances, using brute force.
    """
    n_points_to_create = 16
    min_distances_sum = maxsize
    angle_change = 1 / n_points_to_create * 2 * pi
    accuracy_rounds = 3
    distance_sum = 0
    circle1_point, circle2_point, circle3_point = None, None, None

    for i in range(accuracy_rounds):

        c1.first_angle_to_create = get_first_angle_to_create(c1.closest_angle_point, n_points_to_create, angle_change)
        c2.first_angle_to_create = get_first_angle_to_create(c2.closest_angle_point, n_points_to_create, angle_change)
        c3.first_angle_to_create = get_first_angle_to_create(c3.closest_angle_point, n_points_to_create, angle_change)

        for a in range(n_points_to_create):
            circle1_point = make_point_on_circle(c1.center_point, c1.radius, c1.first_angle_to_create +
                                                 angle_change * a)
            for b in range(n_points_to_create):
                circle2_point = make_point_on_circle(c2.center_point, c2.radius,
                                                     c2.first_angle_to_create + angle_change * b)
                for c in range(n_points_to_create):
                    circle3_point = make_point_on_circle(c3.center_point, c3.radius,
                                                         c3.first_angle_to_create + angle_change * c)

                    distance_sum = get_distances_sum_of_3_points(circle1_point, circle2_point, circle3_point)

                    if distance_sum < min_distances_sum:
                        min_distances_sum = distance_sum
                        c1.closest_angle_point = c1.first_angle_to_create + angle_change * a
                        c2.closest_angle_point = c2.first_angle_to_create + angle_change * b
                        c3.closest_angle_point = c3.first_angle_to_create + angle_change * c

        angle_change = angle_change / 2
    c1min_point, c2min_point, c3min_point = create_3_points(c1, c2, c3)
    return c1min_point, c2min_point, c3min_point


def create_3_points(c1, c2, c3):
    c1min_point = make_point_on_circle(c1.center_point, c1.radius, c1.closest_angle_point)
    c2min_point = make_point_on_circle(c2.center_point, c2.radius, c2.closest_angle_point)
    c3min_point = make_point_on_circle(c3.center_point, c3.radius, c3.closest_angle_point)
    return c1min_point, c2min_point, c3min_point


def get_position(ap1, ap2, ap3):
    """
    param: ap1, ap2, ap3: 3 AccessPoint objects
    return: a point representing the location of the user, calculated according to the ap's locations and
    measured distances
    """
    c1 = Circle(Point(ap1.x, ap1.y), ap1.distance)
    c2 = Circle(Point(ap2.x, ap2.y), ap2.distance)
    c3 = Circle(Point(ap3.x, ap3.y), ap3.distance)
    c1min_point, c2min_point, c3min_point = get_3_closest_points_on_circles(c1, c2, c3)
    return get_triangle_center(c1min_point, c2min_point, c3min_point)


# def adjust_distances(d1, d2, d3):
#     if d1 > d2 - d3:
#         pass
#
#
# def norm(vector):
#     """
#     :param vector:
#     :return: absolute value of vector
#     """
#     return (vector.y * 2 + vector.x * 2) ** 0.5
#
#
# def calculate_position(ap1, ap2, ap3):
#     """
#     :param ap1, ap2, ap3: AccessPoint objects.
#     :return: current position based on the distances and locations of access points, using vector math
#     """
#     # unit vector in a direction from ap1 to point 2
#     p2p1Distance: float = float(pow(pow(ap2.x - ap1.x, 2) + pow(ap2.y - ap1.y, 2), 0.5))
#     ex: Vector = Vector((ap2.x - ap1.x) / p2p1Distance, (ap2.y - ap1.y) / p2p1Distance)
#     aux: Vector = Vector(ap3.x - ap1.x, ap3.y - ap1.y)
#     # signed magnitude of the x component
#     i: float = ex.x * aux.x + ex.y * aux.y
#     # the unit vector in the y direction.
#     aux2 = Vector(ap3.x - ap1.x - i * ex.x, ap3.y - ap1.y - i * ex.y)
#     ey = Vector(aux2.x / norm(aux2), aux2.y / norm(aux2))
#     # the signed magnitude of the y component
#     j: float = ey.x * aux.x + ey.y * aux.y
#     # coordinates
#     x: float = (pow(ap1.distance, 2) - pow(ap2.distance, 2) + pow(p2p1Distance, 2)) / (2 * p2p1Distance)
#     y: float = (pow(ap1.distance, 2) - pow(ap3.distance, 2) + pow(i, 2) + pow(j, 2)) / (2 * j) - i * x / j
#     # result coordinates
#     finalX: float = ap1.x + x * ex.x + y * ey.x
#     finalY: float = ap1.y + x * ex.y + y * ey.y
#     return finalX, finalY


# def trilateration2(point1: Point, point2: Point, point3: Point, r1: float, r2: float, r3: float):
#     """
#     another method to calculate position using analytic math
#     """
#     x = (r1 * 2 - r2 * 2 + point3.x * 2 + point3.y * 2) / (2 * point2.x)
#     y = ((r1 * 2 - r3 * 2 + point3.x * 2 + point3.y * 2 - 2 * point3.x * x) / (2 * point3.y))
#     return Point(x, y)
#
# ap1 = AccessPoint(0, 0, "1", 0, 0, 18 ** 0.5)
# ap2 = AccessPoint(3, 0, "2", 0, 0, 3)
# ap3 = AccessPoint(0, 3, "3", 0, 0, 3)
#
# print(get_position(ap1, ap2, ap3))
