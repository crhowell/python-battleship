class Ship:

    def __init__(self, name='Ship', size=1):
        self.name = name
        self.size = size
        self.destroyed = False

    def __str__(self):
        return '{}'.format(self.name)
