import math, random

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """
    Sets both x and y to 0
    """
    def clear(self):
        self.x = 0
        self.y = 0

    """
    Returns a new Vector object with the same values
    """
    def copy(self):
        return Vector(self.x, self.y)

    """
    Returns the distance between this and another Vector
    """
    def distTo(self, other):
        x = other.x -self.x
        y = other.y - self.y
        return math.sqrt(x**2 + y**2)

    """
    Returns a Vector as a (x, y) tuple
    """
    def tuple(self):
        return ((self.x, self.y))

    """
    Returns the angle of the Vector (in Radians)
    """
    def getAngle(self):
        return math.atan2(self.y, self.x)

    """
    Returns the magnitude ("length") of this Vector
    """
    def getMagnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    """
    Returns a copy of this Vector, with specified magnitude
    """
    def setMagnitude(self, new):
        cur = self.getMagnitude()
        x = self.x * new / cur
        y = self.y * new / cur
        return Vector(x, y)

    """
    Returns a random Vector of length 1
    """
    def random():
        x = random.random()*2-1
        y = random.random()*2-1
        return Vector(x, y).setMagnitude(1)

    def __str__(self):
        out = "{" + str(self.x) + ": " + str(self.y) + "}"
        return out

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, other):
        x = y = 0
        if type(other) == Vector:
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = self.x * other
            y = self.y * other
        return Vector(x, y)

    def __truediv__(self, other):
        x = y = 0
        if type(other) == Vector:
            x = self.x / other.x
            y = self.y / other.y
        else:
            x = self.x / other
            y = self.y / other
        return Vector(x, y)
