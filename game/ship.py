class Ship:

    def __init__(self, name='Ship', size=1):
        self.name = name
        self.size = size
        self.hits_taken = 0
        self.pos = []
        self.angle = None
        self.destroyed = False

    def hit(self):
        """Increment hit on ship by 1.
        Set destroyed flag if hit exceeds size.
        """
        self.hits_taken += 1
        if self.hits_taken >= self.size:
            self.destroyed = True

    def is_sunk(self):
        """Return True, if ship more or equal hits as its size."""
        return True if self.hits_taken >= self.size else False

    def set_pos(self, pos):
        """Sets a list of ship grid locations.

        Keyword arguments:
        pos -- list of grid locations. ex ['A1, B1, C1']
        """
        self.pos = pos

    def set_angle(self, angle):
        """Sets the ships H or V facing angle.

        Keyword arguments:
        angle -- 1 character (H)orizontal or (V)ertical
        """
        self.angle = angle

    def __str__(self):
        return '{}'.format(self.name)
