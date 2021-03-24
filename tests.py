from location import trilateration1
from random import uniform, random
from Point import Point


def change_distances(r1, r2, r3, error_range):
    x, y, z = [x*-1 if random() > 0.5 else x for x in [uniform(0.0, error_range) for i in range(3)]]
    r1 += x
    r2 += y
    r3 += z
    return r1, r2, r3


def calculate_distance_between_2_points(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


def calculate_location_error(point1, point2, point3, r1, r2, r3, distance_error_range):
    q1, q2, q3 = change_distances(r1, r2, r3, distance_error_range)
    return calculate_distance_between_2_points(trilateration1(point1, point2, point3, r1, r2, r3),
                                               trilateration1(point1, point2, point3, q1, q2, q3))


def calculate_location_error_range(point1, point2, point3, r1, r2, r3, max_distance_error, n):
    error_sum = 0.0
    max_error = 0.0

    for i in range(n):
        x = calculate_location_error(point1, point2, point3, r1, r2, r3, max_distance_error)
        error_sum += x
        max_error = x if x > max_error else max_error

    return error_sum / n, max_error


def main():
    point1: Point = Point(1, 1)
    point2: Point = Point(3, 1)
    point3: Point = Point(1, 3)
    r1 = 8 ** 0.5
    r2 = 2
    r3 = 2

    max_distance_error, n = 4, 1000000
    avg_error, max_location_error = calculate_location_error_range(point1, point2, point3, r1, r2, r3,
                                                                   max_distance_error,
                                                                   n)
    print("max distance error - {}\navg location error - {}\nmax location error- {}\n{} times".format(
        max_distance_error, avg_error, max_location_error, n))


if __name__ == '__main__':
    main()
