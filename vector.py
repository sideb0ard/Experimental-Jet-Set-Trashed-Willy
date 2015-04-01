from math import sqrt


class Vector():

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def add(self, other_vect):
        if self.y < 0:
            self.y -= other_vect.y
        else:
            self.y += other_vect.y
        if self.x < 0:
            self.x -= other_vect.x
        else:
            self.x += other_vect.x

    def sub(self, other_vect):
        self.y -= other_vect.y
        self.x -= other_vect.x

    def mult(self, n):
        self.y *= n
        self.x *= n

    def div(self, n):
        self.y /= n
        self.x /= n

    def mag(self):  # length, basically - Pythagorean Theorem
        return sqrt((self.y * self.y) + (self.x * self.x))

    def normalize(self):
        m = self.mag()
        if m != 0:
            self.div(m)

    def limit(self, max):
        if self.mag() > max:
            self.normalize()
            self.mult(max)
