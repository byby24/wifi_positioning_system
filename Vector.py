class Vector:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __str__(self):
        return str(self.x) + " , " + str(self.y)


class Point(Vector):
    def __init__(self, _x, _y):
        super().__init__(_x, _y)
