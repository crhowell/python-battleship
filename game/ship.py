class Ship:

    def __init__(self, name='Ship', size=1):
        self.name = name
        self.size = size
        self.hits_taken = 0
        self.pos = []
        self.angle = None
        self.destroyed = False

    def hit(self):
        self.hits_taken += 1
        if self.hits_taken >= self.size:
            self.destroyed = True

    def is_sunk(self):
        return True if self.hits_taken >= self.size else False

    def set_pos(self, pos):
        self.pos = pos

    def set_angle(self, angle):
        self.angle = angle

    def __str__(self):
        return '{}'.format(self.name)
