class Vector():

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def add(self, other_vector):
        self.y += other_vector.y
        self.x += other_vector.x
