class Point:
    def __init__(self, x=0, y=0):
        if type(x) == type((0, 1)):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return 'Point: X{}, Y{}'.format(self.x, self.y)

    def __getitem__(self, item):
        if item in ['0', 0, 'x']:
            return self.x
        if item in ['1', 1, 'y']:
            return self.y
