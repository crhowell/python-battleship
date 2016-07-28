class Player:

    def __init__(self, name):
        self.name = name

    def prompt_for(self, prompt='fire at'):
        return input('{}: {} > '.format(self.name, prompt)).upper()

    def move(self):
        return self.prompt_for()

    def __str__(self):
        return '{}'.format(self.name)
