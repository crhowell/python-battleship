class Player:

    def __init__(self, name):
        self.name = name

    def move(self):
        return input('{}: fire at > '.format(self.name)).upper()

    def __str__(self):
        return '{}'.format(self.name)
