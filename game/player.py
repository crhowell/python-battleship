class Player:

    def __init__(self, name):
        self.name = name

    def prompt_for(self, prompt='fire at'):
        """Display prompt and return input, uppercased.

        Keyword arguments:
        prompt -- a string to be displayed with input.
        """
        return input('{}: {} > '.format(self.name, prompt)).upper().strip()

    def move(self):
        """Display and return prompt_for() using its default"""
        return self.prompt_for()

    def __str__(self):
        return '{}'.format(self.name)
