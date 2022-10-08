import math

class Vector2:
        def __init__(self, x, y):
                self.x = x
                self.y = y

        def __add__(self, other):
                return Vector2(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
                return Vector2(self.x - other.x, self.y - other.y)

        def __mul__(self, other):
                if (type(other) == Vector2):
                        return Vector2(self.x * other.x, self.y * other.y)     
                return Vector2(self.x * other, self.y * other)


        def __truediv__(self, other):
                if (type(other) == Vector2):
                        return Vector2(self.x / other.x, self.y / other.y)     
                return Vector2(self.x / other, self.y / other)

        def __abs__(self):
                return Vector2(abs(self.x), abs(self.y))

        def __str__(self):
                return f"({self.x}, {self.y})"

        def __eq__(self, other):
                return (self.x == other.x and self.y == other.y)


def dot(a, b):
        return a.x * b.x + a.y * b.y

def hadamard(a, b):
        return Vector2(a.x * b.x, a.y * b.y)

def sqrMagnitude(v):
        return dot(v, v)

def magnitude(v):
        return math.sqrt(sqrMagnitude(v))

def normalized(v):
        return v / magnitude(v)

def distance(a, b):
        return math.sqrt(abs(b.x - a.x) ** 2 + abs(b.y - a.y) ** 2)