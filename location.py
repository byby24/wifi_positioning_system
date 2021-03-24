class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __str__(self):
        return str(self.x) + " , " + str(self.y)


def adjust_distances(d1, d2, d3):
    if d1 > d2 - d3:
        pass


def calculate_position(point1: Point, point2: Point, point3: Point, d1: float, d2: float, d3: float):
    pass


def norm(num):
    return (num.y * 2 + num.x * 2) ** 0.5


def trilateration1(point1: Point, point2: Point, point3: Point, r1: float, r2: float, r3: float):
    resultPose: Point = Point(0, 0)
    # unit vector in a direction from point1 to point 2
    p2p1Distance: float = float(pow(pow(point2.x - point1.x, 2) + pow(point2.y - point1.y, 2), 0.5))
    ex: Point = Point((point2.x - point1.x) / p2p1Distance, (point2.y - point1.y) / p2p1Distance)
    aux: Point = Point(point3.x - point1.x, point3.y - point1.y)
    # signed magnitude of the x component
    i: float = ex.x * aux.x + ex.y * aux.y
    # the unit vector in the y direction.
    aux2: float = Point(point3.x - point1.x - i * ex.x, point3.y - point1.y - i * ex.y)
    ey: float = Point(aux2.x / norm(aux2), aux2.y / norm(aux2))
    # the signed magnitude of the y component
    j: float = ey.x * aux.x + ey.y * aux.y;
    # coordinates
    x: float = (pow(r1, 2) - pow(r2, 2) + pow(p2p1Distance, 2)) / (2 * p2p1Distance)
    y: float = (pow(r1, 2) - pow(r3, 2) + pow(i, 2) + pow(j, 2)) / (2 * j) - i * x / j
    # result coordinates
    finalX: float = point1.x + x * ex.x + y * ey.x
    finalY: float = point1.y + x * ex.y + y * ey.y
    resultPose.x = finalX
    resultPose.y = finalY
    return resultPose


def trilateration2(point1: Point, point2: Point, point3: Point, r1: float, r2: float, r3: float):
    x = (r1 * 2 - r2 * 2 + point3.x * 2 + point3.y * 2) / (2 * point2.x)
    y = ((r1 * 2 - r3 * 2 + point3.x * 2 + point3.y * 2 - 2 * point3.x * x) / (2 * point3.y))
    return Point(x, y)


def main():
    point1: Point = Point(1, 1)
    point2: Point = Point(3, 1)
    point3: Point = Point(1, 3)
    r1 = 8 ** 0.5
    r2 = 2
    r3 = 2

    print(trilateration1(point1, point2, point3, r1, r2, r3))


if __name__ == '__main__':
    main()
