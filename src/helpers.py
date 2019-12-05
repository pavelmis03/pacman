class Vec:
    def __init__(self, x=0, y=0):
        if type(x) == type((0, 1)):  # tuple
            self.x = int(x[0])
            self.y = int(x[1])
        else:
            self.x = int(x)
            self.y = int(y)

    def __repr__(self):
        return '[Vec] | X: {}, Y: {}'.format(self.x, self.y)

    def __getitem__(self, item):
        if item in ['0', 0, 'x']:
            return self.x
        if item in ['1', 1, 'y']:
            return self.y

    def __mul__(self, other):
        if type(other) == type(Vec(0, 1)):  # Vec
            return Vec(self.x * other.x, self.y * other.y)
        elif type(other) == type((0, 1)):  # Tuple
            return Vec(self.x * other[0], self.y * other[1])
        elif type(other) in [type(0.1), type(1)]:  # Float/Int
            return Vec(self.x * other, self.y * other)

    def __add__(self, other):
        if type(other) == type(Vec(0, 1)):  # Vec
            return Vec(self.x + other.x, self.y + other.y)
        elif type(other) == type((0, 1)):  # Tuple
            return Vec(self.x + other[0], self.y + other[1])
        elif type(other) in [type(0.1), type(1)]:  # Float/Int
            return Vec(self.x + other, self.y + other)

    def __eq__(self, other):
        if type(other) == type(Vec(0, 1)):  # Vec
            return self.x == other.x and self.y == other.y
        elif type(other) == type((0, 1)):  # Tuple
            return self.x == other[0] and self.y == other[1]

    def dist(self, other):
        if type(other) == type(Vec(0, 1)):  # Vec
            return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        elif type(other) == type((0, 1)):  # Tuple
            return ((self.x - other[0])**2 + (self.y - other[1])**2)**0.5