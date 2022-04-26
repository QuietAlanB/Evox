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
                if type(other) == int:
                        return Vector2(self.x * other, self.y * other)
                elif type(other) == Vector2:
                        return Vector2(self.x * other.x, self.y * other.y)

        def __truediv__(self, other):
                return Vector2(self.x / other, self.y / other)

        def __abs__(self):
                return Vector2(abs(self.x), abs(self.y))

        def __str__(self):
                return f"({self.x}, {self.y})"


        def __eq__(self, other):
                if other == None:
                        return False

                if self.x == other.x and self.y == other.y:
                        return True
                return False


        def dot(self, other):
                return self.x * other.x + self.y * other.y

        def hadamard(self, other):
                return Vector2(self.x * other.x, self.y * other.y)

        def magnitude(self):
                return math.sqrt( self.dot(self, self) )

        def normalized(self):
                return self / self.magnitude()